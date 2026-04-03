# Verification: Does V8.3 actually predict well at normal scale?
# ==============================================================
# Tests RAW predictions (no filter) against ground truth on a 
# diverse sample of small/medium benchmarks.

import torch
import numpy as np
import sys
import os
import random
import time
import json
from pathlib import Path

sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.meta_calibrator import MetaCalibrator
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES


def _extract_scale_context(graph_data, device):
    visible_nodes = int(graph_data.x.size(0))
    local_nodes = max(visible_nodes - 1, 1)
    total_raw = getattr(graph_data, "total_nodes", None)

    if isinstance(total_raw, torch.Tensor):
        if total_raw.numel() > 0:
            total_nodes = float(total_raw.detach().view(-1)[0].item())
        else:
            total_nodes = float(local_nodes)
    elif total_raw is None:
        total_nodes = float(local_nodes)
    else:
        total_nodes = float(total_raw)

    total_nodes = max(total_nodes, 1.0)
    total_nodes_tensor = torch.tensor([[total_nodes]], dtype=torch.float32, device=device)
    return visible_nodes, total_nodes, total_nodes_tensor


def _resolve_action_plan():
    pass_specs = [
        ("function(loop-unroll)", "Unroll"),
        ("function(gvn)", "GVN"),
        ("function(sroa)", "SROA"),
        ("function(simplifycfg)", "Simplify"),
    ]
    plan = []
    for pass_name, display in pass_specs:
        if pass_name in LLVM_PASSES:
            plan.append((LLVM_PASSES.index(pass_name), display))
        else:
            print(f"[WARN] Pass not found in LLVM_PASSES, skipping: {pass_name}")
    if not plan:
        raise RuntimeError("No verification actions resolved from LLVM_PASSES.")
    return plan


def discover_normal_benchmarks(sample_per_tier=10, rng=None):
    """Sample benchmarks from every non-large-scale tier."""
    rng = rng or random.Random(42)
    benchmarks = []
    
    def sample_dir(directory, tier, exts=('.c', '.cpp'), n=sample_per_tier):
        p = Path(directory)
        if not p.exists(): return
        files = []
        for ext in exts:
            files.extend(sorted(p.glob(f"*{ext}")))
        if len(files) > n:
            files = rng.sample(files, n)
        for f in files:
            benchmarks.append((f, tier))
    
    # Small scale
    sample_dir("benchmarks/synthetic", "synthetic")
    sample_dir("benchmarks/linear-algebra", "linalg", n=5)
    
    # Medium scale (diverse structures)
    sample_dir("benchmarks/stencils", "stencil", n=8)
    sample_dir("benchmarks/diverse_synthetic/control_flow", "ds_control_flow")
    sample_dir("benchmarks/diverse_synthetic/recursive", "ds_recursive")
    sample_dir("benchmarks/diverse_synthetic/pointer_chase", "ds_pointer_chase")
    sample_dir("benchmarks/diverse_synthetic/dense_linalg", "ds_dense_linalg")
    sample_dir("benchmarks/diverse_synthetic/struct_heavy", "ds_struct_heavy")
    sample_dir("benchmarks/diverse_synthetic/multi_func", "ds_multi_func")
    
    # Medium-large scale (real code)
    sample_dir("benchmarks/large_scale/anghaben", "anghaben")
    sample_dir("benchmarks/large_scale/anghaben_wrapped", "anghaben_wrapped")
    
    # Adversarial
    sample_dir("benchmarks/adversarial", "adversarial", n=4)
    
    return benchmarks


