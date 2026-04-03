import sys
import os
import subprocess
from pathlib import Path

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{result.stderr}")
        return False
    return True

def count_instructions(ll_file):
    with open(ll_file, 'r') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith(';') and not line.startswith('!') and not line.startswith('}'):
            if '=' in line or 'call' in line or 'br' in line or 'ret' in line or 'store' in line:
                count += 1
    return count

def main():
    print("--- DIAGNOSING THE UNROLL BLOAT (%) ---")
    
    # 1. Compile fresh IR
    run_cmd(["clang", "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-S", "custom_benchmark.c", "-o", "custom.ll"])
    
    # 2. Baseline cleanup (Mem2Reg)
    run_cmd(["opt", "-S", "-passes=mem2reg,simplifycfg", "custom.ll", "-o", "baseline.ll"])
    baseline_inst = count_instructions("baseline.ll")
    print(f"Baseline Instructions: {baseline_inst}")
    print("-" * 50)
    
    # 3. Naive Unroll (What the user saw)
    run_cmd(["opt", "-S", "-passes=function(loop-unroll)", "baseline.ll", "-o", "naive_unroll.ll"])
    naive_inst = count_instructions("naive_unroll.ll")
    naive_pct = ((naive_inst - baseline_inst) / baseline_inst) * 100
    print(f"Naive Unroll Size......: {naive_inst} instructions ({naive_pct:+.2f}% BLOAT)")
    
    # 4. Canonical Unroll (What the World Model trained on)
    # The World Model dataset environment rotated the loops before unrolling them.
    run_cmd(["opt", "-S", "-passes=function(loop-rotate,loop-simplify,loop-unroll)", "baseline.ll", "-o", "canon_unroll.ll"])
    canon_inst = count_instructions("canon_unroll.ll")
    canon_pct = ((canon_inst - baseline_inst) / baseline_inst) * 100
    print(f"Canonical Unroll Size...: {canon_inst} instructions ({canon_pct:+.2f}% SHRINKAGE)")
    
    print("-" * 50)
    print("World Model Predicted.: -17.04%")
    print(f"World Model Error.....: {abs(-17.04 - canon_pct):.2f}%")

if __name__ == "__main__":
    main()
