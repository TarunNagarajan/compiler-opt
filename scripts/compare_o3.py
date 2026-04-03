import sys
import subprocess
import argparse
import shutil
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.passes.metrics import MetricsCollector
from src.features.ir_graph_extractor import IRGraphExtractor
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS, CLANG
from src.actions.micro_actions import MicroRefiner

NUM_MACROS = len(MACRO_ACTIONS)

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}\n{res.stderr}")
        sys.exit(1)
    return res.stdout

def compare_o3(args):
    c_file = Path(args.file).resolve()
    if not c_file.exists():
        print(f"[ERROR] File not found: {c_file}")
        return

    print(f"\n========================================================")
    print(f"🚀 ANTIGRAVITY AI  VS  LLVM -O3 BENCHMARK")
    print(f"========================================================")
    print(f"Target Program: {c_file.name}")
    print(f"Agent Checkpoint: {Path(args.checkpoint).name}")
    
    workspace_dir = Path("results/benchmark_run")
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Baseline O0 IR
    metrics_collector = MetricsCollector()
    base_ll = workspace_dir / f"{c_file.stem}_O0.ll"
    print(f"\n[1/3] Generating Baseline IR (-O0)... ", end="", flush=True)
    run_cmd(f"{CLANG} -O0 -Xclang -disable-O0-optnone -S -emit-llvm {c_file} -o {base_ll}")
    base_instrs = metrics_collector.count_instructions(str(base_ll))
    print(f"[READY] ({base_instrs} instructions)")

    # 2. Generate O3 Reference IR
    o3_ll = workspace_dir / f"{c_file.stem}_O3.ll"
    print(f"[2/3] Generating Standard LLVM Pipeline (-O3)... ", end="", flush=True)
    run_cmd(f"{CLANG} -O3 -S -emit-llvm {c_file} -o {o3_ll}")
    o3_instrs = metrics_collector.count_instructions(str(o3_ll))
    print(f"[READY] ({o3_instrs} instructions)")

    # 3. Run Antigravity AI
    print(f"[3/3] Running Antigravity AI Compiler...")
    
    # Init Env
    env = CompilerOptEnv([base_ll], max_steps=args.max_steps, reward_mode=RewardMode.SPEED)
    obs, info = env.reset()
    graph = env.get_observation_graph()

    # Load Agent
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.eval()

    device = next(agent.parameters()).device
    optimization_sequence = []

    for step in range(args.max_steps):
        x = graph.x.to(device)
        edge_index = graph.edge_index.to(device)
        edge_attr = getattr(graph, 'edge_attr', None)
        if edge_attr is not None: edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            macro_probs, _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr)
            m_idx = torch.argmax(macro_probs, dim=-1)
            
            # Stop Macro
            if m_idx.item() == NUM_MACROS - 1:
                break
                
            u_logits = agent.get_micro_action(x, edge_index, batch_vec, m_idx, edge_attr=edge_attr, graph_data=graph)
            u_idx = torch.argmax(u_logits, dim=-1)

        base_seq = MACRO_ACTIONS[m_idx.item()]
        final_seq = MicroRefiner.apply_refinement(base_seq, u_idx.item())
        pipeline = [f"module({','.join(final_seq)})"]
        optimization_sequence.extend(final_seq)
        
        # Apply passes
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            break
            
        env.current_ir_path = res.output_path
        
        # Manually extract next graph
        new_g = IRGraphExtractor().parse_file(env.current_ir_path)
        if new_g is None or new_g.number_of_nodes() == 0:
            break
            
        import torch_geometric.utils as utils
        from torch_geometric.data import Data
        
        node_features = [node[1].get('type_feats', [0.0]*4) for node in new_g.nodes(data=True)]
        x_tensor = torch.zeros((len(node_features), FEATURE_DIM), dtype=torch.float)
        x_tensor[:, :4] = torch.tensor(node_features, dtype=torch.float)
        edge_index = utils.from_networkx(new_g).edge_index
        graph = Data(x=x_tensor, edge_index=edge_index)

    ai_instrs = metrics_collector.count_instructions(str(env.current_ir_path))
    
    print("\n========================================================")
    print("🏆 FINAL BENCHMARK RESULTS")
    print("========================================================")
    print(f"  Unoptimized (O0):   {base_instrs} instructions")
    print(f"  LLVM Standard (O3): {o3_instrs} instructions")
    print(f"  Antigravity AI:     {ai_instrs} instructions")
    print("\n--------------------------------------------------------")
    
    o3_improvement = base_instrs - o3_instrs
    ai_improvement = base_instrs - ai_instrs
    
    if ai_instrs < o3_instrs:
        print(f"🎯 RESULT: ANTIGRAVITY WINS! (-{(o3_instrs - ai_instrs)} instructions vs O3)")
    elif ai_instrs == o3_instrs:
        print(f"🤝 RESULT: EXACT TIE WITH -O3.")
    else:
        diff = ai_instrs - o3_instrs
        print(f"❌ RESULT: LLVM WINS (-O3 is {diff} instructions smaller)")
        
    print(f"--------------------------------------------------------")
    print(f"AI Pipeline Generated ({len(optimization_sequence)} passes):")
    print(f" -> {','.join(optimization_sequence)}")
    print(f"========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the .c file to benchmark")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to HRL trained model .pth")
    parser.add_argument("--world_model", type=str, required=True, help="Path to the associated world model .pth")
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--max_steps", type=int, default=20, help="Max optimizations the AI can apply")
    args = parser.parse_args()
    compare_o3(args)
