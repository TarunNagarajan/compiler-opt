import subprocess
import time
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from ..config import CLANG, LLC


@dataclass
class Metrics:
    instruction_count: int
    code_size_bytes: int
    compilation_time_ms: float
    execution_time_ms: Optional[float] = None


class MetricsCollector:
    
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def count_instructions(self, ir_path: str) -> int:
        count = 0
        with open(ir_path, 'r') as f:
            in_function = False
            for line in f:
                stripped = line.strip()
                if stripped.startswith('define '):
                    in_function = True
                    continue
                if stripped == '}':
                    in_function = False
                    continue
                if in_function and stripped and not stripped.startswith(';'):
                    if not stripped.endswith(':') and not stripped.startswith('!'):
                        count += 1
        return count
    
    def measure_compilation_time(self, ir_path: str, passes: list) -> float:
        from ..config import OPT
        
        output = self.temp_dir / "temp_compile.ll"
        pass_args = ",".join(passes) if passes else "default<O0>"
        
        cmd = [str(OPT), "-S", f"-passes={pass_args}", str(ir_path), "-o", str(output)]
        
        start = time.perf_counter()
        subprocess.run(cmd, capture_output=True)
        end = time.perf_counter()
        
        return (end - start) * 1000
    
    def get_code_size(self, ir_path: str) -> int:
        obj_path = self.temp_dir / "temp.o"
        
        cmd = [str(LLC), "-filetype=obj", str(ir_path), "-o", str(obj_path)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if result.returncode == 0 and obj_path.exists():
                return obj_path.stat().st_size
        except:
            pass
        
        return Path(ir_path).stat().st_size
    
    def collect(self, ir_path: str, passes_applied: list = None) -> Metrics:
        passes_applied = passes_applied or []
        
        instruction_count = self.count_instructions(ir_path)
        code_size = self.get_code_size(ir_path)
        compile_time = self.measure_compilation_time(ir_path, passes_applied)
        
        return Metrics(
            instruction_count=instruction_count,
            code_size_bytes=code_size,
            compilation_time_ms=compile_time
        )
    
    def compare(self, before_path: str, after_path: str, passes: list) -> dict:
        before = self.collect(before_path, [])
        after = self.collect(after_path, passes)
        
        instr_reduction = (before.instruction_count - after.instruction_count) / max(before.instruction_count, 1)
        size_reduction = (before.code_size_bytes - after.code_size_bytes) / max(before.code_size_bytes, 1)
        
        return {
            'before': before,
            'after': after,
            'instruction_reduction': instr_reduction,
            'size_reduction': size_reduction,
            'passes': passes
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python metrics.py <ir_file.ll> [ir_file2.ll]")
        sys.exit(1)
    
    collector = MetricsCollector()
    metrics = collector.collect(sys.argv[1])
    
    print(f"\n=== Metrics for {sys.argv[1]} ===")
    print(f"Instructions:     {metrics.instruction_count}")
    print(f"Code size:        {metrics.code_size_bytes} bytes")
    print(f"Compile time:     {metrics.compilation_time_ms:.2f} ms")
    
    if len(sys.argv) >= 3:
        print(f"\n=== Comparing with {sys.argv[2]} ===")
        comparison = collector.compare(sys.argv[1], sys.argv[2], [])
        print(f"Instruction reduction: {comparison['instruction_reduction']:.1%}")
        print(f"Size reduction:        {comparison['size_reduction']:.1%}")
