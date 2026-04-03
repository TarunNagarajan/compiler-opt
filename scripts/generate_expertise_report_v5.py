"""
v5 World Model — Expertise Demo Report (6-Panel Visualization)

Generates a publication-quality 6-panel figure demonstrating the v5 world model's
capabilities: latent space structure, imagination accuracy, metric prediction,
attention analysis, action sensitivity, and summary stats.

Usage:
  uv run python scripts/generate_expertise_report_v5.py --checkpoint models/world_model_v5_checkpoint.pth
"""

import sys
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
from sklearn.decomposition import PCA

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v5 import WorldModelV5
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS, LLVM_PASSES, MODELS_DIR
from torch_geometric.data import Data
import argparse
import random

METRIC_NAMES = ["Instr", "Size", "Cmplx", "Loops", "Calls", "Blocks"]
METRIC_NAMES_FULL = ["Instructions", "Size", "Complexity", "Loops", "Calls", "Blocks"]


def load_model(checkpoint_path, gnn_layers=6):
    model = WorldModelV5(state_dim=FEATURE_DIM, action_dim=NUM_ACTIONS, gnn_layers=gnn_layers)
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
    if 'model_state_dict' in ckpt:
        model.load_state_dict(ckpt['model_state_dict'])
        info = f"iter={ckpt.get('iteration', '?')}, loss={ckpt.get('best_loss', 0):.4f}"
    else:
        model.load_state_dict(ckpt)
        info = "raw"
    model.eval()
    return model, info


def encode_graph(model, graph):
    """Encode a single graph using v5 API."""
    edge_attr = getattr(graph, 'edge_attr', None)
    if edge_attr is None:
        edge_attr = torch.zeros(graph.edge_index.size(1), dtype=torch.long)
    batch_vec = torch.zeros(graph.x.size(0), dtype=torch.long)
    graph_data = Data(x=graph.x, edge_index=graph.edge_index, edge_attr=edge_attr, batch=batch_vec)
    return model.encode_graph(graph_data)


def predict_metrics(model, graph, action):
    """Predict metrics for a single graph + action."""
    state_emb = encode_graph(model, graph)
    action_onehot = torch.zeros(1, NUM_ACTIONS)
    action_onehot[0, action] = 1.0
    _, pred_metrics = model(state_emb, action_onehot)
    return pred_metrics


