import sys
from pathlib import Path
import torch
import numpy as np
import random
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS, CLANG
from src.actions.micro_actions import MicroRefiner
from src.passes.metrics import MetricsCollector

NUM_MACROS = len(MACRO_ACTIONS)

HOTSPOTS = [
    "benchmarks/diverse_synthetic/recursive/recursive_0000.c",
    "benchmarks/synthetic/syn_0279.c",
    "benchmarks/diverse_synthetic/struct_heavy/struct_heavy_0191.c",
    "benchmarks/diverse_synthetic/sparse_access/sparse_access_0063.c",
    "benchmarks/diverse_synthetic/pointer_chase/pointer_chase_0067.c"
]

def run_agent(agent, b_path, metrics_collector, max_steps=25):
    env = CompilerOptEnv([b_path], max_steps=max_steps, reward_mode=RewardMode.HACKABLE)
    env.reset()
    
    terminated = False
    episode_steps = 0
    while not terminated and episode_steps < max_steps:
        graph = env.get_observation_graph()
        if graph is None: break
        x = graph.x; edge_index = graph.edge_index; batch_vec = torch.zeros(x.size(0), dtype=torch.long)
        edge_attr = getattr(graph, 'edge_attr', None)
        
        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            m_idx = torch.argmax(macro_probs, dim=-1)
            if m_idx.item() == NUM_MACROS - 1:
                break
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            u_idx = torch.argmax(u_logits, dim=-1)
            
        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success: break
        env.current_ir_path = res.output_path
        episode_steps += 1
        
    runtime = metrics_collector.measure_runtime(env.current_ir_path, iterations=20)
    env.close()
    return runtime

def validate_global_context(live_checkpoint):
    old_checkpoint = "models/hrl_suggestive_hour_1728.pth"
    print(f"\n[VALIDATION] Comparing Baseline (1728) vs Live ({Path(live_checkpoint).name})")
    print(f"[VALIDATION] Focusing on previously failed Global/Struct hotspots...\n")
    
    metrics_collector = MetricsCollector()
    
    agent_old = create_hrl_agent(FEATURE_DIM, NUM_MACROS, "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    agent_old.load_state_dict(torch.load(old_checkpoint, map_location='cpu', weights_only=True))
    agent_old.eval()
    
    agent_live = create_hrl_agent(FEATURE_DIM, NUM_MACROS, "models/world_model_antigravity_v4_L6_checkpoint.pth", gnn_layers=6)
    agent_live.load_state_dict(torch.load(live_checkpoint, map_location='cpu', weights_only=True))
    agent_live.eval()
    
    header = f"{'Benchmark':<30} | {'-O3 (ms)':<10} | {'Old Agent':<10} | {'Live Agent':<10} | {'Delta (%)'}"
    print(header)
    print("-" * len(header))
    
    for b_path in HOTSPOTS:
        if not Path(b_path).exists():
            print(f"[WARN] Benchmark not found: {b_path}")
            continue
        
        # 1. O3 Baseline
        temp_o3 = Path(f"o3_temp_{Path(b_path).stem}.ll")
        subprocess.run([str(CLANG), "-O3", "-S", "-emit-llvm", b_path, "-o", str(temp_o3)], capture_output=True)
        o3_runtime = metrics_collector.measure_runtime(str(temp_o3), iterations=20)
        
        # 2. Old Agent (Pre-Global Context)
        old_runtime = run_agent(agent_old, b_path, metrics_collector)
        
        # 3. Live Agent (With Global Context)
        live_runtime = run_agent(agent_live, b_path, metrics_collector)
        
        if o3_runtime > 0:
            old_sp = o3_runtime / old_runtime
            live_sp = o3_runtime / live_runtime
            delta = (live_sp - old_sp) / old_sp * 100
            print(f"{Path(b_path).name[:30]:<30} | {o3_runtime:10.2f} | {old_sp:9.2f}x | {live_sp:9.2f}x | {delta:+6.1f}%")
        
        if temp_o3.exists(): temp_o3.unlink()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_global_context.py <live_checkpoint>")
        sys.exit(1)
    validate_global_context(sys.argv[1])
