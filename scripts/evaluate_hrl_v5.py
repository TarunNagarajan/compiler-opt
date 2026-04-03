import sys
import time
import torch
import argparse
import psutil
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import FEATURE_DIM, NUM_ACTIONS, MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

NUM_MACROS = len(MACRO_ACTIONS)

def get_ram_usage():
    """Returns the current RAM usage of the process in MB."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def evaluate_checkpoint(checkpoint_path, world_model_path, test_file, max_steps, deterministic, top_k=3):
    checkpoint_path = Path(checkpoint_path)
    print(f"\n[EVAL] Testing Checkpoint: {checkpoint_path.name}")
    
    # Measure RAM before loading agent
    ram_start = get_ram_usage()
    
    agent = create_hrl_agent_v5(FEATURE_DIM, NUM_MACROS, world_model_path=world_model_path)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if isinstance(ckpt, dict) and 'model_state_dict' in ckpt:
        agent.load_state_dict(ckpt['model_state_dict'])
        step_info = f" (step {ckpt.get('current_step', '?')})"
    else:
        agent.load_state_dict(ckpt)
        step_info = " (legacy)"
    agent.eval()
    
    # RAM after agent load
    ram_agent_loaded = get_ram_usage()
    
    env = CompilerOptEnv([test_file], max_steps=max_steps, reward_mode=RewardMode.SPEED)
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    # Measure initial runtime
    print("  Measuring initial runtime...", end="", flush=True)
    initial_runtime = env.metrics.measure_runtime(env.original_ir_path, iterations=10)
    print(f" {initial_runtime:.4f}s")
    
    # We need to manage the history manually for v5 agent during evaluation
    episode_action_history = []
    
    initial_instructions = info.get('initial_instructions', 0)
    print(f"  Initial Instructions: {initial_instructions}")
    
    current_runtime = initial_runtime
    
    total_reward = 0.0
    recent_macros = []  # Track recent macros for throttling
    
    device = next(agent.parameters()).device
    
    ram_peaks = [ram_agent_loaded]

    for step in range(max_steps):
        # Prepare graph data with action history
        MAX_STEPS = 25
        padded_history = torch.zeros(1, MAX_STEPS, dtype=torch.long)
        if episode_action_history:
            seq = torch.tensor(episode_action_history, dtype=torch.long)
            if len(seq) > MAX_STEPS: seq = seq[-MAX_STEPS:]
            padded_history[0, :len(seq)] = seq
        graph.action_history = padded_history
        
        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None:
            edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            macro_probs, agent_weights = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)
            
            # --- ACTION SAMPLING (Temperature + Top-K) ---
            temperature = 0.7
            
            # Apply temperature to logits before softmax
            macro_logits = torch.log(macro_probs + 1e-8) / temperature
            
            if deterministic:
                # Top-K Sampling
                top_k_logits, top_k_indices = torch.topk(macro_logits, min(top_k, macro_logits.size(-1)))
                
                # Apply throttling to the top-k subset
                if len(recent_macros) >= 2:
                    last_2 = recent_macros[-2:]
                    if all(m == last_2[0] for m in last_2):
                        # Find if last_2 is in top_k
                        for i in range(top_k_indices.size(1)):
                            if top_k_indices[0, i].item() == last_2[0]:
                                top_k_logits[0, i] -= 10.0 # Strongly penalize
                    if len(recent_macros) >= 3:
                        last_3 = recent_macros[-3:]
                        if all(m == last_3[0] for m in last_3):
                            for i in range(top_k_indices.size(1)):
                                if top_k_indices[0, i].item() == last_3[0]:
                                    top_k_logits[0, i] -= 100.0 # Block completely
                                    
                # Re-normalize and sample from top-K
                top_k_probs = torch.softmax(top_k_logits, dim=-1)
                selected_idx = torch.distributions.Categorical(top_k_probs).sample()
                m_idx = top_k_indices[0, selected_idx.item()]
                m_idx_tensor = torch.tensor([m_idx.item()], device=device)
            else:
                m_idx = torch.distributions.Categorical(macro_probs).sample()
                m_idx_tensor = m_idx.clone().detach()
            
            recent_macros.append(m_idx.item())
            if len(recent_macros) > 5: recent_macros.pop(0)
            
            # Record action in history
            episode_action_history.append(m_idx.item() + 1)
            
            if m_idx.item() == NUM_MACROS - 1: # STOP
                print(f"  Step {step+1}: Agent Selected STOP")
                break
                
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx_tensor, edge_attr=edge_attr, graph_data=graph)
            
            if deterministic:
                u_logits_temp = u_logits / temperature
                top_k_u_logits, top_k_u_indices = torch.topk(u_logits_temp, min(top_k, u_logits.size(-1)))
                top_k_u_probs = torch.softmax(top_k_u_logits, dim=-1)
                selected_u_idx = torch.distributions.Categorical(top_k_u_probs).sample()
                u_idx = top_k_u_indices[0, selected_u_idx.item()]
            else:
                u_idx = torch.distributions.Categorical(torch.softmax(u_logits, dim=-1)).sample()
            
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]
        
        # Display weights (Specialist focus)
        # agent_weights is [batch, 3] -> [Bias, Speed_Specialist, Size_Specialist]
        w_speed = agent_weights[0, 1].item()
        w_size = agent_weights[0, 2].item()
        
        # Apply passes
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            print(f"  Step {step+1}: [FAILED]")
            break
            
        env.current_ir_path = res.output_path
        
        # Extract new graph and metrics
        from src.features.ir_graph_extractor import IRGraphExtractor
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None: break
        graph = extractor.to_pyg_data(new_g)
        
        metrics_collector = MetricsCollector()
        inst_after = metrics_collector.count_instructions(str(env.current_ir_path))
        
        # Measure runtime after this step
        runtime_after = env.metrics.measure_runtime(env.current_ir_path, iterations=5)
        
        ram_peaks.append(get_ram_usage())
        
        print(f"  Step {step+1}: M[{m_idx.item()}] U[{u_idx.item()}] -> Inst: {inst_after} ({(initial_instructions - inst_after)/max(initial_instructions, 1)*100:+.1f}%), Time: {runtime_after:.4f}s ({(initial_runtime - runtime_after)/max(initial_runtime, 1e-6)*100:+.1f}%)")
        print(f"    [Weights] Speed Focus: {w_speed:.2f} | Size Focus: {w_size:.2f}")
        current_runtime = runtime_after
        
    final_inst = metrics_collector.count_instructions(str(env.current_ir_path))
    final_runtime = env.metrics.measure_runtime(env.current_ir_path, iterations=10)
    
    instr_improvement = (initial_instructions - final_inst) / max(initial_instructions, 1) * 100
    speedup = (initial_runtime - final_runtime) / max(initial_runtime, 1e-6) * 100
    
    print(f"  Final Speedup (Time): {speedup:.2f}%")
    print(f"  Final Reduction (Inst): {instr_improvement:.2f}%")
    print(f"  RAM Usage: Init={ram_start:.1f}MB, Loaded={ram_agent_loaded:.1f}MB, Peak={max(ram_peaks):.1f}MB")
    
    return {
        'name': checkpoint_path.name,
        'speedup': speedup,
        'instr_reduction': instr_improvement,
        'ram_peak': max(ram_peaks),
        'steps': len(episode_action_history)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints", nargs='+', required=True, help="List of HRL v5 checkpoints")
    parser.add_argument("--world_model", type=str, required=True, help="Path to v5 world model")
    parser.add_argument("--file", type=str, required=True, help="C file to optimize")
    parser.add_argument("--max_steps", type=int, default=15)
    parser.add_argument("--deterministic", action="store_true")
    parser.add_argument("--top_k", type=int, default=3, help="Top-K for deterministic sampling (K=1 is equivalent to pure argmax without throttling)")
    args = parser.parse_args()
    
    test_file = Path(args.file).resolve()
    if not test_file.exists():
        print(f"File not found: {test_file}")
        return

    results = []
    for cp in args.checkpoints:
        res = evaluate_checkpoint(cp, args.world_model, test_file, args.max_steps, args.deterministic, args.top_k)
        results.append(res)
        
    print("\n" + "="*80)
    print(f"{'Checkpoint':<40} | {'Speedup':<8} | {'Inst Red':<8} | {'RAM Peak':<10}")
    print("-" * 80)
    for r in results:
        print(f"{r['name']:<40} | {r['speedup']:>7.2f}% | {r['instr_reduction']:>7.2f}% | {r['ram_peak']:>7.1f} MB")
    print("="*80)

if __name__ == "__main__":
    main()
