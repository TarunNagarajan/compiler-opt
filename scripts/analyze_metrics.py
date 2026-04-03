
import sys
from pathlib import Path
import torch
import numpy as np
from sklearn.metrics import mean_absolute_error

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models import create_world_model
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR

def analyze_metric_performance(name="thorough", samples=100):
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS)
    model_path = MODELS_DIR / f"world_model_{name}.pth"
    if not model_path.exists():
        print(f"Model {model_path} not found.")
        return
    model.load_state_dict(torch.load(model_path))
    model.eval()

    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks)
    
    metrics_labels = ["Instr", "Size", "Cmplx", "Loops", "Calls", "Blocks"]
    all_actual = []
    all_pred = []
    
    print(f"[ANALYSIS] Evaluating {samples} transitions for metric-specific bias...")
    
    count = 0
    while count < samples:
        try:
            obs, info = env.reset()
            curr_graph = env.get_observation_graph()
            
            terminated = False
            while not terminated and count < samples:
                action = env.action_space.sample()
                
                # Model Prediction
                with torch.no_grad():
                    action_t = torch.tensor([action], dtype=torch.long)
                    _, pred_metrics = model(curr_graph.x, curr_graph.edge_index, 
                                          torch.zeros(curr_graph.x.size(0), dtype=torch.long), action_t)
                    pred_metrics = pred_metrics.numpy().flatten()
                
                # Reality
                _, _, terminated, _, info = env.step(action)
                actual_metrics = [
                    (info['instructions_after'] - info['instructions_before']) / max(info['instructions_before'], 1),
                    (info['size_after'] - info['size_before']) / max(info['size_before'], 1),
                    (info['complexity_after'] - info['complexity_before']) / 100.0,
                    (info['loops_after'] - info['loops_before']) / 10.0,
                    (info['calls_after'] - info['calls_before']) / 10.0,
                    (info['blocks_after'] - info['blocks_before']) / 20.0
                ]
                
                all_actual.append(actual_metrics)
                all_pred.append(pred_metrics)
                count += 1
                curr_graph = env.get_observation_graph()
        except:
            continue

    actual = np.array(all_actual)
    pred = np.array(all_pred)
    
    print("\n" + "="*60)
    header = "{:<10} | {:<10} | {:<12} | {:<16}".format("Metric", "MAE", "Mean Bias", "Saturated Error")
    print(header)
    print("-" * 60)
    
    for i in range(6):
        mae = mean_absolute_error(actual[:, i], pred[:, i])
        bias = np.mean(pred[:, i] - actual[:, i])
        
        # Saturated Error: How much does it hallucinate when the REAL delta is 0?
        zero_mask = actual[:, i] == 0
        if np.any(zero_mask):
            sat_error = np.mean(np.abs(pred[zero_mask, i]))
        else:
            sat_error = 0.0
            
        row = "{:<10} | {:<10.4f} | {:<12.4f} | {:<16.4f}".format(
            metrics_labels[i], mae, bias, sat_error
        )
        print(row)
    
    print("="*60)
    print("MAE = Mean Absolute Error (Lower is better)")
    print("Bias = Pred - Actual (Positive = Over-optimistic)")
    print("Saturated Error = Hallucination when Actual=0 (Target of Fine-Tuning)")

if __name__ == "__main__":
    analyze_metric_performance(name="thorough")
