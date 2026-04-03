import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import glob
import random
from src.env import CompilerOptEnv
from src.models.hrl_agent import create_hrl_agent
from src.config import get_benchmark_paths, FEATURE_DIM, MODELS_DIR
from src.actions.macro_actions import MACRO_ACTIONS

def count_empirical_stops():
    benchmarks = get_benchmark_paths()
    # Pick 50 random files to form a deterministic evaluation batch
    random.seed(42)
    eval_batch = random.sample(benchmarks, min(len(benchmarks), 50))
    
    env = CompilerOptEnv(eval_batch, max_steps=1)
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    
    checkpoints = sorted(glob.glob("models/hrl_antigravity_v4_hrl_hour_*.pth"))
    
    print(f"Empirical STOP Action Count across {len(eval_batch)} different C programs:")
    print(f"{'Checkpoint':<45} | {'STOPs on Step 1':<18} | {'% Collapse'}")
    print("-" * 80)

    for ckpt in checkpoints:
        ckpt_path = Path(ckpt)
        agent.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
        agent.eval()
        
        stop_count = 0
        torch.manual_seed(42) # Ensure reproducible sampling
        
        for file_path in eval_batch:
            # We explicitly replace the target list to just one file at a time
            env.benchmark_paths = [file_path]
            obs, info = env.reset()
            graph = env.get_observation_graph()
            
            with torch.no_grad():
                x = graph.x
                edge_index = graph.edge_index
                edge_attr = getattr(graph, 'edge_attr', None)
                batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
                
                # Sample exactly how train_hrl.py does:
                m_idx = torch.distributions.Categorical(macro_probs).sample().item()
                
                if m_idx == (len(MACRO_ACTIONS) - 1): # STOP action is the last index
                    stop_count += 1
                    
        collapse_pct = (stop_count / len(eval_batch)) * 100
        print(f"{ckpt_path.name:<45} | {stop_count:<2} out of {len(eval_batch):<10} | {collapse_pct:6.2f}%")

if __name__ == "__main__":
    count_empirical_stops()
