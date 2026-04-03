import sys
import os
import subprocess
import torch
import tempfile

sys.path.append(os.getcwd())
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.features.ir_graph_extractor import extract_ir_graph
from src.config import NUM_ACTIONS, FEATURE_DIM

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{result.stderr}")
        return False
    return True

def count_instructions(ll_file):
    with open(ll_file, 'r') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith(';') and not line.startswith('!') and not line.startswith('}'):
            if '=' in line or 'call' in line or 'br' in line or 'ret' in line or 'store' in line:
                count += 1
    return count

def main():
    print("--- FINAL ZERO SHOT GENERALIZATION PROOF (PREPARED CODE) ---")
    
    device = torch.device('cpu')
    base_model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    ckpt = torch.load("models/world_model.5_best.pth", map_location=device)
    base_model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    base_model.eval()
    
    model = CalibratedWorldModel(base_model, meta_calibrator_path="models/meta_calibrator_best.pth")
    model.eval()
    
    print("1. Compiling custom_benchmark.c...")
    run_cmd(["clang", "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-S", "custom_benchmark.c", "-o", "custom_final.ll"])
    
    print("2. Running Canonicalization (mem2reg, simplifycfg, loop-rotate, loop-simplify)...")
    run_cmd(["opt", "-S", "-passes=mem2reg,simplifycfg,loop-rotate,loop-simplify", "custom_final.ll", "-o", "prepared_final.ll"])
    
    baseline_inst = count_instructions("prepared_final.ll")
    print(f"\nBaseline Instructions (Prepared): {baseline_inst}")
    print("-" * 65)
    print(f"{'Action':<15} | {'V8.5 Predicted Δ (%)':<20} | {'True LLVM Δ (%)':<20}")
    print("-" * 65)

    graph_data = extract_ir_graph("prepared_final.ll").to(device)
    
    with torch.no_grad():
        state_emb = model.encode_graph(graph_data)

    actions = [
        ("Unroll", 61, "function(loop-unroll)"),
        ("SROA", 54, "function(sroa)"),
        ("SimplifyCFG", 51, "function(simplifycfg)"),
        ("Inline", 34, "inline"),
        ("InstCombine", 41, "function(instcombine)")
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for action_name, action_idx, llvm_flag in actions:
            action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
            action_onehot[0, action_idx] = 1.0
            
            with torch.no_grad():
                _, predicted_metrics = model(state_emb, action_onehot, graph_data=graph_data)
                # The Meta-Calibrator already outputs index 0 (Instructions) as a percentage based on its training distribution
                pred_pct = predicted_metrics[0, 0].item()
                
            out_ir = os.path.join(temp_dir, f"out_{action_name}.ll")
            run_cmd(["opt", "-S", f"-passes={llvm_flag}", "prepared_final.ll", "-o", out_ir])
            
            actual_inst = count_instructions(out_ir)
            actual_pct = ((actual_inst - baseline_inst) / max(baseline_inst, 1)) * 100.0
            
            print(f"{action_name:<15} | {pred_pct:>19.2f}% | {actual_pct:>19.2f}%")

if __name__ == "__main__":
    main()
