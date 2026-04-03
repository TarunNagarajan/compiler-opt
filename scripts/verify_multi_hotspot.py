import sys
from pathlib import Path
import torch

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv
from src.features.ir_graph_extractor_v5 import IRGraphExtractorV5

def verify_multi_hotspot():
    print("=== Multi-Hotspot Scale Verification ===")
    
    # Path to a known large benchmark
    benchmark_path = Path("benchmarks/large_scale/lz4/lz4.c")
    if not benchmark_path.exists():
        print(f"Error: {benchmark_path} not found. Please ensure benchmarks are populated.")
        return

    env = CompilerOptEnv(benchmark_paths=[benchmark_path])
    
    # Trigger reset with the large file
    print(f"Resetting environment with {benchmark_path}...")
    obs, info = env.reset(options={"ir_path": str(benchmark_path)})
    
    # Check selected functions
    focus_funcs = getattr(env, 'focus_functions', None)
    if not focus_funcs:
        print("FAILED: No focus functions selected for large file.")
        return
    
    print(f"SUCCESS: Selected {len(focus_funcs)} focus functions: {focus_funcs}")
    
    if len(focus_funcs) <= 1:
        print("WARNING: Only 1 hotspot selected. Check if file is small or budget is too tight.")
    else:
        print("SUCCESS: Multi-Hotspot logic triggered correctly.")

    # Verify Graph Connectivity
    graph_data = env.get_observation_graph()
    num_nodes = graph_data.x.size(0)
    num_edges = graph_data.edge_index.size(1)
    
    print(f"Graph Data: {num_nodes} nodes, {num_edges} edges")
    
    # Check if we have call edges or loop edges
    edge_types = graph_data.edge_attr
    num_calls = (edge_types == 5).sum().item()
    num_loops = (edge_types == 6).sum().item()
    
    print(f"  - Call Edges: {num_calls}")
    print(f"  - Loop Back-Edges: {num_loops}")
    
    if num_nodes > 1:
        print("=== VERIFICATION PASSED ===")
    else:
        print("=== VERIFICATION FAILED: Empty Graph ===")

if __name__ == "__main__":
    verify_multi_hotspot()
