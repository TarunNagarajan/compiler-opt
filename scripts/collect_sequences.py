
import os
import sys
import argparse
import random
import time
import json
import subprocess
from pathlib import Path
import csv
from multiprocessing import Pool, cpu_count
from typing import List, Dict, Any, Tuple
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import BENCHMARKS_DIR, POLYBENCH_CATEGORIES, LLVM_PASSES, LLVM_BIN_DIR, get_benchmark_paths
from src.features.feature_vector import extract_features
from src.passes.pass_executor import PassExecutor
from src.passes.metrics import MetricsCollector

# Configure output directory
DATASET_DIR = Path(__file__).parent.parent / "dataset"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

def get_benchmarks(categories: List[str] = None) -> List[Path]:
    """Get list of benchmark .c files to process"""
    return get_benchmark_paths(categories)

def compile_to_ir(source_file: Path, output_path: Path) -> bool:
    """
    Compile C source to unoptimized LLVM IR. 
    Lazy-links dependencies ONLY if undefined symbols are found.
    """
    # Choose compiler based on file type
    from src.config import CLANG_CXX, CLANG, LLVM_LINK, LLVM_DIS, LLVM_NM
    compiler = CLANG
    if source_file.suffix == ".cpp" or ".cpp.wrapped." in source_file.name:
        compiler = CLANG_CXX

    # Whitelist of common standard library functions that don't need linking
    STD_LIBS = {
        "printf", "scanf", "malloc", "free", "exit", "atoi", "atol", "rand", "srand",
        "time", "clock", "cos", "sin", "sqrt", "pow", "puts", "fprintf", "stderr", 
        "stdout", "fopen", "fclose", "fscanf", "sscanf", "memset", "memcpy", "memmove", 
        "strlen", "strcmp", "strncmp", "abs", "floor", "ceil", "exp", "log", "log10",
        "fflush", "tolower", "toupper", "isspace", "isdigit", "isalpha",
        # Windows/MinGW/C++ ABI symbols that don't need linking
        "__mingw_printf", "__mingw_fprintf", "__mingw_vfprintf", "__mingw_sprintf",
        "__imp___acrt_iob_func", "__imp__iob", "mainCRTStartup", "__main",
        "__gxx_personality_seh0", "__cxa_begin_catch", "__cxa_end_catch", 
        "_ZSt9terminatev", "_ZSt25__throw_bad_function_callv",
        "_ZTVN10__cxxabiv117__class_type_infoE", "_ZTVN10__cxxabiv120__si_class_type_infoE"
    }

    # 1. First, try to compile the target file only to IR (fast path)
    cmd = [
        str(compiler),
        "-S", "-emit-llvm",
        "-O0", "-Xclang", "-disable-O0-optnone",
        "-Wno-everything",
        "-I", str(source_file.parent),
        "-lm",
        str(source_file),
        "-o", str(output_path)
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            return False
            
        # 2. Check for undefined symbols
        import uuid
        temp_id = uuid.uuid4().hex[:8]
        temp_bc = output_path.with_suffix(f".{temp_id}_check.bc")
        
        # We need bitcode for llvm-nm to be reliable
        bc_cmd = [
            str(compiler), "-c", "-emit-llvm",
            "-Wno-everything", "-I", str(source_file.parent),
            str(source_file), "-o", str(temp_bc)
        ]
        subprocess.run(bc_cmd, capture_output=True)
        
        if not temp_bc.exists():
            return True # Fallback to whatever IR we got
            
        nm_res = subprocess.run([str(LLVM_NM), str(temp_bc)], capture_output=True, text=True)
        if temp_bc.exists(): temp_bc.unlink()
        
        undefined_symbols = []
        for line in nm_res.stdout.splitlines():
            if " U " in line:
                parts = line.split(" U ")
                sym = parts[1].strip() if len(parts) > 1 else ""
                if sym and not sym.startswith("llvm.") and sym not in STD_LIBS:
                    undefined_symbols.append(sym)
        
        if not undefined_symbols:
            return True # Self-contained!
            
        # 3. Slow path: scan directory for helpers
        # SKIP if in a 'generated' directory (redundant for these standalone tests)
        if "generated" in str(source_file.parent).lower():
            return True
            
        source_dir = source_file.parent
        c_files = list(source_dir.glob("*.c")) + list(source_dir.glob("*.cpp"))
        helper_bcs = []
        
        target_bc = output_path.with_suffix(f".{temp_id}_target.bc")
        shutil_cmd = [str(compiler), "-c", "-emit-llvm", "-O0", "-Xclang", "-disable-O0-optnone", "-Wno-everything", "-I", str(source_dir), str(source_file), "-o", str(target_bc)]
        subprocess.run(shutil_cmd, capture_output=True)
        helper_bcs.append(target_bc)

        for c_file in c_files:
            if c_file.name == source_file.name: continue
            
            helper_bc = output_path.with_suffix(f".{temp_id}_{c_file.stem}.bc")
            h_compiler = CLANG_CXX if (c_file.suffix == ".cpp" or ".cpp.wrapped." in c_file.name) else CLANG
            h_cmd = [
                str(h_compiler), "-c", "-emit-llvm",
                "-O0", "-Xclang", "-disable-O0-optnone",
                "-Wno-everything", "-I", str(source_dir),
                str(c_file), "-o", str(helper_bc)
            ]
            subprocess.run(h_cmd, capture_output=True)
            if helper_bc.exists():
                helper_bcs.append(helper_bc)
        
        # 4. Link them (using response file for Windows command limit)
        response_file = output_path.with_suffix(f".{temp_id}_args.txt")
        with open(response_file, "w") as f:
            for p in helper_bcs:
                f.write(str(p).replace("\\", "/") + "\n")
                
        link_cmd = [str(LLVM_LINK), f"@{response_file}", "-S", "-o", str(output_path)]
        subprocess.run(link_cmd, capture_output=True)
        
        # Cleanup
        if response_file.exists(): response_file.unlink()
        for p in helper_bcs:
            if p.exists(): p.unlink()
            
        return output_path.exists()
        
    except Exception as e:
        print(f"[ERROR] Compilation error for {source_file}: {e}")
        return False

def process_benchmark(args) -> List[Dict[str, Any]]:
    """Process a single benchmark with multiple random sequences"""
    benchmark_path, sequences, category = args
    
    results = []
    executor = None
    ir_file = None
    
    try:
        executor = PassExecutor()
        metrics = MetricsCollector()
        
        # 1. Compile to base IR ONCE for all sequences
        ir_file = executor.work_dir / f"{benchmark_path.stem}_base.ll"
        if not compile_to_ir(benchmark_path, ir_file):
             return [{"benchmark": benchmark_path.stem, "error": "Compilation failed"}]
        
        # 2. Extract features ONCE
        features = extract_features(ir_file)
        base_inst = metrics.count_instructions(ir_file)
        base_size = metrics.get_code_size(ir_file)
        
        if base_inst == 0:
            return [{"benchmark": benchmark_path.stem, "error": "Zero instructions in base IR"}]

        # 3. Evaluate each sequence
        for seq_id, sequence in enumerate(sequences):
            safe_seq_name = f"seq_{seq_id}"
            output_ir = executor.work_dir / f"{benchmark_path.stem}_{safe_seq_name}.ll"
            
            start_time = time.time()
            pass_args = sequence
            if not (len(sequence) == 1 and sequence[0].startswith("default<")):
                pipeline = f"module({','.join(sequence)})"
                pass_args = [pipeline]

            pass_result = executor.apply_passes(str(ir_file), pass_args, str(output_ir))
            compile_time = time.time() - start_time
            
            if pass_result.success:
                optimized_ir = Path(pass_result.output_path)
                opt_inst = metrics.count_instructions(optimized_ir)
                opt_size = metrics.get_code_size(optimized_ir)
                
                inst_reduction = (base_inst - opt_inst) / base_inst
                size_reduction = (base_size - opt_size) / base_size if base_size > 0 else 0
                
                results.append({
                    "benchmark": benchmark_path.stem,
                    "category": category,
                    "sequence_id": seq_id,
                    "passes": sequence,
                    "pass_count": len(sequence),
                    "features": features.tolist(),
                    "metrics": {
                        "base_inst": base_inst,
                        "opt_inst": opt_inst,
                        "inst_reduction": inst_reduction,
                        "base_size": base_size,
                        "opt_size": opt_size,
                        "size_reduction": size_reduction,
                        "compile_time": compile_time
                    }
                })
                
                # Cleanup opt IR immediately to save space
                if optimized_ir.exists(): optimized_ir.unlink()
            else:
                results.append({
                    "benchmark": benchmark_path.stem,
                    "category": category,
                    "sequence_id": seq_id,
                    "error": f"Pass failed: {pass_result.error_message}"
                })
                
        return results
    except Exception as e:
        return [{"benchmark": benchmark_path.stem, "error": str(e)}]
    finally:
        if ir_file and ir_file.exists(): ir_file.unlink()
        if executor: executor.cleanup()

def generate_random_sequences(num_sequences: int, min_len: int = 5, max_len: int = 20) -> List[List[str]]:
    """Generate a list of random pass sequences"""
    sequences = []
    
    # Add standard sequences as baseline
    sequences.append(["default<O1>"])
    sequences.append(["default<O2>"]) 
    sequences.append(["default<Os>"])
    sequences.append(["default<O3>"])
    
    # Add random sequences
    for _ in range(num_sequences):
        length = random.randint(min_len, max_len)
        seq = [random.choice(LLVM_PASSES) for _ in range(length)]
        sequences.append(seq)
        
    return sequences

def main():
    parser = argparse.ArgumentParser(description="Collect optimization sequence dataset")
    parser.add_argument("--samples", type=int, default=100, help="Number of random sequences per benchmark")
    parser.add_argument("--categories", nargs="+", help="Specific benchmark categories to run")
    parser.add_argument("--limit-benchmarks", type=int, default=0, help="Limit to a random subset of N benchmarks")
    parser.add_argument("--output", type=str, default="optimization_dataset.json", help="Output JSON file name")
    parser.add_argument("--workers", type=int, default=max(1, cpu_count() - 2), help="Number of parallel workers")
    
    args = parser.parse_args()
    
    print(f"Loading benchmarks...")
    benchmarks = get_benchmarks(args.categories)
    if not benchmarks:
        print("No benchmarks found!")
        return
        
    if args.limit_benchmarks > 0 and args.limit_benchmarks < len(benchmarks):
        print(f"Limiting to a random sample of {args.limit_benchmarks} benchmarks.")
        benchmarks = random.sample(benchmarks, args.limit_benchmarks)

    print(f"Found {len(benchmarks)} benchmarks. Grouping into batches of {args.samples} sequences...")
    
    # Prepare work items (one item per benchmark)
    work_items = []
    for bench in benchmarks:
        category = bench.parent.name
        sequences = generate_random_sequences(args.samples)
        work_items.append((bench, sequences, category))
            
    print(f"Starting collection for {len(benchmarks) * (args.samples + 4)} total evaluations using {args.workers} workers...")
    
    # Timestamp for unique filenames
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create logs directory
    Path("logs").mkdir(parents=True, exist_ok=True)
    csv_filename = Path("logs") / f"optimization_log_{timestamp}.csv"
    
    # Initialize CSV logging
    csv_file = open(csv_filename, "w", newline="")
    fieldnames = ["benchmark", "category", "sequence_id", "pass_count", "inst_reduction", "size_reduction", "compile_time", "passes"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    print(f"Logging to: {csv_filename}")
    
    all_results = []
    benchmarks_processed = 0
    total_evals = 0
    
    with Pool(processes=args.workers) as pool:
        try:
            for bench_results in pool.imap_unordered(process_benchmark, work_items):
                bench_name = bench_results[0].get("benchmark", "unknown")
                
                success_count = 0
                for res in bench_results:
                    if "error" in res:
                        print(f"FAIL: {bench_name} (Seq {res.get('sequence_id', '?')}): {res['error']}")
                        continue
                    
                    success_count += 1
                    all_results.append(res)
                    
                    # Log to CSV
                    writer.writerow({
                        "benchmark": res['benchmark'],
                        "category": res['category'],
                        "sequence_id": res['sequence_id'],
                        "pass_count": res['pass_count'],
                        "inst_reduction": res['metrics']['inst_reduction'],
                        "size_reduction": res['metrics']['size_reduction'],
                        "compile_time": res['metrics']['compile_time'],
                        "passes": ";".join(res['passes'])
                    })
                
                csv_file.flush()
                benchmarks_processed += 1
                total_evals += len(bench_results)
                
                if benchmarks_processed % 5 == 0:
                    avg_reduction = np.mean([r['metrics']['inst_reduction'] for r in bench_results if 'metrics' in r]) * 100 if success_count > 0 else 0
                    print(f"OK:   {bench_name} ({success_count} seqs). Avg Reduction: {avg_reduction:.2f}%")
                    print(f"--- Progress: {benchmarks_processed}/{len(benchmarks)} benchmarks ({total_evals} evals) ---")
                    
        except KeyboardInterrupt:
            print("\n! Interrupted by user! Saving partial results...")
        finally:
            csv_file.close()

    duration = time.time() - start_global if 'start_global' in locals() else 0
    print(f"\nCollection finished. Data points: {len(all_results)}")
    
    # Append timestamp to output filename
    base_name = Path(args.output).stem
    output_filename = f"{base_name}_{timestamp}.json"
    output_path = DATASET_DIR / output_filename
    
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
        
    print(f"Dataset saved to: {output_path}")

if __name__ == "__main__":
    start_global = time.time()
    main()
