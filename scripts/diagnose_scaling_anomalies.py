import torch
import numpy as np
import argparse
import sys
import os
from pathlib import Path
from tqdm import tqdm

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM

def diagnose_scaling_anomalies(checkpoint_path):
    device = torch.device("cpu")
    print(f"[Diagnostic] Loading V8 Candidate: {checkpoint_path}")
    
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    model.load_state_dict(state_dict)
    model.eval()
    
    # Audit across Action Categories
    # 63: Unroll (Aggressive/Global)
    # 57: SROA (Structural/Local)
    # 12: GVN (Local)
    actions_to_test = [63, 57, 12, 45]
    benchmarks = [
        "benchmarks/large_scale/lz4/lz4.c",
        "benchmarks/large_scale/yyjson.c"
    ]
    
    results = []
    
    for path in benchmarks:
        if not Path(path).exists(): continue
        env = CompilerOptEnv([Path(path)], reward_mode=RewardMode.HACKABLE)
        
        for action in actions_to_test:
            obs, _ = env.reset()
            graph_data = env.get_observation_graph()
            total_nodes = getattr(graph_data, 'total_nodes', torch.tensor([100.0])).item()
            
            with torch.no_grad():
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0
                _, pred_metrics = model(None, action_onehot, graph_data=graph_data)
                pred_val = pred_metrics[0, 0].item()
            
            _, _, _, _, info = env.step(action)
            i_before = info.get('instructions_before', 1)
            i_after = info.get('instructions_after', 1)
            actual_val = (i_after - i_before) / max(i_before, 1) * 100.0
            
            error_multiplier = actual_val / pred_val if abs(pred_val) > 0.05 else 1.0
            
            results.append({
                "path": path,
                "action": action,
                "pred": pred_val,
                "actual": actual_val,
                "multiplier": error_multiplier,
                "nodes": total_nodes
            })
            
    print("\n[Audit] Scaling Discrepancy Map")
    print("-" * 80)
    print(f"{'Path':<20} | {'Act':<3} | {'Pred %':<8} | {'Actual %':<8} | {'Multi':<6} | {'Nodes'}")
    print("-" * 80)
    for r in results:
        print(f"{Path(r['path']).name:<20} | {r['action']:<3} | {r['pred']:>8.2f}% | {r['actual']:>8.2f}% | {r['multiplier']:>6.2f} | {int(r['nodes'])}")
    print("-" * 80)
    
    # Calculate Action-Specific Bias
    print("\n[Action Bias Analysis]")
    for act in actions_to_test:
        mults = [r['multiplier'] for r in results if r['action'] == act]
        if mults:
            print(f"Action {act:02d}: Average Calibration Bias = {np.mean(mults):.2f}x")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    diagnose_scaling_anomalies(args.checkpoint)
