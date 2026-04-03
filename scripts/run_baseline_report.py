import sys
import os
import subprocess
import time
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import CLANG, OPT, LLC
from src.passes.metrics import MetricsCollector

def compile_c_to_ll(c_path: Path, output_path: Path) -> bool:
    cmd = [
        str(CLANG),
        "-S", "-emit-llvm",
        "-O0",
        "-Xclang", "-disable-O0-optnone",
        str(c_path),
        "-o", str(output_path)
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {c_path}: {e.stderr.decode()}")
        return False

def run_opt(input_ll: Path, output_ll: Path, level: str) -> float:
    cmd = [
        str(OPT),
        "-S",
        level,
        str(input_ll),
        "-o", str(output_ll)
    ]
    start = time.perf_counter()
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error optimizing {input_ll} with {level}: {e.stderr.decode()}")
        return 0.0
    end = time.perf_counter()
    return (end - start) * 1000  # ms

def get_binary_size(ll_path: Path) -> int:
    obj_path = ll_path.with_suffix('.o')
    cmd = [str(LLC), "-filetype=obj", str(ll_path), "-o", str(obj_path)]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return obj_path.stat().st_size
    except:
        return 0

def main():
    results_dir = Path("results/baseline")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    collector = MetricsCollector()
    
    levels = ["-O0", "-O1", "-O2", "-O3", "-Os"]
    
    # Import categories from config
    from src.config import BENCHMARKS_DIR, POLYBENCH_CATEGORIES
    
    for category in POLYBENCH_CATEGORIES:
        category_dir = BENCHMARKS_DIR / category
        if not category_dir.exists():
            continue
            
        c_files = list(category_dir.glob("*.c"))
        if not c_files:
            continue
            
        print(f"\n{'='*70}")
        print(f" {category.upper()}")
        print(f"{'='*70}")
        print(f"{'Benchmark':<15} {'Level':<8} {'Instr':<10} {'Size (B)':<10} {'Time (ms)':<10} {'Reduct %':<10}")
        print("-" * 70)
        
        for c_file in sorted(c_files):
            if c_file.name == "utilities.c": continue
            
            base_ir = results_dir / f"{c_file.stem}_base.ll"
            if not compile_c_to_ll(c_file, base_ir):
                continue
                
            base_metrics = collector.collect(str(base_ir))
            base_instr = base_metrics.instruction_count
            
            print(f"\n[{c_file.stem}]")
            
            for level in levels:
                opt_ir = results_dir / f"{c_file.stem}{level}.ll"
                
                if level == "-O0":
                    metrics = base_metrics
                    compile_time = 0.0
                else:
                    compile_time = run_opt(base_ir, opt_ir, level)
                    metrics = collector.collect(str(opt_ir))
                
                target_ll = base_ir if level == "-O0" else opt_ir
                bin_size = get_binary_size(target_ll)
                
                reduction = 0.0
                if base_instr > 0:
                    reduction = (base_instr - metrics.instruction_count) / base_instr * 100
                
                print(f"{c_file.stem:<15} {level:<8} {metrics.instruction_count:<10} {bin_size:<10} {compile_time:<10.2f} {reduction:<10.1f}")

if __name__ == "__main__":
    main()
