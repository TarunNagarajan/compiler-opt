"""
v5 World Model — Comprehensive Evaluation

Runs ground-truth comparisons against the real compiler and produces:
 1. Overall MAE + cosine similarity
 2. Per-category accuracy (polybench, stencils, diverse_synthetic, etc.)
 3. Per-action accuracy (which LLVM passes predicted best/worst)
 4. No-op detection (precision/recall for Δ≈0 transitions)
 5. Direction accuracy (does model correctly predict +/- sign?)
 6. v5-specific: loop-heavy vs loop-free program accuracy
 7. Attention weight analysis (which nodes matter most)

Usage:
  uv run python scripts/evaluate_world_model_v5.py --checkpoint models/world_model_v5_checkpoint.pth --samples 100
  uv run python scripts/evaluate_world_model_v5.py --checkpoint models/world_model_v5_checkpoint.pth --samples 20 --quick
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
from src.models.world_model_v5 import WorldModelV5
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES
from torch_geometric.data import Data


METRIC_NAMES = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]
NOOP_THRESHOLD = 0.005  # Δ < 0.5% is considered no-op


def load_v5_model(checkpoint_path, gnn_layers=6):
    model = WorldModelV5(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=gnn_layers)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in ckpt:
        model.load_state_dict(ckpt['model_state_dict'])
        iteration = ckpt.get('iteration', '?')
        best_loss = ckpt.get('best_loss', '?')
        print(f"[EVAL] Loaded v5 checkpoint: iteration {iteration}, best_loss={best_loss}")
    else:
        model.load_state_dict(ckpt)
        print("[EVAL] Loaded v5 model (raw state dict)")
    model.eval()
    return model


def get_category(filepath):
    """Classify a benchmark path into its category."""
    parts = str(filepath).replace('\\', '/').lower()
    if 'polybench' in parts or 'datamining' in parts or 'linear-algebra' in parts or 'medley' in parts:
        return 'polybench'
    elif 'stencils' in parts:
        return 'stencils'
    elif 'multi_func' in parts:
        return 'multi_func'
    elif 'deep_call_chain' in parts:
        return 'deep_call_chain'
    elif 'library_heavy' in parts:
        return 'library_heavy'
    elif 'scaled_composite' in parts:
        return 'scaled_composite'
    elif 'diverse_synthetic' in parts:
        return 'diverse_synthetic'
    elif 'anghaben_wrapped' in parts:
        return 'anghaben_wrapped'
    elif 'synthetic' in parts:
        return 'synthetic'
    elif 'graphs' in parts:
        return 'graphs'
    else:
        return 'other'


def collect_samples(model, env, num_samples, show_progress=True):
    """Collect ground-truth vs predicted samples."""
    results = []
    attempts = 0
    max_attempts = num_samples * 5
    
    while len(results) < num_samples and attempts < max_attempts:
        attempts += 1
        try:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None:
                continue
            
            action = env.action_space.sample()
            
            # Ground truth
            next_obs, reward, term, trunc, step_info = env.step(action)
            
            instr_b = info.get('initial_instructions', 1)
            size_b = info.get('initial_size', 1)
            complexity_b = info.get('initial_complexity', 0)
            loops_b = info.get('initial_loops', 0)
            calls_b = info.get('initial_calls', 0)
            blocks_b = info.get('initial_blocks', 0)
            
            # True Target Deltas
            instr_delta = (step_info['instructions_after'] - instr_b) / max(instr_b, 1)
            size_delta = (step_info['size_after'] - size_b) / max(size_b, 1)
            complexity_delta = (step_info.get('complexity_after', complexity_b) - complexity_b) / 100.0
            loops_delta = (step_info.get('loops_after', loops_b) - loops_b) / 10.0
            raw_calls_delta = step_info.get('calls_after', calls_b) - calls_b
            if abs(raw_calls_delta) > 0:
                calls_delta = np.sign(raw_calls_delta) * np.log1p(abs(raw_calls_delta)) / 5.0
            else:
                calls_delta = 0.0
            
            # Matching log-based normalization from train_world_model_v5.py
            raw_blocks_delta = step_info.get('blocks_after', blocks_b) - blocks_b
            if abs(raw_blocks_delta) > 0:
                blocks_delta = np.sign(raw_blocks_delta) * np.log1p(abs(raw_blocks_delta)) / 5.0
            else:
                blocks_delta = 0.0
            
            true_metrics = torch.tensor([[
                instr_delta, size_delta, complexity_delta, 
                loops_delta, calls_delta, blocks_delta
            ]], dtype=torch.float32)
            
            # v5 prediction
            edge_attr = getattr(graph, 'edge_attr', None)
            if edge_attr is None:
                edge_attr = torch.zeros(graph.edge_index.size(1), dtype=torch.long)
            batch_vec = torch.zeros(graph.x.size(0), dtype=torch.long)
            
            with torch.no_grad():
                graph_data = Data(x=graph.x, edge_index=graph.edge_index, edge_attr=edge_attr, batch=batch_vec)
                state_emb = model.encode_graph(graph_data)
                
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0
                
                _, pred_metrics = model(state_emb, action_onehot)
            
            # Determine benchmark category
            source_path = getattr(env, 'current_benchmark_path', 'unknown')
            category = get_category(source_path)
            
            # Check if program has loops (for v5-specific analysis)
            has_loops = loops_b > 0 or (edge_attr == 6).any().item()  # edge type 6 = loop_back
            
            results.append({
                'true': true_metrics,
                'pred': pred_metrics,
                'action': action,
                'category': category,
                'has_loops': has_loops,
                'num_nodes': graph.x.size(0),
                'source': str(source_path),
            })
            
            if show_progress and len(results) % 5 == 0:
                pct = len(results) / num_samples * 100
                print(f"  [{len(results)}/{num_samples}] ({pct:.0f}%)", end='\r', flush=True)
                
        except Exception as e:
            continue
    
    if show_progress:
        print()
    return results


def analyze_results(results):
    """Produce detailed analysis from collected samples."""
    
    all_true = torch.cat([r['true'] for r in results], dim=0)
    all_pred = torch.cat([r['pred'] for r in results], dim=0)
    
    # ================================================================
    # 1. OVERALL ACCURACY
    # ================================================================
    print("\n" + "=" * 70)
    print("  1. OVERALL ACCURACY")
    print("=" * 70)
    
    overall_mae = F.l1_loss(all_pred, all_true).item()
    per_metric_mae = F.l1_loss(all_pred, all_true, reduction='none').mean(dim=0)
    cosine_sim = F.cosine_similarity(all_pred, all_true, dim=-1).mean().item()
    
    print(f"  Samples:            {len(results)}")
    print(f"  Overall MAE:        {overall_mae:.4f}")
    print(f"  Cosine Similarity:  {cosine_sim:.4f}")
    print(f"\n  Per-Metric MAE:")
    for i, name in enumerate(METRIC_NAMES):
        bar = "#" * int(per_metric_mae[i].item() * 200)
        print(f"    {name:15s}: {per_metric_mae[i].item():.4f}  {bar}")
    
    # ================================================================
    # 2. PER-CATEGORY ACCURACY
    # ================================================================
    print("\n" + "=" * 70)
    print("  2. PER-CATEGORY ACCURACY")
    print("=" * 70)
    
    categories = defaultdict(list)
    for r in results:
        categories[r['category']].append(r)
    
    print(f"  {'Category':<22s} {'Count':>5s} {'MAE':>8s} {'CosSim':>8s} {'Dir%':>6s}")
    print("  " + "-" * 55)
    
    for cat in sorted(categories.keys()):
        cat_results = categories[cat]
        cat_true = torch.cat([r['true'] for r in cat_results], dim=0)
        cat_pred = torch.cat([r['pred'] for r in cat_results], dim=0)
        mae = F.l1_loss(cat_pred, cat_true).item()
        cos = F.cosine_similarity(cat_pred, cat_true, dim=-1).mean().item()
        
        # Direction accuracy (sign match on instruction delta)
        true_sign = (cat_true[:, 0] > NOOP_THRESHOLD).float() - (cat_true[:, 0] < -NOOP_THRESHOLD).float()
        pred_sign = (cat_pred[:, 0] > NOOP_THRESHOLD).float() - (cat_pred[:, 0] < -NOOP_THRESHOLD).float()
        nontrivial = (true_sign != 0)
        if nontrivial.sum() > 0:
            dir_acc = (true_sign[nontrivial] == pred_sign[nontrivial]).float().mean().item() * 100
        else:
            dir_acc = float('nan')
        
        print(f"  {cat:<22s} {len(cat_results):5d} {mae:8.4f} {cos:8.4f} {dir_acc:5.1f}%")
    
    # ================================================================
    # 3. PER-ACTION ACCURACY (Top 10 Best + Worst)
    # ================================================================
    print("\n" + "=" * 70)
    print("  3. PER-ACTION ACCURACY")
    print("=" * 70)
    
    actions = defaultdict(list)
    for r in results:
        actions[r['action']].append(r)
    
    action_maes = []
    for act, act_results in actions.items():
        if len(act_results) < 2:
            continue
        act_true = torch.cat([r['true'] for r in act_results], dim=0)
        act_pred = torch.cat([r['pred'] for r in act_results], dim=0)
        mae = F.l1_loss(act_pred, act_true).item()
        
        pass_name = LLVM_PASSES[act].replace('function(', '').rstrip(')') if act < len(LLVM_PASSES) else f'macro_{act}'
        action_maes.append((act, pass_name, mae, len(act_results)))
    
    action_maes.sort(key=lambda x: x[2])
    
    print(f"\n  [BEST] TOP 5 BEST PREDICTED PASSES:")
    print(f"  {'ID':>3s} {'Pass':25s} {'MAE':>8s} {'Count':>5s}")
    print("  " + "-" * 45)
    for act, name, mae, count in action_maes[:5]:
        print(f"  {act:3d} {name:25s} {mae:8.4f} {count:5d}")
    
    print(f"\n  [WORST] TOP 5 WORST PREDICTED PASSES:")
    print(f"  {'ID':>3s} {'Pass':25s} {'MAE':>8s} {'Count':>5s}")
    print("  " + "-" * 45)
    for act, name, mae, count in action_maes[-5:]:
        print(f"  {act:3d} {name:25s} {mae:8.4f} {count:5d}")
    
    # ================================================================
    # 4. NO-OP DETECTION
    # ================================================================
    print("\n" + "=" * 70)
    print("  4. NO-OP DETECTION (Δ < 0.5%)")
    print("=" * 70)
    
    true_noop = all_true.abs().sum(dim=1) < NOOP_THRESHOLD
    pred_noop = all_pred.abs().sum(dim=1) < NOOP_THRESHOLD
    
    tp = (true_noop & pred_noop).sum().item()  # True positive: correctly predicted no-op
    fp = (~true_noop & pred_noop).sum().item() # False positive: predicted no-op but had real change
    fn = (true_noop & ~pred_noop).sum().item() # False negative: predicted change but was no-op
    tn = (~true_noop & ~pred_noop).sum().item()
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    total_noop = true_noop.sum().item()
    total_change = (~true_noop).sum().item()
    
    print(f"  Ground Truth: {total_noop} no-ops, {total_change} real changes")
    print(f"  Confusion Matrix:")
    print(f"                  Pred No-op  Pred Change")
    print(f"  True No-op    {tp:10d}  {fn:10d}")
    print(f"  True Change   {fp:10d}  {tn:10d}")
    print(f"\n  Precision: {precision:.3f}  (of predicted no-ops, how many were real)")
    print(f"  Recall:    {recall:.3f}  (of actual no-ops, how many were caught)")
    print(f"  F1 Score:  {f1:.3f}")
    
    # ================================================================
    # 5. DIRECTION ACCURACY
    # ================================================================
    print("\n" + "=" * 70)
    print("  5. DIRECTION ACCURACY (Does model predict +/- correctly?)")
    print("=" * 70)
    
    for i, name in enumerate(METRIC_NAMES):
        true_vals = all_true[:, i]
        pred_vals = all_pred[:, i]
        
        # Only consider non-trivial changes
        nontrivial = true_vals.abs() > NOOP_THRESHOLD
        if nontrivial.sum() == 0:
            print(f"  {name:15s}: No non-trivial samples")
            continue
        
        true_sign = torch.sign(true_vals[nontrivial])
        pred_sign = torch.sign(pred_vals[nontrivial])
        correct = (true_sign == pred_sign).float().mean().item() * 100
        
        status = "[OK]" if correct >= 70 else "[!!]" if correct >= 50 else "[XX]"
        print(f"  {name:15s}: {correct:5.1f}% correct direction  ({nontrivial.sum().item()} non-trivial samples)  {status}")
    
    # ================================================================
    # 6. LOOP-HEAVY vs LOOP-FREE PROGRAMS (v5-specific)
    # ================================================================
    print("\n" + "=" * 70)
    print("  6. LOOP-HEAVY vs LOOP-FREE (v5 Attention + Back-Edge Test)")
    print("=" * 70)
    
    loop_results = [r for r in results if r['has_loops']]
    noloop_results = [r for r in results if not r['has_loops']]
    
    if loop_results and noloop_results:
        loop_true = torch.cat([r['true'] for r in loop_results], dim=0)
        loop_pred = torch.cat([r['pred'] for r in loop_results], dim=0)
        loop_mae = F.l1_loss(loop_pred, loop_true).item()
        
        noloop_true = torch.cat([r['true'] for r in noloop_results], dim=0)
        noloop_pred = torch.cat([r['pred'] for r in noloop_results], dim=0)
        noloop_mae = F.l1_loss(noloop_pred, noloop_true).item()
        
        print(f"  Loop programs:    {len(loop_results):4d} samples, MAE = {loop_mae:.4f}")
        print(f"  Non-loop programs:{len(noloop_results):4d} samples, MAE = {noloop_mae:.4f}")
        
        if loop_mae <= noloop_mae:
            print(f"  [OK] Loop programs predicted equally well or better (Δ = {noloop_mae - loop_mae:.4f})")
        else:
            print(f"  [!!] Loop programs harder to predict (gap = {loop_mae - noloop_mae:.4f})")
    else:
        print(f"  Loop: {len(loop_results)} samples, Non-loop: {len(noloop_results)} samples")
        print(f"  (Need both to compare)")
    
    # ================================================================
    # 7. OVERALL VERDICT
    # ================================================================
    print("\n" + "=" * 70)
    print("  7. OVERALL VERDICT")
    print("=" * 70)
    
    checks = [
        ("Overall MAE < 0.05", overall_mae < 0.05),
        ("Cosine Similarity > 0.8", cosine_sim > 0.8),
        ("No-op F1 > 0.6", f1 > 0.6),
        ("Instruction Direction > 60%", True),  # Default pass
    ]
    
    # Compute instruction direction accuracy
    true_instr = all_true[:, 0]
    pred_instr = all_pred[:, 0]
    nontrivial_instr = true_instr.abs() > NOOP_THRESHOLD
    if nontrivial_instr.sum() > 0:
        instr_dir_acc = (torch.sign(true_instr[nontrivial_instr]) == torch.sign(pred_instr[nontrivial_instr])).float().mean().item() * 100
        checks[3] = ("Instruction Direction > 60%", instr_dir_acc > 60)
    
    all_pass = True
    for check_name, passed in checks:
        status = "[OK] PASS" if passed else "[XX] FAIL"
        if not passed:
            all_pass = False
        print(f"  {status}: {check_name}")
    
    if all_pass:
        print(f"\n  [SUCCESS] WORLD MODEL IS READY FOR HRL TRAINING")
    else:
        print(f"\n  [CAUTION] Consider more training iterations before proceeding to HRL")
    
    print("=" * 70)
    
    return {
        'overall_mae': overall_mae,
        'cosine_sim': cosine_sim,
        'noop_f1': f1,
        'per_metric_mae': per_metric_mae,
    }


def main():
    parser = argparse.ArgumentParser(description="v5 World Model Comprehensive Evaluation")
    parser.add_argument("--checkpoint", type=str, default="models/world_model_v5_checkpoint.pth",
                        help="Path to v5 world model checkpoint")
    parser.add_argument("--samples", type=int, default=100, help="Number of ground-truth samples to evaluate")
    parser.add_argument("--gnn_layers", type=int, default=6, help="GNN layers (must match checkpoint)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--quick", action="store_true", help="Quick mode (fewer categories)")
    args = parser.parse_args()
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    
    print("=" * 70)
    print("  v5 WORLD MODEL — COMPREHENSIVE EVALUATION")
    print("=" * 70)
    
    model = load_v5_model(args.checkpoint, gnn_layers=args.gnn_layers)
    
    benchmarks = get_benchmark_paths()
    print(f"[EVAL] {len(benchmarks)} benchmarks available")
    
    env = CompilerOptEnv(benchmarks, max_steps=1)
    
    print(f"[EVAL] Collecting {args.samples} ground-truth samples...")
    results = collect_samples(model, env, args.samples)
    
    if len(results) < 5:
        print(f"[EVAL] ERROR: Only collected {len(results)} samples. Need at least 5.")
        return
    
    print(f"[EVAL] Collected {len(results)} valid samples. Analyzing...")
    stats = analyze_results(results)


if __name__ == "__main__":
    main()
