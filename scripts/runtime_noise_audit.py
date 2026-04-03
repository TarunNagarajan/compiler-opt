import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.passes.metrics import MetricsCollector


def _aggregate(values, mode: str) -> float:
    m = str(mode).strip().lower()
    if not values:
        return 0.0
    if m == "median":
        return float(statistics.median(values))
    if m == "mean":
        return float(statistics.fmean(values))
    if m == "min":
        return float(min(values))
    raise ValueError(f"Unsupported aggregation mode: {mode}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit runtime measurement noise for a single benchmark")
    parser.add_argument("--file", required=True, help="Path to runnable IR file")
    parser.add_argument("--samples", type=int, default=7, help="Number of repeated runtime measurements")
    parser.add_argument("--runs-per-sample", type=int, default=2, help="Harness runs within each measurement sample")
    parser.add_argument("--loop-count", type=int, default=100, help="Harness loop count per run")
    parser.add_argument("--timeout-seconds", type=float, default=20.0, help="Timeout per harness run")
    parser.add_argument("--aggregation", choices=["median", "mean", "min"], default="median", help="Aggregation inside each measurement sample")
    parser.add_argument("--cv-threshold", type=float, default=2.0, help="Coefficient-of-variation threshold for declaring low noise")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = MetricsCollector()
    samples = max(1, int(args.samples))
    runs_per_sample = max(1, int(args.runs_per_sample))
    total_runs = samples * runs_per_sample

    # Single compile + many harness runs (much faster than compile-per-sample).
    _ = metrics.measure_runtime(
        args.file,
        iterations=total_runs,
        max_iterations=total_runs,
        target_rel_ci95_pct=None,
        loop_count=int(args.loop_count),
        timeout_seconds=float(args.timeout_seconds),
        aggregation=args.aggregation,
    )
    runtime_stats = metrics.get_last_runtime_stats()
    raw_values = [float(x) for x in runtime_stats.get("all_per_iter_samples", []) if float(x) > 0.0]

    values = []
    for i in range(0, len(raw_values), runs_per_sample):
        chunk = raw_values[i:i + runs_per_sample]
        if len(chunk) == runs_per_sample:
            values.append(_aggregate(chunk, args.aggregation))

    if not values:
        print(
            json.dumps(
                {
                    "file": args.file,
                    "status": "unmeasurable",
                    "message": "No valid runtime samples were collected. The benchmark may be non-runnable, timing out, or failing to compile in the harness.",
                    "attempted_total_runs": total_runs,
                    "timed_out_runs": int(runtime_stats.get("timed_out_runs", 0)),
                    "failed_runs": int(runtime_stats.get("failed_runs", 0)),
                },
                indent=2,
            )
        )
        return

    mean_v = float(statistics.fmean(values))
    std_v = float(statistics.pstdev(values)) if len(values) > 1 else 0.0
    median_v = float(statistics.median(values))
    min_v = float(min(values))
    max_v = float(max(values))
    cv_v = float(abs(std_v / mean_v) * 100.0) if abs(mean_v) > 1e-12 else float("inf")

    print(
        json.dumps(
            {
                "file": args.file,
                "samples_requested": int(args.samples),
                "samples_collected": len(values),
                "runs_per_sample": int(args.runs_per_sample),
                "total_runs_requested": total_runs,
                "total_runs_collected": len(raw_values),
                "timed_out_runs": int(runtime_stats.get("timed_out_runs", 0)),
                "failed_runs": int(runtime_stats.get("failed_runs", 0)),
                "loop_count": int(args.loop_count),
                "timeout_seconds": float(args.timeout_seconds),
                "aggregation": args.aggregation,
                "raw_cycles_per_iter": values,
                "summary": {
                    "mean": mean_v,
                    "median": median_v,
                    "std": std_v,
                    "min": min_v,
                    "max": max_v,
                    "cv_pct": cv_v,
                },
                "zero_noise_proven": std_v == 0.0,
                "low_noise": cv_v <= float(args.cv_threshold),
                "interpretation": (
                    "Zero noise was not proven; use the observed variance as the measurement noise floor."
                    if std_v > 0.0
                    else "All collected samples were identical, but that still does not prove universal zero noise outside this audit run."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
