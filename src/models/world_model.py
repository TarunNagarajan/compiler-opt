import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from .world_model_v7 import WorldModelV7, TwoHotSymlogHead

class WorldModel(WorldModelV7):
    """
    World Model V8.5: Decomposed Prediction with Residual Scale Correction
    
    Architecture:
      1. Base pathway (inherited from V7/V8): structure-aware prediction
         - GNN encodes graph → state_emb
         - GSI injects scale context (3D: log_local, log_global, foveation_ratio)
         - Action-gated fusion conditions the embedding
         - metrics_head predicts via Two-Hot SymLog
      
      2. Scale correction pathway (NEW):
         - Takes base_pred.detach() + raw scale context + action embedding
         - Produces additive correction: final_pred = base_pred + correction
         - Initialized to output ZERO (starts at V8.4 quality)
         - .detach() prevents correction gradients from corrupting base pathway
    
    This decomposition separates:
      - "What does this action do to this code structure?" (base, trained on 5,400+ benchmarks)
      - "How does foveation affect the module-level prediction?" (correction, focused on scale)
    
    No catastrophic forgetting possible: the correction is additive and the base
    pathway can be frozen during correction training.
    """
    def __init__(self, state_dim=128, action_dim=67, metrics_dim=6, hidden_dim=256,
                 gnn_layers=6, gnn_input_dim=46, gnn_hidden=128, num_relations=10):
        super().__init__(state_dim, action_dim, metrics_dim, hidden_dim,
                         gnn_layers, gnn_input_dim, gnn_hidden, num_relations)
        
        self.metrics_dim = metrics_dim
        
        # V8 GSI: 3D Context Projector
        # [log10(Local_Nodes), log10(Total_Nodes), Foveation_Ratio]
        self.size_proj = nn.Linear(3, hidden_dim // 4)
        
        # =====================================================================
        # RESIDUAL SCALE CORRECTION (RSC) — Action-Aware
        # 
        # Input (metrics_dim + 4 + action_emb_dim = 18):
        #   - base_pred.detach()  [6] : what the base model predicts
        #   - log_local           [1] : how many nodes the GNN sees
        #   - log_global          [1] : how big the full module is
        #   - foveation_ratio     [1] : what fraction is visible
        #   - scale_gap           [1] : log_global - log_local
        #   - action_emb          [8] : compressed action identity
        #
        # The action embedding lets the correction learn:
        #   - "Unroll at fov≈1.0 → add +5% (cancel the hallucination)"
        #   - "SROA at fov≈1.0 → add 0% (base is already correct)"
        #   - "Unroll at fov≈0.1 → add -9% (scale amplification)"
        #
        # ~1,200 parameters total. Still tiny.
        # =====================================================================
        action_emb_dim = 8
        self.action_correction_emb = nn.Linear(action_dim, action_emb_dim)
        
        correction_input_dim = metrics_dim + 4 + action_emb_dim  # 6 + 4 + 8 = 18
        # RSC v2: Gated-Affine Pathway (Multiplier + Shift)
        # This allows the model to 'scale up' industrial winners (multiplier > 1.0)
        # while 'zeroing out' hallucinations (multiplier ≈ 0, shift ≈ 0).
        self.scale_correction = nn.Sequential(
            nn.Linear(correction_input_dim, 64),
            nn.SiLU(),
            nn.Linear(64, 64),
            nn.SiLU(),
            nn.Linear(64, metrics_dim * 2) # [Multiplier_Raw, Shift_Raw]
        )
        
        # CRITICAL: Initialize final layer to ZERO
        # Multiplier = exp(0) = 1.0, Shift = 0.0. Starts as pure identity.
        nn.init.zeros_(self.scale_correction[-1].weight)
        nn.init.zeros_(self.scale_correction[-1].bias)

    def _normalize_count_tensor(self, value, batch_size, device, name):
        if value is None:
            return torch.ones(batch_size, 1, dtype=torch.float32, device=device)

        if isinstance(value, torch.Tensor):
            t = value.to(device=device, dtype=torch.float32)
        else:
            t = torch.tensor(value, dtype=torch.float32, device=device)

        if t.dim() == 0:
            t = t.view(1, 1)
        elif t.dim() == 1:
            t = t.view(-1, 1)
        elif t.dim() == 2:
            if t.size(1) != 1:
                raise ValueError(f"{name} must have shape [batch] or [batch,1], got {tuple(t.shape)}")
        else:
            raise ValueError(f"{name} must be scalar, [batch], or [batch,1], got {tuple(t.shape)}")

        if t.size(0) == 1 and batch_size > 1:
            t = t.expand(batch_size, 1)
        elif t.size(0) != batch_size:
            raise ValueError(f"{name} batch mismatch: got {t.size(0)}, expected {batch_size}")

        return t.clamp(min=1.0)

    def _apply_scale_correction(self, base_pred, raw_scale, action_onehot):
        action_emb = self.action_correction_emb(action_onehot)
        correction_input = torch.cat([base_pred.detach(), raw_scale, action_emb], dim=-1)
        raw_correction = self.scale_correction(correction_input)

        # Keep multiplier numerically stable during long runs.
        log_multiplier = torch.clamp(raw_correction[:, :self.metrics_dim], min=-6.0, max=6.0)
        multiplier = torch.exp(log_multiplier)
        shift = raw_correction[:, self.metrics_dim:]
        return base_pred * multiplier + shift
        
    def get_size_context(self, num_nodes, device, total_nodes=None):
        """
        V8.5: Returns BOTH the projected context AND the raw scale features.
        The raw features feed into the scale_correction network.
        """
        # 1. Local Scale
        if isinstance(num_nodes, torch.Tensor):
            log_local = torch.log10(num_nodes.float().clamp(min=1.0) + 1.0).view(-1, 1)
        else:
            log_local = torch.tensor([[np.log10(max(1, num_nodes) + 1.0)]], dtype=torch.float32, device=device)
            
        # 2. Global Scale
        if total_nodes is None:
            log_global = log_local
        elif isinstance(total_nodes, torch.Tensor):
            log_global = torch.log10(total_nodes.float().clamp(min=1.0) + 1.0).view(-1, 1)
        else:
            log_global = torch.tensor([[np.log10(max(1, total_nodes) + 1.0)]], dtype=torch.float32, device=device)
            
        # 3. Foveation Ratio
        foveation_ratio = (log_local / (log_global + 1e-6)).clamp(0.0, 1.0)
        
        # 4. Scale Gap: how much code is UNSEEN (0 for small files, large for industrial)
        scale_gap = (log_global - log_local).clamp(min=0.0)
        
        # Project for main pathway
        combined_scale = torch.cat([log_local, log_global, foveation_ratio], dim=-1)
        projected = self.size_proj(combined_scale)
        
        # Raw scale features for correction pathway
        raw_scale = torch.cat([log_local, log_global, foveation_ratio, scale_gap], dim=-1)
        
        return projected, raw_scale

    def forward(self, state_emb, action_onehot, target_metrics=None, graph_data=None,
                num_nodes=None, total_nodes=None, sample_weights=None):
        if action_onehot.dim() != 2:
            raise ValueError(f"action_onehot must be rank-2 [batch, action_dim], got shape {tuple(action_onehot.shape)}")
        if action_onehot.size(1) != self.action_dim:
            raise ValueError(f"action_onehot width mismatch: got {action_onehot.size(1)}, expected {self.action_dim}")

        if graph_data is not None:
            state_emb = self.encode_graph(graph_data)
            if num_nodes is None:
                if hasattr(graph_data, 'batch') and graph_data.batch is not None:
                    _, counts = torch.unique(graph_data.batch, return_counts=True)
                    num_nodes = torch.clamp(counts - 1, min=1)
                else:
                    num_nodes = graph_data.x.size(0) - 1
            
            if total_nodes is None and hasattr(graph_data, 'total_nodes'):
                total_nodes = graph_data.total_nodes

        if state_emb is None:
            raise ValueError("state_emb is required when graph_data is not provided")

        batch_size = state_emb.size(0)
        if action_onehot.size(0) == 1 and batch_size > 1:
            action_onehot = action_onehot.expand(batch_size, -1)
        elif action_onehot.size(0) != batch_size:
            raise ValueError(f"action_onehot batch mismatch: got {action_onehot.size(0)}, expected {batch_size}")

        num_nodes = self._normalize_count_tensor(num_nodes, batch_size, state_emb.device, "num_nodes")
        if total_nodes is None:
            total_nodes = num_nodes
        else:
            total_nodes = self._normalize_count_tensor(total_nodes, batch_size, state_emb.device, "total_nodes")

        # Get both projected context and raw scale features
        size_ctx, raw_scale = self.get_size_context(num_nodes, state_emb.device, total_nodes=total_nodes)
        conditioned = self._condition_state(state_emb, action_onehot, size_ctx)
        
        metric_features = torch.cat([conditioned, action_onehot], dim=-1)
        next_state = state_emb + self.transition(conditioned)
        
        if target_metrics is not None:
            if target_metrics.dim() == 3 and target_metrics.size(1) == 1:
                target_metrics = target_metrics.squeeze(1)
            if target_metrics.dim() != 2 or target_metrics.size(1) != self.metrics_dim:
                raise ValueError(f"target_metrics must have shape [batch,{self.metrics_dim}], got {tuple(target_metrics.shape)}")
            if target_metrics.size(0) != batch_size:
                raise ValueError(f"target_metrics batch mismatch: got {target_metrics.size(0)}, expected {batch_size}")

            # === TRAINING MODE ===
            # 1. Base prediction (Two-Hot SymLog)
            logits = self.metrics_head(metric_features)
            symlog_targets = self.metrics_head.symlog(target_metrics)
            two_hot_targets = self.metrics_head.encode_two_hot(symlog_targets)
            
            log_probs = F.log_softmax(logits, dim=-1)
            per_sample_loss = -(two_hot_targets * log_probs).sum(dim=-1).mean(dim=-1)
            
            if sample_weights is not None:
                sample_weights = sample_weights.to(device=state_emb.device, dtype=torch.float32).view(-1)
                if sample_weights.numel() == 1 and batch_size > 1:
                    sample_weights = sample_weights.expand(batch_size)
                elif sample_weights.numel() != batch_size:
                    raise ValueError(f"sample_weights batch mismatch: got {sample_weights.numel()}, expected {batch_size}")
                metrics_loss = (per_sample_loss * sample_weights).mean()
            else:
                metrics_loss = per_sample_loss.mean()
            
            # 2. Action-aware scale correction (Gated-Affine)
            base_pred = self.metrics_head.predict(metric_features)
            corrected_pred = self._apply_scale_correction(base_pred, raw_scale, action_onehot)
            
            # 3. Correction loss: MSE between corrected prediction and target
            correction_loss = F.mse_loss(corrected_pred, target_metrics)
            
            # 4. Combined loss
            total_loss = metrics_loss + 0.5 * correction_loss
                
            return next_state, total_loss, corrected_pred
        else:
            # === INFERENCE MODE ===
            base_pred = self.metrics_head.predict(metric_features)
            corrected_pred = self._apply_scale_correction(base_pred, raw_scale, action_onehot)
            return next_state, corrected_pred

    def transition_step(self, state_emb, action_onehot, num_nodes=100, total_nodes=None):
        """V8.5 Inference wrapper with action-aware scale correction."""
        if action_onehot.dim() != 2:
            raise ValueError(f"action_onehot must be rank-2 [batch, action_dim], got shape {tuple(action_onehot.shape)}")
        if action_onehot.size(1) != self.action_dim:
            raise ValueError(f"action_onehot width mismatch: got {action_onehot.size(1)}, expected {self.action_dim}")

        batch_size = state_emb.size(0)
        if action_onehot.size(0) == 1 and batch_size > 1:
            action_onehot = action_onehot.expand(batch_size, -1)
        elif action_onehot.size(0) != batch_size:
            raise ValueError(f"action_onehot batch mismatch: got {action_onehot.size(0)}, expected {batch_size}")

        num_nodes = self._normalize_count_tensor(num_nodes, batch_size, state_emb.device, "num_nodes")
        if total_nodes is None:
            total_nodes = num_nodes
        else:
            total_nodes = self._normalize_count_tensor(total_nodes, batch_size, state_emb.device, "total_nodes")

        size_ctx, raw_scale = self.get_size_context(num_nodes, state_emb.device, total_nodes=total_nodes)
        conditioned = self._condition_state(state_emb, action_onehot, size_ctx)
        
        metric_features = torch.cat([conditioned, action_onehot], dim=-1)
        next_state = state_emb + self.transition(conditioned)
        
        base_pred = self.metrics_head.predict(metric_features)
        corrected_pred = self._apply_scale_correction(base_pred, raw_scale, action_onehot)
        
        return next_state, corrected_pred


def create_world_model(state_dim=128, num_actions=67, gnn_layers=6, **kwargs):
    """Factory retained for older scripts that import create_world_model."""
    return WorldModel(
        state_dim=state_dim,
        action_dim=num_actions,
        gnn_layers=gnn_layers,
        **kwargs,
    )
