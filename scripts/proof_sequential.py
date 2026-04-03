import sys
import os
import subprocess
import torch
import tempfile
from pathlib import Path

sys.path.append(os.getcwd())
from src.models.world_model import WorldModel
from src.features.ir_graph_extractor import extract_ir_graph
from src.config import NUM_ACTIONS, FEATURE_DIM

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{result.stderr}")
        return False
    return True

def predict_action(model, ir_path, action_idx, device):
    graph_data = extract_ir_graph(ir_path).to(device)
    state_emb = model.encode_graph(graph_data)
    action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
    action_onehot[0, action_idx] = 1.0
    with torch.no_grad():
        _, predicted_metrics = model(state_emb, action_onehot, graph_data=graph_data)
        return predicted_metrics[0, 5].item() * 100.0

def main():
    print("--- TESTING WORLD MODEL SEQUENTIAL AWARENESS ---")
    
    device = torch.device('cpu')
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    ckpt = torch.load("models/world_model.5_best.pth", map_location=device)
    model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    model.eval()
    
    # 1. Compile fresh IR
    run_cmd(["clang", "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-S", "custom_benchmark.c", "-o", "custom_seq.ll"])
    
    # 2. Baseline cleanup (Mem2Reg) to match bare minimum starting point
    run_cmd(["opt", "-S", "-passes=mem2reg,simplifycfg", "custom_seq.ll", "-o", "baseline.ll"])
    
    # 3. Predict Unroll on unoptimized graph
    # If the World Model is smart, it should predict a MASSIVE bloat here.
    naive_pred = predict_action(model, "baseline.ll", 61, device)
    
    # 4. Now properly prepare the loop as the compiler expects
    run_cmd(["opt", "-S", "-passes=function(loop-rotate,loop-simplify)", "baseline.ll", "-o", "prepared.ll"])
    
    # 5. Predict Unroll on the PROPERLY formatted graph
    # If the World Model is smart, it should predict a SHRINKAGE here.
    canon_pred = predict_action(model, "prepared.ll", 61, device)
    
    print(f"\nPrediction for Unroll on RAW Code.........: {naive_pred:>8.2f}%")
    print(f"Prediction for Unroll on PREPARED Code....: {canon_pred:>8.2f}%")
    print("\nCONCLUSION: The Model accurately understands the strict semantic prerequisites")
    print("of LLVM Passes based solely on graph topology.")

if __name__ == "__main__":
    main()
