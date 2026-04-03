import os
import sys
import subprocess
import time
from pathlib import Path

def launch_image(path):
    if os.path.exists(path):
        print(f"Opening {path}...")
        os.system(f"start {path}")
    else:
        print(f"Error: {path} not found.")

def launch_tensorboard():
    print("Launching Tensorboard on http://localhost:6006 ...")
    print("Press Ctrl+C in this terminal to stop.")
    try:
        subprocess.run(["tensorboard", "--logdir", "logs/tensorboard"])
    except KeyboardInterrupt:
        print("\nTensorboard stopped.")

def launch_attention():
    print("Launching Dynamic Attention Visualization in a new console...")
    print("The graphical trace should pop up immediately.")
    # Use 'start' to open a new terminal window to properly support ANSI color codes
    os.system('start cmd /k "uv run python scripts/visualize_attention.py benchmarks/stencils/stencil_512_double_5pt_003.c"')

def launch_suggestions():
    print("Launching World Model Beam Search Predictions in a new console...")
    os.system('start cmd /k "uv run python scripts/demo_wm_suggestions.py"')

def launch_interaction():
    print("Launching HRL & World Model Interaction Trace in a new console...")
    os.system('start cmd /k "uv run python scripts/demo_hrl_wm_interaction.py"')

def launch_external(cmd_arg):
    print(f"Launching modular visualization: {cmd_arg}...")
    os.system(f'start cmd /k "uv run python scripts/demo_additional_views.py {cmd_arg}"')

def run_wm_sample():
    print("===============================================================================")
    print("   V5 TELESCOPIC WORLD MODEL TRAINING (SIMULATED SAMPLE)")
    print("===============================================================================")
    print("Loading Checkpoint: models/world_model_v5_sprint_checkpoint.pth")
    print("Model Architecture: Telescopic GNN v5 (6 Layers, 128 Latent, 10 Relations)")
    print("Dataset: 5,077 IR Graphs... Pre-processing complete.")
    print()
    
    mock_log = [
        "[Epoch 1, Batch 0100] Total Loss: 4.4522 | Cost MSE: 0.941 | Latent KL: 0.051 | Grad: 0.12",
        "[Epoch 1, Batch 0200] Total Loss: 3.1044 | Cost MSE: 0.722 | Latent KL: 0.048 | Grad: 0.10",
        "[Epoch 1, Batch 0300] Total Loss: 2.3810 | Cost MSE: 0.510 | Latent KL: 0.042 | Grad: 0.09",
        "[Epoch 1, Batch 0400] Total Loss: 1.2045 | Cost MSE: 0.384 | Latent KL: 0.038 | Grad: 0.08",
        "[Epoch 1, Batch 0500] Total Loss: 0.8150 | Cost MSE: 0.291 | Latent KL: 0.035 | Grad: 0.07",
        "[Epoch 2, Batch 0100] Total Loss: 0.6402 | Cost MSE: 0.220 | Latent KL: 0.033 | Grad: 0.06",
        "[Epoch 2, Batch 0200] Total Loss: 0.5511 | Cost MSE: 0.185 | Latent KL: 0.031 | Grad: 0.05",
        "[Epoch 3, Batch 0100] Total Loss: 0.4045 | Cost MSE: 0.144 | Latent KL: 0.029 | Grad: 0.04",
        "[Epoch 3, Batch 0200] Total Loss: 0.3522 | Cost MSE: 0.112 | Latent KL: 0.027 | Grad: 0.03",
        "[Epoch 4, Batch 0050] Total Loss: 0.3011 | Cost MSE: 0.095 | Latent KL: 0.025 | Grad: 0.02",
        "[Epoch 4, Batch 0150] Total Loss: 0.2844 | Cost MSE: 0.082 | Latent KL: 0.024 | Grad: 0.02",
    ]
    
    for line in mock_log:
        time.sleep(0.3)
        print(line)
        
    print()
    print("--- SAMPLE COMPLETE (Truncated for Fast Presentation Demo) ---")

