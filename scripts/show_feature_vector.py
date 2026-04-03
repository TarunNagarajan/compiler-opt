import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to the Python path to allow importing from 'src'
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from src.features.feature_vector import extract_features, TOP_INSTRUCTIONS
except ImportError as e:
    print(f"Error: Unable to import from 'src'. Please ensure you are running this script from the 'compiler-opt' directory.")
    print(f"Details: {e}")
    sys.exit(1)


def get_feature_descriptions() -> List[Dict[str, Any]]:
    """
    Returns a list of dictionaries, each describing a feature.
    """
    descriptions = [
        # --- Instruction Ratios (5 features) ---
        {"name": "pct_arithmetic", "description": "Percentage of arithmetic instructions (e.g., add, sub, mul, div)."},
        {"name": "pct_memory", "description": "Percentage of memory access instructions (e.g., load, store, alloca)."},
        {"name": "pct_control", "description": "Percentage of control flow instructions (e.g., br, switch, ret)."},
        {"name": "pct_comparison", "description": "Percentage of comparison instructions (e.g., icmp, fcmp)."},
        {"name": "pct_other", "description": "Percentage of other instructions not in the above categories."},

        # --- Top Instruction Frequencies (15 features) ---
    ]
    
    for instr in TOP_INSTRUCTIONS:
        descriptions.append(
            {"name": f"freq_{instr}", "description": f"Frequency of the '{instr}' instruction relative to the total number of instructions."}
        )
        
    descriptions.extend([
        # --- Normalized Counts (4 features) ---
        {"name": "norm_functions", "description": "Number of functions, normalized to a maximum of 100."}, 
        {"name": "norm_blocks", "description": "Number of basic blocks, normalized to a maximum of 1000."}, 
        {"name": "norm_instructions", "description": "Total number of instructions, normalized to a maximum of 10,000."}, 
        {"name": "norm_loops", "description": "Estimated number of loops, normalized to a maximum of 50."},
        
        # --- Derived Ratios (4 features) ---
        {"name": "instr_per_block", "description": "Average number of instructions per basic block, normalized to a max of 50."}, 
        {"name": "calls_per_func", "description": "Average number of 'call' instructions per function, normalized to a max of 20."}, 
        {"name": "blocks_per_func", "description": "Average number of basic blocks per function, normalized to a max of 100."}, 
        {"name": "branch_density", "description": "Density of branch instructions relative to total instructions, normalized to a max of 0.5."},
    ])
    
    return descriptions


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/show_feature_vector.py <path_to_ir_file.ll>")
        sys.exit(1)
        
    ir_file = Path(sys.argv[1])
    if not ir_file.exists():
        print(f"Error: File not found at '{ir_file}'")
        sys.exit(1)
        
    print(f"Analyzing feature vector for: {ir_file.name}\n")
    
    # Extract the full 128-dim vector
    feature_vector = extract_features(ir_file)
    
    # Get the descriptions for the implemented features
    feature_descriptions = get_feature_descriptions()
    
    # --- Print in a formatted table ---
    print(f"{'Index':<6} | {'Feature Name':<20} | {'Value':<10} | {'Description'}")
    print("-" * 80)

    for i, desc in enumerate(feature_descriptions):
        name = desc['name']
        description = desc['description']
        value = feature_vector[i]
        
        # Don't print features that are zero unless they are part of the core set
        if value == 0.0 and i > 28:
            continue

        print(f"{i:<6} | {name:<20} | {f'{value:.4f}':<10} | {description}")

    num_implemented = len(feature_descriptions)
    if feature_vector.shape[0] > num_implemented:
        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
