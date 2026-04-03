import os
from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def get_max_step():
    log_dir = Path("logs/hrl")
    max_step = 0
    print("Parsing tensorboard logs to calculate true global step...")
    for d in sorted(log_dir.glob("antigravity_v4_hrl_*"), key=os.path.getmtime):
        ea = EventAccumulator(str(d))
        ea.Reload()
        # tensorboard's EventAccumulator uses a different tag structure, we can check ea.Tags()
        tags = ea.Tags().get("scalars", [])
        if "Live/Reward" in tags:
            events = ea.Scalars("Live/Reward")
            if events:
                local_max = max(e.step for e in events)
                print(f"Run {d.name}: {local_max} steps")
                max_step += local_max
    print(f"\nTRUE GLOBAL STEP: {max_step}")

if __name__ == "__main__":
    get_max_step()
