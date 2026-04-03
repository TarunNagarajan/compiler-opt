import sys
from pathlib import Path
import torch
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MODELS_DIR
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def eval_rollout(ckpt_name):
    # Set up environment
    env = CompilerOptEnv(["test_ood_loop.c", "clean_start_bitwise_0104.ll"], max_steps=10, reward_mode=RewardMode.SPEED)
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    
    ckpt_path = Path("models") / ckpt_name
    print(f"Loading {ckpt_path} ...")
    agent.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
    agent.eval()

    terminate_idx = len(MACRO_ACTIONS) - 1

    for i in range(2):
        print(f"\n--- Episode {i+1} ---")
        obs, info = env.reset()
        print(f"Program: {Path(info['ir_path']).name}")
        
        step = 0
        terminated = False
        while not terminated and step < 10:
            graph = env.get_observation_graph()
            x = graph.x
            edge_index = graph.edge_index
            edge_attr = getattr(graph, 'edge_attr', None)
            batch_vec = torch.zeros(x.size(0), dtype=torch.long)
            
            with torch.no_grad():
                macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
                m_idx = torch.distributions.Categorical(macro_probs).sample().item()
                m_probs_np = macro_probs[0].numpy()
                top_m_idx = np.argmax(m_probs_np)
                stop_prob = m_probs_np[terminate_idx]
                
            print(f"  Step {step}:")
            print(f"    STOP Prob: {stop_prob*100:.2f}% (Action {terminate_idx})")
            print(f"    Sampled Macro Action: {m_idx} ({'TERMINATE' if m_idx == terminate_idx else MACRO_ACTIONS[m_idx][0]})")
            
            if m_idx == terminate_idx:
                print(f"    >>> Agent chose to STOP at step {step}.")
                terminated = True
                break
                
            # If not stop, get micro action
            with torch.no_grad():
                u_logits = agent.get_micro_action(x, edge_index, batch_vec, torch.tensor([m_idx]), edge_attr=edge_attr, graph_data=graph)
                u_idx = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).sample().item()
            
            print(f"    Sampled Micro Action: {u_idx}")
            
            base_seq = MACRO_ACTIONS[m_idx]
            final_seq = MicroRefiner.apply_refinement(base_seq, u_idx)
            pipeline = [f"module({','.join(final_seq)})"]
            
            res = env.executor.apply_passes(env.current_ir_path, pipeline)
            if not res.success:
                print("    >>> Pass failed. End episode.")
                terminated = True
            else:
                env.current_ir_path = res.output_path
                print("    >>> Pass applied successfully.")
                
            step += 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, default="hrl_antigravity_v4_hrl_hour_1656.pth")
    args = parser.parse_args()
    eval_rollout(args.ckpt)
