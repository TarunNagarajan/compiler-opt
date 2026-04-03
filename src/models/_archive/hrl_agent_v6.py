"""
v6 HRL Agent — Foveated HBC Architecture
"""

import torch
import torch.nn as nn
from .negotiation import NegotiationModule
from ..actions.micro_actions import NUM_MICRO_ACTIONS
from ..config import NUM_ATOMIC_ACTIONS, NUM_ACTIONS


class HierarchicalMultiAgentV6(nn.Module):
    """
    v6 HRL Agent with:
    - v6 GNN encoder (HBC / Foveated) via world model
    - GRU pass history (full episode memory)
    """
    
    def __init__(self, state_dim, num_macros, world_model, num_actions=NUM_ACTIONS):
        super().__init__()
        
        # 1. Shared Encoder (from v6 world model)
        self.encoder = world_model.gnn_encoder
        
        # 2. GRU Pass History Encoder
        from .hrl_agent_v5 import GRUPassHistoryEncoder
        self.history_encoder = GRUPassHistoryEncoder(
            num_actions=num_actions,
            embed_dim=16,
            hidden_dim=32
        )
        self.history_dim = 32
        
        # 3. Strategic Layer (Negotiation Module)
        self.manager = NegotiationModule(state_dim, num_macros, world_model, history_dim=32, action_offset=num_actions - num_macros)
        
        # 4. Tactical Layer (Worker Module)
        self.worker = nn.Sequential(
            nn.Linear(state_dim + num_macros + self.history_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, NUM_MICRO_ACTIONS)
        )
        
        # 5. Centralized Critic (Value Function for MAPPO)
        self.critic = nn.Sequential(
            nn.Linear(state_dim + self.history_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
    
    def _get_history_emb(self, graph_data):
        if hasattr(graph_data, 'action_history') and graph_data.action_history is not None:
            history = graph_data.action_history
            if history.dim() == 1: history = history.unsqueeze(0)
            return self.history_encoder(history)
        elif hasattr(graph_data, 'pass_history') and graph_data.pass_history is not None:
            hist = graph_data.pass_history
            if hist.dim() == 1: hist = hist.unsqueeze(0)
            action_ids = (hist * NUM_ACTIONS).long().clamp(0, NUM_ACTIONS)
            return self.history_encoder(action_ids)
        else:
            return torch.zeros(1, self.history_dim, device=next(self.parameters()).device)

    def encode_state(self, x, edge_index, edge_attr, batch, block_map=None):
        return self.encoder(x, edge_index, edge_attr, batch=batch, block_map=block_map)

    def get_value(self, x, edge_index, batch, edge_attr=None, graph_data=None):
        block_map = getattr(graph_data, 'block_map', None) if graph_data else None
        state_emb = self.encode_state(x, edge_index, edge_attr, batch, block_map=block_map)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        critic_input = torch.cat([state_emb, history_emb], dim=-1)
        return self.critic(critic_input)

    def get_macro_action(self, x, edge_index, batch, edge_attr=None, graph_data=None):
        block_map = getattr(graph_data, 'block_map', None) if graph_data else None
        state_emb = self.encode_state(x, edge_index, edge_attr, batch, block_map=block_map)
        history_emb = self._get_history_emb(graph_data) if graph_data else None
        # V7 Fix: Pass graph_data so the Manager's internal World Model simulations use foveated vision
        macro_probs, agent_weights = self.manager(x, edge_index, batch, state_emb, edge_attr=edge_attr, history_emb=history_emb, graph_data=graph_data)
        return macro_probs, agent_weights

    def get_micro_action(self, x, edge_index, batch, macro_idx, edge_attr=None, graph_data=None):
        block_map = getattr(graph_data, 'block_map', None) if graph_data else None
        state_emb = self.encode_state(x, edge_index, edge_attr, batch, block_map=block_map)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        
        batch_size = state_emb.size(0)
        macro_onehot = torch.zeros(batch_size, self.manager.num_macros, device=state_emb.device)
        macro_onehot.scatter_(1, macro_idx.view(-1, 1), 1.0)
        
        worker_input = torch.cat([state_emb, macro_onehot, history_emb], dim=-1)
        return self.worker(worker_input)


def create_hrl_agent_v6(state_dim, num_macros, world_model_path=None, gnn_layers=6, num_actions=NUM_ACTIONS):
    from .world_model_v6 import WorldModelV6
    
    wm = WorldModelV6(state_dim=state_dim, action_dim=num_actions, gnn_layers=gnn_layers)
    if world_model_path:
        ckpt = torch.load(world_model_path, map_location='cpu', weights_only=False)
        wm.load_state_dict(ckpt.get('model_state_dict', ckpt), strict=False)
        print(f"[HRL-v6] Loaded world model eyes from {world_model_path}")
    
    return HierarchicalMultiAgentV6(state_dim, num_macros, wm, num_actions=num_actions)
