# Phase 5.0: Comprehensive Calibration Data Collection
# =====================================================
# 
# APPROACH: The model predicts well at normal scale. The error is a function
# of node count. We need to empirically learn f(scale) such that:
#
#   corrected = raw_pred × f(total_nodes, action)
#
# With 6000+ benchmarks spanning many orders of magnitude, we can fit
# this function robustly and it will generalize to unseen programs
# because the correction depends on SCALE, not on program identity.
#
# DATA SOURCES:
#   - benchmarks/synthetic/ (~1000 files, small scale)
#   - benchmarks/stencils/ (~50 files, medium scale)
#   - benchmarks/diverse_synthetic/*/ (16 categories × 200 = ~3200, varied scale)
#   - benchmarks/large_scale/anghaben/ (~200 files, medium scale)
#   - benchmarks/large_scale/anghaben_wrapped/ (~285 files, medium scale)
#   - benchmarks/cpp/generated/ (~500 files, medium scale)
#   - benchmarks/mibench/ (~900 files, medium-large scale)
#   - benchmarks/linear-algebra/ (~19 files, small scale)
#   - benchmarks/adversarial/ (4 files, varied)
#   - benchmarks/large_scale/ industrial modules (6 files, large scale)

import torch
import numpy as np
import sys
import os
import csv
import time
import random
from pathlib import Path

sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM


def discover_benchmarks(sample_per_category=None):
    """Discover ALL available benchmark files across the entire project."""
    benchmarks = []
    
    def add_dir(directory, tier, extensions=('.c', '.cpp'), max_files=None):
        p = Path(directory)
        if not p.exists():
            return
        files = []
        for ext in extensions:
            files.extend(sorted(p.glob(f"*{ext}")))
        if max_files and len(files) > max_files:
            random.seed(42)  # Reproducible sampling
            files = random.sample(files, max_files)
        for f in files:
            benchmarks.append((f, tier))
    
    # Tier 1: Synthetic (small scale, baseline calibration)
    add_dir("benchmarks/synthetic", "synthetic", max_files=sample_per_category)
    
    # Tier 2: Stencils (structured loops, medium scale)
    add_dir("benchmarks/stencils", "stencil")
    
    # Tier 3: Diverse Synthetic (16 categories, varied control flow)
    ds_root = Path("benchmarks/diverse_synthetic")
    if ds_root.exists():
        for category_dir in sorted(ds_root.iterdir()):
            if category_dir.is_dir():
                add_dir(str(category_dir), f"ds_{category_dir.name}", max_files=sample_per_category)
    
    # Tier 4: Real-world code (anghaben)
    add_dir("benchmarks/large_scale/anghaben", "anghaben", max_files=sample_per_category)
    add_dir("benchmarks/large_scale/anghaben_wrapped", "anghaben_wrapped", max_files=sample_per_category)
    
    # Tier 5: Generated C++ (varied structures)
    add_dir("benchmarks/cpp/generated", "cpp_generated", max_files=sample_per_category)
    
    # Tier 6: MiBench (real embedded systems benchmarks)
    mibench_root = Path("benchmarks/mibench")
    if mibench_root.exists():
        # Search recursively for C files in mibench
        c_files = sorted(mibench_root.rglob("*.c"))
        if sample_per_category and len(c_files) > sample_per_category:
            random.seed(42)
            c_files = random.sample(c_files, sample_per_category)
        for f in c_files:
            benchmarks.append((f, "mibench"))
    
    # Tier 7: Linear Algebra (Polybench kernels)
    add_dir("benchmarks/linear-algebra", "linalg")
    
    # Tier 8: Adversarial
    add_dir("benchmarks/adversarial", "adversarial")
    
    # Tier 9: Industrial (the hard cases - always include ALL of these)
    industrial_files = [
        ("benchmarks/large_scale/lz4/lz4.c", "industrial"),
        ("benchmarks/large_scale/yyjson.c", "industrial"),
        ("benchmarks/large_scale/sqlite/sqlite3.c", "industrial"),
        ("benchmarks/large_scale/cjson/cjson.c", "industrial"),
        ("benchmarks/large_scale/tinyxml2/tinyxml2.cpp", "industrial"),
        ("benchmarks/large_scale/miniz.h", "industrial"),
        ("benchmarks/large_scale/stb_image.h", "industrial"),
    ]
    for path, tier in industrial_files:
        p = Path(path)
        if p.exists():
            benchmarks.append((p, tier))
    
    return benchmarks


