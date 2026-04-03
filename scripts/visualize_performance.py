
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

def visualize_performance(dataset_path: str, output_image: str = "performance_comparison.png", no_show: bool = False):
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, 'r') as f:
        data = json.load(f)
        
    o3_reductions = []
    o2_reductions = []
    o1_reductions = []
    custom_reductions = []
    
    print(f"Analyzing {len(data)} entries...")
    
    for entry in data:
        metrics = entry.get("metrics", {})
        red = metrics.get("inst_reduction", 0) * 100
        
        passes = entry.get("passes", [])
        passes_str = " ".join(passes)
        
        if "default<O3>" in passes_str:
            o3_reductions.append(red)
        elif "default<O2>" in passes_str:
            o2_reductions.append(red)
        elif "default<O1>" in passes_str:
            o1_reductions.append(red)
        else:
            custom_reductions.append(red)
            

    o3_avg = np.mean(o3_reductions) if o3_reductions else 0
    custom_avg = np.mean(custom_reductions) if custom_reductions else 0
    custom_max = np.max(custom_reductions) if custom_reductions else 0
    o3_val_for_comparison = o3_avg
    
    print(f"Found {len(o3_reductions)} O3 samples (Avg: {o3_avg:.2f}%)")
    print(f"Found {len(custom_reductions)} Custom samples (Avg: {custom_avg:.2f}%, Max: {custom_max:.2f}%)")
    

    plt.figure(figsize=(10, 6), dpi=120)
    
    labels = ['-O3 (Baseline)', 'Avg Random Seq', 'Top 10% Custom', 'Best Sequence']
    

    if custom_reductions:
        top_10_avg = np.mean(sorted(custom_reductions)[-int(len(custom_reductions)*0.1):])
    else:
        top_10_avg = 0
        
    values = [o3_avg, custom_avg, top_10_avg, custom_max]
    

    colors = [
        '#A3E4D7', 
        '#48C9B0', 
        '#1ABC9C',  
        '#148F77'
    ]
    
    bars = plt.bar(labels, values, color=colors, width=0.6, edgecolor='none')
    

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.tick_params(axis='x', colors='#34495E')
    ax.tick_params(axis='y', colors='#34495E')
    
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", 
                 ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2C3E50')
        
    plt.ylabel("Instruction Reduction (%)", fontsize=11, labelpad=10, color='#34495E')
    plt.title("Optimization Performance: Standard Compiler vs Discovery", 
              fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
    plt.grid(axis='y', alpha=0.2, linestyle='--', color='#BDC3C7')
    plt.ylim(0, max(values) * 1.25)
    
    plt.hlines(o3_avg, -0.4, 3.8, colors='#7F8C8D', linestyles=':', lw=1.5, alpha=0.6)
    plt.text(-0.5, o3_avg, "Baseline", va='center', ha='right', fontsize=9, color='#7F8C8D')
    
    plt.hlines(custom_max, 2.6, 3.8, colors='#148F77', linestyles=':', lw=1.5, alpha=0.6)
    
    improvement = custom_max - o3_avg
    if improvement > 0:
        plt.annotate('', xy=(3.5, custom_max), xytext=(3.5, o3_avg),
                     arrowprops=dict(arrowstyle='<->', color='#27AE60', lw=1.5))
        
        mid_y = (custom_max + o3_avg) / 2
        plt.text(3.6, mid_y, f"+{improvement:.1f}%\nGain", 
                 va='center', ha='left', fontsize=11, fontweight='bold', color='#27AE60')

    plt.figtext(0.5, 0.01, "Source: 378 random benchmark evaluations on Linear Algebra kernels.", 
                ha="center", fontsize=9, color='#7F8C8D', style='italic')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15, right=0.85)
    plt.savefig(output_image, dpi=120)
    print(f"Saved comparison chart to {output_image}")
    
    if not no_show:
        try:
            plt.show()
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize Performance Comparison")
    parser.add_argument("--input", type=str, default="dataset/optimization_dataset.json")
    parser.add_argument("--output", type=str, default="performance_comparison.png")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    
    visualize_performance(args.input, args.output, args.no_show)
