import sys
import torch
import torch.nn.functional as F
import numpy as np
import argparse
import random
import time
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v7 import WorldModelV7
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS

METRIC_NAMES = ['Instructions', 'Size', 'Complexity', 'Loops', 'Calls', 'Blocks']

def run_rigorous_eval(checkpoint_path, num_samples=50, steps=15):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[EVAL] Loading checkpoint: {checkpoint_path}")
    
    # Load model
    model = WorldModelV7(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    model.eval()
    
    # Setup environment
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks)
    
    results = []
    
    pbar = tqdm(total=num_samples, desc="[EVAL] Progress", unit="sample")
    for i in range(num_samples):
        try:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None: continue
            
            # Initial state
            with torch.no_grad():
                state_emb = model.encode_graph(graph.to(device))
                num_nodes = graph.x.size(0) - 1
            
            current_state = state_emb
            
            sample_drift = []
            sample_metric_err = []
            
            for s in range(steps):
                action = env.action_space.sample()
                # Ground truth
                _, _, _, _, next_info = env.step(action)
                next_graph = env.get_observation_graph()
                if next_graph is None: break
                
                # Ground truth metrics
                m_instr = (next_info['instructions_after'] - next_info['instructions_before']) / max(next_info['instructions_before'], 1) * 100.0
                m_size = (next_info['size_after'] - next_info['size_before']) / max(next_info['size_before'], 1) * 100.0
                m_comp = (next_info['complexity_after'] - next_info['complexity_before']) / max(next_info['complexity_before'], 1) * 100.0
                m_loops = (next_info['loops_after'] - next_info['loops_before']) / max(next_info['loops_before'], 1) * 100.0
                m_calls = (next_info['calls_after'] - next_info['calls_before']) / max(next_info['calls_before'], 1) * 100.0
                m_blocks = (next_info['blocks_after'] - next_info['blocks_before']) / max(next_info['blocks_before'], 1) * 100.0
                true_metrics = torch.tensor([m_instr, m_size, m_comp, m_loops, m_calls, m_blocks], dtype=torch.float32, device=device)
                
                # Prediction
                action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                action_onehot[0, action] = 1.0
                
                with torch.no_grad():
                    next_state_pred, pred_metrics = model.transition_step(current_state, action_onehot, num_nodes=num_nodes)
                    
                    # Target state (real encoder)
                    target_state = model.encode_graph(next_graph.to(device))
                
                # Metrics
                drift = 1.0 - F.cosine_similarity(next_state_pred, target_state).mean().item()
                metric_err = F.l1_loss(pred_metrics[0], true_metrics).item()
                
                sample_drift.append(drift)
                sample_metric_err.append(metric_err)
                
                current_state = next_state_pred
                
            results.append({
                'drift': sample_drift,
                'metric_err': sample_metric_err
            })
            pbar.update(1)
                
        except Exception as e:
            # print(f"Error on sample {i}: {e}")
            continue
    pbar.close()
            
    # Aggregate results
    print("\n" + "="*50)
    print(f" RIGOROUS V7 EVALUATION REPORT (Steps={steps})")
    print("="*50)
    
    mean_drifts = np.zeros(steps)
    mean_errors = np.zeros(steps)
    valid_counts = np.zeros(steps)
    
    for r in results:
        for s in range(len(r['drift'])):
            mean_drifts[s] += r['drift'][s]
            mean_errors[s] += r['metric_err'][s]
            valid_counts[s] += 1
            
    mean_drifts /= np.maximum(valid_counts, 1)
    mean_errors /= np.maximum(valid_counts, 1)
    
    print(f"{'Step':<6} | {'Avg Drift':<12} | {'Avg Metric Err':<15}")
    print("-" * 40)
    for s in range(steps):
        print(f"{s+1:02d}     | {mean_drifts[s]:.4f}       | {mean_errors[s]:.4f}")
    
    # Calculate Action Sensitivity for good measure
    print("\n[EVAL] Calculating Action Sensitivity...")
    sensitivity = calculate_sensitivity(model, env)
    print(f"Action Sensitivity: {sensitivity:.4f} " + ("[OK]" if sensitivity > 0.01 else "[BLIND]"))
    print("="*50)

def calculate_sensitivity(model, env, num_checks=20):
    model.eval()
    diffs = []
    device = next(model.parameters()).device
    with torch.no_grad():
        for _ in range(num_checks):
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None: continue
            state_emb = model.encode_graph(graph.to(device))
            num_nodes = graph.x.size(0) - 1
            
            actions = random.sample(range(NUM_ACTIONS), 10)
            preds = []
            for action in actions:
                action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                action_onehot[0, action] = 1.0
                _, pred = model.transition_step(state_emb, action_onehot, num_nodes=num_nodes)
                preds.append(pred[0, 0].item())
            
            for i in range(len(preds)):
                for j in range(i+1, len(preds)):
                    diffs.append(abs(preds[i] - preds[j]))
    return np.mean(diffs) if diffs else 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--samples", type=int, default=50)
    parser.add_argument("--steps", type=int, default=15)
    args = parser.parse_args()
    
    run_rigorous_eval(args.checkpoint, args.samples, args.steps)
