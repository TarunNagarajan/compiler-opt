import sys
from pathlib import Path
import random

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.env.compiler_env import CompilerOptEnv, RewardMode

def verify_windowing():
    sqlite_path = Path("benchmarks/large_scale/sqlite/sqlite3.c")
    if not sqlite_path.exists():
        print(f"File not found: {sqlite_path}")
        return

    print(f"Testing Selective Windowing on {sqlite_path}...")
    
    # Initialize environment with just SQLite
    env = CompilerOptEnv(
        benchmark_paths=[str(sqlite_path)],
        reward_mode=RewardMode.SIZE
    )
    
    # Reset should trigger Selective Windowing
    obs, info = env.reset()
    
    # Check if focus_function was set
    focus = getattr(env, 'focus_function', None)
    print(f"Focus Function: {focus}")
    
    # Check observation graph scale
    graph = env.get_observation_graph()
    if graph:
        print(f"Sub-graph Statistics:")
        print(f"  Nodes: {graph.x.shape[0]}")
        print(f"  Edges: {graph.edge_index.shape[1]}")
        
        # Verify Node 0 has module features
        node0_feat = graph.x[0, :4]
        print(f"  Node 0 Module Feats: {node0_feat.tolist()}")
    else:
        print("Failed to get observation graph.")

    env.close()

if __name__ == "__main__":
    verify_windowing()
