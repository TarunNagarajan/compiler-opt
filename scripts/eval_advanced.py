"""
Advanced inference strategies to maximize agent performance.

New strategies:
  1. best_of_5     — Run agent 5 times with forced_min3, keep the best result
  2. rollback      — After each step, check instruction count. If it regressed, undo and try next-best action
  3. annealed      — Temperature starts at 2.0 (explore) and decays to 0.3 (exploit) over the episode
"""
import sys, os, copy
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import FEATURE_DIM, NUM_ACTIONS, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
import torch

if len(sys.argv) < 3:
    print("Usage: python eval_advanced.py <checkpoint_path> <benchmark1> ...")
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


def run_single(env, temperature=0.7, top_k=3, min_steps=3, anneal=False):
    """Run agent once. Returns (final_inst_count, steps_taken)."""
    obs, info = env.reset()
    graph = env.get_observation_graph()
    episode_action_history = []
    recent_macros = []

    for step in range(25):
        # Annealing: temp goes from 2.0 → 0.3 over 25 steps
        if anneal:
            t = 2.0 - (1.7 * step / 24.0)
        else:
            t = temperature

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
            macro_logits = torch.log(macro_probs + 1e-8) / t

            if step < min_steps:
                macro_logits[0, STOP_IDX] = -float('inf')

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
            selected_idx = torch.distributions.Categorical(top_k_probs).sample()
            m_idx = top_k_indices[0, selected_idx.item()]
            m_idx_tensor = torch.tensor([m_idx.item()], device=device)

            recent_macros.append(m_idx.item())
            if len(recent_macros) > 5: recent_macros.pop(0)
            episode_action_history.append(m_idx.item() + 1)

            if m_idx.item() == STOP_IDX:
                break

            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx_tensor, edge_attr=edge_attr, graph_data=graph)
            u_logits_temp = u_logits / t
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


def run_rollback(env):
    """
    Rollback strategy: after each optimization step, measure instruction count.
    If it increased (regressed), revert to previous IR and try the next-best action.
    """
    obs, info = env.reset()
    graph = env.get_observation_graph()
    episode_action_history = []
    recent_macros = []
    m = env.metrics

    best_ir = str(env.current_ir_path)
    best_count = m.count_instructions(best_ir)
    temperature = 0.7
    total_steps = 0

    for step in range(15):
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

            # Force at least 3 steps
            if step < 3:
                macro_logits[0, STOP_IDX] = -float('inf')

            # Get top 5 candidates for rollback attempts
            top5_logits, top5_indices = torch.topk(macro_logits, min(5, macro_logits.size(-1)))

            # Try each candidate in order of probability
            found_improvement = False
            for candidate_rank in range(top5_indices.size(1)):
                m_idx = top5_indices[0, candidate_rank]

                if m_idx.item() == STOP_IDX:
                    if step >= 3:
                        # Allow stop after min steps
                        found_improvement = True  # signal to break outer loop
                        break
                    continue

                m_idx_tensor = torch.tensor([m_idx.item()], device=device)

                u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx_tensor, edge_attr=edge_attr, graph_data=graph)
                u_logits_temp = u_logits / temperature
                # Greedy micro action for rollback mode
                u_idx = u_logits_temp.argmax(dim=-1)[0]

                base_seq = MACRO_ACTIONS[m_idx.item()]
                final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
                pipeline = [f"module({','.join(final_seq)})"]

                # Apply to a COPY (rollback-safe)
                res = env.executor.apply_passes(env.current_ir_path, pipeline)
                if not res.success:
                    continue

                new_count = m.count_instructions(str(res.output_path))

                if new_count <= best_count:
                    # Accept: this action improved or maintained
                    best_count = new_count
                    best_ir = str(res.output_path)
                    env.current_ir_path = res.output_path
                    episode_action_history.append(m_idx.item() + 1)
                    recent_macros.append(m_idx.item())
                    if len(recent_macros) > 5: recent_macros.pop(0)
                    found_improvement = True
                    total_steps += 1

                    # Re-extract graph
                    from src.features.ir_graph_extractor import IRGraphExtractor
                    extractor = IRGraphExtractor()
                    new_g = extractor.parse_file(env.current_ir_path)
                    if new_g is not None:
                        graph = extractor.to_pyg_data(new_g)
                    break
                # else: rollback — try next candidate

            if not found_improvement:
                break  # No candidate improved; stop

    return best_count, total_steps


STRATEGIES = {
    "forced_min3": lambda env: run_single(env, temperature=0.7, top_k=3, min_steps=3),
    "best_of_5": None,  # handled specially
    "rollback": lambda env: run_rollback(env),
    "annealed": lambda env: run_single(env, top_k=5, min_steps=3, anneal=True),
}

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

    for strat_name in STRATEGIES:
        if strat_name == "best_of_5":
            # Run forced_min3 five times, keep the best
            best_c = c0
            best_steps = 0
            for trial in range(5):
                c_trial, s_trial = run_single(env, temperature=0.7, top_k=3, min_steps=3)
                if c_trial < best_c:
                    best_c = c_trial
                    best_steps = s_trial
            c_agent, steps = best_c, best_steps
        else:
            c_agent, steps = STRATEGIES[strat_name](env)

        r_agent = (c0 - c_agent) / c0 * 100
        tag = f"{stem}" if strat_name == list(STRATEGIES.keys())[0] else ""
        print(f"{tag:<25} | {strat_name:<13} | {r_agent:>9.2f}% | {steps:>5} | {r2:>9.2f}% | {r3:>9.2f}%")
    print()
