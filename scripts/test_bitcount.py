import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from src.passes.metrics import MetricsCollector
from scripts.collect_sequences import compile_to_ir

collector = MetricsCollector()
ir_path = Path('scripts/bitcnts_linked.ll')
success = compile_to_ir(Path('benchmarks/mibench/mibench-master/automotive/bitcount/bitcnts.c'), ir_path)
print(f'Compile Success: {success}')
if success:
    try:
        cycles = collector.measure_runtime(str(ir_path), args=['100'], loop_count=10)
        print(f'Cycles: {cycles}')
    except Exception as e:
        print(f'Measurement Failed: {e}')
