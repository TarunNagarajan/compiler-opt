"""
V7 World Model Evaluation Script

Computes R2 Scores and Drift metrics for the V7 Foveated World Model.
Supports: HBC block_map, Action-dim 67, and Large-Scale IR.
"""

import sys
from pathlib import Path
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from torch_geometric.data import Data, Batch

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v6 import WorldModelV6
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

def evaluate_v7(name="v7_foveated_scratch_latest"):
    print(f"🧪 Evaluating V7 World Model: {name}")
    
    # 1. Load V7 Model
    # Note: action_dim is 67 in current config
    model = WorldModelV6(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6)
    model_path = MODELS_DIR / f"world_model_v6_{name}.pth"
    if not model_path.exists():
        # Try without the v6 prefix if it was a legacy load
        model_path = MODELS_DIR / f"{name}.pth"
        
    if not model_path.exists():
        print(f"❌ Model {model_path} not found.")
        return
        
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"✅ Loaded checkpoint from iter {checkpoint.get('iteration', '?')}")
    else:
        model.load_state_dict(checkpoint)
    
    model.eval()
    
    # 2. Collect Real-World Transitions (Multi-Hotspot)
    benchmarks = get_benchmark_paths()
    # Focus on larger ones for a real test
    benchmarks = [b for b in benchmarks if "large" in str(b) or "library" in str(b) or "poly" in str(b)]
    if not benchmarks: benchmarks = get_benchmark_paths()
    
    env = CompilerOptEnv(benchmarks)
    
    actual_metrics = []
    pred_metrics = []
    
    print(f"📊 Collecting 100 transitions from {len(benchmarks)} benchmarks...")
    
    count = 0
    while count < 100:
        try:
            obs, info = env.reset()
            curr_graph = env.get_observation_graph()
            
            for _ in range(5):
                action = env.action_space.sample()
                next_obs, _, terminated, truncated, info = env.step(action)
                next_graph = env.get_observation_graph()
                
                # Calculate real delta
                instr_red = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
                size_red = (info['size_after'] - info['size_before']) / max(info['size_before'], 1)
                
                # Only keep if there was a change (ignore no-ops for R2 quality)
                if abs(instr_red) < 1e-6 and abs(size_red) < 1e-6 and np.random.random() < 0.7:
                    continue
                
                # Predict
                with torch.no_grad():
                    action_onehot = torch.zeros(1, NUM_ACTIONS)
                    action_onehot[0, action] = 1.0
                    
                    # V7.7: Pass node count for complexity-aware scaling
                    num_nodes = curr_graph.x.size(0) - 1
                    _, pred_met_log = model.transition_step(model.encode_graph(curr_graph), action_onehot, num_nodes=num_nodes)
                    
                    # V7.5: Inverse Log Transform (Factor 10.0)
                    # y = (exp(|y'|) - 1) / 10.0 * sign(y')
                    pred_met_log = pred_met_log.numpy().flatten()
                    pred_met = (np.expm1(np.abs(pred_met_log)) / 10.0) * np.sign(pred_met_log)
                    
                actual_metrics.append([instr_red, size_red])
                pred_metrics.append(pred_met[:2])
                
                curr_graph = next_graph
                count += 1
                if count >= 100: break
                if terminated or truncated: break
        except Exception as e:
            print(f"  [!] Skip: {e}")
            continue

    actual_metrics = np.array(actual_metrics)
    pred_metrics = np.array(pred_metrics)
    
    # 3. Compute R2 Scores
    r2_instr = r2_score(actual_metrics[:, 0], pred_metrics[:, 0])
    r2_size = r2_score(actual_metrics[:, 1], pred_metrics[:, 1])
    
    print("\n" + "="*40)
    print(" V7 WORLD MODEL PERFORMANCE REPORT")
    print("="*40)
    print(f" Instruction Delta R2:  {r2_instr:.4f}")
    print(f" Size Delta R2:         {r2_size:.4f}")
    print("-" * 40)
    
    # 4. Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Instr Plot
    ax1.scatter(actual_metrics[:, 0], pred_metrics[:, 0], alpha=0.5, color='blue')
    if np.var(actual_metrics[:, 0]) > 1e-9:
        m, b = np.polyfit(actual_metrics[:, 0], pred_metrics[:, 0], 1)
        ax1.plot(actual_metrics[:, 0], m*actual_metrics[:, 0] + b, color='red', label=f'Fit (R2={r2_instr:.2f})')
    ax1.set_title("Instruction Reduction Prediction")
    ax1.set_xlabel("Actual Delta")
    ax1.set_ylabel("Predicted Delta")
    ax1.grid(True)
    
    # Size Plot
    ax2.scatter(actual_metrics[:, 1], pred_metrics[:, 1], alpha=0.5, color='green')
    if np.var(actual_metrics[:, 1]) > 1e-9:
        m, b = np.polyfit(actual_metrics[:, 1], pred_metrics[:, 1], 1)
        ax2.plot(actual_metrics[:, 1], m*actual_metrics[:, 1] + b, color='red', label=f'Fit (R2={r2_size:.2f})')
    ax2.set_title("Binary Size Reduction Prediction")
    ax2.set_xlabel("Actual Delta")
    ax2.set_ylabel("Predicted Delta")
    ax2.grid(True)
    
    plt.tight_layout()
    plot_path = f"v7_eval_{name}.png"
    plt.savefig(plot_path)
    print(f"📊 Evaluation Plot saved to {plot_path}")
    
    if r2_instr > 0.4:
        print("\n✅ VERDICT: World Model is highly predictive. Ready for HRL Brain.")
    elif r2_instr > 0.1:
        print("\n⚠️ VERDICT: Model has signal but needs more training iterations.")
    else:
        print("\n❌ VERDICT: Model is currently a random walker. Continue training.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="v7_foveated_scratch_latest")
    args = parser.parse_args()
    evaluate_v7(args.name)
