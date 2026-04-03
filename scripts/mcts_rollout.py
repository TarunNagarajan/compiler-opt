import sys
import torch
import argparse
import time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.features.ir_graph_extractor import IRGraphExtractor
from src.passes.metrics import MetricsCollector
from src.config import FEATURE_DIM, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.models.mcts import MCTS

NUM_MACROS = len(MACRO_ACTIONS)

def format_policy(policy):
    out = ""
    top_indices = np.argsort(policy)[::-1][:3]
    for idx in top_indices:
        if policy[idx] > 0.01:
            out += f"M[{idx}]: {policy[idx]*100:.1f}% | "
    return out

def run_mcts(args):
    print(f"\n[MCTS] Loading Phase 2 Architecture...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.to(device)
    agent.eval()
    
    test_file = Path(args.file).resolve()
    if not test_file.exists():
        print(f"[ERROR] Test file not found: {test_file}")
        return
        
    print(f"\n[MCTS] Target: {test_file.name}")
    print(f"[MCTS] Tree Search Simulating {args.simulations} paths per step...")
    print("-" * 60)
    
    env = CompilerOptEnv([test_file], max_steps=args.max_steps, reward_mode=RewardMode.SPEED)
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    initial_instructions = info.get('initial_instructions', 0)
    print(f"Initial State:\n  Instructions: {initial_instructions}")
    
    optimization_sequence = []
    
    for step in range(args.max_steps):
        print(f"\nStep {step+1}:")
        
        # 1. Initialize MCTS for current state
        mcts = MCTS(agent, num_simulations=args.simulations, c_puct=1.5, num_macros=NUM_MACROS)
        
        # 2. Run MCTS Simulations in Latent Space
        start_time = time.time()
        mcts_policy = mcts.search(graph, device=device)
        print(f"  -> Simulated {args.simulations} paths in {(time.time() - start_time)*1000:.1f}ms")
        print(f"  -> Policy: {format_policy(mcts_policy)}")
        
        # 3. Select Action (Deterministically grabbing the most visited mode)
        m_idx_val = np.argmax(mcts_policy)
        
        # Stop condition
        if m_idx_val == NUM_MACROS - 1:
            print(f"  -> [MCTS Selected STOP]")
            break
            
        m_idx = torch.tensor(m_idx_val, dtype=torch.long, device=device).unsqueeze(0)
        
        # We rely on the single-step actor for the micro-action tuning
        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None: edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            u_idx_val = torch.argmax(u_logits, dim=-1).item()
            
        base_seq = MACRO_ACTIONS[m_idx_val]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx_val)
        pipeline = [f"module({','.join(final_seq)})"]
        optimization_sequence.extend(final_seq)
        
        print(f"  -> Executing: Macro {m_idx_val} + Mod {u_idx_val}")
        print(f"     Passes: {final_seq}")
        
        # Apply to precise physical environment
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            print("  -> [MCTS SELECTION FAILED COMPILATION]")
            break
            
        env.current_ir_path = res.output_path
        
        # Re-extract graph for the next exact physical root state
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None or new_g.number_of_nodes() == 0:
            print("  -> [FAILED TO EXTRACT NEXT GRAPH]")
            break
            
        graph = extractor.to_pyg_data(new_g)

    metrics_collector = MetricsCollector()
    inst_after = metrics_collector.count_instructions(str(env.current_ir_path))
    inst_improvement = initial_instructions - inst_after
    
    print("\n========================================================")
    print("[MCTS] Rollout Complete!")
    print(f"Final Instructions: {inst_after} (Saved {inst_improvement} instructions)")
    print(f"Final Pipeline length: {len(optimization_sequence)} passes")
    print(f"Final Pipeline: {','.join(optimization_sequence)}")
    print("========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the .c file")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to HRL trained model .pth")
    parser.add_argument("--world_model", type=str, required=True, help="Path to the associated world model .pth")
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--max_steps", type=int, default=10)
    parser.add_argument("--simulations", type=int, default=200, help="Number of MCTS tree expansions per step")
    args = parser.parse_args()
    run_mcts(args)
