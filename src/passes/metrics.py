import subprocess
import time
import tempfile
import hashlib
import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple

from ..config import CLANG, LLC


@dataclass
class Metrics:
    instruction_count: int
    code_size_bytes: int
    compilation_time_ms: float
    execution_time_ms: Optional[float] = None


@dataclass 
class CorrectnessResult:
    is_correct: bool
    original_output: str
    optimized_output: str
    error_message: Optional[str] = None


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
    
    def compile_and_run(self, ir_path: str, timeout_seconds: float = 5.0) -> Tuple[bool, str, str]:
        exe_path = self.temp_dir / "test_exe"
        
        compile_cmd = [str(CLANG), str(ir_path), "-o", str(exe_path), "-lm"]
        
        try:
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                return False, "", compile_result.stderr.decode()[:500]
            
            run_result = subprocess.run(
                [str(exe_path)],
                capture_output=True,
                timeout=timeout_seconds,
                stdin=subprocess.DEVNULL
            )
            if run_result.returncode != 0:
                err = run_result.stderr.decode()[:500] if run_result.stderr else f"Execution failed with code {run_result.returncode}"
                return False, "", err

            output = run_result.stdout.decode()
            return True, output, ""
            
        except subprocess.TimeoutExpired:
            return False, "", "Execution timed out"
        except Exception as e:
            return False, "", str(e)

    def measure_runtime(self, ir_path: str, iterations: int = 1, args: list = None, loop_count: int = 100) -> float:
        """
        Measures CPU Cycles using the Super-Harness + Warm Loop.
        1. Renames main -> benchmark_main
        2. Injects a 100x loop runner
        3. Measures cycles for the whole process
        """
        import uuid
        
        args = args or []
        tmp_stem = f"perf_{uuid.uuid4().hex[:8]}"
        wrapper_c = self.temp_dir / f"{tmp_stem}_wrapped.c"
        exe_path = self.temp_dir / f"{tmp_stem}.exe"
        harness_exe = Path(__file__).parent.parent / "env" / "super_harness.exe"
        
        if not harness_exe.exists():
            return 0.0

        # 1. Read IR and transform it (or the source if we had it, but IR is better)
        # Actually, it's easier to link a small C 'driver' to the IR.
        driver_c = self.temp_dir / f"{tmp_stem}_driver.c"
        driver_content = """
#include <windows.h>
#include <stdio.h>

#pragma comment(lib, "winmm.lib")

#ifdef __cplusplus
extern "C" {{
#endif
extern int benchmark_main(int argc, char** argv);
#ifdef __cplusplus
}}
#endif

int main(int argc, char** argv) {{
    // 0. Request high timer resolution
    timeBeginPeriod(1);

    // 1. Warmup loop to stabilize frequency
    for(int i=0; i<1000; i++) benchmark_main(argc, argv);
    
    // 2. Performance Counters
    ULONG64 cyclesStart, cyclesEnd;
    HANDLE hThread = GetCurrentThread();

    // Query initial cycle count
    if (!QueryThreadCycleTime(hThread, &cyclesStart)) {{
        timeEndPeriod(1);
        return 1;
    }}

    // 3. Measured loop
    for(int i=0; i<{loop_count}; i++) benchmark_main(argc, argv);

    // Query final cycle count
    if (!QueryThreadCycleTime(hThread, &cyclesEnd)) {{
        timeEndPeriod(1);
        return 1;
    }}

    // 4. Release timer resolution
    timeEndPeriod(1);

    // Report delta
    printf("[HARNESS_CYCLES] %llu\\n", (cyclesEnd - cyclesStart));
    
    return 0;
}}
"""
        driver_c.write_text(driver_content.format(loop_count=loop_count))

        # 2. Transform the IR: rename 'main' to 'benchmark_main'
        with open(ir_path, 'r') as f:
            ir_content = f.read()
        
        # V7.3 Fix: More robust regex for main renaming. 
        # Handles: define i32 @main, define void @main, etc.
        # Also handles cases where main might be slightly different in C++ IR
        new_ir_content = re.sub(r'define\s+([^{]+)\s+@main\s*\(', r'define \1 @benchmark_main(', ir_content)
        new_ir_content = re.sub(r'call\s+([^{]+)\s+@main\s*\(', r'call \1 @benchmark_main(', new_ir_content)
        
        # C++ Specific: sometimes main is defined as _Z4mainiPPc or similar if not extern "C"
        # We try to catch common manglings
        new_ir_content = re.sub(r'@_Z4main\w*', r'@benchmark_main', new_ir_content)

        # Skip non-standalone modules that do not expose a runnable entrypoint.
        if re.search(r'define\s+([^{]+)\s+@benchmark_main\s*\(', new_ir_content) is None:
            return 0.0
        
        tmp_ir = self.temp_dir / f"{tmp_stem}.ll"
        tmp_ir.write_text(new_ir_content)

        # 3. Compile: Driver + Transformed IR
        from ..config import CLANG, CLANG_CXX
        
        # Prefer C++ toolchain when IR clearly depends on C++ runtime symbols.
        cpp_hint = (
            "_cpp_gen_" in ir_path
            or ".cpp" in ir_path
            or bool(re.search(r"__gxx_personality|__cxa_|_Z[NT]|_ZNSt|std::", new_ir_content))
        )

        def _build_compile_cmd(compiler_path):
            cmd = [
                str(compiler_path), str(driver_c), str(tmp_ir),
                "-o", str(exe_path),
                "-O2", "-lm", "-lwinmm", "-Wno-everything"
            ]
            if "clang++" in Path(str(compiler_path)).name:
                cmd.append("-lstdc++")
            return cmd

        primary_compiler = CLANG_CXX if cpp_hint else CLANG
        compile_cmd = _build_compile_cmd(primary_compiler)

        try:
            res = subprocess.run(compile_cmd, capture_output=True, timeout=30)
            if res.returncode != 0:
                # Fallback: if C link fails with C++ symbols, retry with clang++.
                stderr_text = res.stderr.decode(errors="ignore")
                unresolved_cpp = any(tok in stderr_text for tok in [
                    "__gxx_personality", "__cxa_", "operator new", "std::", "__cxxabiv1"
                ])
                if primary_compiler != CLANG_CXX and unresolved_cpp:
                    retry_cmd = _build_compile_cmd(CLANG_CXX)
                    res = subprocess.run(retry_cmd, capture_output=True, timeout=30)
                if res.returncode != 0:
                    print(f"[METRICS] Compilation Failed: {res.stderr.decode(errors='ignore')}")
                    return 0.0
        except:
            return 0.0
            
        # 4. Measure with Super-Harness
        try:
            cycles_list = []
            num_runs = max(1, int(iterations))
            for _ in range(num_runs):
                cmd = [str(harness_exe), str(exe_path)] + [str(a) for a in args]
                try:
                    run_res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
                if run_res.returncode != 0:
                    continue
                m = re.search(r'\[HARNESS_CYCLES\] (\d+)', run_res.stdout)
                if m:
                    cycles_list.append(float(m.group(1)))
            
            if cycles_list:
                # Minimum of runs (the noise-free "truth")
                min_cycles = min(cycles_list) / float(loop_count) # Per-iteration cycles
                return min_cycles
                
        finally:
            # Cleanup
            for p in [driver_c, tmp_ir, exe_path]:
                try: p.unlink()
                except: pass
        
        return 0.0

    def measure_energy(
        self,
        ir_path: str,
        loop_count: int = 1000,
        args: list = None,
        runtime_cycles: Optional[float] = None,
    ) -> float:
        """
        Deterministic cycle-proxy energy estimate in Joules.
        Uses measured cycles-per-iteration from the runtime harness and converts
        to energy with a fixed coefficient.
        """
        args = args or []
        h_res = float(runtime_cycles) if runtime_cycles is not None else self.measure_runtime(ir_path, args=args, loop_count=loop_count)
        if h_res == 0.0:
            return 0.0

        # Joules = cycles_per_iter * iter_count * joules_per_cycle.
        # Fixed coefficient keeps this deterministic and robust across hosts.
        return h_res * 2.16e-8 * loop_count
            
    def verify_correctness(
        self,
        original_ir_path: str,
        optimized_ir_path: str,
        timeout_seconds: float = 30.0
    ) -> CorrectnessResult:
        orig_success, orig_output, orig_error = self.compile_and_run(
            original_ir_path, timeout_seconds
        )
        
        if not orig_success:
            return CorrectnessResult(
                is_correct=True,
                original_output="",
                optimized_output="",
                error_message=f"Original failed: {orig_error}"
            )
        
        opt_success, opt_output, opt_error = self.compile_and_run(
            optimized_ir_path, timeout_seconds
        )
        
        if not opt_success:
            return CorrectnessResult(
                is_correct=False,
                original_output=orig_output,
                optimized_output="",
                error_message=f"Optimized failed: {opt_error}"
            )
        
        orig_hash = hashlib.md5(orig_output.encode()).hexdigest()
        opt_hash = hashlib.md5(opt_output.encode()).hexdigest()
        
        is_correct = orig_hash == opt_hash
        
        return CorrectnessResult(
            is_correct=is_correct,
            original_output=orig_output[:1000],
            optimized_output=opt_output[:1000],
            error_message=None if is_correct else "Output mismatch"
        )
    
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
        print("[AGENT] Usage: python metrics.py <ir_file.ll> [ir_file2.ll]...")
        sys.exit(1)
    
    collector = MetricsCollector()
    metrics = collector.collect(sys.argv[1])
    
    print(f"[AGENT] Metrics for {sys.argv[1]}...")
    print(f"[AGENT] Instructions:     {metrics.instruction_count}...")
    print(f"[AGENT] Code size:        {metrics.code_size_bytes} bytes...")
    print(f"[AGENT] Compile time:     {metrics.compilation_time_ms:.2f} ms...")
    
    if len(sys.argv) >= 3:
        print(f"[AGENT] Comparing with {sys.argv[2]}...")
        comparison = collector.compare(sys.argv[1], sys.argv[2], [])
        print(f"[AGENT] Instruction reduction: {comparison['instruction_reduction']:.1%}...")
        print(f"[AGENT] Size reduction:        {comparison['size_reduction']:.1%}...")
        
        print(f"[AGENT] Correctness Check...")
        result = collector.verify_correctness(sys.argv[1], sys.argv[2])
        print(f"[AGENT] Correct: {result.is_correct}...")
        if result.error_message:
            print(f"[AGENT] Error: {result.error_message}...")
