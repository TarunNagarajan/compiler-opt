import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

from src.env import CompilerOptEnv
from src.config import LLVM_PASSES, MODELS_DIR


class LoggingCallback(BaseCallback):
    
    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_rewards = []
        self.episode_lengths = []
    
    def _on_step(self) -> bool:
        if self.locals.get("dones") is not None:
            for i, done in enumerate(self.locals["dones"]):
                if done:
                    info = self.locals["infos"][i]
                    if "episode" in info:
                        self.episode_rewards.append(info["episode"]["r"])
                        self.episode_lengths.append(info["episode"]["l"])
        return True


def train(
    benchmark_paths: list,
    total_timesteps: int = 10000,
    max_steps: int = 10,
    save_path: str = None
):
    print(f"Creating environment with {len(benchmark_paths)} benchmarks...")
    print(f"Action space: {len(LLVM_PASSES)} passes")
    print(f"Max steps per episode: {max_steps}")
    print()
    
    env = CompilerOptEnv(
        benchmark_paths=benchmark_paths,
        max_steps=max_steps,
        reward_type="instruction_reduction"
    )
    
    print("Initializing PPO agent...")
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
    )
    
    print(f"\nTraining for {total_timesteps} timesteps...")
    callback = LoggingCallback()
    model.learn(total_timesteps=total_timesteps, callback=callback)
    
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        model.save(save_path)
        print(f"\nModel saved to {save_path}")
    
    env.close()
    return model


def evaluate(model, benchmark_paths: list, num_episodes: int = 5):
    print(f"\n=== Evaluating on {len(benchmark_paths)} benchmarks ===\n")
    
    env = CompilerOptEnv(
        benchmark_paths=benchmark_paths,
        max_steps=10,
        render_mode="human"
    )
    
    total_improvements = []
    
    for ep in range(num_episodes):
        obs, info = env.reset()
        done = False
        episode_reward = 0
        
        print(f"\n--- Episode {ep + 1} ---")
        print(f"Initial instructions: {info['initial_instructions']}")
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            done = terminated or truncated
        
        improvement = env.get_total_improvement()
        total_improvements.append(improvement['reduction_pct'])
        
        print(f"Episode reward: {episode_reward:.4f}")
        print(f"Final reduction: {improvement['reduction_pct']:.1f}%")
        print(f"Passes used: {improvement['passes_applied']}")
    
    avg_improvement = sum(total_improvements) / len(total_improvements)
    print(f"\n=== Average improvement: {avg_improvement:.1f}% ===")
    
    env.close()
    return total_improvements


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PPO agent for compiler optimization")
    parser.add_argument("benchmarks", nargs="+", help="Paths to benchmark IR files")
    parser.add_argument("--timesteps", type=int, default=10000, help="Total training timesteps")
    parser.add_argument("--max-steps", type=int, default=10, help="Max steps per episode")
    parser.add_argument("--save", type=str, default=None, help="Path to save model")
    parser.add_argument("--eval-only", type=str, default=None, help="Path to load model for evaluation only")
    
    args = parser.parse_args()
    
    if args.eval_only:
        print(f"Loading model from {args.eval_only}")
        model = PPO.load(args.eval_only)
        evaluate(model, args.benchmarks)
    else:
        save_path = args.save or str(MODELS_DIR / "ppo_compiler_opt")
        model = train(
            benchmark_paths=args.benchmarks,
            total_timesteps=args.timesteps,
            max_steps=args.max_steps,
            save_path=save_path
        )
        evaluate(model, args.benchmarks, num_episodes=3)
