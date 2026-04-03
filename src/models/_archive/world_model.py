
import torch
import torch.nn as nn
import torch.nn.functional as F

from ..features.graph_encoder import create_default_encoder


class WorldModel(nn.Module):
    def __init__(self, state_dim, num_actions, action_emb_dim=64, hidden_dim=512, gnn_layers=4):
        super(WorldModel, self).__init__()
        
        self.state_dim = state_dim
        self.num_actions = num_actions
        
        # 0. Integrated GNN Encoder (Joint Training)
        self.encoder = create_default_encoder(state_dim, num_layers=gnn_layers)
        
        # 1. Action Embedding (larger dim for richer conditioning)
        self.action_emb = nn.Embedding(num_actions, action_emb_dim)
        
        # 2. FiLM Conditioning: action modulates graph embedding
        # Instead of concat (which lets action dominate), the action
        # produces per-dimension scale (gamma) and shift (beta) that
        # multiplicatively interact with the graph embedding.
        self.film_gamma = nn.Sequential(
            nn.Linear(action_emb_dim, state_dim),
            nn.Sigmoid()  # Scale factors in (0, 1) — gates graph features
        )
        self.film_beta = nn.Sequential(
            nn.Linear(action_emb_dim, state_dim),
            nn.Tanh()  # Shift in (-1, 1)
        )
        
        # 3. Transition Model (operates on FiLM-conditioned state)
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2)
        )
        
        self.next_state_head = nn.Linear(hidden_dim, state_dim)
        
        # 4. Metrics Head (also gets raw graph info via skip connection)
        # Input: hidden features + raw graph embedding (skip connection)
        self.metrics_head = nn.Sequential(
            nn.Linear(hidden_dim + state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 6)
        )
        
    def forward(self, x, edge_index, batch, action, edge_attr=None):
        """
        x, edge_index, batch: Graph data (PyG format)
        action: [batch_size] (indices)
        edge_attr: [num_edges] (optional heterogeneous edge types)
        """
        # 1. Encode State (graph-specific embedding)
        state_emb = self.encoder(x, edge_index, batch, edge_type=edge_attr)
        
        # 2. Action Embedding
        a_emb = self.action_emb(action)
        
        # 3. FiLM Conditioning: action modulates graph features
        # This forces the model to use BOTH signals — the action can't
        # ignore the graph because it's multiplicatively combined.
        gamma = self.film_gamma(a_emb)  # Per-dimension scale
        beta = self.film_beta(a_emb)    # Per-dimension shift
        conditioned = gamma * state_emb + beta
        
        # 4. Predict through transition network
        feat = self.net(conditioned)
        
        # 5. Predict Delta State
        delta_state = self.next_state_head(feat)
        next_state_pred = state_emb + delta_state
        
        # 6. Predict Metrics (with action-conditioned skip connection)
        # We explicitly condition the skip connection on the action so the
        # metrics head cannot bypass the action signal and learn an "average"
        # prediction for the program.
        metrics_input = torch.cat([feat, conditioned], dim=1)
        metrics_pred = self.metrics_head(metrics_input)
        
        return next_state_pred, metrics_pred, state_emb

    def transition(self, state_emb, action):
        """
        Latent transition model for MCTS. Predicts next latent state purely from current latent state and action.
        state_emb: [batch_size, state_dim]
        action: [batch_size] (indices)
        """
        a_emb = self.action_emb(action)
        gamma = self.film_gamma(a_emb)
        beta = self.film_beta(a_emb)
        conditioned = gamma * state_emb + beta
        feat = self.net(conditioned)
        delta_state = self.next_state_head(feat)
        
        metrics_input = torch.cat([feat, conditioned], dim=1)
        metrics_pred = self.metrics_head(metrics_input)
        
        return state_emb + delta_state, metrics_pred


def create_world_model(state_dim=128, num_actions=15, gnn_layers=4):
    return WorldModel(state_dim, num_actions, gnn_layers=gnn_layers)
