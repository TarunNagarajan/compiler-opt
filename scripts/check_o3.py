import sys
from pathlib import Path
sys.path.insert(0, str(Path('.')))
from src.env import CompilerOptEnv, RewardMode
from src.passes.metrics import MetricsCollector
import subprocess

file_name = sys.argv[1] if len(sys.argv) > 1 else "benchmarks/linear-algebra/mvt.c"
env = CompilerOptEnv([file_name], reward_mode=RewardMode.SPEED)
obs, info = env.reset()

m = env.metrics

o0_time = m.measure_runtime(env.original_ir_path, iterations=10)
print(f"O0 runtime: {o0_time:.4f}s")

stem = Path(file_name).stem
o2_file = f"{stem}_o2.ll"
subprocess.run(["clang", "-O2", "-S", "-emit-llvm", file_name, "-o", o2_file])
o2_time = m.measure_runtime(o2_file, iterations=10)
print(f"O2 runtime: {o2_time:.4f}s")
print(f"O2 Speedup: {(o0_time - o2_time) / o0_time * 100:.2f}%")

o3_file = f"{stem}_o3.ll"
subprocess.run(["clang", "-O3", "-S", "-emit-llvm", file_name, "-o", o3_file])
o3_time = m.measure_runtime(o3_file, iterations=10)
print(f"O3 runtime: {o3_time:.4f}s")
print(f"O3 Speedup: {(o0_time - o3_time) / o0_time * 100:.2f}%")
