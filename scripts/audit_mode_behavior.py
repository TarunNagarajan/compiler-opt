#!/usr/bin/env python3
"""
Audit Sports (performance) vs Embedded mode behavior claims.

This script provides executable evidence for:
1) reward-level objective definitions,
2) policy-action distribution differences,
3) outcome-level differences under each mode.
"""

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch

sys.path.append(os.getcwd())

from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.config import FEATURE_DIM, NUM_ACTIONS, NUM_ATOMIC_ACTIONS, get_benchmark_paths
from src.env.compiler_env import CompilerOptEnv, RewardMode
from src.models.calibrated_wrapper import CalibratedWorldModel
from src.models.hrl_agent import HRLAgent
from src.models.world_model import WorldModel


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _select_benchmarks(paths, max_benchmarks, max_source_kb):
    benches = [Path(p) for p in paths if Path(p).exists()]
    if max_source_kb > 0:
        max_bytes = max_source_kb * 1024
        benches = [b for b in benches if b.stat().st_size <= max_bytes]
    benches = sorted(benches)
    if max_benchmarks > 0:
        benches = benches[:max_benchmarks]
    return benches


def _delta(info, before_key, after_key):
    before_v = float(info.get(before_key, 0.0))
    after_v = float(info.get(after_key, 0.0))
    if before_v <= 0:
        return 0.0
    return (before_v - after_v) / max(before_v, 1e-6)


def _metrics_from_info(info):
    i_before = info.get('instructions_before', 1)
    i_after = info.get('instructions_after', 1)
    r_before = info.get('runtime_before', 0.0)
    r_after = info.get('runtime_after', 0.0)
    e_before = info.get('energy_before', 0.0)
    e_after = info.get('energy_after', 0.0)

    inst_gain = (i_before - i_after) / max(i_before, 1) * 100.0
    speed_gain = ((r_before - r_after) / max(r_before, 1e-6) * 100.0) if (r_before > 0 and r_after > 0) else 0.0
    energy_gain = ((e_before - e_after) / max(e_before, 1e-6) * 100.0) if (e_before > 0 and e_after > 0) else 0.0

    edge_proxy = (
        0.24 * _delta(info, 'loads_before', 'loads_after')
        + 0.14 * _delta(info, 'stores_before', 'stores_after')
        + 0.18 * _delta(info, 'allocas_before', 'allocas_after')
        + 0.16 * _delta(info, 'blocks_before', 'blocks_after')
        + 0.12 * _delta(info, 'calls_before', 'calls_after')
        + 0.16 * _delta(info, 'branches_before', 'branches_after')
    )

    return inst_gain, speed_gain, energy_gain, edge_proxy


def load_agent(agent_ckpt, world_model_ckpt, meta_calibrator, device):
    base_wm = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=6).to(device)
    wm_payload = torch.load(world_model_ckpt, map_location=device, weights_only=False)
    base_wm.load_state_dict(wm_payload.get('model_state_dict', wm_payload), strict=False)
    world_model = CalibratedWorldModel(base_wm, meta_calibrator_path=meta_calibrator).to(device)
    world_model.eval()

    agent = HRLAgent(
        state_dim=FEATURE_DIM,
        num_macros=len(MACRO_ACTIONS),
        world_model=world_model,
        num_actions=NUM_ACTIONS,
    ).to(device)

    payload = torch.load(agent_ckpt, map_location=device, weights_only=False)
    agent.load_state_dict(payload['model_state_dict'])
    agent.eval()
    return agent


