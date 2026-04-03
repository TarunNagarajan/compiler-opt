"""
v6 World Model Training & Automated Evaluation Script (HBC Edition)

Features:
1. Hierarchical Block Condensation (HBC) aware training.
2. Recursive Lookahead Evaluation (10 steps) with drift tracking.
3. Automated "Zig-Zag" Error Reporting per Checkpoint.
4. Dataset support with block_map fallback.

Usage:
  uv run python scripts/train_world_model_v6.py --name v6_final --dataset dataset/v5_full_collection_20260307_121355.json --iterations 20 --batch_size 16
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
from datetime import datetime
from pathlib import Path
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data, Batch
from torch.utils.tensorboard import SummaryWriter

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v6 import WorldModelV6
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

# Custom Data Object with HBC support
class TransitionDataV6(Data):
    def __init__(self, **kwargs):
        # Ensure block_map and next_block_map are at least identity mappings if None
        if 'block_map' in kwargs and kwargs['block_map'] is None:
            kwargs['block_map'] = torch.arange(kwargs['x'].size(0), dtype=torch.long)
        if 'next_block_map' in kwargs and kwargs['next_block_map'] is None:
            kwargs['next_block_map'] = torch.arange(kwargs['next_x'].size(0), dtype=torch.long)
        super().__init__(**kwargs)

    def __inc__(self, key, value, *args, **kwargs):
        if key == 'next_edge_index':
            return self.next_x.size(0)
        if key == 'block_map' or key == 'next_block_map':
            return 0 # Absolute indices
        return super().__inc__(key, value, *args, **kwargs)

def collect_data_v6(env, transitions_needed=1000):
    """Collects transitions online with v6 environment."""
    transitions = []
    print(f"[v6] Collecting {transitions_needed} online transitions...")
    while len(transitions) < transitions_needed:
        try:
            obs, info = env.reset()
            curr_graph = env.get_observation_graph()
            if curr_graph is None: continue
            
            for _ in range(5):
                action = env.action_space.sample()
                _, _, terminated, truncated, next_info = env.step(action)
                next_graph = env.get_observation_graph()
                if next_graph is None: break
                
                metrics = torch.tensor([
                    (next_info['instructions_after'] - next_info['instructions_before']) / max(next_info['instructions_before'], 1),
                    (next_info['size_after'] - next_info['size_before']) / max(next_info['size_before'], 1),
                    0, 0, 0, 0
                ], dtype=torch.float32)
                
                # V7.6 Tweak: Hard-Signal Balancing
                # We want exactly 50% No-Ops and 50% Significant Changes
                is_noop = (abs(metrics[0]) < 1e-4 and abs(metrics[1]) < 1e-4)
                
                if is_noop:
                    # Only keep 10% of no-ops during this phase to force contrast
                    if random.random() < 0.90:
                        continue

                transitions.append(TransitionDataV6(
                    x=curr_graph.x, 
                    edge_index=curr_graph.edge_index,
                    edge_attr=getattr(curr_graph, 'edge_attr', torch.zeros(curr_graph.edge_index.size(1), dtype=torch.long)),
                    block_map=getattr(curr_graph, 'block_map', None),
                    action=torch.tensor([action], dtype=torch.long),
                    y_metrics=metrics.unsqueeze(0),
                    next_x=next_graph.x, 
                    next_edge_index=next_graph.edge_index,
                    next_edge_attr=getattr(next_graph, 'edge_attr', torch.zeros(next_graph.edge_index.size(1), dtype=torch.long)),
                    next_block_map=getattr(next_graph, 'block_map', None)
                ))
                curr_graph = next_graph
                if terminated or truncated: break
        except: continue
    return transitions[:transitions_needed]

def run_lookahead_eval_v6(model, env, steps=10):
    """Evaluates the model's ability to predict 10 steps into the future using HBC."""
    model.eval()
    errors = []
    
    print(f"[v6] Running Recursive Lookahead Evaluation ({steps} steps)...")
    
    bench_paths = env.benchmark_paths
    val_subset = random.sample(bench_paths, min(len(bench_paths), 5))
    
    with torch.no_grad():
        for bench in val_subset:
            try:
                env.reset(options={"skip_canonicalization": True, "ir_path": str(bench)})
                curr_graph = env.get_observation_graph()
                if curr_graph is None: continue
                
                # V6 Encode with block_map
                curr_state_emb = model.gnn_encoder(
                    curr_graph.x, 
                    curr_graph.edge_index, 
                    curr_graph.edge_attr,
                    block_map=getattr(curr_graph, 'block_map', None)
                )
                
                bench_errors = []
                for s in range(steps):
                    action = random.randint(0, NUM_ACTIONS - 1)
                    
                    # REAL Step
                    _, _, _, _, info = env.step(action)
                    real_next_graph = env.get_observation_graph()
                    if real_next_graph is None: break
                    
                    real_next_emb = model.gnn_encoder(
                        real_next_graph.x, 
                        real_next_graph.edge_index, 
                        real_next_graph.edge_attr,
                        block_map=getattr(real_next_graph, 'block_map', None)
                    )
                    
                    # Real Metrics
                    real_inst_reduction = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
                    
                    # IMAGINED Step
                    action_onehot = torch.zeros(1, NUM_ACTIONS, device=curr_state_emb.device)
                    action_onehot[0, action] = 1.0
                    
                    # V7.7: Pass assumed node count for scaling intuition
                    num_nodes = curr_graph.x.size(0) - 1
                    pred_next_emb, pred_metrics_log = model.transition_step(curr_state_emb, action_onehot, num_nodes=num_nodes)
                    
                    # V7.5 Fix: Inverse Log Transform for honest error reporting (Factor 10.0)
                    # V7.10: Clip log-space to +/- 4.0 to prevent exponential explosion during uncalibrated early training
                    pred_metrics_log = torch.clamp(pred_metrics_log.view(-1), -4.0, 4.0)
                    pred_inst_red = (torch.expm1(torch.abs(pred_metrics_log[0])) / 10.0) * torch.sign(pred_metrics_log[0])
                    pred_inst_red = pred_inst_red.item()
                    
                    # Distance measurement
                    cos_sim = F.cosine_similarity(pred_next_emb, real_next_emb).item()
                    drift = 1.0 - cos_sim
                    met_err = abs(pred_inst_red - real_inst_reduction)
                    
                    bench_errors.append({
                        'step': s + 1,
                        'drift': drift,
                        'metric_err': met_err
                    })
                    
                    curr_state_emb = pred_next_emb 
                    
                errors.append(bench_errors)
            except Exception as e:
                print(f"[v6] Warning: Eval failed for {bench}: {e}")
                continue
            
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

