
import torch
import torch.nn as nn
from .negotiation import NegotiationModule
from .world_model import WorldModel
from ..actions.micro_actions import NUM_MICRO_ACTIONS

PASS_HISTORY_LEN = 5

class HierarchicalMultiAgent(nn.Module):
    """
    Complete Multi-Agent Hierarchical RL system with MAPPO support.
    Now includes pass history conditioning for sequence-awareness.
    """
    def __init__(self, state_dim, num_macros, world_model):
        super(HierarchicalMultiAgent, self).__init__()
        
        # 1. Shared Encoder
        self.encoder = world_model.encoder
        
        # 2. Pass History Encoder
        # Transforms the raw pass history vector into a small embedding
        self.history_encoder = nn.Sequential(
            nn.Linear(PASS_HISTORY_LEN, 32),
            nn.ReLU(),
            nn.Linear(32, 32)
        )
        
        # 3. Strategic Layer (Negotiation Module)
        self.manager = NegotiationModule(state_dim, num_macros, world_model)
        
        # 4. Tactical Layer (Worker Module)
        # Input: state_emb + macro_onehot + history_emb
        self.worker = nn.Sequential(
            nn.Linear(state_dim + num_macros + 32, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, NUM_MICRO_ACTIONS)
        )
        
        # 5. Centralized Critic (Value Function for MAPPO)
        # Input: state_emb + history_emb
        self.critic = nn.Sequential(
            nn.Linear(state_dim + 32, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )

    def _get_history_emb(self, graph_data):
        """Extract pass history embedding from graph data if available."""
        if hasattr(graph_data, 'pass_history') and graph_data.pass_history is not None:
            return self.history_encoder(graph_data.pass_history)
        else:
            # Return zeros if no history (backward compat)
            batch_size = 1
            return torch.zeros(batch_size, 32, device=next(self.parameters()).device)

    def get_value(self, x, edge_index, batch, edge_attr=None, graph_data=None):
        """Returns the state value for advantage calculation."""
        state_emb = self.encoder(x, edge_index, batch, edge_type=edge_attr)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), 32, device=state_emb.device)
        critic_input = torch.cat([state_emb, history_emb], dim=-1)
        return self.critic(critic_input)

    def get_macro_action(self, x, edge_index, batch, edge_attr=None):
        """Step 1: The Manager selects a Macro strategy."""
        state_emb = self.encoder(x, edge_index, batch, edge_type=edge_attr)
        macro_probs, agent_weights = self.manager(x, edge_index, batch, state_emb, edge_attr=edge_attr)
        return macro_probs, agent_weights

    def get_micro_action(self, x, edge_index, batch, macro_idx, edge_attr=None, graph_data=None):
        """Step 2: The Worker refines the chosen strategy."""
        state_emb = self.encoder(x, edge_index, batch, edge_type=edge_attr)
        history_emb = self._get_history_emb(graph_data) if graph_data else torch.zeros(state_emb.size(0), 32, device=state_emb.device)
        
        # One-hot encoding of chosen macro (Fixed for Batched inputs)
        batch_size = state_emb.size(0)
        macro_onehot = torch.zeros(batch_size, self.manager.num_macros, device=state_emb.device)
        
        # Ensure macro_idx is [Batch, 1] for scatter
        m_idx = macro_idx.view(-1, 1)
        macro_onehot.scatter_(1, m_idx, 1.0)
        
        # Worker decision: state + macro + history
        worker_input = torch.cat([state_emb, macro_onehot, history_emb], dim=-1)
        micro_logits = self.worker(worker_input)
        return micro_logits

def create_hrl_agent(state_dim, num_macros, world_model_path, gnn_layers=6):
    # Load the specialized world model
    from .world_model import create_world_model
    from ..config import NUM_ACTIONS
    
    wm = create_world_model(state_dim=state_dim, num_actions=NUM_ACTIONS, gnn_layers=gnn_layers)
    
    checkpoint = torch.load(world_model_path, map_location='cpu', weights_only=False)
    state_dict = checkpoint['model_state_dict'] if 'model_state_dict' in checkpoint else checkpoint
    
    # ROBUST LOADING: Handle action space expansion
    if 'action_emb.weight' in state_dict:
        old_size = state_dict['action_emb.weight'].shape[0]
        new_size = wm.action_emb.weight.shape[0]
        if old_size != new_size:
            print(f"[MODEL] Resizing World Model Action Embedding: {old_size} -> {new_size}")
            # Create a temporary buffer for the old weights
            old_weights = state_dict['action_emb.weight']
            # Update the state_dict with a new tensor of the correct size
            new_weights = torch.zeros((new_size, old_weights.shape[1]))
            new_weights[:old_size, :] = old_weights
            state_dict['action_emb.weight'] = new_weights
            
    wm.load_state_dict(state_dict)
    
    return HierarchicalMultiAgent(state_dim, num_macros, wm)
