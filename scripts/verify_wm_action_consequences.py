#!/usr/bin/env python3
"""
Action-level world-model audit for V8/V8.5 (+optional calibrator).

This script verifies whether predicted action consequences match measured
compiler outcomes across all 6 world-model metrics:
  [instruction %, size %, complexity, loops, calls, blocks]
"""

import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.append(os.getcwd())

from src.config import (
    FEATURE_DIM,
    LLVM_PASSES,
    NUM_ACTIONS,
    NUM_ATOMIC_ACTIONS,
    get_benchmark_paths,
)
from src.actions.macro_actions import MACRO_ACTIONS
from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.models.world_model import WorldModel


METRIC_NAMES = [
    "instr_pct",
    "size_pct",
    "complexity_delta",
    "loops_delta",
    "calls_delta",
    "blocks_delta",
]


def _resolve_action_name(action_id: int) -> str:
    if action_id < len(LLVM_PASSES):
        return LLVM_PASSES[action_id]
    macro_idx = action_id - NUM_ATOMIC_ACTIONS
    if 0 <= macro_idx < len(MACRO_ACTIONS):
        seq = MACRO_ACTIONS[macro_idx]
        if seq == ["TERMINATE"]:
            return "TERMINATE"
        return "macro(" + ";".join(seq) + ")"
    return f"action_{action_id}"


