import sys
import time
from pathlib import Path
import torch
import argparse
import numpy as np
import random
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, LLVM_PASSES, MACRO_ACTIONS, CLANG, get_benchmark_paths
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

NUM_MACROS = len(MACRO_ACTIONS)

def run_baseline(source_path, level, metrics_collector, executor, iterations=20):
    """Compiles the source to IR with the specified level and measures runtime."""
    temp_ir = executor.work_dir / f"{level}_baseline_{Path(source_path).stem}.ll"
    cmd = [str(CLANG), f"-{level}", "-S", "-emit-llvm", str(source_path), "-o", str(temp_ir), "-Wno-everything"]
    subprocess.run(cmd, capture_output=True)
    
    if temp_ir.exists():
        return metrics_collector.measure_runtime(str(temp_ir), iterations=iterations)
    return None

def evaluate_checkpoints(args):
    checkpoints = args.checkpoints.split(',')
    print(f"\n[EVAL] Comparing {len(checkpoints)} checkpoints across {args.num_benchmarks} benchmarks...")
    
    metrics_collector = MetricsCollector()
    benchmarks = get_benchmark_paths()
    test_benchmarks = random.sample(benchmarks, min(len(benchmarks), args.num_benchmarks))
    
    # Store results: {checkpoint_name: {'o2': [speedup_1, ...], 'o3': [speedup_1, ...]}}
    results = {ckpt: {'o2': [], 'o3': []} for ckpt in checkpoints}
    
    # Load all models into memory to save reloading time per benchmark
    agents = {}
    for ckpt in checkpoints:
        agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
        agent.load_state_dict(torch.load(ckpt, map_location='cpu', weights_only=True))
        agent.eval()
        agents[ckpt] = agent

    # Header
    header = f"{'Benchmark':<30} | {'-O2 (ms)':<8} | {'-O3 (ms)':<8}"
    for ckpt in checkpoints:
        name = Path(ckpt).stem.replace('hrl_stencil_production_hour_', '')
        header += f" | {name:<10}"
    print("\n" + header)
    print("-" * len(header))
    
    for b_path in test_benchmarks:
        try:
            env = CompilerOptEnv([b_path], max_steps=args.max_steps, reward_mode=RewardMode.HACKABLE)
            env.reset()
            
            # Baselines
            o2_runtime = run_baseline(b_path, "O2", metrics_collector, env.executor, iterations=args.repeats)
            o3_runtime = run_baseline(b_path, "O3", metrics_collector, env.executor, iterations=args.repeats)
            
            if o2_runtime is None or o2_runtime <= 0 or o3_runtime is None or o3_runtime <= 0:
                continue
                
            row_str = f"{Path(b_path).name[:30]:<30} | {o2_runtime:8.2f} | {o3_runtime:8.2f}"
            
            # Test each agent
            for ckpt in checkpoints:
                env.reset(options={"ir_path": b_path})
                agent = agents[ckpt]
                
                terminated = False
                episode_steps = 0
                recent_macros = []
                while not terminated and episode_steps < args.max_steps:
                    graph = env.get_observation_graph()
                    if graph is None: break
                    
                    x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                    
                    with torch.no_grad():
                        macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
                        
                        # --- HARSH ACTION THROTTLING (Ferrari Upgrade) ---
                        if len(recent_macros) >= 2:
                            last_2 = recent_macros[-2:]
                            if all(m == last_2[0] for m in last_2):
                                macro_probs[0, last_2[0]] *= 0.1
                            
                            if len(recent_macros) >= 3:
                                last_3 = recent_macros[-3:]
                                if all(m == last_3[0] for m in last_3):
                                    macro_probs[0, last_3[0]] = 0.0
                        
                        macro_probs = macro_probs / (macro_probs.sum() + 1e-8)
                        m_idx = torch.argmax(macro_probs, dim=-1)
                        
                        recent_macros.append(m_idx.item())
                        if len(recent_macros) > 5: recent_macros.pop(0)

                        if m_idx.item() == NUM_MACROS - 1:
                            terminated = True
                            break
                            
                        u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx)
                        u_idx = torch.argmax(u_logits, dim=-1)
                        
                    base_seq = MACRO_ACTIONS[m_idx.item()]
                    final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                    pipeline = [f"module({','.join(final_seq)})"]
                    
                    res = env.executor.apply_passes(env.current_ir_path, pipeline)
                    if not res.success:
                        terminated = True
                    else:
                        env.current_ir_path = res.output_path
                        episode_steps += 1
                
                agent_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=args.repeats)
                
                if agent_runtime > 0:
                    s_o2 = o2_runtime / agent_runtime
                    s_o3 = o3_runtime / agent_runtime
                    results[ckpt]['o2'].append(s_o2)
                    results[ckpt]['o3'].append(s_o3)
                    row_str += f" | {agent_runtime:6.2f}ms({s_o3:4.2f}x)"
                else:
                    row_str += f" | {'ERR':<10}"
            
            print(row_str)
            env.close()
            
        except Exception as e:
            print(f"Error evaluating {b_path}: {e}")

    # Summary
    print("\n" + "=" * len(header))
    print("FINAL SUMMARY (Mean Speedup)")
    print("-" * 50)
    for ckpt in checkpoints:
        name = Path(ckpt).stem.replace('hrl_stencil_production_hour_', '')
        if results[ckpt]['o2']:
            m_o2 = np.mean(results[ckpt]['o2'])
            m_o3 = np.mean(results[ckpt]['o3'])
            wins_o3 = len([s for s in results[ckpt]['o3'] if s > 1.01])
            print(f"Checkpoint {name:<8} : vO2={m_o2:.3f}x | vO3={m_o3:.3f}x  ({wins_o3}/{len(results[ckpt]['o3'])} O3-Wins)")
        else:
            print(f"Checkpoint {name:<8} : No valid data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints", type=str, required=True, help="Comma-separated list of checkpoints")
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--num_benchmarks", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--max_steps", type=int, default=25)
    args = parser.parse_args()
    evaluate_checkpoints(args)
