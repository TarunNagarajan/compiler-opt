import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import PROJECT_ROOT

DATASET_FILE = PROJECT_ROOT / "dataset" / "optimization_dataset.json"

def clean_pass_name(pass_name: str) -> str:
    if pass_name.startswith("function("):
        inner = pass_name[9:-1]
        if "<" in inner:
            inner = inner.split("<")[0]
        return inner
    if "<" in pass_name:
        return pass_name.split("<")[0]
    return pass_name

def discover_macro_actions(dataset_path: Path, top_k: int = 10, min_len: int = 2, max_len: int = 4):
    print(f"Loading dataset from {dataset_path}...")
    try:
        with open(dataset_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    print(f"Analyzing {len(data)} sequences...")
    
    valid_data = [d for d in data if 'error' not in d and 'metrics' in d]
    
    good_seqs = [
        entry for entry in valid_data 
        if entry['metrics'].get('inst_reduction', 0) > 0.05
    ]
    
    print(f"Found {len(good_seqs)} high-performing sequences (>5% reduction).")
    
    ngrams = Counter()
    ngram_improvement = defaultdict(list)
    
    for entry in good_seqs:
        raw_passes = entry['passes']
        if len(raw_passes) == 1 and raw_passes[0].startswith("default"):
            continue
            
        clean_passes = [p for p in raw_passes if not p.startswith('default')]
        
        reduction = entry['metrics']['inst_reduction']
        
        for n in range(min_len, max_len + 1):
            for i in range(len(clean_passes) - n + 1):
                gram = tuple(clean_passes[i:i+n])
                ngrams[gram] += 1
                ngram_improvement[gram].append(reduction)
                
    scored_ngrams = []
    for gram, count in ngrams.items():
        avg_imp = np.mean(ngram_improvement[gram])
        score = count * avg_imp
        scored_ngrams.append({
            'sequence': list(gram),
            'score': score,
            'count': count,
            'avg_improvement': avg_imp,
            'len': len(gram)
        })
        
    scored_ngrams.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n=== Top Discovered Macro-Actions ===")
    
    top_actions = []
    
    for item in scored_ngrams:
        if len(top_actions) >= top_k:
            break
            
        cur_seq = item['sequence']
        is_redundant = False
        
        for selected in top_actions:
            sel_seq = selected['sequence']
            
            # Check if current is subset of selected OR selected is subset of current
            # Using strings for simple sequence-in-sequence checking
            str_cur = " ".join(cur_seq)
            str_sel = " ".join(sel_seq)
            
            if str_cur in str_sel or str_sel in str_cur:
                is_redundant = True
                break
        
        if is_redundant:
            continue
            
        top_actions.append(item)
        print(f"Action {len(top_actions)}: {item['count']}x (Avg Imp: {item['avg_improvement']:.1%}) | Score: {item['score']:.1f}")
        print(f"  Sequence: {' -> '.join(item['sequence'])}")
        
    return top_actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover macro-actions from dataset")
    parser.add_argument("--input", type=str, default=str(DATASET_FILE), help="Path to input dataset JSON")
    parser.add_argument("--top-k", type=int, default=15, help="Number of macro-actions to discover")
    args = parser.parse_args()
    
    discover_macro_actions(Path(args.input), top_k=args.top_k)
