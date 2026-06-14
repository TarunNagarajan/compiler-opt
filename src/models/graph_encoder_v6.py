"""
v6 GNN Encoder — Hierarchical Block Condensation (HBC)

Changes from v5 (graph_encoder_v5.py):
1. NEW: Hierarchical Block Condensation (HBC)
   - Instructions are condensed into Basic Blocks via a local Pre-Encoder.
   - RGCN message passing occurs at the BLOCK level (10x-50x speedup).
2. NEW: Adaptive Re-Expansion
   - Block embeddings are expanded back to instructions for final Attention Pooling.
3. UNCHANGED: 7 relation types, Attention Pooling logic.

This architecture allows processing 10,000+ instructions by treating them as
~200 basic blocks during the expensive relational convolution phase.
"""

import torch
import torch.nn as nn
from torch_geometric.nn import RGCNConv
from torch_geometric.nn.aggr import AttentionalAggregation
try:
    from torch_scatter import scatter_mean, scatter_max
except (ImportError, OSError):
    from torch_geometric.utils import scatter
    def scatter_mean(src, index, dim=0, dim_size=None):
        return scatter(src, index, dim=dim, dim_size=dim_size, reduce='mean')
    def scatter_max(src, index, dim=0, dim_size=None):
        return scatter(src, index, dim=dim, dim_size=dim_size, reduce='max')


class GNNEncoderV6(nn.Module):
    """
    RGCN encoder with Hierarchical Block Condensation.
    
    V5: Instructions -> RGCN -> Pool -> Embedding
    V6: Instructions -> Block-Pool -> RGCN (on Blocks) -> Expand -> Pool -> Embedding
    """
    
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers=6, num_relations=10):
        super().__init__()
        
        # 1. Instruction Level (Local Expert)
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Tier 1 GNN: Instruction-level topological reasoning
        self.tier1_convs = nn.ModuleList([
            RGCNConv(hidden_dim, hidden_dim, num_relations=num_relations),
            RGCNConv(hidden_dim, hidden_dim, num_relations=num_relations)
        ])
        self.tier1_norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(2)])
        
        # 2. Block Level (Global Strategist)
        # Message passing happens on these layers, but with 10x fewer nodes
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(num_layers):
            self.convs.append(RGCNConv(hidden_dim, hidden_dim, num_relations=num_relations))
            self.norms.append(nn.LayerNorm(hidden_dim))
        
        # 3. Final Global Level
        self.attn_pool = AttentionalAggregation(
            gate_nn=nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, 1)
            ),
            nn=nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU()
            )
        )
        
        self.output_proj = nn.Linear(hidden_dim * 2, output_dim)
        
    def forward(self, x, edge_index, edge_attr, batch=None, block_map=None):
        """
        Args:
            x: [N_instr, feat]
            edge_index: [2, E] (Instruction-level edges)
            edge_attr: [E]
            batch: [N_instr]
            block_map: [N_instr] (Instruction ID -> Block ID mapping)
        """
        # --- TIER 1: Instruction Embedding & Local Topology ---
        x = self.input_proj(x)
        
        # Apply Tier 1 Instruction-Level GNN
        for conv, norm in zip(self.tier1_convs, self.tier1_norms):
            residual = x
            x = conv(x, edge_index, edge_attr)
            x = torch.relu(x)
            x = norm(x + residual)
        
        # Fallback for older datasets without block_map
        if block_map is None:
            # Traditional V5 path (Block-less RGCN)
            for conv, norm in zip(self.convs, self.norms):
                residual = x
                x = conv(x, edge_index, edge_attr)
                x = torch.relu(x)
                x = norm(x + residual)
        else:
            # --- TIER 2: HBC (Block-Level Message Passing) ---
            # 1. Condense Instructions into Blocks
            # Node 0 (Global) is Block 0, preserved as-is.
            block_x = scatter_mean(x, block_map, dim=0)
            
            # 2. Lift Edges to Block Level
            # Map [instr_src, instr_dst] to [block_src, block_dst]
            block_edge_index = block_map[edge_index]
            
            # Remove self-loops created by instruction edges within the same block
            mask = block_edge_index[0] != block_edge_index[1]
            
            # SCALE RECAPTURE: Always preserve Global node (3, 4) AND Call edges (5).
            # Also preserve Loop Back-Edges (6) for structural awareness.
            mask = mask | (edge_attr == 3) | (edge_attr == 4) | (edge_attr == 5) | (edge_attr == 6)
            
            # DATA FLOW PRESERVATION: Preserve Type 2 (data flow) edges even within blocks
            # for the Tier 1 embeddings, but for HBC message passing, we usually flatten.
            # However, if it's a cross-block data flow, we MUST keep it.
            # (mask already handles cross-block since block_src != block_dst)
            
            b_edge_index = block_edge_index[:, mask]
            b_edge_attr = edge_attr[mask]
            
            # 3. RGCN on Blocks (The Efficiency Engine)
            # This is 10x-50x faster because len(block_x) << len(x)
            for conv, norm in zip(self.convs, self.norms):
                residual = block_x
                block_x = conv(block_x, b_edge_index, b_edge_attr)
                block_x = torch.relu(block_x)
                block_x = norm(block_x + residual)
            
            # --- TIER 3: Expansion & Pooling ---
            # Re-expand block embeddings back to instructions to keep Attention Pooling granular
            x = block_x[block_map]
        
        # Global Node Extraction (Node 0)
        if batch is None:
            global_out = x[0].unsqueeze(0)
            attn_out = self.attn_pool(x, batch)
        else:
            _, counts = torch.unique(batch, return_counts=True)
            ptr = torch.cat([torch.tensor([0], device=x.device), counts.cumsum(0)[:-1]])
            global_out = x[ptr]
            attn_out = self.attn_pool(x, batch)
            
        graph_emb = torch.cat([global_out, attn_out], dim=-1)
        return self.output_proj(graph_emb)


def create_v6_encoder(input_dim=46, hidden_dim=128, output_dim=128, num_layers=6, num_relations=10):
    return GNNEncoderV6(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        output_dim=output_dim,
        num_layers=num_layers,
        num_relations=num_relations
    )
