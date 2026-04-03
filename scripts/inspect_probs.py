import torch
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.hrl_agent import create_hrl_agent
from src.env import CompilerOptEnv
from src.config import FEATURE_DIM, MACRO_ACTIONS

def inspect_ckpt(ckpt_path, wm_path):
    print(f"\n[INSPECT] {Path(ckpt_path).name}")
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), wm_path, gnn_layers=6)
    agent.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
    agent.eval()
    
    # Just use any benchmark for a single forward pass
    from src.config import get_benchmark_paths
    bench = get_benchmark_paths()[0]
    env = CompilerOptEnv([bench])
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
    with torch.no_grad():
        macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
        macro_probs = macro_probs.squeeze().tolist()
        
    for i, p in enumerate(macro_probs):
        name = MACRO_ACTIONS[i][0]
        print(f"  [{i:2d}] {name:<40} : {p:.6f}")

if __name__ == "__main__":
    wm = "models/world_model_antigravity_v4_L6_checkpoint.pth"
    inspect_ckpt(sys.argv[1], wm)
