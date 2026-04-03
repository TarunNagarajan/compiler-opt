import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import glob as glob_module
import json
import random
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList
from stable_baselines3.common.monitor import Monitor

from src.env import CompilerOptEnv, RewardMode
from src.actions import MACRO_ACTIONS
from src.config import LLVM_PASSES, MODELS_DIR

LOGS_DIR = Path(__file__).parent.parent / "logs"

def expand_globs(patterns):
    files = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern:
            files.extend(glob_module.glob(pattern, recursive=True))
        else:
            files.append(pattern)
    return sorted(list(set(files)))

def train_and_evaluate(
    benchmark_paths: list,
    total_timesteps: int = 100000,
    max_steps: int = 10,
    reward_mode: RewardMode = RewardMode.HACKABLE,
    run_name: str = None,
    test_split: float = 0.2
):
    # LEAK PROOF: Shuffle and Split benchmarks
    random.seed(42)
    random.shuffle(benchmark_paths)
    split_idx = int(len(benchmark_paths) * (1 - test_split))
    train_benchmarks = benchmark_paths[:split_idx]
    test_benchmarks = benchmark_paths[split_idx:]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = run_name or f"GEN_PPO_{reward_mode.value}_{timestamp}"
    
    print(f"[AGENT] --- LEAK-PROOF TRAINING INITIALIZED ---")
    print(f"[AGENT] Total Benchmarks: {len(benchmark_paths)}...")
    print(f"[AGENT] Training Set:    {len(train_benchmarks)}...")
    print(f"[AGENT] Test Set (Unseen): {len(test_benchmarks)}...")
    print(f"[AGENT] Reward Mode:     {reward_mode.value}...")
    
    train_env = CompilerOptEnv(benchmark_paths=train_benchmarks, max_steps=max_steps, reward_mode=reward_mode)
    train_env = Monitor(train_env)
    
    model = PPO(
        "MlpPolicy",
        train_env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=256,
        n_epochs=10,
        tensorboard_log=str(LOGS_DIR / "tensorboard")
    )
    
    print(f"[AGENT] Training for {total_timesteps} steps...")
    model.learn(total_timesteps=total_timesteps, tb_log_name=run_name)
    
    # Save the model
    model_path = MODELS_DIR / f"{run_name}.zip"
    model.save(model_path)
    
    # LEAK PROOF EVALUATION
    print(f"[AGENT] --- COMMENCING ZERO-SHOT EVALUATION ON UNSEEN BENCHMARKS ---")
    eval_results = evaluate(model, test_benchmarks, reward_mode)
    
    with open(LOGS_DIR / f"{run_name}_results.json", 'w') as f:
        json.dump(eval_results, f, indent=2)
    
    return model

def evaluate(model, benchmark_paths: list, reward_mode: RewardMode, num_episodes: int = 5):
    env = CompilerOptEnv(benchmark_paths=benchmark_paths, max_steps=10, reward_mode=reward_mode)
    results = []
    
    for ep in range(num_episodes):
        obs, info = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, term, trunc, info = env.step(action)
            done = term or trunc
        
        improvement = env.get_total_improvement()
        results.append(improvement)
        print(f"[AGENT] Unseen {ep+1}: {improvement['reduction_pct']:.1f}% reduction...")
        
    avg_red = sum(r['reduction_pct'] for r in results) / len(results)
    print(f"[AGENT] Average Zero-Shot Improvement: {avg_red:.1f}%...")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmarks", nargs="+")
    parser.add_argument("--timesteps", type=int, default=10000)
    parser.add_argument("--mode", type=str, default="hackable", 
                        choices=["hackable", "secure", "performance", "size", "security", "compilation_speed"])
    parser.add_argument("--run-name", type=str, help="Custom name for the training run")
    args = parser.parse_args()
    
    files = expand_globs(args.benchmarks)
    
    mode_map = {
        "hackable": RewardMode.HACKABLE,
        "secure": RewardMode.SECURE,
        "performance": RewardMode.PERFORMANCE,
        "size": RewardMode.SIZE,
        "security": RewardMode.SECURITY,
        "compilation_speed": RewardMode.COMPILATION_SPEED
    }
    mode = mode_map[args.mode]
    
    train_and_evaluate(
        files, 
        total_timesteps=args.timesteps, 
        reward_mode=mode, 
        run_name=args.run_name
    )
