import torch
import numpy as np
import argparse
import os
import sys
from pathlib import Path

# Fix for ModuleNotFoundError: No module named 'src'
sys.path.append(os.getcwd())

from src.models.world_model_v7 import WorldModelV7
from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.actions import MACRO_ACTIONS
from src.config import LLVM_PASSES, NUM_ACTIONS

def load_v7_model(checkpoint_path, device):
    # Use the dynamic NUM_ACTIONS from config to match the checkpoint
    model = WorldModelV7(action_dim=NUM_ACTIONS).to(device)
    # V7.4 Fix: Use weights_only=False for backward compatibility with complex types in state_dict
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    # Check if this is a full checkpoint dictionary or just weights
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
        
    model.eval()
    return model

def run_cross_scale_audit(checkpoint, benchmarks, steps=5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_v7_model(checkpoint, device)
    
    results = []
    
    for b_path in benchmarks:
        env = CompilerOptEnv(benchmark_paths=[str(b_path)], max_steps=steps, reward_mode=RewardMode.HACKABLE)
        obs, info = env.reset(options={"ir_path": str(b_path)})
        
        b_name = b_path.name
        is_large = b_path.stat().st_size > 100 * 1024
        
        print(f"\n[AUDIT] Benchmark: {b_name} ({'Large' if is_large else 'Small'})")
        
        for step in range(steps):
            graph_data = env.get_observation_graph()
            if graph_data is None: break
            
            # Predict
            action = np.random.randint(0, len(LLVM_PASSES) + len(MACRO_ACTIONS))
            action_onehot = torch.zeros(1, len(LLVM_PASSES) + len(MACRO_ACTIONS), device=device)
            action_onehot[0, action] = 1.0
            
            with torch.no_grad():
                # Get local node count for context
                num_nodes = graph_data.x.size(0) - 1
                _, pred_metrics = model.transition_step(torch.from_numpy(obs).to(device).unsqueeze(0), action_onehot, num_nodes=num_nodes)
            
            # Step
            obs, reward, term, trunc, info = env.step(action)
            
            # Extract truth
            instr_before = info['instructions_before']
            instr_after = info['instructions_after']
            actual_delta = (instr_after - instr_before) / max(instr_before, 1) * 100
            pred_delta = pred_metrics[0, 0].item() # Instruction Δ is index 0
            
            pass_name = info['pass_applied']
            
            print(f"  Step {step+1:02} | {pass_name[:30]:<30} | Pred: {pred_delta:>6.2f}% | Actual: {actual_delta:>6.2f}%")
            
            results.append({
                'benchmark': b_name,
                'scale': 'Large' if is_large else 'Small',
                'action': pass_name,
                'pred': pred_delta,
                'actual': actual_delta,
                'abs_error': abs(pred_delta - actual_delta)
            })
            
            if term or trunc: break
            
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    
    # 1. Select a few benchmarks
    bench_dir = Path("benchmarks")
    # Synthetic / Small
    small_bench = list(bench_dir.glob("synthetic/*.c"))[:1] 
    diverse_bench = list(bench_dir.glob("diverse_synthetic/*.c"))[:1]
    
    # Industrial / Large
    large_bench = [
        Path("benchmarks/large_scale/lz4/lz4.c"), 
        Path("benchmarks/large_scale/yyjson.c")
    ]
    
    all_targets = small_bench + diverse_bench + large_bench
    
    run_cross_scale_audit(args.checkpoint, all_targets)
