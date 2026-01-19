import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

from ..config import OPT, CLANG, LLVM_PASSES


@dataclass
class PassResult:
    success: bool
    input_path: str
    output_path: str
    passes_applied: List[str]
    error_message: Optional[str] = None


class PassExecutor:
    
    def __init__(self, work_dir: Optional[str] = None):
        self.work_dir = Path(work_dir) if work_dir else Path(tempfile.mkdtemp())
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def apply_pass(self, ir_path: str, pass_name: str, output_path: Optional[str] = None) -> PassResult:
        return self.apply_passes(ir_path, [pass_name], output_path)
    
    def apply_passes(self, ir_path: str, passes: List[str], output_path: Optional[str] = None) -> PassResult:
        ir_path = Path(ir_path)
        if not ir_path.exists():
            return PassResult(
                success=False,
                input_path=str(ir_path),
                output_path="",
                passes_applied=passes,
                error_message=f"Input file not found: {ir_path}"
            )
        
        if output_path is None:
            suffix = "_" + "_".join(passes[:3])
            output_path = self.work_dir / f"{ir_path.stem}{suffix}.ll"
        output_path = Path(output_path)
        
        pass_args = ",".join(passes)
        cmd = [
            str(OPT),
            "-S",
            f"-passes={pass_args}",
            str(ir_path),
            "-o", str(output_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return PassResult(
                    success=False,
                    input_path=str(ir_path),
                    output_path=str(output_path),
                    passes_applied=passes,
                    error_message=result.stderr
                )
            
            return PassResult(
                success=True,
                input_path=str(ir_path),
                output_path=str(output_path),
                passes_applied=passes
            )
            
        except subprocess.TimeoutExpired:
            return PassResult(
                success=False,
                input_path=str(ir_path),
                output_path=str(output_path),
                passes_applied=passes,
                error_message="Pass application timed out"
            )
        except Exception as e:
            return PassResult(
                success=False,
                input_path=str(ir_path),
                output_path=str(output_path),
                passes_applied=passes,
                error_message=str(e)
            )
    
    def apply_sequence(self, ir_path: str, pass_sequence: List[str]) -> List[PassResult]:
        results = []
        current_ir = ir_path
        
        for i, pass_name in enumerate(pass_sequence):
            output_path = self.work_dir / f"step_{i}_{pass_name}.ll"
            result = self.apply_pass(current_ir, pass_name, str(output_path))
            results.append(result)
            
            if not result.success:
                break
            
            current_ir = result.output_path
        
        return results
    
    def cleanup(self):
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir, ignore_errors=True)


def compile_to_ir(source_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
    source_path = Path(source_path)
    
    if output_path is None:
        output_path = source_path.with_suffix('.ll')
    output_path = Path(output_path)
    
    cmd = [
        str(CLANG),
        "-S", "-emit-llvm",
        "-O0",
        "-Xclang", "-disable-O0-optnone",
        str(source_path),
        "-o", str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return False, result.stderr
        return True, str(output_path)
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python pass_executor.py <ir_file.ll> <pass_name> [pass_name2 ...]")
        print(f"\nAvailable passes: {', '.join(LLVM_PASSES)}")
        sys.exit(1)
    
    ir_file = sys.argv[1]
    passes = sys.argv[2:]
    
    executor = PassExecutor()
    
    print(f"Applying passes {passes} to {ir_file}...")
    result = executor.apply_passes(ir_file, passes)
    
    if result.success:
        print(f"✓ Success! Output: {result.output_path}")
        
        from ..features import extract_features
        f1 = extract_features(ir_file)
        f2 = extract_features(result.output_path)
        
        import numpy as np
        diff = np.linalg.norm(f2 - f1)
        print(f"  Feature distance: {diff:.4f}")
    else:
        print(f"✗ Failed: {result.error_message}")
    
    executor.cleanup()
