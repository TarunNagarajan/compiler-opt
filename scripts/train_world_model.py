import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data
from torch.utils.data import DataLoader as VanillaDataLoader
import numpy as np
import argparse
from pathlib import Path
from tqdm import tqdm
import json
import random
import time
import os
import sys
import gc

sys.path.append(os.getcwd())

from src.models.world_model import WorldModel
from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.config import NUM_ACTIONS, FEATURE_DIM, BENCHMARKS_DIR, get_benchmark_paths

def set_global_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def to_scalar_tensor(value, default=100.0):
    if value is None:
        return torch.tensor([default], dtype=torch.float32)
    if isinstance(value, torch.Tensor):
        flat = value.detach().to(dtype=torch.float32, device='cpu').view(-1)
        return flat[:1].clone() if flat.numel() > 0 else torch.tensor([default], dtype=torch.float32)
    if isinstance(value, (list, tuple, np.ndarray)):
        arr = np.asarray(value, dtype=np.float32).reshape(-1)
        return torch.tensor([float(arr[0])], dtype=torch.float32) if arr.size > 0 else torch.tensor([default], dtype=torch.float32)
    return torch.tensor([float(value)], dtype=torch.float32)


def quick_eval(model, env, device, num_samples=30):
    """Lightweight inline eval: returns (mae, sensitivity)."""
    model.eval()
    errors = []
    sensitivities = []
    for _ in range(num_samples):
        try:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None:
                continue
            action = env.action_space.sample()
            _, _, _, _, step_info = env.step(action)

            true_delta = torch.tensor([[
                (step_info['instructions_after'] - step_info['instructions_before']) / max(step_info['instructions_before'], 1) * 100.0,
                (step_info['size_after'] - step_info['size_before']) / max(step_info['size_before'], 1) * 100.0,
                (step_info.get('complexity_after', 0) - step_info.get('complexity_before', 0)) / max(step_info.get('complexity_before', 1), 1) * 100.0,
                (step_info.get('loops_after', 0) - step_info.get('loops_before', 0)) / max(step_info.get('loops_before', 1), 1) * 100.0,
                (step_info.get('calls_after', 0) - step_info.get('calls_before', 0)) / max(step_info.get('calls_before', 1), 1) * 100.0,
                (step_info.get('blocks_after', 0) - step_info.get('blocks_before', 0)) / max(step_info.get('blocks_before', 1), 1) * 100.0
            ]], dtype=torch.float32)

            with torch.no_grad():
                graph = graph.to(device)
                state_emb = model.encode_graph(graph)
                action_oh = torch.zeros(1, NUM_ACTIONS, device=device)
                action_oh[0, action] = 1.0
                num_nodes = graph.x.size(0) - 1
                _, pred = model.transition_step(state_emb, action_oh, num_nodes=num_nodes)
                pred_cpu = pred.cpu()

                alt = random.randint(0, NUM_ACTIONS - 1)
                while alt == action:
                    alt = random.randint(0, NUM_ACTIONS - 1)
                alt_oh = torch.zeros(1, NUM_ACTIONS, device=device)
                alt_oh[0, alt] = 1.0
                _, alt_pred = model.transition_step(state_emb, alt_oh, num_nodes=num_nodes)

            errors.append(F.l1_loss(pred_cpu, true_delta).item())
            sensitivities.append(abs(pred[0, 0].item() - alt_pred[0, 0].item()))
        except Exception:
            continue
    model.train()
    mae = np.mean(errors) if errors else 999.0
    sens = np.mean(sensitivities) if sensitivities else 0.0
    return mae, sens


class TransitionDataV8(Data):
    """PyG Data object for V8 transitions."""
    def __init__(self, **kwargs):
        # Only compute block maps if we have the raw node data (Phase 2)
        if 'x' in kwargs and kwargs['x'] is not None:
            if 'block_map' in kwargs and kwargs['block_map'] is None:
                kwargs['block_map'] = torch.arange(kwargs['x'].size(0), dtype=torch.long)
            if 'next_block_map' in kwargs and kwargs['next_block_map'] is None:
                kwargs['next_block_map'] = torch.arange(kwargs['next_x'].size(0), dtype=torch.long)
        super().__init__(**kwargs)

    def __inc__(self, key, value, *args, **kwargs):
        if key == 'next_edge_index' and hasattr(self, 'next_x'):
            return self.next_x.size(0)
        if key == 'block_map' and hasattr(self, 'num_blocks'):
            return self.num_blocks
        if key == 'next_block_map' and hasattr(self, 'next_num_blocks'):
            return self.next_num_blocks
        return super().__inc__(key, value, *args, **kwargs)