def _sample_benchmarks(seed: int, small_n: int, large_n: int):
    rng = random.Random(seed)
    all_paths = [Path(p) for p in get_benchmark_paths()]
    all_paths = [p for p in all_paths if p.exists()]
    if not all_paths:
        return []

    sized = sorted([(p, p.stat().st_size) for p in all_paths], key=lambda x: x[1])
    split = max(1, len(sized) // 3)
    small_pool = [p for p, _ in sized[:split]]
    large_pool = [p for p, _ in sized[-split:]]

    small_pick = rng.sample(small_pool, min(small_n, len(small_pool)))
    large_pick = rng.sample(large_pool, min(large_n, len(large_pool)))

    seen = set()
    selected = []
    for p in small_pick + large_pick:
        if p not in seen:
            selected.append(p)
            seen.add(p)
    return selected


def _to_total_nodes_tensor(graph_data, device, local_nodes: int):
    total_raw = getattr(graph_data, "total_nodes", None)
    if isinstance(total_raw, torch.Tensor) and total_raw.numel() > 0:
        total_nodes = float(total_raw.detach().view(-1)[0].item())
    elif total_raw is None:
        total_nodes = float(local_nodes)
    else:
        total_nodes = float(total_raw)
    total_nodes = max(total_nodes, 1.0)
    return torch.tensor([total_nodes], dtype=torch.float32, device=device), total_nodes


def _actual_metrics_from_info(info):
    i_before = info.get("instructions_before", 1)
    i_after = info.get("instructions_after", 1)
    s_before = info.get("size_before", 1)
    s_after = info.get("size_after", 1)
    c_before = info.get("complexity_before", 1)
    c_after = info.get("complexity_after", 1)
    l_before = info.get("loops_before", 1)
    l_after = info.get("loops_after", 1)
    call_before = info.get("calls_before", 1)
    call_after = info.get("calls_after", 1)
    b_before = info.get("blocks_before", 1)
    b_after = info.get("blocks_after", 1)

    return np.array(
        [
            (i_after - i_before) / max(i_before, 1) * 100.0,
            (s_after - s_before) / max(s_before, 1) * 100.0,
            (c_after - c_before) / max(c_before, 1),
            (l_after - l_before) / max(l_before, 1),
            (call_after - call_before) / max(call_before, 1),
            (b_after - b_before) / max(b_before, 1),
        ],
        dtype=np.float32,
    )


def _summarize(records):
    pred = np.stack([r["pred"] for r in records], axis=0)
    actual = np.stack([r["actual"] for r in records], axis=0)
    abs_err = np.abs(actual - pred)

    mae = abs_err.mean(axis=0).tolist()
    p90 = np.percentile(abs_err, 90, axis=0).tolist()

    sign_acc = []
    for i in range(actual.shape[1]):
        mask = np.abs(actual[:, i]) > 1e-6
        if mask.any():
            same = np.sign(actual[mask, i]) == np.sign(pred[mask, i])
            sign_acc.append(float(np.mean(same)))
        else:
            sign_acc.append(float("nan"))

    return {
        "mae_by_metric": {k: float(v) for k, v in zip(METRIC_NAMES, mae)},
        "p90_abs_err_by_metric": {k: float(v) for k, v in zip(METRIC_NAMES, p90)},
        "sign_accuracy_by_metric": {k: float(v) for k, v in zip(METRIC_NAMES, sign_acc)},
        "overall_mae": float(np.mean(abs_err)),
        "num_records": int(len(records)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--meta_calibrator", type=str, default=None)
    parser.add_argument("--meta_threshold", type=float, default=None)
    parser.add_argument("--benchmark_paths", nargs="*", default=None, help="Optional explicit benchmark source paths")
    parser.add_argument("--small_benchmarks", type=int, default=3)
    parser.add_argument("--large_benchmarks", type=int, default=3)
    parser.add_argument("--actions_per_benchmark", type=int, default=0, help="0 = all non-terminate actions")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--output", type=str, default="results/wm_action_consequence_report.json")
    parser.add_argument("--max_mae_instr", type=float, default=None)
    parser.add_argument("--max_mae_size", type=float, default=None)
    parser.add_argument("--max_mae_struct", type=float, default=None, help="Threshold for mean MAE over complexity/loops/calls/blocks")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = torch.device("cpu")
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS).to(device)
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    state_dict = ckpt.get("model_state_dict", ckpt)
    base_model.load_state_dict(state_dict)
    model = CalibratedWorldModel(
        base_model,
        meta_calibrator_path=args.meta_calibrator,
        meta_threshold=args.meta_threshold,
    ).to(device)
    model.eval()

    if args.benchmark_paths:
        benches = [Path(p) for p in args.benchmark_paths if Path(p).exists()]
    else:
        benches = _sample_benchmarks(args.seed, args.small_benchmarks, args.large_benchmarks)
    if not benches:
        raise RuntimeError("No benchmarks discovered for audit.")

    action_ids = list(range(NUM_ACTIONS))
    terminate_action = None
    if MACRO_ACTIONS and MACRO_ACTIONS[-1] == ["TERMINATE"]:
        terminate_action = NUM_ATOMIC_ACTIONS + len(MACRO_ACTIONS) - 1
        action_ids = [a for a in action_ids if a != terminate_action]

    records = []
    skipped_compile_error = 0
    skipped_no_graph = 0

    for b_idx, bench in enumerate(benches):
        env = CompilerOptEnv([bench], max_steps=1, reward_mode=RewardMode.HACKABLE)
        per_bench_actions = action_ids
        if args.actions_per_benchmark and args.actions_per_benchmark > 0:
            rng = random.Random(args.seed + b_idx)
            per_bench_actions = rng.sample(action_ids, min(args.actions_per_benchmark, len(action_ids)))

        for action_id in per_bench_actions:
            _, _ = env.reset(seed=args.seed + b_idx, options={"ir_path": str(bench)})
            graph_data = env.get_observation_graph()
            if graph_data is None:
                skipped_no_graph += 1
                continue

            graph_data = graph_data.to(device)
            local_nodes = max(int(graph_data.x.size(0)) - 1, 1)
            num_nodes = torch.tensor([float(local_nodes)], dtype=torch.float32, device=device)
            total_nodes_tensor, total_nodes_value = _to_total_nodes_tensor(graph_data, device, local_nodes)

            with torch.no_grad():
                state_emb = model.encode_graph(graph_data)
                action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                action_onehot[0, action_id] = 1.0
                _, pred_metrics = model.transition_step(
                    state_emb,
                    action_onehot,
                    num_nodes=num_nodes,
                    total_nodes=total_nodes_tensor,
                )
                pred_vec = pred_metrics.squeeze(0).detach().cpu().numpy().astype(np.float32)

            _, _, _, _, info = env.step(action_id)
            if info.get("error"):
                skipped_compile_error += 1
                continue

            actual_vec = _actual_metrics_from_info(info)
            records.append(
                {
                    "benchmark": bench.name,
                    "benchmark_path": str(bench),
                    "total_nodes": int(total_nodes_value),
                    "action_id": int(action_id),
                    "action_name": _resolve_action_name(action_id),
                    "pred": pred_vec.tolist(),
                    "actual": actual_vec.tolist(),
                }
            )

    if not records:
        raise RuntimeError("No valid action records collected (all runs skipped/failed).")

    summary = _summarize(records)
    summary["skipped_compile_error"] = int(skipped_compile_error)
    summary["skipped_no_graph"] = int(skipped_no_graph)
    summary["benchmarks_tested"] = [str(p) for p in benches]
    summary["actions_considered"] = int(len(action_ids))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"summary": summary, "records": records}
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("[WM-AUDIT] records:", summary["num_records"])
    print("[WM-AUDIT] overall MAE:", f"{summary['overall_mae']:.4f}")
    for name in METRIC_NAMES:
        print(f"  {name:<17} MAE={summary['mae_by_metric'][name]:.4f}  P90={summary['p90_abs_err_by_metric'][name]:.4f}")
    print(f"[WM-AUDIT] wrote: {out_path}")

    failures = []
    if args.max_mae_instr is not None and summary["mae_by_metric"]["instr_pct"] > args.max_mae_instr:
        failures.append(f"instr MAE {summary['mae_by_metric']['instr_pct']:.4f} > {args.max_mae_instr}")
    if args.max_mae_size is not None and summary["mae_by_metric"]["size_pct"] > args.max_mae_size:
        failures.append(f"size MAE {summary['mae_by_metric']['size_pct']:.4f} > {args.max_mae_size}")
    if args.max_mae_struct is not None:
        struct_vals = [
            summary["mae_by_metric"]["complexity_delta"],
            summary["mae_by_metric"]["loops_delta"],
            summary["mae_by_metric"]["calls_delta"],
            summary["mae_by_metric"]["blocks_delta"],
        ]
        struct_mean = float(np.mean(struct_vals))
        if struct_mean > args.max_mae_struct:
            failures.append(f"struct mean MAE {struct_mean:.4f} > 
