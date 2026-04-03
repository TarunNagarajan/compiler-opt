
import sys
import torch
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent import create_hrl_agent
from src.config import get_benchmark_paths, FEATURE_DIM
from src.actions.macro_actions import MACRO_ACTIONS
from src.actions.micro_actions import MicroRefiner

def compare_to_o3(checkpoint_path):
    print(f"=== BATTLE: HRL (Hour 06) vs. LLVM -O3 ===")
    benchmarks = get_benchmark_paths()
    test_samples = [
        "benchmarks/mibench/mibench-master/telecomm/adpcm/src/rawcaudio.c", 
        "benchmarks/mibench/mibench-master/network/dijkstra/dijkstra_small.c"
    ]
    
    env = CompilerOptEnv(benchmarks, max_steps=10, reward_mode=RewardMode.SPEED)
    agent = create_hrl_agent(FEATURE_DIM, len(MACRO_ACTIONS), "models/world_model_final.pth")
    agent.load_state_dict(torch.load(checkpoint_path, weights_only=True))
    agent.eval()

    for bc in test_samples:
        if not Path(bc).exists(): continue
        print(f"\n[BENCHMARK] {Path(bc).name}")
        
        # 1. Measure -O3
        temp_o3 = "temp_o3.ll"
        subprocess.run(f"clang -O3 -S -emit-llvm {bc} -o {temp_o3}", shell=True, capture_output=True)
        runtime_o3 = env.metrics.measure_runtime(temp_o3, iterations=20)
        
        # 2. Measure HRL
        obs, info = env.reset(options={"ir_path": bc})
        runtime_o0 = env.prev_runtime
        current_ir = env.current_ir_path
        
        for step in range(5):
            graph = env.get_observation_graph()
            if graph is None: break
            x = graph.x; edge_index = graph.edge_index
            batch_vec = torch.zeros(x.size(0), dtype=torch.long)
            
            with torch.no_grad():
                macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec)
                m_idx = torch.argmax(macro_probs).item()
                u_logits = agent.get_micro_action(x, edge_index, batch_vec, torch.tensor([m_idx]))
                u_idx = torch.argmax(u_logits).item()
            
            base_seq = MACRO_ACTIONS[m_idx]
            final_seq = MicroRefiner.apply_refinement(base_seq, u_idx)
            res = env.executor.apply_passes(current_ir, ["module({})".format(",".join(final_seq))])
            if res.success: current_ir = res.output_path
            else: break
            
        runtime_hrl = env.metrics.measure_runtime(current_ir, iterations=20)
        
        print(f"  -O0 Runtime: {runtime_o0:.6f}s")
        print(f"  -O3 Runtime: {runtime_o3:.6f}s ({(runtime_o0-runtime_o3)/max(runtime_o0,1e-6)*100:.1f}% speedup)")
        print(f"  HRL Runtime: {runtime_hrl:.6f}s ({(runtime_o0-runtime_hrl)/max(runtime_o0,1e-6)*100:.1f}% speedup)")
        
        if runtime_hrl < runtime_o3 and runtime_hrl > 0:
            print("  >>> SUCCESS: HRL BEAT -O3!")
        else:
            gap = (runtime_hrl - runtime_o3) / max(runtime_o3, 1e-6) * 100
            print(f"  >>> FAILED: HRL is {gap:.1f}% slower than -O3.")

if __name__ == "__main__":
    compare_to_o3("models/hrl_industrial_hour_0619.pth")
