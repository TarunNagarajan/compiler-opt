import sys
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def trace_agent_choices(checkpoint, file_path):
    NUM_MACROS = len(MACRO_ACTIONS)
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    agent.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True))
    agent.eval()
    
    env = CompilerOptEnv([file_path], max_steps=25, reward_mode=RewardMode.HACKABLE)
    obs, info = env.reset()
    
    print(f"\n[TRACE] File: {file_path}")
    graph = env.get_observation_graph()
    print(f"Initial State Graph Nodes: {graph.num_nodes}")
    
    terminated = False
    step = 0
    while not terminated and step < 25:
        graph = env.get_observation_graph()
        x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
        edge_attr = getattr(graph, 'edge_attr', None)
        
        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            m_idx = torch.argmax(macro_probs, dim=-1)
            
            if m_idx.item() == NUM_MACROS - 1:
                print(f"Step {step}: TERMINATE")
                break
                
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            u_idx = torch.argmax(u_logits, dim=-1)
            
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        print(f"Step {step}: Macro[{m_idx.item()}] Micro[{u_idx.item()}] -> {final_seq}")
        
        pipeline = [f"module({','.join(final_seq)})"]
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            print("FAILED")
            break
        env.current_ir_path = res.output_path
        step += 1
    
    final_path = Path("data/real_world_agent_final.ll")
    import shutil
    shutil.copy(env.current_ir_path, final_path)
    print(f"\nFinal IR saved to {final_path}")
    env.close()

if __name__ == "__main__":
    trace_agent_choices("models/hrl_suggestive_hour_1923.pth", "data/real_world_test.c")
