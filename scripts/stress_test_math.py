"""
V7.8 Numerical Stability Stress Test
Verifies that the new complexity scaling and log-transforms are nan-proof.
"""

import torch
import torch.nn.functional as F
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.world_model_v6 import WorldModelV6

def stress_test():
    print("🧪 Starting V7.8 Stress Test...")
    device = torch.device("cpu")
    model = WorldModelV6(gnn_layers=2).to(device) # Small layers for fast test
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    # Test Case 1: The "Empty" Graph (The NaN Killer)
    print("--- Case 1: Empty Graph (1 node total) ---")
    state_emb = torch.randn(1, 128)
    action_oh = torch.zeros(1, 59); action_oh[0, 5] = 1.0
    
    # Simulate num_nodes = 0 (after subtraction)
    try:
        next_s, metrics = model.forward(state_emb, action_oh, num_nodes=torch.tensor([0]))
        if torch.isnan(next_s).any() or torch.isnan(metrics).any():
            print("❌ FAILED: NaN detected in Empty Graph case!")
        else:
            print("✅ PASSED: Empty Graph handled safely.")
    except Exception as e:
        print(f"❌ FAILED: Exception in Empty Graph: {e}")

    # Test Case 2: The "Library" Scale (100,000 nodes)
    print("--- Case 2: Massive Library (100,000 nodes) ---")
    try:
        next_s, metrics = model.forward(state_emb, action_oh, num_nodes=torch.tensor([100000]))
        if torch.isnan(next_s).any() or torch.isnan(metrics).any():
            print("❌ FAILED: NaN detected in Massive Scale case!")
        else:
            print(f"✅ PASSED: Massive Scale handled. Scale Signal: {1.0 + np.log10(100000)/4.0:.2f}x")
    except Exception as e:
        print(f"❌ FAILED: Exception in Massive Scale: {e}")

    # Test Case 3: Log-Metric Backward Pass
    print("--- Case 3: Log-Metric Backward Pass (Stability) ---")
    target_delta = torch.tensor([[-0.25, 0.0, 0.0, 0.0, 0.0, 0.0]]) # 25% win
    log_target = torch.sign(target_delta) * torch.log1p(torch.abs(target_delta) * 10.0)
    
    optimizer.zero_grad()
    _, pred_met = model.forward(state_emb, action_oh, num_nodes=torch.tensor([500]))
    loss = F.mse_loss(pred_met, log_target)
    loss.backward()
    
    # Check gradients
    has_nan_grad = False
    for p in model.parameters():
        if p.grad is not None and torch.isnan(p.grad).any():
            has_nan_grad = True
            break
    
    if has_nan_grad:
        print("❌ FAILED: NaN detected in Gradients!")
    else:
        print("✅ PASSED: Backward pass is numerically stable.")

    # Test Case 4: Latent Transition Step
    print("--- Case 4: Pure Latent Transition Step ---")
    try:
        # Pass exactly what the eval script passes
        _, pred_met_log = model.transition_step(state_emb, action_oh, num_nodes=1000)
        if torch.isnan(pred_met_log).any():
            print("❌ FAILED: NaN in transition_step!")
        else:
            print("✅ PASSED: Latent transition is stable.")
    except Exception as e:
        print(f"❌ FAILED: Exception in transition_step: {e}")

    print("\n🏁 STRESS TEST COMPLETE.")

if __name__ == "__main__":
    stress_test()
