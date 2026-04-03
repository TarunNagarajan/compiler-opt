"""
v7 World Model — Targeted Stress Test
Evaluates V7 performance on a SPECIFIC file across many random actions.
"""

import sys
import torch
import torch.nn.functional as F
import numpy as np
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v7 import WorldModelV7
from src.env import CompilerOptEnv, RewardMode
from src.config import FEATURE_DIM, NUM_ACTIONS

def load_v7_model(checkpoint_path):
    model = WorldModelV7(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    state_dict = ckpt['model_state_dict'] if 'model_state_dict' in ckpt else ckpt
    model.load_state_dict(state_dict)
    model.eval()
    return model

def stress_test(model, file_path, samples=20):
    print(f"\n[STRESS-TEST] Target: {file_path}")
    print(f"[STRESS-TEST] Running {samples} random actions...")
    
    # Initialize env with ONLY the target file
    env = CompilerOptEnv([file_path], reward_mode=RewardMode.SECURE)
    
    results = []
    for i in range(samples):
        obs, info = env.reset()
        graph = env.get_observation_graph()
        
        # Take a random action
        action = env.action_space.sample()
        obs_next, reward, terminated, truncated, info_step = env.step(action)
        
        # Calculate true % change
        true_instr = (info_step['instructions_after'] - info_step['instructions_before']) / max(info_step['instructions_before'], 1) * 100.0
        true_size = (info_step['size_after'] - info_step['size_before']) / max(info_step['size_before'], 1) * 100.0
        
        # Model Prediction
        with torch.no_grad():
            state_emb = model.encode_graph(graph)
            action_onehot = torch.zeros(1, NUM_ACTIONS)
            action_onehot[0, action] = 1.0
            num_nodes = graph.x.size(0) - 1
            _, pred_metrics = model.transition_step(state_emb, action_onehot, num_nodes=num_nodes)
            
        results.append({
            'true_i': true_instr,
            'pred_i': pred_metrics[0, 0].item(),
            'true_s': true_size,
            'pred_s': pred_metrics[0, 1].item(),
            'num_nodes': num_nodes
        })
        
        if (i+1) % 5 == 0:
            print(f"  Processed {i+1}/{samples}...")

    # Statistics
    instr_errs = [abs(r['pred_i'] - r['true_i']) for r in results]
    size_errs = [abs(r['pred_s'] - r['true_s']) for r in results]
    
    print("\n" + "="*50)
    print(f"  STRESS TEST RESULTS: {Path(file_path).name}")
    print("="*50)
    print(f"  Avg Instructions MAE (%): {np.mean(instr_errs):.4f}")
    print(f"  Avg Size MAE (%):         {np.mean(size_errs):.4f}")
    print(f"  Max Instr Error (%):     {np.max(instr_errs):.4f}")
    print(f"  Nodes in Graph:          {results[0]['num_nodes']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--samples", type=int, default=20)
    args = parser.parse_args()
    
    model = load_v7_model(args.checkpoint)
    stress_test(model, args.file, args.samples)
