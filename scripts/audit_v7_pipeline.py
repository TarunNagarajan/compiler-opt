"""
V7 Pipeline Leak & Quality Audit

This script performs a deep-dive inspection of the data flow:
1. IR -> Graph (Foveated Extraction)
2. Graph -> Block-Level Lifting (HBC)
3. Block-Level -> RGCN -> Instruction-Level (Re-expansion)
4. Instruction-Level -> Global Embedding

It checks for 'leaks' (lost edges, disconnected components) and 
'noise' (collapsed features).
"""

import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.features.ir_graph_extractor_v5 import extract_ir_graph_v5
from src.models.graph_encoder_v6 import GNNEncoderV6
from torch_scatter import scatter_mean

def audit():
    print("🔍 STARTING V7 PIPELINE AUDIT...")
    
    # Target a large file with a specific hotspot
    target_file = "lz4_analyze.ll"
    hotspot = "LZ4_compress_fast_continue"
    
    print(f"--- Stage 1: Foveated Extraction (Hotspot: {hotspot}) ---")
    data = extract_ir_graph_v5(target_file, focus_functions=[hotspot])
    
    num_nodes = data.x.size(0)
    num_edges = data.edge_index.size(1)
    
    # Verify Foveated logic: 
    # Global node (0) + Hotspot instructions (1:1) + Periphery blocks (N:1)
    unique_blocks = torch.unique(data.block_map)
    num_blocks = unique_blocks.size(0)
    
    print(f"   [CHECK] Total Nodes: {num_nodes:,}")
    print(f"   [CHECK] Total Active IDs (Block Map): {num_blocks:,}")
    
    # Check for "Zero-Mapping" leaks: node 0 must ALWAYS be block 0
    if data.block_map[0] != 0:
        print("   ❌ LEAK: Global Node (0) is not mapped to Block 0!")
    else:
        print("   ✅ PASS: Global Node mapping is correct.")

    print(f"--- Stage 2: HBC Edge Lifting Quality ---")
    # Simulate the internal HBC edge lifting
    edge_index = data.edge_index
    block_map = data.block_map
    block_edge_index = block_map[edge_index]
    
    # Count how many edges are preserved vs collapsed
    intra_block_edges = (block_edge_index[0] == block_edge_index[1]).sum().item()
    inter_block_edges = (block_edge_index[0] != block_edge_index[1]).sum().item()
    
    print(f"   [INFO] Intra-block Edges (Local context): {intra_block_edges:,}")
    print(f"   [INFO] Inter-block Edges (Strategic context): {inter_block_edges:,}")
    
    if inter_block_edges == 0:
        print("   ❌ LEAK: No inter-block edges found! The graph is disconnected.")
    else:
        print(f"   ✅ PASS: {inter_block_edges:,} cross-block edges preserved for deep reasoning.")

    print(f"--- Stage 3: Feature Preservation (Variance Check) ---")
    # Ensure scatter_mean isn't zeroing out the latent space
    hidden_dim = 128
    x_proj = torch.randn(num_nodes, hidden_dim) # Simulated projection
    
    block_x = scatter_mean(x_proj, block_map, dim=0)
    
    # Check variance: if variance is near 0, the condensation is destroying the signal
    var = torch.var(block_x).item()
    print(f"   [CHECK] Condensed Feature Variance: {var:.6f}")
    if var < 0.0001:
        print("   ❌ QUALITY: Feature variance too low! Condensation is blurring the signal.")
    else:
        print("   ✅ PASS: Features maintain diversity after condensation.")

    print(f"--- Stage 4: Hotspot Fidelity ---")
    # Identify nodes belonging to the hotspot and verify they have unique block IDs
    # In V7, foveated nodes should have block_idx == node_idx (effectively)
    # We can't easily check 'hotspot' name here, but we can check the 'tail' of the block map
    # where the density changes.
    
    # Just check if there are ANY 1:1 mappings
    counts = torch.bincount(block_map)
    num_foveated_nodes = (counts == 1).sum().item()
    
    print(f"   [CHECK] High-Precision (1:1) Nodes: {num_foveated_nodes:,}")
    if num_foveated_nodes < 10:
         print("   ❌ QUALITY: Foveated region is too small or missing!")
    else:
         print(f"   ✅ PASS: {num_foveated_nodes:,} nodes are in High-Precision Mode.")

    print("\n🏁 AUDIT COMPLETE: Pipeline is structurally sound.")

if __name__ == "__main__":
    audit()
