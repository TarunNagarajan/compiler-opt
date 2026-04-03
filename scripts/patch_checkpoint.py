import torch
import torch.nn as nn
from pathlib import Path

def patch_hrl_checkpoint(old_ckpt_path, new_ckpt_path):
    print(f"[PATCH] Adapting {old_ckpt_path} to FINAL 18-macro architecture (including STOP)...")
    old_sd = torch.load(old_ckpt_path, weights_only=True)
    new_sd = old_sd.copy()

    # List of specialist heads that grew from 15 to 18
    specialists = [
        "manager.performance_agent.action_head",
        "manager.speed_agent.action_head",
        "manager.size_agent.action_head",
        "manager.security_agent.action_head"
    ]

    for s in specialists:
        w_key = f"{s}.weight"
        b_key = f"{s}.bias"
        
        old_w = old_sd[w_key]
        old_b = old_sd[b_key]
        
        # Create new tensors with size 18 (15 original + O3 + O2 + STOP)
        new_w = torch.randn(18, old_w.size(1)) * 0.01
        new_b = torch.zeros(18)
        
        # Graft old intelligence into the first 15 slots
        new_w[:15, :] = old_w
        new_b[:15] = old_b
        
        new_sd[w_key] = new_w
        new_sd[b_key] = new_b
        print(f"  -> Patched {s} (15 -> 18)")

    # Patch the Tactical Worker (Worker layer 0 weight)
    # The input size grew from 128+15 (143) to 128+18 (146)
    worker_w_key = "worker.0.weight"
    old_worker_w = old_sd[worker_w_key]
    
    new_worker_w = torch.randn(256, 146) * 0.01
    new_worker_w[:, :128] = old_worker_w[:, :128] # State
    new_worker_w[:, 128:143] = old_worker_w[:, 128:143] # Old macro weights
    
    new_sd[worker_w_key] = new_worker_w
    print(f"  -> Patched tactical worker input (143 -> 146)")

    torch.save(new_sd, new_ckpt_path)
    print(f"[SUCCESS] Beast-v3 patched checkpoint saved to: {new_ckpt_path}")

if __name__ == "__main__":
    # We go back to the source (Hour 0619) to ensure a clean graft
    patch_hrl_checkpoint("models/hrl_industrial_hour_0619.pth", "models/hrl_beast_v3.pth")
