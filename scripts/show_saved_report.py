import json
from pathlib import Path

def main():
    """
    Loads pre-computed evaluation data from JSON files and prints a
    comparison table for the HACKABLE and SECURE models.
    """
    log_dir = Path(__file__).parent.parent / "logs"
    hackable_json_path = log_dir / "hackable_50k_eval.json"
    secure_json_path = log_dir / "secure_50k_eval.json"

    if not hackable_json_path.exists() or not secure_json_path.exists():
        print(f"Error: Could not find evaluation logs in {log_dir}")
        print(f"Looked for: {hackable_json_path.name}, {secure_json_path.name}")
        return

    with open(hackable_json_path) as f:
        hackable_data = json.load(f)

    with open(secure_json_path) as f:
        secure_data = json.load(f)

    metrics = {
        'Instruction Reduction': {
            'HACKABLE': f"{hackable_data['avg_instruction_reduction']:.1f}%",
            'SECURE': f"{secure_data['avg_instruction_reduction']:.1f}%"
        },
        'Size Increase': {
            'HACKABLE': f"{-hackable_data['avg_size_change']:.1f}%",
            'SECURE': f"{-secure_data['avg_size_change']:.1f}%"
        },
        'Pass Diversity': {
            'HACKABLE': f"{hackable_data['avg_pass_diversity']:.2f}",
            'SECURE': f"{secure_data['avg_pass_diversity']:.2f}"
        },
        'Episode Reward': {
            # The user's table has these values swapped
            'HACKABLE': f"{hackable_data['avg_episode_reward']:.2f}",
            'SECURE': f"{secure_data['avg_episode_reward']:.2f}"
        }
    }

    # --- Print the table ---
    print(f"{'Metric':<22}| {'HACKABLE':<9}| {'SECURE'}")
    print("-" * 45)
    
    for metric_name, values in metrics.items():
        print(f"{metric_name:<22}| {values['HACKABLE']:<9}| {values['SECURE']}")

if __name__ == "__main__":
    main()
