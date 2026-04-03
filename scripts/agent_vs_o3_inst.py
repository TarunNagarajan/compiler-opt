import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode

from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import FEATURE_DIM, NUM_ACTIONS, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
import torch

if len(sys.argv) < 3:
    print("Usage: python agent_vs_o3_inst.py <checkpoint_path> <benchmark1> <benchmark2> ...")
    sys.exit(1)

checkpoint_path = sys.argv[1]
files = sys.argv[2:]

world_model_path = "models/world_model_v5_sprint_checkpoint.pth"
agent = create_hrl_agent_v5(FEATURE_DIM, len(MACRO_ACTIONS), world_model_path=world_model_path)
ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
agent.load_state_dict(ckpt['model_state_dict'])
agent.eval()
device = next(agent.parameters()).device

print(f"{'Benchmark':<30} | {'Agent Inst%':<12} | {'O2 Inst%':<10} | {'O3 Inst%':<10}")
print("-" * 70)

for f in files:
    stem = os.path.basename(f).replace('.c', '')
    
    # 1. Measure O2 / O3 baseline via env tools
    env = CompilerOptEnv([f], max_steps=1, reward_mode=RewardMode.SPEED)
    env.reset()
    m = env.metrics
    c0 = m.count_instructions(str(env.original_ir_path))
    
    res_o2 = env.executor.apply_passes(env.original_ir_path, ["default<O2>"])
    c2 = m.count_instructions(str(res_o2.output_path))
    
    res_o3 = env.executor.apply_passes(env.original_ir_path, ["default<O3>"])
    c3 = m.count_instructions(str(res_o3.output_path))
    
    r2 = (c0 - c2) / c0 * 100
    r3 = (c0 - c3) / c0 * 100
    
    # 2. Evaluate Agent
    obs, info = env.reset()
    graph = env.get_observation_graph()
    episode_action_history = []
    recent_macros = []
    
    for step in range(25):
        padded_history = torch.zeros(1, 25, dtype=torch.long)
        if episode_action_history:
            seq = torch.tensor(episode_action_history, dtype=torch.long)
            if len(seq) > 25: seq = seq[-25:]
            padded_history[0, :len(seq)] = seq
        graph.action_history = padded_history
        
        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None: edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
            temperature = 0.7
            macro_logits = torch.log(macro_probs + 1e-8) / temperature
            top_k_logits, top_k_indices = torch.topk(macro_logits, min(3, macro_logits.size(-1)))
            
            if len(recent_macros) >= 2:
                last_2 = recent_macros[-2:]
                if all(m == last_2[0] for m in last_2):
                    for i in range(top_k_indices.size(1)):
                        if top_k_indices[0, i].item() == last_2[0]: top_k_logits[0, i] -= 10.0
                if len(recent_macros) >= 3:
                    last_3 = recent_macros[-3:]
                    if all(m == last_3[0] for m in last_3):
                        for i in range(top_k_indices.size(1)):
                            if top_k_indices[0, i].item() == last_3[0]: top_k_logits[0, i] -= 100.0
            
            top_k_probs = torch.softmax(top_k_logits, dim=-1)
            selected_idx = torch.distributions.Categorical(top_k_probs).sample()
            m_idx = top_k_indices[0, selected_idx.item()]
            m_idx_tensor = torch.tensor([m_idx.item()], device=device)
            
            recent_macros.append(m_idx.item())
            if len(recent_macros) > 5: recent_macros.pop(0)
            episode_action_history.append(m_idx.item() + 1)
            
            if m_idx.item() == len(MACRO_ACTIONS) - 1: break
            
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx_tensor, edge_attr=edge_attr, graph_data=graph)
            u_logits_temp = u_logits / temperature
            top_k_u_logits, top_k_u_indices = torch.topk(u_logits_temp, min(3, u_logits.size(-1)))
            top_k_u_probs = torch.softmax(top_k_u_logits, dim=-1)
            selected_u_idx = torch.distributions.Categorical(top_k_u_probs).sample()
            u_idx = top_k_u_indices[0, selected_u_idx.item()]
            
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]
        
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success: break
        env.current_ir_path = res.output_path
        
        from src.features.ir_graph_extractor import IRGraphExtractor
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None: break
        graph = extractor.to_pyg_data(new_g)
        
    c_agent = m.count_instructions(str(env.current_ir_path))
    r_agent = (c0 - c_agent) / c0 * 100
    
    print(f"{stem:<30} | {r_agent:>11.2f}% | {r2:>9.2f}% | {r3:>9.2f}%")