def collect_transitions(env, model, device, transitions_needed=500, include_noops=True, store_graphs=False, rng=None):
    """
    V8.5: Collects transitions and pre-computes graph embeddings (Embed-Once Opt).
    Since base model is frozen in Phase 1, we only need the fixed state_emb vectors.
    """
    transitions = []
    noop_count = 0
    active_count = 0
    pbar = tqdm(total=transitions_needed, desc="  Collecting", unit="step", leave=False)
    
    model.eval()
    rng = rng or random
    while len(transitions) < transitions_needed:
        obs, info = env.reset(seed=rng.randint(0, 2**31 - 1))
        graph_data = env.get_observation_graph()
        
        for _ in range(env.max_steps):
            if graph_data is None: break
            
            # Embed-Once: Compute state_emb now so we don't do it inside the 15-epoch loop
            with torch.no_grad():
                gd = graph_data.to(device)
                encoded = model.encode_graph(gd).detach().cpu()
                if encoded.dim() == 2 and encoded.size(0) == 1:
                    state_emb = encoded.squeeze(0)
                elif encoded.dim() == 1:
                    state_emb = encoded
                else:
                    raise ValueError(f"Unexpected encoded state shape: {tuple(encoded.shape)}")
                
            action = rng.randint(0, NUM_ACTIONS - 1)
            
            local_nodes = max(int(graph_data.x.size(0)) - 1, 1)
            total_nodes = to_scalar_tensor(getattr(graph_data, 'total_nodes', None), default=float(local_nodes))
            
            next_obs, reward, terminated, truncated, info = env.step(action)
            next_graph_data = env.get_observation_graph()
            
            if next_graph_data is not None:
                # Logic to determine instruct/size change
                i_before = info.get('instructions_before', 0)
                i_after = info.get('instructions_after', 0)
                
                y_metrics = torch.tensor([
                    (i_after - i_before) / max(i_before, 1) * 100.0,
                    (info.get('size_after', 0) - info.get('size_before', 0)) / max(info.get('size_before', 1), 1) * 100.0,
                    (info.get('complexity_after', 0) - info.get('complexity_before', 0)) / max(info.get('complexity_before', 1), 1),
                    (info.get('loops_after', 0) - info.get('loops_before', 0)) / max(info.get('loops_before', 1), 1),
                    (info.get('calls_after', 0) - info.get('calls_before', 0)) / max(info.get('calls_before', 1), 1),
                    (info.get('blocks_after', 0) - info.get('blocks_before', 0)) / max(info.get('blocks_before', 1), 1)
                ], dtype=torch.float)
                
                is_noop = torch.abs(y_metrics).sum() < 1e-5
                if is_noop:
                    noop_ratio = noop_count / max(noop_count + active_count, 1)
                    if not include_noops or noop_ratio > 0.4:
                        graph_data = next_graph_data
                        if terminated or truncated or graph_data is None: break
                        continue
                    noop_count += 1
                else:
                    active_count += 1
                
                # Store EVERYTHING needed based on phase
                kwargs = {
                    'state_emb': state_emb.clone(),
                    'num_nodes': torch.tensor([float(local_nodes)], dtype=torch.float32),
                    'action': torch.tensor([action], dtype=torch.long),
                    'y_metrics': y_metrics,
                    'total_nodes': total_nodes.clone(),
                }
                
                if store_graphs:
                    kwargs['x'] = graph_data.x.clone()
                    kwargs['edge_index'] = graph_data.edge_index.clone()
                    if hasattr(graph_data, 'edge_attr') and graph_data.edge_attr is not None:
                        kwargs['edge_attr'] = graph_data.edge_attr.clone()
                    
                transitions.append(TransitionDataV8(**kwargs))
                pbar.update(1)
                if len(transitions) >= transitions_needed: break
            
            graph_data = next_graph_data
            if terminated or truncated or graph_data is None: break
            
    pbar.close()
    total = active_count + noop_count
    print(f"    Collected {len(transitions)}: "
          f"{active_count} active ({active_count/max(total,1)*100:.0f}%), "
          f"{noop_count} no-ops ({noop_count/max(total,1)*100:.0f}%)")
    return transitions


