"""
v5 World Model — Uses v5 GNN Encoder

Changes from v4 (world_model.py):
1. Uses GNNEncoderV5 with attention pooling + 7 relation types
2. Compatible with v4 FiLM conditioning, transition, and metrics heads
3. Can load partial weights from v4 checkpoints (GNN layers transfer, pooling head is new)
"""

import torch
import torch.nn as nn
from .graph_encoder_v5 import create_v5_encoder


class WorldModelV5(nn.Module):
    def __init__(self, state_dim=128, action_dim=59, metrics_dim=6, hidden_dim=256,
                 gnn_layers=6, gnn_input_dim=46, gnn_hidden=128, num_relations=10):
        super().__init__()
        
        # v5 GNN encoder with attention pooling + 7 relations
        self.gnn_encoder = create_v5_encoder(
            input_dim=gnn_input_dim,
            hidden_dim=gnn_hidden,
            output_dim=state_dim,
            num_layers=gnn_layers,
            num_relations=num_relations
        )
        
        # FiLM Conditioning: Action → (scale, shift) for state modulation
        self.film_generator = nn.Sequential(
            nn.Linear(action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim * 2)  # gamma + beta
        )
        
        # Transition Network: Predicts next latent state (residual)
        self.transition = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )
        
        # Metrics Head: Predicts optimization metrics
        self.metrics_head = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, metrics_dim)
        )
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        
    def encode_graph(self, graph_data):
        """Encode an IR graph into a latent state vector."""
        return self.gnn_encoder(
            graph_data.x,
            graph_data.edge_index,
            graph_data.edge_attr,
            batch=graph_data.batch if hasattr(graph_data, 'batch') else None
        )
    
    def forward(self, state_emb, action_onehot, graph_data=None):
        """
        Full forward: encode graph (if given) → FiLM condition → predict next state + metrics.
        """
        if graph_data is not None:
            state_emb = self.encode_graph(graph_data)
        
        # FiLM conditioning
        film_params = self.film_generator(action_onehot)
        gamma, beta = film_params.chunk(2, dim=-1)
        conditioned = gamma * state_emb + beta
        
        # Residual transition
        delta = self.transition(conditioned)
        next_state = state_emb + delta
        
        # Metrics prediction
        metrics = self.metrics_head(next_state)
        
        return next_state, metrics
    
    def transition_step(self, state_emb, action_onehot):
        """
        Lightweight transition for MCTS rollouts (no graph encoding needed).
        """
        film_params = self.film_generator(action_onehot)
        gamma, beta = film_params.chunk(2, dim=-1)
        conditioned = gamma * state_emb + beta
        
        delta = self.transition(conditioned)
        next_state = state_emb + delta
        metrics = self.metrics_head(next_state)
        
        return next_state, metrics

    @classmethod
    def load_from_v4(cls, v4_checkpoint_path, **kwargs):
        """
        Load a v4 checkpoint, transferring compatible weights.
        Handles key name mapping (v4 encoder.* → v5 gnn_encoder.*) and
        RGCN weight shape differences (6 relations → 7 relations).
        """
        model = cls(**kwargs)
        
        v4_state = torch.load(v4_checkpoint_path, map_location='cpu', weights_only=False)
        if 'model_state_dict' in v4_state:
            v4_state = v4_state['model_state_dict']
        
        # Key mapping: v4 name → v5 name
        KEY_MAP = {
            'encoder.input_proj.weight': 'gnn_encoder.input_proj.weight',
            'encoder.input_proj.bias': 'gnn_encoder.input_proj.bias',
            'encoder.output_proj.weight': 'gnn_encoder.output_proj.weight',
            'encoder.output_proj.bias': 'gnn_encoder.output_proj.bias',
        }
        # Dynamic mapping for layers/convs and norms
        for i in range(10):  # up to 10 layers
            KEY_MAP[f'encoder.layers.{i}.root'] = f'gnn_encoder.convs.{i}.root'
            KEY_MAP[f'encoder.layers.{i}.bias'] = f'gnn_encoder.convs.{i}.bias'
            KEY_MAP[f'encoder.layers.{i}.weight'] = f'gnn_encoder.convs.{i}.weight'
            KEY_MAP[f'encoder.norms.{i}.weight'] = f'gnn_encoder.norms.{i}.weight'
            KEY_MAP[f'encoder.norms.{i}.bias'] = f'gnn_encoder.norms.{i}.bias'
        # Also map non-encoder keys that might exist
        for k in v4_state:
            if k not in KEY_MAP and not k.startswith('encoder.'):
                KEY_MAP[k] = k  # Keep as-is (film_generator, transition, metrics_head, action_emb)
        
        model_state = model.state_dict()
        transferred = 0
        skipped = 0
        partial = 0
        
        for v4_key, v4_value in v4_state.items():
            v5_key = KEY_MAP.get(v4_key, v4_key)
            
            if v5_key not in model_state:
                skipped += 1
                continue
            
            v5_shape = model_state[v5_key].shape
            
            if v4_value.shape == v5_shape:
                # Exact match — direct copy
                model_state[v5_key] = v4_value
                transferred += 1
            elif 'weight' in v5_key and 'convs' in v5_key and len(v4_value.shape) == 3:
                # RGCN weight: v4 is [6*H, H, 1] or [6, H, H], v5 is [7*H, H, 1] or [7, H, H]
                # Copy the first 6 relations, leave 7th (loop_back) randomly initialized
                v4_rels = v4_value.shape[0]
                v5_rels = v5_shape[0]
                if v4_rels < v5_rels and v4_value.shape[1:] == v5_shape[1:]:
                    model_state[v5_key][:v4_rels] = v4_value
                    partial += 1
                else:
                    skipped += 1
            else:
                skipped += 1
        
        model.load_state_dict(model_state)
        print(f"[WorldModelV5] Loaded from v4: {transferred} exact, {partial} partial (6→7 rels), {skipped} skipped")
        return model
