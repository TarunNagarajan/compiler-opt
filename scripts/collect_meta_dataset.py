import torch
import random
import argparse
import numpy as np
import sys
import os
sys.path.append(os.getcwd())

from tqdm import tqdm

from src.env.compiler_env import CompilerOptEnv
from src.models.world_model import WorldModel
from src.config import NUM_ACTIONS, FEATURE_DIM, get_benchmark_paths

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def to_scale_tensor(value, default=100.0, device='cpu'):
    if value is None:
        return torch.tensor([[default]], dtype=torch.float32, device=device)
    if isinstance(value, torch.Tensor):
        scale = value.to(device=device, dtype=torch.float32).view(-1, 1)
    else:
        scale = torch.tensor([value], dtype=torch.float32, device=device).view(-1, 1)
    if scale.size(0) > 1:
        scale = scale[:1]
    return scale.clamp(min=1.0)


def collect_meta_dataset(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    set_seed(args.seed)
    rng = random.Random(args.seed)
    
    # Initialize Environment
    # We want a mix of standard and industrial files for calibration
    all_benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(all_benchmarks, max_steps=args.max_steps_per_file)
    print(f"Found {len(env.benchmark_paths)} total benchmarks.")
    
    # Initialize World Model V8.5
    model = WorldModel(
        state_dim=FEATURE_DIM,
        action_dim=NUM_ACTIONS
    ).to(device)
    
    checkpoint = torch.load(args.checkpoint, map_location=device)
    state_dict = checkpoint.get('model_state_dict', checkpoint) if isinstance(checkpoint, dict) else checkpoint
    model.load_state_dict(state_dict)
    model.eval()
    print(f"Loaded Base World Model: {args.checkpoint}")
    
    dataset = []
    
    with torch.no_grad():
        pbar = tqdm(total=args.num_samples, desc="Collecting V8.5 vs Truth tuples")
        while len(dataset) < args.num_samples:
            obs, _ = env.reset(seed=rng.randint(0, 2**31 - 1))
            graph_data = env.get_observation_graph()
            
            for _ in range(args.max_steps_per_file):
                if len(dataset) >= args.num_samples:
                    break
                    
                action_idx = rng.randint(0, NUM_ACTIONS - 1)
                
                # ---------- 1. Get V8.5 Prediction ----------
                if graph_data is None:
                    break
                graph_data = graph_data.to(device)

                state_emb = model.encode_graph(graph_data)
                local_nodes = max(int(graph_data.x.size(0)) - 1, 1)
                num_nodes = torch.tensor([[float(local_nodes)]], dtype=torch.float32, device=device)
                total_nodes = to_scale_tensor(getattr(graph_data, 'total_nodes', None), default=float(local_nodes), device=device)
                
                actions_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                actions_onehot[0, action_idx] = 1.0
                
                # Predict
                _, predicted_metrics = model.transition_step(
                    state_emb, actions_onehot, num_nodes=num_nodes, total_nodes=total_nodes
                )
                
                # ---------- 2. Get Absolute Ground Truth ----------
                # We need the actual delta from the compiler
                obs, _, terminated, truncated, info = env.step(action_idx)
                
                i_before = info.get('instructions_before', 0)
                i_after = info.get('instructions_after', 0)
                actual_metrics = torch.tensor([
                    (i_after - i_before) / max(i_before, 1) * 100.0,
                    (info.get('size_after', 0) - info.get('size_before', 0)) / max(info.get('size_before', 1), 1) * 100.0,
                    (info.get('complexity_after', 0) - info.get('complexity_before', 0)) / max(info.get('complexity_before', 1), 1),
                    (info.get('loops_after', 0) - info.get('loops_before', 0)) / max(info.get('loops_before', 1), 1),
                    (info.get('calls_after', 0) - info.get('calls_before', 0)) / max(info.get('calls_before', 1), 1),
                    (info.get('blocks_after', 0) - info.get('blocks_before', 0)) / max(info.get('blocks_before', 1), 1)
                ], dtype=torch.float32, device=device)
                
                # ---------- 3. Store Tuple ----------
                bench_path = getattr(env, "current_benchmark_path", None)
                dataset.append({
                    'v8_prediction': predicted_metrics.squeeze(0).cpu(),
                    'action': actions_onehot.squeeze(0).cpu(),
                    'scale': total_nodes.squeeze(0).cpu(),
                    'truth': actual_metrics.cpu(),
                    'benchmark': str(bench_path) if bench_path is not None else ""
                })
                pbar.update(1)
                
                # Update graph data for next step
                graph_data = env.get_observation_graph()
                
                if terminated or truncated:
                    break
                    
    pbar.close()
    
    # Save the dataset
    os.makedirs('models', exist_ok=True)
    out_path = "models/meta_dataset.pt"
    torch.save(dataset, out_path)
    print(f"\n[SUCCESS] Meta-Calibration dataset saved to {out_path} ({len(dataset)} samples)")

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to V8.5 best checkpoint")
    parser.add_argument("--num_samples", type=int, default=3000, help="How many tuples to collect")
    parser.add_argument("--max_steps_per_file", type=int, default=10, help="Max steps before hitting another file")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for deterministic collection")
    args = parser.parse_args()
    collect_meta_dataset(args)