def generate_report(args):
    print(f"[REPORT] Generating v5 Expertise Report...")
    
    model, model_info = load_model(args.checkpoint, gnn_layers=args.gnn_layers)
    print(f"[REPORT] Model: {model_info}")
    
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks, max_steps=10)
    random.seed(42)
    
    # ===============================================================
    # Collect diverse program graphs
    # ===============================================================
    print("[REPORT] Collecting program graphs...")
    graphs = []
    graph_infos = []
    for _ in range(100):
        try:
            obs, info = env.reset()
            g = env.get_observation_graph()
            if g is not None and g.x.shape[0] > 5:
                graphs.append(g)
                graph_infos.append(info)
        except:
            continue
        if len(graphs) >= 30:
            break
    
    print(f"[REPORT] Collected {len(graphs)} programs")
    
    # ===============================================================
    # FIGURE SETUP
    # ===============================================================
    fig = plt.figure(figsize=(20, 13))
    fig.patch.set_facecolor('#1a1a2e')
    fig.suptitle("World Model v5 — Expertise Report", 
                 fontsize=20, fontweight='bold', color='white', y=0.97)
    subtitle = f"Checkpoint: {Path(args.checkpoint).name} ({model_info})"
    fig.text(0.5, 0.94, subtitle, ha='center', fontsize=10, color='#8888aa')
    
    # ===============================================================
    # PANEL 1: Program DNA Map (PCA of Latent Space)
    # ===============================================================
    print("[REPORT] Panel 1: Program DNA Map...")
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.set_facecolor('#16213e')
    
    embeddings = []
    complexities = []
    node_counts = []
    
    with torch.no_grad():
        for g, info in zip(graphs, graph_infos):
            emb = encode_graph(model, g)
            embeddings.append(emb.squeeze().numpy())
            complexities.append(info.get('initial_complexity', 0))
            node_counts.append(g.x.shape[0])
    
    if len(embeddings) > 2:
        emb_array = np.array(embeddings)
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(emb_array)
        
        sc = ax1.scatter(pcs[:, 0], pcs[:, 1], 
                        c=complexities, cmap='magma', 
                        s=[max(20, n) for n in node_counts],
                        edgecolors='white', linewidth=0.3, alpha=0.85)
        cbar = plt.colorbar(sc, ax=ax1, shrink=0.8)
        cbar.set_label('Cyclomatic Complexity', fontsize=8, color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        var_explained = pca.explained_variance_ratio_
        ax1.text(0.02, 0.98, f"Var: {var_explained[0]:.1%} + {var_explained[1]:.1%}",
                transform=ax1.transAxes, fontsize=7, color='#aaaacc', va='top')
    
    ax1.set_title("1. Program DNA Map", fontsize=11, color='white', pad=10)
    ax1.set_xlabel("Principal Component 1", fontsize=8, color='#aaaacc')
    ax1.set_ylabel("Principal Component 2", fontsize=8, color='#aaaacc')
    ax1.tick_params(colors='#aaaacc', labelsize=7)
    ax1.grid(True, alpha=0.1, color='white')
    
    # ===============================================================
    # PANEL 2: 5-Step Imagination Path
    # ===============================================================
    print("[REPORT] Panel 2: 5-Step Imagination...")
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_facecolor('#16213e')
    
    obs, info = env.reset()
    graph = env.get_observation_graph()
    
    # Representative pass sequence
    action_seq = [16, 18, 28, 0, 21]  # mem2reg, instcombine, simplifycfg, loop-unroll, gvn
    action_labels = ['mem2reg', 'instcomb', 'simpcfg', 'unroll', 'gvn']
    
    actual_cum = [0.0]
    pred_cum = [0.0]
    current_instr = info.get('initial_instructions', 1)
    
    with torch.no_grad():
        for i, action in enumerate(action_seq):
            if graph is None:
                break
            
            pred_m = predict_metrics(model, graph, action)
            pred_delta = pred_m[0, 0].item()
            
            obs, reward, term, trunc, step_info = env.step(action)
            actual_instr = step_info.get('instructions_after', current_instr)
            actual_delta = (actual_instr - current_instr) / max(current_instr, 1)
            
            actual_cum.append(actual_cum[-1] + actual_delta)
            pred_cum.append(pred_cum[-1] + pred_delta)
            
            current_instr = actual_instr
            graph = env.get_observation_graph()
    
    steps = range(len(pred_cum))
    ax2.fill_between(steps, pred_cum, actual_cum, alpha=0.15, color='#e94560')
    ax2.plot(steps, pred_cum, 'o--', color='#e94560', label='Predicted', linewidth=2, markersize=6)
    ax2.plot(steps, actual_cum, 's-', color='#0f3460', label='Actual', linewidth=2, markersize=6,
             markerfacecolor='#53bf9d', markeredgecolor='white')
    
    x_labels = ["Init"] + action_labels[:len(pred_cum)-1]
    ax2.set_xticks(range(len(x_labels)))
    ax2.set_xticklabels(x_labels, rotation=30, ha='right', fontsize=7, color='#aaaacc')
    ax2.set_ylabel("Cumul. Instr Δ (%)", fontsize=8, color='#aaaacc')
    ax2.set_title("2. 5-Step Imagination Path", fontsize=11, color='white', pad=10)
    ax2.legend(fontsize=8, loc='best', facecolor='#16213e', edgecolor='#333366', labelcolor='white')
    ax2.tick_params(colors='#aaaacc', labelsize=7)
    ax2.grid(True, alpha=0.1, color='white')
    
    # ===============================================================
    # PANEL 3: Per-Metric Radar Chart
    # ===============================================================
    print("[REPORT] Panel 3: Radar Chart...")
    ax3 = fig.add_subplot(2, 3, 3, polar=True)
    ax3.set_facecolor('#16213e')
    
    # Collect one real sample for radar
    obs, info = env.reset()
    graph = env.get_observation_graph()
    if graph is not None:
        test_action = 18  # instcombine
        
        with torch.no_grad():
            pred_m = predict_metrics(model, graph, test_action)
        
        obs, _, _, _, step_info = env.step(test_action)
        
        instr_b = info.get('initial_instructions', 1)
        size_b = info.get('initial_size', 1)
        cmplx_b = info.get('initial_complexity', 0)
        loops_b = info.get('initial_loops', 0)
        calls_b = info.get('initial_calls', 0)
        blocks_b = info.get('initial_blocks', 0)
        
        actual_vals = [
            (step_info['instructions_after'] - instr_b) / max(instr_b, 1),
            (step_info['size_after'] - size_b) / max(size_b, 1),
            (step_info.get('complexity_after', cmplx_b) - cmplx_b) / 100.0,
            (step_info.get('loops_after', loops_b) - loops_b) / 10.0,
            (step_info.get('calls_after', calls_b) - calls_b) / 10.0,
            (step_info.get('blocks_after', blocks_b) - blocks_b) / 20.0,
        ]
        pred_vals = pred_m[0].numpy().tolist()
        
        # Radar chart
        angles = np.linspace(0, 2 * np.pi, len(METRIC_NAMES), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        actual_r = [abs(v) for v in actual_vals] + [abs(actual_vals[0])]
        pred_r = [abs(v) for v in pred_vals] + [abs(pred_vals[0])]
        
        ax3.plot(angles, pred_r, 'o-', color='#e94560', linewidth=2, label='Predicted')
        ax3.fill(angles, pred_r, alpha=0.15, color='#e94560')
        ax3.plot(angles, actual_r, 's-', color='#53bf9d', linewidth=2, label='Actual')
        ax3.fill(angles, actual_r, alpha=0.15, color='#53bf9d')
        
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(METRIC_NAMES, fontsize=8, color='white')
        ax3.tick_params(colors='#aaaacc', labelsize=6)
    
    ax3.set_title("3. Metric Radar (instcombine)", fontsize=11, color='white', pad=20)
    ax3.legend(fontsize=7, loc='upper right', bbox_to_anchor=(1.3, 1.1),
              facecolor='#16213e', edgecolor='#333366', labelcolor='white')
    
    # ===============================================================
    # PANEL 4: Attention Spread (v5-specific)
    # ===============================================================
    print("[REPORT] Panel 4: Attention Analysis...")
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.set_facecolor('#16213e')
    
    # Collect attention entropy across programs
    attn_entropies = []
    attn_maxes = []
    program_sizes = []
    
    with torch.no_grad():
        for g in graphs[:20]:
            edge_attr = getattr(g, 'edge_attr', None)
            if edge_attr is None:
                edge_attr = torch.zeros(g.edge_index.size(1), dtype=torch.long)
            batch_vec = torch.zeros(g.x.size(0), dtype=torch.long)
            
            # Run through encoder layers to get pre-pooling node features
            encoder = model.gnn_encoder
            x = encoder.input_proj(g.x)
            for conv, norm in zip(encoder.convs, encoder.norms):
                x_new = conv(x, g.edge_index, edge_attr)
                x_new = norm(x_new)
                x_new = torch.relu(x_new)
                if x_new.shape == x.shape:
                    x_new = x_new + x
                x = x_new
            
            # Get attention gate scores
            gate_nn = encoder.attn_pool.gate_nn
            gate_scores = gate_nn(x).squeeze(-1)   # [N]
            attn_weights = torch.softmax(gate_scores, dim=0)  # [N]
            
            # Entropy of attention distribution
            entropy = -(attn_weights * torch.log(attn_weights + 1e-8)).sum().item()
            max_entropy = np.log(len(attn_weights))  # Uniform distribution entropy
            normalized_entropy = entropy / max(max_entropy, 1e-6)
            
            attn_entropies.append(normalized_entropy)
            attn_maxes.append(attn_weights.max().item())
            program_sizes.append(g.x.shape[0])
    
    if attn_entropies:
        sc4 = ax4.scatter(program_sizes, attn_entropies, 
                         c=attn_maxes, cmap='YlOrRd_r', 
                         s=50, edgecolors='white', linewidth=0.3, alpha=0.85)
        cbar4 = plt.colorbar(sc4, ax=ax4, shrink=0.8)
        cbar4.set_label('Max Attn Weight', fontsize=8, color='white')
        cbar4.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar4.ax.axes, 'yticklabels'), color='white')
        
        ax4.axhline(y=0.8, color='#53bf9d', linestyle='--', alpha=0.5, label='Uniform threshold')
        ax4.axhline(y=0.3, color='#e94560', linestyle='--', alpha=0.5, label='Focused threshold')
    
    ax4.set_xlabel("Program Size (nodes)", fontsize=8, color='#aaaacc')
    ax4.set_ylabel("Attention Entropy (normalized)", fontsize=8, color='#aaaacc')
    ax4.set_title("4. Attention Focus (v5-specific)", fontsize=11, color='white', pad=10)
    ax4.tick_params(colors='#aaaacc', labelsize=7)
    ax4.grid(True, alpha=0.1, color='white')
    ax4.legend(fontsize=7, facecolor='#16213e', edgecolor='#333366', labelcolor='white')
    
    # ===============================================================
    # PANEL 5: Action Sensitivity Heatmap
    # ===============================================================
    print("[REPORT] Panel 5: Action Sensitivity Heatmap...")
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.set_facecolor('#16213e')
    
    # Pick 10 representative actions
    test_actions = [0, 2, 5, 10, 16, 18, 21, 28, 30, 35]
    test_actions = [a for a in test_actions if a < NUM_ACTIONS]
    action_short_names = []
    for a in test_actions:
        name = LLVM_PASSES[a] if a < len(LLVM_PASSES) else f'macro_{a}'
        name = name.replace('function(', '').rstrip(')').split('<')[0]
        if len(name) > 12:
            name = name[:12]
        action_short_names.append(name)
    
    # Average prediction across multiple programs
    sensitivity_matrix = np.zeros((len(test_actions), 6))
    
    with torch.no_grad():
        for g in graphs[:10]:
            state_emb = encode_graph(model, g)
            for i, action in enumerate(test_actions):
                action_onehot = torch.zeros(1, NUM_ACTIONS)
                action_onehot[0, action] = 1.0
                _, pred_m = model(state_emb, action_onehot)
                sensitivity_matrix[i] += pred_m[0].numpy()
    
    sensitivity_matrix /= min(len(graphs), 10)
    
    im = ax5.imshow(sensitivity_matrix.T, cmap='RdBu_r', aspect='auto', 
                    vmin=-np.abs(sensitivity_matrix).max(), 
                    vmax=np.abs(sensitivity_matrix).max())
    
    ax5.set_xticks(range(len(test_actions)))
    ax5.set_xticklabels(action_short_names, rotation=45, ha='right', fontsize=7, color='#aaaacc')
    ax5.set_yticks(range(6))
    ax5.set_yticklabels(METRIC_NAMES, fontsize=8, color='#aaaacc')
    ax5.set_title("5. Action → Metric Sensitivity", fontsize=11, color='white', pad=10)
    
    cbar5 = plt.colorbar(im, ax=ax5, shrink=0.8)
    cbar5.set_label('Predicted Δ', fontsize=8, color='white')
    cbar5.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar5.ax.axes, 'yticklabels'), color='white')
    
    # ===============================================================
    # PANEL 6: Summary Statistics
    # ===============================================================
    print("[REPORT] Panel 6: Summary...")
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.set_facecolor('#16213e')
    ax6.axis('off')
    
    # Compute quick stats from imagination path
    if len(pred_cum) > 1:
        path_error = np.mean([abs(p - a) for p, a in zip(pred_cum, actual_cum)])
    else:
        path_error = float('nan')
    
    avg_entropy = np.mean(attn_entropies) if attn_entropies else float('nan')
    avg_max_attn = np.mean(attn_maxes) if attn_maxes else float('nan')
    
    lines = [
        ("MODEL SUMMARY", "", "#ffffff", True),
        ("", "", "", False),
        ("Architecture", "GNNv5 + AttentionPool + FiLM", "#53bf9d", False),
        ("Params", f"{sum(p.numel() for p in model.parameters()):,}", "#53bf9d", False),
        ("Edge Types", "7 (incl. loop_back)", "#53bf9d", False),
        ("Pooling", "Learned Attention", "#53bf9d", False),
        ("", "", "", False),
        ("DEMO RESULTS", "", "#ffffff", True),
        ("", "", "", False),
        ("Programs Encoded", f"{len(graphs)}", "#aaaacc", False),
        ("Imagination Error", f"{path_error:.4f}" if not np.isnan(path_error) else "N/A", "#e94560" if path_error > 0.1 else "#53bf9d", False),
        ("Avg Attn Entropy", f"{avg_entropy:.3f}", "#aaaacc", False),
        ("Avg Max Attn", f"{avg_max_attn:.3f}", "#aaaacc", False),
        ("", "", "", False),
        ("STATUS", "[OK] Ready for Evaluation" if path_error < 0.2 else "[!!] Needs More Training", "#53bf9d" if path_error < 0.2 else "#e94560", True),
    ]
    
    y_pos = 0.95
    for label, value, color, bold in lines:
        if label == "" and value == "":
            y_pos -= 0.03
            continue
        weight = 'bold' if bold else 'normal'
        if value:
            ax6.text(0.05, y_pos, f"{label}:", fontsize=10, color='#8888aa',
                    transform=ax6.transAxes, fontweight=weight, family='monospace')
            ax6.text(0.55, y_pos, value, fontsize=10, color=color,
                    transform=ax6.transAxes, fontweight=weight, family='monospace')
        else:
            ax6.text(0.05, y_pos, label, fontsize=12, color=color,
                    transform=ax6.transAxes, fontweight=weight, family='monospace')
        y_pos -= 0.065
    
    # ===============================================================
    # SAVE
    # ===============================================================
    plt.tight_layout(rect=[0, 0.02, 1, 0.93])
    
    output_path = f"expertise_report_v5.png"
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"\n[REPORT] Expertise Report saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="v5 World Model Expertise Report")
    parser.add_argument("--checkpoint", type=str, default="models/world_model_v5_checkpoint.pth")
    parser.add_argument("--gnn_layers", type=int, default=6)
    args = parser.parse_args()
    generate_report(args)
