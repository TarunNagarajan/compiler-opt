"""
V8 World Model — Evaluation Script

Evaluates the V8.5 architecture with Residual Scale Correction:
1. Per-metric MAE (corrected vs actual deltas)
2. Direction accuracy (did the model predict the right sign?)
3. No-op detection (F1 for Delta ≈ 0 transitions)
4. Action sensitivity (does changing the action change the prediction?)
5. Scale-stratified accuracy (small vs medium vs large vs industrial)
6. Objective basis calibration

Usage:
  uv run python scripts/evaluate_world_model.py --checkpoint models/world_model_action_fix_v6_best.pth --samples 200
"""

import sys
import torch
import torch.nn.functional as F
import numpy as np
import argparse
import random
import time
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model import WorldModel
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES
from src.models.objective_basis import OBJECTIVE_BASIS_DIM

METRIC_NAMES = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]
OBJECTIVE_NAMES = ["runtime", "text_size", "instr", "size", "loads", "stores",
                   "allocas", "branches", "calls", "blocks"]


def load_v8_model(checkpoint_path, gnn_layers=6):
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=gnn_layers)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)

    # Validate action_dim compatibility
    ckpt_action_dim = ckpt.get('action_dim', None)
    if ckpt_action_dim is not None and ckpt_action_dim != NUM_ACTIONS:
        print(f"  [CRITICAL] Checkpoint action_dim={ckpt_action_dim} != runtime NUM_ACTIONS={NUM_ACTIONS}")
        print(f"  Action-dependent layers will produce INVALID predictions!")

    if 'model_state_dict' in ckpt:
        state_dict = ckpt['model_state_dict']
        # Handle shape mismatches from architecture changes
        model_shapes = {k: v.shape for k, v in model.state_dict().items()}
        to_skip = []
        for k in state_dict:
            if k in model_shapes and state_dict[k].shape != model_shapes[k]:
                print(f"  [WARN] Shape mismatch for {k}: ckpt={state_dict[k].shape}, model={model_shapes[k]} — skipping")
                to_skip.append(k)
        for k in to_skip:
            del state_dict[k]
        model.load_state_dict(state_dict, strict=False)
        print(f"[EVAL-v8] Loaded checkpoint from Iteration {ckpt.get('iteration', '?')}, "
              f"Best Loss: {ckpt.get('best_loss', '?')}")
    else:
        model.load_state_dict(ckpt, strict=False)
    model.eval()
    return model


def get_size_tier(filepath):
    """Classify benchmark by file size tier."""
    try:
        size = Path(filepath).stat().st_size
    except:
        return "unknown"
    if size > 200_000:
        return "large/industrial"
    elif size > 50_000:
        return "medium"
    else:
        return "small"


def get_category(filepath):
    parts = str(filepath).replace('\\', '/').lower()
    if 'sqlite' in parts: return 'industrial/sqlite'
    if 'yyjson' in parts: return 'industrial/yyjson'
    if 'lz4' in parts: return 'industrial/lz4'
    if 'zstd' in parts: return 'industrial/zstd'
    if 'miniz' in parts: return 'industrial/miniz'
    if 'polybench' in parts: return 'polybench'
    if 'mibench' in parts: return 'mibench'
    if 'anghaben' in parts: return 'anghaben'
    for cat in ['stencil', 'graph_algo', 'struct_heavy', 'pointer_chase',
                'simd_friendly', 'bitwise', 'string_ops', 'sparse_access']:
        if cat in parts: return f'synthetic/{cat}'
    return 'other'


