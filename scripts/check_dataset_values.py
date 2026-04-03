import torch
import os

def main():
    if not os.path.exists("meta_dataset.pt"):
        print("meta_dataset.pt not found")
        return
        
    data = torch.load("meta_dataset.pt")
    print(f"Loaded {len(data)} samples")
    
    unroll_samples = []
    for sample in data:
        # Action index for unroll is 61 (atomic) or find it in action onehot
        action_idx = sample['action'].argmax().item()
        if action_idx == 0: # Check if Action 61 in Atomic
             # Atomic Action 0 in LLVM_PASSES is unroll? No, let's check config.
             pass
        
        # In MACRO_ACTIONS or LLVM_PASSES?
        # Action 61 is Atomic.
        if action_idx == 0: # LLVM_PASSES[0] is function(loop-unroll)
            unroll_samples.append(sample)
            
    print(f"Found {len(unroll_samples)} Unroll samples")
    if unroll_samples:
         truths = torch.stack([s['truth'] for s in unroll_samples])
         print(f"Unroll Truth (Index 0 - Inst Delta %):")
         print(f"  Mean: {truths[:, 0].mean().item():.2f}")
         print(f"  Min:  {truths[:, 0].min().item():.2f}")
         print(f"  Max:  {truths[:, 0].max().item():.2f}")
         
         predictions = torch.stack([s['v8_prediction'] for s in unroll_samples])
         print(f"Unroll Base Prediction (Index 0):")
         print(f"  Mean: {predictions[:, 0].mean().item():.2f}")
         print(f"  Min:  {predictions[:, 0].min().item():.2f}")
         print(f"  Max:  {predictions[:, 0].max().item():.2f}")

if __name__ == "__main__":
    main()
