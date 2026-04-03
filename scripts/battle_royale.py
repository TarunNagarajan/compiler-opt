
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from stable_baselines3 import PPO

from src.env import CompilerOptEnv, RewardMode
from src.models import create_world_model
from src.config import FEATURE_DIM, NUM_ACTIONS, CLANG, OPT, LLVM_BIN_DIR, MODELS_DIR
from src.passes.pass_executor import compile_to_ir, PassExecutor
from src.passes.metrics import MetricsCollector

class WorldModelAgent:
    def __init__(self, model_path):
        self.model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.eval()
        
    def predict(self, env):
        graph = env.get_observation_graph()
        if graph is None: return env.action_space.sample()
        best_action, best_delta = 0, 1.0
        with torch.no_grad():
            x, edge_index = graph.x, graph.edge_index
            batch = torch.zeros(x.size(0), dtype=torch.long)
            for a in range(NUM_ACTIONS):
                _, metrics = self.model(x, edge_index, batch, torch.tensor([a]))
                if metrics[0, 0].item() < best_delta:
                    best_delta = metrics[0, 0].item()
                    best_action = a
        return best_action

import time

def measure_execution_speed(ir_path, iterations=100):
    from src.config import CLANG
    import tempfile
    
    # Use a short stable path to avoid Windows "path too long" error
    temp_dir = Path(tempfile.gettempdir())
    exe_path = temp_dir / "battle_temp.exe"
    
    # Compile IR to Binary
    subprocess.run([str(CLANG), str(ir_path), "-o", str(exe_path), "-lm"], capture_output=True)
    
    if not exe_path.exists():
        print(f"Failed to compile {ir_path}")
        return 0.0
    
    # Measure
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        subprocess.run([str(exe_path)], capture_output=True)
        times.append((time.perf_counter() - start) * 1000)
    
    return np.mean(times) # Average ms

def run_battle():
    source_c = Path("data/real_world_test.c")
    base_ll = Path("data/real_world_test.ll")
    
    # 1. Compile to base IR
    print(f"[BATTLE] Compiling {source_c} to base IR...")
    success, base_ll_str = compile_to_ir(str(source_c), output_path=str(base_ll))
    if not success:
        print(f"Compilation Failed: {base_ll_str}")
        return
    base_ll = Path(base_ll_str)
    
    metrics = MetricsCollector()
    initial_instr = metrics.count_instructions(str(base_ll))
    print(f"Initial Instructions: {initial_instr}")
    initial_speed = measure_execution_speed(base_ll)

    # 2. RUN LLVM -O3
    print("[BATTLE] Running LLVM -O3...")
    o3_ll = Path("data/real_world_test_o3.ll")
    subprocess.run([str(OPT), "-S", "-O3", str(base_ll), "-o", str(o3_ll)], capture_output=True)
    o3_instr = metrics.count_instructions(str(o3_ll))
    o3_speed = measure_execution_speed(o3_ll)
    
    # 3. RUN PPO-SECURE
    print("[BATTLE] Running PPO-Secure...")
    ppo_s = PPO.load("models/ppo_secure.zip")
    env = CompilerOptEnv([str(base_ll)], max_steps=10)
    obs, info = env.reset(options={"ir_path": str(base_ll)})
    terminated = False
    while not terminated:
        action, _ = ppo_s.predict(obs, deterministic=True)
        obs, _, terminated, _, _ = env.step(action)
    ppo_instr = metrics.count_instructions(env.current_ir_path)
    ppo_speed = measure_execution_speed(env.current_ir_path)
    
    # 4. RUN WORLD MODEL GREEDY
    print("[BATTLE] Running World-Model-Greedy (final)...")
    wm_agent = WorldModelAgent("models/world_model_final.pth")
    obs, info = env.reset(options={"ir_path": str(base_ll)})
    terminated = False
    while not terminated:
        action = wm_agent.predict(env)
        obs, _, terminated, _, _ = env.step(action)
    wm_instr = metrics.count_instructions(env.current_ir_path)
    wm_speed = measure_execution_speed(env.current_ir_path)

    # REPORT
    print("\n" + "="*85)
    header = "{:<25} | {:<12} | {:<12} | {:<12} | {:<12}".format(
        "Strategy", "Instr Count", "Instr Reduc", "Avg Time(ms)", "Speedup"
    )
    print(header)
    print("-" * 85)
    
    def print_row(name, instr, time_ms, base_time):
        speedup = base_time/time_ms if time_ms > 0 else 0
        print("{:<25} | {:<12} | {:11.2%} | {:12.4f} | {:11.2f}x".format(
            name, instr, (initial_instr-instr)/initial_instr, time_ms, speedup
        ))

    print_row("Original (-O0)", initial_instr, initial_speed, initial_speed)
    print_row("LLVM -O3", o3_instr, o3_speed, initial_speed)
    print_row("PPO-Secure", ppo_instr, ppo_speed, initial_speed)
    print_row("World-Model-Greedy", wm_instr, wm_speed, initial_speed)
    print("="*85)

if __name__ == "__main__":
    run_battle()
