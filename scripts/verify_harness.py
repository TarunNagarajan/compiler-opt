from pathlib import Path
import sys
# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.passes.metrics import MetricsCollector

def test_harness():
    collector = MetricsCollector()
    test_ir = Path("scripts/work_test.ll")
    
    if not test_ir.exists():
        print(f"Compiling {test_ir.with_suffix('.c')} to IR...")
        from scripts.collect_sequences import compile_to_ir
        compile_to_ir(test_ir.with_suffix('.c'), test_ir)

    print("Starting 10-run convergence test...")
    results = []
    for i in range(10):
        cycles = collector.measure_runtime(str(test_ir))
        print(f"Run {i+1}: {cycles}")
        results.append(cycles)
    
    import numpy as np
    mean_cycles = np.mean(results)
    std_cycles = np.std(results)
    variance_pct = (std_cycles / mean_cycles) * 100
    print(f"\nMean: {mean_cycles}")
    print(f"StdDev: {std_cycles}")
    print(f"Variance: {variance_pct:.4f}%")
    
    # Check for trend (Convergence)
    first_half = np.mean(results[:5])
    second_half = np.mean(results[5:])
    print(f"First 5 Avg: {first_half}")
    print(f"Second 5 Avg: {second_half}")
    if second_half < first_half:
         print("Trend: Cycles decreasing (Potential Turbo ramp-up/Warmup effect)")
    else:
         print("Trend: Cycles stable or increasing")

if __name__ == "__main__":
    test_harness()
