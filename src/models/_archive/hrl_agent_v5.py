"""
v5 HRL Agent — GRU Pass History + v5 Architecture

Changes from v4 (hrl_agent.py):
1. NEW: GRU-based pass history encoder (replaces fixed 5-step MLP)
   - Processes FULL episode history as a sequence
   - Hidden state carries temporal context across steps
2. Uses v5 world model (attention pooling + 7 relations)
3. All other components (manager, worker, critic) are architecturally compatible with v4

The GRU addresses the "rotation trap" — the v4 agent repeats passes because
it only sees the last 5 actions. The GRU can remember the entire episode.
"""

import torch
import torch.nn as nn
from .negotiation import NegotiationModule
from ..actions.micro_actions import NUM_MICRO_ACTIONS
from ..config import NUM_ATOMIC_ACTIONS


class GRUPassHistoryEncoder(nn.Module):
    """
    Encodes the full pass history sequence using a GRU.
    
    v4 used:  Linear(5 → 32) — fixed window, no temporal reasoning.
    v5 uses:  GRU(action_dim → 32) — variable-length, full episode memory.
    
    Input: sequence of action indices → embedded → GRU → final hidden state (32-dim)
    """
    
    def __init__(self, num_actions, embed_dim=16, hidden_dim=32):
        super().__init__()
        self.action_embed = nn.Embedding(num_actions + 1, embed_dim, padding_idx=0)
        self.gru = nn.GRU(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True
        )
        self.hidden_dim = hidden_dim
        
    def forward(self, action_history):
        """
        Args:
            action_history: Tensor of shape [batch, seq_len] — action indices, 0-padded
        Returns:
            history_emb: Tensor of shape [batch, hidden_dim]
        """
        # Embed action indices
        embedded = self.action_embed(action_history)  # [batch, seq_len, embed_dim]
        
        # GRU processes the full sequence
        _, hidden = self.gru(embedded)  # hidden: [1, batch, hidden_dim]
        
        return hidden.squeeze(0)  # [batch, hidden_dim]


