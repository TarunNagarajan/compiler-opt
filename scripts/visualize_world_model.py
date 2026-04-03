
import sys
from pathlib import Path
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from torch_geometric.data import Data, Batch

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models import create_world_model
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

def visualize_predictions(name="multi"):
    # Load Model
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS, gnn_layers=6)
    model_path = MODELS_DIR / f"world_model_{name}_checkpoint.pth"
    if not model_path.exists():
        print(f"Model {model_path} not found. Train first.")
        return
        
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"Model loaded. (Iteration {checkpoint.get('iteration', 'unknown')})")
    else:
        model.load_state_dict(checkpoint)
        
    model.eval()
    
    # Collect a few test samples
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks) 
    
    print(f"Collecting test samples for {name}...")
    transitions = []
    
    # Collect 200 samples
    while len(transitions) < 200:
        try:
            obs, info = env.reset()
            curr_graph = env.get_observation_graph()
            
            terminated = False
            truncated = False
            
            while not (terminated or truncated):
                action = env.action_space.sample()
                next_obs, reward, terminated, truncated, info = env.step(action)
                next_graph = env.get_observation_graph()
                
                # Metrics
                instr_delta = (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1)
                size_delta = (info['size_after'] - info['size_before']) / max(info['size_before'], 1)
                complexity_delta = (info['complexity_after'] - info['complexity_before']) / 100.0
                loops_delta = (info['loops_after'] - info['loops_before']) / 10.0
                calls_delta = (info['calls_after'] - info['calls_before']) / 10.0
                blocks_delta = (info['blocks_after'] - info['blocks_before']) / 20.0
                
                # Filter No-ops for viz (we want to see if it predicts CHANGES)
                is_noop = (instr_delta == 0 and size_delta == 0 and 
                           complexity_delta == 0 and loops_delta == 0 and 
                           calls_delta == 0 and blocks_delta == 0)
                
                if is_noop:
                     if np.random.random() < 0.8: # Skip most no-ops to focus on changes
                        obs = next_obs
                        curr_graph = next_graph
                        continue
                
                metrics = [instr_delta, size_delta, complexity_delta, loops_delta, calls_delta, blocks_delta]
                
                # Store
                transitions.append((curr_graph, action, metrics))
                
                obs = next_obs
                curr_graph = next_graph
                
                if len(transitions) >= 200: break
        except:
            continue
            
    # Batching
    actual_metrics = np.array([t[2] for t in transitions])
    pred_metrics_list = []
    
    print("Predicting...")
    with torch.no_grad():
        for graph, action, _ in transitions:
            # Single item batch
            batch_vec = torch.zeros(graph.x.size(0), dtype=torch.long)
            action_tensor = torch.tensor([action], dtype=torch.long)
            
            # Forward
            _, pred_metrics, _ = model(graph.x, graph.edge_index, batch_vec, action_tensor)
            
            pred_metrics_list.append(pred_metrics.numpy().flatten())
            
    pred_metrics = np.array(pred_metrics_list)
    
    # Calculate R2
    print("-" * 30)
    print(f"Model Evaluation ({name}) - R2 Score:")
    titles = ["Instr Delta", "Size Delta", "Complexity", "Loops", "Calls", "Blocks"]
    for i in range(6):
        r2 = r2_score(actual_metrics[:, i], pred_metrics[:, i])
        print(f"{titles[i]}: {r2:.4f}")
    print("-" * 30)
    
    # Plot
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i in range(6):
        ax = axes[i]
        ax.scatter(actual_metrics[:, i], pred_metrics[:, i], alpha=0.6)
        
        # Perfect prediction line
        min_val = min(actual_metrics[:, i].min(), pred_metrics[:, i].min())
        max_val = max(actual_metrics[:, i].max(), pred_metrics[:, i].max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect')
        
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title(titles[i])
        ax.legend()
        ax.grid(True)
        
    plt.tight_layout()
    output_plot = f"world_model_{name}_eval.png"
    plt.savefig(output_plot)
    print(f"Plot saved to {output_plot}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize World Model Predictions")
    parser.add_argument("--name", type=str, default="multi", help="Suffix for the model to load (e.g. 'thorough')")
    args = parser.parse_args()
    visualize_predictions(args.name)
