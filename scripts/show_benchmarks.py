import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import BENCHMARKS_DIR, POLYBENCH_CATEGORIES

def print_slow(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    print()
    print_slow("=" * 64)
    print_slow("       POLYBENCH/C 4.2 BENCHMARK SUITE (30 Kernels)        ")
    print_slow("=" * 64)
    print()
    time.sleep(0.5)

    total = 0
    for category in POLYBENCH_CATEGORIES:
        category_path = BENCHMARKS_DIR / category
        
        if not category_path.exists():
            continue
        
        benchmarks = sorted([f.stem for f in category_path.glob('*.c')])
        total += len(benchmarks)
        
        print_slow(f"[{category.upper()}] ({len(benchmarks)} kernels)", delay=0.01)
        print_slow("-" * 40, delay=0.005)
        
        for i, bench in enumerate(benchmarks):
            prefix = "|--" if i < len(benchmarks) - 1 else "`--"
            print_slow(f"  {prefix} {bench}.c", delay=0.015)
            time.sleep(0.1)
        
        print()
        time.sleep(0.3)

    print_slow("=" * 64)
    print_slow(f"Total: {total} benchmark programs")
    print()

if __name__ == "__main__":
    main()
