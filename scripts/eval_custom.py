import sys
import os
sys.path.append(os.getcwd())

import torch
import argparse
from pathlib import Path
from src.env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES

def eval_custom_file(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
        
    # Load base model
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    ckpt = torch.load(args.checkpoint, map_location=device)
    base_model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    base_model.eval()
    
    # Load calibrated wrapper
    model = CalibratedWorldModel(base_model, meta_calibrator_path=args.meta_calibrator)
    model.eval()
    
    # Single-file environment
    env = CompilerOptEnv([args.file], max_steps=10, reward_mode=RewardMode.SIZE)
    
    obs, info = env.reset()
    graph_data = env.get_observation_graph().to(device)

    print(f"\nEvaluating on '{args.file}' | Initial Nodes: {graph_data.x.size(0)}")

    pass_to_idx = {p: i for i, p in enumerate(LLVM_PASSES)}
    actions_to_test = [
        ("Unroll", "function(loop-unroll)"),
        ("SROA", "function(sroa)"),
        ("SimplifyCFG", "function(simplifycfg)"),
        ("Inline", "inline"),
    ]
    
    print(f"\n{'Action':<15} | {'Predicted Δ (%)':<15} | {'Actual Δ (%)':<15}")
    print("-" * 50)
    
    for action_name, pass_name in actions_to_test:
        action_idx = pass_to_idx.get(pass_name)
        if action_idx is None:
            print(f"{action_name:<15} | {'SKIPPED':>14} | {'N/A':>14}")
            continue

        # Reset to base state for true comparison
        obs, info = env.reset()
        graph_data = env.get_observation_graph().to(device)
        
        # Action onehot
        action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
        action_onehot[0, action_idx] = 1.0
        
        # State embedding
        state_emb = model.encode_graph(graph_data)
        
        # Predict
        with torch.no_grad():
            _, predicted_metrics = model(state_emb, action_onehot, graph_data=graph_data)
            # Metric 0 is instruction delta in percentage points.
            pred_inst_delta_pct = predicted_metrics[0, 0].item()
            
        # Ground truth
        new_obs, _, _, _, info = env.step(action_idx)
        inst_before = info['instructions_before']
        inst_after = info['instructions_after']
        actual_inst_delta_pct = ((inst_after - inst_before) / max(inst_before, 1)) * 100.0
        
        # Print
        print(f"{action_name:<15} | {pred_inst_delta_pct:>14.2f}% | {actual_inst_delta_pct:>14.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to LLVM IR file to evaluate")
    parser.add_argument("--checkpoint", type=str, default="models/world_model.5_best.pth")
    parser.add_argument("--meta_calibrator", type=str, default="models/meta_calibrator_best.pth")
    args = parser.parse_args()
    eval_custom_file(args)
