import sys
import torch
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.world_model_v5 import WorldModelV5
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS

def test_world_model_fidelity():
    print("=== WORLD MODEL FIDELITY TEST ===")
    
    # 1. Load Model
    # The checkpoint was trained with input_dim=44 and num_relations=7
    wm = WorldModelV5(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6, gnn_input_dim=44, num_relations=7)
    checkpoint = torch.load("models/world_model_v5.pth", weights_only=False)
    wm.load_state_dict(checkpoint['model_state_dict'])
    wm.eval()
    
    # 2. Setup Env
    # 2. Setup Env with a guaranteed fast, lightweight file
    test_file = Path("test_ood.c").resolve()
    env = CompilerOptEnv([test_file], max_steps=5)
    
    samples = 3
    total_error_pct = 0
    
    for i in range(samples):
        obs, info = env.reset(options={"ir_path": str(test_file)})
        graph = env.get_observation_graph()
        if graph is None: continue
        
        # Pick a simple atomic action (e.g., GVN)
        action_idx = 11 # gvn
        
        with torch.no_grad():
            batch_vec = torch.zeros(graph.x.size(0), dtype=torch.long)
            
            action_onehot = torch.zeros(1, NUM_ACTIONS)
            action_onehot[0, action_idx] = 1.0
            
            # The checkpoint expects 44-dim input, but the extractor generates 46-dim.
            # Truncate the feature dimension before passing to the model.
            graph.x = graph.x[:, :44]
            
            # The checkpoint only has 7 relations (0-6), but the new extractor generates up to 10 (0-9).
            # Filter out edges with relation type >= 7 to prevent out-of-bounds indexing.
            if graph.edge_attr is not None:
                valid_edges = graph.edge_attr < 7
                graph.edge_index = graph.edge_index[:, valid_edges]
                graph.edge_attr = graph.edge_attr[valid_edges]
            
            _, metrics_pred = wm(None, action_onehot, graph_data=graph)
        
        # Predicted instruction delta (%)
        pred_instr_delta = metrics_pred[0, 0].item()
        
        # Real execution
        obs_next, reward, term, trunc, info_next = env.step(action_idx)
        real_instr_before = info_next['instructions_before']
        real_instr_after = info_next['instructions_after']
        real_instr_delta = (real_instr_before - real_instr_after) / max(real_instr_before, 1)
        
        error = abs(pred_instr_delta - real_instr_delta)
        total_error_pct += error
        
        print(f"Sample {i+1}:")
        print(f"  Predicted Instr Delta: {pred_instr_delta*100:.2f}%")
        print(f"  Real Instr Delta:      {real_instr_delta*100:.2f}%")
        print(f"  Model Error:           {error*100:.2f}%")

    avg_error = (total_error_pct / samples) * 100
    print(f"\n[SUMMARY] Average Prediction Error: {avg_error:.2f}%")
    if avg_error < 5.0:
        print(">>> RESULT: World Model is HIGH FIDELITY. Backtracking is viable!")
    else:
        print(">>> RESULT: World Model accuracy is too low for MCTS.")

if __name__ == "__main__":
    test_world_model_fidelity()
