import sys
from pathlib import Path
import torch
import numpy as np
import random

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, get_benchmark_paths
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def check_pass_counts(ckpt_names):
    benchmarks = get_benchmark_paths()
    random.seed(42)
    test_benchmarks = random.sample(benchmarks, 10)  # Reduced to 10 for faster evaluation across multiple ckpts
    
    env = CompilerOptEnv(test_benchmarks, max_steps=25, reward_mode=RewardMode.SPEED)
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    
    for ckpt_name in ckpt_names:
        ckpt_path = Path("models") / ckpt_name
        if not ckpt_path.exists():
            print(f"\nSkipping {ckpt_name} (Not found)")
            continue
            
        agent.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
        agent.eval()

        terminate_idx = len(MACRO_ACTIONS) - 1

        print(f"\n========================================================================================")
        print(f"Evaluating {ckpt_name} over 10 benchmarks...")
        print(f"{'Benchmark':<45} | {'Num Passes':<10} | {'Action if stopped on Step 0'}")
        print("-" * 88)

        for b in test_benchmarks:
            # Force the environment to use this specific benchmark
            env = CompilerOptEnv([b], max_steps=25, reward_mode=RewardMode.SPEED)
            obs, info = env.reset()
            
            step = 0
            terminated = False
            first_step_m_idx = None
            while not terminated and step < 25:
                graph = env.get_observation_graph()
                x = graph.x
                edge_index = graph.edge_index
                edge_attr = getattr(graph, 'edge_attr', None)
                batch_vec = torch.zeros(x.size(0), dtype=torch.long)
                
                with torch.no_grad():
                    macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
                    m_idx = torch.argmax(macro_probs[0]).item()
                
                if step == 0:
                    first_step_m_idx = m_idx
                    
                if m_idx == terminate_idx:
                    terminated = True
                    break
                    
                with torch.no_grad():
                    u_logits = agent.get_micro_action(x, edge_index, batch_vec, torch.tensor([m_idx]), edge_attr=edge_attr, graph_data=graph)
                    u_idx = torch.argmax(u_logits[0]).item()
                
                base_seq = MACRO_ACTIONS[m_idx]
                final_seq = MicroRefiner.apply_refinement(base_seq, u_idx)
                pipeline = [f"module({','.join(final_seq)})"]
                
                res = env.executor.apply_passes(env.current_ir_path, pipeline)
                if not res.success:
                    terminated = True
                else:
                    env.current_ir_path = res.output_path
                
                step += 1
                
            print(f"{b.name:<45} | {step:<10} | {'TERMINATE' if step == 0 and first_step_m_idx == terminate_idx else 'N/A'}")

if __name__ == "__main__":
    checkpoints_to_test = [
        "hrl_antigravity_v4_hrl_hour_0048.pth",
        "hrl_antigravity_v4_hrl_hour_1430.pth",
        "hrl_antigravity_v4_hrl_hour_1656.pth", 
        "hrl_antigravity_v4_hrl_hour_1804.pth",
        "hrl_antigravity_v4_hrl_hour_2134.pth"
    ]
    check_pass_counts(checkpoints_to_test)
