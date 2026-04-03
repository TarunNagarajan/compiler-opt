"""
Direct BEAT_O3 Policy — Lean agent for beating -O3 on runtime.

Strips out the negotiation module (4 specialists + world model imagination)
and replaces it with a direct policy: GNN encoder -> policy head -> action.

Architecture:
  GNNEncoderV6 (reused, frozen or fine-tuned) -> state_emb [128]
  GRUPassHistoryEncoder (reused) -> history_emb [32]
  PolicyHead: [160] -> [256] -> [256] -> [num_actions] logits
  ValueHead:  [160] -> [256] -> [256] -> [1] value estimate
"""

import torch
import torch.nn as nn
from torch.distributions import Categorical

from .graph_encoder import GNNEncoderV6
from .history_encoder import GRUPassHistoryEncoder
from ..config import FEATURE_DIM, NUM_ACTIONS


class DirectBeatO3Policy(nn.Module):

    def __init__(self, state_dim=FEATURE_DIM, num_actions=NUM_ACTIONS,
                 history_dim=32, hidden_dim=256):
        super().__init__()
        self.state_dim = state_dim
        self.num_actions = num_actions
        self.history_dim = history_dim

        # Reusable components (load weights from existing checkpoints)
        self.encoder = GNNEncoderV6(
            in_channels=46,
            hidden_channels=state_dim,
            out_channels=state_dim,
            num_relations=7,
            num_layers=6,
        )
        self.history_encoder = GRUPassHistoryEncoder(
            num_actions=num_actions,
            embed_dim=16,
            hidden_dim=history_dim,
        )

        combined_dim = state_dim + history_dim

        # Direct policy head
        self.policy_head = nn.Sequential(
            nn.Linear(combined_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, num_actions),
        )

        # Value head (separate network for PPO)
        self.value_head = nn.Sequential(
            nn.Linear(combined_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )

    # ------------------------------------------------------------------
    def _encode(self, x, edge_index, batch=None, edge_attr=None,
                action_history=None, graph_data=None):
        """Shared encoder forward: graph + history -> combined embedding."""
        block_map = getattr(graph_data, 'block_map', None) if graph_data else None
        state_emb = self.encoder(x, edge_index, edge_attr, batch=batch,
                                 block_map=block_map)

        if action_history is None:
            action_history = torch.zeros(
                state_emb.size(0), 1, dtype=torch.long, device=state_emb.device)
        history_emb = self.history_encoder(action_history)

        combined = torch.cat([state_emb, history_emb], dim=-1)
        return combined, state_emb, history_emb

    # ------------------------------------------------------------------
    def forward(self, x, edge_index, batch=None, edge_attr=None,
                action_history=None, graph_data=None):
        """Returns action logits, state_emb, history_emb."""
        combined, state_emb, history_emb = self._encode(
            x, edge_index, batch, edge_attr, action_history, graph_data)
        logits = self.policy_head(combined)
        return logits, state_emb, history_emb

    # ------------------------------------------------------------------
    def get_action_and_value(self, x, edge_index, batch=None, edge_attr=None,
                             action_history=None, graph_data=None):
        """
        Rollout inference: sample action + compute value.

        Returns (action, log_prob, value, state_emb, history_emb).
        """
        combined, state_emb, history_emb = self._encode(
            x, edge_index, batch, edge_attr, action_history, graph_data)

        logits = self.policy_head(combined)
        dist = Categorical(logits=logits)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        value = self.value_head(combined).squeeze(-1)

        return action, log_prob, value, state_emb, history_emb

    # ------------------------------------------------------------------
    def evaluate(self, x, edge_index, action, batch=None, edge_attr=None,
                 action_history=None, graph_data=None):
        """
        PPO re-evaluation: compute log_prob, value, entropy for given action.

        Returns (log_prob, value, entropy).
        """
        combined, state_emb, history_emb = self._encode(
            x, edge_index, batch, edge_attr, action_history, graph_data)

        logits = self.policy_head(combined)
        dist = Categorical(logits=logits)
        log_prob = dist.log_prob(action)
        entropy = dist.entropy().mean()
        value = self.value_head(combined).squeeze(-1)

        return log_prob, value, entropy

    # ------------------------------------------------------------------
    def get_value(self, state_emb, history_emb):
        """Value estimate from cached embeddings (used in GAE)."""
        combined = torch.cat([state_emb, history_emb], dim=-1)
        return self.value_head(combined).squeeze(-1)

    # ------------------------------------------------------------------
    @classmethod
    def from_pretrained_gnn(cls, checkpoint_path, device='cpu', **kwargs):
        """
        Create a DirectBeatO3Policy and load the GNN encoder weights
        from an existing world model or HRL checkpoint.
        """
        policy = cls(**kwargs).to(device)
        ckpt = torch.load(checkpoint_path, map_location=device)

        # Try loading GNN encoder from various checkpoint formats
        state_dict = ckpt if isinstance(ckpt, dict) and 'model_state_dict' not in ckpt else \
            ckpt.get('model_state_dict', ckpt)

        # Extract GNN encoder weights
        gnn_prefix_candidates = [
            'gnn_encoder.',          # world model v8
            'base_model.gnn_encoder.',  # calibrated wrapper
            'encoder.',              # hrl agent v8
        ]

        loaded = False
        for prefix in gnn_prefix_candidates:
            gnn_weights = {
                k.replace(prefix, ''): v
                for k, v in state_dict.items()
                if k.startswith(prefix)
            }
            if gnn_weights:
                res = policy.encoder.load_state_dict(gnn_weights, strict=False)
                if len(res.unexpected_keys) == 0:
                    print(f"[BEAT-O3] Loaded GNN encoder from prefix '{prefix}' "
                          f"({len(gnn_weights)} params, "
                          f"{len(res.missing_keys)} missing)")
                    loaded = True
                    break

        if not loaded:
            print("[BEAT-O3] WARNING: Could not load GNN encoder weights")

        return policy
