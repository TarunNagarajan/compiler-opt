
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
import argparse
import random
from stable_baselines3 import PPO
from torch_geometric.data import Data

from src.env import CompilerOptEnv, RewardMode
from src.models import create_world_model
from src.config import FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES, get_benchmark_paths, MODELS_DIR

class WorldModelAgent:
    def __init__(self, model_path):
        self.model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.eval()
        
    def predict(self, env):
        graph = env.get_observation_graph()
        if graph is None:
            return env.action_space.sample()
            
        best_action = 0
        best_delta = 1.0 # Looking for most negative delta (reduction)
        
        with torch.no_grad():
            x = graph.x
            edge_index = graph.edge_index
            batch = torch.zeros(x.size(0), dtype=torch.long)
            
            # Evaluate all possible actions
            for a in range(NUM_ACTIONS):
                action_t = torch.tensor([a], dtype=torch.long)
                _, metrics = self.model(x, edge_index, batch, action_t)
                
                # metrics: [instr, size, cmplx, loops, calls, blocks]
                instr_delta = metrics[0, 0].item()
                
                if instr_delta < best_delta:
                    best_delta = instr_delta
                    best_action = a
                    
        return best_action

def evaluate_agent(agent, env, num_episodes=5):
    all_results = []
    
    for ep in range(num_episodes):
        obs, info = env.reset()
        terminated = False
        truncated = False
        
        while not (terminated or truncated):
            if isinstance(agent, WorldModelAgent):
                action = agent.predict(env)
            else:
                action, _ = agent.predict(obs, deterministic=True)
                
            obs, reward, terminated, truncated, info = env.step(action)
            
        res = env.get_total_improvement()
        all_results.append(res)
        
    # Aggregate
    avg_reduction = np.mean([r['reduction_pct'] for r in all_results])
    avg_size = np.mean([r['size_change_pct'] for r in all_results])
    avg_diversity = np.mean([r['pass_diversity'] for r in all_results])
    
    return {
        'reduction': avg_reduction,
        'size_change': avg_size,
        'diversity': avg_diversity
    }

def run_comparison():
    benchmarks = get_benchmark_paths()
    # Use a small stable set for comparison
    test_benchmarks = random.sample(benchmarks, min(len(benchmarks), 10))
    
    print("Comparing agents on {} benchmarks...".format(len(test_benchmarks)))
    
    # 1. PPO Hackable (Performance focus)
    print("Loading PPO-Hackable...")
    ppo_h = PPO.load("models/ppo_hackable.zip")
    
    # 2. PPO Secure (Constraint focus)
    print("Loading PPO-Secure...")
    ppo_s = PPO.load("models/ppo_secure.zip")
    
    # 3. World Model Agent (The "Good" one)
    print("Loading World Model Agent (final)...")
    wm_agent = WorldModelAgent("models/world_model_final.pth")
    
    env = CompilerOptEnv(test_benchmarks, max_steps=10)
    
    print("\n" + "="*70)
    header = "{:<20} | {:<14} | {:<14} | {:<10}".format("Agent", "Instr Reduc %", "Size Change %", "Diversity")
    print(header)
    print("-" * 70)
    
    # Eval Hackable
    res_h = evaluate_agent(ppo_h, env)
    row_h = "{:<20} | {:12.2f}% | {:12.2f}% | {:10.2f}".format(
        "PPO-Hackable", res_h['reduction'], res_h['size_change'], res_h['diversity']
    )
    print(row_h)
    
    # Eval Secure
    res_s = evaluate_agent(ppo_s, env)
    row_s = "{:<20} | {:12.2f}% | {:12.2f}% | {:10.2f}".format(
        "PPO-Secure", res_s['reduction'], res_s['size_change'], res_s['diversity']
    )
    print(row_s)
    
    # Eval World Model
    res_wm = evaluate_agent(wm_agent, env)
    row_wm = "{:<20} | {:12.2f}% | {:12.2f}% | {:10.2f}".format(
        "World-Model-Greedy", res_wm['reduction'], res_wm['size_change'], res_wm['diversity']
    )
    print(row_wm)
    
    print("="*70)

if __name__ == "__main__":
    run_comparison()
