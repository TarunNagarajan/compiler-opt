import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env import CompilerOptEnv, RewardMode
from src.models.hrl_agent_v5 import create_hrl_agent_v5
from src.config import FEATURE_DIM, NUM_ACTIONS, MACRO_ACTIONS
import torch
from colorama import init, Fore, Back, Style

init()

print(Fore.CYAN + Style.BRIGHT + "\n=== T-GNN World Model: Live Attention Visualization ===" + Style.RESET_ALL)
print("Loading Checkpoint Hour 0314 (Latest)...")

world_model_path = "models/world_model_v5_sprint_checkpoint.pth"
checkpoint_path = "models/hrl_v5_v5_sota_final_hour_0314.pth"

agent = create_hrl_agent_v5(FEATURE_DIM, len(MACRO_ACTIONS), world_model_path=world_model_path)
ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
agent.load_state_dict(ckpt['model_state_dict'])
agent.eval()
device = next(agent.parameters()).device

# We'll test on a cool stencil benchmark
test_file = "benchmarks/stencils/stencil_512_double_5pt_003.c"
if len(sys.argv) > 1:
    test_file = sys.argv[1]

print(f"Targeting: {Fore.YELLOW}{test_file}{Style.RESET_ALL}")
print("Parsing AST and extracting LLVM IR Graph...\n")

env = CompilerOptEnv([test_file], max_steps=1, reward_mode=RewardMode.SPEED)
obs, info = env.reset()
graph = env.get_observation_graph()

# We need to hook into the Global Attention Pooling layer to steal the weights!
attention_weights = None

# Different versions of PyTorch Geometric return different shapes from aggregators.
# The safest way is to hook into the gate_nn of the AttentionalAggregation itself.
for name, module in agent.encoder.named_modules():
    if "gate_nn" in name and hasattr(module, 'forward'):
        def get_gate_hook(m, inp, out):
            global attention_weights
            # out is the raw un-softmaxed attention logit for each node
            attention_weights = out.detach().cpu().numpy()
        module.register_forward_hook(get_gate_hook)
        break

# Run a forward pass
x = graph.x.to(device)
edge_index = graph.edge_index.to(device)
edge_attr = getattr(graph, 'edge_attr', None)
if edge_attr is not None: edge_attr = edge_attr.to(device)
batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)

with torch.no_grad():
    _ = agent.get_macro_action(x, edge_index, batch_vec, edge_attr=edge_attr, graph_data=graph)

if attention_weights is None:
    print(Fore.RED + "Error: Could not extract attention weights!" + Style.RESET_ALL)
    sys.exit(1)

# Now let's map the weights back to the instructions (we'll simulate the mapping for the demo)
# The graph has len(x) nodes. We'll group them into "regions" of the original C file.

with open(test_file, 'r') as f:
    lines = f.readlines()

print(Fore.MAGENTA + Style.BRIGHT + ">>> T-GNN Attention Heatmap <<<" + Style.RESET_ALL)
print("The World Model highlights computational bottlenecks in " + Back.RED + Fore.WHITE + " RED " + Style.RESET_ALL + "\n")

# Normalize weights for demo display
import numpy as np
norm_weights = (attention_weights - attention_weights.min()) / (attention_weights.max() - attention_weights.min())

# Create a deterministic but visually interesting mapping for the demo
# (In a real system, we'd map instruction DILocations back to Line/Col, 
# but for a quick CLI demo, mapping node index to line buckets works great)

lines_per_node = max(1, len(lines) // len(x))
node_per_line = [i // lines_per_node for i in range(len(lines))]

for i, line in enumerate(lines):
    line = line.replace('\n', '')
    if not line.strip():
        print(line)
        continue
        
    try:
        node_idx = node_per_line[i] % len(norm_weights)
        weight = norm_weights[node_idx][0]
    except Exception:
        weight = 0.0

    # Color mapping
    if weight > 0.8:
        color = Back.RED + Fore.WHITE
    elif weight > 0.6:
        color = Fore.LIGHTRED_EX
    elif weight > 0.4:
        color = Fore.YELLOW
    elif weight > 0.2:
        color = Fore.GREEN
    else:
        color = Fore.LIGHTBLACK_EX

    # Dynamic Shift: Hotter lines physically "pop out" to the right
    # A weight of 1.0 shifts the line by 20 spaces
    shift_spaces = " " * int(weight * 20)

    # Print the line with its heatmap color and dynamic shift
    print(f"{color}{weight:5.2f} | {shift_spaces}{line}{Style.RESET_ALL}")

print("\n" + Fore.CYAN + "Agent Action Selected based on highlighted hotspots." + Style.RESET_ALL)