def run_hrl_sample():
    print("===============================================================================")
    print("   MULTI-AGENT HRL TRAINING LOOP (SIMULATED SAMPLE)")
    print("===============================================================================")
    print("Loading World Model: models/hrl_v5_v5_sota_final_hour_0601.pth")
    print("Initializing Replay Buffer: 10,000 capacity")
    print("PPO-Lagrangian Multiplier: 0.012 (Size Constraint: 5%)")
    print("Starting Training Episodes...")
    print()
    
    episodes = [
        """[EPISODE] Source: sparse_access_0091.c | IR: step_1.ll
  Baseline: 0.4ms | O3: 0.4ms | Gap to beat: -3.4%
  Step 18002: M[0] U[11]... [OK] Reward: 0.0029
  Step 18003: M[2] U[14]... [OK] Reward: -0.1120
  Step 18004: M[2] U[19]... [OK] Reward: 0.0768
  Step 18005: M[6] U[7]... [OK] Reward: -0.0941
  Step 18006: M[9] U[3]... [CORRUPT]

  Step 18006: [HEAVY REGRESSION] Episode terminated for safety (+20% slowdown).""",

        """[EPISODE] Source: bitwise_0006.c | IR: step_1.ll
  Baseline: 2.8ms | O3: 1.7ms | Gap to beat: 39.1%
  Step 18007: M[1] U[1]... [OK] Reward: 0.0324
  Step 18008: STOP (BLEND 5.9% | rt:+3.7% instr:+10.8%). Reward: +0.1279 (eff: +0.0192) [2.8ms->2.7ms, O3:1.7ms]""",

        """[EPISODE] Source: pointer_chase_0076.c | IR: step_1.ll
  Baseline: 1.4ms | O3: 1.1ms | Gap to beat: 20.7%
  Step 18009: M[3] U[0]... [OK] Reward: 0.2000
  Step 18010: STOP (RT 27.1% | rt:+27.1% instr:+10.6%). Reward: +0.2000 (eff: +0.0192) [1.4ms->1.1ms, O3:1.1ms] BEAT-O3""",

        """[EPISODE] Source: library_heavy_0060.c | IR: step_1.ll
  Baseline: 0.3ms | O3: 0.2ms | Gap to beat: 17.2%
  Step 18011: M[13] U[17]... [OK] Reward: 0.0742
  Step 18012: M[9] U[16]... [OK] Reward: -0.1722
  Step 18013: M[6] U[14]... [OK] Reward: 0.0579
  Step 18014: M[13] U[7]... [OK] Reward: 0.0297
  Step 18015: M[6] U[4]... [OK] Reward: 0.0055
  Step 18016: M[8] U[3]... [OK] Reward: 0.0620
  Step 18017: STOP (RT 10.2% | rt:+10.2% instr:+1.6%). Reward: +0.1676 (eff: +0.0152) [0.3ms->0.3ms, O3:0.2ms]""",

        """[EPISODE] Source: struct_heavy_0178.c | IR: step_1.ll
  Baseline: 0.5ms | O3: 0.5ms | Gap to beat: 14.9%
  Step 18018: M[3] U[8]... [OK] Reward: -0.0668
  Step 18019: STOP (BLEND 4.4% | rt:+0.0% instr:+14.5%). Reward: +0.1128 (eff: +0.0192) [0.5ms->0.5ms, O3:0.5ms]""",

        """[EPISODE] Source: string_ops_0049.c | IR: step_1.ll
  Baseline: 0.7ms | O3: 0.6ms | Gap to beat: 15.9%
  Step 18020: M[1] U[10]... [OK] Reward: 0.1292
  Step 18021: STOP (RT 13.4% | rt:+13.4% instr:+17.1%). Reward: +0.2000 (eff: +0.0192) [0.7ms->0.6ms, O3:0.6ms]""",

        """[EPISODE] Source: recursive_0034.c | IR: step_1.ll
  Baseline: 16.3ms | O3: 0.2ms | Gap to beat: 98.6%
  Step 18022: M[11] U[0]... [OK] Reward: -0.0066
  Step 18023: STOP (Premature/Slower). Penalty: -0.1""",

        """[EPISODE] Source: multi_func_0102.c | IR: step_1.ll
  Baseline: 0.5ms | O3: 0.2ms | Gap to beat: 60.3%
  Step 18024: M[2] U[14]... [OK] Reward: 0.0334
  Step 18025: M[4] U[18]... [OK] Reward: 0.0930
  Step 18026: STOP (RT 13.3% | rt:+13.3% instr:+0.0%). Reward: +0.2000 (eff: +0.0184) [0.5ms->0.4ms, O3:0.2ms]""",
    ]
    
    for ep in episodes:
        for line in ep.split('\n'):
            time.sleep(0.15)
            print(line)
        print()
        time.sleep(0.5)
        
    print()
    print("--- SAMPLE COMPLETE (Truncated for Fast Presentation Demo) ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python demo_launcher.py <command>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "macro_viz":
        launch_image("macro_actions_dist.png")
        launch_image("macro_actions_landscape.png")
    elif cmd == "wm_viz":
        launch_image("world_model_eval.png")
        launch_image("world_model_final_viz.png")
        launch_image("expertise_report_antigravity_v4_L6_thorough.png")
    elif cmd == "tensorboard":
        launch_tensorboard()
    elif cmd == "wm_sample":
        run_wm_sample()
    elif cmd == "hrl_sample":
        run_hrl_sample()
    elif cmd == "dataset":
        os.system("uv run python scripts/check_dataset_health.py")
    elif cmd == "macros":
        os.system("uv run python scripts/recap_macro_actions.py")
    elif cmd == "attention":
        launch_attention()
    elif cmd == "suggestions":
        launch_suggestions()
    elif cmd == "interaction":
        launch_interaction()
    elif cmd in ["reward", "ast", "refiner", "latency", "clusters", "hardware"]:
        launch_external(cmd)
