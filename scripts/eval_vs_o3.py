"""
Comprehensive Evaluation: Agent vs O3 vs O2.

For each benchmark:
1. Compile at O0 (canonicalized) -> agent applies learned sequence
2. Compile at O2, O3 -> measure runtime baselines
3. Compare agent vs O3 vs O2 with high-precision runtime measurement
4. Optionally: llvm-mca diagnostic analysis

Reports:
- Per-benchmark: CPU cycles delta, CI95 intervals
- Summary: "Beat O3 on X/Y benchmarks by average Z%"
- Breakdown by benchmark category
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import CLANG, get_benchmark_paths
from src.passes import PassExecutor, MetricsCollector
from src.passes.mca_analyzer import MCAAnalyzer
import subprocess


def compile_at_level(source_path: Path, level: str, executor: PassExecutor) -> str:
    """Compile source at given optimization level, return IR path."""
    out_ir = executor.work_dir / f"{source_path.stem}_{level}.ll"
    cmd = [
        str(CLANG), f"-{level}", "-S", "-emit-llvm",
        "-Wno-everything", str(source_path), "-o", str(out_ir)
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        return ""
    return str(out_ir)


def evaluate_benchmark(
    source_path: Path,
    agent_passes: list,
    metrics: MetricsCollector,
    mca: MCAAnalyzer,
    runtime_iterations: int = 10,
    loop_count: int = 500,
) -> dict:
    """Evaluate a single benchmark: agent vs O2 vs O3."""
    executor = PassExecutor()
    result = {"benchmark": source_path.name, "category": _infer_category(source_path)}

    try:
        # Compile baselines
        o2_ir = compile_at_level(source_path, "O2", executor)
        o3_ir = compile_at_level(source_path, "O3", executor)

        if not o2_ir or not o3_ir:
            result["error"] = "Failed to compile baselines"
            return result

        # Agent: O0 + canonicalization + learned passes
        from src.passes.pass_executor import compile_to_ir
        agent_ir_path = executor.work_dir / f"{source_path.stem}_agent.ll"
        ok, agent_ir = compile_to_ir(str(source_path), output_path=str(agent_ir_path))
        if not ok:
            result["error"] = f"Failed to compile agent IR: {agent_ir}"
            return result

        # Apply canonicalization
        canon = ["module(function(sroa),function(mem2reg),function(simplifycfg),function(instcombine<no-verify-fixpoint>),function(tailcallelim))"]
        canon_result = executor.apply_passes(agent_ir, canon)
        if canon_result.success:
            agent_ir = canon_result.output_path

        # Apply agent's learned passes
        for pass_name in agent_passes:
            pass_result = executor.apply_passes(agent_ir, [pass_name])
            if pass_result.success:
                agent_ir = pass_result.output_path

        # Measure runtimes
        measure_kwargs = dict(
            iterations=runtime_iterations,
            loop_count=loop_count,
            timeout_seconds=30.0,
            aggregation="median",
            max_iterations=runtime_iterations * 2,
            target_rel_ci95_pct=1.5,
        )

        o2_runtime = metrics.measure_runtime(o2_ir, **measure_kwargs)
        o2_stats = metrics.get_last_runtime_stats()

        o3_runtime = metrics.measure_runtime(o3_ir, **measure_kwargs)
        o3_stats = metrics.get_last_runtime_stats()

        agent_runtime = metrics.measure_runtime(agent_ir, **measure_kwargs)
        agent_stats = metrics.get_last_runtime_stats()

        result.update({
            "o2_runtime": o2_runtime,
            "o2_ci95_pct": o2_stats.get("relative_ci95_pct", 100.0),
            "o3_runtime": o3_runtime,
            "o3_ci95_pct": o3_stats.get("relative_ci95_pct", 100.0),
            "agent_runtime": agent_runtime,
            "agent_ci95_pct": agent_stats.get("relative_ci95_pct", 100.0),
        })

        # Compute deltas
        if o3_runtime > 0:
            result["vs_o3_pct"] = (o3_runtime - agent_runtime) / o3_runtime * 100
            result["beat_o3"] = agent_runtime < o3_runtime
        if o2_runtime > 0:
            result["vs_o2_pct"] = (o2_runtime - agent_runtime) / o2_runtime * 100
            result["beat_o2"] = agent_runtime < o2_runtime

        # Instruction counts
        result["o3_instr"] = metrics.count_instructions(o3_ir)
        result["agent_instr"] = metrics.count_instructions(agent_ir)

        # Optional: llvm-mca diagnostics
        o3_mca = mca.analyze(o3_ir)
        agent_mca = mca.analyze(agent_ir)
        if o3_mca and agent_mca:
            result["mca_o3_cycles"] = o3_mca.total_cycles
            result["mca_agent_cycles"] = agent_mca.total_cycles
            result["mca_o3_ipc"] = o3_mca.ipc
            result["mca_agent_ipc"] = agent_mca.ipc

    except Exception as e:
        result["error"] = str(e)
    finally:
        executor.cleanup()

    return result


def _infer_category(path: Path) -> str:
    s = str(path).lower().replace("\\", "/")
    if any(k in s for k in ["linear-algebra", "datamining", "stencils", "medley"]):
        return "polybench"
    if "mibench" in s:
        return "mibench"
    if "synthetic" in s:
        return "synthetic"
    if any(k in s for k in ["large_scale", "brotli", "zstd", "miniz", "lua"]):
        return "industrial"
    return "other"


def main():
    parser = argparse.ArgumentParser(description="Evaluate agent vs O2/O3")
    parser.add_argument("--passes", nargs="+", required=True, help="Agent's learned pass sequence")
    parser.add_argument("--benchmarks", nargs="*", help="Specific benchmark files (default: all)")
    parser.add_argument("--iterations", type=int, default=10, help="Runtime measurement iterations")
    parser.add_argument("--loop-count", type=int, default=500, help="Inner loop count for measurement")
    parser.add_argument("--output", type=str, default=None, help="JSON output file")
    args = parser.parse_args()

    if args.benchmarks:
        benchmarks = [Path(b) for b in args.benchmarks]
    else:
        benchmarks = get_benchmark_paths()

    metrics = MetricsCollector()
    mca = MCAAnalyzer()
    results = []

    print(f"Evaluating {len(benchmarks)} benchmarks with passes: {args.passes}")
    print("=" * 70)

    for i, bench in enumerate(benchmarks):
        print(f"[{i+1}/{len(benchmarks)}] {bench.name}...", end=" ", flush=True)
        r = evaluate_benchmark(bench, args.passes, metrics, mca, args.iterations, args.loop_count)
        results.append(r)

        if "error" in r:
            print(f"ERROR: {r['error']}")
        elif "beat_o3" in r:
            symbol = "+" if r["beat_o3"] else "-"
            print(f"vs O3: {r['vs_o3_pct']:+.2f}% [{symbol}]  vs O2: {r['vs_o2_pct']:+.2f}%")
        else:
            print("no runtime data")

    # Summary
    print("\n" + "=" * 70)
    valid = [r for r in results if "beat_o3" in r]
    if valid:
        beat_o3 = sum(1 for r in valid if r["beat_o3"])
        beat_o2 = sum(1 for r in valid if r.get("beat_o2", False))
        avg_vs_o3 = sum(r["vs_o3_pct"] for r in valid) / len(valid)
        avg_vs_o2 = sum(r.get("vs_o2_pct", 0) for r in valid) / len(valid)

        print(f"Beat O3: {beat_o3}/{len(valid)} benchmarks (avg {avg_vs_o3:+.2f}%)")
        print(f"Beat O2: {beat_o2}/{len(valid)} benchmarks (avg {avg_vs_o2:+.2f}%)")

        # By category
        cats = {}
        for r in valid:
            cat = r.get("category", "other")
            cats.setdefault(cat, []).append(r)
        for cat, cat_results in sorted(cats.items()):
            cat_beat = sum(1 for r in cat_results if r["beat_o3"])
            cat_avg = sum(r["vs_o3_pct"] for r in cat_results) / len(cat_results)
            print(f"  {cat}: {cat_beat}/{len(cat_results)} beat O3 (avg {cat_avg:+.2f}%)")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
