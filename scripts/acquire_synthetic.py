
import os
import random
import sys
import argparse
from pathlib import Path
OUTPUT_DIR = Path("benchmarks/synthetic")

OUTPUT_DIR = Path("benchmarks/synthetic")
NUM_BENCHMARKS = 1000

def generate_c_code(seed):
    random.seed(seed)
    
    code = []
    code.append("#include <stdio.h>")
    code.append("#include <stdlib.h>")
    code.append("")
    
    array_size = random.randint(100, 1000)
    code.append(f"#define N {array_size}")
    code.append("int A[N];")
    code.append("int B[N];")
    code.append("int C[N];")
    code.append("")
    
    code.append("void sink(int x) {")
    code.append("    if (x == 123456789) printf(\"%d\", x);") 
    code.append("}")
    code.append("")
    
    code.append("int main() {")
    code.append("    // Initialize")
    code.append("    for (int i = 0; i < N; i++) {")
    code.append("        A[i] = i;")
    code.append("        B[i] = i * 2;")
    code.append("        C[i] = 0;")
    code.append("    }")
    code.append("")
    
    num_kernels = random.randint(2, 5)
    
    for k in range(num_kernels):
        kernel_type = random.choice(["vector_add", "reduction", "matmul_fake", "branchy"])
        
        code.append(f"    // Kernel {k}: {kernel_type}")
        code.append("    {")
        
        if kernel_type == "vector_add":
            code.append("        for (int i = 0; i < N; i++) {")
            ops = random.choice(["+", "-", "*", "^", "|", "&"])
            code.append(f"            C[i] += A[i] {ops} B[i];")
            code.append("        }")
            
        elif kernel_type == "reduction":
            code.append("        int sum = 0;")
            code.append("        for (int i = 0; i < N; i++) {")
            code.append("            sum += A[i];")
            code.append("        }")
            code.append("        sink(sum);")
            
        elif kernel_type == "matmul_fake":
            code.append("        for (int i = 0; i < N/10; i++) {")
            code.append("            for (int j = 0; j < N/10; j++) {")
            code.append("                C[i] += A[j] * B[j];")
            code.append("            }")
            code.append("        }")
            
        elif kernel_type == "branchy":
            code.append("        for (int i = 0; i < N; i++) {")
            code.append("            if (A[i] % 2 == 0) {")
            code.append("                C[i] = A[i] * 3;")
            code.append("            } else {")
            code.append("                C[i] = B[i] + 5;")
            code.append("            }")
            code.append("        }")
            
        code.append("    }")
        code.append("")
        
    code.append("    // Prevent Dead Code Elimination")
    code.append("    int total = 0;")
    code.append("    for (int i = 0; i < N; i++) total += C[i];")
    code.append("    sink(total);")
    code.append("")
    code.append("    return 0;")
    code.append("}")
    
    return "\n".join(code)

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic C benchmarks.")
    parser.add_argument("--count", type=int, default=NUM_BENCHMARKS,
                        help="Number of benchmarks to generate.")
    parser.add_argument("--output_dir", type=Path, default=OUTPUT_DIR,
                        help="Directory to save the generated benchmarks.")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[Synthetic] Generating {args.count} benchmarks in {output_dir}...")
    
    success_count = 0
    for i in range(args.count):
        filename = f"syn_{i:04d}.c"
        filepath = output_dir / filename
        
        try:
            code = generate_c_code(seed=i)
            
            with open(filepath, "w") as f:
                f.write(code)
                
            success_count += 1
            if i % 5 == 0:
                size_kb = len(code) / 1024
                print(f"[Gen] Created {filename} ({size_kb:.2f} KB) - Valid")
                
        except Exception as e:
            print(f"[Error] Failed to generate {filename}: {e}")

    print(f"\n[Synthetic] Complete! Generated {success_count}/{args.count} benchmarks.")
    print(f"[Synthetic] Saved to {output_dir}")
    
if __name__ == "__main__":
    main()
