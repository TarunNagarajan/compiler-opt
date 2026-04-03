"""
v6 World Model — Uses v6 GNN Encoder (HBC)
"""

import torch
import torch.nn as nn
import numpy as np
from .graph_encoder_v6 import create_v6_encoder


class WorldModelV6(nn.Module):
    def __init__(self, state_dim=128, action_dim=59, metrics_dim=6, hidden_dim=256,
                 gnn_layers=6, gnn_input_dim=46, gnn_hidden=128, num_relations=10):
        super().__init__()
        
        # v6 GNN encoder with HBC (Hierarchical Block Condensation)
        self.gnn_encoder = create_v6_encoder(
            input_dim=gnn_input_dim,
            hidden_dim=gnn_hidden,
            output_dim=state_dim,
            num_layers=gnn_layers,
            num_relations=num_relations
        )
        
        self.film_generator = nn.Sequential(
            nn.Linear(action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim * 2)
        )
        
        self.transition = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )
        
        self.metrics_head = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, metrics_dim)
        )
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        
    def encode_graph(self, graph_data):
        return self.gnn_encoder(
            graph_data.x,
            graph_data.edge_index,
            graph_data.edge_attr,
            batch=graph_data.batch if hasattr(graph_data, 'batch') else None,
            block_map=graph_data.block_map if hasattr(graph_data, 'block_map') else None
        )
    
    def forward(self, state_emb, action_onehot, graph_data=None, num_nodes=None):
        if graph_data is not None:
            state_emb = self.encode_graph(graph_data)
            num_nodes = graph_data.x.size(0) - 1
        
        # V7.7: Complexity-Aware Amplification
        if num_nodes is not None:
            if isinstance(num_nodes, torch.Tensor):
                # Batch of node counts
                # V7.9 Fix: Internal clamp to prevent log10(0) nan
                scale_signal = 1.0 + torch.log10(torch.clamp(num_nodes.float(), min=1.0)) / 4.0
                state_emb = state_emb * scale_signal.view(-1, 1)
            else:
                # Scalar node count
                scale_signal = 1.0 + np.log10(max(1, num_nodes)) / 4.0
                state_emb = state_emb * scale_signal

        film_params = self.film_generator(action_onehot)
        gamma, beta = film_params.chunk(2, dim=-1)
        conditioned = gamma * state_emb + beta
        
        delta = self.transition(conditioned)
        next_state = state_emb + delta
        
        # V7.2 Fix: Predict metrics from interaction
        metrics = self.metrics_head(conditioned)
        
        return next_state, metrics
    
    def transition_step(self, state_emb, action_onehot, num_nodes=100):
        # Apply scaling to the latent state based on assumed complexity
        scale_signal = 1.0 + np.log10(max(1, num_nodes)) / 4.0
        scaled_emb = state_emb * scale_signal
        
        film_params = self.film_generator(action_onehot)
        gamma, beta = film_params.chunk(2, dim=-1)
        conditioned = gamma * scaled_emb + beta
        
        delta = self.transition(conditioned)
        next_state = scaled_emb + delta
        metrics = self.metrics_head(conditioned)
        
        return next_state, metrics
