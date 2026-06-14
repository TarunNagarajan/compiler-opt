import sys
import os
sys.path.append(os.getcwd())

import torch
import argparse
from src.env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES


def _pct_delta(before, after, denom_floor=1.0):
    before_v = float(before)
    after_v = float(after)
    if before_v <= 0:
        return 0.0
    return ((before_v - after_v) / max(before_v, float(denom_floor))) * 100.0


def _get_reward_mode(mode_name: str) -> RewardMode:
    key = str(mode_name).strip().upper()
    try:
        return RewardMode[key]
    except KeyError as exc:
        valid = ", ".join(m.name.lower() for m in RewardMode)
        raise ValueError(f"Unknown reward mode '{mode_name}'. Valid: {valid}") from exc


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
    
    # Single-file environment. Force speed metrics collection so runtime/energy deltas are populated.
    env = CompilerOptEnv(
        [args.file],
        max_steps=10,
        reward_mode=_get_reward_mode(args.reward_mode),
        collect_speed_metrics=bool(args.collect_speed_metrics),
        runtime_measure_runs=args.runtime_measure_runs,
    )
    
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
    
    print(f"\n{'Action':<15} | {'Pred Raw Gain (%)':<18} | {'Pred Cal Gain (%)':<18} | {'Actual Gain (%)':<16}")
    print("-" * 74)
    
    for action_name, pass_name in actions_to_test:
        action_idx = pass_to_idx.get(pass_name)
        if action_idx is None:
            print(f"{action_name:<15} | {'SKIPPED':>17} | {'SKIPPED':>17} | {'N/A':>15}")
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
            # Pre-calibration prediction from base world model.
            _, raw_metrics = base_model(state_emb=state_emb, action_onehot=action_onehot, graph_data=graph_data)
            # Metrics head predicts (after-before)/before. Convert to gain convention ((before-after)/before).
            raw_inst_delta_pct = -raw_metrics[0, 0].item()

            # Post-calibration prediction from calibrated wrapper.
            _, calibrated_metrics = model(state_emb, action_onehot, graph_data=graph_data)
            calibrated_inst_delta_pct = -calibrated_metrics[0, 0].item()
            
        # Ground truth
        new_obs, _, _, _, info = env.step(action_idx)
        inst_before = info['instructions_before']
        inst_after = info['instructions_after']
        actual_inst_delta_pct = _pct_delta(inst_before, inst_after, denom_floor=1.0)
        
        # Print
        print(
            f"{action_name:<15} | {raw_inst_delta_pct:>14.2f}% | {calibrated_inst_delta_pct:>14.2f}% | {actual_inst_delta_pct:>14.2f}%"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to LLVM IR file to evaluate")
    parser.add_argument("--checkpoint", type=str, default="models/world_model_v8.5_best.pth")
    parser.add_argument("--meta_calibrator", type=str, default="models/meta_calibrator_best.pth")
    parser.add_argument("--reward_mode", type=str, default="size", help="Env reward mode for eval (speed|size|performance|...)")
    parser.add_argument("--runtime_measure_runs", type=int, default=3, help="Runtime measurement repetitions per step")
    parser.add_argument("--collect_speed_metrics", type=int, default=1, help="Set 0 for faster eval without runtime/energy measurement")
    args = parser.parse_args()
    eval_custom_file(args)
