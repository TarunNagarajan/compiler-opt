"""
V8 World Model — Action Ranking Evaluation

The critical question: given a program state, does the model rank actions
correctly? Does it predict that the best pass is actually the best?

Metrics:
1. Top-1 accuracy: model's best action = actual best action
2. Top-3 accuracy: actual best action in model's top-3
3. Pairwise accuracy: for all (a_i, a_j) pairs, does model agree which is better?
4. Spearman rank correlation: overall ranking agreement
5. Regret: how much worse is the model's top pick vs the actual best?

Usage:
  uv run python scripts/evaluate_ranking_v8.py --checkpoint models/world_model_action_fix_v6_best.pth --programs 30 --actions_per_program 10
"""

import sys
import torch
import numpy as np
import argparse
import random
import time
from pathlib import Path
from scipy import stats as scipy_stats
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model import WorldModel
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS


def load_model(checkpoint_path):
    model = WorldModel(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    state_dict = ckpt.get('model_state_dict', ckpt)
    model_shapes = {k: v.shape for k, v in model.state_dict().items()}
    to_skip = [k for k in state_dict if k in model_shapes and state_dict[k].shape != model_shapes[k]]
    for k in to_skip:
        del state_dict[k]
    model.load_state_dict(state_dict, strict=False)
    model.eval()
    return model


def get_size_tier(filepath):
    try:
        size = Path(filepath).stat().st_size
    except:
        return "unknown"
    if size > 200_000:
        return "large/industrial"
    elif size > 50_000:
        return "medium"
    else:
        return "small"


def evaluate_ranking(model, env, num_programs, actions_to_test, seed=42):
    """
    For each program:
      1. Reset to a random program state
      2. Try N random actions, record actual instruction delta
      3. Ask the model to predict instruction delta for each action
      4. Compare rankings
    """
    rng = random.Random(seed)
    results = []
    errors = 0

    print(f"[RANK] Evaluating ranking on {num_programs} programs, {actions_to_test} actions each")
    print(f"[RANK] Total action-evaluations: {num_programs * actions_to_test}")
    t0 = time.time()

    for prog_i in range(num_programs):
        if (prog_i + 1) % 5 == 0:
            elapsed = time.time() - t0
            print(f"  [{prog_i+1}/{num_programs}] {elapsed:.0f}s elapsed")

        try:
            # Get a fresh program state
            obs, info = env.reset()
            graph = env.get_observation_graph()
            if graph is None:
                errors += 1
                continue

            num_nodes = graph.x.size(0) - 1
            total_nodes = getattr(graph, 'total_nodes', num_nodes)
            filepath = str(env.current_benchmark_path)

            # Encode the graph once
            with torch.no_grad():
                state_emb = model.encode_graph(graph)

            # Pick random actions to test
            action_pool = rng.sample(range(NUM_ACTIONS), min(actions_to_test, NUM_ACTIONS))

            actual_deltas = []
            predicted_deltas = []
            action_ids = []

            for action in action_pool:
                # Reset to the SAME program state for fair comparison
                env.reset(options={"ir_path": filepath})
                _, _, _, _, step_info = env.step(action)

                # Actual instruction delta
                # Training convention: (after - before)/before * 100
                # So NEGATIVE = reduction = good
                instr_before = step_info.get('instructions_before', 1)
                instr_after = step_info.get('instructions_after', instr_before)
                actual_delta = (instr_after - instr_before) / max(instr_before, 1) * 100.0

                # Model prediction (same convention: negative = reduction)
                with torch.no_grad():
                    action_onehot = torch.zeros(1, NUM_ACTIONS)
                    action_onehot[0, action] = 1.0
                    _, pred_metrics = model(
                        state_emb, action_onehot,
                        num_nodes=num_nodes, total_nodes=total_nodes
                    )
                    pred_delta = pred_metrics[0, 0].item()

                actual_deltas.append(actual_delta)
                predicted_deltas.append(pred_delta)
                action_ids.append(action)

            if len(actual_deltas) < 2:
                continue

            actual_arr = np.array(actual_deltas)
            pred_arr = np.array(predicted_deltas)

            # Rankings (lower/more-negative delta = better, so argsort ascending)
            actual_rank = np.argsort(actual_arr)
            pred_rank = np.argsort(pred_arr)

            # Top-1: does model's best match actual best?
            top1_match = actual_rank[0] == pred_rank[0]

            # Top-3: is actual best in model's top 3?
            k = min(3, len(action_pool))
            top3_match = actual_rank[0] in pred_rank[:k]

            # Pairwise accuracy
            # Convention: lower delta = better (more reduction)
            n_pairs = 0
            n_correct = 0
            for i in range(len(actual_arr)):
                for j in range(i + 1, len(actual_arr)):
                    if abs(actual_arr[i] - actual_arr[j]) < 0.01:
                        continue  # Skip ties
                    n_pairs += 1
                    actual_better = actual_arr[i] < actual_arr[j]
                    pred_better = pred_arr[i] < pred_arr[j]
                    if actual_better == pred_better:
                        n_correct += 1
            pairwise_acc = n_correct / max(n_pairs, 1)

            # Spearman rank correlation
            if np.std(actual_arr) > 1e-6 and np.std(pred_arr) > 1e-6:
                spearman_r, _ = scipy_stats.spearmanr(actual_arr, pred_arr)
            else:
                spearman_r = 0.0

            # Regret: how much worse is model's pick vs actual best?
            # Best = most negative delta. Regret = model_pick - actual_best (>= 0, lower is better)
            model_best_idx = pred_rank[0]
            actual_best_delta = actual_arr[actual_rank[0]]
            model_pick_actual_delta = actual_arr[model_best_idx]
            regret = model_pick_actual_delta - actual_best_delta  # >= 0, lower is better

            # Check if model's pick is at least "non-harmful"
            model_pick_safe = model_pick_actual_delta <= 0.5  # didn't increase instructions by >0.5%

            results.append({
                'top1': top1_match,
                'top3': top3_match,
                'pairwise_acc': pairwise_acc,
                'spearman': spearman_r,
                'regret': regret,
                'model_pick_safe': model_pick_safe,
                'actual_best_delta': actual_best_delta,
                'model_pick_delta': model_pick_actual_delta,
                'n_actions': len(action_pool),
                'n_pairs': n_pairs,
                'num_nodes': num_nodes,
                'tier': get_size_tier(filepath),
                'filepath': filepath,
                'actual_deltas': actual_arr,
                'pred_deltas': pred_arr,
            })

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  [ERROR] Program {prog_i}: {e}")
            continue

    elapsed = time.time() - t0
    print(f"[RANK] Done: {len(results)} programs in {elapsed:.0f}s ({errors} errors)")
    return results


def analyze_ranking(results):
    if not results:
        print("No results!")
        return

    print("\n" + "=" * 72)
    print("  V8 WORLD MODEL — ACTION RANKING EVALUATION")
    print("=" * 72)
    print(f"  Programs evaluated: {len(results)}")
    total_actions = sum(r['n_actions'] for r in results)
    print(f"  Total action evals: {total_actions}")

    # ── Core Ranking Metrics ──
    top1 = np.mean([r['top1'] for r in results])
    top3 = np.mean([r['top3'] for r in results])
    pairwise = np.mean([r['pairwise_acc'] for r in results])
    spearman = np.mean([r['spearman'] for r in results])
    avg_regret = np.mean([r['regret'] for r in results])
    median_regret = np.median([r['regret'] for r in results])
    safe_pct = np.mean([r['model_pick_safe'] for r in results])

    print(f"\n  RANKING ACCURACY:")
    print(f"    Top-1 Accuracy:      {top1:.1%}  (model's #1 = actual #1)")
    print(f"    Top-3 Accuracy:      {top3:.1%}  (actual #1 in model's top 3)")
    print(f"    Pairwise Accuracy:   {pairwise:.1%}  (correct ordering of action pairs)")
    print(f"    Spearman Corr:       {spearman:.3f}  (rank correlation, 1.0 = perfect)")

    print(f"\n  REGRET (lower = better):")
    print(f"    Mean Regret:         {avg_regret:.2f}%  (gap: model's pick vs actual best)")
    print(f"    Median Regret:       {median_regret:.2f}%")
    print(f"    Safe Pick Rate:      {safe_pct:.1%}  (model's pick doesn't harm >0.5%)")

    # ── Regret Distribution ──
    regrets = [r['regret'] for r in results]
    print(f"\n  REGRET DISTRIBUTION:")
    print(f"    0% (perfect pick):   {sum(1 for r in regrets if r < 0.1)}/{len(regrets)}")
    print(f"    <1% regret:          {sum(1 for r in regrets if r < 1.0)}/{len(regrets)}")
    print(f"    <5% regret:          {sum(1 for r in regrets if r < 5.0)}/{len(regrets)}")
    print(f"    >=5% regret:         {sum(1 for r in regrets if r >= 5.0)}/{len(regrets)}")

    # ── Stratified by tier ──
    tiers = defaultdict(list)
    for r in results:
        tiers[r['tier']].append(r)

    if len(tiers) > 1:
        print(f"\n  BY SCALE TIER:")
        for tier in ['small', 'medium', 'large/industrial']:
            if tier not in tiers:
                continue
            tr = tiers[tier]
            t_top1 = np.mean([r['top1'] for r in tr])
            t_pair = np.mean([r['pairwise_acc'] for r in tr])
            t_regret = np.mean([r['regret'] for r in tr])
            t_spear = np.mean([r['spearman'] for r in tr])
            print(f"    {tier:20s}: n={len(tr):>3}, Top1={t_top1:.0%}, Pair={t_pair:.0%}, "
                  f"Regret={t_regret:.2f}%, Spearman={t_spear:.3f}")

    # ── Worst Cases ──
    print(f"\n  TOP-5 HIGHEST REGRET PROGRAMS:")
    sorted_results = sorted(results, key=lambda r: -r['regret'])
    for i, r in enumerate(sorted_results[:5]):
        fname = Path(r['filepath']).name
        print(f"    {i+1}. regret={r['regret']:.2f}%  actual_best={r['actual_best_delta']:.2f}%  "
              f"model_pick={r['model_pick_delta']:.2f}%  nodes={r['num_nodes']}  file={fname}")

    # ── Best Cases ──
    print(f"\n  TOP-5 BEST RANKED PROGRAMS (perfect or near-perfect):")
    sorted_best = sorted(results, key=lambda r: r['regret'])
    for i, r in enumerate(sorted_best[:5]):
        fname = Path(r['filepath']).name
        print(f"    {i+1}. regret={r['regret']:.2f}%  spearman={r['spearman']:.3f}  "
              f"pairwise={r['pairwise_acc']:.0%}  nodes={r['num_nodes']}  file={fname}")

    # ── Verdict ──
    print(f"\n" + "=" * 72)
    if pairwise >= 0.7 and top3 >= 0.6 and safe_pct >= 0.85:
        verdict = "READY FOR HRL"
    elif pairwise >= 0.6 and safe_pct >= 0.75:
        verdict = "USABLE (marginal)"
    else:
        verdict = "NOT READY"
    print(f"  VERDICT: {verdict}")
    print(f"  Pairwise={pairwise:.1%}  Top3={top3:.1%}  SafePick={safe_pct:.1%}  Spearman={spearman:.3f}")
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate V8 World Model Action Ranking")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--programs", type=int, default=30,
                        help="Number of programs to evaluate")
    parser.add_argument("--actions_per_program", type=int, default=10,
                        help="Number of random actions to compare per program")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    model = load_model(args.checkpoint)
    print(f"[RANK] Loaded model: {sum(p.numel() for p in model.parameters()):,} params")

    env = CompilerOptEnv(get_benchmark_paths())
    results = evaluate_ranking(model, env, args.programs, args.actions_per_program, seed=args.seed)
    analyze_ranking(results)