def collect_calibration_data(checkpoint_path, output_path, sample_per_category=None):
    device = torch.device("cpu")
    print(f"[Data Collection] Loading V8 Checkpoint: {checkpoint_path}")
    
    # Initialize Base Model (NO wrapper - raw predictions only)
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    base_model.load_state_dict(state_dict)
    base_model.eval()
    
    # Discover ALL benchmarks
    benchmarks = discover_benchmarks(sample_per_category=sample_per_category)
    
    # Actions to test
    test_actions = [63, 12, 57, 45]  # Unroll, GVN, SROA, Simplifier
    
    total_expected = len(benchmarks) * len(test_actions)
    print(f"[Data Collection] Found {len(benchmarks)} benchmarks × {len(test_actions)} actions = {total_expected} potential data points")
    print(f"[Data Collection] Output: {output_path}")
    
    # Write header
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'benchmark', 'tier', 'action_id',
            'total_nodes', 'visible_nodes', 'num_edges',
            'foveation_ratio',
            'edge_density',
            'raw_pred_pct',
            'actual_pct',
            'error_pct',
            'error_ratio',
        ])
    
    collected = 0
    skipped = 0
    start_time = time.time()
    
    for bench_idx, (bench_path, tier) in enumerate(benchmarks):
        try:
            env = CompilerOptEnv([bench_path], reward_mode=RewardMode.HACKABLE)
        except Exception as e:
            skipped += len(test_actions)
            continue
        
        for action_id in test_actions:
            try:
                obs, _ = env.reset()
                graph_data = env.get_observation_graph()
                
                total_nodes_val = getattr(graph_data, 'total_nodes', torch.tensor([0])).item()
                visible_nodes = graph_data.x.size(0)
                num_edges = graph_data.edge_index.size(1)
                
                foveation_ratio = visible_nodes / max(total_nodes_val, 1) if total_nodes_val > 0 else 1.0
                edge_density = num_edges / max(visible_nodes, 1)
                
                # Raw prediction
                with torch.no_grad():
                    action_onehot = torch.zeros(1, NUM_ACTIONS)
                    action_onehot[0, action_id] = 1.0
                    tn = torch.tensor([total_nodes_val]) if total_nodes_val > 0 else None
                    _, raw_metrics = base_model(None, action_onehot, graph_data=graph_data, total_nodes=tn)
                    raw_pred = raw_metrics[0, 0].item()
                
                # Ground truth
                _, _, _, _, info = env.step(action_id)
                i_before = info.get('instructions_before', 1)
                i_after = info.get('instructions_after', 1)
                actual_pct = (i_after - i_before) / max(i_before, 1) * 100.0
                
                error_pct = actual_pct - raw_pred
                error_ratio = actual_pct / raw_pred if abs(raw_pred) > 0.01 else 0.0
                
                with open(output_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        bench_path.name, tier, action_id,
                        int(total_nodes_val), visible_nodes, num_edges,
                        f"{foveation_ratio:.6f}",
                        f"{edge_density:.4f}",
                        f"{raw_pred:.6f}",
                        f"{actual_pct:.6f}",
                        f"{error_pct:.6f}",
                        f"{error_ratio:.6f}",
                    ])
                collected += 1
                
            except Exception:
                skipped += 1
                continue
        
        # Progress every 20 benchmarks
        if (bench_idx + 1) % 20 == 0:
            elapsed = time.time() - start_time
            rate = collected / max(elapsed, 1)
            eta = (total_expected - collected) / max(rate, 0.01)
            print(f"  [{bench_idx+1}/{len(benchmarks)}] Collected: {collected}/{total_expected} | "
                  f"Rate: {rate:.1f}/s | ETA: {eta:.0f}s | Skipped: {skipped}")
    
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"[COMPLETE] {collected} data points collected, {skipped} skipped")
    print(f"[COMPLETE] Time: {elapsed:.1f}s")
    print(f"[COMPLETE] Output: {output_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect calibration dataset for V8 World Model")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--output", type=str, default="calibration_dataset.csv")
    parser.add_argument("--sample", type=int, default=None,
                        help="Max files to sample per category (None = use all)")
    args = parser.parse_args()
    collect_calibration_data(args.checkpoint, args.output, sample_per_category=args.sample)
