
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv

def test_compilation():
    print(f"Testing compilation of ALL synthetic benchmarks...")
    
    # Get all synthetic files
    syn_dir = Path("benchmarks/synthetic")
    syn_files = list(syn_dir.glob("*.c"))
    
    # We cheat and pass a dummy list to init env
    env = CompilerOptEnv([str(syn_files[0])])
    
    failures = 0
    total = len(syn_files)
    
    for i, syn_path in enumerate(syn_files):
        try:
            # We must wrap in try-except because env.reset might raise if it fails
            # But wait, env.reset catches exceptions and prints "Skipping" then retries with random.
            # IF we use options={'ir_path': ...}, it re-raises the exception if it fails (is_forced=True).
            env.reset(options={"ir_path": str(syn_path)})
        except Exception as e:
            print(f"Failed {syn_path.name}: {e}")
            failures += 1
            
        if (i+1) % 100 == 0:
            print(f"Processed {i+1}/{total}...")
            
    print(f"Done. Failures: {failures}/{total}")

if __name__ == "__main__":
    test_compilation()
