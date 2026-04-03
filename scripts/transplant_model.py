import torch
import torch.nn as nn
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS

def transplant_weights(old_checkpoint_path, new_checkpoint_path):
    OLD_NUM_MACROS = 16
    NEW_NUM_MACROS = len(MACRO_ACTIONS) # 18
    
    print(f"Transplanting {OLD_NUM_MACROS} -> {NEW_NUM_MACROS} macros...")
    
    old_state = torch.load(old_checkpoint_path, map_location='cpu', weights_only=True)
    
    # We must use create_hrl_agent with the NEW number of macros
    new_agent = create_hrl_agent(FEATURE_DIM, NEW_NUM_MACROS, world_model_path="models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    new_state = new_agent.state_dict()
    
    for name, param in old_state.items():
        if name in new_state:
            if param.shape == new_state[name].shape:
                new_state[name].copy_(param)
            else:
                print(f"Resizing layer: {name} {param.shape} -> {new_state[name].shape}")
                # The macro-related layers are deeper in the hierarchy
                # e.g., manager.performance_agent.action_head.weight
                if len(param.shape) == 2: # Linear weight [Out, In]
                    new_state[name][:param.shape[0], :param.shape[1]] = param
                elif len(param.shape) == 1: # Bias [Out]
                    new_state[name][:param.shape[0]] = param
                    
    torch.save(new_state, new_checkpoint_path)
    print(f"Transplant complete: {new_checkpoint_path}")

if __name__ == "__main__":
    transplant_weights("models/hrl_suggestive_hour_1923.pth", "models/hrl_suggestive_v5_expanded.pth")
