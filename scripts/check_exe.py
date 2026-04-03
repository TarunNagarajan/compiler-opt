import subprocess
import re

file_name = "benchmarks/linear-algebra/mvt.c"

def run_and_parse(opt_flag):
    # Compile
    subprocess.run(["clang", opt_flag, file_name, "-o", "mvt_test.exe"], check=True)
    
    # Run multiple times and take the minimum (best) to reduce noise
    times = []
    for _ in range(5):
        out = subprocess.run(["./mvt_test.exe"], capture_output=True, text=True, check=True).stdout
        match = re.search(r"MVT Execution Time: ([0-9.]+) s", out)
        if match:
            times.append(float(match.group(1)))
    
    return min(times)

o0_time = run_and_parse("-O0")
print(f"O0 runtime: {o0_time:.6f}s")

o2_time = run_and_parse("-O2")
print(f"O2 runtime: {o2_time:.6f}s")
print(f"O2 Speedup vs O0: {(o0_time - o2_time) / o0_time * 100:.2f}%")

o3_time = run_and_parse("-O3")
print(f"O3 runtime: {o3_time:.6f}s")
print(f"O3 Speedup vs O0: {(o0_time - o3_time) / o0_time * 100:.2f}%")