def eval_mode(agent, mode_name, benches, seed, max_steps):
    reward_mode = RewardMode.SPEED if mode_name == 'performance' else RewardMode.SIZE
    collect_speed_metrics = mode_name == 'embedded'

    env = CompilerOptEnv(
        benches,
        max_steps=max_steps,
        reward_mode=reward_mode,
        collect_speed_metrics=collect_speed_metrics,
        runtime_measure_runs=2,
    )

    macro_hist = Counter()
    micro_hist = Counter()

    entropies = []
    all_rewards = []
    all_speed = []
    all_instr = []
    all_energy = []
    all_edge = []
    sports_obj = []
    embedded_obj = []

    episode_rows = []

    with torch.no_grad():
        for eidx, bench in enumerate(benches):
            env.reset(seed=seed + eidx, options={'ir_path': str(bench)})
            history = [0]
            ep_reward = 0.0
            ep_speed = []
            ep_instr = []
            ep_energy = []
            ep_edge = []

            for _ in range(max_steps):
                graph_data = env.get_observation_graph()
                if graph_data is None:
                    break

                hist_tensor = torch.tensor([history], dtype=torch.long)
                macro_probs, _, history_emb, state_emb = agent(
                    graph_data.x,
                    graph_data.edge_index,
                    getattr(graph_data, 'batch', None),
                    edge_attr=graph_data.edge_attr,
                    action_history=hist_tensor,
                    graph_data=graph_data,
                )

                macro_entropy = torch.distributions.Categorical(macro_probs).entropy().item()
                entropies.append(macro_entropy)

                macro_act = int(torch.argmax(macro_probs, dim=-1).item())
                macro_hist[macro_act] += 1

                macro_onehot = torch.zeros(1, len(MACRO_ACTIONS))
                macro_onehot[0, macro_act] = 1.0
                micro_probs = agent.get_worker_act(state_emb, macro_onehot, history_emb)
                micro_act = int(torch.argmax(micro_probs, dim=-1).item())
                micro_hist[micro_act] += 1

                terminate_idx = len(MACRO_ACTIONS) - 1
                if macro_act == terminate_idx:
                    break

                base_seq = MACRO_ACTIONS[macro_act]
                refined_seq = MicroRefiner.apply_refinement(base_seq, micro_act)
                refined_pipeline = [f"module({','.join(refined_seq)})"]
                _, reward, terminated, truncated, info = env.step(
                    NUM_ATOMIC_ACTIONS + macro_act,
                    custom_passes=refined_pipeline,
                )

                inst_gain, speed_gain, energy_gain, edge_proxy = _metrics_from_info(info)

                ep_reward += float(reward)
                ep_speed.append(speed_gain)
                ep_instr.append(inst_gain)
                ep_energy.append(energy_gain)
                ep_edge.append(edge_proxy * 100.0)

                sports_obj.append(speed_gain)
                embedded_obj.append(0.4 * inst_gain + 0.1 * speed_gain + 0.5 * energy_gain + 10.0 * edge_proxy)

                history.append(NUM_ATOMIC_ACTIONS + macro_act)
                if terminated or truncated:
                    break

            all_rewards.append(ep_reward)
            all_speed.extend(ep_speed)
            all_instr.extend(ep_instr)
            all_energy.extend(ep_energy)
            all_edge.extend(ep_edge)
            episode_rows.append(
                {
                    'benchmark': bench.name,
                    'episode_reward_sum': ep_reward,
                    'mean_speed_gain_pct': float(np.mean(ep_speed)) if ep_speed else 0.0,
                    'mean_instr_gain_pct': float(np.mean(ep_instr)) if ep_instr else 0.0,
                    'mean_energy_gain_pct': float(np.mean(ep_energy)) if ep_energy else 0.0,
                    'mean_edge_proxy_pct': float(np.mean(ep_edge)) if ep_edge else 0.0,
                }
            )

    macro_total = sum(macro_hist.values())
    micro_total = sum(micro_hist.values())

    return {
        'mode': mode_name,
        'benchmarks': [str(b) for b in benches],
        'episodes': episode_rows,
        'num_steps': int(len(all_speed)),
        'mean_macro_entropy': float(np.mean(entropies)) if entropies else 0.0,
        'mean_episode_reward': float(np.mean(all_rewards)) if all_rewards else 0.0,
        'mean_speed_gain_pct': float(np.mean(all_speed)) if all_speed else 0.0,
        'mean_instr_gain_pct': float(np.mean(all_instr)) if all_instr else 0.0,
        'mean_energy_gain_pct': float(np.mean(all_energy)) if all_energy else 0.0,
        'mean_edge_proxy_pct': float(np.mean(all_edge)) if all_edge else 0.0,
        'mean_sports_objective_pct': float(np.mean(sports_obj)) if sports_obj else 0.0,
        'mean_embedded_objective_pct': float(np.mean(embedded_obj)) if embedded_obj else 0.0,
        'macro_action_distribution': {
            str(k): (v / macro_total if macro_total else 0.0) for k, v in sorted(macro_hist.items())
        },
        'micro_action_distribution': {
            str(k): (v / micro_total if micro_total else 0.0) for k, v in sorted(micro_hist.items())
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sports_checkpoint', required=True)
    ap.add_argument('--embedded_checkpoint', required=True)
    ap.add_argument('--world_model', required=True)
    ap.add_argument('--meta_calibrator', required=True)
    ap.add_argument('--max_benchmarks', type=int, default=4)
    ap.add_argument('--max_source_kb', type=int, default=32)
    ap.add_argument('--max_steps', type=int, default=10)
    ap.add_argument('--seed', type=int, default=1337)
    ap.add_argument('--output', default='results/mode_behavior_audit.json')
    args = ap.parse_args()

    set_seed(args.seed)

    benches = _select_benchmarks(get_benchmark_paths(), args.max_benchmarks, args.max_source_kb)
    if not benches:
        raise RuntimeError('No benchmarks found for mode behavior audit.')

    device = torch.device('cpu')

    sports_agent = load_agent(args.sports_checkpoint, args.world_model, args.meta_calibrator, device)
    embedded_agent = load_agent(args.embedded_checkpoint, args.world_model, args.meta_calibrator, device)

    sports_eval = eval_mode(sports_agent, 'performance', benches, args.seed, args.max_steps)
    embedded_eval = eval_mode(embedded_agent, 'embedded', benches, args.seed + 101, args.max_steps)

    conclusions = {
        'sports_priority_speed': sports_eval['mean_sports_objective_pct'] >= embedded_eval['mean_sports_objective_pct'],
        'embedded_priority_embedded_obj': embedded_eval['mean_embedded_objective_pct'] >= sports_eval['mean_embedded_objective_pct'],
        'mode_distributions_differ': sports_eval['macro_action_distribution'] != embedded_eval['macro_action_distribution'],
    }

    out = {
        'sports_eval': sports_eval,
        'embedded_eval': embedded_eval,
        'conclusions': conclusions,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')

    print('[MODE-AUDIT] wrote:', out_path)
    print('[MODE-AUDIT] sports mean speed objective:', sports_eval['mean_sports_objective_pct'])
    print('[MODE-AUDIT] embedded mean speed objective:', embedded_eval['mean_sports_objective_pct'])
    print('[MODE-AUDIT] sports mean embedded objective:', sports_eval['mean_embedded_objective_pct'])
    print('[MODE-AUDIT] embedded mean embedded objective:', embedded_eval['mean_embedded_objective_pct'])
    print('[MODE-AUDIT] conclusions:', conclusions)


if __name__ == '__main__':
    main()