def _resolve_meta_threshold(meta_calibrator_path, override=None, fallback=0.4):
    if override is not None:
        return float(override)
    sidecar = os.path.splitext(meta_calibrator_path)[0] + ".meta.json"
    if not os.path.exists(sidecar):
        return float(fallback)
    try:
        with open(sidecar, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        return float(metadata.get("inference_threshold", fallback))
    except Exception as exc:
        print(f"[WARN] Failed to parse threshold sidecar {sidecar}: {exc}")
        return float(fallback)


def verify_normal_scale(checkpoint_path, meta_calibrator_path=None, meta_threshold=None):
    device = torch.device("cpu")
    print(f"[Normal-Scale Verify] Loading V8 Checkpoint: {checkpoint_path}")
    
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    base_model.load_state_dict(state_dict)
    base_model.eval()

    meta_net = None
    applied_threshold = None
    if meta_calibrator_path:
        print(f"[Normal-Scale Verify] Loading Meta-Calibrator: {meta_calibrator_path}")
        meta_net = MetaCalibrator(pred_dim=6, action_dim=NUM_ACTIONS, hidden_dim=64).to(device)
        meta_net.load_state_dict(torch.load(meta_calibrator_path, map_location=device))
        meta_net.eval()
        applied_threshold = _resolve_meta_threshold(meta_calibrator_path, override=meta_threshold)
        print(f"[Normal-Scale Verify] Meta threshold: {applied_threshold:.3f}")
    
    rng = random.Random(42)
    benchmarks = discover_normal_benchmarks(sample_per_tier=10, rng=rng)
    action_plan = _resolve_action_plan()
    
    print(f"[Normal-Scale Verify] Testing {len(benchmarks)} benchmarks × {len(action_plan)} actions\n")
    
    results = []
    errors_by_scale = {}  # {scale_bucket: [abs_errors]}
    
    print(f"{'Benchmark':<30} | {'Tier':<18} | {'Nodes':<8} | {'Act':<8} | {'RawPred':<9} | {'Actual':<9} | {'AbsErr'}")
    print("-" * 110)
    
    for bench_path, tier in benchmarks:
        try:
            env = CompilerOptEnv([bench_path], reward_mode=RewardMode.HACKABLE)
        except Exception as e:
            print(f"[WARN] Failed to initialize env for {bench_path}: {e}")
            continue
        
        for action_id, action_name in action_plan:
            try:
                obs, _ = env.reset(seed=42)
                graph_data = env.get_observation_graph()
                if graph_data is None:
                    print(f"[WARN] No graph data for {bench_path}")
                    continue
                graph_data = graph_data.to(device)
                visible_nodes, total_nodes, total_nodes_tensor = _extract_scale_context(graph_data, device)
                
                with torch.no_grad():
                    action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                    action_onehot[0, action_id] = 1.0
                    _, raw_metrics = base_model(None, action_onehot, graph_data=graph_data, total_nodes=total_nodes_tensor)

                    if meta_net is not None:
                        raw_metrics = meta_net(raw_metrics, action_onehot, total_nodes_tensor, threshold=applied_threshold)

                    raw_pred = raw_metrics[0, 0].item()
                
                _, _, _, _, info = env.step(action_id)
                i_before = info.get('instructions_before', 1)
                i_after = info.get('instructions_after', 1)
                actual_pct = (i_after - i_before) / max(i_before, 1) * 100.0
                
                abs_err = abs(actual_pct - raw_pred)
                
                # Bucket by scale
                if total_nodes == 0:
                    bucket = f"~{visible_nodes} (vis)"
                    scale_key = visible_nodes
                else:
                    bucket = str(int(total_nodes))
                    scale_key = int(total_nodes)
                
                if scale_key not in errors_by_scale:
                    errors_by_scale[scale_key] = []
                errors_by_scale[scale_key].append(abs_err)
                
                results.append({
                    'benchmark': bench_path.name,
                    'tier': tier,
                    'total_nodes': int(total_nodes),
                    'action': action_name,
                    'raw_pred': raw_pred,
                    'actual': actual_pct,
                    'abs_err': abs_err,
                })
                
                print(f"{bench_path.name:<30} | {tier:<18} | {int(total_nodes):<8} | {action_name:<8} | {raw_pred:>8.2f}% | {actual_pct:>8.2f}% | {abs_err:>6.2f}%")
            except Exception as e:
                print(f"[WARN] Failed case {bench_path.name} action={action_name}: {e}")
                continue
    
    # Summary Statistics
    if results:
        all_errors = [r['abs_err'] for r in results]
        print(f"\n{'='*80}")
        print(f"SUMMARY: {len(results)} data points collected")
        print(f"{'='*80}")
        print(f"  Mean Absolute Error:   {np.mean(all_errors):.2f}%")
        print(f"  Median Absolute Error: {np.median(all_errors):.2f}%")
        print(f"  Std Absolute Error:    {np.std(all_errors):.2f}%")
        print(f"  Max Absolute Error:    {np.max(all_errors):.2f}%")
        print(f"  90th Percentile:       {np.percentile(all_errors, 90):.2f}%")
        
        # Error by action
        print(f"\nError by Action:")
        for _, name in action_plan:
            action_errors = [r['abs_err'] for r in results if r['action'] == name]
            if action_errors:
                print(f"  {name:<10}: Mean={np.mean(action_errors):.2f}%, Median={np.median(action_errors):.2f}%, N={len(action_errors)}")
        
        # Error by tier
        print(f"\nError by Tier:")
        tiers = sorted(set(r['tier'] for r in results))
        for t in tiers:
            tier_errors = [r['abs_err'] for r in results if r['tier'] == t]
            tier_nodes = [r['total_nodes'] for r in results if r['tier'] == t]
            if tier_errors:
                print(f"  {t:<20}: Mean={np.mean(tier_errors):.2f}%, Median={np.median(tier_errors):.2f}%, "
                      f"AvgNodes={np.mean(tier_nodes):.0f}, N={len(tier_errors)}")
        
        # Error by scale bucket
        print(f"\nError by Scale (node count ranges):")
        all_nodes = sorted(set(r['total_nodes'] for r in results))
        buckets = [(0, 100), (100, 500), (500, 2000), (2000, 10000), (10000, 100000)]
        for lo, hi in buckets:
            bucket_errors = [r['abs_err'] for r in results if lo <= r['total_nodes'] < hi]
            if bucket_errors:
                print(f"  [{lo:>6} - {hi:>6}): Mean={np.mean(bucket_errors):.2f}%, "
                      f"Median={np.median(bucket_errors):.2f}%, N={len(bucket_errors)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--meta_calibrator", type=str, default=None, help="Path to meta calibrator model")
    parser.add_argument("--meta_threshold", type=float, default=None, help="Optional override for calibrator gate threshold")
    args = parser.parse_args()
    verify_normal_scale(args.checkpoint, args.meta_calibrator, args.meta_threshold)
