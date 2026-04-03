import sys
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

def trace_with_diversity(checkpoint, file_path):
    NUM_MACROS = len(MACRO_ACTIONS)
    # The new hrl_agent.py handles the world model resize automatically
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    
    # Load the TRANSPLANTED checkpoint which matches the 18-macro size
    agent.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    metrics_collector = MetricsCollector()
    env = CompilerOptEnv([file_path], max_steps=25, reward_mode=RewardMode.HACKABLE)
    obs, info = env.reset()
    
    print(f"\n[TRACE] File: {file_path}")
    print(f"Mandatory Canon nodes: {env.get_observation_graph().num_nodes}")
    
    initial_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=5)
    print(f"Post-Canonicalization Runtime: {initial_runtime:.2f}ms")
    
    step = 0
    recent_macros = []
    while step < 25:
        graph = env.get_observation_graph()
        x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
        edge_attr = getattr(graph, 'edge_attr', None)
        
        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            
            # HARSH THROTTLING
            if len(recent_macros) >= 2:
                last_2 = recent_macros[-2:]
                if all(m == last_2[0] for m in last_2):
                    macro_probs[0, last_2[0]] *= 0.01 
                    macro_probs = macro_probs / macro_probs.sum()
            
            m_idx = torch.argmax(macro_probs, dim=-1)
            
            if m_idx.item() == NUM_MACROS - 1:
                print(f"Step {step}: TERMINATE")
                break
                
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            u_idx = torch.argmax(u_logits, dim=-1)
            
        recent_macros.append(m_idx.item())
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        print(f"Step {step}: Macro[{m_idx.item()}] Micro[{u_idx.item()}] -> {final_seq}")
        
        pipeline = [f"module({','.join(final_seq)})"]
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success: break
        env.current_ir_path = res.output_path
        step += 1
    
    agent_runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=20)
    print(f"\nFinal Agent Runtime (FERRARI): {agent_runtime:.2f}ms")
    print(f"Speedup vs Canon: {initial_runtime / agent_runtime:.2f}x")
    env.close()

if __name__ == "__main__":
    trace_with_diversity("models/hrl_suggestive_v5_ferrari.pth", "data/real_world_test.c")