def get_industrial_benchmarks():
    """Returns paths to industrial-scale benchmark files."""
    INDUSTRIAL_KEYWORDS = {'sqlite', 'lz4', 'yyjson', 'cjson', 'tinyxml2',
                           'miniz', 'stb_image', 'zstd', 'brotli'}
    all_bench = get_benchmark_paths()
    industrial = [p for p in all_bench if any(kw in p.name.lower() for kw in INDUSTRIAL_KEYWORDS)]
    diverse = [p for p in all_bench if p not in industrial]
    return industrial, diverse


def train_v8(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    set_global_seed(args.seed)
    print(f"[v8.5] Using seed: {args.seed}")
    
    industrial_bench, diverse_bench = get_industrial_benchmarks()
    print(f"[v8.5] Industrial: {len(industrial_bench)} files, Diverse: {len(diverse_bench)} files")
    
    # Create environments
    diverse_env = CompilerOptEnv(diverse_bench, max_steps=10, reward_mode=RewardMode.HACKABLE)
    industrial_env = CompilerOptEnv(industrial_bench, max_steps=10, reward_mode=RewardMode.HACKABLE) if industrial_bench else None
    
    # Initialize model
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    
    # Load checkpoint with compatibility handling
    ckpt = torch.load(args.load_checkpoint, map_location=device, weights_only=False)
    state_dict = ckpt.get('model_state_dict', ckpt)
    
    # Handle older checkpoints missing scale_correction or with 2D size_proj
    size_proj_key = 'size_proj.weight'
    if size_proj_key in state_dict and state_dict[size_proj_key].shape[1] == 2:
        print(f"[v8.5] Migrating size_proj 2D → 3D")
        old_w = state_dict[size_proj_key]
        new_w = torch.zeros(old_w.shape[0], 3); new_w[:, :2] = old_w
        nn.init.xavier_uniform_(new_w[:, 2:3])
        state_dict[size_proj_key] = new_w
    
    # Remove scale_correction keys from checkpoint (we want fresh zero-init)
    sc_keys = [k for k in state_dict if 'scale_correction' in k]
    for k in sc_keys:
        del state_dict[k]
    
    model.load_state_dict(state_dict, strict=False)
    print(f"[v8.5] Loaded checkpoint: {args.load_checkpoint}")
    print(f"[v8.5] scale_correction initialized to ZERO (fresh start)")
    
    # =========================================================================
    # TWO-PHASE TRAINING
    # =========================================================================
    if args.mode == "correction":
        train_correction_phase(model, diverse_env, industrial_env, args, device)
    elif args.mode == "full":
        train_full_phase(model, diverse_env, industrial_env, args, device)
    else:
        raise ValueError(f"Unknown mode: {args.mode}")


def train_correction_phase(model, diverse_env, industrial_env, args, device):
    """
    PHASE 1: Correction-Only Training
    
    Freeze the ENTIRE base model. Train ONLY the scale_correction network.
    
    Data: Mixed (70% diverse + 30% industrial)
    - The correction must learn to output ~0 on diverse benchmarks (base is accurate)
    - The correction must learn the right adjustment on industrial benchmarks
    
    This is impossible to cause catastrophic forgetting because we don't touch
    the base model weights at all.
    """
    print(f"\n{'='*60}")
    print(f"[PHASE 1] Correction-Only Training")
    print(f"{'='*60}")
    
    # Freeze everything except scale_correction
    for name, param in model.named_parameters():
        if 'scale_correction' not in name:
            param.requires_grad = False
    
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"[PHASE 1] Training {trainable}/{total} parameters ({trainable/total*100:.1f}%)")
    
    optimizer = optim.Adam(
        [p for p in model.parameters() if p.requires_grad],
        lr=1e-3  # Higher LR for the small correction network
    )
    
    replay_buffer = []
    best_loss = float('inf')
    rng = random.Random(args.seed)
    
    for it in range(args.iterations):
        print(f"\n--- Iteration {it+1}/{args.iterations} ---")
        
        # Collect data: 50/50 balanced mix for Phase 1
        diverse_steps = int(args.steps_per_iter * 0.50)
        industrial_steps = args.steps_per_iter - diverse_steps
        
        new_data = collect_transitions(
            diverse_env, model, device, diverse_steps, include_noops=True, store_graphs=False, rng=rng
        )
        if industrial_env and industrial_steps > 0:
            print(f"    Collecting {industrial_steps} industrial transitions...")
            new_data.extend(
                collect_transitions(
                    industrial_env, model, device, industrial_steps, include_noops=True, store_graphs=False, rng=rng
                )
            )
        
        replay_buffer.extend(new_data)
        if len(replay_buffer) > args.buffer_size:
            replay_buffer = replay_buffer[-args.buffer_size:]
        print(f"    Replay buffer: {len(replay_buffer)}")
        
        # Optimization: Use a custom collate that only batches vectors, ignoring heavy graphs
        def correction_collate(batch):
            return {
                'state_emb': torch.stack([b.state_emb for b in batch]),
                'action': torch.stack([b.action for b in batch]),
                'y_metrics': torch.stack([b.y_metrics for b in batch]),
                'total_nodes': torch.stack([b.total_nodes for b in batch]),
                'num_nodes': torch.stack([b.num_nodes for b in batch])
            }
            
        from torch.utils.data import DataLoader as VanillaDataLoader
        dl_generator = torch.Generator().manual_seed(args.seed + it)
        train_loader = VanillaDataLoader(replay_buffer, batch_size=args.batch_size, 
                                          shuffle=True, collate_fn=correction_collate, generator=dl_generator)
        model.train()
        gc.collect()
        
        optimizer = optim.Adam(
            [p for p in model.parameters() if p.requires_grad],
            lr=5e-4  # Slightly more conservative for the 64x64 network
        )
        
        epoch_pbar = tqdm(range(args.epochs), desc="  Training", unit="epoch")
        for epoch in epoch_pbar:
            total_loss = 0; n = 0
            for batch in train_loader:
                # Use dict access for the batched tensors
                s_emb = batch['state_emb'].to(device)
                if s_emb.dim() == 3 and s_emb.size(1) == 1:
                    s_emb = s_emb.squeeze(1)
                if s_emb.dim() != 2:
                    raise ValueError(f"Unexpected state_emb batch shape: {tuple(s_emb.shape)}")

                y_true = batch['y_metrics'].to(device)
                if y_true.dim() == 3 and y_true.size(1) == 1:
                    y_true = y_true.squeeze(1)
                if y_true.dim() != 2:
                    raise ValueError(f"Unexpected y_metrics batch shape: {tuple(y_true.shape)}")

                act_idx = batch['action'].to(device).view(-1)     # [batch]
                t_nodes = batch['total_nodes'].to(device).view(-1, 1).clamp(min=1.0)
                n_nodes = batch['num_nodes'].to(device).view(-1, 1).clamp(min=1.0)
                
                optimizer.zero_grad()
                
                actions_onehot = torch.zeros(s_emb.size(0), NUM_ACTIONS, device=device)
                actions_onehot.scatter_(1, act_idx.view(-1, 1), 1.0)
                
                # Scale-weighted importance sampling
                # Use .view(-1) to ensure 1D vectors for element-wise multiplication
                weights = (1.0 + torch.log10(t_nodes / 100.0).clamp(min=0.0)).view(-1)
                actual_abs = torch.abs(y_true).sum(dim=-1).view(-1)
                noop_mask = (actual_abs < 1e-3).float()
                weights = weights * (1.0 + 1.0 * noop_mask)
                
                # EMBED-ONCE: Pass state_emb directly, no graph_data
                _, loss, _ = model(
                    state_emb=s_emb, action_onehot=actions_onehot,
                    target_metrics=y_true, graph_data=None,
                    num_nodes=n_nodes, total_nodes=t_nodes, sample_weights=weights
                )
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                total_loss += loss.item(); n += 1
            
            avg = total_loss / max(n, 1)
            epoch_pbar.set_postfix(loss=f"{avg:.4f}")
        
        if avg < best_loss:
            best_loss = avg
            torch.save({'model_state_dict': model.state_dict(), 'phase': 'correction', 'iteration': it},
                       f"models/world_model_{args.phase}_best.pth")
            print(f"    [BEST] {best_loss:.4f} (Saved best checkpoint)")
        
        torch.save({'model_state_dict': model.state_dict(), 'phase': 'correction', 'iteration': it},
                   f"models/world_model_{args.phase}_iter_{it+1}.pth")
        print(f"    [SAVED] Iteration {it+1} checkpoint")
    
    # Unfreeze for potential Phase 2
    for param in model.parameters():
        param.requires_grad = True
    
    torch.save({'model_state_dict': model.state_dict(), 'phase': 'correction_done'},
               f"models/world_model_{args.phase}_final.pth")
    print(f"\n[PHASE 1] Complete. Best loss: {best_loss:.4f}")


