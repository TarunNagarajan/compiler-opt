
import os
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
# Import relative to script location
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.passes.pass_executor import compile_to_ir

BENCH_DIR = Path("benchmarks/large_scale/anghaben")

# Common missing headers based on function usage
HEADER_MAP = {
    'printf': '<stdio.h>',
    'malloc': '<stdlib.h>',
    'free': '<stdlib.h>',
    'sqrt': '<math.h>',
    'pow': '<math.h>',
    'log': '<math.h>',
    'fabs': '<math.h>',
    'sin': '<math.h>',
    'cos': '<math.h>',
    'clock': '<time.h>',
    'time': '<time.h>',
    'strlen': '<string.h>',
    'strcpy': '<string.h>',
    'memset': '<string.h>',
    'memcpy': '<string.h>',
    'INT_MAX': '<limits.h>',
    'bool': '<stdbool.h>',
}

def analyze_and_fix(file_path):
    """
    Attempts to fix a C file by:
    1. Uncommenting structs/typedefs if they look like LeetCode boilerplate.
    2. Adding missing headers.
    3. Adding a dummy main function if missing.
    """
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        original_content = content
        
        # Strategy 1: Uncomment LeetCode struct definitions
        # Pattern: /** ... struct TreeNode { ... }; ... */
        # We look for commented out struct defs
        
        # Simple heuristic: If we see "struct X {" inside a comment block, unlikely to be correct C.
        # But LeetCode often puts the definition in a comment block at the top.
        
        # Let's look for known Leetcode patterns like:
        # /**
        #  * Definition for a binary tree node.
        #  * struct TreeNode {
        #  *     int val;
        #  *     struct TreeNode *left;
        #  *     struct TreeNode *right;
        #  * };
        #  */
        
        # Implementation: Remove the " * " prefix and the surrounding /* */ if it contains "struct"
        # This is risky regex, but let's try a safer approach:
        # Identify block comments containing "struct"
        
        struct_matches = list(re.finditer(r'/\*.*?(struct\s+\w+\s*\{.*?\};).*?\*/', content, re.DOTALL))
        for m in struct_matches:
            # Check if it looks like a definition
            if "Definition for" in m.group(0) or "struct" in m.group(1):
                # Extract the inner part, strip " * " leaders
                inner = m.group(0)
                # Remove comment markers
                inner = re.sub(r'^/\*', '', inner)
                inner = re.sub(r'\*/$', '', inner)
                # Remove * prefixes on each line
                inner = re.sub(r'^\s*\*\s?', '', inner, flags=re.MULTILINE)
                
                # Replace the original comment with the uncommented code
                content = content.replace(m.group(0), inner)

        # Strategy 2: Add missing headers
        headers_to_add = set()
        for func, header in HEADER_MAP.items():
            if re.search(r'\b' + func + r'\b', content) and header not in content:
                headers_to_add.add(header)
                
        if headers_to_add:
            header_block = "\n".join([f"#include {h}" for h in headers_to_add])
            content = header_block + "\n" + content

        # Strategy 3: Add main if missing
        if not re.search(r'\bint\s+main\s*\(', content):
            # We need to call the functions to prevent them from being optimized away?
            # Actually, just having them defined is often enough for module compilation (-S -emit-llvm)
            # But the linker might complain if we tried to build an executable.
            # Our `compile_to_ir` uses `clang -S` which compiles to assembly/IR (module level),
            # so `main` IS NOT REQUIRED for intermediate representation!
            # The previous failures might not be due to missing main, but effectively just syntax errors.
            pass

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
            
        return False
    except Exception as e:
        print(f"Error repairing {file_path}: {e}")
        return False

def attempt_recover():
    # 1. Re-acquire the files first (since we deleted them)
    # We can rely on the user running acquire_anghaben.py again, or just call it?
    # Let's assume the user wants us to fix the ones we JUST deleted. 
    # But they are deleted. We need to re-download.
    print("Re-downloading datasets to recover deleted files...")
    import subprocess
    subprocess.run(["uv", "run", "python", "scripts/acquire_anghaben.py"], check=True)
    
    files = list(BENCH_DIR.rglob("*.c"))
    print(f"Scanning {len(files)} files for repairs...")
    
    # Identify broken ones again
    initial_broken = []
    
    for f in files:
         success, _ = compile_to_ir(str(f), output_path=None)
         if not success:
             initial_broken.append(f)
             
    print(f"Found {len(initial_broken)} initially broken files. Attempting repairs...")
    
    repaired_count = 0
    
    for f in initial_broken:
        modified = analyze_and_fix(f)
        if modified:
            # Try compiling again
            success, _ = compile_to_ir(str(f), output_path=None)
            if success:
                print(f"SUCCESS: Repaired {f.name}")
                repaired_count += 1
            else:
                # Still broken, delete
                # print(f"FAILED: Could not repair {f.name} even after modifications.")
                os.remove(f)
        else:
            # No fix available, delete
            os.remove(f)
            
    print(f"Repair Complete.")
    print(f"Recovered: {repaired_count}/{len(initial_broken)}")
    print(f"Total Valid: {len(files) - len(initial_broken) + repaired_count}")

if __name__ == "__main__":
    attempt_recover()
