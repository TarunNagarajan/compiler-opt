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

def run_o2_baseline(source_path, metrics_collector, executor):
    """Compiles the source to IR with -O2 and measures runtime."""
    temp_o2_ir = executor.work_dir / f"o2_baseline_{Path(source_path).stem}.ll"
    cmd = [str(CLANG), "-O2", "-S", "-emit-llvm", str(source_path), "-o", str(temp_o2_ir), "-Wno-everything"]
    subprocess.run(cmd, capture_output=True)
    
    if temp_o2_ir.exists():
        runtime = metrics_collector.measure_runtime(str(temp_o2_ir), iterations=20)
        return runtime
    return None

def evaluate_vs_o2(args):
    print(f"\n[EVAL] Loading HRL Agent: {args.checkpoint}...")
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    metrics_collector = MetricsCollector()
    
    benchmarks = get_benchmark_paths()
    if args.limit:
        test_benchmarks = random.sample(benchmarks, min(len(benchmarks), args.limit))
    else:
        test_benchmarks = benchmarks[:5] # Default to first 5
        
    results = []
    
    print(f"\n{'Benchmark':<30} | {'-O2 (ms)':<10} | {'Agent (ms)':<10} | {'Speedup':<10}")
    print("-" * 70)
    
    for b_path in test_benchmarks:
        try:
            env = CompilerOptEnv([b_path], max_steps=25, reward_mode=RewardMode.SPEED)
            obs, info = env.reset()
            
            # 1. Run -O2 Baseline
            o2_runtime = run_o2_baseline(b_path, metrics_collector, env.executor)
            if o2_runtime is None or o2_runtime <= 0:
                print(f"{Path(b_path).name:<30} | Error in -O2")
                continue
                
            # 2. Run Agent
            terminated = False
            episode_steps = 0
            while not terminated and episode_steps < args.max_steps:
                graph = env.get_observation_graph()
                x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                with torch.no_grad():
                    macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
                    
                    # Evaluation should be deterministic
                    m_idx = torch.argmax(macro_probs, dim=-1)
                    
                    terminate_idx = NUM_MACROS - 1
                    if m_idx.item() == terminate_idx:
                        terminated = True
                        break
                        
                    u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx)
                    u_idx = torch.argmax(u_logits, dim=-1)
                    
                base_seq = MACRO_ACTIONS[m_idx.item()]
                final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                pipeline = ["module({})".format(",".join(final_seq))]
                
                res = env.executor.apply_passes(env.current_ir_path, pipeline)
                if not res.success:
                    terminated = True
                else:
                    env.current_ir_path = res.output_path
                    episode_steps += 1
            
            # Final Agent Runtime (with more iterations for accuracy)
            agent_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=20)
            
            if agent_runtime <= 0:
                print(f"{Path(b_path).name:<30} | Error in Agent")
                continue
                
            speedup = o2_runtime / agent_runtime
            results.append(speedup)
            
            print(f"{Path(b_path).name[:30]:<30} | {o2_runtime:10.2f} | {agent_runtime:10.2f} | {speedup:10.2f}x")
            
            env.close()
        except Exception as e:
            print(f"Error evaluating {b_path}: {e}")

    if results:
        avg_speedup = np.mean(results)
        print("-" * 70)
        print(f"{'AVERAGE SPEEDUP':<30} | {'':<10} | {'':<10} | {avg_speedup:10.2f}x")
        
        wins = len([r for r in results if r > 1.05])
        losses = len([r for r in results if r < 0.95])
        ties = len(results) - wins - losses
        print(f"Summary: Wins: {wins}, Ties: {ties}, Losses: {losses}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--max_steps", type=int, default=25)
    args = parser.parse_args()
    evaluate_vs_o2(args)
