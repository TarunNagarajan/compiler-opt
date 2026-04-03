import torch

dataset = torch.load("models/meta_dataset.pt", map_location='cpu', weights_only=False)

unroll_idx = 61
total_unrolls = 0
decreases = 0
increases = 0
zeros = 0
avg_decrease = 0.0
avg_increase = 0.0

for item in dataset:
    action_onehot = item['action']
    action_idx = int(torch.argmax(action_onehot).item())
    
    if action_idx == unroll_idx:
        total_unrolls += 1
        true_val = item['truth'][0].item()  # Index 0 is inst_delta_pct
        
        if abs(true_val) < 1e-5:
            zeros += 1
        elif true_val < 0:
            decreases += 1
            avg_decrease += true_val
        else:
            increases += 1
            avg_increase += true_val

if total_unrolls > 0:
    print(f"Total Unroll actions in dataset: {total_unrolls}")
    print(f"Zeros (no effect): {zeros} ({zeros/total_unrolls*100:.1f}%)")
    print(f"Increases (bloat): {increases} ({increases/total_unrolls*100:.1f}%)")
    print(f"Decreases (shrink): {decreases} ({decreases/total_unrolls*100:.1f}%)")
    if decreases > 0:
        print(f"Avg shrink: {avg_decrease/decreases*100:.2f}%")
    if increases > 0:
        print(f"Avg bloat: {avg_increase/increases*100:.2f}%")
else:
    print("No unroll actions found.")