def train_full_phase(model, diverse_env, industrial_env, args, device):
    """
    PHASE 2: Targeted Head Fine-Tuning (anti-overfit design)

    Freezes GNN encoder, state_proj, action_gate, transition (~80% of params).
    Only trains: metrics_head, size_proj, scale_correction, action_correction_emb.
    Uses AdamW with weight_decay for regularization + CosineAnnealingLR.
    """
    print(f"\n{'='*60}")
    print(f"[PHASE 2] Targeted Head Fine-Tuning (GNN frozen)")
    print(f"{'='*60}")

    # Freeze the expensive, already-trained components
    frozen_parts = ('gnn_encoder', 'state_proj', 'action_gate', 'transition')
    trainable_parts = ('scale_correction', 'size_proj', 'action_correction_emb', 'metrics_head')

    for name, param in model.named_parameters():
        param.requires_grad = any(part in name for part in trainable_parts)

    total_count = sum(p.numel() for p in model.parameters())
    frozen_count = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    trainable_count = total_count - frozen_count
    print(f"[PHASE 2] Frozen: {frozen_count:,} params ({frozen_count/total_count*100:.1f}%)")
    print(f"[PHASE 2] Trainable: {trainable_count:,} params ({trainable_count/total_count*100:.1f}%)")

    param_groups = [
        {'params': model.size_proj.parameters(),       'lr': 1e-4,  'name': 'size_proj'},
        {'params': model.metrics_head.parameters(),    'lr': 1e-4,  'name': 'metrics_head'},
        {'params': model.action_correction_emb.parameters(), 'lr': 3e-4, 'name': 'action_correction_emb'},
        {'params': model.scale_correction.parameters(),'lr': 3e-4,  'name': 'scale_correction'},
    ]
    optimizer = optim.AdamW(param_groups, weight_decay=1e-4)
    total_steps_estimate = args.iterations * args.epochs * max(args.steps_per_iter // args.batch_size, 1)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=total_steps_estimate, eta_min=1e-6)

    for pg in param_groups:
        print(f"    {pg['name']:<25}: {pg['lr']}")

    replay_buffer = []
    best_loss = float('inf')
    rng = random.Random(args.seed)

    for it in range(args.iterations):
        print(f"\n--- Iteration {it+1}/{args.iterations} ---")

        diverse_steps = int(args.steps_per_iter * 0.85)
        industrial_steps = args.steps_per_iter - diverse_steps

        # GNN is frozen → use Embed-Once (store_graphs=False, pre-computed state_emb)
        new_data = collect_transitions(
            diverse_env, model, device, diverse_steps, include_noops=True, store_graphs=False, rng=rng
        )
        if industrial_env and industrial_steps > 0:
            print(f"    Collecting {industrial_steps} industrial transitions...")
            new_data.extend(
                collect_transitions(
                    industrial_env, model, device, industrial_steps, include_noops=True, store_graphs=False, rng=rng
                )
            )

        replay_buffer.extend(new_data)
        if len(replay_buffer) > args.buffer_size:
            replay_buffer = replay_buffer[-args.buffer_size:]
        print(f"    Replay buffer: {len(replay_buffer)}")

        def _collate(batch):
            return {
                'state_emb': torch.stack([b.state_emb for b in batch]),
                'action': torch.stack([b.action for b in batch]),
                'y_metrics': torch.stack([b.y_metrics for b in batch]),
                'total_nodes': torch.stack([b.total_nodes for b in batch]),
                'num_nodes': torch.stack([b.num_nodes for b in batch]),
            }

        dl_generator = torch.Generator().manual_seed(args.seed + it)
        train_loader = VanillaDataLoader(replay_buffer, batch_size=args.batch_size,
                                         shuffle=True, collate_fn=_collate, generator=dl_generator)
        model.train()
        gc.collect()

        epoch_pbar = tqdm(range(args.epochs), desc="  Training", unit="epoch")
        for epoch in epoch_pbar:
            total_loss = 0; n = 0
            for batch in train_loader:
                s_emb = batch['state_emb'].to(device)
                if s_emb.dim() == 3 and s_emb.size(1) == 1:
                    s_emb = s_emb.squeeze(1)
                y_true = batch['y_metrics'].to(device)
                if y_true.dim() == 3 and y_true.size(1) == 1:
                    y_true = y_true.squeeze(1)
                act_idx = batch['action'].to(device).view(-1)
                t_nodes = batch['total_nodes'].to(device).view(-1, 1).clamp(min=1.0)
                n_nodes = batch['num_nodes'].to(device).view(-1, 1).clamp(min=1.0)

                optimizer.zero_grad()

                actions_onehot = torch.zeros(s_emb.size(0), NUM_ACTIONS, device=device)
                actions_onehot.scatter_(1, act_idx.view(-1, 1), 1.0)

                weights = (1.0 + torch.log10(t_nodes / 100.0).clamp(min=0.0)).view(-1)
                # Down-weight no-ops to prevent bias toward predicting zero
                actual_abs = torch.abs(y_true).sum(dim=-1).view(-1)
                noop_mask = (actual_abs < 1e-3).float()
                weights = weights * (1.0 - 0.5 * noop_mask)

                _, loss, _ = model(
                    state_emb=s_emb, action_onehot=actions_onehot,
                    target_metrics=y_true, graph_data=None,
                    num_nodes=n_nodes, total_nodes=t_nodes, sample_weights=weights
                )

                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                total_loss += loss.item(); n += 1

            avg = total_loss / max(n, 1)
            epoch_pbar.set_postfix(loss=f"{avg:.4f}", lr=f"{optimizer.param_groups[0]['lr']:.2e}")

        # Quick inline eval
        eval_mae, eval_sens = quick_eval(model, diverse_env, device, num_samples=30)
        print(f"    [EVAL] MAE={eval_mae:.4f}%, Sensitivity={eval_sens:.4f}")

        if avg < best_loss:
            best_loss = avg
            torch.save({'model_state_dict': model.state_dict(), 'phase': 'full', 'iteration': it,
                        'action_dim': NUM_ACTIONS},
                       f"models/world_model_{args.phase}_best.pth")
            print(f"    [BEST] {best_loss:.4f} (Saved best checkpoint)")

        torch.save({'model_state_dict': model.state_dict(), 'phase': 'full', 'iteration': it,
                    'action_dim': NUM_ACTIONS},
                   f"models/world_model_{args.phase}_iter_{it+1}.pth")
        print(f"    [SAVED] Iteration {it+1} checkpoint")

    torch.save({'model_state_dict': model.state_dict(), 'phase': 'full_done', 'action_dim': NUM_ACTIONS},
               f"models/world_model_{args.phase}_final.pth")
    print(f"\n[PHASE 2] Complete. Best loss: {best_loss:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="V8.5 World Model Training with Residual Scale Correction")
    parser.add_argument("--load_checkpoint", type=str, required=True)
    parser.add_argument("--mode", type=str, choices=["correction", "full"], default="correction",
                        help="'correction' = Phase 1 (freeze base, train correction only). "
                             "'full' = Phase 2 (gentle full fine-tuning)")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--steps_per_iter", type=int, default=1000)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--buffer_size", type=int, default=8000)
    parser.add_argument("--phase", type=str, default="v8.5")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for deterministic training")
    args = parser.parse_args()
    
    train_v8(args)