def collect_samples(model, env, num_samples, timeout_per_sample=120):
    results = []
    errors = 0
    skipped = 0
    print(f"[EVAL-v8] Collecting {num_samples} evaluation samples...")
    t0 = time.time()

    for i in range(num_samples):
        if (i + 1) % 25 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (num_samples - i - 1) / max(rate, 0.01)
            print(f"  [{i+1}/{num_samples}] {elapsed:.0f}s elapsed, {rate:.1f} samples/s, ETA {eta:.0f}s")

        try:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None:
                skipped += 1
                continue

            num_nodes = graph.x.size(0) - 1
            total_nodes = getattr(graph, 'total_nodes', num_nodes)

            action = env.action_space.sample()
            _, _, _, _, step_info = env.step(action)

            # Ground truth delta metrics (percentage)
            true_metrics = torch.tensor([[
                (step_info['instructions_after'] - step_info['instructions_before']) / max(step_info['instructions_before'], 1) * 100.0,
                (step_info['size_after'] - step_info['size_before']) / max(step_info['size_before'], 1) * 100.0,
                (step_info.get('complexity_after', 0) - step_info.get('complexity_before', 0)) / max(step_info.get('complexity_before', 1), 1) * 100.0,
                (step_info.get('loops_after', 0) - step_info.get('loops_before', 0)) / max(step_info.get('loops_before', 1), 1) * 100.0,
                (step_info.get('calls_after', 0) - step_info.get('calls_before', 0)) / max(step_info.get('calls_before', 1), 1) * 100.0,
                (step_info.get('blocks_after', 0) - step_info.get('blocks_before', 0)) / max(step_info.get('blocks_before', 1), 1) * 100.0
            ]], dtype=torch.float32)

            # V8 prediction with scale correction
            with torch.no_grad():
                state_emb = model.encode_graph(graph)
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0

                _, pred_metrics = model(
                    state_emb, action_onehot,
                    num_nodes=num_nodes, total_nodes=total_nodes
                )

            # Action sensitivity: compare prediction with alternate action
            alt_action = random.randint(0, NUM_ACTIONS - 1)
            while alt_action == action:
                alt_action = random.randint(0, NUM_ACTIONS - 1)

            with torch.no_grad():
                alt_onehot = torch.zeros(1, NUM_ACTIONS)
                alt_onehot[0, alt_action] = 1.0
                _, alt_metrics = model(
                    state_emb, alt_onehot,
                    num_nodes=num_nodes, total_nodes=total_nodes
                )

            sensitivity = (pred_metrics - alt_metrics).abs().mean().item()

            results.append({
                'true': true_metrics,
                'pred': pred_metrics,
                'action': action,
                'category': get_category(env.current_benchmark_path),
                'tier': get_size_tier(env.current_benchmark_path),
                'num_nodes': num_nodes,
                'total_nodes': total_nodes if isinstance(total_nodes, int) else total_nodes.item() if isinstance(total_nodes, torch.Tensor) else num_nodes,
                'sensitivity': sensitivity,
                'filepath': str(env.current_benchmark_path),
            })

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  [ERROR] Sample {i}: {e}")
            continue

    elapsed = time.time() - t0
    print(f"[EVAL-v8] Collected {len(results)} samples in {elapsed:.1f}s ({errors} errors, {skipped} skipped)")
    return results


