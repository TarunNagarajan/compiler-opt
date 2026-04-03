import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.passes.metrics import MetricsCollector
from scripts.collect_sequences import compile_to_ir

def audit_benchmark(name, source_path, args=None, loop_count=100):
    print(f"\n--- Auditing: {name} (loop={loop_count}) ---")
    ir_path = Path(f"scripts/{name}_audit.ll")
    
    if not ir_path.exists():
        print(f"Compiling {source_path} to IR...")
        if not compile_to_ir(Path(source_path), ir_path):
            print(f"FAILED to compile {name}")
            return
            
    collector = MetricsCollector()
    
    # We want to prove that the MINIMUM of 7 runs is stable.
    # So we do 3 "Measurement Sets", each being a Min-of-7.
    min_results = []
    
    print(f"Running 3 'Min-of-7' sets for {name}...")
    for j in range(3):
        print(f"  Set {j+1} starting...")
        # iterations=7 means measure_runtime will do Min-of-7 internally
        min_cycle = collector.measure_runtime(str(ir_path), iterations=7, args=args, loop_count=loop_count)
        print(f"    Set {j+1} Result (Min-of-7): {min_cycle:,.2f} cycles")
        min_results.append(min_cycle)
    
    mean = np.mean(min_results)
    std = np.std(min_results)
    variance = (std / mean) * 100 if mean > 0 else 0
    
    print(f"Final Stability for {name} (Min-to-Min):")
    print(f"  Mean:     {mean:,.2f}")
    print(f"  StdDev:   {std:,.2f}")
    print(f"  Variance: {variance:.4f}%")
    
    return variance

def main():
    benchmarks = [
        {
            "name": "stencil",
            "source": "benchmarks/diverse_synthetic/stencil/stencil_0000.c",
            "args": [],
            "loop_count": 1000
        },
        {
            "name": "gemm",
            "source": "benchmarks/linear-algebra/gemm.c",
            "args": [],
            "loop_count": 10
        },
        {
            "name": "qsort",
            "source": "benchmarks/mibench/mibench-master/automotive/qsort/qsort_small.c",
            "args": ["scripts/qsort_data.txt"],
            "loop_count": 100
        },
        {
            "name": "deep_call",
            "source": "benchmarks/diverse_synthetic/deep_call_chain/deep_call_chain_0000.c",
            "args": [],
            "loop_count": 1000
        }
    ]
    
    variances = []
    for b in benchmarks:
        v = audit_benchmark(b['name'], b['source'], b['args'], b['loop_count'])
        if v is not None:
            variances.append(v)
            
    if variances:
        print(f"\nOverall Average Variance: {np.mean(variances):.4f}%")

if __name__ == "__main__":
    main()
