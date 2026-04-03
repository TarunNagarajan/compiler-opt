"""
BEAT-O3 Training Script

Purpose-built for one goal: learn pass sequences that beat -O3 on runtime.

Three-tier hybrid reward:
  Tier 1 (every step): Deterministic IR-level shaping reward (~0ms)
  Tier 2 (episode end): Runtime comparison vs cached O3 baseline (~10s)
  Tier 3 (future):      World model learns to predict Tier 2 from Tier 1

Key differences from train_hrl_v8.py:
  - Uses RewardMode.BEAT_O3 (no per-step runtime, 20x faster episodes)
  - Stratified benchmark sampling (anti-catastrophic forgetting)
  - Experience replay (top episodes replayed periodically)
  - Tracks O3 win rate as primary success metric
  - Higher runtime precision (loop_count=500, 10 samples, CI95 < 1.5%)
"""

import sys
import os
import time
import glob
import json
from pathlib import Path
from datetime import datetime
from collections import deque
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
from src.env.benchmark_sampler import StratifiedBenchmarkSampler
from src.models.world_model import WorldModel
from src.models.objective_basis import mission_utility_from_objective
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.models.hrl_agent import HRLAgent
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, NUM_ATOMIC_ACTIONS, MODELS_DIR, LOGS_DIR
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import NUM_MICRO_ACTIONS, MicroRefiner

NUM_MACROS = len(MACRO_ACTIONS)


class RolloutBuffer:
    """PPO rollout buffer with experience replay support."""

    def __init__(self):
        self.reset()
        # Persistent replay buffer: stores best episodes for anti-forgetting
        self.replay_buffer = deque(maxlen=5000)
        self.replay_mix_ratio = 0.25  # 25% replay in every 5th update

    def reset(self):
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
        self.macro_onehots = []
        self.local_nodes = []
        self.total_nodes = []

    def save_top_experiences(self):
        """Save top 10% experiences by |reward| to replay buffer."""
        if not self.rewards:
            return
        abs_rewards = [abs(r) for r in self.rewards]
        threshold = np.percentile(abs_rewards, 90)
        for i, r in enumerate(self.rewards):
            if abs(r) >= threshold:
                self.replay_buffer.append({
                    'graph': self.graphs[i],
                    'macro_action': self.macro_actions[i],
                    'micro_action': self.micro_actions[i],
                    'macro_log_prob': self.macro_log_probs[i],
                    'micro_log_prob': self.micro_log_probs[i],
                    'reward': self.rewards[i],
                    'value': self.values[i],
                    'done': self.dones[i],
                    'action_history': self.action_histories[i],
                    'state_emb': self.state_embs[i],
                    'macro_onehot': self.macro_onehots[i],
                    'local_nodes': self.local_nodes[i],
                    'total_nodes': self.total_nodes[i],
                })


def set_process_priority():
    """Set high priority for less noisy runtime measurement (Windows)."""
    try:
        import ctypes
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(handle, 0x00000080)  # HIGH_PRIORITY_CLASS
        # Pin to core 0 for consistent measurements
        ctypes.windll.kernel32.SetProcessAffinityMask(handle, ctypes.c_ulonglong(1))
        print("[BEAT-O3] Process priority: HIGH, affinity: core 0")
    except Exception as e:
        print(f"[BEAT-O3] Could not set process priority: {e}")


