"""
v5 World Model Training & Automated Evaluation Script

Features:
1. Online & Offline (JSON) Dataset Training.
2. Recursive Lookahead Evaluation (10 steps).
3. Automated "Zig-Zag" Error Reporting per Checkpoint.
4. Proxy Correlation Tracking (Instructions vs. Real Cycle Counts).

Usage:
  uv run python scripts/train_world_model_v5.py --name v5_final --dataset dataset/v5_full_collection.json --iterations 20 --batch_size 32
"""

import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import argparse
import time
import json
from pathlib import Path
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data, Batch
from torch.utils.tensorboard import SummaryWriter

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v5 import WorldModelV5
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

# Custom Data Object
class TransitionData(Data):
    def __inc__(self, key, value, *args, **kwargs):
        if key == 'next_edge_index':
            return self.next_x.size(0)
        return super().__inc__(key, value, *args, **kwargs)

def collect_data(env, transitions_needed=1000, mode="random"):
    """Collects transitions online with v5 environment."""
    transitions = []
    print(f"[v5] Collecting {transitions_needed} online transitions...")
    while len(transitions) < transitions_needed:
        try:
            obs, info = env.reset()
            curr_graph = env.get_observation_graph()
            if curr_graph is None: continue
            
            for _ in range(5): # Small steps per benchmark
                action = env.action_space.sample()
                _, _, terminated, truncated, next_info = env.step(action)
                next_graph = env.get_observation_graph()
                if next_graph is None: break
                
                metrics = torch.tensor([
                    (next_info['instructions_after'] - next_info['instructions_before']) / max(next_info['instructions_before'], 1),
                    (next_info['size_after'] - next_info['size_before']) / max(next_info['size_before'], 1),
                    0, 0, 0, 0
                ], dtype=torch.float32)
                
                transitions.append(TransitionData(
                    x=curr_graph.x, edge_index=curr_graph.edge_index,
                    edge_attr=getattr(curr_graph, 'edge_attr', torch.zeros(curr_graph.edge_index.size(1), dtype=torch.long)),
                    action=torch.tensor([action], dtype=torch.long),
                    y_metrics=metrics.unsqueeze(0),
                    next_x=next_graph.x, next_edge_index=next_graph.edge_index,
                    next_edge_attr=getattr(next_graph, 'edge_attr', torch.zeros(next_graph.edge_index.size(1), dtype=torch.long))
                ))
                curr_graph = next_graph
                if terminated or truncated: break
        except: continue
    return transitions[:transitions_needed]

def run_lookahead_eval(model, env, steps=10):
    """Evaluates the model's ability to predict 10 steps into the future."""
    model.eval()
    errors = []
    proxy_correlations = []
    
    print(f"[v5] Running Recursive Lookahead Evaluation ({steps} steps)...")
    
    # Select 5 diverse benchmarks for validation
    bench_paths = env.benchmark_paths
    val_subset = random.sample(bench_paths, min(len(bench_paths), 5))
    
    with torch.no_grad():
        for bench in val_subset:
            try:
                # 1. Start Ground Truth (Raw IR for realistic testing)
                env.reset(options={"skip_canonicalization": True, "ir_path": str(bench)})
                curr_graph = env.get_observation_graph()
                if curr_graph is None: continue
                curr_state_emb = model.encode_graph(curr_graph)
                
                bench_errors = []
                for s in range(steps):
                    # 2. Pick a Macro Action for larger impact
                    if random.random() < 0.3:
                        action = env.action_space.sample() # Random atomic
                    else:
                        # Pick a macro action (indices >= num_atomic_passes)
                        action = random.randint(env.num_atomic_passes, env.num_atomic_passes + env.num_macro_actions - 1)
                    
                    # 3. REAL Step
                    _, _, _, _, info = env.step(action)
                    real_next_graph = env.get_observation_graph()
                    if real_next_graph is None: break
                    real_next_emb = model.encode_graph(real_next_graph)
                    
                    # Real Metrics
                    real_inst_reduction = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
                    real_cycle_red = (info['runtime_after'] - info['runtime_before']) / max(info['runtime_before'], 1) if info.get('runtime_before', 0) > 0 else 0
                    
                    # 4. IMAGINED Step
                    action_onehot = torch.zeros(1, NUM_ACTIONS)
                    if action < NUM_ACTIONS:
                        action_onehot[0, action] = 1.0
                    pred_next_emb, pred_metrics = model(curr_state_emb, action_onehot)
                    pred_inst_red = pred_metrics[0, 0].item()
                    
                    # Distance measurement
                    cos_sim = F.cosine_similarity(pred_next_emb, real_next_emb).item()
                    drift = 1.0 - cos_sim
                    met_err = abs(pred_inst_red - real_inst_reduction)
                    
                    bench_errors.append({
                        'step': s + 1,
                        'drift': drift,
                        'metric_err': met_err,
                        'inst_proxy': real_inst_reduction,
                        'cycle_real': real_cycle_red
                    })
                    
                    # Update imagined state for next step (recursive)
                    curr_state_emb = pred_next_emb 
                    
                errors.append(bench_errors)
            except Exception as e:
                print(f"[v5] Warning: Eval failed for {bench}: {e}")
                continue
            
    # Aggregating
    avg_by_step = []
    for s in range(steps):
        step_drifts = [e[s]['drift'] for e in errors if len(e) > s]
        step_errs = [e[s]['metric_err'] for e in errors if len(e) > s]
        avg_by_step.append({
            'step': s+1,
            'avg_drift': np.mean(step_drifts) if step_drifts else 0,
            'avg_metric_err': np.mean(step_errs) if step_errs else 0
        })
        
    return avg_by_step

