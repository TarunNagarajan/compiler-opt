"""
V6 HBC Architecture Verification Script

This script proves the efficiency of Hierarchical Block Condensation (HBC) by:
1. Extracting a massive graph from lz4_analyze.ll (~3.5MB).
2. Comparing the Instruction count vs. Block count.
3. Benchmarking the forward pass latency of V5 (Flat) vs. V6 (HBC).
4. Verifying mathematical consistency (output dimensions).
"""

import torch
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.features.ir_graph_extractor_v5 import extract_ir_graph_v5
from src.models.graph_encoder_v6 import GNNEncoderV6

def verify():
    print("🚀 Initializing V6 HBC Architecture Verification...")
    
    # 1. Load a massive file
    target_file = "lz4_analyze.ll"
    if not Path(target_file).exists():
        print(f"❌ Error: {target_file} not found. Please ensure it exists in the root.")
        return

    print(f"📦 Loading {target_file}...")
    start_parse = time.time()
    # Extract multiple hotspots for a truly massive graph
    data = extract_ir_graph_v5(target_file)
    parse_time = time.time() - start_parse
    
    num_instr = data.x.size(0)
    num_blocks = data.block_map.max().item() + 1
    
    print(f"📊 Graph Stats:")
    print(f"   - Instruction Nodes: {num_instr:,}")
    print(f"   - Basic Block Nodes: {num_blocks:,}")
    print(f"   - Compression Factor: {num_instr / num_blocks:.2f}x")
    print(f"   - Parse Time: {parse_time:.2f}s")

    # 2. Setup Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"💻 Using Device: {device}")
    
    input_dim = data.x.size(1)
    hidden_dim = 128
    output_dim = 128
    model = GNNEncoderV6(input_dim, hidden_dim, output_dim, num_layers=6).to(device)
    model.eval()
    
    data = data.to(device)
    
    # 3. Benchmark V5 Mode (Flat Instruction RGCN)
    print("\n⏱️ Benchmarking V5 Mode (Flat Instruction RGCN)...")
    with torch.no_grad():
        # Warmup
        _ = model(data.x, data.edge_index, data.edge_attr, block_map=None)
        
        start_v5 = time.time()
        for _ in range(5):
            out_v5 = model(data.x, data.edge_index, data.edge_attr, block_map=None)
        avg_v5 = (time.time() - start_v5) / 5
    print(f"   - Avg Latency: {avg_v5*1000:.2f}ms")

    # 4. Benchmark V6 Mode (HBC Block-Level RGCN)
    print("⏱️ Benchmarking V6 Mode (Hierarchical Block Condensation)...")
    with torch.no_grad():
        # Warmup
        _ = model(data.x, data.edge_index, data.edge_attr, block_map=data.block_map)
        
        start_v6 = time.time()
        for _ in range(5):
            out_v6 = model(data.x, data.edge_index, data.edge_attr, block_map=data.block_map)
        avg_v6 = (time.time() - start_v6) / 5
    print(f"   - Avg Latency: {avg_v6*1000:.2f}ms")

    # 5. Summary
    speedup = avg_v5 / avg_v6
    print("\n🏁 VERIFICATION RESULT:")
    print(f"   - RGCN Node Reduction: {num_instr} -> {num_blocks} ({(1 - num_blocks/num_instr)*100:.1f}% less work)")
    print(f"   - Latency Speedup: {speedup:.2f}x")
    print(f"   - Output Consistency: {'PASSED' if out_v5.shape == out_v6.shape else 'FAILED'}")
    
    if speedup > 2.0:
        print("\n✅ PROOF COMPLETE: V6 HBC is significantly more efficient for large-scale IR.")
    else:
        print("\n⚠️ PROOF PARTIAL: Speedup observed but less than expected for this graph size.")

if __name__ == "__main__":
    verify()
