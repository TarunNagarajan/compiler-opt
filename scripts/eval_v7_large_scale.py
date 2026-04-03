"""
V7 Large-Scale IR Evaluation Script

Evaluates the World Model specifically on massive files (e.g. LZ4).
Proves the 'Foveated Vision' efficacy under extreme node counts.
"""

import sys
from pathlib import Path
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v6 import WorldModelV6
from src.env import CompilerOptEnv, RewardMode
from src.config import FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

def evaluate_large(name="v7_final_calibrated_latest", target_file="lz4_analyze.ll"):
    print(f"🚀 Benchmarking V7 World Model on LARGE SCALE: {target_file}")
    
    if not Path(target_file).exists():
        print(f"❌ Error: {target_file} not found.")
        return

    # 1. Load Model
    model = WorldModelV6(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6)
    model_path = MODELS_DIR / f"world_model_v6_{name}.pth"
    if not model_path.exists(): model_path = MODELS_DIR / f"{name}.pth"
    
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    model.load_state_dict(checkpoint['model_state_dict'] if 'model_state_dict' in checkpoint else checkpoint)
    model.eval()
    
    # 2. Setup Env for specific large file
    # We use SPEED mode to get real runtime signals if possible, but HACKABLE is faster for R2.
    env = CompilerOptEnv([target_file], reward_mode=RewardMode.PERFORMANCE)
    
    actual_instr = []
    pred_instr = []
    
    print(f"📊 Collecting 50 transitions on {target_file}...")
    
    try:
        # Reset once to the large file
        obs, info = env.reset(options={"ir_path": target_file})
        curr_graph = env.get_observation_graph()
        
        print(f"   [INFO] Graph Scale: {curr_graph.x.size(0)} nodes, {curr_graph.edge_index.size(1)} edges")
        
        for i in range(50):
            action = env.action_space.sample()
            
            # Real Step
            next_obs, reward, terminated, truncated, info = env.step(action)
            next_graph = env.get_observation_graph()
            
            # Calculate real delta
            instr_red = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
            
            # Predict
            with torch.no_grad():
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0
                
                # V7.7: Pass node count for scaling intuition
                num_nodes = curr_graph.x.size(0) - 1
                _, pred_met_log = model.transition_step(model.encode_graph(curr_graph), action_onehot, num_nodes=num_nodes)
                
                # V7.5: Inverse Log Transform (Factor 10.0)
                pred_met_log = pred_met_log.numpy().flatten()
                pred_met = (np.expm1(np.abs(pred_met_log)) / 10.0) * np.sign(pred_met_log)
            
            actual_instr.append(instr_red)
            pred_instr.append(pred_met[0])
            
            print(f"   Step {i+1:02d}: Action={action:02d} | Actual={instr_red:+.4f} | Pred={pred_instr[-1]:+.4f}")
            
            curr_graph = next_graph
            if terminated or truncated:
                obs, info = env.reset(options={"ir_path": target_file})
                curr_graph = env.get_observation_graph()
                
    except Exception as e:
        print(f"❌ Error during collection: {e}")

    actual_instr = np.array(actual_instr)
    pred_instr = np.array(pred_instr)
    
    # 3. Stats
    r2 = r2_score(actual_instr, pred_instr)
    mae = np.mean(np.abs(actual_instr - pred_instr))
    
    print("\n" + "="*40)
    print(f" LARGE SCALE REPORT: {target_file}")
    print("="*40)
    print(f" Instruction R2 Score: {r2:.4f}")
    print(f" Mean Absolute Error:  {mae:.4f}")
    print("-" * 40)
    
    # 4. Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(actual_instr, pred_instr, alpha=0.7, label='Transitions')
    if len(actual_instr) > 1:
        m, b = np.polyfit(actual_instr, pred_instr, 1)
        plt.plot(actual_instr, m*actual_instr + b, color='red', label=f'Fit (R2={r2:.2f})')
    
    plt.title(f"V7 World Model Performance on {target_file}")
    plt.xlabel("Actual Instruction Delta")
    plt.ylabel("Predicted Instruction Delta")
    plt.legend()
    plt.grid(True)
    
    output_plot = f"v7_large_scale_{target_file.split('.')[0]}.png"
    plt.savefig(output_plot)
    print(f"📊 Plot saved to {output_plot}")

if __name__ == "__main__":
    evaluate_large()
