"""
Training script for hierarchical reinforcement learning agent using Dyna-style 
world model refinement.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import argparse
import random
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from torch_geometric.data import Batch

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv, RewardMode
from src.models.world_model import WorldModel
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.models.hrl_agent import HRLAgent
from src.env.hardware_profiler import HardwareProfiler
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, NUM_ATOMIC_ACTIONS, MODELS_DIR, LOGS_DIR
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import NUM_MICRO_ACTIONS, MicroRefiner

NUM_MACROS = len(MACRO_ACTIONS)

class MAPPOBuffer:
    def __init__(self):
        self.graphs = []
        self.macro_actions = []
        self.micro_actions = []
        self.macro_log_probs = []
        self.micro_log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []
        self.action_histories = []
        self.state_embs = []
        self.mission_targets = []
        self.macro_onehots = []
        self.local_nodes = []
        self.total_nodes = []

    def reset(self):
        self.graphs = []; self.macro_actions = []; self.micro_actions = []
        self.macro_log_probs = []; self.micro_log_probs = []
        self.rewards = []; self.values = []; self.dones = []
        self.action_histories = []
        self.state_embs = []
        self.mission_targets = []
        self.macro_onehots = []
        self.local_nodes = []
        self.total_nodes = []


class MissionTargetPredictor(nn.Module):
    """
    Predicts mission-specific scalar targets from the metrics output.
    """
    def __init__(self, metrics_dim=6, hidden_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(metrics_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, metrics):
        return self.net(metrics).squeeze(-1)


def train_hrl(args):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_id = f"hrl_{args.name}_{timestamp}"
    log_dir = LOGS_DIR / "hrl" / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[HRL] Training on {device}")
    
    # 1. Load World Model
    base_wm = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    wm_ckpt = torch.load(args.world_model, map_location=device)
    base_wm.load_state_dict(wm_ckpt.get('model_state_dict', wm_ckpt))
    
    world_model = CalibratedWorldModel(base_wm, meta_calibrator_path=args.meta_calibrator).to(device)
    world_model.eval()

    
    # 2. Initialize V8 HRL Agent
    agent = HRLAgent(
        state_dim=FEATURE_DIM,
        num_macros=NUM_MACROS,
        world_model=world_model,
        num_actions=NUM_ACTIONS
    ).to(device)
    
    agent_optimizer = optim.Adam(agent.parameters(), lr=args.lr)
    mission_target_head = MissionTargetPredictor(metrics_dim=6, hidden_dim=32).to(device)
    mission_target_head.eval()
    # Dyna-Dagger: jointly refine world-model scale-correction and mission-target mapping
    wm_optimizer = optim.Adam([
        {'params': world_model.base_model.scale_correction.parameters(), 'lr': 1e-5},
        {'params': mission_target_head.parameters(), 'lr': 3e-4},
    ])
    
    # 3. Environment & Mission Setup
    mission = args.mission
    reward_mode = RewardMode.SPEED if mission == "performance" else RewardMode.SIZE
    collect_speed_metrics = mission == "embedded"
    print(f"[HRL-v8] Mission: {mission.upper()} | RewardMode: {reward_mode.value}")
    
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(
        benchmarks,
        max_steps=25,
        reward_mode=reward_mode,
        collect_speed_metrics=collect_speed_metrics,
    )
    
    buffer = MAPPOBuffer()
    current_step = 0
    gamma = 0.99
    lam = 0.95
    eps_clip = 0.2
    last_save_time = time.time()
    start_time = time.time()
    
    PER_STEP_COST = -0.0025
    
    pass_stats = {i: {'count': 0, 'crashes': 0, 'regressions': 0, 'speedups': 0} for i in range(NUM_MACROS)}
    
    print(f"[HRL-v8] Starting training loop for {args.timesteps} steps...")
    
    while current_step < args.timesteps:
        # --- HOURLY CHECKPOINT ---
        if time.time() - last_save_time > 3600:
            elapsed_hr = int((time.time() - start_time) // 3600)
            ckpt_path = MODELS_DIR / f"hrl_{run_id}_hour_{elapsed_hr:03}.pth"
            torch.save({
                'model_state_dict': agent.state_dict(),
                'optimizer_state_dict': agent_optimizer.state_dict(),
                'wm_scale_state_dict': world_model.base_model.scale_correction.state_dict(),
                'wm_target_head_state_dict': mission_target_head.state_dict(),
                'step': current_step
            }, ckpt_path)
            print(f"  [Checkpoint] Saved hourly model to {ckpt_path}")
            last_save_time = time.time()

        # --- ROLLOUT PHASE ---
        obs, info = env.reset()
        source_name = Path(env.current_benchmark_path).name if hasattr(env, 'current_benchmark_path') else "unknown"
        initial_instr = info.get('initial_instructions', 999)
        
        # O3 Baseline for reference (matching v5 style)
        o3_runtime = info.get('o3_runtime', 0.0)
        o3_instr = info.get('o3_instructions', 0)
        o3_energy = info.get('o3_energy', 0.0)
        initial_runtime = info.get('initial_runtime', 1.0)
        initial_energy = info.get('initial_energy', 1e-6)
        
        o3_gap = (initial_runtime - o3_runtime) / max(initial_runtime, 1e-6) * 100 if o3_runtime > 0 else 0
        o3_instr_gap = (initial_instr - o3_instr) / max(initial_instr, 1) * 100 if o3_instr > 0 else 0
        o3_energy_gap = (initial_energy - o3_energy) / max(initial_energy, 1e-6) * 100 if o3_energy > 0 else 0
        
        print(f"\n[EPISODE] Source: {source_name} | Initial Instructions: {initial_instr}")
        if mission == "performance":
            print(f"  O3 Baseline: {o3_runtime:.1f}ms | Gap: {o3_gap:+.1f}%")
        else:
            print(f"  O3 Baseline: {o3_energy*1000:.1f}mJ | Gap: {o3_energy_gap:+.1f}%")
        if o3_runtime > 0 or o3_instr > 0:
            print(f"  Baseline: {initial_runtime:.1f}ms | O3: {o3_runtime:.1f}ms | Gap: {o3_gap:+.1f}%", end="", flush=True)
            if o3_instr > 0:
                print(f" (O3 Instr: {o3_instr} | Gap: {o3_instr_gap:+.1f}%)", flush=True)
            else:
                print("", flush=True)
        
        history = [0]
        episode_reward = 0
        best_instr = initial_instr
        terminate_idx = NUM_MACROS - 1
        
        for t in range(25):
            graph_data = env.get_observation_graph()
            if graph_data is None: break

            local_nodes = max(int(graph_data.x.size(0) - 1), 1)
            raw_total_nodes = getattr(graph_data, 'total_nodes', torch.tensor([float(local_nodes)]))
            if isinstance(raw_total_nodes, torch.Tensor):
                total_nodes_val = float(raw_total_nodes.view(-1)[0].item())
            else:
                total_nodes_val = float(raw_total_nodes)
            
            # Action History Tensor
            hist_tensor = torch.tensor([history], dtype=torch.long, device=device)
            
            # Get Selection Probs (incorporates Calibrated Imagination)
            with torch.no_grad():
                macro_probs, _, history_emb, state_emb = agent(
                    graph_data.x.to(device), 
                    graph_data.edge_index.to(device), 
                    getattr(graph_data, 'batch', None),
                    edge_attr=graph_data.edge_attr.to(device),
                    action_history=hist_tensor,
                    graph_data=graph_data
                )
                
                # Sample Macro
                dist_m = torch.distributions.Categorical(macro_probs)
                macro_act = dist_m.sample()
                m_log_prob = dist_m.log_prob(macro_act)
                
                # Get Worker Refinement
                macro_onehot = torch.zeros(1, NUM_MACROS, device=device)
                macro_onehot[0, macro_act] = 1.0
                micro_probs = agent.get_worker_act(state_emb, macro_onehot, history_emb)
                
                dist_u = torch.distributions.Categorical(micro_probs)
                micro_act = dist_u.sample()
                u_log_prob = dist_u.log_prob(micro_act)
                
                val = agent.get_value(state_emb, history_emb)

            # Step logic: step with the macro action
            # Logging style: Step {step}: M[{idx}] U[{idx}] [Imag: -5.4% | True: -5.2%]... [OK] Reward: {val}
            with torch.no_grad():
                wm_action_onehot = torch.zeros(1, NUM_ACTIONS, device=device)
                wm_action_onehot[0, NUM_ATOMIC_ACTIONS + macro_act.item()] = 1.0
                wm_num_nodes = torch.tensor([float(local_nodes)], dtype=torch.float32, device=device)
                wm_total_nodes = torch.tensor([float(total_nodes_val)], dtype=torch.float32, device=device)
                _, imag_metrics = world_model.transition_step(
                    state_emb,
                    wm_action_onehot,
                    num_nodes=wm_num_nodes,
                    total_nodes=wm_total_nodes,
                )
                imag_val = mission_target_head(imag_metrics)[0].item()
            
            print(f"  Step {current_step}: M[{macro_act.item()}] U[{micro_act.item()}] [Imag({'Spd' if mission=='performance' else 'Carbon'}): {imag_val:+.2f}%", end="", flush=True)

            if macro_act.item() == terminate_idx:
                terminated = True
                truncated = False
                reward = 0.0
                info_step = info
            else:
                base_seq = MACRO_ACTIONS[macro_act.item()]
                refined_seq = MicroRefiner.apply_refinement(base_seq, micro_act.item())
                refined_pipeline = [f"module({','.join(refined_seq)})"]
                _, reward, terminated, truncated, info_step = env.step(
                    NUM_ATOMIC_ACTIONS + macro_act.item(),
                    custom_passes=refined_pipeline,
                )
                info = info_step
                
                # Mission-aware True values
                runtime_before = info_step.get('runtime_before', 0.0)
                runtime_after = info_step.get('runtime_after', 0.0)
                instr_before = info_step.get('instructions_before', 1)
                instr_after = info_step.get('instructions_after', 1)
                energy_before = info_step.get('energy_before', 0.0)
                energy_after = info_step.get('energy_after', 0.0)

                true_spd = 0.0
                if runtime_before > 0 and runtime_after > 0:
                    true_spd = (runtime_before - runtime_after) / max(runtime_before, 1e-6) * 100.0
                true_inst = (instr_before - instr_after) / max(instr_before, 1) * 100.0
                true_energy = 0.0
                if energy_before > 0 and energy_after > 0:
                    true_energy = (energy_before - energy_after) / max(energy_before, 1e-6) * 100.0
                
                if mission == "performance":
                    print(f" | True(Spd): {true_spd:+.2f}% | Instr: {true_inst:+.2f}%]...", end="", flush=True)
                else:
                    # Nuanced Embedded (Total Carbon): Dynamic weights
                    carbon_score = (
                        args.weight_size * true_inst +
                        args.weight_speed * true_spd +
                        args.weight_energy * true_energy
                    )

                    # Edge-device structural proxy: smaller memory traffic and flatter CFG.
                    def _delta(before_key, after_key):
                        before_v = float(info_step.get(before_key, 0.0))
                        after_v = float(info_step.get(after_key, 0.0))
                        if before_v <= 0:
                            return 0.0
                        return (before_v - after_v) / max(before_v, 1e-6)

                    edge_proxy = (
                        0.30 * _delta('loads_before', 'loads_after') +
                        0.15 * _delta('stores_before', 'stores_after') +
                        0.20 * _delta('allocas_before', 'allocas_after') +
                        0.20 * _delta('blocks_before', 'blocks_after') +
                        0.15 * _delta('calls_before', 'calls_after')
                    )
                    reward = (carbon_score / 100.0) + (0.10 * edge_proxy) + PER_STEP_COST
                    print(
                        f" | True(Carbon): {carbon_score:+.2f}% | Energy: {true_energy:+.2f}% | Edge: {edge_proxy*100:+.2f}%]...",
                        end="",
                        flush=True,
                    )
                
                # Action repetition penalty (matching v5)
                if len(history) > 1 and (NUM_ATOMIC_ACTIONS + macro_act.item()) == history[-1]:
                    reward -= 0.01
                reward = max(min(reward, 0.2), -0.2)

            # --- End of Episode Payout ---
            if terminated or truncated or macro_act.item() == terminate_idx:
                if macro_act.item() == terminate_idx: print("] -> [STOP]", end="", flush=True)
                
                # Instruction Reduction
                instr_final = info.get('instructions_after', initial_instr)
                instr_red = (initial_instr - instr_final) / max(initial_instr, 1)
                
                # Runtime Reduction
                runtime_final = info.get('runtime_after', 0.0)
                runtime_red = (initial_runtime - runtime_final) / max(initial_runtime, 1e-6)
                energy_final = info.get('energy_after', 0.0)
                energy_red = (initial_energy - energy_final) / max(initial_energy, 1e-6) if initial_energy > 0 else 0.0
                
                if mission == "performance":
                    total_reduction = runtime_red if initial_runtime > 0 else instr_red
                else:
                    total_reduction = (
                        args.weight_size * instr_red +
                        args.weight_speed * runtime_red +
                        args.weight_energy * energy_red
                    )
                
                if total_reduction > 0.03:
                    term_bonus = min(0.2, 0.05 + total_reduction)
                    reward += term_bonus
                    print(f" [TERM REWARD: +{term_bonus:.4f}]", end="")
                elif macro_act.item() == terminate_idx:
                    reward -= 0.1
                    print(f" [TERM PENALTY: -0.1000]", end="")
                
                # Cap the combined final reward
                reward = max(min(reward, 0.4), -0.4) 
                if macro_act.item() == terminate_idx: print("") # Newline for explicit STOP
                else: print(f" [OK] Reward: {reward:.4f}")
            else:
                print(f" [OK] Reward: {reward:.4f}")
            
            pass_stats[macro_act.item()]['count'] += 1
            if reward > 0.01: pass_stats[macro_act.item()]['speedups'] += 1
            if reward < -0.01: pass_stats[macro_act.item()]['regressions'] += 1
            
            buffer.graphs.append(graph_data)
            buffer.macro_actions.append(macro_act)
            buffer.micro_actions.append(micro_act)
            buffer.macro_log_probs.append(m_log_prob)
            buffer.micro_log_probs.append(u_log_prob)
            buffer.rewards.append(reward)
            buffer.values.append(val.squeeze())
            buffer.dones.append(terminated or truncated)
            buffer.action_histories.append(hist_tensor.cpu())
            buffer.state_embs.append(state_emb.detach())
            buffer.local_nodes.append(float(local_nodes))
            buffer.total_nodes.append(float(total_nodes_val))
            
            # For World Model Refinement (Dyna-Dagger): Store mission-relevant delta
            if macro_act.item() == terminate_idx:
                target_red = 0.0
            elif mission == "performance":
                # Store CYCLE SPEEDUP (positive-good convention)
                r_before = info.get('runtime_before', 0.0)
                r_after = info.get('runtime_after', 0.0)
                if r_before > 0 and r_after > 0:
                    target_red = (r_before - r_after) / max(r_before, 1e-6) * 100.0
                else:
                    target_red = 0.0
            else:
                # Store CARBON SCORE (weighted positive-good convention).
                i_before = info.get('instructions_before', 1)
                i_after = info.get('instructions_after', 1)
                r_before = info.get('runtime_before', 0.0)
                r_after = info.get('runtime_after', 0.0)
                e_before = info.get('energy_before', 0.0)
                e_after = info.get('energy_after', 0.0)
                inst_red = (i_before - i_after) / max(i_before, 1) * 100.0
                spd_red = ((r_before - r_after) / max(r_before, 1e-6) * 100.0) if (r_before > 0 and r_after > 0) else 0.0
                energy_red = ((e_before - e_after) / max(e_before, 1e-6) * 100.0) if (e_before > 0 and e_after > 0) else 0.0
                target_red = (
                    args.weight_size * inst_red +
                    args.weight_speed * spd_red +
                    args.weight_energy * energy_red
                )
            
            buffer.mission_targets.append(target_red)
            wm_oh = torch.zeros(NUM_ACTIONS, device=device)
            wm_oh[NUM_ATOMIC_ACTIONS + macro_act.item()] = 1.0
            buffer.macro_onehots.append(wm_oh)
            
            episode_reward += reward
            history.append(NUM_ATOMIC_ACTIONS + macro_act.item())
            current_step += 1
            
            current_instr = info.get('instructions_after', initial_instr)
            if current_instr < best_instr: best_instr = current_instr
            
            if terminated or truncated:
                instr_final = info.get('instructions_after', initial_instr)
                runtime_final = info.get('runtime_after', 0.0)
                energy_final = info.get('energy_after', 0.0)
                
                improvement = (initial_instr - instr_final) / max(initial_instr, 1) * 100
                speedup = (initial_runtime - runtime_final) / max(initial_runtime, 1e-6) * 100
                energy_save = (initial_energy - energy_final) / max(initial_energy, 1e-6) * 100
                
                print(f"  STOP (Instr: {improvement:+.1f}% | Spd: {speedup:+.1f}% | Energy: {energy_save:+.1f}%) Episode Reward: {episode_reward:.4f}")
                break
                
            if current_step % 500 == 0:
                print("\n--- PER-PASS PERFORMANCE (Last 500 steps) ---")
                for midx in range(NUM_MACROS):
                    s = pass_stats[midx]
                    if s['count'] > 0:
                        name = MACRO_ACTIONS[midx][0][:15]
                        print(f"Pass {midx:<2} ({name:<15}): Count: {s['count']:<3} | Speedups: {s['speedups']:<3} | Regressions: {s['regressions']:<3}")
                pass_stats = {i: {'count': 0, 'crashes': 0, 'regressions': 0, 'speedups': 0} for i in range(NUM_MACROS)}

        # --- UPDATE PHASE (PPO) ---
        if len(buffer.rewards) >= args.rollout_steps:
            # 1. Calculate Advantages (GAE)
            values = torch.stack(buffer.values).detach()
            rewards = torch.tensor(buffer.rewards, dtype=torch.float32, device=device)
            dones = torch.tensor(buffer.dones, dtype=torch.float32, device=device)
            
            advantages = torch.zeros_like(rewards)
            last_gae = 0
            for t in reversed(range(len(rewards))):
                if t == len(rewards) - 1:
                    next_value = 0
                else:
                    next_value = values[t+1]
                
                delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
                last_gae = delta + gamma * lam * (1 - dones[t]) * last_gae
                advantages[t] = last_gae
            
            returns = advantages + values
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
            
            # 2. PPO Update Epochs
            agent.train()
            optimizer = agent_optimizer # map to correct optimizer
            for _ in range(4): # 4 Epochs
                indices = np.arange(len(buffer.rewards))
                np.random.shuffle(indices)
                for start in range(0, len(buffer.rewards), 32):
                    end = start + 32
                    batch_idx = indices[start:end]
                    
                    batch_graphs = Batch.from_data_list([buffer.graphs[i] for i in batch_idx]).to(device)
                    batch_hist = torch.cat([buffer.action_histories[i] for i in batch_idx], dim=0).to(device)
                    
                    m_probs, _, history_emb, state_emb = agent(
                        batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, 
                        edge_attr=batch_graphs.edge_attr,
                        action_history=batch_hist, graph_data=batch_graphs
                    )
                    
                    # Policy Loss (Simplified for dry-run/bootstrap)
                    m_actions = torch.stack([buffer.macro_actions[i] for i in batch_idx]).to(device)
                    new_m_log = torch.distributions.Categorical(m_probs).log_prob(m_actions)
                    old_m_log = torch.stack([buffer.macro_log_probs[i] for i in batch_idx]).to(device)
                    
                    ratio = torch.exp(new_m_log - old_m_log)
                    surr1 = ratio * advantages[batch_idx]
                    surr2 = torch.clamp(ratio, 1-eps_clip, 1+eps_clip) * advantages[batch_idx]
                    
                    val_pred = agent.get_value(state_emb, history_emb)
                    loss = -torch.min(surr1, surr2).mean() + 0.5 * F.mse_loss(val_pred.squeeze(), returns[batch_idx])
                    
                    optimizer.zero_grad(); loss.backward(); optimizer.step()
            
            print(f"  [Update] Step {current_step} | Mean Buffer Reward: {np.mean(buffer.rewards):.4f}")

            # 3. Dyna-Dagger: World Model Refinement (Learning from exploration)
            world_model.train()
            mission_target_head.train()
            if getattr(world_model, 'meta_net', None) is not None:
                # Keep calibrator deterministic; optimize only scale-correction + mission-target head.
                world_model.meta_net.eval()
            for _ in range(4): # 4 Epochs
                indices = np.arange(len(buffer.rewards))
                np.random.shuffle(indices)
                for start in range(0, len(buffer.rewards), 32):
                    end = start + 32
                    batch_idx = indices[start:end]
                    
                    b_state_embs = torch.stack([buffer.state_embs[i] for i in batch_idx]).to(device)
                    b_macro_oh = torch.stack([buffer.macro_onehots[i] for i in batch_idx]).to(device)
                    b_actual_red = torch.tensor([buffer.mission_targets[i] for i in batch_idx], dtype=torch.float32, device=device)
                    b_local_nodes = torch.tensor([buffer.local_nodes[i] for i in batch_idx], dtype=torch.float32, device=device)
                    b_total_nodes = torch.tensor([buffer.total_nodes[i] for i in batch_idx], dtype=torch.float32, device=device)
                    
                    # Predict Δ% using Scale Correction Pathway
                    _, imag_metrics = world_model.transition_step(
                        b_state_embs,
                        b_macro_oh,
                        num_nodes=b_local_nodes,
                        total_nodes=b_total_nodes,
                    )
                    pred_red = mission_target_head(imag_metrics)
                    
                    wm_loss = F.mse_loss(pred_red, b_actual_red)
                    wm_optimizer.zero_grad(); wm_loss.backward(); wm_optimizer.step()
            
            print(f"  [Dyna] Refined mission-target mapping + scale-correction | Loss: {wm_loss.item():.6f}")
            buffer.reset()
            world_model.eval()
            mission_target_head.eval()

    final_ckpt_path = MODELS_DIR / f"hrl_{run_id}_final.pth"
    torch.save({
        'model_state_dict': agent.state_dict(),
        'optimizer_state_dict': agent_optimizer.state_dict(),
        'wm_scale_state_dict': world_model.base_model.scale_correction.state_dict(),
        'wm_target_head_state_dict': mission_target_head.state_dict(),
        'step': current_step
    }, final_ckpt_path)
    print(f"[HRL-v8] Saved final checkpoint to {final_ckpt_path}")
    writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="v8_hrl")
    parser.add_argument("--timesteps", type=int, default=250000)
    parser.add_argument("--rollout_steps", type=int, default=1024)
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--meta_calibrator", type=str, required=True)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--mission", type=str, choices=["performance", "embedded"], default="performance",
                        help="performance: prioritize runtime speed | embedded: weighted size+speed+energy objective")
    
    # ⚖️ Dynamic Carbon Weights (Only for 'embedded' mission)
    parser.add_argument("--weight_size", type=float, default=None, help="Weight for Code Size reduction (0.0 - 1.0)")
    parser.add_argument("--weight_speed", type=float, default=None, help="Weight for Execution Speed reduction (0.0 - 1.0)")
    parser.add_argument("--weight_energy", type=float, default=None, help="Weight for Energy (J) reduction (0.0 - 1.0)")
    
    args = parser.parse_args()
    
    # Auto-Architecture Detection
    if args.mission == "embedded" and (args.weight_size is None or args.weight_speed is None or args.weight_energy is None):
        profiler = HardwareProfiler()
        profile = profiler.detect_profile()
        profiler.print_summary()
        
        args.weight_size = args.weight_size if args.weight_size is not None else profile.weight_size
        args.weight_speed = args.weight_speed if args.weight_speed is not None else profile.weight_speed
        args.weight_energy = args.weight_energy if args.weight_energy is not None else profile.weight_energy

    # Ensure defaults for performance mission or fallback
    args.weight_size = 0.4 if args.weight_size is None else args.weight_size
    args.weight_speed = 0.3 if args.weight_speed is None else args.weight_speed
    args.weight_energy = 0.3 if args.weight_energy is None else args.weight_energy
    
    # Normalize weights just in case
    total_w = args.weight_size + args.weight_speed + args.weight_energy
    if total_w > 0:
        args.weight_size /= total_w; args.weight_speed /= total_w; args.weight_energy /= total_w
    
    train_hrl_v8(args)
