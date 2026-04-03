import torch
import numpy as np
import argparse
import sys
import os
from pathlib import Path
from tqdm import tqdm

# Fix for ModuleNotFoundError
sys.path.append(os.getcwd())

from src.models.world_model import WorldModel
from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES


def _resolve_sequence(steps):
    pass_sequence = [
        "function(loop-unroll)",
        "function(gvn)",
        "function(simplifycfg)",
        "function(sroa)",
        "function(loop-mssa(licm))",
    ]
    resolved = []
    for pass_name in pass_sequence:
        if pass_name in LLVM_PASSES:
            resolved.append((LLVM_PASSES.index(pass_name), pass_name))
        else:
            print(f"[WARN] Pass not found in LLVM_PASSES, skipping: {pass_name}")
    if not resolved:
        raise RuntimeError("No foresight sequence actions resolved from LLVM_PASSES.")
    return resolved[:steps]


def _extract_scale_context(graph_data, device):
    local_nodes = max(int(graph_data.x.size(0)) - 1, 1)
    total_raw = getattr(graph_data, "total_nodes", None)
    if isinstance(total_raw, torch.Tensor) and total_raw.numel() > 0:
        total_nodes = float(total_raw.detach().view(-1)[0].item())
    elif total_raw is None:
        total_nodes = float(local_nodes)
    else:
        total_nodes = float(total_raw)
    total_nodes = max(total_nodes, 1.0)
    return local_nodes, total_nodes, torch.tensor([[total_nodes]], dtype=torch.float32, device=device)

def run_foresight_audit(checkpoint_path, benchmark_path, steps=3):
    device = torch.device("cpu")
    print(f"[Foresight] Loading V8 Checkpoint: {checkpoint_path}")
    
    # Initialize Model
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    model.load_state_dict(state_dict)
    model.eval()
    
    # Initialize Env
    env = CompilerOptEnv([Path(benchmark_path)], reward_mode=RewardMode.HACKABLE)
    obs, info = env.reset()
    
    total_pred = 0
    total_actual = 0
    
    print(f"\n[Foresight] Auditing Trajectory on: {benchmark_path}")
    print("-" * 60)
    print(f"{'Step':<5} | {'Action':<8} | {'Pred %':<10} | {'Actual %':<10} | {'Error'}")
    print("-" * 60)
    
    # Fixed sequence for reproducibility
    sequence = _resolve_sequence(steps)
    
    state_emb = None
    
    for i, (action, pass_name) in enumerate(sequence):
        # 1. Get Model Prediction
        graph_data = env.get_observation_graph()
        if graph_data is None:
            print("[WARN] Missing graph data; ending trajectory early.")
            break
        graph_data = graph_data.to(device)
        num_nodes, total_nodes, total_nodes_tensor = _extract_scale_context(graph_data, device)
        
        with torch.no_grad():
            if state_emb is None:
                state_emb = model.encode_graph(graph_data)
            
            action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
            action_onehot[0, action] = 1.0
            
            next_state, pred_metrics = model.transition_step(
                state_emb, action_onehot, num_nodes=num_nodes, total_nodes=total_nodes_tensor
            )
            
            pred_val = pred_metrics[0, 0].item() # Instructions Delta %
            
        # 2. Get Actual Environment Step
        next_obs, reward, terminated, truncated, info = env.step(action)
        
        i_before = info.get('instructions_before', 0)
        i_after = info.get('instructions_after', 0)
        actual_val = (i_after - i_before) / max(i_before, 1) * 100.0
        
        total_pred += pred_val
        total_actual += actual_val
        error = abs(pred_val - actual_val)
        
        print(f"{i+1:<5} | {pass_name:<8} | {pred_val:>9.2f}% | {actual_val:>9.2f}% | {error:>6.2f}")
        
        # Update for next step in latent space
        state_emb = next_state
        if terminated or truncated: break
        
    print("-" * 60)
    print(f"{'TOTAL':<14} | {total_pred:>9.2f}% | {total_actual:>9.2f}% | Delta: {abs(total_pred - total_actual):>6.2f}%")
    
    # Comparison to hypothetical V7 Baseline (Scale-Blind)
    # V7 would predict ~-1% per step.
    v7_total = -1.0 * steps
    print(f"[Analogy] V7 Blind Total Prediction: {v7_total:.2f}% (Error: {abs(v7_total - total_actual):.2f})")
    print(f"[Analogy] V8.3 Gain: Model is {abs(v7_total - total_actual) - abs(total_pred - total_actual):.2f}% closer to reality.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--benchmark", type=str, default="benchmarks/large_scale/lz4/lz4.c")
    parser.add_argument("--steps", type=int, default=3)
    args = parser.parse_args()
    
    run_foresight_audit(args.checkpoint, args.benchmark, args.steps)