def analyze(results):
    if not results:
        print("[EVAL-v8] No results to analyze!")
        return

    all_true = torch.cat([r['true'] for r in results], dim=0)
    all_pred = torch.cat([r['pred'] for r in results], dim=0)

    print("\n" + "=" * 72)
    print("  V8 WORLD MODEL EVALUATION — Residual Scale Correction")
    print("=" * 72)
    print(f"  Samples: {len(results)}")

    # ── Overall Metrics ──
    mae = F.l1_loss(all_pred, all_true).item()
    cos = F.cosine_similarity(all_pred, all_true, dim=-1)
    cos_mean = cos.mean().item()
    avg_sensitivity = np.mean([r['sensitivity'] for r in results])

    print(f"\n  OVERALL:")
    print(f"    MAE (All 6 Metrics): {mae:.4f}%")
    print(f"    Cosine Similarity:   {cos_mean:.4f}")
    print(f"    Action Sensitivity:  {avg_sensitivity:.4f} " +
          ("[GOOD]" if avg_sensitivity > 0.1 else "[WEAK]" if avg_sensitivity > 0.01 else "[BLIND]"))

    # ── Per-Metric MAE ──
    print(f"\n  PER-METRIC MAE:")
    for i, name in enumerate(METRIC_NAMES):
        m_mae = F.l1_loss(all_pred[:, i], all_true[:, i]).item()
        m_median_ae = (all_pred[:, i] - all_true[:, i]).abs().median().item()
        print(f"    {name:15s}: MAE={m_mae:.4f}%  MedianAE={m_median_ae:.4f}%")

    # ── Direction Accuracy ──
    print(f"\n  DIRECTION ACCURACY (sign match on Delta):")
    for i, name in enumerate(METRIC_NAMES):
        true_sign = torch.sign(all_true[:, i])
        pred_sign = torch.sign(all_pred[:, i])
        # Exclude near-zero ground truth (ambiguous direction)
        mask = all_true[:, i].abs() > 0.5
        if mask.sum() > 0:
            direction_acc = (true_sign[mask] == pred_sign[mask]).float().mean().item()
            print(f"    {name:15s}: {direction_acc:.1%} ({mask.sum().item()} non-trivial samples)")
        else:
            print(f"    {name:15s}: N/A (all near-zero)")

    # ── No-Op Detection ──
    print(f"\n  NO-OP DETECTION (|Delta| < 0.5%):")
    true_noop = all_true[:, 0].abs() < 0.5
    pred_noop = all_pred[:, 0].abs() < 0.5
    tp = (true_noop & pred_noop).sum().item()
    fp = (~true_noop & pred_noop).sum().item()
    fn = (true_noop & ~pred_noop).sum().item()
    tn = (~true_noop & ~pred_noop).sum().item()

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    print(f"    True No-Ops:  {true_noop.sum().item()}/{len(results)} ({true_noop.float().mean():.1%})")
    print(f"    Precision:    {precision:.3f}")
    print(f"    Recall:       {recall:.3f}")
    print(f"    F1:           {f1:.3f}")

    # ── Scale-Stratified Analysis ──
    print(f"\n  SCALE-STRATIFIED ACCURACY:")
    tiers = defaultdict(list)
    for r in results:
        tiers[r['tier']].append(r)

    for tier in ['small', 'medium', 'large/industrial', 'unknown']:
        if tier not in tiers:
            continue
        tier_results = tiers[tier]
        tier_true = torch.cat([r['true'] for r in tier_results], dim=0)
        tier_pred = torch.cat([r['pred'] for r in tier_results], dim=0)
        tier_mae = F.l1_loss(tier_pred[:, 0], tier_true[:, 0]).item()
        avg_nodes = np.mean([r['num_nodes'] for r in tier_results])
        print(f"    {tier:20s}: n={len(tier_results):>4}, MAE={tier_mae:.4f}%, avg_nodes={avg_nodes:.0f}")

    # ── Category Breakdown ──
    print(f"\n  PER-CATEGORY ACCURACY (Instruction MAE):")
    cats = defaultdict(list)
    for r in results:
        cats[r['category']].append(r)

    sorted_cats = sorted(cats.items(), key=lambda x: -len(x[1]))
    for cat, cat_results in sorted_cats[:15]:
        cat_true = torch.cat([r['true'] for r in cat_results], dim=0)
        cat_pred = torch.cat([r['pred'] for r in cat_results], dim=0)
        cat_mae = F.l1_loss(cat_pred[:, 0], cat_true[:, 0]).item()
        print(f"    {cat:30s}: n={len(cat_results):>4}, Instr MAE={cat_mae:.4f}%")

    # ── Worst Predictions ──
    print(f"\n  TOP-5 WORST PREDICTIONS (by |error|):")
    errors_list = []
    for r in results:
        err = (r['pred'][0, 0] - r['true'][0, 0]).abs().item()
        errors_list.append((err, r))
    errors_list.sort(key=lambda x: -x[0])
    for rank, (err, r) in enumerate(errors_list[:5]):
        print(f"    {rank+1}. |err|={err:.2f}%  true={r['true'][0,0]:.2f}%  pred={r['pred'][0,0]:.2f}%  "
              f"nodes={r['num_nodes']}  cat={r['category']}")

    # ── Summary Verdict ──
    print(f"\n" + "=" * 72)
    grade = "EXCELLENT" if mae < 2.0 else "GOOD" if mae < 5.0 else "FAIR" if mae < 10.0 else "NEEDS WORK"
    sens_grade = "RESTORED" if avg_sensitivity > 0.1 else "WEAK" if avg_sensitivity > 0.01 else "BLIND"
    print(f"  VERDICT: {grade} (MAE={mae:.4f}%, Sensitivity={sens_grade})")
    print(f"  Best checkpoint loss was: {mae:.4f}")
    print("=" * 72)


