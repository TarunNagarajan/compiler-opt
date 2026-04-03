import sys
import time
from pathlib import Path
import torch
import numpy as np
import argparse
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import get_benchmark_paths, FEATURE_DIM
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def evaluate_checkpoint(agent, env, checkpoint_path):
    print(f"Loading checkpoint: {checkpoint_path.name}")
    agent.load_state_dict(torch.load(checkpoint_path, map_location='cpu', weights_only=True))
    agent.eval()
    
    total_rewards = []
    total_steps = []
    
    for i in range(len(env.benchmark_paths)):
        obs, info = env.reset()
        graph = env.get_observation_graph()
        episode_reward = 0
        steps = 0
        
        terminated = False
        while not terminated:
            x = graph.x
            edge_index = graph.edge_index
            edge_attr = getattr(graph, 'edge_attr', None)
            batch_vec = torch.zeros(x.size(0), dtype=torch.long)
            
            with torch.no_grad():
                macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
                m_idx = torch.distributions.Categorical(macro_probs).sample()
                
                terminate_idx = len(MACRO_ACTIONS) - 1
                if m_idx.item() == terminate_idx:
                    terminated = True
                    break
                    
                u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
                u_idx = torch.argmax(u_logits, dim=-1) # Greedy for evaluation
                
            base_seq = MACRO_ACTIONS[m_idx.item()]
            final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
            pipeline = ["module({})".format(",".join(final_seq))]
            
            res = env.executor.apply_passes(env.current_ir_path, pipeline)
            if not res.success:
                terminated = True
                break
                
            runtime_before = env.prev_runtime
            env.current_ir_path = res.output_path
            runtime_after = env.metrics.measure_runtime(env.current_ir_path, iterations=5)
            
            if runtime_after > 0:
                reward = (runtime_before - runtime_after) / max(runtime_before, 1e-6)
                episode_reward += reward
                env.prev_runtime = runtime_after
            else:
                terminated = True
                break
                
            steps += 1
            graph = env.get_observation_graph()
            if env.current_step >= env.max_steps:
                terminated = True
                
        total_rewards.append(episode_reward)
        total_steps.append(steps)
        
    avg_reward = np.mean(total_rewards)
    avg_steps = np.mean(total_steps)
    print(f"  -> Avg Reward: {avg_reward:.4f} | Avg Steps: {avg_steps:.2f}\n")
    return avg_reward, avg_steps

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    args = parser.parse_args()
    
    benchmarks = get_benchmark_paths()
    # Select a small subset of consistent testing files
    test_benchmarks = benchmarks[:10]
    
    env = CompilerOptEnv(test_benchmarks, max_steps=15, reward_mode=RewardMode.SPEED)
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), args.world_model, gnn_layers=args.gnn_layers)
    
    checkpoints = [
        "hrl_antigravity_v4_hrl_hour_0018.pth",
        "hrl_antigravity_v4_hrl_hour_0605.pth",
        "hrl_antigravity_v4_hrl_hour_1203.pth",
        "hrl_antigravity_v4_hrl_hour_1816.pth",
        "hrl_antigravity_v4_hrl_hour_2309.pth",
    ]
    
    results = []
    
    for ckpt_name in checkpoints:
        ckpt_path = Path("models") / ckpt_name
        if ckpt_path.exists():
            avg_r, avg_s = evaluate_checkpoint(agent, env, ckpt_path)
            results.append((ckpt_name, avg_r, avg_s))
        else:
            print(f"Checkpoint not found: {ckpt_path}")

    print("="*50)
    print("CHECKPOINT PROGRESSION RESULTS")
    print("="*50)
    for name, r, s in results:
        print(f"{name:35s} : Reward = {r:+.4f}, Steps = {s:.2f}")

if __name__ == "__main__":
    main()
