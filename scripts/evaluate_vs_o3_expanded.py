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

def run_o3_baseline(source_path, metrics_collector, executor, iterations=50):
    """Compiles the source to IR with -O3 and measures runtime."""
    temp_o3_ir = executor.work_dir / f"o3_baseline_{Path(source_path).stem}.ll"
    cmd = [str(CLANG), "-O3", "-S", "-emit-llvm", str(source_path), "-o", str(temp_o3_ir), "-Wno-everything"]
    subprocess.run(cmd, capture_output=True)
    
    if temp_o3_ir.exists():
        runtime = metrics_collector.measure_runtime(str(temp_o3_ir), iterations=iterations)
        return runtime
    return None

def bootstrap_ci(data, n_iterations=1000, alpha=0.05):
    """Computes bootstrap confidence interval for the mean."""
    means = []
    n = len(data)
    for _ in range(n_iterations):
        resample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(resample))
    
    lower = np.percentile(means, (alpha/2) * 100)
    upper = np.percentile(means, (1 - alpha/2) * 100)
    return lower, upper

def evaluate_vs_o3(args):
    print(f"\n[EVAL] Loading HRL Agent: {args.checkpoint}...")
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    metrics_collector = MetricsCollector()
    
    benchmarks = get_benchmark_paths()
    # Pick a smaller set of benchmarks because 50 repeats is heavy
    test_benchmarks = random.sample(benchmarks, min(len(benchmarks), args.num_benchmarks))
        
    all_speedups = []
    
    print(f"\n{'Benchmark':<30} | {'-O3 (ms)':<10} | {'Agent (ms)':<10} | {'Speedup':<10}")
    print("-" * 75)
    
    for b_path in test_benchmarks:
        try:
            env = CompilerOptEnv([b_path], max_steps=args.max_steps, reward_mode=RewardMode.SPEED)
            obs, info = env.reset()
            
            # 1. Run -O3 Baseline
            o3_runtime = run_o3_baseline(b_path, metrics_collector, env.executor, iterations=args.repeats)
            if o3_runtime is None or o3_runtime <= 0:
                print(f"{Path(b_path).name:<30} | Error in -O3")
                continue
                
            # 2. Run Agent
            terminated = False
            episode_steps = 0
            while not terminated and episode_steps < args.max_steps:
                graph = env.get_observation_graph()
                x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                with torch.no_grad():
                    macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
                    m_idx = torch.argmax(macro_probs, dim=-1)
                    
                    terminate_idx = NUM_MACROS - 1
                    if m_idx.item() == terminate_idx:
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
            
            # Final Agent Runtime
            agent_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=args.repeats)
            
            if agent_runtime <= 0:
                print(f"{Path(b_path).name:<30} | Error in Agent")
                continue
                
            speedup = o3_runtime / agent_runtime
            all_speedups.append(speedup)
            
            print(f"{Path(b_path).name[:30]:<30} | {o3_runtime:10.2f} | {agent_runtime:10.2f} | {speedup:10.2f}x")
            
            env.close()
        except Exception as e:
            print(f"Error evaluating {b_path}: {e}")

    if all_speedups:
        mean_speedup = np.mean(all_speedups)
        wins = len([s for s in all_speedups if s > 1.01])
        regressions_5 = len([s for s in all_speedups if s < 0.95])
        
        lower, upper = bootstrap_ci(all_speedups)
        
        print("-" * 75)
        print(f"Mean Speedup:      {mean_speedup:.4f}x")
        print(f"Wins (>1%):        {(wins/len(all_speedups))*100:.1f}%")
        print(f"Regressions (>5%): {(regressions_5/len(all_speedups))*100:.1f}%")
        print(f"95% Bootstrap CI:  [{lower:.4f}, {upper:.4f}]")
        print("-" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--num_benchmarks", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--max_steps", type=int, default=25)
    args = parser.parse_args()
    evaluate_vs_o3(args)
