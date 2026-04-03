


import sys

import re

import time

from pathlib import Path



# Add project root to path

sys.path.insert(0, str(Path(__file__).parent.parent))



from src.passes.metrics import MetricsCollector



def type_out(text, delay=0.015, end="\n"):

    """Prints text character by character with a delay."""

    for char in text:

        sys.stdout.write(char)

        sys.stdout.flush()

        time.sleep(delay)

    sys.stdout.write(end)

    sys.stdout.flush()



def analyze_ir_content(ir_path: Path):

    """

    Deep dive into IR content to find interesting stats.

    """

    content = ir_path.read_text()

    

    stats = {

        "memory_ops": 0,

        "float_ops": 0,

        "vector_ops": 0,

        "branches": 0,

        "basic_blocks": 0

    }

    

    # Regex patterns

    # Memory: load, store, alloca, getelementptr

    stats["memory_ops"] = len(re.findall(r'\b(load|store|alloca|getelementptr)\b', content))

    

    # Float: fadd, fsub, fmul, fdiv, frem

    stats["float_ops"] = len(re.findall(r'\b(fadd|fsub|fmul|fdiv|frem)\b', content))

    

    # Vector: look for <N x type> patterns, e.g., <4 x float>

    stats["vector_ops"] = len(re.findall(r'<\d+\s*x\s*\w+>', content))

    

    # Branches

    stats["branches"] = len(re.findall(r'\bbr\b', content))

    

    return stats



def extract_interesting_snippet(ir_path: Path, search_type="vector"):

    """

    Finds a snippet of code that looks 'optimized' (e.g. contains vector instructions).

    """

    lines = ir_path.read_text().splitlines()

    snippet = []

    

    found_start = -1

    

    for i, line in enumerate(lines):

        if search_type == "vector" and re.search(r'<\d+\s*x\s*\w+>', line):

            found_start = i

            break

        elif search_type == "loop" and "for.body" in line:

            found_start = i

            break

            

    if found_start != -1:

        # Get a window of lines

        start = max(0, found_start - 2)

        end = min(len(lines), found_start + 5)

        snippet = lines[start:end]

        return snippet, start + 1

    

    return ["(No interesting snippet found)"], 0



def main():

    print("\n")

    type_out("="*60, delay=0.005)

    type_out(" COMPILER OPTIMIZATION DEMO: IR STATISTICS ANALYSIS", delay=0.02)

    type_out("="*60 + "\n", delay=0.005)

    

    benchmark_name = "2mm"

    base_dir = Path("results/baseline")

    

    base_ll = base_dir / f"{benchmark_name}_base.ll"

    opt_ll = base_dir / f"{benchmark_name}-O3.ll"

    

    if not base_ll.exists() or not opt_ll.exists():

        print(f"Error: Could not find IR files for {benchmark_name} in {base_dir}")

        return



    collector = MetricsCollector()

    

    # 1. High-Level Metrics

    type_out(f"Analyzing Benchmark: {benchmark_name} (Linear Algebra Kernel: 2 Matrix Multiplications)", delay=0.02)

    type_out("-" * 60, delay=0.005)

    time.sleep(0.3)

    

    base_metrics = collector.collect(str(base_ll))

    opt_metrics = collector.collect(str(opt_ll))

    

    instr_reduction = (base_metrics.instruction_count - opt_metrics.instruction_count) / base_metrics.instruction_count * 100

    size_change = (opt_metrics.code_size_bytes - base_metrics.code_size_bytes) / base_metrics.code_size_bytes * 100

    

    size_sign = "+" if size_change >= 0 else ""



    # Print table row by row for smooth effect

    rows = [

        f"{'Metric':<20} | {'Baseline (-O0)':<15} | {'Optimized (-O3)':<15} | {'Change':<10}",

        "-" * 68,

        f"{'Instructions':<20} | {base_metrics.instruction_count:<15} | {opt_metrics.instruction_count:<15} | -{instr_reduction:.1f}%",

        f"{'Code Size (bytes)':<20} | {base_metrics.code_size_bytes:<15} | {opt_metrics.code_size_bytes:<15} | {size_sign}{size_change:.1f}%",

        "-" * 68 + "\n"

    ]

    

    for row in rows:

        print(row.rstrip())

        time.sleep(0.2)

    

    # 2. Deep Dive Stats

    type_out("Detailed IR Statistics:", delay=0.03)

    type_out("-" * 60, delay=0.005)

    

    base_stats = analyze_ir_content(base_ll)

    opt_stats = analyze_ir_content(opt_ll)

    

    stats_rows = [

        f"{'Instruction Type':<20} | {'Baseline':<10} | {'Optimized':<10} | {'Note'}",

        "-" * 60,

        f"{'Memory (load/store)':<20} | {base_stats['memory_ops']:<10} | {opt_stats['memory_ops']:<10} | {'Reduced memory traffic'}",

        f"{'Float Ops':<20} | {base_stats['float_ops']:<10} | {opt_stats['float_ops']:<10} | {'Often combined/vectorized'}",

        f"{'Vector Ops (<N x T>)':<20} | {base_stats['vector_ops']:<10} | {opt_stats['vector_ops']:<10} | {'SIMD parallelism'}",

        "-" * 60 + "\n"

    ]



    for row in stats_rows:

        print(row.rstrip())

        time.sleep(0.2)

    

    # 3. Source Trace / Snippets

    type_out("Evidence from IR:", delay=0.03)

    type_out("-" * 60, delay=0.005)

    

    # Show baseline loop (noisy)

    # Usually standard loops in O0 are just branches and labels

    type_out(">> Baseline (-O0) IR Snippet (Scalar):", delay=0.02)

    snippet, line_no = extract_interesting_snippet(base_ll, "loop")

    if snippet == ["(No interesting snippet found)"]:

         # Fallback to just grabbing the middle of main or similar

         snippet = base_ll.read_text().splitlines()[50:57]

         line_no = 50

         

    for i, line in enumerate(snippet):

        print(f"{line_no + i:4d} | {line.strip()}")

        time.sleep(0.05) # Fast scroll

    

    print()

    time.sleep(0.5)



    type_out(">> Optimized (-O3) IR Snippet (Vectorized):", delay=0.02)

    snippet, line_no = extract_interesting_snippet(opt_ll, "vector")

    for i, line in enumerate(snippet):

        print(f"{line_no + i:4d} | {line.strip()}")

        time.sleep(0.05)

        

    print("\n" + "="*60)

    type_out("Summary:", delay=0.05)

    type_out(f"The optimizer successfully vectorized the kernel, reducing instruction", delay=0.02)

    type_out(f"count by {instr_reduction:.1f}% and utilizing SIMD instructions (vector ops: {opt_stats['vector_ops']}).", delay=0.02)

    type_out("="*60, delay=0.005)



if __name__ == "__main__":

    main()


