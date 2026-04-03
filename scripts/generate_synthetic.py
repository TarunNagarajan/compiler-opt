import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

STRESS_BIN = Path("C:/msys64/mingw64/bin/llvm-stress.exe")
OUTPUT_DIR = Path("benchmarks/large_scale/synthetic")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Generate 500 adversarial files
NUM_FILES = 500

def generate_stress(idx):
    out_path = OUTPUT_DIR / f"stress_{idx}.ll"
    # Size 500-2000 instructions
    size = 500 + (idx * 3)
    cmd = [str(STRESS_BIN), f"-size={size}", "-o", str(out_path)]
    subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    print(f"Generating {NUM_FILES} adversarial IR files...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(NUM_FILES):
            executor.submit(generate_stress, i)
    print("Done.")
