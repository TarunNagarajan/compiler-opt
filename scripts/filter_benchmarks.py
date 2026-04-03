
import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.passes.pass_executor import compile_to_ir

BENCH_DIR = Path("benchmarks/large_scale/anghaben")

def check_and_clean(file_path):
    """
    Tries to compile the file. If fails, deletes it.
    Returns True if kept, False if deleted.
    """
    try:
        # We don't need the output, just want to see if it compiles
        success, _ = compile_to_ir(str(file_path), output_path=None)
        
        if not success:
            os.remove(file_path)
            return False
            
        # Also clean up the generated .ll file to save space/clutter
        ll_path = file_path.with_suffix('.ll')
        if ll_path.exists():
            os.remove(ll_path)
            
        return True
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        try:
            os.remove(file_path)
        except:
            pass
        return False

def filter_benchmarks():
    if not BENCH_DIR.exists():
        print(f"Benchmark directory {BENCH_DIR} does not exist.")
        return

    files = list(BENCH_DIR.rglob("*.c"))
    print(f"Found {len(files)} files in {BENCH_DIR}. Filtering...")
    
    kept = 0
    deleted = 0
    
    # Use threading to speed up compilation checks
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check_and_clean, files))
        
    kept = sum(results)
    deleted = len(results) - kept
    
    print(f"Filtering Complete.")
    print(f"Kept: {kept}")
    print(f"Deleted: {deleted}")
    print(f"Valid benchmarks remaining: {kept}")

if __name__ == "__main__":
    filter_benchmarks()
