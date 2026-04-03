import sys
from pathlib import Path
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from torch_geometric.data import Batch

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models import create_world_model
from src.env import CompilerOptEnv, RewardMode
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

def evaluate_model(model_name="final", num_samples=100):
    print("\n\033[94m[WORLD MODEL EVAL] LOADING: world_model_{}.pth\033[0m".format(model_name))
    
    # 1. Load Model
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS)
    model_path = MODELS_DIR / "world_model_{}.pth".format(model_name)
    if not model_path.exists():
        print("Error: {} not found.".format(model_path))
        return
    model.load_state_dict(torch.load(model_path, weights_only=True))
    model.eval()

    # 2. Fast Environment (No runtime measurement)
    benchmarks = get_benchmark_paths()
    # Use HACKABLE mode to avoid wall-clock benchmarking
    env = CompilerOptEnv(benchmarks, reward_mode=RewardMode.HACKABLE)
    
    print("Collecting {} structural transitions...".format(num_samples))
    transitions = []
    
    while len(transitions) < num_samples:
        obs, info = env.reset()
        graph = env.get_observation_graph()
        if graph is None: continue
        
        for _ in range(5): # 5 steps per benchmark
            action = env.action_space.sample()
            next_obs, reward, terminated, truncated, info = env.step(action)
            
            # Structural Delta Extraction
            actual = [
                (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1),
                (info['size_after'] - info['size_before']) / max(info['size_before'], 1),
                (info['complexity_after'] - info['complexity_before']) / 100.0,
                (info['loops_after'] - info['loops_before']) / 10.0,
                (info['calls_after'] - info['calls_before']) / 10.0,
                (info['blocks_after'] - info['blocks_before']) / 20.0
            ]
            
            transitions.append((graph, action, actual))
            graph = env.get_observation_graph()
            if terminated or len(transitions) >= num_samples: break

    # 3. Prediction
    actual_arr = np.array([t[2] for t in transitions])
    pred_list = []
    
    print("Simulating neural 'imagination'...")
    with torch.no_grad():
        for g, a, _ in transitions:
            batch_vec = torch.zeros(g.x.size(0), dtype=torch.long)
            act_tensor = torch.tensor([a], dtype=torch.long)
            _, pred = model(g.x, g.edge_index, batch_vec, act_tensor)
            pred_list.append(pred.numpy().flatten())
            
    pred_arr = np.array(pred_list)
    
    # 4. Results
    titles = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]
    print("\n" + "="*40)
    print(" WORLD MODEL FIDELITY REPORT (R^2)")
    print("="*40)
    for i in range(6):
        r2 = r2_score(actual_arr[:, i], pred_arr[:, i])
        print(" {:<15}: {:.4f}".format(titles[i], r2))
    print("="*40)

    # 5. Visualization
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for i in range(6):
        ax = axes[i]
        ax.scatter(actual_arr[:, i], pred_arr[:, i], alpha=0.5, color='blue')
        m = max(abs(actual_arr[:, i].min()), abs(actual_arr[:, i].max()), 
                abs(pred_arr[:, i].min()), abs(pred_arr[:, i].max()), 0.1)
        ax.plot([-m, m], [-m, m], 'r--', label='Ideal')
        ax.set_title(titles[i])
        ax.set_xlabel("Actual Delta")
        ax.set_ylabel("Predicted Delta")
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_name = "world_model_{}_viz.png".format(model_name)
    plt.savefig(plot_name)
    print("\n[VISUAL] Fidelity plot saved to: {}".format(plot_name))

if __name__ == "__main__":
    evaluate_model(num_samples=150)