class HierarchicalMultiAgentV5(nn.Module):
    """
    v5 HRL Agent with:
    - v5 GNN encoder (attention pooling + 7 relations) via world model
    - GRU pass history (full episode memory)
    - Same Manager/Worker/Critic architecture as v4 for weight transfer
    """
    
    def __init__(self, state_dim, num_macros, world_model, num_actions=59):
        super().__init__()
        
        # 1. Shared Encoder (from v5 world model)
        self.encoder = world_model.gnn_encoder
        
        # 2. GRU Pass History Encoder (NEW — replaces fixed-window MLP)
        self.history_encoder = GRUPassHistoryEncoder(
            num_actions=num_actions,
            embed_dim=16,
            hidden_dim=32
        )
        self.history_dim = 32
        
        # 3. Strategic Layer (Negotiation Module)
        self.manager = NegotiationModule(state_dim, num_macros, world_model, history_dim=32, action_offset=num_actions - num_macros)
        
        # 4. Tactical Layer (Worker Module)
        # Input: state_emb + macro_onehot + history_emb
        self.worker = nn.Sequential(
            nn.Linear(state_dim + num_macros + self.history_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, NUM_MICRO_ACTIONS)
        )
        
        # 5. Centralized Critic (Value Function for MAPPO)
        # Input: state_emb + history_emb
        self.critic = nn.Sequential(
            nn.Linear(state_dim + self.history_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
    
    def _get_history_emb(self, graph_data):
        """Extract pass history embedding using GRU."""
        if hasattr(graph_data, 'action_history') and graph_data.action_history is not None:
            # v5 path: full episode action sequence
            history = graph_data.action_history
            if history.dim() == 1:
                history = history.unsqueeze(0)  # [1, seq_len]
            return self.history_encoder(history)
        elif hasattr(graph_data, 'pass_history') and graph_data.pass_history is not None:
            # v4 fallback: treat the 5-element vector as a sequence of indices
            # Convert normalized indices back to action IDs (approximate)
            hist = graph_data.pass_history
            if hist.dim() == 1:
                hist = hist.unsqueeze(0)
            # Approximate: scale back from [0,1] to action indices
            action_ids = (hist * 59).long().clamp(0, 59)
            return self.history_encoder(action_ids)
        else:
            batch_size = 1
            return torch.zeros(batch_size, self.history_dim, device=next(self.parameters()).device)

    def get_value(self, x, edge_index, batch, edge_attr=None, graph_data=None):
        """Returns the state value for advantage calculation."""
        state_emb = self.encoder(x, edge_index, edge_attr, batch=batch)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        critic_input = torch.cat([state_emb, history_emb], dim=-1)
        return self.critic(critic_input)

    def get_macro_action(self, x, edge_index, batch, edge_attr=None, graph_data=None):
        """Step 1: The Manager selects a Macro strategy (now history-aware)."""
        state_emb = self.encoder(x, edge_index, edge_attr, batch=batch)
        history_emb = self._get_history_emb(graph_data) if graph_data else None
        macro_probs, agent_weights = self.manager(x, edge_index, batch, state_emb, edge_attr=edge_attr, history_emb=history_emb)
        return macro_probs, agent_weights

    def get_micro_action(self, x, edge_index, batch, macro_idx, edge_attr=None, graph_data=None):
        """Step 2: The Worker refines the chosen strategy."""
        state_emb = self.encoder(x, edge_index, edge_attr, batch=batch)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        
        batch_size = state_emb.size(0)
        macro_onehot = torch.zeros(batch_size, self.manager.num_macros, device=state_emb.device)
        m_idx = macro_idx.view(-1, 1)
        macro_onehot.scatter_(1, m_idx, 1.0)
        
        worker_input = torch.cat([state_emb, macro_onehot, history_emb], dim=-1)
        micro_logits = self.worker(worker_input)
        return micro_logits


def create_hrl_agent_v5(state_dim, num_macros, world_model_path=None, gnn_layers=6, 
                         v4_checkpoint_path=None, num_actions=59):
    """
    Factory function for v5 HRL agent.
    
    Can optionally warm-start from:
    - v4 world model checkpoint (partial weight transfer)
    - v4 HRL checkpoint (manager/worker/critic weights transfer, GRU starts fresh)
    """
    from .world_model_v5 import WorldModelV5
    
    if world_model_path:
        # Load v5 world model checkpoint directly
        wm = WorldModelV5(state_dim=state_dim, action_dim=num_actions, gnn_layers=gnn_layers)
        checkpoint = torch.load(world_model_path, map_location='cpu', weights_only=False)
        state_dict = checkpoint.get('model_state_dict', checkpoint)
        wm.load_state_dict(state_dict, strict=False)
        print(f"[HRL-v5] Loaded v5 world model from {world_model_path}")
    else:
        wm = WorldModelV5(state_dim=state_dim, action_dim=num_actions, gnn_layers=gnn_layers)
    
    agent = HierarchicalMultiAgentV5(state_dim, num_macros, wm, num_actions=num_actions)
    
    # Optionally transfer v4 HRL weights
    if v4_checkpoint_path:
        v4_state = torch.load(v4_checkpoint_path, map_location='cpu', weights_only=False)
        if 'model_state_dict' in v4_state:
            v4_state = v4_state['model_state_dict']
        
        model_state = agent.state_dict()
        transferred = 0
        for key, value in v4_state.items():
            # Skip the old history encoder (MLP → GRU, incompatible)
            if 'history_encoder' in key:
                continue
            if key in model_state and model_state[key].shape == value.shape:
                model_state[key] = value
                transferred += 1
        
        agent.load_state_dict(model_state)
        print(f"[HRL-v5] Warm-started from v4: {transferred} weights transferred (GRU history starts fresh)")
    
    return agent
