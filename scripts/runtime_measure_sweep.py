import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import LLVM_PASSES
from src.env import CompilerOptEnv, RewardMode


def pct_delta(before: float, after: float) -> float:
    b = float(before)
    a = float(after)
    if b <= 0.0:
        return 0.0
    return ((b - a) / b) * 100.0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Empirical runtime measurement sweep")
    p.add_argument("--file", required=True, help="Benchmark source or IR file")
    p.add_argument("--pass_name", default="function(simplifycfg)", help="LLVM pass name to test")
    p.add_argument("--runs", type=int, nargs="+", default=[1, 2, 3, 5], help="runtime_measure_runs values to sweep")
    p.add_argument("--trials", type=int, default=4, help="Trials per runs value")
    p.add_argument("--max_steps", type=int, default=1, help="Env max steps")
    p.add_argument("--reward_mode", default="size", help="Reward mode for env")
    p.add_argument("--std_threshold", type=float, default=0.5, help="Stability threshold on std dev")
    p.add_argument("--cv_threshold", type=float, default=20.0, help="Stability threshold on coefficient of variation")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    pass_to_idx = {p: i for i, p in enumerate(LLVM_PASSES)}
    action_idx = pass_to_idx.get(args.pass_name, 0)
    reward_mode = RewardMode[str(args.reward_mode).upper()]

    print(
        f"[sweep] file={args.file} pass={args.pass_name} action_idx={action_idx} "
        f"runs={list(args.runs)} trials={args.trials}",
        flush=True,
    )

    sweep = {}
    for runs in args.runs:
        print(f"[sweep] start runs={runs}", flush=True)
        env = CompilerOptEnv(
            [args.file],
            max_steps=args.max_steps,
            reward_mode=reward_mode,
            collect_speed_metrics=True,
            runtime_measure_runs=int(runs),
        )
        values = []
        for t in range(int(args.trials)):
            print(f"[sweep] runs={runs} trial={t+1}/{int(args.trials)} reset", flush=True)
            env.reset()
            print(f"[sweep] runs={runs} trial={t+1}/{int(args.trials)} step", flush=True)
            _, _, _, _, info = env.step(action_idx)
            values.append(pct_delta(info.get("runtime_before", 0.0), info.get("runtime_after", 0.0)))

        mean_v = statistics.mean(values)
        std_v = statistics.pstdev(values) if len(values) > 1 else 0.0
        cv_v = abs(std_v / mean_v) * 100.0 if abs(mean_v) > 1e-9 else float("inf")
        sweep[int(runs)] = {
            "trials": len(values),
            "mean_runtime_gain_pct": mean_v,
            "std_runtime_gain_pct": std_v,
            "cv_pct": cv_v,
            "samples": values,
        }

    recommended = None
    for runs in args.runs:
        r = sweep[int(runs)]
        if r["std_runtime_gain_pct"] <= args.std_threshold and r["cv_pct"] <= args.cv_threshold:
            recommended = int(runs)
            break

    print(
        json.dumps(
            {
                "file": args.file,
                "pass_name": args.pass_name,
                "action_idx": action_idx,
                "reward_mode": args.reward_mode,
                "runs_tested": [int(x) for x in args.runs],
                "trials": int(args.trials),
                "stability_thresholds": {
                    "std_runtime_gain_pct": args.std_threshold,
                    "cv_pct": args.cv_threshold,
                },
                "results": sweep,
                "recommended_runtime_measure_runs": recommended if recommended is not None else f">={max(args.runs)}",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