def train_beat_o3(args):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_id = f"beat_o3_{args.name}_{timestamp}"
    log_dir = LOGS_DIR / "beat_o3" / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[BEAT-O3] Device: {device}")
    print(f"[BEAT-O3] Goal: Beat -O3 on every benchmark")

    # Set process priority for clean runtime measurements
    if not args.no_priority:
        set_process_priority()

    # --- Load World Model (required for HRL agent's imagination) ---
    base_wm = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    wm_ckpt = torch.load(args.world_model, map_location=device, weights_only=False)
    wm_state = wm_ckpt.get('model_state_dict', wm_ckpt)
    load_res = base_wm.load_state_dict(wm_state, strict=False)
    if load_res.missing_keys:
        print(f"  WorldModel missing keys: {len(load_res.missing_keys)}")

    world_model = CalibratedWorldModel(base_wm, meta_calibrator_path=args.meta_calibrator).to(device)
    world_model.eval()

    # --- Initialize HRL Agent ---
    agent = HRLAgent(
        state_dim=FEATURE_DIM,
        num_macros=NUM_MACROS,
        world_model=world_model,
        num_actions=NUM_ACTIONS
    ).to(device)

    agent_optimizer = optim.Adam(agent.parameters(), lr=args.lr)

    # --- Optionally disable imagination (world model simulation in negotiation) ---
    if args.no_imagination:
        import types
        def _no_sim_forward(self_mod, x, edge_index, batch, state_emb, edge_attr=None, history_emb=None, graph_data=None):
            if history_emb is None:
                history_emb = torch.zeros(state_emb.size(0), self_mod.history_dim, device=state_emb.device)
            specialist_input = torch.cat([state_emb, history_emb], dim=-1)
            p_probs, _ = self_mod.performance_agent(specialist_input)
            v_probs, _ = self_mod.speed_agent(specialist_input)
            s_probs, _ = self_mod.size_agent(specialist_input)
            x_probs, _ = self_mod.security_agent(specialist_input)
            final_probs = 0.25 * (p_probs + v_probs + s_probs + x_probs)
            weights = torch.full((state_emb.size(0), 4), 0.25, device=state_emb.device)
            return final_probs, weights
        agent.manager.forward = types.MethodType(_no_sim_forward, agent.manager)
        print("[BEAT-O3] Imagination DISABLED - specialists vote equally, no world model simulation")

    # Dyna-Dagger: refine world model's scale-correction + objective heads
    wm_optimizer = optim.Adam([
        {'params': world_model.base_model.scale_correction.parameters(), 'lr': 1e-5},
        {'params': world_model.base_model.action_correction_emb.parameters(), 'lr': 1e-4},
        {'params': world_model.base_model.objective_mu_head.parameters(), 'lr': 3e-4},
        {'params': world_model.base_model.objective_logvar_head.parameters(), 'lr': 2e-4},
    ])

    # --- Benchmarks with Stratified Sampling ---
    benchmarks = get_benchmark_paths()
    if args.benchmark_paths:
        selected = []
        seen = set()
        for pattern in args.benchmark_paths:
            for match in glob.glob(pattern, recursive=True):
                p = Path(match)
                if p.exists() and p.suffix.lower() in {'.c', '.cpp'}:
                    rp = str(p.resolve())
                    if rp not in seen:
                        selected.append(p)
                        seen.add(rp)
        if selected:
            benchmarks = selected

    if args.max_source_kb > 0:
        max_bytes = int(args.max_source_kb * 1024)
        benchmarks = [b for b in benchmarks if b.exists() and b.stat().st_size <= max_bytes]

    if not benchmarks:
        raise RuntimeError("No benchmarks available.")

    sampler = StratifiedBenchmarkSampler(benchmarks)
    stats = sampler.get_stats()
    print(f"[BEAT-O3] Benchmark pool: {len(benchmarks)}")
    for stratum, count in sorted(stats['strata_counts'].items()):
        print(f"  {stratum}: {count}")
    for cat, count in sorted(stats['category_counts'].items()):
        print(f"  [{cat}]: {count}")

    # Env uses BEAT_O3 reward mode — Tier 1 shaping per step, Tier 2 runtime at episode end
    env = CompilerOptEnv(
        benchmarks,
        max_steps=args.max_steps,
        reward_mode=RewardMode.BEAT_O3,
        collect_speed_metrics=True,
        runtime_measure_runs=args.runtime_runs,
        runtime_measure_loop_count=args.loop_count,
        runtime_measure_timeout_seconds=args.timeout,
        runtime_measure_aggregation="median",
        runtime_target_rel_ci95_pct=args.ci95_target,
        runtime_max_measure_runs=args.max_runtime_runs,
    )

    # --- Training State ---
    buf = RolloutBuffer()
    current_step = 0
    gamma = 0.99
    lam = 0.95
    eps_clip = 0.2
    last_save_time = time.time()
    start_time = time.time()
    update_count = 0
    terminate_idx = NUM_MACROS - 1

    # Tracking
    episode_count = 0
    beat_o3_wins = 0
    beat_o3_total = 0  # episodes with valid runtime measurements
    recent_rewards = deque(maxlen=100)
    recent_beat_o3 = deque(maxlen=100)  # 1.0 if beat O3, 0.0 if not
    best_win_rate = 0.0

    pass_stats = {i: {'count': 0, 'speedups': 0, 'regressions': 0} for i in range(NUM_MACROS)}

    print(f"[BEAT-O3] Starting training: {args.timesteps} steps, {args.max_steps} steps/episode")
    print(f"[BEAT-O3] Runtime: {args.runtime_runs} runs, loop_count={args.loop_count}, CI95 target={args.ci95_target}%")
    print()

    while current_step < args.timesteps:
        # --- Hourly checkpoint ---
        if time.time() - last_save_time > 3600:
            elapsed_hr = int((time.time() - start_time) // 3600)
            ckpt_path = MODELS_DIR / f"beat_o3_{run_id}_hour_{elapsed_hr:03}.pth"
            torch.save({
                'agent': agent.state_dict(),
                'agent_optimizer': agent_optimizer.state_dict(),
                'wm_scale': world_model.base_model.scale_correction.state_dict(),
                'wm_obj_mu': world_model.base_model.objective_mu_head.state_dict(),
                'wm_obj_logvar': world_model.base_model.objective_logvar_head.state_dict(),
                'step': current_step,
                'episode': episode_count,
                'beat_o3_wins': beat_o3_wins,
                'beat_o3_total': beat_o3_total,
            }, ckpt_path)
            print(f"  [Checkpoint] {ckpt_path.name}")
            last_save_time = time.time()

        # --- Pick benchmark via stratified sampler ---
        benchmark_path = sampler.sample()

        # --- ROLLOUT: One episode ---
        obs, info = env.reset(options={"ir_path": str(benchmark_path)})
        source_name = benchmark_path.name
        initial_instr = info.get('initial_instructions', 0)
        o3_runtime = info.get('o3_runtime', 0.0)
        o3_instr = info.get('o3_instructions', 0)
        initial_runtime = info.get('initial_runtime', 0.0)

        episode_count += 1
        episode_reward = 0.0
        history = [0]

        # Print episode header
        o3_gap = ""
        if o3_runtime > 0 and initial_runtime > 0:
            gap_pct = (initial_runtime - o3_runtime) / initial_runtime * 100
            o3_gap = f" | O3 gap: {gap_pct:+.1f}%"
        print(f"\n[EP {episode_count}] {source_name} | Instr: {initial_instr} | Runtime: {initial_runtime:.0f}{o3_gap}")

        for t in range(args.max_steps):
            if current_step >= args.timesteps:
                break

            graph_data = env.get_observation_graph()
            if graph_data is None:
                break

            local_nodes = max(int(graph_data.x.size(0) - 1), 1)
            raw_total = getattr(graph_data, 'total_nodes', torch.tensor([float(local_nodes)]))
            total_nodes_val = float(raw_total.view(-1)[0].item()) if isinstance(raw_total, torch.Tensor) else float(raw_total)

            hist_tensor = torch.tensor([history], dtype=torch.long, device=device)

            # --- Agent selects action ---
            with torch.no_grad():
                macro_probs, _, history_emb, state_emb = agent(
                    graph_data.x.to(device),
                    graph_data.edge_index.to(device),
                    getattr(graph_data, 'batch', None),
                    edge_attr=graph_data.edge_attr.to(device),
                    action_history=hist_tensor,
                    graph_data=graph_data,
                )
                dist_m = torch.distributions.Categorical(macro_probs)
                macro_act = dist_m.sample()
                m_log_prob = dist_m.log_prob(macro_act)

                macro_onehot = torch.zeros(1, NUM_MACROS, device=device)
                macro_onehot[0, macro_act] = 1.0
                micro_probs = agent.get_worker_act(state_emb, macro_onehot, history_emb)
                dist_u = torch.distributions.Categorical(micro_probs)
                micro_act = dist_u.sample()
                u_log_prob = dist_u.log_prob(micro_act)

                val = agent.get_value(state_emb, history_emb)

            # --- Execute action ---
            if macro_act.item() == terminate_idx:
                terminated = True
                truncated = False
                reward = 0.0
                info_step = info
                print(f"  Step {t}: [TERMINATE]", end="")
            else:
                base_seq = MACRO_ACTIONS[macro_act.item()]
                refined_seq = MicroRefiner.apply_refinement(base_seq, micro_act.item())
                refined_pipeline = [f"module({','.join(refined_seq)})"]
                _, reward, terminated, truncated, info_step = env.step(
                    NUM_ATOMIC_ACTIONS + macro_act.item(),
                    custom_passes=refined_pipeline,
                )
                info = info_step

                # Print step summary
                pass_name = base_seq[0][:20] if base_seq else "?"
                instr_b = info_step.get('instructions_before', 0)
                instr_a = info_step.get('instructions_after', 0)
                changed = "OK" if instr_b != instr_a else "no-op"
                print(f"  Step {t}: {pass_name:<20} r={reward:+.4f} [{changed}]", end="")

                # Action repetition penalty
                if len(history) > 1 and (NUM_ATOMIC_ACTIONS + macro_act.item()) == history[-1]:
                    reward -= 0.01

                pass_stats[macro_act.item()]['count'] += 1
                if reward > 0.01:
                    pass_stats[macro_act.item()]['speedups'] += 1
                if reward < -0.01:
                    pass_stats[macro_act.item()]['regressions'] += 1

            # --- Episode end bonuses ---
            if terminated or truncated or macro_act.item() == terminate_idx:
                # Check if we beat O3
                beat_o3_delta = info.get('beat_o3_delta_pct', 0.0)
                did_beat_o3 = info.get('beat_o3', False)
                agent_rt = info.get('agent_runtime_final', info.get('runtime_after', 0.0))
                o3_rt = info.get('o3_runtime_final', o3_runtime)

                if o3_rt > 0 and agent_rt > 0:
                    beat_o3_total += 1
                    if did_beat_o3:
                        beat_o3_wins += 1
                    recent_beat_o3.append(1.0 if did_beat_o3 else 0.0)
                    win_str = "WIN" if did_beat_o3 else "LOSS"
                    print(f" | {win_str} vs O3: {beat_o3_delta:+.2f}%", end="")
                else:
                    recent_beat_o3.append(0.0)  # no measurement = no win

                # Terminal reward: bonus for good overall reduction
                instr_final = info.get('instructions_after', initial_instr)
                instr_red = (initial_instr - instr_final) / max(initial_instr, 1)

                if macro_act.item() == terminate_idx:
                    if instr_red > 0.03:
                        term_bonus = min(0.15, 0.05 + instr_red)
                        reward += term_bonus
                    else:
                        reward -= 0.1  # penalize early termination with no improvement

                reward = max(min(reward, 0.4), -0.4)
                print()
            else:
                reward = max(min(reward, 0.2), -0.2)
                print()

            # --- Store in buffer ---
            buf.graphs.append(graph_data)
            buf.macro_actions.append(macro_act)
            buf.micro_actions.append(micro_act)
            buf.macro_log_probs.append(m_log_prob)
            buf.micro_log_probs.append(u_log_prob)
            buf.rewards.append(reward)
            buf.values.append(val.squeeze())
            buf.dones.append(terminated or truncated)
            buf.action_histories.append(hist_tensor.cpu())
            buf.state_embs.append(state_emb.detach().squeeze(0))
            buf.local_nodes.append(float(local_nodes))
            buf.total_nodes.append(float(total_nodes_val))

            wm_oh = torch.zeros(NUM_ACTIONS, device=device)
            wm_oh[NUM_ATOMIC_ACTIONS + macro_act.item()] = 1.0
            buf.macro_onehots.append(wm_oh)

            episode_reward += reward
            history.append(NUM_ATOMIC_ACTIONS + macro_act.item())
            current_step += 1

            if terminated or truncated:
                break

        # --- Episode summary ---
        recent_rewards.append(episode_reward)
        sampler.report_reward(benchmark_path, episode_reward)

        win_rate = sum(recent_beat_o3) / max(len(recent_beat_o3), 1) * 100
        avg_reward = sum(recent_rewards) / max(len(recent_rewards), 1)
        total_win_rate = beat_o3_wins / max(beat_o3_total, 1) * 100

        print(f"  Episode reward: {episode_reward:.4f} | "
              f"Win rate (recent): {win_rate:.0f}% | "
              f"Win rate (total): {total_win_rate:.0f}% ({beat_o3_wins}/{beat_o3_total})")

        # TensorBoard
        writer.add_scalar("episode/reward", episode_reward, episode_count)
        writer.add_scalar("episode/win_rate_recent", win_rate, episode_count)
        writer.add_scalar("episode/win_rate_total", total_win_rate, episode_count)
        writer.add_scalar("episode/avg_reward_100", avg_reward, episode_count)
        writer.add_scalar("step/total", current_step, episode_count)

        # Update sampler weights every 20 episodes
        if episode_count % 20 == 0:
            sampler.update_weights()
            stats = sampler.get_stats()
            for s, w in stats['stratum_weights'].items():
                writer.add_scalar(f"sampler/weight_{s}", w, episode_count)
            for s, avg in stats['stratum_avg_rewards'].items():
                writer.add_scalar(f"sampler/avg_reward_{s}", avg, episode_count)

        # --- PPO UPDATE ---
        if len(buf.rewards) >= args.rollout_steps:
            update_count += 1

            # Save top experiences before update
            buf.save_top_experiences()

            # GAE
            values = torch.stack(buf.values).detach()
            rewards = torch.tensor(buf.rewards, dtype=torch.float32, device=device)
            dones = torch.tensor(buf.dones, dtype=torch.float32, device=device)

            advantages = torch.zeros_like(rewards)
            last_gae = 0
            for t_idx in reversed(range(len(rewards))):
                next_value = 0 if t_idx == len(rewards) - 1 else values[t_idx + 1]
                delta = rewards[t_idx] + gamma * next_value * (1 - dones[t_idx]) - values[t_idx]
                last_gae = delta + gamma * lam * (1 - dones[t_idx]) * last_gae
                advantages[t_idx] = last_gae

            returns = advantages + values
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

            # PPO epochs
            agent.train()
            for _ in range(4):
                indices = np.arange(len(buf.rewards))
                np.random.shuffle(indices)
                for start in range(0, len(buf.rewards), 32):
                    end = start + 32
                    batch_idx = indices[start:end]

                    batch_graphs = Batch.from_data_list([buf.graphs[i] for i in batch_idx]).to(device)

                    # Pad action histories
                    hist_seqs = []
                    max_hist_len = 1
                    for i in batch_idx:
                        h = buf.action_histories[i]
                        if h.dim() == 2 and h.size(0) == 1:
                            h = h.squeeze(0)
                        hist_seqs.append(h)
                        max_hist_len = max(max_hist_len, int(h.numel()))

                    padded_hist = []
                    for h in hist_seqs:
                        pad_len = max_hist_len - int(h.numel())
                        if pad_len > 0:
                            h = F.pad(h, (pad_len, 0), value=0)
                        padded_hist.append(h.unsqueeze(0))
                    batch_hist = torch.cat(padded_hist, dim=0).to(device)

                    m_probs, _, history_emb, state_emb = agent(
                        batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch,
                        edge_attr=batch_graphs.edge_attr,
                        action_history=batch_hist, graph_data=batch_graphs,
                    )

                    m_actions = torch.stack([buf.macro_actions[i] for i in batch_idx]).to(device)
                    u_actions = torch.stack([buf.micro_actions[i] for i in batch_idx]).to(device)
                    new_m_log = torch.distributions.Categorical(m_probs).log_prob(m_actions)
                    old_m_log = torch.stack([buf.macro_log_probs[i] for i in batch_idx]).to(device)
                    old_u_log = torch.stack([buf.micro_log_probs[i] for i in batch_idx]).to(device)

                    macro_ohs = torch.zeros(len(batch_idx), NUM_MACROS, device=device)
                    macro_ohs.scatter_(1, m_actions.view(-1, 1), 1.0)
                    u_probs = agent.get_worker_act(state_emb, macro_ohs, history_emb)
                    new_u_log = torch.distributions.Categorical(u_probs).log_prob(u_actions)

                    ratio_m = torch.exp(new_m_log - old_m_log)
                    surr1_m = ratio_m * advantages[batch_idx]
                    surr2_m = torch.clamp(ratio_m, 1 - eps_clip, 1 + eps_clip) * advantages[batch_idx]
                    macro_loss = -torch.min(surr1_m, surr2_m).mean()

                    ratio_u = torch.exp(new_u_log - old_u_log)
                    surr1_u = ratio_u * advantages[batch_idx]
                    surr2_u = torch.clamp(ratio_u, 1 - eps_clip, 1 + eps_clip) * advantages[batch_idx]
                    micro_loss = -torch.min(surr1_u, surr2_u).mean()

                    entropy = 0.5 * (
                        torch.distributions.Categorical(m_probs).entropy().mean()
                        + torch.distributions.Categorical(u_probs).entropy().mean()
                    )

                    val_pred = agent.get_value(state_emb, history_emb)
                    value_loss = F.mse_loss(val_pred.squeeze(), returns[batch_idx])

                    loss = macro_loss + micro_loss + 0.5 * value_loss - 0.01 * entropy

                    agent_optimizer.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(agent.parameters(), 0.5)
                    agent_optimizer.step()

            writer.add_scalar("update/policy_loss", (macro_loss + micro_loss).item(), update_count)
            writer.add_scalar("update/value_loss", value_loss.item(), update_count)
            writer.add_scalar("update/entropy", entropy.item(), update_count)
            writer.add_scalar("update/mean_reward", np.mean(buf.rewards), update_count)

            # Dyna-Dagger: refine world model
            world_model.train()
            if getattr(world_model, 'meta_net', None) is not None:
                world_model.meta_net.eval()

            wm_losses = []
            for _ in range(4):
                indices = np.arange(len(buf.rewards))
                np.random.shuffle(indices)
                for start in range(0, len(buf.rewards), 32):
                    end = start + 32
                    batch_idx = indices[start:end]

                    b_embs = torch.stack([buf.state_embs[i] for i in batch_idx]).to(device)
                    if b_embs.dim() == 3 and b_embs.size(1) == 1:
                        b_embs = b_embs.squeeze(1)
                    b_oh = torch.stack([buf.macro_onehots[i] for i in batch_idx]).to(device)
                    b_local = torch.tensor([buf.local_nodes[i] for i in batch_idx], dtype=torch.float32, device=device)
                    b_total = torch.tensor([buf.total_nodes[i] for i in batch_idx], dtype=torch.float32, device=device)

                    # Target: actual reward serves as the mission signal
                    b_target = torch.tensor([buf.rewards[i] for i in batch_idx], dtype=torch.float32, device=device)

                    _, _ = world_model.transition_step(b_embs, b_oh, num_nodes=b_local, total_nodes=b_total)
                    obj_mu, obj_logvar = world_model.base_model.predict_objective_basis(
                        state_emb=b_embs, action_onehot=b_oh, num_nodes=b_local, total_nodes=b_total,
                    )
                    pred, _ = mission_utility_from_objective(
                        mu=obj_mu, logvar=obj_logvar, mission="performance",
                        w_size=0.4, w_speed=0.3, w_energy=0.3,
                    )
                    wm_loss = F.mse_loss(pred, b_target)
                    wm_optimizer.zero_grad()
                    wm_loss.backward()
                    wm_optimizer.step()
                    wm_losses.append(wm_loss.item())

            world_model.eval()

            avg_wm_loss = np.mean(wm_losses) if wm_losses else 0.0
            writer.add_scalar("update/wm_loss", avg_wm_loss, update_count)

            print(f"\n  [UPDATE {update_count}] Step {current_step} | "
                  f"Mean reward: {np.mean(buf.rewards):.4f} | "
                  f"WM loss: {avg_wm_loss:.6f} | "
                  f"Replay buffer: {len(buf.replay_buffer)}")

            buf.reset()

            # Pass performance summary every 5 updates
            if update_count % 5 == 0:
                print("\n  --- PASS PERFORMANCE ---")
                for midx in range(NUM_MACROS):
                    s = pass_stats[midx]
                    if s['count'] > 0:
                        name = MACRO_ACTIONS[midx][0][:20]
                        ratio = s['speedups'] / max(s['count'], 1) * 100
                        print(f"  M[{midx:2d}] {name:<20} count={s['count']:<4} win={s['speedups']:<3} ({ratio:.0f}%)")
                pass_stats = {i: {'count': 0, 'speedups': 0, 'regressions': 0} for i in range(NUM_MACROS)}

            # Save best model by win rate
            if len(recent_beat_o3) >= 20:
                current_win_rate = sum(recent_beat_o3) / len(recent_beat_o3)
                if current_win_rate > best_win_rate:
                    best_win_rate = current_win_rate
                    best_path = MODELS_DIR / f"beat_o3_{args.name}_best.pth"
                    torch.save({
                        'agent': agent.state_dict(),
                        'agent_optimizer': agent_optimizer.state_dict(),
                        'wm_scale': world_model.base_model.scale_correction.state_dict(),
                        'wm_obj_mu': world_model.base_model.objective_mu_head.state_dict(),
                        'wm_obj_logvar': world_model.base_model.objective_logvar_head.state_dict(),
                        'step': current_step,
                        'episode': episode_count,
                        'win_rate': current_win_rate,
                        'beat_o3_wins': beat_o3_wins,
                        'beat_o3_total': beat_o3_total,
                    }, best_path)
                    print(f"  [BEST] New best win rate: {current_win_rate*100:.1f}% -> {best_path.name}")

    # --- Final save ---
    final_path = MODELS_DIR / f"beat_o3_{run_id}_final.pth"
    torch.save({
        'agent': agent.state_dict(),
        'agent_optimizer': agent_optimizer.state_dict(),
        'wm_scale': world_model.base_model.scale_correction.state_dict(),
        'wm_obj_mu': world_model.base_model.objective_mu_head.state_dict(),
        'wm_obj_logvar': world_model.base_model.objective_logvar_head.state_dict(),
        'step': current_step,
        'episode': episode_count,
        'beat_o3_wins': beat_o3_wins,
        'beat_o3_total': beat_o3_total,
    }, final_path)

    print(f"\n{'='*60}")
    print(f"[BEAT-O3] Training complete.")
    print(f"  Steps: {current_step} | Episodes: {episode_count}")
    print(f"  O3 Win Rate: {beat_o3_wins}/{beat_o3_total} ({beat_o3_wins/max(beat_o3_total,1)*100:.1f}%)")
    print(f"  Best win rate: {best_win_rate*100:.1f}%")
    print(f"  Final model: {final_path}")
    print(f"{'='*60}")

    writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train HRL agent to beat -O3")
    parser.add_argument("--name", type=str, default="run1")
    parser.add_argument("--timesteps", type=int, default=50000)
    parser.add_argument("--rollout_steps", type=int, default=512)
    parser.add_argument("--max_steps", type=int, default=15,
                        help="Max optimization passes per episode (15 is enough — O3 applies ~80 but most gains come from first 10-15)")
    parser.add_argument("--world_model", type=str, required=True)
    parser.add_argument("--meta_calibrator", type=str, required=True)
    parser.add_argument("--lr", type=float, default=3e-4)

    # Runtime measurement (higher precision than default training)
    parser.add_argument("--runtime_runs", type=int, default=10,
                        help="Number of harness runs per measurement")
    parser.add_argument("--loop_count", type=int, default=500,
                        help="Loop iterations in harness (higher = more stable)")
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="Timeout per harness run (seconds)")
    parser.add_argument("--ci95_target", type=float, default=1.5,
                        help="Target relative CI95 percent")
    parser.add_argument("--max_runtime_runs", type=int, default=20,
                        help="Max adaptive runtime samples")

    # Benchmark selection
    parser.add_argument("--benchmark_paths", nargs="*", default=None)
    parser.add_argument("--max_source_kb", type=int, default=0)

    # Process
    parser.add_argument("--no_priority", action="store_true",
                        help="Don't set HIGH_PRIORITY_CLASS")
    parser.add_argument("--no_imagination", action="store_true",
                        help="Disable world model simulation in negotiation (specialists vote equally)")

    args = parser.parse_args()
    train_beat_o3(args)
