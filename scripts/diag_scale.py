import torch
import sys
import os

sys.path.append(os.getcwd())
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.features.ir_graph_extractor import extract_ir_graph
from src.config import NUM_ACTIONS, FEATURE_DIM

def main():
    device = torch.device('cpu')
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    ckpt = torch.load("models/world_model.5_best.pth", map_location=device)
    base_model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    base_model.eval()
    
    cal_model = CalibratedWorldModel(base_model, meta_calibrator_path="models/meta_calibrator_best.pth")
    cal_model.eval()
    
    # We'll use the prepared IR we just made
    ir_path = "prepared_final.ll"
    if not os.path.exists(ir_path):
        print(f"Error: {ir_path} not found. Run prove_generalization_prepared.py first.")
        return

    graph_data = extract_ir_graph(ir_path).to(device)
    state_emb = base_model.encode_graph(graph_data)
    
    # Test Action 41 (InstCombine) - It gave -1165.36%
    action_idx = 41 
    action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
    action_onehot[0, action_idx] = 1.0
    
    print(f"--- DIAGNOSTIC: Action {action_idx} (InstCombine) ---")
    
    with torch.no_grad():
        # 1. Base Model Output
        _, base_metrics = base_model(state_emb, action_onehot, graph_data=graph_data)
        print(f"Base Model Output (inst): {base_metrics[0, 5].item():.4f}")
        
        # 2. Calibrated Model Output
        _, cal_metrics = cal_model(state_emb, action_onehot, graph_data=graph_data)
        print(f"Calibrated Output (inst): {cal_metrics[0, 0].item():.4f}")
        
    # Check MetaCalibrator weights
    if cal_model.meta_net:
        print(f"MetaNet Learned Scale (inst): {cal_model.meta_net.learned_scale[0].item():.4f}")

if __name__ == "__main__":
    main()
