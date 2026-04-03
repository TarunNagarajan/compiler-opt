import torch
import torch.nn as nn
import torch.nn.functional as F
from .negotiation import NegotiationModule
from .hrl_agent_v5 import GRUPassHistoryEncoder
from .hrl_worker_v8 import HRLWorker
from ..actions.micro_actions import NUM_MICRO_ACTIONS
from ..config import NUM_ATOMIC_ACTIONS

class HRLAgent(nn.Module):
    """
    v8 HRL Agent with:
    - v8.5 Base GNN encoder (inherited from CalibratedWorldModel)
    - Calibrated World Model integration (Hurdle Gating + Industrial Scale)
    - GRU pass history (full episode memory)
    """
    
    def __init__(self, state_dim, num_macros, world_model, num_actions=151):
        super().__init__()
        
        # 1. Calibrated World Model (Wraps V8.5 base + Meta-Calibrator)
        # Inherits the GNN encoder directly from the world model's base pathway
        self.world_model = world_model
        self.encoder = world_model.base_model.gnn_encoder
        
        # 2. GRU Pass History Encoder
        self.history_encoder = GRUPassHistoryEncoder(
            num_actions=num_actions,
            embed_dim=16,
            hidden_dim=32
        )
        self.history_dim = 32
        
        # 3. Strategic Layer (Negotiation Module)
        self.manager = NegotiationModule(
            state_dim, 
            num_macros, 
            world_model, 
            history_dim=32, 
            action_offset=NUM_ATOMIC_ACTIONS
        )
        
        # 4. Tactical Layer (Worker Module)
        self.worker = HRLWorker(state_dim, num_macros, history_dim=32, hidden_dim=256)
        
        # 5. Centralized Critic (Value Function for MAPPO)
        # Input: state_emb + history_emb
        self.critic = nn.Sequential(
            nn.Linear(state_dim + self.history_dim, 256),
            nn.SiLU(),
            nn.Linear(256, 256),
            nn.SiLU(),
            nn.Linear(256, 1)
        )

    def forward(self, x, edge_index, batch, edge_attr=None, action_history=None, graph_data=None):
        """
        Policy Forward Pass:
        1. Encodes graph structure
        2. Encodes temporal history
        3. Negotiates a macro goal (Strategic)
        4. Selects a micro refinement (Tactical)
        """
        # 1. State Encoding
        # V6 Encoder needs block_map for HBC optimization!
        block_map = getattr(graph_data, 'block_map', None)
        state_emb = self.encoder(x, edge_index, edge_attr, batch=batch, block_map=block_map)
        
        # V6 encoder already returns a graph-level embedding [batch, state_dim]
        # if it's unbatched, it returns [1, state_dim]. 
        # No extra pooling needed here.
            
        # 2. History Encoding [batch, seq_len]
        if action_history is None:
            action_history = torch.zeros(state_emb.size(0), 1, dtype=torch.long, device=state_emb.device)
        history_emb = self.history_encoder(action_history)
        
        # 3. Manager Negotiation (Macro Goal Selection)
        macro_probs, agent_weights = self.manager(
            x, edge_index, batch, state_emb, 
            edge_attr=edge_attr, 
            history_emb=history_emb,
            graph_data=graph_data
        )
        
        return macro_probs, agent_weights, history_emb, state_emb

    def get_value(self, state_emb, history_emb):
        return self.critic(torch.cat([state_emb, history_emb], dim=-1))

    def get_worker_act(self, state_emb, macro_onehot, history_emb):
        # Pass individual tensors; HRLWorker.forward handles concatenation and softmax
        return self.worker(state_emb, macro_onehot, history_emb)
