import sys
import os
import subprocess
import torch
import shutil
import tempfile
from pathlib import Path

# Add project root to path so we can import src
sys.path.append(os.getcwd())

from src.models.world_model import WorldModel
from src.features.ir_graph_extractor import extract_ir_graph
from src.config import NUM_ACTIONS, FEATURE_DIM

def run_cmd(cmd):
    # Runs a command and returns True if successful
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {result.stderr}")
        return False
    return True

def count_instructions(ll_file):
    # Counts the number of non-comment, non-metadata lines (approximate instruction count)
    with open(ll_file, 'r') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith(';') and not line.startswith('!') and not line.startswith('}'):
            # Only count actual basic block instructions (ones indented)
            if '=' in line or 'call' in line or 'br' in line or 'ret' in line or 'store' in line:
                count += 1
    return count

def main():
    print("\n--- ZERO SHOT GENERALIZATION PROOF ---")
    print("This script bypasses the entire RL environment to run raw LLVM `opt` against")
    print("the raw neural network on a 100% unseen C file (custom_benchmark.c).")
    
    device = torch.device('cpu')
    print(f"\n1. Loading Base World Model V8.5...")
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    ckpt = torch.load("models/world_model.5_best.pth", map_location=device)
    model.load_state_dict(ckpt.get('model_state_dict', ckpt))
    model.eval()
    
    # Recompile clean IR
    print("2. Compiling custom_benchmark.c to clean LLVM IR...")
    run_cmd(["clang", "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-S", "custom_benchmark.c", "-o", "custom_benchmark.ll"])
    
    # We must run mem2reg first because raw clang output has too many alloca/load/store for the model to parse well natively,
    # as the training data was pre-processed with basic mem2reg.
    print("   Running mandatory baseline cleanups (-mem2reg -simplifycfg)...")
    run_cmd(["opt", "-S", "-passes=mem2reg,simplifycfg", "custom_benchmark.ll", "-o", "custom_baseline.ll"])
    
    baseline_inst = count_instructions("custom_baseline.ll")
    print(f"\nBaseline Instructions: {baseline_inst}")
    print("-" * 65)
    print(f"{'Action':<15} | {'V8.5 Predicted Δ (%)':<20} | {'True LLVM Δ (%)':<20}")
    print("-" * 65)

    # Now, let's extract the graph of the baseline and run it through the model.
    graph_data = extract_ir_graph("custom_baseline.ll").to(device)
    
    # Calculate state embedding once
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
            # Predict
            action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
            action_onehot[0, action_idx] = 1.0
            
            with torch.no_grad():
                _, predicted_metrics = model(state_emb, action_onehot, graph_data=graph_data)
                pred_pct = predicted_metrics[0, 5].item() * 100.0
                
            # Ground Truth (Raw opt pass)
            out_ir = os.path.join(temp_dir, f"out_{action_name}.ll")
            run_cmd(["opt", "-S", f"-passes={llvm_flag.strip('-')}", "custom_baseline.ll", "-o", out_ir])
            
            actual_inst = count_instructions(out_ir)
            actual_pct = ((actual_inst - baseline_inst) / max(baseline_inst, 1)) * 100.0
            
            print(f"{action_name:<15} | {pred_pct:>19.2f}% | {actual_pct:>19.2f}%")

if __name__ == "__main__":
    main()
