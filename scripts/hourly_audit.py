import sys
import time
import torch
import subprocess
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.hrl_agent import create_hrl_agent
from src.env import CompilerOptEnv, RewardMode
from src.config import FEATURE_DIM, MODELS_DIR, OPT
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

def run_performance_test(model_path):
    # Setup
    num_macros = len(MACRO_ACTIONS)
    agent = create_hrl_agent(FEATURE_DIM, num_macros, "models/world_model_final.pth")
    agent.load_state_dict(torch.load(model_path, weights_only=True))
    agent.eval()

    test_c = Path("data/real_world_test.c")
    test_ll = Path("data/real_world_test.ll")
    metrics = MetricsCollector()
    
    # 1. Base Time
    env = CompilerOptEnv([str(test_ll)], max_steps=10)
    obs, info = env.reset(options={"ir_path": str(test_ll)})
    base_time = info['initial_runtime_ms']
    
    # 2. Agent Run
    current_time = base_time
    terminated = False
    graph = env.get_observation_graph()
    
    while not terminated:
        x = graph.x; edge_index = graph.edge_index
        batch = torch.zeros(x.size(0), dtype=torch.long)
        
        with torch.no_grad():
            m_probs, _ = agent.get_macro_action(x, edge_index, batch)
            m_idx = torch.argmax(m_probs, dim=-1)
            u_logits = agent.get_micro_action(x, edge_index, batch, m_idx)
            u_idx = torch.argmax(u_logits, dim=-1)
            
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        res = env.executor.apply_passes(env.current_ir_path, final_seq)
        if not res.success: break
        
        env.current_ir_path = res.output_path
        current_time = env.metrics.measure_runtime(env.current_ir_path, iterations=30)
        env.current_step += 1
        terminated = env.current_step >= env.max_steps
        graph = env.get_observation_graph()

    # 3. LLVM -O3 Baseline
    o3_ll = Path("data/real_world_test_o3.ll")
    subprocess.run([str(OPT), "-S", "-O3", str(test_ll), "-o", str(o3_ll)], capture_output=True)
    o3_time = metrics.measure_runtime(str(o3_ll), iterations=30)

    return base_time / max(current_time, 1e-6), base_time / max(o3_time, 1e-6)

def main():
    print("[AUDITOR] Starting Hourly Watcher...")
    seen_models = set()
    
    while True:
        # Look for hourly checkpoints
        models = list(MODELS_DIR.glob("hrl_industrial_hour_*.pth"))
        models.sort(key=lambda x: x.stat().st_mtime)
        
        for m in models:
            if m.name not in seen_models:
                print("\n[AUDITOR] New Checkpoint Detected: {}".format(m.name))
                print("[AUDITOR] Benchmarking performance...")
                try:
                    agent_speedup, o3_speedup = run_performance_test(m)
                    print("="*50)
                    print(" RESULT FOR: {}".format(m.name))
                    print(" HRL Agent Speedup: {:.2f}x".format(agent_speedup))
                    print(" LLVM -O3 Speedup:  {:.2f}x".format(o3_speedup))
                    print(" Delta to -O3:      {:+.2f}x".format(agent_speedup - o3_speedup))
                    print("="*50)
                except Exception as e:
                    print("[AUDITOR] Error during test: {}".format(e))
                seen_models.add(m.name)
        
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    main()
