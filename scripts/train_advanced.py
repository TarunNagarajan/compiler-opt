
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import torch
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.monitor import Monitor

from src.env import CompilerOptEnv, RewardMode
from src.config import get_benchmark_paths, MODELS_DIR, LOGS_DIR, CONSTRAINT_SIZE_LIMIT_PCT

class LagrangianRewardWrapper(gym.Wrapper):
    def __init__(self, env, lambda_size=0.0):
        super().__init__(env)
        self.lambda_size = lambda_size
        self.last_constraints = {}
        
    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        # PPO-Lagrangian Reward Modification
        # R' = R - lambda * constraint_cost
        # We only punish if constraint > limit (or just raw cost if we want to minimize it)
        # Typically: cost = max(0, violation)
        
        constraints = info.get('constraints', {})
        size_increase = constraints.get('size_increase_pct', 0.0)
        
        # Violation: Amount exceeding the limit
        violation = max(0, size_increase - CONSTRAINT_SIZE_LIMIT_PCT)
        
        penalty = self.lambda_size * violation
        new_reward = reward - penalty
        
        info['lambda_size'] = self.lambda_size
        info['penalty'] = penalty
        self.last_constraints = constraints
        
        return obs, new_reward, terminated, truncated, info

class LagrangianCallback(BaseCallback):
    """
    Updates Lagrange multipliers based on constraint violations.
    Dual Gradient Ascent: lambda = max(0, lambda + lr * (cost - limit))
    """
    def __init__(self, env_wrapper, verbose=0, lr=0.01):
        super().__init__(verbose)
        self.env_wrapper = env_wrapper
        self.lr = lr
        self.history = []
        
    def _on_step(self):
        # Access the wrapper through the VecEnv
        # Assuming DummyVecEnv with 1 env
        # In SB3, training_env is a VecEnv.
        
        # We need to get the actual violations from the last step.
        # This is tricky with VecEnv wrappers. 
        # A better way is to check the 'infos' buffer if available, or just
        # update based on the episode end.
        
        # Let's update per episode or batch for stability.
        # But 'on_step' is called every step.
        # Let's inspect locals['infos']
        
        infos = self.locals.get("infos", [])
        if infos:
            for info in infos:
                constraints = info.get('constraints', {})
                size_increase = constraints.get('size_increase_pct', 0.0)
                violation = size_increase - CONSTRAINT_SIZE_LIMIT_PCT
                
                # Update Lambda
                # lambda <- lambda + alpha * violation
                # If violation > 0, lambda increases (more penalty)
                # If violation < 0, lambda decreases
                
                new_lambda = self.env_wrapper.lambda_size + self.lr * violation
                self.env_wrapper.lambda_size = max(0.0, new_lambda)
                
                self.logger.record("train/lambda_size", self.env_wrapper.lambda_size)
                self.logger.record("train/size_violation", violation)
                
        return True

def train_advanced():
    run_name = "PPO_Lagrangian_Graph"
    benchmarks = get_benchmark_paths()
    train_benchmarks = benchmarks[:int(len(benchmarks)*0.8)]
    
    # Base Env
    env = CompilerOptEnv(
        benchmark_paths=train_benchmarks, 
        reward_mode=RewardMode.CONSTRAINED
    )
    env = Monitor(env)
    
    # Wrap for Lagrangian
    lag_env = LagrangianRewardWrapper(env, lambda_size=1.0) # Start with some penalty
    
    # Callbacks
    # We need to pass the wrapper instance to the callback
    callback = LagrangianCallback(lag_env, lr=0.05)
    
    print(f"[AGENT] Training PPO-Lagrangian on {len(train_benchmarks)} benchmarks...")
    
    model = PPO(
        "MlpPolicy", 
        lag_env, 
        verbose=1,
        tensorboard_log=str(LOGS_DIR / "tensorboard"),
        learning_rate=3e-4
    )
    
    model.learn(total_timesteps=50000, callback=callback, tb_log_name=run_name)
    
    model.save(MODELS_DIR / f"{run_name}.zip")
    print("[AGENT] Training Complete.")

if __name__ == "__main__":
    train_advanced()
