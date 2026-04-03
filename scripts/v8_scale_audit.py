import torch
import numpy as np
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES


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


def _resolve_action_id(pass_name):
    if pass_name not in LLVM_PASSES:
        raise ValueError(f"Pass not found in LLVM_PASSES: {pass_name}")
    return LLVM_PASSES.index(pass_name)

def audit_v8(checkpoint_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Audit] Loading V8 Checkpoint: {checkpoint_path}")
    
    # Initialize V8 Model with correct dimensions
    model = WorldModel(state_dim=FEATURE_DIM, hidden_dim=256, action_dim=NUM_ACTIONS).to(device)
    
    # Load state dict (handle nested structure)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    model.eval()

    # Expanded Generalization Test Suite
    targets = [
        # 1. SMALL (Synthetic)
        {"path": "benchmarks/synthetic/syn_0000.c", "name": "syn_0000 (Small)", "pass_name": "function(loop-unroll)", "label": "Unroll"},
        {"path": "benchmarks/synthetic/syn_0042.c", "name": "syn_0042 (Small)", "pass_name": "function(sroa)", "label": "SROA"},
        
        # 2. MEDIUM (Mibench / Stencils)
        {"path": "benchmarks/mibench/bit_chaos.c", "name": "bit_chaos (Medium)", "pass_name": "function(loop-unroll)", "label": "Unroll"},
        {"path": "benchmarks/stencils/stencil_512_double_5pt_003.c", "name": "stencil_512 (Medium)", "pass_name": "function(sroa)", "label": "SROA"},
        
        # 3. INDUSTRIAL (The Stress Test)
        {"path": "benchmarks/large_scale/lz4/lz4.c", "name": "lz4 (Large)", "pass_name": "function(loop-unroll)", "label": "Unroll"},
        {"path": "benchmarks/large_scale/yyjson.c", "name": "yyjson (Large)", "pass_name": "function(sroa)", "label": "SROA"},
    ]

    print("\n" + "="*80)
    print(f"{'Benchmark':<20} | {'Action':<15} | {'Pred Inst %':<12} | {'Actual Inst %':<12} | {'Scale Fix'}")
    print("-" * 80)

    for target in targets:
        file_path = Path(target['path'])
        if not file_path.exists():
            print(f"[WARN] Missing benchmark, skipping: {file_path}")
            continue

        try:
            action_id = _resolve_action_id(target["pass_name"])
        except ValueError as e:
            print(f"[WARN] {e}")
            continue

        env = CompilerOptEnv([file_path], reward_mode=RewardMode.HACKABLE)
        obs, _ = env.reset(seed=42)
        
        # Predict
        with torch.no_grad():
            # Get graph data (V8 style)
            graph_data = env.get_observation_graph()
            if graph_data is None:
                print(f"[WARN] No graph data for {file_path}")
                continue
            graph_data = graph_data.to(device)
            local_nodes, total_nodes, total_nodes_tensor = _extract_scale_context(graph_data, device)
            
            # Action One-Hot
            action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
            action_onehot[0, action_id] = 1.0
            
            # Forward pass
            next_state, pred_metrics = model(None, action_onehot, graph_data=graph_data, total_nodes=total_nodes_tensor)
            pred_inst_delta = pred_metrics[0, 0].item()
            
            print(f"[Audit] Benchmark Scale: Local={local_nodes} Total={int(total_nodes)}")
        
        # Actual
        _, reward, _, _, info = env.step(action_id)
        i_before = info['instructions_before']
        i_after = info['instructions_after']
        actual_inst_delta = (i_after - i_before) / max(i_before, 1) * 100.0
        
        # Assessment
        error_ratio = abs(pred_inst_delta) / max(abs(actual_inst_delta), 1e-6)
        scale_fix = "[OK] CALIBRATED" if 0.5 <= error_ratio <= 2.0 else "[GAP] STILL PRESENT"
        if actual_inst_delta == 0 and abs(pred_inst_delta) < 0.5:
            scale_fix = "[OK] CALIBRATED (Small)"

        print(f"{target['name']:<20} | {target['label']:<15} | {pred_inst_delta:>11.2f}% | {actual_inst_delta:>11.2f}% | {scale_fix}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    audit_v8(args.checkpoint)
