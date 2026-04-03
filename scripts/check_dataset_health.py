import os
import sys
import random
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.passes.pass_executor import compile_to_ir
from src.config import get_benchmark_paths, BENCHMARKS_DIR

def check_file(file_path):
    success, _ = compile_to_ir(str(file_path), output_path=None)
    # Clean up any potential byproduct (though compile_to_ir usually handles it or we pass None)
    # Actually compile_to_ir with output_path=None generates a .ll in the same dir by default in some versions,
    # or the current implementation might place it next to source.
    # Let's check the implementation of compile_to_ir in pass_executor.py
    # It defaults to source_path.with_suffix('.ll'). We should clean that up.
    ll_path = file_path.with_suffix('.ll')
    if ll_path.exists():
        try:
            os.remove(ll_path)
        except:
            pass
    return file_path, success

def check_dataset_health():
    print(f"Scanning benchmarks in {BENCHMARKS_DIR}...")
    
    # 1. Find all C files
    files = list(BENCHMARKS_DIR.rglob("*.c"))
    print(f"Total C files found: {len(files)}")

    # If more than 50 files, take a random sample for the demo
    if len(files) > 50:
        print("More than 50 files found. Taking a random sample of 50 for this demo.")
        files = random.sample(files, 50)
        print(f"Sampled files to check: {len(files)}")
    
    # 2. Check compilability
    results = defaultdict(lambda: {"total": 0, "broken": 0})
    
    print("Checking compilability (this may take a minute)...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(check_file, f): f for f in files}
        
        for i, future in enumerate(future_to_file):
            if i > 0 and i % 10 == 0:
                print(f"Processed {i}/{len(files)}...")
            
            f = future_to_file[future]
            try:
                _, success = future.result()
                
                # Determine suite name from path
                # e.g. benchmarks/large_scale/anghaben/... -> anghaben
                # e.g. benchmarks/mibench/... -> mibench
                parts = f.relative_to(BENCHMARKS_DIR).parts
                if len(parts) > 0:
                    suite = parts[0]
                    if suite == "large_scale" and len(parts) > 1:
                        suite = parts[1] # e.g. anghaben
                else:
                    suite = "root"
                    
                results[suite]["total"] += 1
                if not success:
                    results[suite]["broken"] += 1
                    
            except Exception as e:
                print(f"Error checking {f}: {e}")
    
    print(f"Processed {len(files)}/{len(files)}... Done.")

    # 3. Report
    print("\n" + "="*40)
    print("DATASET HEALTH REPORT")
    print("="*40)
    print(f"{'SUITE':<20} | {'TOTAL':<8} | {'BROKEN':<8} | {'FAILURE RATE':<8}")
    print("-" * 60)
    
    total_broken = 0
    total_files = 0
    
    for suite, stats in sorted(results.items()):
        broken = stats["broken"]
        total = stats["total"]
        rate = (broken / total) * 100 if total > 0 else 0
        
        print(f"{suite:<20} | {total:<8} | {broken:<8} | {rate:6.2f}%")
        
        total_broken += broken
        total_files += total
        
    print("-" * 60)
    grand_rate = (total_broken / total_files) * 100 if total_files > 0 else 0
    print(f"{'OVERALL':<20} | {total_files:<8} | {total_broken:<8} | {grand_rate:6.2f}%")
    print("="*40)

if __name__ == "__main__":
    check_dataset_health()
