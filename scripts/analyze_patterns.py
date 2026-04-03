
import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import BENCHMARKS_DIR, POLYBENCH_CATEGORIES

DATASET_FILE = Path(__file__).parent.parent / "dataset" / "optimization_dataset.json"

def load_dataset(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} entries from {filepath}")
    return data

def analyze_domain_patterns(data):
    """Analyze which passes are most effective per domain"""
    df = pd.DataFrame(data)
    
    # Filter out errors
    if 'error' in df.columns:
        df = df[df['error'].isna() | (df['error'] == "")]
        
    # Expand metrics
    df['inst_reduction'] = df['metrics'].apply(lambda x: x.get('inst_reduction', 0))
    df['size_reduction'] = df['metrics'].apply(lambda x: x.get('size_reduction', 0))
    df['compile_time'] = df['metrics'].apply(lambda x: x.get('compile_time', 0))
    
    print("\n=== Domain-Specific Analysis ===")
    
    domain_stats = {}
    
    for domain in df['category'].unique():
        domain_df = df[df['category'] == domain]
        
        # Get top 5 sequences by instruction reduction
        top_seqs = domain_df.nlargest(5, 'inst_reduction')
        
        # Count pass frequency in top 10% of sequences
        top_10_percent = domain_df.nlargest(int(len(domain_df) * 0.1), 'inst_reduction')
        pass_counts = Counter()
        for passes in top_10_percent['passes']:
            pass_counts.update(passes)
            
        total_passes = sum(pass_counts.values())
        pass_freq = {k: v/total_passes for k,v in pass_counts.most_common(5)}
        
        domain_stats[domain] = {
            'best_reduction': top_seqs.iloc[0]['inst_reduction'],
            'avg_reduction': domain_df['inst_reduction'].mean(),
            'top_passes': pass_freq,
            'best_seq': top_seqs.iloc[0]['passes']
        }
        
        print(f"\n[{domain.upper()}]")
        print(f"  Best Inst Reduction: {domain_stats[domain]['best_reduction']:.2%}")
        print(f"  Avg  Inst Reduction: {domain_stats[domain]['avg_reduction']:.2%}")
        print(f"  Top Passes: {', '.join([f'{k}({v:.1%})' for k,v in pass_freq.items()])}")
        print(f"  Best Sequence (len {len(domain_stats[domain]['best_seq'])}): {domain_stats[domain]['best_seq']}")

    return domain_stats

def find_common_subsequences(data, min_len=2, max_len=4):
    """Find common N-grams in high-performing sequences (Macro-Action candidates)"""
    df = pd.DataFrame(data)
    if 'error' in df.columns:
        df = df[df['error'].isna()]
        
    # Filter high performers (> 10% reduction)
    high_perf = df[df['metrics'].apply(lambda x: x.get('inst_reduction', 0) > 0.1)]
    
    ngrams = Counter()
    
    for passes in high_perf['passes']:
        clean_passes = [p for p in passes if not p.startswith('default<')] # Skip standard levels
        if len(clean_passes) < min_len:
            continue
            
        for n in range(min_len, max_len + 1):
            for i in range(len(clean_passes) - n + 1):
                gram = tuple(clean_passes[i:i+n])
                ngrams[gram] += 1
                
    print("\n=== Macro-Action Candidates (Common Subsequences) ===")
    for gram, count in ngrams.most_common(10):
        print(f"  {count}x: {' -> '.join(gram)}")
        
    return ngrams

def main():
    parser = argparse.ArgumentParser(description="Analyze optimization dataset")
    parser.add_argument("--input", type=str, default="dataset/optimization_dataset.json", help="Input JSON file path")
    args = parser.parse_args()
    
    dataset_file = Path(args.input)
    if not dataset_file.exists():
        print(f"Dataset not found at {dataset_file}")
        return
        
    data = load_dataset(dataset_file)
    analyze_domain_patterns(data)
    find_common_subsequences(data)

if __name__ == "__main__":
    main()
