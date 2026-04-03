import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from src.passes.metrics import MetricsCollector
from scripts.collect_sequences import compile_to_ir

collector = MetricsCollector()
ir_path = Path('scripts/basicmath_linked.ll')
success = compile_to_ir(Path('benchmarks/mibench/mibench-master/automotive/basicmath/basicmath_small.c'), ir_path)
print(f'Compile Success: {success}')
if success:
    try:
        cycles = collector.measure_runtime(str(ir_path), iterations=1, loop_count=1)
        print(f'Cycles: {cycles}')
    except Exception as e:
        print(f'Measurement Failed: {e}')
