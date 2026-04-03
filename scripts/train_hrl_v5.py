"""
v5 HRL Agent Training Script

Uses HierarchicalMultiAgentV5 with:
- GRU pass history encoder (full episode memory)
- v5 GNN encoder (attention pooling + 7 relations including loop back-edges)

Usage:
  # From scratch:
  uv run python scripts/train_hrl_v5.py --name v5_fresh --world_model models/world_model_v5.pth --timesteps 100000
  
  # Warm-start from v4 HRL checkpoint:
  uv run python scripts/train_hrl_v5.py --name v5_warmstart --world_model models/world_model_v5.pth --warmstart_v4 models/hrl_industrial_final.pth --timesteps 100000
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
from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, MODELS_DIR, LOGS_DIR
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner, NUM_MICRO_ACTIONS

NUM_MACROS = len(MACRO_ACTIONS)


class MAPPOBuffer:
    def __init__(self, size):
        self.graphs = []; self.macro_actions = []; self.micro_actions = []
        self.macro_log_probs = []; self.micro_log_probs = []
        self.rewards = []; self.values = []; self.dones = []
        self.action_histories = []  # NEW v5: track full episode action history
        self.size = size

    def reset(self):
        self.graphs = []; self.macro_actions = []; self.micro_actions = []
        self.macro_log_probs = []; self.micro_log_probs = []
        self.rewards = []; self.values = []; self.dones = []
        self.action_histories = []


def train_hrl_v5(args):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_id = f"{args.name}_{timestamp}"
    log_dir = LOGS_DIR / "hrl" / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(log_dir=str(log_dir))
    
    benchmarks = get_benchmark_paths()
    
    num_new = sum(1 for b in [str(p) for p in benchmarks] if any(cat in str(b) for cat in ['multi_func', 'deep_call_chain', 'library_heavy', 'scaled_composite', 'anghaben_wrapped']))
    print(f"[HRL-v5] Found {len(benchmarks)} total benchmarks, including {num_new} from new v5 categories.")

    # === STRATIFIED BENCHMARK SAMPLING ===
    # Group benchmarks by category for balanced training
    benchmark_categories = {}
    for b in benchmarks:
        # Extract category from path (e.g., 'recursive', 'pointer_chase', 'linear-algebra')
        parts = b.relative_to(b.parents[1]).parts if len(b.parts) > 2 else (b.parent.name,)
        cat = parts[0] if parts else 'unknown'
        benchmark_categories.setdefault(cat, []).append(b)
    
    # Sample equally from each category
    max_per_cat = max(50, 1500 // max(len(benchmark_categories), 1))
    train_benchmarks = []
    for cat, cat_benchmarks in benchmark_categories.items():
        sampled = random.sample(cat_benchmarks, min(len(cat_benchmarks), max_per_cat))
        train_benchmarks.extend(sampled)
    random.shuffle(train_benchmarks)
    print(f"[HRL-v5] Stratified sampling: {len(train_benchmarks)} benchmarks from {len(benchmark_categories)} categories")
    MAX_STEPS = 25
    env = CompilerOptEnv(train_benchmarks, max_steps=MAX_STEPS, reward_mode=RewardMode.SPEED)
    
    # ===== v5 AGENT =====
    agent = create_hrl_agent_v5(
        state_dim=FEATURE_DIM,
        num_macros=NUM_MACROS,
        world_model_path=args.world_model,
        gnn_layers=args.gnn_layers,
        v4_checkpoint_path=args.warmstart_v4,
        num_actions=NUM_ACTIONS  # Must match world model's action_dim
    )
    
    current_step = 0
    if args.checkpoint and Path(args.checkpoint).exists():
        print(f"[HRL-v5] Resuming from v5 checkpoint: {args.checkpoint}")
        ckpt = torch.load(args.checkpoint, weights_only=False)
        if isinstance(ckpt, dict) and 'model_state_dict' in ckpt:
            agent.load_state_dict(ckpt['model_state_dict'])
            current_step = ckpt.get('current_step', 0)
            print(f"[HRL-v5] Resumed at step {current_step} (entropy coeff: {max(0.003, 0.03 * (1.0 - current_step / args.timesteps)):.4f})")
        else:
            # Legacy checkpoint: just model weights, no step info
            agent.load_state_dict(ckpt)
            current_step = 0
            print(f"[HRL-v5] Legacy checkpoint loaded (no step info, starting from step 0)")
    
    total_params = sum(p.numel() for p in agent.parameters())
    print(f"[HRL-v5] Agent: {total_params:,} parameters")
    # ====================
    
    optimizer = optim.Adam(agent.parameters(), lr=args.lr)
    
    ppo_epochs = 10; eps_clip = 0.2; last_save_time = time.time()
    
    PATIENCE = 8
    MIN_IMPROVE = 0.05  # Raised to 5% to match environment noise floor
    PER_STEP_COST = -0.0025
    REPEAT_PENALTY = -0.01  # Penalty for repeating the same macro action
    CORRECTNESS_PENALTY = -5.0
    
    pass_stats = {i: {'count': 0, 'crashes': 0, 'regressions': 0, 'speedups': 0} for i in range(NUM_MACROS)}
    
    print(f"[HRL-v5] Launching v5 Training: {run_id}")
    
    csv_path = LOGS_DIR / f"optimization_log_v5_{timestamp}.csv"
    with open(csv_path, 'w', newline='') as f:
        writer_csv = csv.writer(f)
        writer_csv.writerow(['Step', 'Program', 'Macro_Action_ID', 'Macro_Name', 'Micro_Action_ID', 'Reward', 'Value', 'Num_Instr_Before', 'Num_Instr_After'])
        
    while current_step < args.timesteps:
        buffer = MAPPOBuffer(args.rollout_steps)
        episode_lengths = [] 
        
        while len(buffer.rewards) < args.rollout_steps:
            obs, info = env.reset()
            graph = env.get_observation_graph()
            source_file = getattr(env, 'current_benchmark_path', 'unknown')
            print(f"\n[EPISODE] Source: {Path(source_file).name} | IR: {Path(info['ir_path']).name}", flush=True)
            
            initial_runtime = env.metrics.measure_runtime(env.original_ir_path, iterations=20) if getattr(env, 'original_ir_path', None) else float('inf')
            initial_instructions = env.metrics.count_instructions(env.original_ir_path) if getattr(env, 'original_ir_path', None) else 999
            o3_runtime = getattr(env, 'o3_runtime', 0.0)
            if o3_runtime > 0 and initial_runtime > 0:
                o3_gap = (initial_runtime - o3_runtime) / initial_runtime * 100
                print(f"  Baseline: {initial_runtime:.1f}ms | O3: {o3_runtime:.1f}ms | Gap to beat: {o3_gap:.1f}%", flush=True)
            elif initial_runtime <= 0:
                print(f"  [SKIP] Baseline measurement failed (runtime=0.0). Skipping benchmark.", flush=True)
                continue
            
            env.prev_runtime = initial_runtime
            
            terminated = False
            episode_steps = 0
            last_improve_step = 0
            recent_macros = []
            episode_action_history = []  # NEW v5: track all actions this episode
            best_runtime = initial_runtime  # Track best runtime seen during episode
            best_instructions = initial_instructions  # Track best instruction count
            prev_instructions = initial_instructions  # Track per-step instruction count
            
            while not terminated and len(buffer.rewards) < args.rollout_steps:
                termination_msg = ""
                x = graph.x; edge_index = graph.edge_index; edge_attr = getattr(graph, 'edge_attr', None)
                batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                # NEW v5: Attach action history to graph for GRU (with fixed-length padding for batching)
                padded_history = torch.zeros(1, MAX_STEPS, dtype=torch.long)
                if episode_action_history:
                    seq = torch.tensor(episode_action_history, dtype=torch.long)
                    if len(seq) > MAX_STEPS: seq = seq[-MAX_STEPS:] 
                    padded_history[0, :len(seq)] = seq
                
                # Double-check shape to prevent batching crashes
                if padded_history.shape != (1, MAX_STEPS):
                    padded_history = padded_history.view(1, MAX_STEPS)
                graph.action_history = padded_history
                
                with torch.no_grad():
                    macro_probs, agent_weights = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
                    
                    # Action throttling (same as v4)
                    if len(recent_macros) >= 2:
                        last_2 = recent_macros[-2:]
                        if all(m == last_2[0] for m in last_2):
                            macro_probs[0, last_2[0]] *= 0.1
                        if len(recent_macros) >= 3:
                            last_3 = recent_macros[-3:]
                            if all(m == last_3[0] for m in last_3):
                                macro_probs[0, last_3[0]] = 0.0
                    
                    macro_probs = macro_probs / (macro_probs.sum() + 1e-8)
                    
                    val = agent.get_value(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
                    m_idx = torch.distributions.Categorical(macro_probs).sample()
                    
                    recent_macros.append(m_idx.item())
                    if len(recent_macros) > 5: recent_macros.pop(0)
                    
                    terminate_idx = len(MACRO_ACTIONS) - 1
                    
                    if m_idx.item() == terminate_idx and episode_steps == 0:
                        macro_probs_clone = macro_probs.clone()
                        macro_probs_clone[0, terminate_idx] = 0.0
                        m_idx = torch.distributions.Categorical(macro_probs_clone / macro_probs_clone.sum()).sample()
                        
                    if m_idx.item() == terminate_idx:
                        current_instructions = env.metrics.count_instructions(env.current_ir_path) if env.current_ir_path else 0
                        
                        is_correct = True
                        if env.original_ir_path and env.current_ir_path:
                            correctness = env.metrics.verify_correctness(env.original_ir_path, env.current_ir_path)
                            if not correctness.is_correct:
                                is_correct = False
                                
                        if not is_correct:
                            print(f"  Step {current_step}: STOP (CORRECTNESS VIOLATION). Penalty: {CORRECTNESS_PENALTY}", flush=True)
                            final_reward = CORRECTNESS_PENALTY
                        elif env.prev_runtime <= 0.001 and current_instructions < (initial_instructions * 0.1):
                            print(f"  Step {current_step}: STOP (DELETED CODE/CHEATING). Penalty: -2.0", flush=True)
                            final_reward = -2.0
                        else:
                            # Adaptive composite for STOP decision: Did the episode improve over the INITIAL baseline?
                            instr_improvement = (initial_instructions - best_instructions) / max(initial_instructions, 1)
                            runtime_improvement = (initial_runtime - best_runtime) / max(initial_runtime, 1e-6) if best_runtime > 0 and initial_runtime > 0 else 0
                            
                            # Trust runtime when clear, blend when ambiguous
                            if abs(runtime_improvement) > 0.05:
                                composite_improvement = runtime_improvement
                                mode_tag = 'RT'
                            else:
                                composite_improvement = 0.7 * runtime_improvement + 0.3 * instr_improvement
                                mode_tag = 'BLEND'
                            
                            if composite_improvement > 0.03:  # 3% threshold for STOP (lower = encourages stopping)
                                efficiency_bonus = 0.02 * max(0, (MAX_STEPS - episode_steps) / MAX_STEPS)
                                final_reward = min(0.2, 0.05 + composite_improvement + efficiency_bonus)
                                beat_o3 = best_runtime < o3_runtime if o3_runtime > 0 and best_runtime > 0 else False
                                o3_tag = ' BEAT-O3' if beat_o3 else ''
                                print(f"  Step {current_step}: STOP ({mode_tag} {composite_improvement*100:.1f}% | rt:{runtime_improvement*100:+.1f}% instr:{instr_improvement*100:+.1f}%). Reward: +{final_reward:.4f} (eff: +{efficiency_bonus:.4f}) [{initial_runtime:.1f}ms->{best_runtime:.1f}ms, O3:{o3_runtime:.1f}ms]{o3_tag}", flush=True)
                            else:
                                print(f"  Step {current_step}: STOP (Premature/Slower). Penalty: -0.1", flush=True)
                                final_reward = -0.1
                            
                        if episode_steps > 0:
                            episode_lengths.append(episode_steps)
                            
                        buffer.rewards.append(final_reward)
                        buffer.graphs.append(graph); buffer.macro_actions.append(m_idx.squeeze())
                        buffer.micro_actions.append(torch.tensor(0)) 
                        buffer.macro_log_probs.append(torch.distributions.Categorical(macro_probs).log_prob(m_idx).squeeze())
                        buffer.micro_log_probs.append(torch.tensor(0.0).squeeze())
                        buffer.values.append(val.item()); buffer.dones.append(True)
                        
                        with open(csv_path, 'a', newline='') as f:
                            csv.writer(f).writerow([
                                current_step, Path(env.current_ir_path).name if env.current_ir_path else "unknown",
                                m_idx.item(), "TERMINATE", 0, round(final_reward, 4), round(val.item(), 4),
                                env.prev_runtime, env.prev_runtime
                            ])
                        
                        current_step += 1
                        terminated = True
                        break

                    u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
                    u_idx = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).sample()
                
                # NEW v5: Record action in episode history
                episode_action_history.append(m_idx.item() + 1)  # +1 because 0 is padding
                
                # === ACTION REPETITION PENALTY ===
                # Penalize the agent for picking the same macro as the previous step
                repeat_penalty = 0.0
                if len(recent_macros) >= 2 and recent_macros[-1] == recent_macros[-2]:
                    repeat_penalty = REPEAT_PENALTY
                
                base_seq = MACRO_ACTIONS[m_idx.item()]
                final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                pipeline = ["module({})".format(",".join(final_seq))]
                
                print(f"  Step {current_step}: M[{m_idx.item()}] U[{u_idx.item()}]...", end="", flush=True)
                
                # Use environment's step function directly, passing our dynamically refined pipeline
                action_idx = m_idx.item() + env.num_atomic_passes
                obs, reward, terminated, truncated, info = env.step(action_idx, custom_passes=pipeline)
                
                pass_stats[m_idx.item()]['count'] += 1
                
                if info.get('error'):
                    print(" [FAIL] End Episode.", flush=True)
                    pass_stats[m_idx.item()]['crashes'] += 1
                    reward = -0.2
                    terminated = True
                else:
                    reward = max(min(reward, 0.2), -1.0)
                    if reward <= -0.2:  # Safe shutoff for heavy regressions or metric timeouts
                        print(" [CORRUPT]", flush=True)
                        reward = -0.2
                        terminated = True
                        termination_msg = f"  Step {current_step}: [HEAVY REGRESSION] Episode terminated for safety (+20% slowdown)."
                    else:
                        print(f" [OK] Reward: {reward:.4f}", flush=True)
                        if reward < -0.01:
                            pass_stats[m_idx.item()]['regressions'] += 1
                        elif reward > 0.01:
                            pass_stats[m_idx.item()]['speedups'] += 1
                            last_improve_step = episode_steps
                        
                        # Periodically verify correctness (expensive, so not every step)
                        if current_step % 10 == 0 and env.original_ir_path:
                            correctness = env.metrics.verify_correctness(env.original_ir_path, env.current_ir_path)
                            if not correctness.is_correct:
                                reward = CORRECTNESS_PENALTY
                                terminated = True
                                print(" [CORRECTNESS VIOLATION]", flush=True)
                
                # Apply action repetition penalty if chosen SAME macro twice
                reward += repeat_penalty
                
                # Update best state tracking for episode termination logic
                current_instr = info.get('instructions_after', 999)
                if current_instr < best_instructions:
                    best_instructions = current_instr
                runtime_after = info.get('runtime_after', 0.0)
                if runtime_after > 0 and runtime_after < best_runtime:
                    best_runtime = runtime_after

                # Handle Termination Reason Printing
                # Note: termination_msg might already be set by regression/error checks above
                
                # Case 1: Environment-level termination (usually max_steps)
                if terminated and not termination_msg:
                    if info.get('error'):
                        termination_msg = f"  Step {current_step}: [FAIL] Environment Error: {info['error']}"
                    else:
                        runtime_improvement = (initial_runtime - best_runtime) / max(initial_runtime, 1e-6) if best_runtime > 0 and initial_runtime > 0 else 0
                        beat_o3 = best_runtime < o3_runtime if o3_runtime > 0 and best_runtime > 0 else False
                        o3_tag = ' BEAT-O3' if beat_o3 else ''
                        
                        if runtime_improvement > 0.03:
                            termination_msg = f"  ENV-LIMIT (max_steps). rt:{runtime_improvement*100:+.1f}% [{initial_runtime:.1f}ms->{best_runtime:.1f}ms, O3:{o3_runtime:.1f}ms]{o3_tag}"
                        else:
                            termination_msg = f"  ENV-LIMIT (max_steps). No significant improvement. [{initial_runtime:.1f}ms->{best_runtime:.1f}ms]"

                buffer.graphs.append(graph); buffer.macro_actions.append(m_idx.squeeze()); buffer.micro_actions.append(u_idx.squeeze())
                buffer.macro_log_probs.append(torch.distributions.Categorical(macro_probs).log_prob(m_idx).squeeze())
                buffer.micro_log_probs.append(torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).log_prob(u_idx).squeeze())
                buffer.rewards.append(reward); buffer.values.append(val.item()); buffer.dones.append(terminated)
                
                source_name = Path(getattr(env, 'current_benchmark_path', 'unknown')).name
                
                runtime_b = info.get('runtime_before', env.prev_runtime) if 'info' in locals() else env.prev_runtime
                runtime_a = info.get('runtime_after', 0.0) if 'info' in locals() else 0.0
                
                with open(csv_path, 'a', newline='') as f:
                    csv.writer(f).writerow([
                        current_step, source_name,
                        m_idx.item(), MACRO_ACTIONS[m_idx.item()][0] if m_idx.item() < len(MACRO_ACTIONS) else "M", 
                        u_idx.item(), round(reward, 4), round(val.item(), 4),
                        runtime_b, runtime_a
                    ])
                current_step += 1
                episode_steps += 1
                
                # Patience Check (Script-side termination)
                if not terminated and (episode_steps - last_improve_step >= PATIENCE):
                    terminated = True
                    is_correct = True
                    if env.original_ir_path and env.current_ir_path:
                        correctness = env.metrics.verify_correctness(env.original_ir_path, env.current_ir_path)
                        if not correctness.is_correct:
                            is_correct = False
                    
                    if not is_correct:
                        final_reward = CORRECTNESS_PENALTY
                        termination_msg = f"  Step {current_step}: PATIENCE (CORRECTNESS VIOLATION). Penalty: {CORRECTNESS_PENALTY}"
                    else:
                        final_reward = -0.15
                        runtime_improvement = (initial_runtime - best_runtime) / max(initial_runtime, 1e-6) if best_runtime > 0 else 0
                        beat_o3 = best_runtime < o3_runtime if o3_runtime > 0 and best_runtime > 0 else False
                        o3_tag = ' BEAT-O3' if beat_o3 else ''
                        termination_msg = f"  Step {current_step}: PATIENCE (Stalled). Penalty: -0.15 | rt:{runtime_improvement*100:+.1f}% [{initial_runtime:.1f}ms->{best_runtime:.1f}ms, O3:{o3_runtime:.1f}ms]{o3_tag}"
                    
                    buffer.rewards[-1] = final_reward

                # Step limit Check (Script-side termination)
                if not terminated and env.current_step >= env.max_steps:
                    terminated = True
                    is_correct = True
                    if env.original_ir_path and env.current_ir_path:
                        correctness = env.metrics.verify_correctness(env.original_ir_path, env.current_ir_path)
                        if not correctness.is_correct:
                            is_correct = False
                    
                    if not is_correct:
                        final_reward = CORRECTNESS_PENALTY
                    else:
                        # Adaptive composite improvement
                        instr_improvement = (initial_instructions - best_instructions) / max(initial_instructions, 1)
                        runtime_improvement = (initial_runtime - best_runtime) / max(initial_runtime, 1e-6) if best_runtime > 0 else 0
                        
                        if abs(runtime_improvement) > 0.05:
                            composite_improvement = runtime_improvement
                            mode_tag = 'RT'
                        else:
                            composite_improvement = 0.7 * runtime_improvement + 0.3 * instr_improvement
                            mode_tag = 'BLEND'
                        
                        if composite_improvement > 0.05:  # 5% threshold
                            final_reward = min(0.2, 0.05 + composite_improvement)
                            beat_o3 = best_runtime < o3_runtime if o3_runtime > 0 and best_runtime > 0 else False
                            o3_tag = ' BEAT-O3' if beat_o3 else ''
                            termination_msg = f"  Step {current_step}: LIMIT ({mode_tag} {composite_improvement*100:.1f}% | rt:{runtime_improvement*100:+.1f}% instr:{instr_improvement*100:+.1f}%). Reward: +{final_reward:.4f} [{initial_runtime:.1f}ms->{best_runtime:.1f}ms, O3:{o3_runtime:.1f}ms]{o3_tag}"
                        else:
                            final_reward = -0.1
                            termination_msg = f"  Step {current_step}: LIMIT (Budget exhausted). Penalty: -0.1"
                    
                    buffer.rewards[-1] = final_reward
                
                # Check if we hit the PPO rollout limit mid-episode
                if not terminated and len(buffer.rewards) >= args.rollout_steps:
                    termination_msg = f"  Step {current_step}: [ROLLOUT BUFFER FULL] Truncating episode prematurely for PPO update."
                
                # Final Print if we have a termination message
                if termination_msg:
                    print(f"\n{termination_msg}", flush=True)
                
                graph = env.get_observation_graph()
                
                writer.add_scalar("Live/Reward", reward, current_step)
                if current_step % 10 == 0: writer.flush()
                
                if current_step % 500 == 0:
                    print("\n--- PER-PASS PERFORMANCE (Last 500 steps) ---")
                    for midx in range(NUM_MACROS):
                        s = pass_stats[midx]
                        if s['count'] > 0:
                            print(f"Pass {midx:<2} ({MACRO_ACTIONS[midx][0][:15]}): Count: {s['count']:<3} | Speedups: {s['speedups']:<3} | Crashes: {s['crashes']:<3} | Regressions: {s['regressions']:<3}")
                    pass_stats = {i: {'count': 0, 'crashes': 0, 'regressions': 0, 'speedups': 0} for i in range(NUM_MACROS)}

        # PPO update
        gamma = 0.99; lam = 0.90
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
        if len(advantages) > 1: advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        old_m_log = torch.stack(buffer.macro_log_probs).detach()
        old_u_log = torch.stack(buffer.micro_log_probs).detach()

        opt_batch_size = 32
        for _ in range(ppo_epochs):
            indices = np.arange(len(buffer.rewards))
            np.random.shuffle(indices)
            for start in range(0, len(buffer.rewards), opt_batch_size):
                end = start + opt_batch_size
                batch_idx = indices[start:end]
                batch_graphs = Batch.from_data_list([buffer.graphs[i] for i in batch_idx])
                batch_edge_attr = getattr(batch_graphs, 'edge_attr', None)
                
                # PASS graph_data=batch_graphs to ensure the update isn't history-blind!
                m_probs, _ = agent.get_macro_action(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, edge_attr=batch_edge_attr, graph_data=batch_graphs)
                val = agent.get_value(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, edge_attr=batch_edge_attr, graph_data=batch_graphs)
                
                m_actions = torch.stack([buffer.macro_actions[i] for i in batch_idx])
                new_m_log = torch.distributions.Categorical(m_probs).log_prob(m_actions)
                
                u_logits = agent.get_micro_action(batch_graphs.x, batch_graphs.edge_index, batch_graphs.batch, m_actions, edge_attr=batch_edge_attr, graph_data=batch_graphs)
                u_actions = torch.stack([buffer.micro_actions[i] for i in batch_idx])
                new_u_log = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).log_prob(u_actions)
                
                ratio_m = torch.exp(new_m_log - old_m_log[batch_idx])
                ratio_u = torch.exp(new_u_log - old_u_log[batch_idx])
                
                # Advantages are already normalized globally before the epoch loop
                adv_batch = advantages[batch_idx]
                
                surr1_m = ratio_m * adv_batch; surr2_m = torch.clamp(ratio_m, 1-eps_clip, 1+eps_clip) * adv_batch
                surr1_u = ratio_u * adv_batch; surr2_u = torch.clamp(ratio_u, 1-eps_clip, 1+eps_clip) * adv_batch
                m_entropy = torch.distributions.Categorical(m_probs).entropy().mean()
                u_entropy = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).entropy().mean()
                # === ENTROPY ANNEALING ===
                # Start high (0.03) to encourage exploration, decay to 0.003 for policy sharpening
                entropy_coeff = max(0.003, 0.03 * (1.0 - current_step / args.timesteps))
                entropy_bonus = entropy_coeff * (m_entropy + u_entropy)
                policy_loss = -torch.min(surr1_m, surr2_m).mean() - torch.min(surr1_u, surr2_u).mean()
                value_loss = 0.5 * F.mse_loss(val.squeeze(), returns[batch_idx])
                loss = policy_loss + value_loss - entropy_bonus
                optimizer.zero_grad(); loss.backward(); optimizer.step()

        if time.time() - last_save_time > 3600:
            checkpoint_data = {
                'model_state_dict': agent.state_dict(),
                'current_step': current_step,
                'entropy_coeff': max(0.003, 0.03 * (1.0 - current_step / args.timesteps)),
            }
            torch.save(checkpoint_data, MODELS_DIR / f"hrl_v5_{args.name}_hour_{datetime.now().strftime('%H%M')}.pth")
            last_save_time = time.time()

    # Final save with step info
    final_data = {
        'model_state_dict': agent.state_dict(),
        'current_step': current_step,
        'entropy_coeff': max(0.003, 0.03 * (1.0 - current_step / args.timesteps)),
    }
    torch.save(final_data, MODELS_DIR / f"hrl_v5_{args.name}_final.pth")
    print(f"[HRL-v5] Training complete at step {current_step}. Final model saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train HRL Agent v5 (GRU History + Attention Pooling)")
    parser.add_argument("--name", type=str, default="v5")
    parser.add_argument("--timesteps", type=int, default=100000)
    parser.add_argument("--rollout_steps", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--world_model", type=str, required=True, help="Path to trained v5 world model checkpoint")
    parser.add_argument("--warmstart_v4", type=str, default=None, help="Path to v4 HRL checkpoint for warm-starting (optional)")
    parser.add_argument("--gnn_layers", type=int, default=6, help="Number of GNN layers (must match world model)")
    parser.add_argument("--checkpoint", type=str, default=None, help="Path to v5 HRL checkpoint to resume from")
    args = parser.parse_args()
    train_hrl_v5(args)
