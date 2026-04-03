import sys
from pathlib import Path
import torch
import torch.nn.functional as F
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv
from src.models import create_world_model
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS

def evaluate_model(checkpoint_path, num_samples=50):
    print(f"\n[EVAL] Loading World Model from {checkpoint_path}...")
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS, gnn_layers=6)
    
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"[EVAL] Model loaded. (Iteration {checkpoint.get('iteration', 'unknown')})")
    else:
        model.load_state_dict(checkpoint)
        print("[EVAL] Model loaded directly.")
        
    model.eval()
    
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks, max_steps=1) # 1 step per reset
    
    print(f"\n[EVAL] Running {num_samples} ground-truth evaluations...")
    
    all_true = []
    all_pred = []
    
    successes = 0
    with torch.no_grad():
        for i in range(num_samples):
            try:
                # Reset to get a random graph
                obs, info = env.reset()
                graph = env.get_observation_graph()
                if graph is None: continue
                
                # Pick a random action
                action = env.action_space.sample()
                
                # Extract initial metrics to compute true delta
                instr_before = info['initial_instructions']
                size_before = info['initial_size']
                complexity_before = info['initial_complexity']
                loops_before = info.get('initial_loops', 0)
                calls_before = info.get('initial_calls', 0)
                blocks_before = info.get('initial_blocks', 0)
                
                # Execute action in actual environment (Ground Truth)
                next_obs, reward, term, trunc, step_info = env.step(action)
                
                instr_after = step_info['instructions_after']
                size_after = step_info['size_after']
                complexity_after = step_info.get('complexity_after', 0)
                loops_after = step_info.get('loops_after', 0)
                calls_after = step_info.get('calls_after', 0)
                blocks_after = step_info.get('blocks_after', 0)
                
                # Compute True Target Deltas
                instr_delta = (instr_after - instr_before) / max(instr_before, 1)
                size_delta = (size_after - size_before) / max(size_before, 1)
                complexity_delta = (complexity_after - complexity_before) / 100.0
                loops_delta = (loops_after - loops_before) / 10.0
                calls_delta = (calls_after - calls_before) / 10.0
                blocks_delta = (blocks_after - blocks_before) / 20.0
                
                true_metrics = torch.tensor([[
                    instr_delta, size_delta, complexity_delta, 
                    loops_delta, calls_delta, blocks_delta
                ]], dtype=torch.float32)
                
                # Predict via World Model
                action_tensor = torch.tensor([action], dtype=torch.long)
                edge_attr = getattr(graph, 'edge_attr', None)
                if edge_attr is None: edge_attr = torch.zeros(graph.edge_index.size(1), dtype=torch.long)
                
                _, pred_metrics, _ = model(
                    graph.x.unsqueeze(0) if graph.x.dim() == 1 else graph.x, 
                    graph.edge_index, 
                    torch.zeros(graph.x.size(0), dtype=torch.long), 
                    action_tensor, 
                    edge_attr=edge_attr
                )
                
                all_true.append(true_metrics)
                all_pred.append(pred_metrics)
                successes += 1
                
                print(f"  Sample {successes}/{num_samples} | Action: {action:2d} | True Instr Δ: {instr_delta*100:+8.2f}% | Pred Instr Δ: {pred_metrics[0][0].item()*100:+8.2f}%", end='\r')
                
                if successes >= num_samples:
                    break
                    
            except Exception as e:
                continue
                
    print("\n\n[EVAL] Finished collecting samples. Computing error statistics...")
    
    if len(all_true) == 0:
        print("[EVAL] Failed to collect any valid samples.")
        return
        
    y_true = torch.cat(all_true, dim=0)
    y_pred = torch.cat(all_pred, dim=0)
    
    # Calculate Mean Absolute Error across the entire dataset
    mae = F.l1_loss(y_pred, y_true).item()
    
    # Calculate Per-Metric MAE
    metric_names = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]
    mae_per_metric = F.l1_loss(y_pred, y_true, reduction='none').mean(dim=0)
    
    print(f"\n============================================================")
    print(f"🌎 World Model Predictive Accuracy")
    print(f"============================================================")
    print(f"Total Samples Evaluated: {successes}")
    print(f"Overall Mean Absolute Error (MAE): {mae:.4f}")
    print("\nPer-Metric Mean Absolute Errors:")
    for i, name in enumerate(metric_names):
        print(f"  - {name:15s}: {mae_per_metric[i].item():.4f}")
        
    print(f"\nSample Predictions (Instr | Size):")
    for i in range(min(5, successes)):
        t_i, t_s = y_true[i][0].item(), y_true[i][1].item()
        p_i, p_s = y_pred[i][0].item(), y_pred[i][1].item()
        print(f"  Sample {i+1}: True[{t_i*100:+6.1f}%, {t_s*100:+5.1f}%] -> Pred[{p_i*100:+6.1f}%, {p_s*100:+5.1f}%]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="models/world_model_antigravity_v4_L6_checkpoint.pth")
    parser.add_argument("--samples", type=int, default=100)
    args = parser.parse_args()
    
    evaluate_model(args.checkpoint, args.samples)
