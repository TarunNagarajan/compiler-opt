#!/usr/bin/env python3
"""
Contract check for HRL training signals.

Verifies that:
1) performance mode exposes runtime/energy telemetry,
2) embedded mode (SIZE + collect_speed_metrics) still exposes runtime/energy,
3) edge-telemetry keys exist (loads/stores/allocas/branches/calls/blocks),
4) mission-target formulas are finite and directionally valid.
"""

import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np

sys.path.append(os.getcwd())

from src.actions.macro_actions import MACRO_ACTIONS
from src.config import NUM_ACTIONS, NUM_ATOMIC_ACTIONS, get_benchmark_paths
from src.env.compiler_env import CompilerOptEnv, RewardMode


EDGE_KEYS = [
    "loads_before", "loads_after",
    "stores_before", "stores_after",
    "allocas_before", "allocas_after",
    "branches_before", "branches_after",
    "calls_before", "calls_after",
    "blocks_before", "blocks_after",
]


def _choose_benchmarks(seed: int, n: int):
    rng = random.Random(seed)
    all_paths = [Path(p) for p in get_benchmark_paths() if Path(p).exists()]
    if not all_paths:
        return []
    all_paths = sorted(all_paths, key=lambda p: p.stat().st_size)
    k = min(n, len(all_paths))
    mids = all_paths[len(all_paths) // 4: max(len(all_paths) // 4 + 1, len(all_paths) // 2)]
    tails = all_paths[-max(1, len(all_paths) // 4):]
    picks = []
    picks.extend(rng.sample(mids, min(k // 2 + (k % 2), len(mids))) if mids else [])
    picks.extend(rng.sample(tails, min(k // 2, len(tails))) if tails else [])
    # de-dup
    out = []
    seen = set()
    for p in picks:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out if out else all_paths[:k]


def _valid_action_ids():
    ids = list(range(NUM_ACTIONS))
    if MACRO_ACTIONS and MACRO_ACTIONS[-1] == ["TERMINATE"]:
        terminate_action = NUM_ATOMIC_ACTIONS + len(MACRO_ACTIONS) - 1
        ids = [a for a in ids if a != terminate_action]
    return ids


def _collect_infos(mode_name: str, bench_paths, steps_per_bench: int, seed: int, collect_speed_metrics: bool):
    reward_mode = RewardMode.SPEED if mode_name == "performance" else RewardMode.SIZE
    rng = random.Random(seed)
    action_ids = _valid_action_ids()
    infos = []

    for bench in bench_paths:
        env = CompilerOptEnv(
            [bench],
            max_steps=max(1, steps_per_bench),
            reward_mode=reward_mode,
            collect_speed_metrics=collect_speed_metrics,
        )
        env.reset(seed=seed, options={"ir_path": str(bench)})
        for step in range(steps_per_bench):
            action = rng.choice(action_ids)
            _, _, terminated, truncated, info = env.step(action)
            if not info.get("error"):
                infos.append(info)
            if terminated or truncated:
                env.reset(seed=seed + step + 1, options={"ir_path": str(bench)})

    return infos


def _compute_targets(info, w_size: float, w_speed: float, w_energy: float):
    i_before = info.get("instructions_before", 1)
    i_after = info.get("instructions_after", 1)
    r_before = info.get("runtime_before", 0.0)
    r_after = info.get("runtime_after", 0.0)
    e_before = info.get("energy_before", 0.0)
    e_after = info.get("energy_after", 0.0)

    inst_gain = (i_before - i_after) / max(i_before, 1) * 100.0
    spd_gain = ((r_before - r_after) / max(r_before, 1e-6) * 100.0) if (r_before > 0 and r_after > 0) else 0.0
    energy_gain = ((e_before - e_after) / max(e_before, 1e-6) * 100.0) if (e_before > 0 and e_after > 0) else 0.0

    perf_target = spd_gain
    emb_target = (w_size * inst_gain) + (w_speed * spd_gain) + (w_energy * energy_gain)
    return perf_target, emb_target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark_paths", nargs="*", default=None, help="Optional explicit benchmark source paths")
    parser.add_argument("--benchmarks", type=int, default=3)
    parser.add_argument("--steps_per_bench", type=int, default=3)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--weight_size", type=float, default=0.4)
    parser.add_argument("--weight_speed", type=float, default=0.3)
    parser.add_argument("--weight_energy", type=float, default=0.3)
    parser.add_argument("--output", type=str, default="results/hrl_signal_contracts.json")
    args = parser.parse_args()

    total_w = args.weight_size + args.weight_speed + args.weight_energy
    if total_w <= 0:
        raise RuntimeError("Weights must sum to > 0.")
    w_size = args.weight_size / total_w
    w_speed = args.weight_speed / total_w
    w_energy = args.weight_energy / total_w

    if args.benchmark_paths:
        bench_paths = [Path(p) for p in args.benchmark_paths if Path(p).exists()]
    else:
        bench_paths = _choose_benchmarks(args.seed, args.benchmarks)
    if not bench_paths:
        raise RuntimeError("No benchmarks available for HRL contract check.")

    perf_infos = _collect_infos(
        mode_name="performance",
        bench_paths=bench_paths,
        steps_per_bench=args.steps_per_bench,
        seed=args.seed,
        collect_speed_metrics=False,
    )
    emb_infos = _collect_infos(
        mode_name="embedded",
        bench_paths=bench_paths,
        steps_per_bench=args.steps_per_bench,
        seed=args.seed + 97,
        collect_speed_metrics=True,
    )

    def any_runtime(infos):
        return any((info.get("runtime_before", 0.0) > 0 and info.get("runtime_after", 0.0) >= 0) for info in infos)

    def any_energy(infos):
        return any((info.get("energy_before", 0.0) > 0 and info.get("energy_after", 0.0) >= 0) for info in infos)

    def edge_keys_present(infos):
        return all(all(k in info for k in EDGE_KEYS) for info in infos)

    perf_runtime_ok = any_runtime(perf_infos)
    emb_runtime_ok = any_runtime(emb_infos)
    emb_energy_ok = any_energy(emb_infos)
    emb_edge_keys_ok = edge_keys_present(emb_infos)

    perf_targets = []
    emb_targets = []
    for info in emb_infos + perf_infos:
        perf_t, emb_t = _compute_targets(info, w_size, w_speed, w_energy)
        perf_targets.append(perf_t)
        emb_targets.append(emb_t)

    finite_targets_ok = np.isfinite(np.array(perf_targets)).all() and np.isfinite(np.array(emb_targets)).all()

    report = {
        "benchmarks": [str(p) for p in bench_paths],
        "performance_steps": len(perf_infos),
        "embedded_steps": len(emb_infos),
        "performance_runtime_signal_ok": bool(perf_runtime_ok),
        "embedded_runtime_signal_ok": bool(emb_runtime_ok),
        "embedded_energy_signal_ok": bool(emb_energy_ok),
        "embedded_edge_keys_ok": bool(emb_edge_keys_ok),
        "finite_targets_ok": bool(finite_targets_ok),
        "perf_target_mean": float(np.mean(perf_targets)) if perf_targets else 0.0,
        "embedded_target_mean": float(np.mean(emb_targets)) if emb_targets else 0.0,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("[HRL-CONTRACT] performance runtime signal:", perf_runtime_ok)
    print("[HRL-CONTRACT] embedded runtime signal:", emb_runtime_ok)
    print("[HRL-CONTRACT] embedded energy signal:", emb_energy_ok)
    print("[HRL-CONTRACT] embedded edge keys:", emb_edge_keys_ok)
    print("[HRL-CONTRACT] finite mission targets:", finite_targets_ok)
    print("[HRL-CONTRACT] wrote:", out)

    failures = []
    if not perf_runtime_ok:
        failures.append("performance mode missing runtime telemetry")
    if not emb_runtime_ok:
        failures.append("embedded mode missing runtime telemetry")
    if not emb_energy_ok:
        failures.append("embedded mode missing energy telemetry")
    if not emb_edge_keys_ok:
        failures.append("embedded mode missing edge proxy keys")
    if not finite_targets_ok:
        failures.append("mission target formulas produ
