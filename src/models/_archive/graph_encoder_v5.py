"""
v5 GNN Encoder — Attention Pooling + 7 Relation Types

Changes from v4 (graph_encoder.py):
1. NEW: GlobalAttention pooling replaces additive mean+max pooling
2. NEW: 7 relation types (added loop_back) instead of 6
3. UNCHANGED: RGCN layers, residual connections, LayerNorm

The attention gate learns which nodes matter most for the embedding,
solving the feature dilution problem in large graphs where hot-loop
instructions were weighted equally with boilerplate.
"""

import torch
import torch.nn as nn
from torch_geometric.nn import RGCNConv
from torch_geometric.nn.aggr import AttentionalAggregation


class GNNEncoderV5(nn.Module):
    """
    RGCN encoder with learned attention pooling.
    
    Improvements over v4:
    - Attention-gated global pooling (instead of mean+max)
    - 7th relation type for loop back-edges
    - Optional max pooling kept as additive residual
    """
    
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers=4, num_relations=7):
        super().__init__()
        
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(num_layers):
            self.convs.append(RGCNConv(hidden_dim, hidden_dim, num_relations=num_relations))
            self.norms.append(nn.LayerNorm(hidden_dim))
        
        # NEW: Learned attention pooling
        # The gate_nn learns a scalar importance score per node
        # This replaces the equal-weight mean pooling
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
        
        # Keep max pooling as additive signal (preserves strongest features)
        self.use_max_pool = True
        pool_dim = hidden_dim * 2 if self.use_max_pool else hidden_dim
        
        self.output_proj = nn.Linear(pool_dim, output_dim)
        
    def forward(self, x, edge_index, edge_attr, batch=None):
        x = self.input_proj(x)
        
        for conv, norm in zip(self.convs, self.norms):
            residual = x
            x = conv(x, edge_index, edge_attr)
            x = torch.relu(x)
            x = norm(x + residual)
        
        # NEW: Telescopic Global Node Extraction
        # The Telescopic structure ensures Node 0 is the Global Node.
        # We need to extract Node 0 for each graph in the batch.
        if batch is None:
            # Single graph: Node 0 is the first row
            global_out = x[0].unsqueeze(0)
            attn_out = self.attn_pool(x, batch)
        else:
            # Batched graphs: Find the first index of each batch element
            # Since nodes are sequentially appended, the first node of each batch index is its Global Node
            _, counts = torch.unique(batch, return_counts=True)
            # The indices of the global nodes are the cumulative sums of the counts (shifted by 1)
            # e.g. counts = [10, 15, 5] -> indices = [0, 10, 25]
            ptr = torch.cat([torch.tensor([0], device=x.device), counts.cumsum(0)[:-1]])
            global_out = x[ptr]
            attn_out = self.attn_pool(x, batch)
            
        graph_emb = torch.cat([global_out, attn_out], dim=-1)
        
        return self.output_proj(graph_emb)


def create_v5_encoder(input_dim=46, hidden_dim=128, output_dim=128, num_layers=6, num_relations=10):
    """Factory function matching the v4 API but with v5 architecture."""
    return GNNEncoderV5(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        output_dim=output_dim,
        num_layers=num_layers,
        num_relations=num_relations
    )
