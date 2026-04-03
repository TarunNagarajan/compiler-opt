import torch
import torch.nn as nn
import torch.nn.functional as F
from ..actions.micro_actions import NUM_MICRO_ACTIONS

class HRLWorker(nn.Module):
    """
    Tactical Worker Module for Phase 7.
    Input: state_emb + macro_onehot + history_emb
    Output: Softmax distribution over NUM_MICRO_ACTIONS
    """
    def __init__(self, state_dim, num_macros, history_dim=32, hidden_dim=256):
        super(HRLWorker, self).__init__()
        
        # Input: state (128) + macro (25) + history (32) = 185
        input_dim = state_dim + num_macros + history_dim
        
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, NUM_MICRO_ACTIONS)
        )

    def forward(self, state_emb, macro_onehot, history_emb):
        worker_input = torch.cat([state_emb, macro_onehot, history_emb], dim=-1)
        logits = self.net(worker_input)
        return F.softmax(logits, dim=-1)
