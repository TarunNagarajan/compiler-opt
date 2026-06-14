import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple
from enum import Enum
import random
import time
import shutil

from ..config import LLVM_PASSES, FEATURE_DIM
from ..features import extract_ir_graph
from ..models.graph_encoder_v6 import create_v6_encoder
from ..passes import PassExecutor, MetricsCollector
from ..features.ir_parser import IRParser
import torch
import numpy as np
from ..actions import MACRO_ACTIONS


class RewardMode(Enum):
    HACKABLE = "hackable"
    SECURE = "secure"
    PERFORMANCE = "performance"
    SIZE = "size"
    SECURITY = "security"
    COMPILATION_SPEED = "compilation_speed"
    CONSTRAINED = "constrained"
    SPEED = "speed"


class CompilerOptEnv(gym.Env):
    
    metadata = {"render_modes": ["human"]}
    
    
    def __init__(
        self,
        benchmark_paths: List[str],
        max_steps: int = 10,
        reward_mode: RewardMode = RewardMode.HACKABLE,
        collect_speed_metrics: bool = False,
        runtime_measure_runs: int = 3,
        runtime_measure_loop_count: int = 100,
        runtime_measure_timeout_seconds: float = 20.0,
        runtime_measure_aggregation: str = "median",
        runtime_target_rel_ci95_pct: float = 2.5,
        runtime_max_measure_runs: int = 5,
        render_mode: Optional[str] = None
    ):
        super().__init__()
        
        # Store original paths for clean resets
        self.original_benchmark_paths = [Path(p) for p in benchmark_paths]
        self.benchmark_paths = self.original_benchmark_paths.copy()
                
        self.max_steps = max_steps
        self.reward_mode = reward_mode
        self.collect_speed_metrics = collect_speed_metrics
        self.runtime_measure_runs = max(1, int(runtime_measure_runs))
        self.runtime_measure_loop_count = max(1, int(runtime_measure_loop_count))
        self.runtime_measure_timeout_seconds = max(1.0, float(runtime_measure_timeout_seconds))
        self.runtime_measure_aggregation = str(runtime_measure_aggregation).strip().lower()
        self.runtime_target_rel_ci95_pct = max(0.1, float(runtime_target_rel_ci95_pct))
        self.runtime_max_measure_runs = max(self.runtime_measure_runs, int(runtime_max_measure_runs))
        self.render_mode = render_mode
        
        self.num_atomic_passes = len(LLVM_PASSES)
        self.num_macro_actions = len(MACRO_ACTIONS)
        self.action_space = spaces.Discrete(self.num_atomic_passes + self.num_macro_actions)
        
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(FEATURE_DIM,), dtype=np.float32
        )
        
        # Executor and Metrics
        self.executor = PassExecutor()
        self.metrics = MetricsCollector()
        
        # Graph Encoder (initialized here for now, acts as random projection or pre-trained)
        self.gnn = create_v6_encoder(output_dim=FEATURE_DIM)
        # In the future, load pretrained weights:
        # self.gnn.load_state_dict(torch.load("gnn_pretrained.pt"))
        
        self.current_ir_path: Optional[str] = None
        self.original_ir_path: Optional[str] = None
        self.current_step: int = 0
        self.applied_passes: List[str] = []
        self.initial_metrics: Optional[dict] = None
        self.prev_size: int = 0
        self.total_compile_time: float = 0.0
        self.episode_stats: dict = {}
        self.pass_history: list = []  # Track last N actions for state augmentation
        self.HISTORY_LEN = 5
        self._notified_large_files = set() # V7.5: Persistence across resets

    def _should_measure_speed_metrics(self) -> bool:
        return self.reward_mode == RewardMode.SPEED or self.collect_speed_metrics
    
    def _get_observation(self, ir_path: str) -> np.ndarray:
        try:
            # 1. Extract Graph (v5: supports selective windowing)
            data = extract_ir_graph(ir_path, focus_functions=getattr(self, 'focus_functions', None))
            
            # 2. Augment with pass history
            # Normalize action IDs to [0, 1] range
            total_actions = self.num_atomic_passes + self.num_macro_actions
            history = list(self.pass_history[-self.HISTORY_LEN:])
            # Pad to fixed length
            while len(history) < self.HISTORY_LEN:
                history.insert(0, -1)  # -1 = no action yet
            history_vec = torch.tensor(
                [(h + 1) / (total_actions + 1) for h in history],
                dtype=torch.float
            )
            data.pass_history = history_vec.unsqueeze(0)  # [1, HISTORY_LEN]
            
            # 3. Augment with V8 Global Scale Signal
            current_total_instr = self.metrics.count_instructions(ir_path)
            data.total_nodes = torch.tensor([current_total_instr], dtype=torch.float)
            
            self.last_graph_data = data  # Cache for world model
            
            # 4. Encode to Fixed Vector
            with torch.no_grad():
                embedding = self.gnn(
                    data.x, 
                    data.edge_index, 
                    data.edge_attr, 
                    batch=getattr(data, 'batch', None),
                    block_map=getattr(data, 'block_map', None)
                )
                
            return embedding.squeeze(0).numpy()
        except Exception as e:
            print(f"[ENV] Graph Extractor Failed for {ir_path}: {e}")
            self.last_graph_data = None
            return np.zeros(FEATURE_DIM, dtype=np.float32)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        
        skip_canon = options.get("skip_canonicalization", False) if options else False
        
        # LEAK PROOF: Always cleanup before starting fresh
        self.executor.cleanup()
        self.executor = PassExecutor() # New fresh workspace
        
        if options and "ir_path" in options:
            # Force specific path, no retry logic if this fails (user intent)
            source_path = Path(options["ir_path"])
            is_forced = True
        else:
            is_forced = False
            
        for attempt in range(100):
            if not is_forced:
                source_path = random.choice(self.benchmark_paths)
            
            self.current_benchmark_path = source_path
            # LEAK PROOF: Ensure we are starting from a clean IR
            try:
                if source_path.suffix in ['.c', '.cpp']:
                    from ..passes.pass_executor import compile_to_ir
                    temp_ir = self.executor.work_dir / f"clean_start_{source_path.stem}.ll"
                    success, ir_path = compile_to_ir(str(source_path), output_path=str(temp_ir))
                    if not success:
                        if is_forced:
                            raise RuntimeError(f"[AGENT] Critical: Failed to compile {source_path}. Error: {ir_path}")
                        print(f"[ENV] Skipping broken benchmark {source_path.name} Reason: {ir_path}")
                        continue
                    self.original_ir_path = str(temp_ir)
                else:
                    # Copy original .ll to temp workspace to prevent cross-episode pollution
                    temp_ir = self.executor.work_dir / f"reset_{source_path.name}"
                    shutil.copy(source_path, temp_ir)
                    self.original_ir_path = str(temp_ir)
                
                # If we got here, success
                break
            except Exception as e:
                if is_forced:
                    raise e
                print(f"[ENV] Error loading {source_path.name}: {e}")
                continue
        else:
            raise RuntimeError("[ENV] Failed to find a compilable benchmark after 100 attempts.")
            
        self.current_ir_path = self.original_ir_path
        self.current_step = 0
        self.applied_passes = []
        self.total_compile_time = 0.0
        self.pass_history = []  # Reset pass history for new episode

        # SELECTIVE WINDOWING: If file is large, pick multiple focus functions
        self.focus_functions = None
        if source_path.stat().st_size > 100 * 1024: # 100KB threshold
            try:
                parser = IRParser(self.current_ir_path or str(temp_ir))
                stats = parser.parse()
                if stats.functions:
                    # Multi-Hotspot Selection: Top-N sorted by complexity
                    all_funcs = []
                    for f in stats.functions:
                        blocks = stats.function_details.get(f, {}).get('blocks', 0)
                        all_funcs.append({'name': f, 'blocks': blocks})
                    
                    # Sort by blocks descending
                    all_funcs.sort(key=lambda x: x['blocks'], reverse=True)
                    
                    self.focus_functions = []
                    cumulative_blocks = 0
                    MIN_FUNCS = 2 
                    MAX_BLOCK_BUDGET = 1024
                    HARD_BLOCK_CAP = 2500 # Prevent Segfaults on ultra-complex industrial kernels like SQLite dispatcher
                    
                    for i, f_info in enumerate(all_funcs):
                        # V8.1 Dynamic Foveation Logic:
                        # 1. Skip functions that are SO large they would crash the GNN (e.g. 6k blocks)
                        if f_info['blocks'] > HARD_BLOCK_CAP:
                            continue
                            
                        # 2. Add until we hit MAX_BLOCK_BUDGET or MIN_FUNCS
                        if i < MIN_FUNCS or (cumulative_blocks + f_info['blocks'] <= MAX_BLOCK_BUDGET):
                            # Final safety check for the collective budget
                            if cumulative_blocks + f_info['blocks'] > HARD_BLOCK_CAP:
                                break
                            self.focus_functions.append(f_info['name'])
                            cumulative_blocks += f_info['blocks']
                        else:
                            # 3. If we can't fit more big ones, try to fit smaller ones later in the list
                            if f_info['blocks'] < (MAX_BLOCK_BUDGET // 4):
                                if cumulative_blocks + f_info['blocks'] <= MAX_BLOCK_BUDGET:
                                    self.focus_functions.append(f_info['name'])
                                    cumulative_blocks += f_info['blocks']
                                    
                    # V8.2 Fallback: If ALL functions are too large, just take the first one but it will be handled at Block-Level
                    if not self.focus_functions and all_funcs:
                        self.focus_functions = [all_funcs[0]['name']]
                        cumulative_blocks = all_funcs[0]['blocks']
                    
                    # V7.5 Tweak: Only print detection once per unique benchmark to silence log noise
                    file_id = str(source_path.absolute())
                    if file_id not in self._notified_large_files:
                        print(f"[ENV] Large file detected. Focusing on {len(self.focus_functions)} functions: {self.focus_functions} (Total Blocks: {cumulative_blocks})")
                        self._notified_large_files.add(file_id)
            except Exception as e:
                print(f"[ENV] Failed to select focus functions: {e}")

        # --- MANDATORY CANONICALIZATION (Real-World Readiness) ---
        # We apply standard cleanup passes to ensure the agent starts with a normalized graph.
        # This prevents the agent from being overwhelmed by frontend-specific IR mess.
        if not skip_canon:
            canon_pipeline = ["module(function(sroa),function(mem2reg),function(simplifycfg),function(instcombine<no-verify-fixpoint>),function(tailcallelim))"]
            res = self.executor.apply_passes(self.current_ir_path, canon_pipeline)
            if res.success:
                self.current_ir_path = res.output_path
                self.original_ir_path = res.output_path # Benchmark baseline is now the clean IR
        
        initial_instr = self.metrics.count_instructions(self.current_ir_path)
        initial_size = self.metrics.get_code_size(self.current_ir_path)
        
        measure_speed_metrics = self._should_measure_speed_metrics()
        # Performance optimization: skip heavy runtime measurement when not requested.
        initial_runtime = 0.0
        self.o3_runtime = 0.0
        self.o3_instr = 0
        self.o3_energy = 0.0
        if measure_speed_metrics:
            initial_runtime = self.metrics.measure_runtime(
                self.current_ir_path,
                iterations=self.runtime_measure_runs,
                loop_count=self.runtime_measure_loop_count,
                timeout_seconds=self.runtime_measure_timeout_seconds,
                aggregation=self.runtime_measure_aggregation,
                max_iterations=self.runtime_max_measure_runs,
                target_rel_ci95_pct=self.runtime_target_rel_ci95_pct,
            )
            initial_runtime_stats = self.metrics.get_last_runtime_stats()
            # --- O3 BASELINE: Measure the target to beat ---
            from ..config import CLANG, CLANG_CXX
            import subprocess
            
            # V7.3 Fix: Use C++ compiler for C++ source files
            baseline_compiler = CLANG
            if "_cpp_gen_" in source_path.name or source_path.suffix == ".cpp":
                baseline_compiler = CLANG_CXX
                
            temp_o3_ir = self.executor.work_dir / "o3_baseline.ll"
            cmd = [str(baseline_compiler), "-O3", "-S", "-emit-llvm", str(source_path), "-o", str(temp_o3_ir), "-Wno-everything"]
            subprocess.run(cmd, capture_output=True)
            if temp_o3_ir.exists():
                self.o3_runtime = self.metrics.measure_runtime(
                    str(temp_o3_ir),
                    iterations=self.runtime_measure_runs,
                    loop_count=self.runtime_measure_loop_count,
                    timeout_seconds=self.runtime_measure_timeout_seconds,
                    aggregation=self.runtime_measure_aggregation,
                    max_iterations=self.runtime_max_measure_runs,
                    target_rel_ci95_pct=self.runtime_target_rel_ci95_pct,
                )
                self.o3_runtime_stats = self.metrics.get_last_runtime_stats()
                self.o3_instr = self.metrics.count_instructions(str(temp_o3_ir))
                self.o3_energy = self.metrics.measure_energy(str(temp_o3_ir), runtime_cycles=self.o3_runtime)
            else:
                # Do not fabricate O3 numbers; leave as unknown when baseline build fails.
                self.o3_runtime = 0.0
                self.o3_runtime_stats = self.metrics.get_last_runtime_stats()
                self.o3_instr = 0
                self.o3_energy = 0.0
        else:
            initial_runtime_stats = self.metrics.get_last_runtime_stats()
            self.o3_runtime_stats = self.metrics.get_last_runtime_stats()
        
        try:
            initial_parser = IRParser(self.current_ir_path)
            initial_stats = initial_parser.parse()
            initial_complexity = initial_stats.cyclomatic_complexity
            initial_loops = initial_stats.num_loops
            initial_calls = initial_stats.num_calls
            initial_blocks = initial_stats.num_basic_blocks
            initial_instr_counts = initial_stats.instruction_counts
            initial_loads = initial_instr_counts.get("load", 0)
            initial_stores = initial_instr_counts.get("store", 0)
            initial_allocas = initial_instr_counts.get("alloca", 0)
            initial_branches = initial_instr_counts.get("br", 0) + initial_instr_counts.get("switch", 0)
        except Exception as e:
            print(f"[ENV] IRParser failed at reset for {self.current_ir_path}: {e}")
            initial_complexity = 0
            initial_loops = 0
            initial_calls = 0
            initial_blocks = 0
            initial_loads = 0
            initial_stores = 0
            initial_allocas = 0
            initial_branches = 0

        self.initial_metrics = {
            'instructions': initial_instr,
            'size': initial_size,
            'complexity': initial_complexity,
            'loops': initial_loops,
            'calls': initial_calls,
            'blocks': initial_blocks,
            'loads': initial_loads,
            'stores': initial_stores,
            'allocas': initial_allocas,
            'branches': initial_branches,
            'runtime': initial_runtime
        }
        # Runtime/energy measurement is expensive and can hang on non-standalone
        # benchmarks; keep it enabled only when requested.
        if measure_speed_metrics:
            self.initial_energy = self.metrics.measure_energy(self.current_ir_path, runtime_cycles=initial_runtime)
        else:
            self.initial_energy = 0.0
        self.prev_size = initial_size
        self.prev_runtime = initial_runtime
        self.prev_runtime_stats = dict(initial_runtime_stats)
        self.prev_energy = self.initial_energy
        self.last_graph_data = None # Cache for world model
        
        self.episode_stats = {
            'correctness_violations': 0,
            'size_increases': 0,
            'repeated_passes': 0,
            'total_size_delta': 0
        }
        
        observation = self._get_observation(self.current_ir_path)
        
        info = {
            "ir_path": self.current_ir_path,
            "initial_instructions": initial_instr,
            "initial_size": initial_size,
            "initial_complexity": self.initial_metrics['complexity'],
            "initial_loads": self.initial_metrics['loads'],
            "initial_stores": self.initial_metrics['stores'],
            "initial_allocas": self.initial_metrics['allocas'],
            "initial_branches": self.initial_metrics['branches'],
            "initial_runtime": initial_runtime,
            "initial_energy": self.initial_energy,
            "o3_runtime": self.o3_runtime,
            "o3_energy": getattr(self, 'o3_energy', 0.0),
            "o3_instructions": self.o3_instr,
            "runtime_measure_runs": self.runtime_measure_runs,
            "runtime_measure_loop_count": self.runtime_measure_loop_count,
            "runtime_measure_timeout_seconds": self.runtime_measure_timeout_seconds,
            "runtime_measure_aggregation": self.runtime_measure_aggregation,
            "runtime_target_rel_ci95_pct": self.runtime_target_rel_ci95_pct,
            "runtime_max_measure_runs": self.runtime_max_measure_runs,
            "runtime_initial_rel_ci95_pct": float(self.prev_runtime_stats.get('relative_ci95_pct', 100.0)),
            "reward_mode": self.reward_mode.value
        }
        
        return observation, info

    def get_observation_graph(self) -> Optional['Data']:
        """Returns the full PyG graph of the last observation."""
        return self.last_graph_data

    def step(self, action: int, custom_passes: list = None) -> Tuple[np.ndarray, float, bool, bool, dict]:
        if custom_passes is not None:
            pass_seq = custom_passes
            pass_name = f"refined_macro({';'.join(pass_seq)})"
        elif action < self.num_atomic_passes:
            pass_seq = [LLVM_PASSES[action]]
            pass_name = LLVM_PASSES[action]
        else:
            macro_idx = action - self.num_atomic_passes
            pass_seq = MACRO_ACTIONS[macro_idx]
            pass_name = f"macro({';'.join(pass_seq)})"
            
        start_time = time.perf_counter()
        result = self.executor.apply_passes(self.current_ir_path, pass_seq)
        compile_time = (time.perf_counter() - start_time) * 1000
        self.total_compile_time += compile_time
        
        self.current_step += 1
        
        is_repeated = len(self.applied_passes) > 0 and self.applied_passes[-1] == pass_name
        if is_repeated:
            self.episode_stats['repeated_passes'] += 1
        
        self.applied_passes.append(pass_name)
        self.pass_history.append(action)  # Track for state augmentation
        
        if not result.success:
            # Pass failed, state unchanged
            current_instr = self.metrics.count_instructions(self.current_ir_path)
            current_size = self.metrics.get_code_size(self.current_ir_path)
            observation = self._get_observation(self.current_ir_path)
            
            info = {
                "pass_applied": pass_name,
                "instructions_before": current_instr,
                "instructions_after": current_instr,
                "size_before": current_size,
                "size_after": current_size,
                "compile_time_ms": compile_time,
                "is_repeated": is_repeated,
                "total_passes": len(self.applied_passes),
                "passes": self.applied_passes.copy(),
                "error": result.error_message
            }
            if self.reward_mode == RewardMode.CONSTRAINED:
                 info["constraints"] = {
                    "size_increase_pct": 0.0,
                    "compile_time_ms": compile_time
                }
            
            return observation, -1.0, True, False, info
        
        
        prev_instructions = self.metrics.count_instructions(self.current_ir_path)
        runtime_before = self.prev_runtime
        try:
            prev_parser = IRParser(self.current_ir_path)
            prev_stats = prev_parser.parse()
            prev_complexity = prev_stats.cyclomatic_complexity
            prev_loops = prev_stats.num_loops
            prev_calls = prev_stats.num_calls
            prev_blocks = prev_stats.num_basic_blocks
            prev_instr_counts = prev_stats.instruction_counts
            prev_loads = prev_instr_counts.get("load", 0)
            prev_stores = prev_instr_counts.get("store", 0)
            prev_allocas = prev_instr_counts.get("alloca", 0)
            prev_branches = prev_instr_counts.get("br", 0) + prev_instr_counts.get("switch", 0)
        except Exception:
            prev_complexity = 0
            prev_loops = 0
            prev_calls = 0
            prev_blocks = 0
            prev_loads = 0
            prev_stores = 0
            prev_allocas = 0
            prev_branches = 0

        self.current_ir_path = result.output_path
        new_instructions = self.metrics.count_instructions(self.current_ir_path)
        new_size = self.metrics.get_code_size(self.current_ir_path)
        
        measure_speed_metrics = self._should_measure_speed_metrics()
        # Performance optimization: skip heavy runtime measurement when not requested.
        new_runtime = 0.0
        new_energy = 0.0
        runtime_before_stats = dict(getattr(self, 'prev_runtime_stats', {}))
        new_runtime_stats = self.metrics.get_last_runtime_stats()
        if measure_speed_metrics:
            new_runtime = self.metrics.measure_runtime(
                self.current_ir_path,
                iterations=self.runtime_measure_runs,
                loop_count=self.runtime_measure_loop_count,
                timeout_seconds=self.runtime_measure_timeout_seconds,
                aggregation=self.runtime_measure_aggregation,
                max_iterations=self.runtime_max_measure_runs,
                target_rel_ci95_pct=self.runtime_target_rel_ci95_pct,
            )
            new_runtime_stats = self.metrics.get_last_runtime_stats()
            new_energy = self.metrics.measure_energy(self.current_ir_path, runtime_cycles=new_runtime)

        runtime_gain_raw_pct = 0.0
        runtime_gain_noise_floor_pct = 0.0
        runtime_gain_denoised_pct = 0.0
        runtime_gain_significant = False
        runtime_confidence = 0.0
        if runtime_before > 0 and new_runtime > 0:
            runtime_gain_raw_pct = (runtime_before - new_runtime) / max(runtime_before, 1e-6) * 100.0
            runtime_gain_noise_floor_pct = float(runtime_before_stats.get('relative_ci95_pct', 100.0)) + float(new_runtime_stats.get('relative_ci95_pct', 100.0))
            runtime_gain_significant = abs(runtime_gain_raw_pct) > runtime_gain_noise_floor_pct
            runtime_gain_denoised_pct = np.sign(runtime_gain_raw_pct) * max(0.0, abs(runtime_gain_raw_pct) - runtime_gain_noise_floor_pct)
            runtime_confidence = min(1.0, abs(runtime_gain_raw_pct) / max(abs(runtime_gain_raw_pct) + runtime_gain_noise_floor_pct, 1e-6))
        
        try:
            new_parser = IRParser(self.current_ir_path)
            new_stats = new_parser.parse()
            new_complexity = new_stats.cyclomatic_complexity
            new_loops = new_stats.num_loops
            new_calls = new_stats.num_calls
            new_blocks = new_stats.num_basic_blocks
            new_instr_counts = new_stats.instruction_counts
            new_loads = new_instr_counts.get("load", 0)
            new_stores = new_instr_counts.get("store", 0)
            new_allocas = new_instr_counts.get("alloca", 0)
            new_branches = new_instr_counts.get("br", 0) + new_instr_counts.get("switch", 0)
        except Exception:
            new_complexity = 0
            new_loops = 0
            new_calls = 0
            new_blocks = 0
            new_loads = 0
            new_stores = 0
            new_allocas = 0
            new_branches = 0
        
        prev_size = self.prev_size
        prev_energy = self.prev_energy
        size_delta = new_size - prev_size
        self.episode_stats['total_size_delta'] += size_delta
        if size_delta > 0:
            self.episode_stats['size_increases'] += 1
        
        reward = 0.0
        if self.reward_mode == RewardMode.SPEED:
            # Reward is based on step-to-step improvement
            # We want to encourage making the code faster than it was BEFORE this action
            # Positive = action improved runtime, Negative = action made it slower
            if runtime_before > 0 and new_runtime > 0:
                reward = runtime_gain_denoised_pct / 100.0
            else:
                reward = 0.0

            # Small step cost to encourage efficiency
            reward -= 0.005
        elif self.reward_mode in [RewardMode.HACKABLE, RewardMode.PERFORMANCE]:
            reward = self._compute_hackable_reward(prev_instructions, new_instructions)
            if self.reward_mode == RewardMode.PERFORMANCE:
                # Add penalty for extreme slowdowns to distinguish from HACKABLE
                time_penalty = min(compile_time / 2000.0, 0.5)
                reward -= time_penalty
        elif self.reward_mode == RewardMode.SECURE:
            reward = self._compute_secure_reward(
                prev_instructions, new_instructions,
                prev_size, new_size,
                compile_time, is_repeated
            )
        elif self.reward_mode == RewardMode.SIZE:
            reward = self._compute_size_reward(prev_size, new_size)
        elif self.reward_mode == RewardMode.SECURITY:
            reward = self._compute_security_reward(
                prev_instructions, new_instructions,
                prev_size, new_size,
                compile_time
            )
        elif self.reward_mode == RewardMode.COMPILATION_SPEED:
            reward = self._compute_compilation_speed_reward(compile_time)
        elif self.reward_mode == RewardMode.CONSTRAINED:
            # Pure performance reward
            reward = self._compute_hackable_reward(prev_instructions, new_instructions)
            # Constraints are handled by the agent via info['constraints']
            
        self.prev_size = new_size
        self.prev_runtime = new_runtime
        self.prev_runtime_stats = dict(new_runtime_stats)
        self.prev_energy = new_energy
        
        terminated = self.current_step >= self.max_steps
        truncated = False
        
        observation = self._get_observation(self.current_ir_path)
        
        info = {
            "pass_applied": pass_name,
            "instructions_before": prev_instructions,
            "instructions_after": new_instructions,
            "complexity_before": prev_complexity,
            "complexity_after": new_complexity,
            "loops_before": prev_loops,
            "loops_after": new_loops,
            "calls_before": prev_calls,
            "calls_after": new_calls,
            "blocks_before": prev_blocks,
            "blocks_after": new_blocks,
            "loads_before": prev_loads,
            "loads_after": new_loads,
            "stores_before": prev_stores,
            "stores_after": new_stores,
            "allocas_before": prev_allocas,
            "allocas_after": new_allocas,
            "branches_before": prev_branches,
            "branches_after": new_branches,
            "runtime_before": runtime_before,
            "runtime_after": new_runtime,
            "runtime_before_rel_ci95_pct": float(runtime_before_stats.get('relative_ci95_pct', 100.0)),
            "runtime_after_rel_ci95_pct": float(new_runtime_stats.get('relative_ci95_pct', 100.0)),
            "runtime_before_cv_pct": float(runtime_before_stats.get('cv_pct', 100.0)),
            "runtime_after_cv_pct": float(new_runtime_stats.get('cv_pct', 100.0)),
            "runtime_before_samples": int(runtime_before_stats.get('sample_count', 0)),
            "runtime_after_samples": int(new_runtime_stats.get('sample_count', 0)),
            "runtime_gain_raw_pct": runtime_gain_raw_pct,
            "runtime_gain_noise_floor_pct": runtime_gain_noise_floor_pct,
            "runtime_gain_denoised_pct": runtime_gain_denoised_pct,
            "runtime_gain_significant": bool(runtime_gain_significant),
            "runtime_confidence": float(runtime_confidence),
            "energy_before": prev_energy,
            "energy_after": new_energy,
            "size_before": prev_size,
            "size_after": new_size,
            "compile_time_ms": compile_time,
            "is_repeated": is_repeated,
            "total_passes": len(self.applied_passes),
            "passes": self.applied_passes.copy(),
            "constraints": {
                "size_increase_pct": max(0, (new_size - prev_size) / max(prev_size, 1)),
                "compile_time_ms": compile_time
            }
        }
        
        if self.render_mode == "human":
            self._render_step(info)
        
        return observation, reward, terminated, truncated, info
    
    def _compute_hackable_reward(self, prev_instr: int, new_instr: int) -> float:
        if prev_instr > 0:
            return (prev_instr - new_instr) / prev_instr
        return 0.0
    
    def _compute_size_reward(self, prev_size: int, new_size: int) -> float:
        if prev_size > 0:
            # Reward size reduction, penalize increase
            return (prev_size - new_size) / prev_size
        return 0.0

    def _compute_security_reward(
        self,
        prev_instr: int,
        new_instr: int,
        prev_size: int,
        new_size: int,
        compile_time: float
    ) -> float:
        # Security agent prioritizes correctness and preservation of potential checks.
        # It penalizes aggressive code removal that might strip security bounds.
        instr_change = abs(prev_instr - new_instr) / max(prev_instr, 1)
        stability_reward = 1.0 - instr_change # High when change is minimal
        
        # Penalize slowdown but less than performance agent
        time_penalty = min(compile_time / 1000.0, 1.0) * 0.2
        
        return (stability_reward * 0.8) - time_penalty

    def _compute_compilation_speed_reward(self, compile_time_ms: float) -> float:
        # High reward for low compile time
        # Reward = 1 / (1 + time_in_seconds)
        time_sec = compile_time_ms / 1000.0
        return 1.0 / (1.0 + time_sec)

    def _compute_secure_reward(
        self,
        prev_instr: int,
        new_instr: int,
        prev_size: int,
        new_size: int,
        compile_time: float,
        is_repeated: bool
    ) -> float:
        instr_reward = (prev_instr - new_instr) / max(prev_instr, 1)
        size_ratio = (new_size - prev_size) / max(prev_size, 1)
        size_penalty = max(0, size_ratio) * 0.5
        time_penalty = min(compile_time / 1000.0, 1.0) * 0.1
        repetition_penalty = 0.2 if is_repeated else 0.0
        return instr_reward - size_penalty - time_penalty - repetition_penalty
    
    def _render_step(self, info: dict):
        print(f"[AGENT] Step {self.current_step}: {info['pass_applied']}...")
    
    def get_total_improvement(self) -> dict:
        current_instructions = self.metrics.count_instructions(self.current_ir_path)
        current_size = self.metrics.get_code_size(self.current_ir_path)
        initial_instructions = self.initial_metrics['instructions']
        initial_size = self.initial_metrics['size']
        
        instr_reduction = (initial_instructions - current_instructions) / max(initial_instructions, 1)
        size_change = (current_size - initial_size) / max(initial_size, 1)
        
        # Calculate diversity: unique passes / total passes
        unique_passes = len(set(self.applied_passes))
        total_passes = len(self.applied_passes)
        diversity = unique_passes / total_passes if total_passes > 0 else 0
        
        return {
            'reduction_pct': instr_reduction * 100,
            'size_change_pct': size_change * 100,
            'passes_applied': self.applied_passes,
            'total_compile_time_ms': self.total_compile_time,
            'pass_diversity': diversity,
            'episode_stats': self.episode_stats.copy()
        }
    
    def close(self):
        self.executor.cleanup()
