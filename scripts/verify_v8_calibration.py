"""
V8.4 Verification Script: Tests RAW model predictions on both  
normal-scale and industrial-scale benchmarks to verify retraining quality.
No post-hoc filter applied - the model must be accurate on its own.
"""
import torch
import numpy as np
import sys
import os
import random
import json
from pathlib import Path

sys.path.append(os.getcwd())

from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.meta_calibrator import MetaCalibrator
from src.config import NUM_ACTIONS, FEATURE_DIM, LLVM_PASSES


def _extract_scale_context(graph_data, device):
    local_nodes = max(int(graph_data.x.size(0)) - 1, 1)
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
    return local_nodes, total_nodes, total_nodes_tensor


def _resolve_action_plan():
    pass_specs = [
        ("function(loop-unroll)", "Unroll"),
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


def verify(checkpoint_path, meta_calibrator_path=None, meta_threshold=None):
    device = torch.device("cpu")
    print(f"[V8.4 Verify] Loading checkpoint: {checkpoint_path}")
    
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    state_dict = ckpt.get('model_state_dict', ckpt)
    model.load_state_dict(state_dict)
    model.eval()

    meta_net = None
    applied_threshold = None
    if meta_calibrator_path:
        print(f"[V8.4 Verify] Loading Meta-Calibrator: {meta_calibrator_path}")
        meta_net = MetaCalibrator(pred_dim=6, action_dim=NUM_ACTIONS, hidden_dim=64).to(device)
        meta_net.load_state_dict(torch.load(meta_calibrator_path, map_location=device))
        meta_net.eval()
        applied_threshold = _resolve_meta_threshold(meta_calibrator_path, override=meta_threshold)
        print(f"[V8.4 Verify] Meta threshold: {applied_threshold:.3f}")
    
    # Comprehensive test set spanning all scales and code patterns
    rng = random.Random(42)
    test_cases = []
    
    # Small: Sample 5 synthetic
    syn_dir = Path("benchmarks/synthetic")
    if syn_dir.exists():
        syns = sorted(syn_dir.glob("*.c"))
        for f in rng.sample(syns, min(5, len(syns))):
            test_cases.append((f, "synthetic"))
    
    # Medium: Key diverse categories
    for cat in ["control_flow", "recursive", "pointer_chase", "struct_heavy", "dense_linalg"]:
        d = Path(f"benchmarks/diverse_synthetic/{cat}")
        if d.exists():
            files = sorted(d.glob("*.c"))
            if files:
                test_cases.append((rng.choice(files), f"ds_{cat}"))
    
    # Stencil
    d = Path("benchmarks/stencils")
    if d.exists():
        files = sorted(d.glob("*.c"))
        if files:
            test_cases.append((rng.choice(files), "stencil"))
    
    # Anghaben
    d = Path("benchmarks/large_scale/anghaben_wrapped")
    if d.exists():
        files = sorted(d.glob("*.c"))
        for f in rng.sample(files, min(3, len(files))):
            test_cases.append((f, "anghaben"))
    
    # Industrial (always include all)
    industrial = [
        ("benchmarks/large_scale/lz4/lz4.c", "industrial"),
        ("benchmarks/large_scale/yyjson.c", "industrial"),
        ("benchmarks/large_scale/sqlite/sqlite3.c", "industrial"),
        ("benchmarks/large_scale/cjson/cjson.c", "industrial"),
        ("benchmarks/large_scale/tinyxml2/tinyxml2.cpp", "industrial"),
    ]
    for p, t in industrial:
        if Path(p).exists():
            test_cases.append((Path(p), t))
    
    test_actions = _resolve_action_plan()
    
    print(f"\n{'='*100}")
    print(f"{'Benchmark':<28} | {'Tier':<15} | {'Nodes':<8} | {'Act':<8} | {'Predicted':<10} | {'Actual':<10} | {'Error'}")
    print(f"{'-'*100}")
    
    results = []
    for bench_path, tier in test_cases:
        try:
            env = CompilerOptEnv([bench_path], reward_mode=RewardMode.HACKABLE)
        except Exception as e:
            print(f"[WARN] Failed to initialize env for {bench_path}: {e}")
            continue
        
        for action_id, action_name in test_actions:
            try:
                obs, _ = env.reset(seed=42)
                graph_data = env.get_observation_graph()
                if graph_data is None:
                    print(f"[WARN] No graph data for {bench_path}")
                    continue
                graph_data = graph_data.to(device)
                _, total_nodes, total_nodes_tensor = _extract_scale_context(graph_data, device)
                
                with torch.no_grad():
                    action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                    action_onehot[0, action_id] = 1.0
                    _, raw_metrics = model(None, action_onehot, graph_data=graph_data, total_nodes=total_nodes_tensor)
                    
                    if meta_net is not None:
                        raw_metrics = meta_net(raw_metrics, action_onehot, total_nodes_tensor, threshold=applied_threshold)
                        
                    pred = raw_metrics[0, 0].item()
                
                _, _, _, _, info = env.step(action_id)
                i_before = info.get('instructions_before', 1)
                i_after = info.get('instructions_after', 1)
                actual = (i_after - i_before) / max(i_before, 1) * 100.0
                
                err = actual - pred
                results.append({'tier': tier, 'nodes': int(total_nodes), 'action': action_name,
                               'pred': pred, 'actual': actual, 'abs_err': abs(err)})
                
                print(f"{bench_path.name:<28} | {tier:<15} | {int(total_nodes):<8} | "
                      f"{action_name:<8} | {pred:>9.2f}% | {actual:>9.2f}% | {err:>+7.2f}%")
            except Exception as e:
                print(f"[WARN] Failed case {bench_path.name} action={action_name}: {e}")
                continue
    
    # Summary
    if results:
        all_err = [r['abs_err'] for r in results]
        print(f"\n{'='*60}")
        print(f"OVERALL: Mean={np.mean(all_err):.2f}%, Median={np.median(all_err):.2f}%, "
              f"90th={np.percentile(all_err, 90):.2f}%, N={len(results)}")
        
        for tier in sorted(set(r['tier'] for r in results)):
            te = [r['abs_err'] for r in results if r['tier'] == tier]
            print(f"  {tier:<15}: Mean={np.mean(te):.2f}%, N={len(te)}")
        
        for act in sorted(set(r['action'] for r in results)):
            ae = [r['abs_err'] for r in results if r['action'] == act]
            print(f"  {act:<15}: Mean={np.mean(ae):.2f}%, N={len(ae)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--meta_calibrator", type=str, default=None, help="Path to meta calibrator model")
    parser.add_argument("--meta_threshold", type=float, default=None, help="Optional override for calibrator gate threshold")
    args = parser.parse_args()
    verify(args.checkpoint, args.meta_calibrator, args.meta_threshold)
