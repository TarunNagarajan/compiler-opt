import torch.nn as nn


class GRUPassHistoryEncoder(nn.Module):
    """
    Encodes the full pass history sequence using a GRU.

    Input: sequence of action indices -> embedded -> GRU -> final hidden state
    Output: [batch, hidden_dim] temporal context vector

    Originally introduced in v5 to fix the "rotation trap" where the agent
    repeats passes because it only sees a fixed window of recent actions.
    The GRU can remember the entire episode.
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
            action_history: Tensor of shape [batch, seq_len] -- action indices, 0-padded
        Returns:
            history_emb: Tensor of shape [batch, hidden_dim]
        """
        embedded = self.action_embed(action_history)  # [batch, seq_len, embed_dim]
        _, hidden = self.gru(embedded)  # hidden: [1, batch, hidden_dim]
        return hidden.squeeze(0)  # [batch, hidden_dim]
