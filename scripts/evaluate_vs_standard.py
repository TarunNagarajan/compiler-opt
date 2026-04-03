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

def run_baseline(source_path, opt_level, metrics_collector, executor, iterations=20):
    """Compiles the source to IR with specified opt level and measures runtime."""
    print(f"  [DEBUG] Running -{opt_level} baseline...")
    temp_ir = executor.work_dir / f"{opt_level}_baseline_{Path(source_path).stem}.ll"
    cmd = [str(CLANG), f"-{opt_level}", "-S", "-emit-llvm", str(source_path), "-o", str(temp_ir), "-Wno-everything"]
    subprocess.run(cmd, capture_output=True)
    
    if temp_ir.exists():
        runtime = metrics_collector.measure_runtime(str(temp_ir), iterations=iterations)
        return runtime
    return None

def bootstrap_ci(data, n_iterations=1000, alpha=0.05):
    """Computes bootstrap confidence interval for the mean."""
    means = []
    n = len(data)
    if n == 0: return 0, 0
    for _ in range(n_iterations):
        resample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(resample))
    
    lower = np.percentile(means, (alpha/2) * 100)
    upper = np.percentile(means, (1 - alpha/2) * 100)
    return lower, upper

def evaluate_against_baselines(args):
    print(f"\n[EVAL] Loading HRL Agent: {args.checkpoint}...")
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    metrics_collector = MetricsCollector()
    
    benchmarks = get_benchmark_paths()
    if args.file:
        test_benchmarks = [args.file]
    else:
        # Sample benchmarks
        test_benchmarks = random.sample(benchmarks, min(len(benchmarks), args.num_benchmarks))
    
    print(f"Selected {len(test_benchmarks)} benchmarks for evaluation.")
        
    speedups_vs_o2 = []
    speedups_vs_o3 = []
    
    results_table = []
    
    for i, b_path in enumerate(test_benchmarks):
        print(f"\n[{i+1}/{len(test_benchmarks)}] Evaluating: {Path(b_path).name}...")
        try:
            # Use HACKABLE mode during setup to avoid redundant reset timings
            env = CompilerOptEnv([b_path], max_steps=args.max_steps, reward_mode=RewardMode.HACKABLE)
            obs, info = env.reset()
            
            # 1. Run -O2 Baseline
            o2_runtime = run_baseline(b_path, "O2", metrics_collector, env.executor, iterations=args.repeats)
            
            # 2. Run -O3 Baseline
            o3_runtime = run_baseline(b_path, "O3", metrics_collector, env.executor, iterations=args.repeats)
            
            if o2_runtime is None or o2_runtime <= 0 or o3_runtime is None or o3_runtime <= 0:
                print(f"  [ERROR] Baseline measurement failed for {Path(b_path).name}")
                continue
            
            print(f"  [DEBUG] -O2: {o2_runtime:.2f}ms, -O3: {o3_runtime:.2f}ms")
                
            # 3. Run Agent
            print(f"  [DEBUG] Running Agent (max {args.max_steps} steps)...")
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

                    terminate_idx = NUM_MACROS - 1
                    if m_idx.item() == terminate_idx:
                        terminated = True
                        break
                        
                    u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx)
                    u_idx = torch.argmax(u_logits, dim=-1)
                    
                print(f"    Step {episode_steps+1}: Macro {m_idx.item()} | Mod {u_idx.item()}")
                base_seq = MACRO_ACTIONS[m_idx.item()]
                final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                pipeline = [f"module({','.join(final_seq)})"]
                
                res = env.executor.apply_passes(env.current_ir_path, pipeline)
                if not res.success:
                    terminated = True
                else:
                    env.current_ir_path = res.output_path
                    episode_steps += 1
            
            print(f"  [DEBUG] Agent finished in {episode_steps} steps. Measuring runtime...")
            # Final Agent Runtime
            agent_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=args.repeats)
            
            if agent_runtime <= 0:
                print(f"  [ERROR] Agent measurement failed for {Path(b_path).name}")
                continue
                
            s_o2 = o2_runtime / agent_runtime
            s_o3 = o3_runtime / agent_runtime
            speedups_vs_o2.append(s_o2)
            speedups_vs_o3.append(s_o3)
            
            print(f"  [RESULT] Agent: {agent_runtime:.2f}ms | vO2: {s_o2:.2f}x | vO3: {s_o3:.2f}x")
            results_table.append({
                'name': Path(b_path).name,
                'o2': o2_runtime,
                'o3': o3_runtime,
                'agent': agent_runtime,
                'vO2': s_o2,
                'vO3': s_o3
            })
            
            env.close()
        except Exception as e:
            print(f"  [CRITICAL] Error evaluating {b_path}: {e}")

    # Final Summary Table
    print(f"\n\n{'Benchmark':<30} | {'-O2 (ms)':<10} | {'-O3 (ms)':<10} | {'Agent (ms)':<10} | {'v O2':<8} | {'v O3':<8}")
    print("-" * 95)
    for r in results_table:
        print(f"{r['name'][:30]:<30} | {r['o2']:10.2f} | {r['o3']:10.2f} | {r['agent']:10.2f} | {r['vO2']:7.2f}x | {r['vO3']:7.2f}x")

    def print_stats(name, data):
        if not data: return
        mean = np.mean(data)
        wins = len([s for s in data if s > 1.01])
        regressions = len([s for s in data if s < 0.95])
        low, high = bootstrap_ci(data)
        print(f"\nStats vs {name}:")
        print(f"  Mean Speedup:      {mean:.4f}x")
        print(f"  Wins (>1%):        {(wins/len(data))*100:.1f}%")
        print(f"  Regressions (>5%): {(regressions/len(data))*100:.1f}%")
        print(f"  95% Bootstrap CI:  [{low:.4f}, {high:.4f}]")

    print("\n" + "="*95)
    print_stats("O2", speedups_vs_o2)
    print_stats("O3", speedups_vs_o3)
    print("="*95)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--num_benchmarks", type=int, default=10)
    parser.add_argument("--file", type=str, default=None, help="Path to a specific file to evaluate")
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--max_steps", type=int, default=25)
    args = parser.parse_args()
    evaluate_against_baselines(args)
