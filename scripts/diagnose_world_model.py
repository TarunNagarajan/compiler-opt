"""
World Model Averaging Diagnostic
Run this against a checkpoint to verify the model produces
DIFFERENT predictions for DIFFERENT programs.

Usage:
  uv run python scripts/diagnose_world_model.py --checkpoint models/world_model_antigravity_v4_L6_checkpoint.pth --gnn_layers 6
"""

import sys
import torch
import numpy as np
import argparse
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.env import CompilerOptEnv
from src.config import get_benchmark_paths, FEATURE_DIM, NUM_ACTIONS
from src.models.world_model import create_world_model


def diagnose(args):
    # Load model
    model = create_world_model(state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS, gnn_layers=args.gnn_layers)
    ckpt = torch.load(args.checkpoint, weights_only=False)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    iteration = ckpt.get('iteration', '?')
    print(f"Loaded checkpoint: iteration {iteration}, best_loss={ckpt.get('best_loss', '?'):.4f}")
    print(f"GNN layers: {args.gnn_layers}\n")

    # Collect diverse graphs
    benchmarks = get_benchmark_paths()
    env = CompilerOptEnv(benchmarks, max_steps=5)
    random.seed(42)

    graphs = []
    for _ in range(50):
        obs, info = env.reset()
        g = env.get_observation_graph()
        if g is not None and g.x.shape[0] > 5:
            graphs.append(g)
        if len(graphs) == 5:
            break

    if len(graphs) < 2:
        print("ERROR: Could not collect enough graphs!")
        return

    # TEST 1: Encoder embeddings
    print("=" * 60)
    print("TEST 1: Are encoder embeddings DIFFERENT per program?")
    print("=" * 60)
    embs = []
    for i, g in enumerate(graphs):
        batch = torch.zeros(g.x.size(0), dtype=torch.long)
        ea = getattr(g, 'edge_attr', torch.zeros(g.edge_index.size(1), dtype=torch.long))
        with torch.no_grad():
            emb = model.encoder(g.x, g.edge_index, batch, edge_type=ea)
        embs.append(emb)
        print(f"  Graph {i} ({g.x.shape[0]:3d} nodes, {g.edge_index.shape[1]:4d} edges): "
              f"mean={emb.mean():.4f}, std={emb.std():.4f}, norm={emb.norm():.2f}")

    print("\n  Pairwise L2 distances:")
    all_same = True
    for i in range(len(embs)):
        for j in range(i + 1, len(embs)):
            d = (embs[i] - embs[j]).norm().item()
            if d > 0.01:
                all_same = False
            print(f"    [{i}] vs [{j}]: {d:.4f}")

    if all_same:
        print("\n  ❌ VERDICT: COLLAPSED — all embeddings identical")
    else:
        print("\n  ✅ VERDICT: DISTINCT — model sees different programs")

    # TEST 2: Predictions for same action on different programs
    print("\n" + "=" * 60)
    print("TEST 2: Same action → different predictions?")
    print("=" * 60)
    test_actions = [0, 2, 16, 18, 21, 25, 26, 28]  # Diverse mix
    from src.config import LLVM_PASSES
    action_names = [LLVM_PASSES[a].replace('function(', '').rstrip(')') if a < len(LLVM_PASSES) else f'macro_{a}' for a in test_actions]

    for act, name in zip(test_actions, action_names):
        if act >= NUM_ACTIONS:
            continue
        preds_instr = []
        preds_size = []
        print(f"\n  Action {act} ({name}):")
        for i, g in enumerate(graphs):
            batch = torch.zeros(g.x.size(0), dtype=torch.long)
            ea = getattr(g, 'edge_attr', torch.zeros(g.edge_index.size(1), dtype=torch.long))
            with torch.no_grad():
                _, metrics, _ = model(g.x, g.edge_index, batch, torch.tensor([act]), edge_attr=ea)
            instr = metrics[0, 0].item()
            size = metrics[0, 1].item()
            preds_instr.append(instr)
            preds_size.append(size)
            print(f"    Graph {i}: instr={instr * 100:+.3f}%, size={size * 100:+.3f}%")

        std_i = np.std(preds_instr) * 100
        std_s = np.std(preds_size) * 100
        status = "AVERAGING" if std_i < 0.01 and std_s < 0.01 else "PROGRAM-AWARE"
        print(f"    StdDev: instr={std_i:.4f}%, size={std_s:.4f}% → {status}")

    # TEST 3: Different actions on same program
    print("\n" + "=" * 60)
    print("TEST 3: Different actions on same program → different predictions?")
    print("=" * 60)
    g = graphs[0]
    batch = torch.zeros(g.x.size(0), dtype=torch.long)
    ea = getattr(g, 'edge_attr', torch.zeros(g.edge_index.size(1), dtype=torch.long))
    for act, name in zip(test_actions, action_names):
        if act >= NUM_ACTIONS:
            continue
        with torch.no_grad():
            _, metrics, _ = model(g.x, g.edge_index, batch, torch.tensor([act]), edge_attr=ea)
        print(f"  Action {act:2d} ({name:15s}): instr={metrics[0,0].item()*100:+.3f}%, "
              f"size={metrics[0,1].item()*100:+.3f}%")

    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="World Model Averaging Diagnostic")
    parser.add_argument("--checkpoint", type=str, 
                        default="models/world_model_antigravity_v4_L6_checkpoint.pth")
    parser.add_argument("--gnn_layers", type=int, default=6)
    args = parser.parse_args()
    diagnose(args)
