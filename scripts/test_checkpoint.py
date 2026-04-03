
import sys
import torch
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import get_benchmark_paths, FEATURE_DIM
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def try_checkpoint(checkpoint_path):
    print(f"[TEST] Loading Checkpoint: {checkpoint_path}")
    
    # 1. Setup Environment
    benchmarks = get_benchmark_paths()
    test_samples = random.sample(benchmarks, min(len(benchmarks), 5))
    # Crucial: Use SPEED mode to ensure measurements are actually taken
    env = CompilerOptEnv(test_samples, max_steps=5, reward_mode=RewardMode.SPEED)
    
    # 2. Load Agent
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_final.pth")
    agent.load_state_dict(torch.load(checkpoint_path, weights_only=True))
    agent.eval()
    
    total_speedup = 0
    
    for bc in test_samples:
        print(f"\n[BENCHMARK] {Path(bc).name}")
        # Use options to force specific benchmark
        obs, info = env.reset(options={"ir_path": bc})
        base_runtime = env.prev_runtime
        print(f"  Baseline (-O0) Runtime: {base_runtime:.6f}s")
        
        current_runtime = base_runtime
        for step in range(5):
            graph = env.get_observation_graph()
            if graph is None:
                print("  [WARN] Graph extraction failed, skipping.")
                break
                
            x = graph.x; edge_index = graph.edge_index
            batch_vec = torch.zeros(x.size(0), dtype=torch.long)
            
            with torch.no_grad():
                macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
                m_idx = torch.argmax(macro_probs).item()
                u_logits = agent.get_micro_action(x, edge_index, batch_vec, torch.tensor([m_idx]))
                u_idx = torch.argmax(torch.softmax(u_logits, dim=-1)).item()
            
            base_seq = MACRO_ACTIONS[m_idx]
            final_seq = MicroRefiner.apply_refinement(base_seq, u_idx)
            pipeline = ["module({})".format(",".join(final_seq))]
            
            res = env.executor.apply_passes(env.current_ir_path, pipeline)
            if res.success:
                env.current_ir_path = res.output_path
                new_runtime = env.metrics.measure_runtime(env.current_ir_path, iterations=10)
                if new_runtime > 0:
                    improvement = (current_runtime - new_runtime) / max(current_runtime, 1e-6)
                    print(f"  Step {step+1}: M[{m_idx}] U[{u_idx}] -> Reward: {improvement:.4f}")
                    current_runtime = new_runtime
                else:
                    print(f"  Step {step+1}: Corruption detected.")
                    break
            else:
                print(f"  Step {step+1}: Pass failed. Error: {res.error_message}")
                break
        
        final_improvement = (base_runtime - current_runtime) / max(base_runtime, 1e-6)
        total_speedup += final_improvement
        print(f"  Final Cumulative Speedup: {final_improvement*100:.2f}%")

    print(f"\n[SUMMARY] Average Speedup across sample: {(total_speedup/len(test_samples))*100:.2f}%")

if __name__ == "__main__":
    ckpt = "models/hrl_industrial_hour_0619.pth"
    try_checkpoint(ckpt)
