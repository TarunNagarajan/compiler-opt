"""
v7 World Model — Distribution Sharpness Proof
Visualizes the categorical probability distributions to prove the model 
is making sharp, high-confidence predictions rather than lazy averaging.
"""

import sys
import torch
import numpy as np
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v7 import WorldModelV7
from src.env import CompilerOptEnv, RewardMode
from src.config import FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES

def load_v7_model(checkpoint_path):
    model = WorldModelV7(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    state_dict = ckpt['model_state_dict'] if 'model_state_dict' in ckpt else ckpt
    model.load_state_dict(state_dict)
    model.eval()
    return model

def prove_sharpness(model, file_path):
    print(f"\n[PROOF] Target: {file_path}")
    env = CompilerOptEnv([file_path], reward_mode=RewardMode.SECURE)
    
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    # Pick 3 interesting actions: A known optimizer, a known no-op, and a random one.
    # We'll use pass names to find actions if possible, or just pick indices.
    actions_to_test = [
        (env.num_atomic_passes + 0, "Macro 0 (Aggressive)"),
        (env.num_atomic_passes + len(LLVM_PASSES)//2, "Macro Mid"),
        (0, "Atomic 0 (Annotation)")
    ]
    
    print("\n" + "="*70)
    print("  DISTRIBUTION SHARPNESS PROOF")
    print("="*70)
    
    for action_idx, action_name in actions_to_test:
        with torch.no_grad():
            state_emb = model.encode_graph(graph)
            action_onehot = torch.zeros(1, NUM_ACTIONS)
            action_onehot[0, action_idx] = 1.0
            num_nodes = graph.x.size(0) - 1
            
            # Get raw logits from the transition head's metric predictor
            # We access the internal layer to see the "Confidence"
            size_ctx = model.get_size_context(num_nodes, state_emb.device)
            conditioned = model._condition_state(state_emb, action_onehot, size_ctx)
            
            # V7.1 Action Injection
            metric_features = torch.cat([conditioned, action_onehot], dim=-1)
            logits = model.metrics_head.net(metric_features) # [1, out_dim * 255]
            
            # Split into Instructions and Size
            instr_logits = logits[:, :255]
            instr_probs = torch.softmax(instr_logits, dim=-1).squeeze()
            
            # Calculate certainty (Entropy)
            entropy = -torch.sum(instr_probs * torch.log(instr_probs + 1e-10)).item()
            max_prob = torch.max(instr_probs).item()
            predicted_val = model.metrics_head.predict(metric_features)[0, 0].item()
            
            # Find the peak bin
            peak_bin = torch.argmax(instr_probs).item()
            # Map bin back to Symlog -> Linear value for context
            bins = model.metrics_head.bins.to(instr_probs.device)
            peak_symlog = bins[peak_bin].item()
            
            print(f"\n  Action: {action_name}")
            print(f"    Predicted Change: {predicted_val:>7.4f}%")
            print(f"    Peak Confidence:  {max_prob*100:>7.2f}% (Bin {peak_bin})")
            print(f"    Entropy:          {entropy:>7.4f} (Lower = Sharper)")
            
            bar_width = 40
            peak_idx = int(max_prob * bar_width)
            bar = "#" * peak_idx + "-" * (bar_width - peak_idx)
            print(f"    Confidence Bar:   [{bar}]")
            
            if entropy < 1.0:
                print("    VERDICT: [SHARP] Model is certain and targeting a specific magnitude.")
            elif entropy < 3.0:
                print("    VERDICT: [FOCUSED] Model sees a clear signal with minor variance.")
            else:
                print("    VERDICT: [DIFFUSE] Model is uncertain (averaging).")

    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()
    
    model = load_v7_model(args.checkpoint)
    prove_sharpness(model, args.file)
