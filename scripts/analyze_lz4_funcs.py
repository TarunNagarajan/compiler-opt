import sys
from pathlib import Path
import os

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.features.ir_parser import IRParser

def analyze_lz4():
    # We need to compile it to IR first if it's not already there
    from src.passes.pass_executor import compile_to_ir
    source_path = "benchmarks/large_scale/lz4/lz4.c"
    ir_path = "lz4_analyze.ll"
    
    print(f"Compiling {source_path} to IR...")
    success, out_path = compile_to_ir(source_path, output_path=ir_path)
    if not success:
        print("Compilation failed.")
        return

    parser = IRParser(ir_path)
    stats = parser.parse()
    
    print(f"Total Functions: {len(stats.functions)}")
    
    funcs = []
    for f in stats.functions:
        funcs.append({
            'name': f,
            'blocks': stats.function_details.get(f, {}).get('blocks', 0),
            'instrs': stats.function_details.get(f, {}).get('instructions', 0)
        })
    
    # Sort by blocks
    funcs.sort(key=lambda x: x['blocks'], reverse=True)
    
    print("\nTop 10 Functions by Block Count:")
    for f in funcs[:10]:
        print(f"  {f['name']}: {f['blocks']} blocks, {f['instrs']} instructions")

if __name__ == "__main__":
    analyze_lz4()
