import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from .graph_encoder import create_v6_encoder as create_encoder

class TwoHotSymlogHead(nn.Module):
    """
    Two-hot categorical encoding for SymLog targets.
    
    Predicts categorical distributions over fixed bins in symlog space 
    to improve numerical stability.
    """
    def __init__(self, in_dim, out_dim=6, num_bins=255, min_val=-20.0, max_val=20.0):
        super().__init__()
        self.out_dim = out_dim
        self.num_bins = num_bins
        self.min_val = min_val
        self.max_val = max_val
        
        self.register_buffer('bins', torch.linspace(min_val, max_val, num_bins))
        
        self.net = nn.Sequential(
            nn.Linear(in_dim, 256),
            nn.LayerNorm(256),
            nn.SiLU(),
            nn.Linear(256, 256),
            nn.LayerNorm(256),
            nn.SiLU(),
            nn.Linear(256, out_dim * num_bins)
        )
        
    def symlog(self, x):
        return torch.sign(x) * torch.log(1 + torch.abs(x))
        
    def symexp(self, x):
        return torch.sign(x) * (torch.exp(torch.abs(x)) - 1)
        
    def encode_two_hot(self, labels):
        labels = torch.clamp(labels, self.min_val, self.max_val)
        delta = (self.max_val - self.min_val) / (self.num_bins - 1)
        b = (labels - self.min_val) / delta
        
        lower_idx = torch.floor(b).long()
        upper_idx = torch.ceil(b).long()
        lower_weight = upper_idx.float() - b
        upper_weight = b - lower_idx.float()
        
        exact_match = (lower_idx == upper_idx)
        lower_weight[exact_match] = 1.0
        upper_weight[exact_match] = 0.0
        
        lower_idx = torch.clamp(lower_idx, 0, self.num_bins - 1)
        upper_idx = torch.clamp(upper_idx, 0, self.num_bins - 1)
        
        batch_size = labels.size(0)
        two_hot = torch.zeros(batch_size, self.out_dim, self.num_bins, device=labels.device)
        b_idx = torch.arange(batch_size, device=labels.device).view(-1, 1).expand(-1, self.out_dim)
        d_idx = torch.arange(self.out_dim, device=labels.device).view(1, -1).expand(batch_size, -1)
        
        two_hot[b_idx, d_idx, lower_idx] = lower_weight
        two_hot[b_idx, d_idx, upper_idx] = upper_weight
        return two_hot
        
    def forward(self, features):
        logits = self.net(features)
        return logits.view(-1, self.out_dim, self.num_bins)
        
    def loss(self, features, targets):
        logits = self.forward(features)
        symlog_targets = self.symlog(targets)
        two_hot_targets = self.encode_two_hot(symlog_targets)
        log_probs = F.log_softmax(logits, dim=-1)
        return -(two_hot_targets * log_probs).sum(dim=-1).mean()
        
    def predict(self, features):
        logits = self.forward(features)
        probs = F.softmax(logits, dim=-1)
        expected_symlog = (probs * self.bins.view(1, 1, -1)).sum(dim=-1)
        return self.symexp(expected_symlog)

class WorldModelBase(nn.Module):
    """
    Base world model for transition and metric prediction.
    """
    def __init__(self, state_dim=128, action_dim=59, metrics_dim=6, hidden_dim=256,
                 gnn_layers=6, gnn_input_dim=46, gnn_hidden=128, num_relations=10):
        super().__init__()
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        
        self.gnn_encoder = create_encoder(
            input_dim=gnn_input_dim,
            hidden_dim=gnn_hidden,
            output_dim=state_dim,
            num_layers=gnn_layers,
            num_relations=num_relations
        )
        
        self.size_proj = nn.Linear(1, hidden_dim // 4)
        self.action_gate = nn.Linear(action_dim, hidden_dim * 2) 
        self.state_proj = nn.Linear(state_dim + (hidden_dim // 4), hidden_dim)
        
        self.transition = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.LayerNorm(hidden_dim * 2),
            nn.SiLU(),
            nn.Linear(hidden_dim * 2, state_dim)
        )
        
        self.metrics_head = TwoHotSymlogHead(in_dim=hidden_dim + action_dim, out_dim=metrics_dim)
        
    def get_size_context(self, num_nodes, device):
        if isinstance(num_nodes, torch.Tensor):
            log_size = torch.log10(num_nodes.float().clamp(min=1.0) + 1.0).view(-1, 1)
        else:
            log_size = torch.tensor([[np.log10(max(1, num_nodes) + 1.0)]], dtype=torch.float32, device=device)
        return self.size_proj(log_size)
        
    def encode_graph(self, graph_data):
        return self.gnn_encoder(
            graph_data.x,
            graph_data.edge_index,
            graph_data.edge_attr,
            batch=graph_data.batch if hasattr(graph_data, 'batch') else None,
            block_map=graph_data.block_map if hasattr(graph_data, 'block_map') else None
        )
        
    def _condition_state(self, state_emb, action_onehot, size_ctx):
        contextual_state = torch.cat([state_emb, size_ctx], dim=-1)
        mapped_state = self.state_proj(contextual_state)
        gate_scale = self.action_gate(action_onehot)
        gate, scale = gate_scale.chunk(2, dim=-1)
        return mapped_state * torch.sigmoid(gate) + torch.tanh(scale)
        
    def forward(self, state_emb, action_onehot, target_metrics=None, graph_data=None, num_nodes=None):
        if graph_data is not None:
            state_emb = self.encode_graph(graph_data)
            if num_nodes is None:
                if hasattr(graph_data, 'batch') and graph_data.batch is not None:
                    _, counts = torch.unique(graph_data.batch, return_counts=True)
                    num_nodes = torch.clamp(counts - 1, min=1)
                else:
                    num_nodes = graph_data.x.size(0) - 1
            
        size_ctx = self.get_size_context(num_nodes, state_emb.device)
        conditioned = self._condition_state(state_emb, action_onehot, size_ctx)
        metric_features = torch.cat([conditioned, action_onehot], dim=-1)
        next_state = state_emb + self.transition(conditioned)
        
        if target_metrics is not None:
            metrics_loss = self.metrics_head.loss(metric_features, target_metrics)
            pred_metrics = self.metrics_head.predict(metric_features)
            return next_state, metrics_loss, pred_metrics
        else:
            pred_metrics = self.metrics_head.predict(metric_features)
            return next_state, pred_metrics
            
    def transition_step(self, state_emb, action_onehot, num_nodes=100):
        size_ctx = self.get_size_context(num_nodes, state_emb.device)
        conditioned = self._condition_state(state_emb, action_onehot, size_ctx)
        metric_features = torch.cat([conditioned, action_onehot], dim=-1)
        next_state = state_emb + self.transition(conditioned)
        pred_metrics = self.metrics_head.predict(metric_features)
        return next_state, pred_metrics
