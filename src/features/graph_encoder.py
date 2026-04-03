
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import RGCNConv, global_mean_pool, global_max_pool

class GNNEncoder(nn.Module):
    """
    Heterogeneous GNN with Residual Connections.
    4 layers to avoid over-smoothing while capturing local+global structure.
    """
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers=4, num_relations=6):
        super(GNNEncoder, self).__init__()
        self.layers = nn.ModuleList()
        self.norms = nn.ModuleList()
        
        # 1. Initial Embedding / Projection
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # 2. Deep Relational Layers
        for i in range(num_layers):
            # RGCN handles heterogeneous edge types (0-4)
            self.layers.append(RGCNConv(hidden_dim, hidden_dim, num_relations=num_relations))
            self.norms.append(nn.LayerNorm(hidden_dim))
                
        # 3. Output Head
        self.output_proj = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, edge_index, batch=None, edge_type=None):
        # Fallback for old callers who don't pass edge_type
        if edge_type is None:
            edge_type = torch.zeros(edge_index.size(1), dtype=torch.long, device=edge_index.device)
            
        # 1. Input Projection
        x = F.leaky_relu(self.input_proj(x), 0.2)
        
        # 2. Deep GNN with Residuals
        for i, (conv, norm) in enumerate(zip(self.layers, self.norms)):
            identity = x
            x = conv(x, edge_index, edge_type)
            x = F.leaky_relu(x, 0.2)
            x = norm(x)
            x = x + identity
            
        # 3. Rich Pooling: mean + max for program-specific signal
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        
        x_mean = global_mean_pool(x, batch)
        x_max = global_max_pool(x, batch)
        x_pooled = x_mean + x_max  # Additive combination preserves both signals
        
        # 4. Final Projection (NO L2 normalization — preserve magnitude!)
        out = self.output_proj(x_pooled)
        return out

def create_default_encoder(feature_dim=128, num_layers=4):
    # Match the enriched IRGraphExtractor output dim (40 opcode + 4 type = 44)
    # 6 edge types: 0=next, 1=branch, 2=data, 3=global_out, 4=global_in, 5=call
    INPUT_DIM = 44 
    return GNNEncoder(input_dim=INPUT_DIM, hidden_dim=128, output_dim=feature_dim, num_layers=num_layers, num_relations=6)