def train_world_model_v5(args):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks)
    
    log_dir = Path(args.log_dir) / args.name
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    model = WorldModelV5(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=args.gnn_layers)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.iterations)
    
    print(f"[v5] Initializing World Model v5 ({args.gnn_layers} layers)...")
    
    if args.load_checkpoint:
        checkpoint_path = Path(args.load_checkpoint)
        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path)
            # Handle both raw state_dicts and composite checkpoints
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                print(f"  [*] Loaded model state from {checkpoint_path}")
                if 'optimizer_state_dict' in checkpoint:
                    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                    print(f"  [*] Loaded optimizer state from {checkpoint_path}")
            else:
                model.load_state_dict(checkpoint)
                print(f"  [*] Loaded weights from {checkpoint_path}")
        else:
            print(f"  [!] Checkpoint not found: {checkpoint_path}")
    
    replay_buffer = []
    best_lookahead = float('inf')

    for it in range(args.iterations):
        print(f"\n[v5] --- Iteration {it+1}/{args.iterations} ---")
        
        # 1. Data Collection (Streamed/Mixed)
        new_data = collect_data(env, transitions_needed=args.steps_per_iter)
        replay_buffer.extend(new_data)
        if len(replay_buffer) > 30000: replay_buffer = replay_buffer[-30000:]
        
        # 2. Training Loop
        train_loader = DataLoader(replay_buffer, batch_size=args.batch_size, shuffle=True, follow_batch=['x', 'next_x'])
        model.train()
        epoch_losses = []
        for epoch in range(args.epochs_per_iter):
            for batch in train_loader:
                optimizer.zero_grad()
                actions_onehot = torch.zeros(batch.action.size(0), NUM_ACTIONS).scatter_(1, batch.action.view(-1, 1), 1.0)
                
                # Correct batch for each graph attribute
                curr_data = Data(x=batch.x, edge_index=batch.edge_index, edge_attr=batch.edge_attr, batch=batch.x_batch)
                state_emb = model.encode_graph(curr_data)
                
                pred_next, pred_met = model(state_emb, actions_onehot)
                
                with torch.no_grad():
                    next_v_data = Data(x=batch.next_x, edge_index=batch.next_edge_index, edge_attr=batch.next_edge_attr, batch=batch.next_x_batch)
                    target_next = model.encode_graph(next_v_data)
                
                loss_s = 1.0 - F.cosine_similarity(pred_next, target_next).mean()
                loss_m = F.mse_loss(pred_met, batch.y_metrics.squeeze(1))
                loss = loss_s + 5.0 * loss_m # Prioritize metrics for planning accuracy
                
                loss.backward()
                optimizer.step()
                epoch_losses.append(loss.item())
        
        print(f"  Avg Loss: {np.mean(epoch_losses):.4f}")
        writer.add_scalar('Loss/Iter', np.mean(epoch_losses), it)
        
        # 3. AUTOMATED EVALUATION (The Zig-Zag Report)
        report = run_lookahead_eval(model, env, steps=10)
        
        print(f"=== Lookahead Report (Iter {it+1}) ===")
        for row in report:
            print(f"  Step {row['step']}: Drift={row['avg_drift']:.4f}, MetricErr={row['avg_metric_err']:.4f}")
            writer.add_scalar(f'Eval/Drift_Step_{row["step"]}', row['avg_drift'], it)
            writer.add_scalar(f'Eval/MetricErr_Step_{row["step"]}', row['avg_metric_err'], it)
        
        # Save Report JSON
        report_path = LOG_DIR / f"eval_report_it_{it+1}.json"
        with open(report_path, 'w') as f: json.dump(report, f, indent=2)
        
        # 4. Save Checkpoints
        # Unconditional per-iteration save (RESILIENCE)
        iter_path = MODELS_DIR / f"world_model_{args.name}_iter_{it+1}.pth"
        torch.save({
            'iteration': it + 1,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': np.mean(epoch_losses),
            'report': report
        }, iter_path)
        
        # Best-of-run symlink/copy save
        current_step5_drift = report[4]['avg_drift']
        if current_step5_drift < best_lookahead:
            best_lookahead = current_step5_drift
            best_path = MODELS_DIR / f"world_model_{args.name}_best_lookahead.pth"
            torch.save(model.state_dict(), best_path)
            print(f"  [*] New Best Lookahead Checkpoint Saved: {current_step5_drift:.4f}")
            
        scheduler.step()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--steps_per_iter", type=int, default=1000)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--epochs_per_iter", type=int, default=10)
    parser.add_argument("--name", type=str, default="v5_final")
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--log_dir", type=str, default="runs/world_model")
    parser.add_argument("--load_checkpoint", type=str, default=None)
    args = parser.parse_args()
    
    # Global LOG_DIR for report saving
    LOG_DIR = Path(args.log_dir) / args.name
    train_world_model_v5(args)
