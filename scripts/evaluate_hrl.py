import sys
from pathlib import Path
import torch
import argparse
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, LLVM_PASSES, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

NUM_MACROS = len(MACRO_ACTIONS)

def evaluate(args):
    print(f"\n[EVAL] Loading HRL Agent: {args.checkpoint}...")
    
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    test_file = Path(args.file).resolve()
    if not test_file.exists():
        print(f"[ERROR] Test file not found: {test_file}")
        return
        
    print(f"\n[EVAL] Target: {test_file.name}")
    print("-" * 60)
    
    env = CompilerOptEnv([test_file], max_steps=15, reward_mode=RewardMode.SPEED)
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    initial_instructions = info.get('initial_instructions', 0)
    initial_size = info.get('initial_size', 0)
    
    print(f"Initial State:\n  Instructions: {initial_instructions}\n  Size: {initial_size} bytes\n")
    
    total_reward = 0.0
    optimization_sequence = []
    recent_macros = []
    
    device = next(agent.parameters()).device

    for step in range(args.max_steps):
        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None:
            edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            macro_probs, agent_weights = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            
            # --- HARSH ACTION THROTTLING (Ferrari Upgrade) ---
            if len(recent_macros) >= 2:
                last_2 = recent_macros[-2:]
                if all(m == last_2[0] for m in last_2):
                    macro_probs[0, last_2[0]] *= 0.1
                
                if len(recent_macros) >= 3:
                    last_3 = recent_macros[-3:]
                    if all(m == last_3[0] for m in last_3):
                        macro_probs[0, last_3[0]] = 0.0
            
            macro_probs = macro_probs / (macro_probs.sum() + 1e-8)

            # Use argmax instead of sampling for deterministic evaluation
            if args.deterministic:
                m_idx = torch.argmax(macro_probs, dim=-1)
            else:
                m_idx = torch.distributions.Categorical(macro_probs).sample()
            
            recent_macros.append(m_idx.item())
            if len(recent_macros) > 5: recent_macros.pop(0)

            print(f"  -> [DEBUG] Top 3 Macro Probs: {torch.topk(macro_probs, 3).values.squeeze().tolist()} at indices {torch.topk(macro_probs, 3).indices.squeeze().tolist()}")
                
            # STOP condition
            terminate_idx = NUM_MACROS - 1
            if m_idx.item() == terminate_idx:
                print(f"Step {step+1}: [Agent Selected STOP] -> IGNORING (Force Continue)")
                # Sample the next best if we ignore stop (just for testing logic)
                macro_probs[0, terminate_idx] = -float('inf')
                m_idx = torch.argmax(macro_probs, dim=-1) if args.deterministic else torch.distributions.Categorical(torch.softmax(macro_probs, dim=-1)).sample()
                
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            
            if args.deterministic:
                u_idx = torch.argmax(u_logits, dim=-1)
            else:
                u_idx = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).sample()
                
        # Format the chosen action
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]
        
        action_name = f"Macro {m_idx.item()} + Mod {u_idx.item()}"
        optimization_sequence.extend(final_seq)
        
        # Display Agent Thoughts
        w_perf = agent_weights[0, 1].item()
        w_size = agent_weights[0, 2].item()
        
        print(f"Step {step+1}: Action: {action_name}")
        print(f"  -> Passes: {final_seq}")
        print(f"  -> Weight Focus: Speed={w_perf:.2f}, Size={w_size:.2f}")
        
        # Apply the passes
        print(f"  -> Applying passes... ", end="", flush=True)
        runtime_before = env.prev_runtime
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        
        if not res.success:
            print("[FAILED]")
            break
            
        env.current_ir_path = res.output_path
        
        # We need to manually update the graph using the extractor to get the next step's metrics
        from src.features.ir_graph_extractor import IRGraphExtractor
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None or new_g.number_of_nodes() == 0:
            print("[FAILED TO EXTRACT GRAPH]")
            break
            
        new_graph = extractor.to_pyg_data(new_g)
        
        env.current_ir_path_size = test_file.stat().st_size
        
        # Compute rewards simply for display via differences in instruction count
        metrics_collector = MetricsCollector()
        inst_after = metrics_collector.count_instructions(str(env.current_ir_path))
        
        inst_improvement = initial_instructions - inst_after
        inst_pct = (inst_improvement / initial_instructions * 100) if initial_instructions > 0 else 0
        
        print(f"[SUCCESS]")
        print(f"  -> Resulting Instructions: {inst_after} ({inst_pct:+.1f}%)")
        print("-" * 60)
        
        graph = new_graph
        graph.x = graph.x.to(device)
        graph.edge_index = graph.edge_index.to(device)
        
    print("\n[EVAL] Optimization Complete!")
    print(f"Final Pipeline length: {len(optimization_sequence)} passes")
    print(f"Final Pipeline: {','.join(optimization_sequence)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the dummy test file")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to HRL trained model .pth")
    parser.add_argument("--world_model", type=str, required=True, help="Path to the associated world model .pth")
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--max_steps", type=int, default=10, help="Max passes to apply")
    parser.add_argument("--deterministic", action="store_true", help="Use argmax instead of sampling")
    args = parser.parse_args()
    evaluate(args)
