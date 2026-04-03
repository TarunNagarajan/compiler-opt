import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime


def load_training_log(log_path: str) -> dict:
    with open(log_path, 'r') as f:
        return json.load(f)


def load_eval_log(log_path: str) -> dict:
    with open(log_path, 'r') as f:
        return json.load(f)


def analyze_pass_sequences(eval_data: dict) -> dict:
    all_passes = []
    pass_sequences = []
    first_passes = Counter()
    pass_pairs = Counter()
    pass_counts = Counter()
    
    for episode in eval_data.get('episodes', []):
        passes = episode.get('passes', [])
        pass_sequences.append(passes)
        all_passes.extend(passes)
        
        if passes:
            first_passes[passes[0]] += 1
        
        for p in passes:
            pass_counts[p] += 1
        
        for i in range(len(passes) - 1):
            pair = f"{passes[i]} -> {passes[i+1]}"
            pass_pairs[pair] += 1
    
    unique_sequences = len(set(tuple(s) for s in pass_sequences))
    avg_unique_passes = sum(len(set(s)) for s in pass_sequences) / max(len(pass_sequences), 1)
    avg_length = sum(len(s) for s in pass_sequences) / max(len(pass_sequences), 1)
    
    repetition_count = 0
    for seq in pass_sequences:
        for i in range(len(seq) - 1):
            if seq[i] == seq[i+1]:
                repetition_count += 1
    
    return {
        'total_episodes': len(pass_sequences),
        'unique_sequences': unique_sequences,
        'avg_sequence_length': round(avg_length, 2),
        'avg_unique_passes_per_episode': round(avg_unique_passes, 2),
        'total_repetitions': repetition_count,
        'most_common_passes': pass_counts.most_common(10),
        'most_common_first_pass': first_passes.most_common(5),
        'most_common_transitions': pass_pairs.most_common(10)
    }


def analyze_reward_progression(training_data: dict) -> dict:
    episodes = training_data.get('episodes', [])
    
    if not episodes:
        return {}
    
    rewards = [e['reward'] for e in episodes]
    
    n = len(rewards)
    first_quarter = rewards[:n//4] if n >= 4 else rewards
    last_quarter = rewards[-n//4:] if n >= 4 else rewards
    
    avg_first = sum(first_quarter) / max(len(first_quarter), 1)
    avg_last = sum(last_quarter) / max(len(last_quarter), 1)
    
    max_reward = max(rewards)
    min_reward = min(rewards)
    avg_reward = sum(rewards) / len(rewards)
    
    positive_episodes = sum(1 for r in rewards if r > 0)
    
    return {
        'total_episodes': len(rewards),
        'avg_reward': round(avg_reward, 4),
        'max_reward': round(max_reward, 4),
        'min_reward': round(min_reward, 4),
        'avg_first_quarter': round(avg_first, 4),
        'avg_last_quarter': round(avg_last, 4),
        'improvement': round(avg_last - avg_first, 4),
        'positive_episode_pct': round(100 * positive_episodes / len(rewards), 1)
    }


def compare_agents(hackable_eval: dict, secure_eval: dict) -> dict:
    h_analysis = analyze_pass_sequences(hackable_eval)
    s_analysis = analyze_pass_sequences(secure_eval)
    
    return {
        'hackable': {
            'avg_unique_passes': h_analysis['avg_unique_passes_per_episode'],
            'total_repetitions': h_analysis['total_repetitions'],
            'top_pass': h_analysis['most_common_passes'][0] if h_analysis['most_common_passes'] else None,
            'unique_sequences': h_analysis['unique_sequences']
        },
        'secure': {
            'avg_unique_passes': s_analysis['avg_unique_passes_per_episode'],
            'total_repetitions': s_analysis['total_repetitions'],
            'top_pass': s_analysis['most_common_passes'][0] if s_analysis['most_common_passes'] else None,
            'unique_sequences': s_analysis['unique_sequences']
        },
        'diversity_improvement': round(
            s_analysis['avg_unique_passes_per_episode'] - h_analysis['avg_unique_passes_per_episode'], 2
        ),
        'repetition_reduction': h_analysis['total_repetitions'] - s_analysis['total_repetitions']
    }


def print_analysis(analysis: dict, title: str):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)
    
    for key, value in analysis.items():
        if isinstance(value, list):
            print(f"\n{key}:")
            for item in value[:5]:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")


def save_analysis(analysis: dict, output_path: Path):
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"\nAnalysis saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze pass sequences from training logs")
    parser.add_argument("--training", type=str, help="Path to training JSON log")
    parser.add_argument("--eval", type=str, help="Path to evaluation JSON log")
    parser.add_argument("--compare-hackable", type=str, help="Path to hackable eval log")
    parser.add_argument("--compare-secure", type=str, help="Path to secure eval log")
    parser.add_argument("--output", type=str, help="Path to save analysis JSON")
    
    args = parser.parse_args()
    
    results = {}
    
    if args.training:
        training_data = load_training_log(args.training)
        reward_analysis = analyze_reward_progression(training_data)
        results['reward_progression'] = reward_analysis
        print_analysis(reward_analysis, "Reward Progression")
    
    if args.eval:
        eval_data = load_eval_log(args.eval)
        pass_analysis = analyze_pass_sequences(eval_data)
        results['pass_sequences'] = pass_analysis
        print_analysis(pass_analysis, "Pass Sequence Analysis")
    
    if args.compare_hackable and args.compare_secure:
        hackable_data = load_eval_log(args.compare_hackable)
        secure_data = load_eval_log(args.compare_secure)
        comparison = compare_agents(hackable_data, secure_data)
        results['agent_comparison'] = comparison
        print_analysis(comparison, "Agent Comparison (HACKABLE vs SECURE)")
    
    if args.output and results:
        save_analysis(results, Path(args.output))
    
    if not any([args.training, args.eval, args.compare_hackable]):
        print("Usage examples:")
        print("  Analyze training: python analyze_passes.py --training logs/hackable_training.json")
        print("  Analyze eval:     python analyze_passes.py --eval logs/hackable_eval.json")
        print("  Compare agents:   python analyze_passes.py --compare-hackable logs/hackable_eval.json --compare-secure logs/secure_eval.json")
