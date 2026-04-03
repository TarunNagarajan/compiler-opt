"""
v6 HRL Agent Training Script (Foveated HBC Edition)

Uses HierarchicalMultiAgentV6 with:
- GNNEncoderV6 (Hierarchical Block Condensation / Foveated Perception)
- GRU pass history encoder (full episode memory)
"""

import sys
import time
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import argparse
import random
import csv
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from torch_geometric.data import Batch

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent_v6 import create_hrl_agent_v6
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR, LOGS_DIR
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner, NUM_MICRO_ACTIONS

NUM_MACROS = len(MACRO_ACTIONS)


class MAPPOBufferV6:
    def __init__(self, size):
        self.graphs = []; self.macro_actions = []; self.micro_actions = []
        self.macro_log_probs = []; self.micro_log_probs = []
        self.rewards = []; self.values = []; self.dones = []
        self.size = size

    def reset(self):
        self.graphs = []; self.macro_actions = []; self.micro_actions = []
        self.macro_log_probs = []; self.micro_log_probs = []
        self.rewards = []; self.values = []; self.dones = []


def train_hrl_v6(args):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_id = f"{args.name}_{timestamp}"
    log_dir = LOGS_DIR / "hrl_v6" / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks, max_steps=25, reward_mode=RewardMode.SPEED)
    
    # ===== v6 AGENT =====
    agent = create_hrl_agent_v6(
        state_dim=FEATURE_DIM,
        num_macros=NUM_MACROS,
        world_model_path=args.world_model,
        gnn_layers=args.gnn_layers,
        num_actions=NUM_ACTIONS
    )
    
    current_step = 0
    if args.checkpoint and Path(args.checkpoint).exists():
        ckpt = torch.load(args.checkpoint, weights_only=False)
        agent.load_state_dict(ckpt['model_state_dict'] if 'model_state_dict' in ckpt else ckpt)
        current_step = ckpt.get('current_step', 0)
        print(f"[HRL-v6] Resumed from {args.checkpoint} at step {current_step}")
    
    optimizer = optim.Adam(agent.parameters(), lr=args.lr)
    ppo_epochs = 10; eps_clip = 0.2; last_save_time = time.time()
    
    csv_path = LOGS_DIR / f"optimization_log_v6_{timestamp}.csv"
    with open(csv_path, 'w', newline='') as f:
        writer_csv = csv.writer(f)
        writer_csv.writerow(['Step', 'Program', 'Macro', 'Micro', 'Reward', 'Value', 'Runtime_B', 'Runtime_A'])
        
    while current_step < args.timesteps:
        buffer = MAPPOBufferV6(args.rollout_steps)
        
        while len(buffer.rewards) < args.rollout_steps:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            
            initial_runtime = info.get('initial_runtime_ms', 1.0)
            terminated = False
            episode_steps = 0
            episode_action_history = []
            
            while not terminated and len(buffer.rewards) < args.rollout_steps:
                x = graph.x; edge_index = graph.edge_index; edge_attr = getattr(graph, 'edge_attr', None)
                batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                # Attach action history for GRU
                padded_history = torch.zeros(1, 25, dtype=torch.long)
                if episode_action_history:
                    seq = torch.tensor(episode_action_history, dtype=torch.long)
                    padded_history[0, :min(len(seq), 25)] = seq[-25:]
                graph.action_history = padded_history
                
                with torch.no_grad():
                    macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
                    m_idx = torch.distributions.Categorical(macro_probs).sample()
                    val = agent.get_value(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
                    
                    if m_idx.item() == NUM_MACROS - 1: # TERMINATE
                        micro_logits = torch.zeros(1, NUM_MICRO_ACTIONS)
                        u_idx = torch.tensor([0])
                    else:
                        u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
                        u_idx = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).sample()
                
                # Execute
                if m_idx.item() == NUM_MACROS - 1:
                    reward = 0.0 # Calculate final composite reward in real world logic if needed
                    terminated = True
                else:
                    base_seq = MACRO_ACTIONS[m_idx.item()]
                    final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                    pipeline = ["module({})".format(",".join(final_seq))]
                    
                    obs, reward, terminated, truncated, info = env.step(m_idx.item() + env.num_atomic_passes, custom_passes=pipeline)
                    episode_action_history.append(m_idx.item() + 1)
                
                buffer.graphs.append(graph); buffer.macro_actions.append(m_idx.squeeze()); buffer.micro_actions.append(u_idx.squeeze())
                buffer.macro_log_probs.append(torch.distributions.Categorical(macro_probs).log_prob(m_idx).squeeze())
                buffer.micro_log_probs.append(torch.distributions.Categorical(torch.softmax(u_logits if m_idx.item() < NUM_MACROS-1 else torch.zeros(1, NUM_MICRO_ACTIONS), dim=-1)).log_prob(u_idx).squeeze())
                buffer.rewards.append(reward); buffer.values.append(val.item()); buffer.dones.append(terminated)
                
                current_step += 1
                episode_steps += 1
                graph = env.get_observation_graph()
                
                if current_step % 100 == 0:
                    print(f"  Step {current_step} | Reward: {reward:.4f} | Val: {val.item():.4f}")

        # PPO update
        gamma = 0.99; lam = 0.95
        values_t = torch.tensor(buffer.values, dtype=torch.float32)
        rewards_t = torch.tensor(buffer.rewards, dtype=torch.float32)
        dones_t = torch.tensor(buffer.dones, dtype=torch.float32)
        
        advantages = torch.zeros_like(rewards_t)
        gae = 0.0
        for t in reversed(range(len(buffer.rewards))):
            next_val = 0.0 if t == len(buffer.rewards) - 1 else values_t[t + 1]
            delta = rewards_t[t] + gamma * next_val * (1 - dones_t[t]) - values_t[t]
            gae = delta + gamma * lam * (1 - dones_t[t]) * gae
            advantages[t] = gae
        returns = advantages + values_t
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        for _ in range(ppo_epochs):
            indices = np.arange(len(buffer.rewards))
            np.random.shuffle(indices)
            for start in range(0, len(buffer.rewards), 32):
                end = start + 32
                b_idx = indices[start:end]
                batch_graphs = Batch.from_data_list([buffer.graphs[i] for i in b_idx])
                
                # V6 Forward with block_map
                m_probs, _ = agent.get_macro_action(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, 
                                                   edge_attr=batch_graphs.edge_attr, graph_data=batch_graphs)
                val = agent.get_value(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, 
                                     edge_attr=batch_graphs.edge_attr, graph_data=batch_graphs)
                
                m_acts = torch.stack([buffer.macro_actions[i] for i in b_idx])
                u_acts = torch.stack([buffer.micro_actions[i] for i in b_idx])
                
                new_m_log = torch.distributions.Categorical(m_probs).log_prob(m_acts)
                u_logits = agent.get_micro_action(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, m_acts, 
                                                 edge_attr=batch_graphs.edge_attr, graph_data=batch_graphs)
                new_u_log = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).log_prob(u_acts)
                
                ratio_m = torch.exp(new_m_log - torch.stack([buffer.macro_log_probs[i] for i in b_idx]))
                ratio_u = torch.exp(new_u_log - torch.stack([buffer.micro_log_probs[i] for i in b_idx]))
                
                surr1 = ratio_m * advantages[b_idx]; surr2 = torch.clamp(ratio_m, 1-eps_clip, 1+eps_clip) * advantages[b_idx]
                loss = -torch.min(surr1, surr2).mean() + 0.5 * F.mse_loss(val.squeeze(), returns[b_idx])
                
                optimizer.zero_grad(); loss.backward(); optimizer.step()

        if time.time() - last_save_time > 3600:
            torch.save(agent.state_dict(), MODELS_DIR / f"hrl_v6_{args.name}_latest.pth")
            last_save_time = time.time()

    torch.save(agent.state_dict(), MODELS_DIR / f"hrl_v6_{args.name}_final.pth")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="v6_hrl")
    parser.add_argument("--timesteps", type=int, default=100000)
    parser.add_argument("--rollout_steps", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--checkpoint", type=str, default=None)
    args = parser.parse_args()
    train_hrl_v6(args)
