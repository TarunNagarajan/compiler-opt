"""
v7 World Model Training & Automated Evaluation Script

Features:
1. Two-Hot Categorical SymLog Optimization (DreamerV3 style)
2. State-Action Cross-Attention Conditioning.
3. Native Size Context Injection.
4. Recursive Lookahead Evaluation (10 steps) with drift tracking.

Usage:
  uv run python scripts/train_world_model_v7.py --name v7_final --dataset dataset/some_dataset.json --iterations 20 --batch_size 16
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
from tqdm import tqdm

METRIC_NAMES = ['Instructions', 'Size', 'Complexity', 'Loops', 'Calls', 'Blocks']

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v7 import WorldModelV7
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

# Custom Data Object with HBC support
class TransitionDataV7(Data):
    def __init__(self, **kwargs):
        if 'block_map' in kwargs and kwargs['block_map'] is None:
            kwargs['block_map'] = torch.arange(kwargs['x'].size(0), dtype=torch.long)
        if 'next_block_map' in kwargs and kwargs['next_block_map'] is None:
            kwargs['next_block_map'] = torch.arange(kwargs['next_x'].size(0), dtype=torch.long)
        super().__init__(**kwargs)

    def __inc__(self, key, value, *args, **kwargs):
        if key == 'next_edge_index':
            return self.next_x.size(0)
        if key == 'block_map':
            return self.num_blocks
        if key == 'next_block_map':
            return self.next_num_blocks
        return super().__inc__(key, value, *args, **kwargs)

def collect_data_v7(env, transitions_needed=1000):
    transitions = []
    pbar = tqdm(total=transitions_needed, desc="[v7] Collecting Data", unit="step", leave=False)
    
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
                
                # V7.2: Capture all 6 metrics from the environment
                m_instr = (next_info['instructions_after'] - next_info['instructions_before']) / max(next_info['instructions_before'], 1) * 100.0
                m_size = (next_info['size_after'] - next_info['size_before']) / max(next_info['size_before'], 1) * 100.0
                m_comp = (next_info['complexity_after'] - next_info['complexity_before']) / max(next_info['complexity_before'], 1) * 100.0
                m_loops = (next_info['loops_after'] - next_info['loops_before']) / max(next_info['loops_before'], 1) * 100.0
                m_calls = (next_info['calls_after'] - next_info['calls_before']) / max(next_info['calls_before'], 1) * 100.0
                m_blocks = (next_info['blocks_after'] - next_info['blocks_before']) / max(next_info['blocks_before'], 1) * 100.0
                
                metrics = torch.tensor([m_instr, m_size, m_comp, m_loops, m_calls, m_blocks], dtype=torch.float32)
                
                # V7.2 Active Contrast (Keep meaningful changes in ANY of the 6 dimensions)
                is_noop = (metrics.abs().max() < 0.01)
                if is_noop and random.random() < 0.90:
                    continue

                # V7.3: Calculate and store number of blocks for correct batching
                b_map = getattr(curr_graph, 'block_map', None)
                if b_map is None: b_map = torch.arange(curr_graph.x.size(0), dtype=torch.long)
                n_blocks = b_map.max().item() + 1

                nb_map = getattr(next_graph, 'block_map', None)
                if nb_map is None: nb_map = torch.arange(next_graph.x.size(0), dtype=torch.long)
                next_n_blocks = nb_map.max().item() + 1

                transitions.append(TransitionDataV7(
                    x=curr_graph.x, 
                    edge_index=curr_graph.edge_index,
                    edge_attr=getattr(curr_graph, 'edge_attr', torch.zeros(curr_graph.edge_index.size(1), dtype=torch.long)),
                    block_map=b_map,
                    num_blocks=n_blocks,
                    action=torch.tensor([action], dtype=torch.long),
                    y_metrics=metrics.unsqueeze(0),
                    next_x=next_graph.x, 
                    next_edge_index=next_graph.edge_index,
                    next_edge_attr=getattr(next_graph, 'edge_attr', torch.zeros(next_graph.edge_index.size(1), dtype=torch.long)),
                    next_block_map=nb_map,
                    next_num_blocks=next_n_blocks
                ))
                pbar.update(1)
                curr_graph = next_graph
                if len(transitions) >= transitions_needed: break
                if terminated or truncated: break
        except Exception as e: 
            continue
    pbar.close()
    return transitions[:transitions_needed]

def run_lookahead_eval_v7(model, env, steps=15):
    model.eval()
    errors = []
    
    bench_paths = env.benchmark_paths
    val_subset = random.sample(bench_paths, min(len(bench_paths), 5))
    
    pbar = tqdm(total=len(val_subset) * steps, desc="[v7] Lookahead Eval", unit="step", leave=False)
    
    with torch.no_grad():
        for bench in val_subset:
            try:
                env.reset(options={"skip_canonicalization": True, "ir_path": str(bench)})
                curr_graph = env.get_observation_graph()
                if curr_graph is None: continue
                
                curr_state_emb = model.gnn_encoder(
                    curr_graph.x, 
                    curr_graph.edge_index, 
                    curr_graph.edge_attr,
                    block_map=getattr(curr_graph, 'block_map', None)
                )
                
                bench_errors = []
                for s in range(steps):
                    action = random.randint(0, NUM_ACTIONS - 1)
                    
                    _, _, _, _, info = env.step(action)
                    real_next_graph = env.get_observation_graph()
                    if real_next_graph is None: break
                    
                    real_next_emb = model.gnn_encoder(
                        real_next_graph.x, 
                        real_next_graph.edge_index, 
                        real_next_graph.edge_attr,
                        block_map=getattr(real_next_graph, 'block_map', None)
                    )
                    
                    real_inst_reduction = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
                    
                    action_onehot = torch.zeros(1, NUM_ACTIONS, device=curr_state_emb.device)
                    action_onehot[0, action] = 1.0
                    
                    num_nodes = curr_graph.x.size(0) - 1
                    
                    pred_next_emb, pred_metrics = model.transition_step(curr_state_emb, action_onehot, num_nodes=num_nodes)
                    
                    pred_inst_red = pred_metrics[0, 0].item() / 100.0 # Rescale from *100
                    
                    cos_sim = F.cosine_similarity(pred_next_emb, real_next_emb).item()
                    drift = 1.0 - cos_sim
                    met_err = abs(pred_inst_red - real_inst_reduction)
                    
                    bench_errors.append({
                        'step': s + 1,
                        'drift': drift,
                        'metric_err': met_err
                    })
                    
                    curr_state_emb = pred_next_emb 
                    pbar.update(1)
                    
                errors.append(bench_errors)
            except Exception as e:
                continue
    pbar.close()
            
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

def check_action_sensitivity(model, env, num_checks=5):
    """
    Verifies that the model predicts DIFFERENT values for DIFFERENT actions.
    Returns 'Sensitivity' (mean pairwise diff). 0.0 means total Action-Blindness.
    """
    model.eval()
    diffs = []
    
    with torch.no_grad():
        try:
            # Get a fresh state
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None: return 0.0
            
            state_emb = model.encode_graph(graph)
            num_nodes = graph.x.size(0) - 1
            
            predictions = []
            # Check a few diverse actions: some atomic, some macros
            test_actions = random.sample(range(NUM_ACTIONS), num_checks)
            
            for action in test_actions:
                action_onehot = torch.zeros(1, NUM_ACTIONS, device=state_emb.device)
                action_onehot[0, action] = 1.0
                _, pred_metrics = model.transition_step(state_emb, action_onehot, num_nodes=num_nodes)
                predictions.append(pred_metrics[0, 0].item()) # Instruction prediction
            
            # Calculate mean pairwise absolute difference
            for i in range(len(predictions)):
                for j in range(i + 1, len(predictions)):
                    diffs.append(abs(predictions[i] - predictions[j]))
                    
        except Exception as e:
            return 0.0
            
    return np.mean(diffs) if diffs else 0.0


def train_world_model_v7(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks)
    
    log_dir = Path(args.log_dir) / args.name
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    model = WorldModelV7(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=args.gnn_layers).to(device)
    
    # Can use higher LR because Two-Hot Categorical Cross Entropy is very stable compared to MSE
    optimizer = optim.Adam(model.parameters(), lr=1e-4) 
    
    if args.load_checkpoint:
        ckpt = torch.load(args.load_checkpoint, map_location=device, weights_only=False)
        model.load_state_dict(ckpt.get('model_state_dict', ckpt), strict=False)
        print(f"[v7] Warm-started from {args.load_checkpoint}")

    replay_buffer = []

    if args.dataset:
        dataset_path = Path(args.dataset)
        if dataset_path.exists():
            print(f"[v7] Loading offline dataset: {args.dataset}")
            try:
                with open(args.dataset, 'r') as f:
                    data_list = json.load(f)
                    
                added = 0
                for d in data_list:
                    if 'x' in d and 'edge_index' in d and 'next_x' in d:
                        # Convert to percentages for V7 SymLog distribution
                        metrics = torch.tensor(d['metrics'], dtype=torch.float)
                        metrics[0:2] *= 100.0
                        
                        # V7.3: Ensure block_map batching is safe for offline data
                        bm = torch.tensor(d.get('block_map', []), dtype=torch.long) if 'block_map' in d else None
                        if bm is not None and bm.numel() == 0: bm = None
                        if bm is None: bm = torch.arange(torch.tensor(d['x']).size(0), dtype=torch.long)
                        nbm = torch.tensor(d.get('next_block_map', []), dtype=torch.long) if 'next_block_map' in d else None
                        if nbm is not None and nbm.numel() == 0: nbm = None
                        if nbm is None: nbm = torch.arange(torch.tensor(d['next_x']).size(0), dtype=torch.long)
                        
                        replay_buffer.append(TransitionDataV7(
                            x=torch.tensor(d['x'], dtype=torch.float),
                            edge_index=torch.tensor(d['edge_index'], dtype=torch.long),
                            edge_attr=torch.tensor(d.get('edge_attr', [0]*len(d['edge_index'][0])), dtype=torch.long),
                            block_map=bm,
                            num_blocks=bm.max().item() + 1,
                            action=torch.tensor([d['action']], dtype=torch.long),
                            y_metrics=metrics.unsqueeze(0),
                            next_x=torch.tensor(d['next_x'], dtype=torch.float),
                            next_edge_index=torch.tensor(d['next_edge_index'], dtype=torch.long),
                            next_edge_attr=torch.tensor(d.get('next_edge_attr', [0]*len(d['next_edge_index'][0])), dtype=torch.long),
                            next_block_map=nbm,
                            next_num_blocks=nbm.max().item() + 1
                        ))
                        added += 1
                
                if added == 0:
                    print(f"[v7] WARNING: Dataset {args.dataset} contains 0 valid valid transitions.")
                else:
                    print(f"[v7] Loaded {added} valid transitions from offline dataset.")
            except Exception as e:
                print(f"[v7] Failed to load dataset: {e}. Falling back to online collection.")

    best_lookahead = float('inf')
    
    # V7.4: Stability - Learning Rate Decay
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    
    # Stability/Persistence Fix: Larger initial buffer
    if len(replay_buffer) < args.steps_per_iter * 2:
        print(f"[v7] Initial buffer too small. Collecting {args.steps_per_iter * 2} fresh transitions for stability...")
        replay_buffer.extend(collect_data_v7(env, transitions_needed=args.steps_per_iter * 2))

    # V7.2: Loss Weighting
    lambda_metrics = 5.0 # Give metrics more signal since they are harder to learn than cosine drift
    
    iter_pbar = tqdm(range(args.iterations), desc="[v7] Training Iterations", unit="iter")
    for it in iter_pbar:
        # LR Decay: Reduce LR over time to lock in the "Brain"
        current_lr = args.lr * (0.85 ** (it // 2))
        for param_group in optimizer.param_groups:
            param_group['lr'] = current_lr
        
        new_data = collect_data_v7(env, transitions_needed=args.steps_per_iter // 5)
        replay_buffer.extend(new_data)
        if len(replay_buffer) > 40000: replay_buffer = replay_buffer[-40000:]
        
        train_loader = DataLoader(replay_buffer, batch_size=args.batch_size, shuffle=True, follow_batch=['x', 'next_x'])
        model.train()
        
        epoch_losses_total = []
        epoch_losses_s = []
        epoch_losses_m = []
        
        # Collapse Diagnostics
        metric_var_ratios = []
        state_spreads = []
        
        epoch_pbar = tqdm(range(args.epochs_per_iter), desc=f"  Iter {it+1} Epochs", unit="epoch", leave=False)
        for epoch in epoch_pbar:
            for b_idx, batch in enumerate(train_loader):
                batch = batch.to(device)
                optimizer.zero_grad()
                
                # V7.3.1: Batch Structural Sanity Check (First batch of iteration 1 only)
                if it == 0 and epoch == 0 and b_idx == 0:
                    print(f"\n[v7] [SANITY CHECK] First Batch Structure:")
                    print(f"  - Instructions: {batch.x.size(0)}")
                    print(f"  - Blocks (scattered): {batch.block_map.max().item() + 1}")
                    print(f"  - Total Graphs in Batch: {batch.num_graphs}")
                    print(f"  - Avg Blocks/Graph: {(batch.block_map.max().item() + 1) / batch.num_graphs:.1f}")
                
                actions_onehot = torch.zeros(batch.action.size(0), NUM_ACTIONS, device=device).scatter_(1, batch.action.view(-1, 1), 1.0)
                
                # Get lengths required for context projector
                with torch.no_grad():
                    _, counts = torch.unique(batch.batch, return_counts=True)
                    num_nodes_batch = torch.clamp(counts - 1, min=1)
                
                # The V7 Model now jointly predicts state transition & directly returns the Two-Hot CE loss for metrics!
                pred_next, loss_m, pred_metrics = model(
                    state_emb=None, 
                    action_onehot=actions_onehot, 
                    target_metrics=batch.y_metrics,
                    graph_data=batch,
                    num_nodes=num_nodes_batch
                )
                
                with torch.no_grad():
                    target_next_raw = model.gnn_encoder(
                        batch.next_x, 
                        batch.next_edge_index, 
                        batch.next_edge_attr, 
                        batch=batch.next_x_batch,
                        block_map=getattr(batch, 'next_block_map', None)
                    )
                    
                    # --- COLLAPSE DIAGNOSTICS: Metric Variance Ratio ---
                    # Higher is better. 0.0 means the model is just predicting the average (collapse).
                    # V7.2.1: Use a mask to avoid division by zero on sparse metrics
                    var_pred = torch.var(pred_metrics, dim=0)
                    var_target = torch.var(batch.y_metrics, dim=0)
                    
                    # Only compute ratio for metrics that actually vary in this batch
                    valid_mask = var_target > 1e-4
                    if valid_mask.any():
                        ratios = var_pred[valid_mask] / var_target[valid_mask]
                        var_ratio = ratios.mean().item()
                    else:
                        var_ratio = 1.0 # Default to 1 (not collapsed) if the batch is uniform
                        
                    metric_var_ratios.append(var_ratio)
                    
                    # --- COLLAPSE DIAGNOSTICS: State Spread ---
                    # Average Euclidean distance between batch embeddings.
                    # If this drops to near-zero, all states are mapping to the same point.
                    pdist = F.pairwise_distance(pred_next[0:1], pred_next).mean()
                    state_spreads.append(pdist.item())
                
                loss_s = 1.0 - F.cosine_similarity(pred_next, target_next_raw).mean()
                
                # V7 Loss combines State Drift (Cosine) + Metrics CE
                loss = loss_s + (lambda_metrics * loss_m)
                
                if not torch.isfinite(loss):
                    print(f"\n[!!!] Non-finite loss detected: {loss.item()}! Skipping batch.")
                    optimizer.zero_grad()
                    continue
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                
                epoch_losses_total.append(loss.item())
                epoch_losses_s.append(loss_s.item())
                epoch_losses_m.append(loss_m.item())
            
            epoch_pbar.set_postfix({
                "loss": f"{np.mean(epoch_losses_total):.3f}",
                "var_r": f"{np.mean(metric_var_ratios):.3f}",
                "spread": f"{np.mean(state_spreads):.3f}"
            })
        
        avg_loss = np.mean(epoch_losses_total)
        avg_s = np.mean(epoch_losses_s)
        avg_m = np.mean(epoch_losses_m)
        avg_var_r = np.mean(metric_var_ratios)
        avg_spread = np.mean(state_spreads)
        
        print(f"\n[v7] Iteration {it+1} Results:")
        print(f"  Avg Total Loss: {avg_loss:.4f} (State: {avg_s:.4f}, Metrics: {avg_m:.4f})")
        print(f"  Collapse Check: VarRatio={avg_var_r:.4f}, StateSpread={avg_spread:.4f}")
        
        writer.add_scalar('Loss/Iter', avg_loss, it)
        writer.add_scalar('Loss/State', avg_s, it)
        writer.add_scalar('Loss/Metrics_CE', avg_m, it)
        writer.add_scalar('Collapse/Metric_Var_Ratio', avg_var_r, it)
        writer.add_scalar('Collapse/State_Spread', avg_spread, it)
        
        # 3. Evaluation
        report = run_lookahead_eval_v7(model, env, steps=10)
        sensitivity = check_action_sensitivity(model, env)
        
        print(f"=== V7 Lookahead Report (Iter {it+1}) ===")
        print(f"  Action Sensitivity: {sensitivity:.4f} " + ("[OK]" if sensitivity > 1e-4 else "[!!! BLIND !!!]"))
        
        for row in report:
            print(f"  Step {row['step']:02d}: Drift={row['avg_drift']:.4f}, MetricErr={row['avg_metric_err']:.4f}")
            writer.add_scalar(f'Eval/Drift_Step_{row["step"]}', row['avg_drift'], it)
        
        writer.add_scalar('Eval/Action_Sensitivity', sensitivity, it)
        
        # V7.4: Step the scheduler after each iteration
        scheduler.step()
        print(f"  [LR] Current Learning Rate: {scheduler.get_last_lr()[0]:.2e}")

        # 4. Save Checkpoints
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        iter_path = MODELS_DIR / f"world_model_v7_{args.name}_{timestamp_file}_iter_{it+1}.pth"
        
        save_dict = {
            'model_state_dict': model.state_dict(),
            'avg_loss': avg_loss,
            'iteration': it,
            'sensitivity': sensitivity,
            'timestamp': timestamp_file
        }
        
        torch.save(save_dict, iter_path)
        print(f"  [+] Saved unique checkpoint: {iter_path.name}")
        
        # Also keep a symlink-style 'latest' for secondary scripts
        latest_path = MODELS_DIR / f"world_model_v7_{args.name}_latest.pth"
        torch.save(save_dict, latest_path)
        
        if report[4]['avg_drift'] < best_lookahead:
            best_lookahead = report[4]['avg_drift']
            best_path = MODELS_DIR / f"world_model_v7_{args.name}_{timestamp_file}_best.pth"
            torch.save(save_dict, best_path)
            print(f"  [*] New Best Lookahead: {best_lookahead:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--steps_per_iter", type=int, default=1000)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--epochs_per_iter", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-4) # Base LR for decay
    parser.add_argument("--name", type=str, default="v7_dev")
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--log_dir", type=str, default="runs/world_model_v7")
    parser.add_argument("--load_checkpoint", type=str, default=None)
    args = parser.parse_args()
    train_world_model_v7(args)
