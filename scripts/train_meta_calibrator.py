import argparse
import json
import os
import random
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler

sys.path.append(os.getcwd())

from src.config import NUM_ACTIONS
from src.models.meta_calibrator import MetaCalibrator

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def safe_split_size(n: int, ratio: float = 0.9):
    if n <= 1:
        return n
    size = int(ratio * n)
    size = max(1, min(size, n - 1))
    return size


def grouped_benchmark_split(benchmark_ids, ratio=0.9, seed=1337):
    """Leakage-safe split that keeps each benchmark entirely in train or val."""
    groups = {}
    for idx, bench in enumerate(benchmark_ids):
        key = bench if bench else f"__unknown__{idx}"
        groups.setdefault(key, []).append(idx)

    keys = list(groups.keys())
    rng = random.Random(seed)
    rng.shuffle(keys)

    total = len(benchmark_ids)
    target_train = max(1, min(int(total * ratio), max(total - 1, 1)))
    train_idx = []
    val_idx = []

    remaining = total
    for key in keys:
        idxs = groups[key]
        remaining -= len(idxs)
        force_val = (len(val_idx) == 0 and remaining == 0)
        if len(train_idx) < target_train and not force_val:
            train_idx.extend(idxs)
        else:
            val_idx.extend(idxs)

    if total > 1 and len(val_idx) == 0 and len(train_idx) > 1:
        moved = train_idx.pop()
        val_idx.append(moved)
    if len(train_idx) == 0 and len(val_idx) > 1:
        moved = val_idx.pop()
        train_idx.append(moved)

    return torch.tensor(train_idx, dtype=torch.long), torch.tensor(val_idx, dtype=torch.long)


def parse_threshold_grid(spec: str):
    if spec:
        values = []
        for token in spec.split(','):
            token = token.strip()
            if not token:
                continue
            values.append(float(token))
    else:
        values = [x / 100.0 for x in range(10, 91, 5)]

    clipped = [min(max(v, 0.01), 0.99) for v in values]
    unique = sorted(set(clipped))
    if not unique:
        unique = [0.4]
    return unique


def select_split_indices(num_samples, split_ratio, seed, split_strategy, benchmark_ids):
    use_benchmark_split = split_strategy == "benchmark" and benchmark_ids is not None and any(benchmark_ids)
    if use_benchmark_split:
        train_idx, val_idx = grouped_benchmark_split(benchmark_ids, ratio=split_ratio, seed=seed)
        if train_idx.numel() > 0 and val_idx.numel() > 0:
            return train_idx, val_idx, "benchmark"
        print("[WARN] Benchmark split could not produce non-empty train/val. Falling back to random split.")

    train_size = safe_split_size(num_samples, ratio=split_ratio)
    split_gen = torch.Generator().manual_seed(seed)
    indices = torch.randperm(num_samples, generator=split_gen)
    train_idx, val_idx = indices[:train_size], indices[train_size:]
    return train_idx, val_idx, "random"


def tune_inference_threshold(model, v8_preds, actions, scales, truths, device, threshold_grid):
    if v8_preds.numel() == 0:
        return 0.4, {"mae": float("nan"), "inst_mae": float("nan"), "threshold": 0.4}

    model.eval()
    with torch.no_grad():
        v8 = v8_preds.to(device)
        act = actions.to(device)
        scl = scales.to(device)
        y_true = truths.to(device)

        best = None
        for threshold in threshold_grid:
            pred = model(v8, act, scl, threshold=threshold)
            mae = torch.mean(torch.abs(pred - y_true)).item()
            inst_mae = torch.mean(torch.abs(pred[:, 0] - y_true[:, 0])).item()
            if best is None or mae < best["mae"]:
                best = {"threshold": float(threshold), "mae": float(mae), "inst_mae": float(inst_mae)}

    return best["threshold"], best


