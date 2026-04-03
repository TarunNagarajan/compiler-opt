import sys
import subprocess
import argparse
import shutil
import time
import torch
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.passes.metrics import MetricsCollector
from src.features.ir_graph_extractor import IRGraphExtractor
from src.models.hrl_agent import create_hrl_agent
from src.config import FEATURE_DIM, MACRO_ACTIONS, CLANG
from src.actions.micro_actions import MicroRefiner
from src.models.mcts import MCTS

NUM_MACROS = len(MACRO_ACTIONS)

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}\n{res.stderr}")
        sys.exit(1)
    return res.stdout

def format_policy(policy):
    out = ""
    top_indices = np.argsort(policy)[::-1][:3]
    for idx in top_indices:
        if policy[idx] > 0.01:
            out += f"M[{idx}]: {policy[idx]*100:.1f}% | "
    return out

def compare_o3_mcts(args):
    c_file = Path(args.file).resolve()
    if not c_file.exists():
        print(f"[ERROR] File not found: {c_file}")
        return

    print(f"\n========================================================")
    print(f"  ANTIGRAVITY AI (MCTS)  VS  LLVM -O3 BENCHMARK")
    print(f"========================================================")
    print(f"Target Program: {c_file.name}")
    print(f"Agent Checkpoint: {Path(args.checkpoint).name}")
    print(f"MCTS Simulations per step: {args.simulations}")
    
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

    # 3. Run Antigravity AI with MCTS
    print(f"[3/3] Running Antigravity AI (MCTS) Compiler...")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    agent = create_hrl_agent(FEATURE_DIM, NUM_MACROS, args.world_model, gnn_layers=args.gnn_layers)
    agent.load_state_dict(torch.load(args.checkpoint, map_location='cpu', weights_only=True))
    agent.to(device)
    agent.eval()

    env = CompilerOptEnv([base_ll], max_steps=args.max_steps, reward_mode=RewardMode.SPEED)
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    optimization_sequence = []

    for step in range(args.max_steps):
        print(f"\n  [Step {step+1}] Running Tree Search...", end="", flush=True)
        mcts = MCTS(agent, num_simulations=args.simulations, c_puct=1.5, num_macros=NUM_MACROS)
        
        start_time = time.time()
        mcts_policy, root_node = mcts.search(graph, device=device)
        print(f" done ({(time.time() - start_time)*1000:.1f}ms)")
        
        # Write streaming JSON output for the Rust TUI
        try:
            import json
            tui_dir = Path("tui")
            tui_dir.mkdir(exist_ok=True)
            tui_file = tui_dir / "mcts_state.json"
            
            # The python script is run from the root, write into tui/
            with open(tui_file, "w") as f:
                json.dump(root_node.to_dict(), f)
        except Exception as e:
            print(f"  -> [TUI Error] Failed to export state: {e}")
            
        print(f"  -> Policy: {format_policy(mcts_policy)}")
        
        m_idx_val = np.argmax(mcts_policy)
        
        if m_idx_val == NUM_MACROS - 1:
            print(f"  -> [MCTS Selected STOP]")
            break
            
        m_idx = torch.tensor(m_idx_val, dtype=torch.long, device=device).unsqueeze(0)
        
        # Get micro-action for refinement
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
        
        print(f"  -> Executing: Macro {m_idx_val} + Mod {u_idx_val} | Passes: {final_seq}")
        
        res = env.executor.apply_passes(env.current_ir_path, pipeline)
        if not res.success:
            print("  -> [MCTS SELECTION FAILED COMPILATION] Halting search.")
            break
            
        env.current_ir_path = res.output_path
        
        extractor = IRGraphExtractor()
        new_g = extractor.parse_file(env.current_ir_path)
        if new_g is None or new_g.number_of_nodes() == 0:
            print("  -> [FAILED TO EXTRACT NEXT GRAPH] Halting search.")
            break
            
        graph = extractor.to_pyg_data(new_g)

    ai_instrs = metrics_collector.count_instructions(str(env.current_ir_path))
    
    print("\n========================================================")
    print("  FINAL MCTS BENCHMARK RESULTS")
    print("========================================================")
    print(f"  Unoptimized (O0):   {base_instrs} instructions")
    print(f"  LLVM Standard (O3): {o3_instrs} instructions")
    print(f"  Antigravity MCTS:   {ai_instrs} instructions")
    print("\n--------------------------------------------------------")
    
    o3_improvement = base_instrs - o3_instrs
    ai_improvement = base_instrs - ai_instrs
    
    if ai_instrs < o3_instrs:
        print(f"  RESULT: ANTIGRAVITY MCTS WINS! (-{(o3_instrs - ai_instrs)} instructions vs O3)")
    elif ai_instrs == o3_instrs:
        print(f"  RESULT: EXACT TIE WITH -O3.")
    else:
        diff = ai_instrs - o3_instrs
        print(f"  RESULT: LLVM WINS (-O3 is {diff} instructions smaller)")
        
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
    parser.add_argument("--simulations", type=int, default=200, help="Number of MCTS tree expansions per step")
    args = parser.parse_args()
    compare_o3_mcts(args)
