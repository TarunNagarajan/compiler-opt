"""
Validate all benchmarks by attempting to compile each .c file to LLVM IR.
Moves broken files to benchmarks/_quarantine/ and generates a report.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from collections import Counter
from multiprocessing import Pool, cpu_count

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import get_benchmark_paths, CLANG

QUARANTINE_DIR = Path("benchmarks/_quarantine")


def test_compile(file_path):
    """Returns (path, ok, error_msg)"""
    from src.config import CLANG, LLVM_BIN_DIR
    CLANG_CPP = LLVM_BIN_DIR / "clang++.exe"
    
    compiler = str(CLANG_CPP) if file_path.suffix == '.cpp' else str(CLANG)
    
    try:
        r = subprocess.run(
            [compiler, "-S", "-emit-llvm", str(file_path), "-o", "-", "-Wno-everything"],
            capture_output=True, timeout=10
        )
        if r.returncode == 0:
            return (file_path, True, "")
        else:
            err = r.stderr.decode(errors='replace').strip().split('\n')[0][:120]
            return (file_path, False, err)
    except subprocess.TimeoutExpired:
        return (file_path, False, "TIMEOUT")
    except Exception as e:
        return (file_path, False, str(e)[:120])


def main():
    benchmarks = get_benchmark_paths()
    print(f"[VALIDATE] Testing {len(benchmarks)} benchmarks for compilability...")
    print(f"[VALIDATE] Using {cpu_count()} workers\n")

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    ok_files = []
    broken_files = []
    suite_stats = Counter()
    suite_broken = Counter()

    # Parallel compilation test
    with Pool(min(cpu_count(), 8)) as pool:
        results = pool.map(test_compile, benchmarks)

    for path, is_ok, err in results:
        # Determine suite name
        parts = path.parts
        idx = [i for i, p in enumerate(parts) if p == 'benchmarks'][0]
        suite = parts[idx + 1]
        suite_stats[suite] += 1

        if is_ok:
            ok_files.append(path)
        else:
            broken_files.append((path, err))
            suite_broken[suite] += 1

    # Report
    print(f"{'Suite':<25} {'Total':>6} {'OK':>6} {'Broken':>6} {'Rate':>7}")
    print("-" * 55)
    for suite in sorted(suite_stats.keys()):
        total = suite_stats[suite]
        broken = suite_broken.get(suite, 0)
        ok = total - broken
        rate = ok / total * 100
        print(f"{suite:<25} {total:>6} {ok:>6} {broken:>6} {rate:>6.1f}%")

    print("-" * 55)
    print(f"{'TOTAL':<25} {len(benchmarks):>6} {len(ok_files):>6} {len(broken_files):>6} {len(ok_files)/len(benchmarks)*100:>6.1f}%")

    # Move broken files to quarantine
    if broken_files:
        print(f"\n[VALIDATE] Moving {len(broken_files)} broken files to {QUARANTINE_DIR}/...")
        for path, err in broken_files:
            parts = path.parts
            idx = [i for i, p in enumerate(parts) if p == 'benchmarks'][0]
            relative = Path(*parts[idx + 1:])
            dest = QUARANTINE_DIR / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))

        # Save report
        report_path = QUARANTINE_DIR / "broken_report.txt"
        with open(report_path, "w") as f:
            for path, err in broken_files:
                f.write(f"{path.name}: {err}\n")
        print(f"[VALIDATE] Report saved to {report_path}")

    # Recount
    clean = get_benchmark_paths()
    print(f"\n[VALIDATE] Clean benchmark pool: {len(clean)} programs (was {len(benchmarks)})")


if __name__ == "__main__":
    main()