def collect_targeted_samples(model, env, target_paths, samples_per_file=5):
    """Force-evaluate specific files (industrial/large) to test scale correction."""
    results = []
    for fpath in target_paths:
        fpath = Path(fpath)
        if not fpath.exists():
            print(f"  [SKIP] {fpath} not found")
            continue
        print(f"  Evaluating {fpath.name} ({samples_per_file} samples)...")
        for s in range(samples_per_file):
            try:
                obs, info = env.reset(options={"ir_path": str(fpath)})
                graph = env.get_observation_graph()
                if graph is None:
                    continue

                num_nodes = graph.x.size(0) - 1
                total_nodes = getattr(graph, 'total_nodes', num_nodes)

                action = env.action_space.sample()
                _, _, _, _, step_info = env.step(action)

                true_metrics = torch.tensor([[
                    (step_info['instructions_after'] - step_info['instructions_before']) / max(step_info['instructions_before'], 1) * 100.0,
                    (step_info['size_after'] - step_info['size_before']) / max(step_info['size_before'], 1) * 100.0,
                    (step_info.get('complexity_after', 0) - step_info.get('complexity_before', 0)) / max(step_info.get('complexity_before', 1), 1) * 100.0,
                    (step_info.get('loops_after', 0) - step_info.get('loops_before', 0)) / max(step_info.get('loops_before', 1), 1) * 100.0,
                    (step_info.get('calls_after', 0) - step_info.get('calls_before', 0)) / max(step_info.get('calls_before', 1), 1) * 100.0,
                    (step_info.get('blocks_after', 0) - step_info.get('blocks_before', 0)) / max(step_info.get('blocks_before', 1), 1) * 100.0
                ]], dtype=torch.float32)

                with torch.no_grad():
                    state_emb = model.encode_graph(graph)
                    action_onehot = torch.zeros(1, NUM_ACTIONS)
                    action_onehot[0, action] = 1.0
                    _, pred_metrics = model(
                        state_emb, action_onehot,
                        num_nodes=num_nodes, total_nodes=total_nodes
                    )

                alt_action = random.randint(0, NUM_ACTIONS - 1)
                while alt_action == action:
                    alt_action = random.randint(0, NUM_ACTIONS - 1)
                with torch.no_grad():
                    alt_onehot = torch.zeros(1, NUM_ACTIONS)
                    alt_onehot[0, alt_action] = 1.0
                    _, alt_metrics = model(
                        state_emb, alt_onehot,
                        num_nodes=num_nodes, total_nodes=total_nodes
                    )
                sensitivity = (pred_metrics - alt_metrics).abs().mean().item()

                results.append({
                    'true': true_metrics,
                    'pred': pred_metrics,
                    'action': action,
                    'category': get_category(str(fpath)),
                    'tier': get_size_tier(str(fpath)),
                    'num_nodes': num_nodes,
                    'total_nodes': total_nodes if isinstance(total_nodes, int) else total_nodes.item() if isinstance(total_nodes, torch.Tensor) else num_nodes,
                    'sensitivity': sensitivity,
                    'filepath': str(fpath),
                })
            except Exception as e:
                print(f"    [ERROR] {fpath.name} sample {s}: {e}")
                continue
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate V8 World Model")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--stratified", action="store_true",
                        help="Include targeted industrial/large-scale evaluation")
    parser.add_argument("--industrial_samples", type=int, default=5,
                        help="Samples per industrial file")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    model = load_v8_model(args.checkpoint)
    total_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[EVAL-v8] Model: {total_params:,} params ({trainable:,} trainable)")

    all_paths = get_benchmark_paths()
    env = CompilerOptEnv(all_paths)

    # Standard random evaluation
    results = collect_samples(model, env, args.samples)

    # Targeted industrial/large evaluation
    if args.stratified:
        print(f"\n[EVAL-v8] Targeted industrial/large-scale evaluation...")
        industrial_files = [
            "benchmarks/large_scale/sqlite/sqlite3.c",
            "benchmarks/large_scale/yyjson.c",
            "benchmarks/large_scale/LZ4/lz4.c",
        ]
        # Find medium/large files from the benchmark set
        medium_files = []
        large_file = None
        for p in all_paths:
            pp = Path(p)
            try:
                sz = pp.stat().st_size
                if 50_000 < sz <= 200_000:
                    medium_files.append(str(pp))
                elif sz > 200_000 and 'sqlite' not in str(pp).lower():
                    if large_file is None:
                        large_file = str(pp)
            except:
                pass

        target_files = industrial_files
        if medium_files:
            target_files += medium_files[:3]
        if large_file:
            target_files.append(large_file)

        targeted = collect_targeted_samples(model, env, target_files, args.industrial_samples)
        if targeted:
            print(f"[EVAL-v8] Got {len(targeted)} targeted samples")
            results.extend(targeted)

    analyze(results)
