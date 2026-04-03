import torch
import torch.nn as nn
import torch.nn.functional as F

class MetaCalibrator(nn.Module):
    """
    Two-Stage Hurdle Model: 
    1. Gate Network (Binary Classifier): Predicts if the action does ANYTHING.
    2. Magnitude Network (Conditional Regressor): If gate is open, predict HOW MUCH.
    """
    def __init__(self, pred_dim=6, action_dim=151, hidden_dim=64):
        super().__init__()
        
        self.input_dim = pred_dim + action_dim + 1 # +1 for the scale feature
        
        # 1. Gate Network (Classification)
        # Using LayerNorm because scale_nodes has extreme range (175 vs 22,000)
        # Outputs a logit
        self.gate = nn.Sequential(
            nn.Linear(self.input_dim, 128),
            nn.LayerNorm(128),
            nn.SiLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.LayerNorm(64),
            nn.SiLU(),
            nn.Linear(64, 1)
        )
        
        # 2. Magnitude Network (Regression)
        self.magnitude = nn.Sequential(
            nn.Linear(self.input_dim, 64),
            nn.SiLU(),
            nn.Linear(64, 32),
            nn.SiLU(),
            nn.Linear(32, pred_dim)
        )
        
        # Residual Skip Connection Parameter
        self.learned_scale = nn.Parameter(torch.ones(pred_dim))
        
        nn.init.zeros_(self.magnitude[-1].weight)
        nn.init.zeros_(self.magnitude[-1].bias)

    def forward(self, v8_prediction, action_onehot, num_nodes, threshold=0.4, return_gate_logit=False):
        """
        Inference: Uses Hard Gating.
        """
        if v8_prediction.dim() != 2:
            raise ValueError(f"v8_prediction must be rank-2 [batch,pred_dim], got {tuple(v8_prediction.shape)}")
        if action_onehot.dim() != 2:
            raise ValueError(f"action_onehot must be rank-2 [batch,action_dim], got {tuple(action_onehot.shape)}")

        if action_onehot.size(0) == 1 and v8_prediction.size(0) > 1:
            action_onehot = action_onehot.expand(v8_prediction.size(0), -1)
        elif action_onehot.size(0) != v8_prediction.size(0):
            raise ValueError(f"Batch mismatch: predictions={v8_prediction.size(0)}, actions={action_onehot.size(0)}")

        if not isinstance(num_nodes, torch.Tensor):
            num_nodes = torch.tensor(num_nodes, dtype=torch.float32, device=v8_prediction.device)
        else:
            num_nodes = num_nodes.to(device=v8_prediction.device, dtype=torch.float32)

        if num_nodes.dim() == 0:
            num_nodes = num_nodes.view(1, 1)
        elif num_nodes.dim() == 1:
            num_nodes = num_nodes.unsqueeze(1)
        elif num_nodes.dim() == 2:
            if num_nodes.size(1) != 1:
                raise ValueError(f"num_nodes must have shape [batch] or [batch,1], got {tuple(num_nodes.shape)}")
        else:
            raise ValueError(f"num_nodes must be scalar, [batch], or [batch,1], got {tuple(num_nodes.shape)}")

        if num_nodes.size(0) == 1 and v8_prediction.size(0) > 1:
            num_nodes = num_nodes.expand(v8_prediction.size(0), 1)
        elif num_nodes.size(0) != v8_prediction.size(0):
            raise ValueError(f"Batch mismatch: predictions={v8_prediction.size(0)}, num_nodes={num_nodes.size(0)}")

        scale_feature = torch.log10(num_nodes.clamp(min=1.0)).clamp(min=0.0, max=8.0)
        x = torch.cat([v8_prediction, action_onehot, scale_feature], dim=-1)
        if x.size(1) != self.input_dim:
            raise ValueError(f"MetaCalibrator input width mismatch: got {x.size(1)}, expected {self.input_dim}")
        
        gate_logit = self.gate(x)
        
        if return_gate_logit:
            mag = (v8_prediction * self.learned_scale) + self.magnitude(x)
            return gate_logit, mag
            
        gate_prob = torch.sigmoid(gate_logit)
        gate_mask = (gate_prob > threshold).float()
        
        # Final = v8_pred * learned_scale + correction
        mag_correction = self.magnitude(x)
        final_magnitude = (v8_prediction * self.learned_scale) + mag_correction
        
        # Hard Gating
        return final_magnitude * gate_mask
