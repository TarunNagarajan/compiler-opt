import os
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

log_dir = "logs/hrl/antigravity_v4_hrl_20260226_2012"
print(f"Reading Tensorboard logs from: {log_dir}")

event_acc = EventAccumulator(log_dir)
event_acc.Reload()

tags = event_acc.Tags()
print("\nLog Tags found:", tags)

print("\n--- Recent Training Metrics ---")
try:
    for tag in tags.get('scalars', []):
        events = event_acc.Scalars(tag)
        if events:
            # Get the last 5 events
            recent = events[-5:]
            vals = [e.value for e in recent]
            avg_recent = sum(vals) / len(vals)
            print(f"{tag}:")
            print(f"  Latest val: {vals[-1]:.4f}")
            print(f"  Recent avg: {avg_recent:.4f}")
            print(f"  Trend (last 5): {[round(v, 4) for v in vals]}")
            print()
except Exception as e:
    print("Error parsing specific tags:", e)
