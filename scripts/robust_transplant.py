import torch
import torch.nn as nn
from pathlib import Path
import sys
import argparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS

def robust_transplant(old_checkpoint_path, new_checkpoint_path):
    print(f"[TRANSPLANT] Loading Old Checkpoint: {old_checkpoint_path}")
    old_state = torch.load(old_checkpoint_path, map_location='cpu', weights_only=True)
    
    # Define new architecture (18 macros)
    NEW_NUM_MACROS = len(MACRO_ACTIONS)
    WORLD_MODEL_PATH = "models/world_model_antigravity_v4_L6_checkpoint.pth"
    
    # Create new agent with the current code's architecture
    new_agent = create_hrl_agent(FEATURE_DIM, NEW_NUM_MACROS, WORLD_MODEL_PATH, gnn_layers=6)
    new_state = new_agent.state_dict()
    
    layers_resized = 0
    layers_copied = 0
    
    for name, param in old_state.items():
        if name in new_state:
            if param.shape == new_state[name].shape:
                new_state[name].copy_(param)
                layers_copied += 1
            else:
                print(f"  [RESIZE] Layer: {name} | {param.shape} -> {new_state[name].shape}")
                # For Specialists and Worker layers
                if len(param.shape) == 2: # Weight matrix [Out, In]
                    # We copy existing columns/rows
                    out_min = min(param.shape[0], new_state[name].shape[0])
                    in_min = min(param.shape[1], new_state[name].shape[1])
                    new_state[name][:out_min, :in_min] = param[:out_min, :in_min]
                elif len(param.shape) == 1: # Bias
                    out_min = min(param.shape[0], new_state[name].shape[0])
                    new_state[name][:out_min] = param[:out_min]
                layers_resized += 1
        else:
            print(f"  [MISSING] Layer {name} not in new model architecture.")

    torch.save(new_state, new_checkpoint_path)
    print(f"\n[SUCCESS] Transplant complete.")
    print(f"  Copied: {layers_copied}")
    print(f"  Resized: {layers_resized}")
    print(f"  Saved to: {new_checkpoint_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", type=str, required=True)
    parser.add_argument("--new", type=str, required=True)
    args = parser.parse_args()
    robust_transplant(args.old, args.new)
