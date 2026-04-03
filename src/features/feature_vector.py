
import numpy as np
import torch
from pathlib import Path
from typing import Union

from .ir_parser import IRParser
from ..config import FEATURE_DIM


TOP_INSTRUCTIONS = [
    'load', 'store', 'alloca', 'getelementptr',
    'add', 'sub', 'mul',
    'icmp', 'br', 'call', 'ret',
    'phi', 'sext', 'zext', 'trunc'
]


def normalize(value: float, max_val: float) -> float:
    return min(value / max_val, 1.0)


def extract_scalar_features(ir_path: Union[str, Path]) -> np.ndarray:
    """Extract the scalar (non-GNN) features from an IR file.
    These are combined with the GNN embedding by the canonical encoder."""
    parser = IRParser(str(ir_path))
    stats = parser.parse()
    ratios = parser.get_instruction_ratios()
    
    scalar_features = []
    
    scalar_features.append(ratios['pct_arithmetic'])
    scalar_features.append(ratios['pct_memory'])
    scalar_features.append(ratios['pct_control'])
    scalar_features.append(ratios['pct_comparison'])
    scalar_features.append(ratios['pct_other'])
    
    total_instr = max(stats.num_instructions, 1)
    for instr in TOP_INSTRUCTIONS:
        count = stats.instruction_counts.get(instr, 0)
        scalar_features.append(count / total_instr)
    
    scalar_features.append(normalize(stats.num_functions, 100))
    scalar_features.append(normalize(stats.num_basic_blocks, 1000))
    scalar_features.append(normalize(stats.num_instructions, 10000))
    scalar_features.append(normalize(stats.num_loops, 50))
    scalar_features.append(normalize(stats.max_loop_depth, 5))
    scalar_features.append(normalize(stats.num_edges / max(stats.num_basic_blocks, 1), 3.0))
    scalar_features.append(normalize(stats.cyclomatic_complexity, 100))
    
    if stats.num_basic_blocks > 0:
        scalar_features.append(normalize(stats.num_instructions / stats.num_basic_blocks, 50))
    else:
        scalar_features.append(0.0)
        
    if stats.num_functions > 0:
        scalar_features.append(normalize(stats.num_calls / stats.num_functions, 20))
    else:
        scalar_features.append(0.0)
        
    if stats.num_instructions > 0:
        scalar_features.append(normalize(stats.num_branches / stats.num_instructions, 0.5))
    else:
        scalar_features.append(0.0)
        
    return np.array(scalar_features, dtype=np.float32)


# LEGACY COMPATIBILITY: For scripts that still call extract_features()
# This returns a flat 128-dim vector by zero-padding the scalar features.
# New code should use extract_ir_graph() + GNNEncoder for the full pipeline.
def extract_features(ir_path: Union[str, Path]) -> np.ndarray:
    """Legacy compatibility wrapper. Returns 128-dim flat vector.
    For new code, use the canonical pipeline: extract_ir_graph() -> GNNEncoder."""
    scalar_vec = extract_scalar_features(ir_path)
    
    # Pad to FEATURE_DIM (no more frozen random GNN projection)
    if len(scalar_vec) > FEATURE_DIM:
        return scalar_vec[:FEATURE_DIM]
    elif len(scalar_vec) < FEATURE_DIM:
        padding = np.zeros(FEATURE_DIM - len(scalar_vec), dtype=np.float32)
        return np.concatenate([scalar_vec, padding])
    return scalar_vec


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit(1)
    features = extract_features(sys.argv[1])
    print(f"[AGENT] Extracted Scalar Features: {features.shape}...")
    print(f"[AGENT] Non-zero elements: {np.sum(features != 0)}...")
