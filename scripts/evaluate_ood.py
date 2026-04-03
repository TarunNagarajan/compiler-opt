import sys
from pathlib import Path
import torch
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv
from src.models import create_world_model
from src.config import FEATURE_DIM, NUM_ACTIONS

def evaluate_ood(checkpoint_path, c_file_path):
    print(f"\n[OOD TEST] Loading World Model from {checkpoint_path}...")
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS, gnn_layers=6)
    
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    model.eval()
    
    # Initialize env with JUST our novel C program
    env = CompilerOptEnv([c_file_path], max_steps=1)
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    if graph is None:
        print("Failed to compile or extract graph from test_ood.c")
        return
        
    print(f"\n[OOD TEST] Successfully parsed {c_file_path}")
    print(f"  Initial Instructions: {info['initial_instructions']}")
    print(f"  Initial Size: {info['initial_size']} bytes")
    
    # Let's test specific actions that we KNOW should have an impact
    # based on the way we wrote the C code.
    # 0: loop-unroll, 16: mem2reg, 18: instcombine, 25: dse
    test_actions = [0, 16, 18, 25]
    action_names = ["loop-unroll", "mem2reg", "instcombine", "dse"]
    
    print("\n[OOD TEST] Evaluating Predictions vs Reality...")
    
    for act_idx, action_name in zip(test_actions, action_names):
        print(f"\n--- Testing Action: {action_name} ({act_idx}) ---")
        
        # 1. World Model Prediction
        action_tensor = torch.tensor([act_idx], dtype=torch.long)
        batch_vec = torch.zeros(graph.x.size(0), dtype=torch.long)
        edge_attr = getattr(graph, 'edge_attr', None)
        
        with torch.no_grad():
            _, pred_metrics, _ = model(graph.x, graph.edge_index, batch_vec, action_tensor, edge_attr=edge_attr)
            pred_instr = pred_metrics[0][0].item() * 100
            pred_size = pred_metrics[0][1].item() * 100
            
        print(f"  [Oracle] Predicted Instruction Delta: {pred_instr:+8.2f}%")
        print(f"  [Oracle] Predicted Size Delta:        {pred_size:+8.2f}%")
        
        # 2. Ground Truth (LLVM)
        # We must reset the environment to the original test_ood.c state for each test
        obs, info = env.reset() 
        current_instr = info['initial_instructions']
        current_size = info['initial_size']
        
        next_obs, reward, term, trunc, step_info = env.step(act_idx)
        
        actual_instr_delta = ((step_info['instructions_after'] - current_instr) / max(current_instr, 1)) * 100
        actual_size_delta = ((step_info['size_after'] - current_size) / max(current_size, 1)) * 100
        
        print(f"  [LLVM]   Actual Instruction Delta:    {actual_instr_delta:+8.2f}%")
        print(f"  [LLVM]   Actual Size Delta:           {actual_size_delta:+8.2f}%")
        
        error_instr = abs(pred_instr - actual_instr_delta)
        print(f"  => Absolute Error: {error_instr:.2f}%")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="models/world_model_antigravity_v4_L6_checkpoint.pth")
    parser.add_argument("--file", type=str, default="test_ood.c")
    args = parser.parse_args()
    
    evaluate_ood(args.checkpoint, args.file)
