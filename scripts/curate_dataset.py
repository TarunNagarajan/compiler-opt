import os
import shutil
from pathlib import Path
from src.features.ir_parser import IRParser
from src.passes.pass_executor import compile_to_ir

SOURCE_DIRS = [
    Path("benchmarks/large_scale/anghaben"),
    Path("benchmarks/mibench"),
    Path("benchmarks/graphs")
]
CURATED_DIR = Path("benchmarks/curated")
CURATED_DIR.mkdir(parents=True, exist_ok=True)

MIN_BLOCKS = 5
MIN_INSTR = 30

def curate():
    count = 0
    for sdir in SOURCE_DIRS:
        print(f"Processing {sdir}...")
        for c_file in sdir.glob("*.c"):
            # 1. Compile to IR
            success, ir_path = compile_to_ir(str(c_file))
            if not success:
                continue
            
            # 2. Analyze
            try:
                parser = IRParser(ir_path)
                stats = parser.parse()
                
                # 3. Filter
                if stats.num_basic_blocks >= MIN_BLOCKS and stats.num_instructions >= MIN_INSTR:
                    target = CURATED_DIR / f"{c_file.stem}.ll"
                    shutil.move(ir_path, target)
                    count += 1
                else:
                    os.remove(ir_path) # Clean up simple files
            except Exception as e:
                if os.path.exists(ir_path): os.remove(ir_path)
                
    print(f"Curation complete. {count} complex kernels moved to {CURATED_DIR}.")

if __name__ == "__main__":
    curate()
