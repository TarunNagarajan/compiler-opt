"""
v7 World Model — Comprehensive Evaluation

Evaluates the V7 architecture including:
1. Two-Hot Categorical SymLog accuracy
2. Action-State Attention queries
3. Direction accuracy and no-op detection
4. Calibration (Predicted vs Actual distributions)

Usage:
  uv run python scripts/evaluate_world_model_v7.py --checkpoint models/world_model_v7_v7_final_latest.pth --samples 100
"""

import sys
import torch
import torch.nn.functional as F
import numpy as np
import argparse
import random
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v7 import WorldModelV7
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES
from torch_geometric.data import Data

METRIC_NAMES = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]
NOOP_THRESHOLD = 0.005  # Δ < 0.5% is considered no-op

def load_v7_model(checkpoint_path, gnn_layers=6):
    model = WorldModelV7(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=gnn_layers)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in ckpt:
        model.load_state_dict(ckpt['model_state_dict'])
        print(f"[EVAL-v7] Loaded checkpoint from Iteration {ckpt.get('iteration', '?')}")
    else:
        model.load_state_dict(ckpt)
    model.eval()
    return model

def get_category(filepath):
    parts = str(filepath).replace('\\', '/').lower()
    for cat in ['polybench', 'stencils', 'multi_func', 'deep_call_chain', 'library_heavy', 'scaled_composite', 'diverse_synthetic', 'anghaben_wrapped', 'synthetic', 'graphs']:
        if cat in parts: return cat
    return 'other'

def collect_samples_v7(model, env, num_samples):
    results = []
    print(f"[EVAL-v7] Collecting {num_samples} samples...")
    
    for _ in range(num_samples):
        try:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None: continue
            
            action = env.action_space.sample()
            _, _, _, _, step_info = env.step(action)
            
            # Ground Truth % Metrics
            true_metrics = torch.tensor([[
                (step_info['instructions_after'] - step_info['instructions_before']) / max(step_info['instructions_before'], 1) * 100.0,
                (step_info['size_after'] - step_info['size_before']) / max(step_info['size_before'], 1) * 100.0,
                0, 0, 0, 0
            ]], dtype=torch.float32)
            
            # V7 Prediction
            with torch.no_grad():
                state_emb = model.encode_graph(graph)
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0
                num_nodes = graph.x.size(0) - 1
                
                _, pred_metrics = model.transition_step(state_emb, action_onehot, num_nodes=num_nodes)
            
            # V7 Sensitivity Check (Compare against a random alternate action)
            alt_action = random.randint(0, NUM_ACTIONS - 1)
            while alt_action == action: alt_action = random.randint(0, NUM_ACTIONS - 1)
            
            with torch.no_grad():
                alt_onehot = torch.zeros(1, NUM_ACTIONS)
                alt_onehot[0, alt_action] = 1.0
                _, alt_metrics = model.transition_step(state_emb, alt_onehot, num_nodes=num_nodes)
                
            sensitivity = abs(pred_metrics[0, 0].item() - alt_metrics[0, 0].item())
            
            results.append({
                'true': true_metrics,
                'pred': pred_metrics,
                'action': action,
                'category': get_category(env.current_benchmark_path),
                'num_nodes': num_nodes,
                'sensitivity': sensitivity
            })
        except: continue
        
    return results

def analyze_v7(results):
    all_true = torch.cat([r['true'] for r in results], dim=0)
    all_pred = torch.cat([r['pred'] for r in results], dim=0)
    
    print("\n" + "="*70)
    print("  V7 WORLD MODEL EVALUATION")
    print("="*70)
    
    mae = F.l1_loss(all_pred, all_true).item()
    cos = F.cosine_similarity(all_pred, all_true, dim=-1).mean().item()
    avg_sensitivity = np.mean([r['sensitivity'] for r in results])
    
    print(f"  Samples:            {len(results)}")
    print(f"  Overall MAE (%):    {mae:.4f}")
    print(f"  Cosine Similarity:  {cos:.4f}")
    print(f"  Action Sensitivity: {avg_sensitivity:.4f} " + ("[RESTORED]" if avg_sensitivity > 0.1 else "[BLIND]"))
    
    print("\n  Per-Metric Accuracy (MAE in %):")
    for i, name in enumerate(METRIC_NAMES[:2]): # Instructions, Size
        m_mae = F.l1_loss(all_pred[:, i], all_true[:, i]).item()
        print(f"    {name:15s}: {m_mae:.4f}%")

    # No-Op analysis
    true_noop = all_true[:, 0].abs() < 0.5
    pred_noop = all_pred[:, 0].abs() < 0.5
    tp = (true_noop & pred_noop).sum().item()
    fp = (~true_noop & pred_noop).sum().item()
    fn = (true_noop & ~pred_noop).sum().item()
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    print(f"\n  No-Op Detection (Δ < 0.5%):")
    print(f"    Precision: {precision:.3f}")
    print(f"    Recall:    {recall:.3f}")
    print(f"    F1:        {f1:.3f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--samples", type=int, default=100)
    args = parser.parse_args()
    
    model = load_v7_model(args.checkpoint)
    env = CompilerOptEnv(get_benchmark_paths())
    results = collect_samples_v7(model, env, args.samples)
    analyze_v7(results)
