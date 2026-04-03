import torch
import torch.nn as nn
import json
import os

class CalibratedWorldModel(nn.Module):
    """
    V8.4: Clean Pass-Through Wrapper.
    
    After V8.5 and Phase 6 Offline Meta-Calibrator, the base predictions are
    fed into the standalone Meta Calibrator (a tiny MLP trained with L1 loss
    to exactly squash noise while preserving large-scale precision).
    """
    def __init__(self, base_model, meta_calibrator_path=None, meta_threshold=None, strict_meta=True):
        super().__init__()
        self.base_model = base_model
        self.meta_threshold = float(meta_threshold) if meta_threshold is not None else 0.4
        self.strict_meta = strict_meta
        
        self.meta_net = None
        if meta_calibrator_path:
            from .meta_calibrator import MetaCalibrator
            device = next(base_model.parameters()).device
            self.meta_net = MetaCalibrator(pred_dim=6, action_dim=self.base_model.action_dim, hidden_dim=64).to(device)
            # Find closest matching relative path if executed differently
            if not os.path.exists(meta_calibrator_path):
                alt_path = os.path.join(os.getcwd(), meta_calibrator_path)
                if os.path.exists(alt_path):
                    meta_calibrator_path = alt_path
                elif strict_meta:
                    raise FileNotFoundError(f"Meta-Calibrator checkpoint not found: {meta_calibrator_path}")
                else:
                    print(f"[Warning] Meta-Calibrator checkpoint not found: {meta_calibrator_path}")
                    self.meta_net = None
                    return
            
            try:
                payload = torch.load(meta_calibrator_path, map_location=device)
                loaded_threshold = None
                if isinstance(payload, dict) and 'state_dict' in payload:
                    loaded_threshold = payload.get('inference_threshold', None)
                    payload = payload['state_dict']
                self.meta_net.load_state_dict(payload)
                self.meta_net.eval()

                if meta_threshold is None:
                    if loaded_threshold is not None:
                        self.meta_threshold = float(loaded_threshold)
                    else:
                        sidecar_path = os.path.splitext(meta_calibrator_path)[0] + ".meta.json"
                        if os.path.exists(sidecar_path):
                            with open(sidecar_path, "r", encoding="utf-8") as f:
                                metadata = json.load(f)
                            if 'inference_threshold' in metadata:
                                self.meta_threshold = float(metadata['inference_threshold'])
            except Exception as e:
                if strict_meta:
                    raise RuntimeError(f"Failed to load Meta-Calibrator from {meta_calibrator_path}: {e}") from e
                print(f"[Warning] Failed to load Meta-Calibrator from {meta_calibrator_path}: {e}")
                self.meta_net = None

    @property
    def action_dim(self):
        return self.base_model.action_dim

    def _align_action_batch(self, action_onehot, batch_size):
        if action_onehot.dim() != 2:
            raise ValueError(f"action_onehot must be rank-2 [batch, action_dim], got {tuple(action_onehot.shape)}")
        if action_onehot.size(0) == 1 and batch_size > 1:
            return action_onehot.expand(batch_size, -1)
        if action_onehot.size(0) != batch_size:
            raise ValueError(f"action_onehot batch mismatch: got {action_onehot.size(0)}, expected {batch_size}")
        return action_onehot

    def _to_scale_tensor(self, scale_source, batch_size, device):
        if scale_source is None:
            return torch.full((batch_size, 1), 100.0, dtype=torch.float32, device=device)

        if isinstance(scale_source, torch.Tensor):
            scale = scale_source.to(device=device, dtype=torch.float32)
        else:
            scale = torch.tensor(scale_source, dtype=torch.float32, device=device)

        if scale.dim() == 0:
            scale = scale.view(1, 1)
        elif scale.dim() == 1:
            scale = scale.view(-1, 1)
        elif scale.dim() == 2:
            if scale.size(1) != 1:
                raise ValueError(f"Scale tensor must have shape [batch] or [batch,1], got {tuple(scale.shape)}")
        else:
            raise ValueError(f"Scale tensor rank must be <=2, got {tuple(scale.shape)}")

        if scale.size(0) == 1 and batch_size > 1:
            scale = scale.expand(batch_size, 1)
        elif scale.size(0) != batch_size:
            raise ValueError(f"Scale batch mismatch: got {scale.size(0)}, expected {batch_size}")

        return scale.clamp(min=1.0)

    def forward(self, state_emb, action_onehot, graph_data=None, num_nodes=None, total_nodes=None):
        out_state, raw_metrics = self.base_model(
            state_emb=state_emb, 
            action_onehot=action_onehot, 
            graph_data=graph_data, 
            num_nodes=num_nodes,
            total_nodes=total_nodes
        )
        
        if self.meta_net is not None:
            batch_size = raw_metrics.size(0)
            action_for_meta = self._align_action_batch(action_onehot, batch_size)

            if total_nodes is not None:
                scale_source = total_nodes
            elif graph_data is not None and hasattr(graph_data, 'total_nodes'):
                scale_source = getattr(graph_data, 'total_nodes')
            elif num_nodes is not None:
                scale_source = num_nodes
            elif graph_data is not None:
                if hasattr(graph_data, 'batch') and graph_data.batch is not None:
                    _, counts = torch.unique(graph_data.batch, return_counts=True)
                    scale_source = torch.clamp(counts - 1, min=1)
                else:
                    scale_source = torch.tensor([max(graph_data.x.size(0) - 1, 1)], dtype=torch.float32, device=raw_metrics.device)
            else:
                scale_source = None

            scale_tensor = self._to_scale_tensor(scale_source, batch_size, raw_metrics.device)
            raw_metrics = self.meta_net(raw_metrics, action_for_meta, scale_tensor, threshold=self.meta_threshold)
             
        return out_state, raw_metrics

    def encode_graph(self, graph_data):
        return self.base_model.encode_graph(graph_data)
        
    def transition_step(self, state_emb, action_onehot, num_nodes=100, total_nodes=None):
        out_state, raw_metrics = self.base_model.transition_step(
            state_emb=state_emb, 
            action_onehot=action_onehot, 
            num_nodes=num_nodes, 
            total_nodes=total_nodes
        )
        
        if self.meta_net is not None:
            batch_size = raw_metrics.size(0)
            action_for_meta = self._align_action_batch(action_onehot, batch_size)
            scale_source = total_nodes if total_nodes is not None else num_nodes
            scale_tensor = self._to_scale_tensor(scale_source, batch_size, raw_metrics.device)
            raw_metrics = self.meta_net(raw_metrics, action_for_meta, scale_tensor, threshold=self.meta_threshold)
             
        return out_state, raw_metrics