def train_meta_calibrator(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    set_seed(args.seed)
    print(f"Using seed: {args.seed}")
    
    # 1. Load Dataset
    dataset_path = args.dataset
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Run collect_meta_dataset.py first.")
        
    raw_data = torch.load(dataset_path, map_location='cpu')
    if len(raw_data) == 0:
        raise ValueError("Meta-calibration dataset is empty. Collect dataset first.")
    print(f"Loaded {len(raw_data)} samples from {dataset_path}")
    
    # 2. Convert to Tensors
    v8_preds = torch.stack([d['v8_prediction'] for d in raw_data]).float()
    actions = torch.stack([d['action'] for d in raw_data]).float()
    scales = torch.stack([d['scale'] for d in raw_data]).float()
    truths = torch.stack([d['truth'] for d in raw_data]).float()
    if scales.dim() == 1:
        scales = scales.unsqueeze(1)
    elif scales.dim() == 2 and scales.size(1) != 1:
        scales = scales[:, :1]
    
    abs_truths = truths.abs().sum(dim=1)
    binary_labels = (abs_truths > 1e-5).float().unsqueeze(1)
    
    num_nonzeros = binary_labels.sum().item()
    num_zeros = len(binary_labels) - num_nonzeros
    print(f"Dataset Stats: {int(num_zeros)} Zeroes, {int(num_nonzeros)} Non-Zeros.")
    
    benchmark_ids = [str(d.get('benchmark', '')) for d in raw_data]
    # 3. Split Train/Val (configurable)
    num_samples = len(raw_data)
    train_idx, val_idx, split_used = select_split_indices(
        num_samples=num_samples,
        split_ratio=args.split_ratio,
        seed=args.seed,
        split_strategy=args.split_strategy,
        benchmark_ids=benchmark_ids,
    )
    print(
        f"Split strategy: {split_used} | "
        f"Train={int(train_idx.numel())} samples, Val={int(val_idx.numel())} samples"
    )
    
    # Gate Datasets (All Data)
    gate_train_dataset = TensorDataset(v8_preds[train_idx], actions[train_idx], scales[train_idx], binary_labels[train_idx])
    gate_val_dataset = TensorDataset(v8_preds[val_idx], actions[val_idx], scales[val_idx], binary_labels[val_idx])
    
    # Weighted Sampler for Gate
    train_labels = binary_labels[train_idx].view(-1)
    train_nonzeros = train_labels.sum().item()
    train_zeros = len(train_labels) - train_nonzeros
    pos_weight = torch.tensor([train_zeros / max(train_nonzeros, 1)], device=device)
    print(
        f"Gate Train Stats: {int(train_zeros)} Zeroes, {int(train_nonzeros)} Non-Zeros. "
        f"pos_weight={pos_weight.item():.2f}"
    )
    train_loader_gen = torch.Generator().manual_seed(args.seed + 1)
    if train_nonzeros > 0 and train_zeros > 0:
        weight_neg = 1.0 / float(train_zeros)
        weight_pos = 1.0 / float(train_nonzeros)
        sample_weights = torch.where(train_labels > 0.5, torch.tensor(weight_pos), torch.tensor(weight_neg)).float()
        sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True, generator=train_loader_gen)
        gate_train_loader = DataLoader(gate_train_dataset, batch_size=args.batch_size, sampler=sampler)
    else:
        gate_train_loader = DataLoader(gate_train_dataset, batch_size=args.batch_size, shuffle=True, generator=train_loader_gen)
    gate_val_loader = DataLoader(gate_val_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Magnitude Datasets (Only nonzero true labels)
    nonzero_mask = abs_truths > 1e-5
    mag_train_idx = train_idx[nonzero_mask[train_idx]]
    mag_val_idx = val_idx[nonzero_mask[val_idx]]

    # Keep stage-2 split leakage-safe by deriving from the same train/val partition.
    if mag_train_idx.numel() > 1 and mag_val_idx.numel() == 0:
        mag_val_idx = mag_train_idx[-1:].clone()
        mag_train_idx = mag_train_idx[:-1]
    if mag_train_idx.numel() == 0 and mag_val_idx.numel() > 1:
        mag_train_idx = mag_val_idx[-1:].clone()
        mag_val_idx = mag_val_idx[:-1]

    m_num = int(mag_train_idx.numel() + mag_val_idx.numel())
    if mag_train_idx.numel() > 0 and mag_val_idx.numel() > 0:
        mag_train_dataset = TensorDataset(
            v8_preds[mag_train_idx], actions[mag_train_idx], scales[mag_train_idx], truths[mag_train_idx]
        )
        mag_val_dataset = TensorDataset(
            v8_preds[mag_val_idx], actions[mag_val_idx], scales[mag_val_idx], truths[mag_val_idx]
        )

        mag_loader_gen = torch.Generator().manual_seed(args.seed + 4)
        mag_train_loader = DataLoader(mag_train_dataset, batch_size=args.batch_size, shuffle=True, generator=mag_loader_gen)
        mag_val_loader = DataLoader(mag_val_dataset, batch_size=args.batch_size, shuffle=False)
    else:
        mag_train_loader = None
        mag_val_loader = None
    
    # 4. Model
    model = MetaCalibrator(pred_dim=6, action_dim=NUM_ACTIONS, hidden_dim=64).to(device)
    
    # ========================================
    # STAGE 1: Train Gate Network
    # ========================================
    print("\n--- STAGE 1: Training Gate Network (BCE) ---")
    gate_criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    gate_opt = optim.Adam(model.gate.parameters(), lr=args.lr, weight_decay=1e-5)
    
    best_gate_loss = float('inf')
    for epoch in range(args.gate_epochs):
        model.train()
        total_loss = 0
        for v8_p, act, scale, y_bin in gate_train_loader:
            v8_p, act, scale, y_bin = v8_p.to(device), act.to(device), scale.to(device), y_bin.to(device)
            gate_opt.zero_grad()
            logit, _ = model(v8_p, act, scale, return_gate_logit=True)
            loss = gate_criterion(logit, y_bin)
            loss.backward()
            gate_opt.step()
            total_loss += loss.item()
            
        train_loss = total_loss / max(len(gate_train_loader), 1)
        
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for v8_p, act, scale, y_bin in gate_val_loader:
                v8_p, act, scale, y_bin = v8_p.to(device), act.to(device), scale.to(device), y_bin.to(device)
                logit, _ = model(v8_p, act, scale, return_gate_logit=True)
                val_loss += gate_criterion(logit, y_bin).item()
        val_loss /= max(len(gate_val_loader), 1)
        
        if epoch % 5 == 0 or epoch == args.gate_epochs - 1:
            print(f"Gate Epoch {epoch+1:03d}/{args.gate_epochs} | Train BCE: {train_loss:.4f} | Val BCE: {val_loss:.4f}")
            
        if val_loss < best_gate_loss:
            best_gate_loss = val_loss
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            torch.save(model.state_dict(), args.output)
             
    # Load best gate before moving to magnitude
    model.load_state_dict(torch.load(args.output, map_location=device))
    
    # Freeze Gate
    for param in model.gate.parameters():
        param.requires_grad = False
        
    # ========================================
    # STAGE 2: Train Magnitude Network
    # ========================================
    skip_stage2 = False
    if m_num == 0 or mag_train_loader is None or mag_val_loader is None:
        print("\n[INFO] Insufficient non-zero train/val samples for Stage 2; skipping magnitude training.")
        skip_stage2 = True

    best_mag_loss = float('inf')
    if not skip_stage2:
        print("\n--- STAGE 2: Training Magnitude Network (Huber) ---")
        mag_criterion = nn.HuberLoss(delta=1.0)
        mag_opt = optim.Adam(list(model.magnitude.parameters()) + [model.learned_scale], lr=args.lr, weight_decay=1e-5)
        
        for epoch in range(args.mag_epochs):
            model.train()
            model.gate.eval() # Keep gate in eval mode for dropout/layernorm
            total_loss = 0
            for v8_p, act, scale, y_true in mag_train_loader:
                v8_p, act, scale, y_true = v8_p.to(device), act.to(device), scale.to(device), y_true.to(device)
                mag_opt.zero_grad()
                _, mag = model(v8_p, act, scale, return_gate_logit=True)
                loss = mag_criterion(mag, y_true)
                loss.backward()
                mag_opt.step()
                total_loss += loss.item()
                
            train_loss = total_loss / max(len(mag_train_loader), 1)
            
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for v8_p, act, scale, y_true in mag_val_loader:
                    v8_p, act, scale, y_true = v8_p.to(device), act.to(device), scale.to(device), y_true.to(device)
                    _, mag = model(v8_p, act, scale, return_gate_logit=True)
                    val_loss += mag_criterion(mag, y_true).item()
            val_loss /= max(len(mag_val_loader), 1)
            
            if epoch % 10 == 0 or epoch == args.mag_epochs - 1:
                print(f"Mag Epoch {epoch+1:03d}/{args.mag_epochs} | Train Huber: {train_loss:.4f} | Val Huber: {val_loss:.4f}")
                
            if val_loss < best_mag_loss:
                best_mag_loss = val_loss
                torch.save(model.state_dict(), args.output)
        
        print(f"\n[SUCCESS] Hurdle Meta-Calibrator trained! Best Mag Huber Loss: {best_mag_loss:.4f}")
    else:
        print("\n[SUCCESS] Gate-only Meta-Calibrator trained.")

    # Load best model and tune hard-gate threshold on holdout split.
    model.load_state_dict(torch.load(args.output, map_location=device))
    tune_idx = val_idx if val_idx.numel() > 0 else train_idx
    threshold_grid = parse_threshold_grid(args.threshold_grid)
    best_threshold, best_threshold_stats = tune_inference_threshold(
        model,
        v8_preds[tune_idx],
        actions[tune_idx],
        scales[tune_idx],
        truths[tune_idx],
        device,
        threshold_grid,
    )
    print(
        f"[Threshold Tune] best={best_threshold:.3f} "
        f"(MAE={best_threshold_stats['mae']:.4f}, InstMAE={best_threshold_stats['inst_mae']:.4f})"
    )

    meta_path = os.path.splitext(args.output)[0] + ".meta.json"
    metadata = {
        "inference_threshold": best_threshold,
        "split_strategy": split_used,
        "split_ratio": float(args.split_ratio),
        "val_samples": int(tune_idx.numel()),
        "seed": int(args.seed),
        "val_mae": best_threshold_stats["mae"],
        "val_inst_mae": best_threshold_stats["inst_mae"],
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model to {args.output}")
    print(f"Saved metadata to {meta_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="models/meta_dataset.pt")
    parser.add_argument("--gate_epochs", type=int, default=30) # Separate epochs
    parser.add_argument("--mag_epochs", type=int, default=100) # Separate epochs
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--split_ratio", type=float, default=0.9)
    parser.add_argument("--split_strategy", type=str, choices=["benchmark", "random"], default="benchmark")
    parser.add_argument("--threshold_grid", type=str, default="0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60")
    parser.add_argument("--output", type=str, default="models/meta_calibrator_best.pth")
    args = parser.parse_args()
    train_meta_calibrator(args)
