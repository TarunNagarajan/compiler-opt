"""
Multi-strategy agent evaluator.
Tests different sampling/forcing strategies to elicit decisions from conservative checkpoints.

Strategies:
  1. forced_min3  — Mask STOP action for first 3 steps, then allow stopping. Top-K=3, temp=0.7
  2. high_temp    — Temperature=1.5 with Top-K=5 (maximum exploration)
  3. greedy       — Argmax (Top-1) sampling, temp=0.3 (sharp, deterministic)
  4. nucleus_p90  — Nucleus (Top-p=0.9) sampling instead of Top-K
"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import FEATURE_DIM, NUM_ACTIONS, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
import torch

if len(sys.argv) < 3:
    print("Usage: python eval_strategies.py <checkpoint_path> <benchmark1> ...")
    sys.exit(1)

checkpoint_path = sys.argv[1]
files = sys.argv[2:]

world_model_path = "models/world_model_v5_sprint_checkpoint.pth"
agent = create_hrl_agent_v5(FEATURE_DIM, len(MACRO_ACTIONS), world_model_path=world_model_path)
ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
agent.load_state_dict(ckpt['model_state_dict'])
agent.eval()
device = next(agent.parameters()).device

STOP_IDX = len(MACRO_ACTIONS) - 1


def run_agent(env, strategy):
    """Run the agent with a specific sampling strategy. Returns instruction count."""
    obs, info = env.reset()
    graph = env.get_observation_graph()
    episode_action_history = []
    recent_macros = []

    # Strategy params
    if strategy == "forced_min3":
        temperature, top_k, min_steps, top_p = 0.7, 3, 3, None
    elif strategy == "high_temp":
        temperature, top_k, min_steps, top_p = 1.5, 5, 0, None
    elif strategy == "greedy":
        temperature, top_k, min_steps, top_p = 0.3, 1, 0, None
    elif strategy == "nucleus_p90":
        temperature, top_k, min_steps, top_p = 0.7, None, 0, 0.90
    else:
        temperature, top_k, min_steps, top_p = 0.7, 3, 0, None

    for step in range(25):
        padded_history = torch.zeros(1, 25, dtype=torch.long)
        if episode_action_history:
            seq = torch.tensor(episode_action_history, dtype=torch.long)
            if len(seq) > 25: seq = seq[-25:]
            padded_history[0, :len(seq)] = seq
        graph.action_history = padded_history

        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None: edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)

        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
            macro_logits = torch.log(macro_probs + 1e-8) / temperature

            # === FORCED MIN STEPS: mask STOP ===
            if step < min_steps:
                macro_logits[0, STOP_IDX] = -float('inf')

            # === SAMPLING STRATEGY ===
            if top_k is not None:
                # Top-K sampling
                k = min(top_k, macro_logits.size(-1))
                top_k_logits, top_k_indices = torch.topk(macro_logits, k)

                # Repetition throttle
                if len(recent_macros) >= 2:
                    last_2 = recent_macros[-2:]
                    if all(m == last_2[0] for m in last_2):
                        for i in range(top_k_indices.size(1)):
                            if top_k_indices[0, i].item() == last_2[0]:
                                top_k_logits[0, i] -= 10.0

                top_k_probs = torch.softmax(top_k_logits, dim=-1)

                if k == 1:
                    # Greedy
                    m_idx = top_k_indices[0, 0]
                else:
                    selected_idx = torch.distributions.Categorical(top_k_probs).sample()
                    m_idx = top_k_indices[0, selected_idx.item()]

            elif top_p is not None:
                # Nucleus (Top-p) sampling
                sorted_logits, sorted_indices = torch.sort(macro_logits[0], descending=True)
                sorted_probs = torch.softmax(sorted_logits, dim=-1)
                cumulative = torch.cumsum(sorted_probs, dim=-1)

                # Find cutoff
                cutoff_mask = cumulative - sorted_probs > top_p
                sorted_logits[cutoff_mask] = -float('inf')

                # Repetition throttle
                if len(recent_macros) >= 2:
                    last_2 = recent_macros[-2:]
                    if all(m == last_2[0] for m in last_2):
                        for i in range(sorted_indices.size(0)):
                            if sorted_indices[i].item() == last_2[0]:
                                sorted_logits[i] -= 10.0

                probs = torch.softmax(sorted_logits, dim=-1)
                selected = torch.distributions.Categorical(probs).sample()
                m_idx = sorted_indices[selected.item()]

            m_idx_tensor = torch.tensor([m_idx.item()], device=device)

            recent_macros.append(m_idx.item())
            if len(recent_macros) > 5: recent_macros.pop(0)
            episode_action_history.append(m_idx.item() + 1)

            if m_idx.item() == STOP_IDX:
                break

            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx_tensor, edge_attr=edge_attr, graph_data=graph)
            u_logits_temp = u_logits / temperature
            tk_u_logits, tk_u_indices = torch.topk(u_logits_temp, min(3, u_logits.size(-1)))
            tk_u_probs = torch.softmax(tk_u_logits, dim=-1)
            sel_u = torch.distributions.Categorical(tk_u_probs).sample()
            u_idx = tk_u_indices[0, sel_u.item()]

        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]

        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            break
        env.current_ir_path = res.output_path

        from src.features.ir_graph_extractor import IRGraphExtractor
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None:
            break
        graph = extractor.to_pyg_data(new_g)

    m = env.metrics
    return m.count_instructions(str(env.current_ir_path)), step + 1


STRATEGIES = ["forced_min3", "high_temp", "greedy", "nucleus_p90"]

print(f"Checkpoint: {checkpoint_path}")
print(f"{'Benchmark':<25} | {'Strategy':<13} | {'Reduction':>10} | {'Steps':>5} | {'O2':>10} | {'O3':>10}")
print("-" * 85)

for f in files:
    stem = os.path.basename(f).replace('.c', '')

    env = CompilerOptEnv([f], max_steps=1, reward_mode=RewardMode.SPEED)
    env.reset()
    m = env.metrics
    c0 = m.count_instructions(str(env.original_ir_path))

    res_o2 = env.executor.apply_passes(env.original_ir_path, ["default<O2>"])
    c2 = m.count_instructions(str(res_o2.output_path))
    res_o3 = env.executor.apply_passes(env.original_ir_path, ["default<O3>"])
    c3 = m.count_instructions(str(res_o3.output_path))
    r2 = (c0 - c2) / c0 * 100
    r3 = (c0 - c3) / c0 * 100

    for strat in STRATEGIES:
        c_agent, steps = run_agent(env, strat)
        r_agent = (c0 - c_agent) / c0 * 100
        tag = f"{stem}" if strat == STRATEGIES[0] else ""
        print(f"{tag:<25} | {strat:<13} | {r_agent:>9.2f}% | {steps:>5} | {r2:>9.2f}% | {r3:>9.2f}%")
    print()
