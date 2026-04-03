import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.features import extract_ir_graph

def analyze_large_scale():
    sqlite_path = "benchmarks/large_scale/sqlite/sqlite3.c"
    print(f"Analyzing {sqlite_path}...")
    
    # Compile to IR first if needed (should already be there from previous steps, but let's be safe)
    from src.passes.pass_executor import compile_to_ir
    ir_path = "benchmarks/large_scale/sqlite/sqlite3.ll"
    success, actual_ir_path = compile_to_ir(sqlite_path, output_path=ir_path)
    
    if not success:
        print(f"Failed to compile: {actual_ir_path}")
        return

    # Extract Graph
    print("Extracting Graph (this may take a minute for 9MB of C)...")
    data = extract_ir_graph(actual_ir_path)
    
    print(f"\nGraph Statistics for SQLite:")
    print(f"  Number of Nodes: {data.x.shape[0]}")
    print(f"  Number of Edges: {data.edge_index.shape[1]}")
    print(f"  Node Feature Dim: {data.x.shape[1]}")
    
    # Break down by node types if available in features
    # (Assuming node type is the first few bits of x)
    # This is a bit speculative without seeing the feature mapping, 
    # but basic count is what was asked.

if __name__ == "__main__":
    analyze_large_scale()
