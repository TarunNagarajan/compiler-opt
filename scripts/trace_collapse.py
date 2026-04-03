import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import glob
import numpy as np
from src.env import CompilerOptEnv
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MODELS_DIR
from src.actions.macro_actions import MACRO_ACTIONS

def trace_collapse():
    env = CompilerOptEnv(["test_ood_loop.c"], max_steps=1)
    env.reset()
    graph = env.get_observation_graph()

    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    
    checkpoints = sorted(glob.glob("models/hrl_antigravity_v4_hrl_hour_*.pth"))
    
    print(f"Tracing STOP probability across {len(checkpoints)} checkpoints for test_ood_loop.c:\n")
    print(f"{'Checkpoint':<45} | {'STOP Prob':<10} | {'Top Action':<15} | {'Top Prob':<10}")
    print("-" * 88)

    for ckpt in checkpoints:
        ckpt_path = Path(ckpt)
        agent.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
        agent.eval()
        
        with torch.no_grad():
            x = graph.x
            edge_index = graph.edge_index
            edge_attr = getattr(graph, 'edge_attr', None)
            batch_vec = torch.zeros(x.size(0), dtype=torch.long)
            
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            probs = macro_probs[0].numpy()
            
            stop_prob = probs[15]
            
            # Find top action (excluding STOP for a moment to see what else it wanted)
            top_idx = -1
            top_p = -1
            top_overall = np.argmax(probs)
            
            top_overall_idx = np.argsort(probs)[-1]
            if top_overall_idx == 15:
                top_2_idx = np.argsort(probs)[-2]
                top_action_name = MACRO_ACTIONS[top_2_idx][0]
                top_2_prob = probs[top_2_idx]
            else:
                top_action_name = MACRO_ACTIONS[top_overall_idx][0]
                top_2_prob = probs[top_overall_idx]

            
            print(f"{ckpt_path.name:<45} | {stop_prob*100:6.2f}%    | {MACRO_ACTIONS[top_overall_idx][0]:<15} | {probs[top_overall_idx]*100:6.2f}%")

if __name__ == "__main__":
    trace_collapse()