def train_world_model_v6(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Use few benchmarks for online collection to save time
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks)
    
    log_dir = Path(args.log_dir) / args.name
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    model = WorldModelV6(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=args.gnn_layers).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    if args.load_checkpoint:
        ckpt = torch.load(args.load_checkpoint, map_location=device, weights_only=False)
        model.load_state_dict(ckpt.get('model_state_dict', ckpt), strict=False)
        print(f"[v6] Warm-started from {args.load_checkpoint}")

    replay_buffer = []
    
    # If offline dataset provided, load it
    if args.dataset:
        dataset_path = Path(args.dataset)
        if dataset_path.exists():
            print(f"[v6] Loading offline dataset: {args.dataset}")
            try:
                with open(args.dataset, 'r') as f:
                    data_list = json.load(f)
                    
                added = 0
                for d in data_list:
                    # VALIDATION: Only load if it has graph data (x, edge_index)
                    if 'x' in d and 'edge_index' in d and 'next_x' in d:
                        replay_buffer.append(TransitionDataV6(
                            x=torch.tensor(d['x'], dtype=torch.float),
                            edge_index=torch.tensor(d['edge_index'], dtype=torch.long),
                            edge_attr=torch.tensor(d.get('edge_attr', []), dtype=torch.long),
                            block_map=torch.tensor(d.get('block_map', []), dtype=torch.long) if 'block_map' in d else None,
                            action=torch.tensor([d['action']], dtype=torch.long),
                            y_metrics=torch.tensor(d['metrics'], dtype=torch.float).unsqueeze(0),
                            next_x=torch.tensor(d['next_x'], dtype=torch.float),
                            next_edge_index=torch.tensor(d['next_edge_index'], dtype=torch.long),
                            next_edge_attr=torch.tensor(d.get('next_edge_attr', []), dtype=torch.long),
                            next_block_map=torch.tensor(d.get('next_block_map', []), dtype=torch.long) if 'next_block_map' in d else None
                        ))
                        added += 1
                
                if added == 0:
                    print(f"[v6] WARNING: Dataset {args.dataset} contains 0 valid graph transitions. Falling back to 100% online collection.")
                else:
                    print(f"[v6] Loaded {added} valid transitions from offline dataset.")
            except Exception as e:
                print(f"[v6] Failed to load dataset: {e}. Falling back to online collection.")
        else:
            print(f"[v6] Dataset not found: {args.dataset}. Proceeding with online collection.")

    best_lookahead = float('inf')
    
    # INITIAL BUFFER FILL: Ensure we don't start training on empty data
    if len(replay_buffer) < args.steps_per_iter:
        print(f"[v6] Initial buffer too small ({len(replay_buffer)}). Collecting {args.steps_per_iter} fresh transitions...")
        replay_buffer.extend(collect_data_v6(env, transitions_needed=args.steps_per_iter))

    for it in range(args.iterations):
        print(f"\n[v6] --- Iteration {it+1}/{args.iterations} ---")
        
        # 1. Online Refresh (Always collect some HBC-native data)
        new_data = collect_data_v6(env, transitions_needed=args.steps_per_iter // 5)
        replay_buffer.extend(new_data)
        if len(replay_buffer) > 40000: replay_buffer = replay_buffer[-40000:]
        
        train_loader = DataLoader(replay_buffer, batch_size=args.batch_size, shuffle=True, follow_batch=['x', 'next_x'])
        model.train()
        epoch_losses = []
        
        for epoch in range(args.epochs_per_iter):
            for batch in train_loader:
                batch = batch.to(device)
                optimizer.zero_grad()
                
                actions_onehot = torch.zeros(batch.action.size(0), NUM_ACTIONS, device=device).scatter_(1, batch.action.view(-1, 1), 1.0)
                
                # V6 Encode with block_map
                state_emb = model.gnn_encoder(
                    batch.x, 
                    batch.edge_index, 
                    batch.edge_attr, 
                    batch=batch.batch,
                    block_map=getattr(batch, 'block_map', None)
                )
                
                # V7.7: Pass node counts for complexity scaling during training
                with torch.no_grad():
                    _, counts = torch.unique(batch.batch, return_counts=True)
                    # V7.8 Fix: Clamp to min=1 to prevent log10(0) -> -inf -> nan
                    num_nodes_batch = torch.clamp(counts - 1, min=1)
                
                pred_next, pred_met = model(state_emb, actions_onehot, num_nodes=num_nodes_batch)
                
                with torch.no_grad():
                    target_next_raw = model.gnn_encoder(
                        batch.next_x, 
                        batch.next_edge_index, 
                        batch.next_edge_attr, 
                        batch=batch.next_x_batch,
                        block_map=getattr(batch, 'next_block_map', None)
                    )
                    # For consistency, target should also be scaled by its specific complexity
                    _, next_counts = torch.unique(batch.next_x_batch, return_counts=True)
                    next_num_nodes = torch.clamp(next_counts - 1, min=1)
                    target_scale = 1.0 + torch.log10(next_num_nodes.float().to(device)) / 4.0
                    target_next = target_next_raw * target_scale.view(-1, 1)
                
                loss_s = 1.0 - F.cosine_similarity(pred_next, target_next).mean()
                
                # V7.5: Balanced Log-Scale Normalization
                # y' = sign(y) * log(1 + |y| * 10.0)
                # Prevents Gradient Explosion while maintaining multi-scale signal.
                target_metrics = batch.y_metrics
                log_target = torch.sign(target_metrics) * torch.log1p(torch.abs(target_metrics) * 10.0)
                
                # V7.6: Active Contrast Weighting
                # Assign 5x more weight to samples with real signal (delta > 1%)
                with torch.no_grad():
                    # We look at the raw metrics, not the log-transformed ones
                    magnitude = torch.abs(batch.y_metrics[:, 0]) # Instruction delta
                    weights = torch.where(magnitude > 0.01, 5.0, 1.0)
                
                loss_m_elementwise = F.mse_loss(pred_met, log_target, reduction='none')
                # Weight only the metric loss (multiply by column and batch weights)
                loss_m = (loss_m_elementwise.mean(dim=1) * weights).mean()
                
                loss = loss_s + 10.0 * loss_m # Balanced weight
                
                loss.backward()
                # V7.5: Gradient Clipping to prevent "Log-Scale Whiplash"
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                epoch_losses.append(loss.item())
        
        avg_loss = np.mean(epoch_losses)
        print(f"  Avg Loss: {avg_loss:.4f}")
        writer.add_scalar('Loss/Iter', avg_loss, it)
        
        # 3. Evaluation
        report = run_lookahead_eval_v6(model, env, steps=10)
        print(f"=== V6 Lookahead Report (Iter {it+1}) ===")
        for row in report:
            print(f"  Step {row['step']:02d}: Drift={row['avg_drift']:.4f}, MetricErr={row['avg_metric_err']:.4f}")
            writer.add_scalar(f'Eval/Drift_Step_{row["step"]}', row['avg_drift'], it)

        # 4. Save Checkpoints
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M")
        ckpt_path = MODELS_DIR / f"world_model_v6_{args.name}_latest.pth"
        torch.save({'model_state_dict': model.state_dict(), 'avg_loss': avg_loss, 'iteration': it}, ckpt_path)
        print(f"  [+] Saved latest checkpoint to {ckpt_path.name}")
        
        # V7: Also save iteration-specific checkpoint with timestamp for history
        iter_path = MODELS_DIR / f"world_model_v6_{args.name}_{timestamp_file}_iter_{it+1}.pth"
        torch.save(model.state_dict(), iter_path)
        
        if report[4]['avg_drift'] < best_lookahead:
            best_lookahead = report[4]['avg_drift']
            best_path = MODELS_DIR / f"world_model_v6_{args.name}_{timestamp_file}_best.pth"
            torch.save(model.state_dict(), best_path)
            print(f"  [*] New Best Lookahead: {best_lookahead:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--steps_per_iter", type=int, default=1000)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--epochs_per_iter", type=int, default=10)
    parser.add_argument("--name", type=str, default="v6_dev")
    parser.add_argument("--lr", type=float, default=2e-5) # V7.5: Default to safer LR
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--log_dir", type=str, default="runs/world_model_v6")
    parser.add_argument("--load_checkpoint", type=str, default=None)
    args = parser.parse_args()
    train_world_model_v6(args)
