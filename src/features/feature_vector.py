import numpy as np
from pathlib import Path
from typing import Union

from .ir_parser import IRParser, IRStats
from ..config import FEATURE_DIM


TOP_INSTRUCTIONS = [
    'load', 'store', 'alloca', 'getelementptr',
    'add', 'sub', 'mul',
    'icmp', 'br', 'call', 'ret',
    'phi', 'sext', 'zext', 'trunc'
]

MAX_FUNCTIONS = 100
MAX_BLOCKS = 1000
MAX_INSTRUCTIONS = 10000
MAX_LOOPS = 50
MAX_CALLS = 500


def normalize(value: float, max_val: float) -> float:
    return min(value / max_val, 1.0)


def extract_features(ir_path: Union[str, Path]) -> np.ndarray:
    parser = IRParser(str(ir_path))
    stats = parser.parse()
    ratios = parser.get_instruction_ratios()
    
    features = np.zeros(FEATURE_DIM, dtype=np.float32)
    idx = 0
    
    features[idx] = ratios['pct_arithmetic']; idx += 1
    features[idx] = ratios['pct_memory']; idx += 1
    features[idx] = ratios['pct_control']; idx += 1
    features[idx] = ratios['pct_comparison']; idx += 1
    features[idx] = ratios['pct_other']; idx += 1
    
    total_instr = max(stats.num_instructions, 1)
    for instr in TOP_INSTRUCTIONS:
        count = stats.instruction_counts.get(instr, 0)
        features[idx] = count / total_instr
        idx += 1
    
    features[idx] = normalize(stats.num_functions, MAX_FUNCTIONS); idx += 1
    features[idx] = normalize(stats.num_basic_blocks, MAX_BLOCKS); idx += 1
    features[idx] = normalize(stats.num_instructions, MAX_INSTRUCTIONS); idx += 1
    features[idx] = normalize(stats.num_loops, MAX_LOOPS); idx += 1
    
    if stats.num_basic_blocks > 0:
        features[idx] = normalize(stats.num_instructions / stats.num_basic_blocks, 50)
    idx += 1
    
    if stats.num_functions > 0:
        features[idx] = normalize(stats.num_calls / stats.num_functions, 20)
    idx += 1
    
    if stats.num_functions > 0:
        features[idx] = normalize(stats.num_basic_blocks / stats.num_functions, 100)
    idx += 1
    
    if stats.num_instructions > 0:
        features[idx] = normalize(stats.num_branches / stats.num_instructions, 0.5)
    idx += 1
    
    return features


def compare_features(ir_path1: str, ir_path2: str) -> dict:
    f1 = extract_features(ir_path1)
    f2 = extract_features(ir_path2)
    
    diff = f2 - f1
    l2_distance = np.linalg.norm(diff)
    
    return {
        'features_before': f1,
        'features_after': f2,
        'difference': diff,
        'l2_distance': l2_distance,
        'num_changed': np.sum(np.abs(diff) > 0.001),
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python feature_vector.py <ir_file.ll> [ir_file2.ll]")
        sys.exit(1)
    
    features = extract_features(sys.argv[1])
    
    print(f"\n=== Feature Vector for {sys.argv[1]} ===")
    print(f"Shape: {features.shape}")
    print(f"Non-zero features: {np.sum(features != 0)}")
    print(f"Min: {features.min():.4f}, Max: {features.max():.4f}")
    
    print(f"\n=== First 28 features (named) ===")
    names = (
        ['pct_arithmetic', 'pct_memory', 'pct_control', 'pct_comparison', 'pct_other']
        + [f'freq_{instr}' for instr in TOP_INSTRUCTIONS]
        + ['norm_functions', 'norm_blocks', 'norm_instructions', 'norm_loops']
        + ['instr_per_block', 'calls_per_func', 'blocks_per_func', 'branch_density']
    )
    for i, name in enumerate(names):
        print(f"  [{i:2d}] {name:20s} = {features[i]:.4f}")
    
    if len(sys.argv) >= 3:
        print(f"\n=== Comparing with {sys.argv[2]} ===")
        comparison = compare_features(sys.argv[1], sys.argv[2])
        print(f"L2 distance: {comparison['l2_distance']:.4f}")
        print(f"Features changed: {comparison['num_changed']}")
