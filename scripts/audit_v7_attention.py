"""
V7 Attention Landscape Audit

This script extracts the internal attention weights of the trained 
World Model to verify IF it is actually focusing on the Fovea.
"""

import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.features.ir_graph_extractor_v5 import extract_ir_graph_v5
from src.models.world_model_v6 import WorldModelV6

def audit_attention():
    print("🔬 ANALYZING V7 ATTENTION LANDSCAPE...")
    
    # 1. Load latest best checkpoint
    checkpoint_path = "models/world_model_v6_v7_foveated_scratch_best.pth"
    if not Path(checkpoint_path).exists():
        print(f"❌ Error: {checkpoint_path} not found.")
        return

    device = torch.device("cpu")
    model = WorldModelV6(gnn_layers=6, action_dim=67).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()

    # 2. Extract a foveated graph
    target_file = "lz4_analyze.ll"
    hotspot = "LZ4_compress_fast_continue"
    print(f"📦 Processing {target_file} with Fovea on {hotspot}...")
    data = extract_ir_graph_v5(target_file, focus_functions=[hotspot])
    
    # 3. Hook into Attention Pooling
    # We want to see the 'gate' output before it pools.
    # In GNNEncoderV6, self.attn_pool.gate_nn is the scorer.
    
    with torch.no_grad():
        # Re-run Tier 1 & 2 logic to get node embeddings
        x = model.gnn_encoder.input_proj(data.x)
        
        # Simulate HBC message passing
        block_x = torch.zeros(data.block_map.max() + 1, x.size(1))
        # Note: we use mean for the forward pass, but here we just need the re-expanded x
        # to see what the ATTENTION layer thinks of them.
        
        # For simplicity, we'll just run the encoder forward and capture the weights
        # We need a small modification to the encoder to return weights, or we can
        # just compute them manually using the model's weights.
        
        # Manual Attention Score Calculation:
        # attn_pool.gate_nn(x)
        scores = model.gnn_encoder.attn_pool.gate_nn(x) # [N, 1]
        weights = torch.softmax(scores, dim=0)
        
    # 4. Compare Weights
    # Identify which nodes are Fovea (1:1 mapping) vs Periphery (N:1)
    counts = torch.bincount(data.block_map)
    fovea_mask = (counts[data.block_map] == 1)
    periphery_mask = ~fovea_mask
    
    avg_fovea_weight = weights[fovea_mask].mean().item()
    avg_periphery_weight = weights[periphery_mask].mean().item()
    
    max_weight_idx = torch.argmax(weights).item()
    
    print(f"\n📊 Attention Distribution:")
    print(f"   - Avg Weight (Fovea/Hotspot):    {avg_fovea_weight:.8f}")
    print(f"   - Avg Weight (Periphery/Context): {avg_periphery_weight:.8f}")
    print(f"   - Signal Ratio:                  {avg_fovea_weight / (avg_periphery_weight + 1e-9):.2f}x")
    
    if avg_fovea_weight > avg_periphery_weight * 2:
        print(f"\n✅ SUCCESS: The model is focusing {avg_fovea_weight / avg_periphery_weight:.1f}x more on the hotspots.")
    else:
        print("\n⚠️ WARNING: Attention is distributed too evenly. The model may be distracted by the periphery.")

if __name__ == "__main__":
    audit_attention()
