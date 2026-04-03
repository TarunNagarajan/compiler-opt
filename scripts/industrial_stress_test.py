import torch
import numpy as np
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM

def run_stress_test(checkpoint_path):
    device = torch.device("cpu")
    print(f"[Industrial Super-Audit] Loading V8 Checkpoint: {checkpoint_path}")
    
    # 1. Initialize Base Model
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    base_model.load_state_dict(state_dict)
    
    # 2. Wrap with Phase 4.9b Gravity Filter (Final)
    model = CalibratedWorldModel(base_model)
    model.eval()
    
    # Final Super-Audit targets
    targets = [
        {"path": "benchmarks/large_scale/lz4/lz4.c", "action": 63, "label": "LZ4 (Unroll)"},
        {"path": "benchmarks/large_scale/yyjson.c", "action": 63, "label": "YYJSON (Unroll)"},
        {"path": "benchmarks/large_scale/yyjson.c", "action": 57, "label": "YYJSON (SROA)"},
        {"path": "benchmarks/large_scale/sqlite/sqlite3.c", "action": 63, "label": "SQLite (Unroll)"},
        {"path": "benchmarks/large_scale/cjson/cjson.c", "action": 63, "label": "cJSON (Unroll)"},
        {"path": "benchmarks/large_scale/tinyxml2/tinyxml2.cpp", "action": 63, "label": "TinyXML2 (Unroll)"},
    ]
    
    print("\n" + "="*90)
    print(f"{'Target':<20} | {'Nodes':<10} | {'Raw Pred':<10} | {'Calib Pred':<10} | {'Actual'}")
    print("-" * 90)
    
    for target in targets:
        p = Path(target['path'])
        if not p.exists():
            print(f"Skipping {target['label']} (File not found: {target['path']})")
            continue
            
        env = CompilerOptEnv([p], reward_mode=RewardMode.HACKABLE)
        obs, _ = env.reset()
        graph_data = env.get_observation_graph()
        total_nodes = getattr(graph_data, 'total_nodes', torch.tensor([100.0]))
        
        with torch.no_grad():
            action_onehot = torch.zeros(1, NUM_ACTIONS)
            action_onehot[0, target['action']] = 1.0
            
            _, raw_metrics = base_model(None, action_onehot, graph_data=graph_data)
            raw_val = raw_metrics[0, 0].item()
            
            _, calib_metrics = model(None, action_onehot, graph_data=graph_data, total_nodes=total_nodes)
            calib_val = calib_metrics[0, 0].item()
            
        _, _, _, _, info = env.step(target['action'])
        i_before = info.get('instructions_before', 1)
        i_after = info.get('instructions_after', 1)
        actual_val = (i_after - i_before) / max(i_before, 1) * 100.0
        
        print(f"{target['label']:<20} | {int(total_nodes.item()):<10} | {raw_val:>9.2f}% | {calib_val:>9.2f}% | {actual_val:>9.2f}%")
    print("-" * 90)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    run_stress_test(args.checkpoint)
