import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from pathlib import Path

def visualize_clusters(dataset_path: str, k: int = 5, output_image: str = "cluster_diagram.png"):
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, 'r') as f:
        data = json.load(f)
        
    sequences = []
    labels = []
    
    print(f"Processing {len(data)} entries...")
    for entry in data:
        seq_str = " ".join(entry['passes'])
        sequences.append(seq_str)
        labels.append(entry.get('category', 'unknown'))
        
    print("Vectorizing sequences...")
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(sequences).toarray()
    
    print(f"Running K-Means (K={k})...")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    
    print("Projecting to 2D with PCA...")
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X)
    
    print(f"Generating plot: {output_image}...")
    plt.figure(figsize=(14, 8))
    
    plt.subplots_adjust(right=0.7)
    
    scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=clusters, cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Cluster ID')
    
    centers_2d = pca.transform(kmeans.cluster_centers_)
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], c='red', s=200, marker='X', label='Centroids')
    
    plt.title(f"K-Means Clustering of Optimization Sequences (K={k})")
    plt.xlabel("PC1: Granularity (Custom Passes vs Standard Levels)")
    plt.ylabel("PC2: Optimization Type (Logic vs Loop Opts)")
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    cluster_metrics = {i: {'reductions': [], 'categories': []} for i in range(k)}
    
    for i, entry in enumerate(data):
        cid = clusters[i]
        
        reduction = entry.get('metrics', {}).get('inst_reduction', 0) * 100
        category = entry.get('category', 'unknown')
        
        cluster_metrics[cid]['reductions'].append(reduction)
        cluster_metrics[cid]['categories'].append(category)
    
    analysis_text = "Cluster Analysis:\n"
    for i in range(k):
        top_terms = [terms[ind] for ind in order_centroids[i, :3]]
        
        reductions = cluster_metrics[i]['reductions']
        categories = cluster_metrics[i]['categories']
        avg_red = np.mean(reductions) if reductions else 0
        
        if categories:
            from collections import Counter
            dom_cat, dom_count = Counter(categories).most_common(1)[0]
            dom_pct = (dom_count / len(categories)) * 100
            cat_str = f"{dom_cat} ({dom_pct:.0f}%)"
        else:
            cat_str = "N/A"
            
        count = len(reductions)
        analysis_text += f"\nCluster {i} (n={count}, Avg Red: {avg_red:.1f}%):\n  {', '.join(top_terms)}\n  Dom: {cat_str}"
        
    print(f"\n{analysis_text}")
    
    print("\n=== PCA Component Interpretation ===")
    components = pca.components_
    feature_names = vectorizer.get_feature_names_out()
    
    pca_text = ""
    for i in range(2):
        print(f"\nPC{i+1} Top Features (Loadings):")
        indices = np.argsort(np.abs(components[i]))[::-1][:5]
        term_list = []
        for idx in indices:
            weight = components[i][idx]
            name = feature_names[idx]
            sign = "+" if weight > 0 else "-"
            print(f"  {name}: {weight:.4f}")
            term_list.append(f"{sign}{name}")
        pca_text += f"PC{i+1}: {', '.join(term_list)}\n"

    plt.figtext(0.72, 0.85, analysis_text, fontsize=10, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.savefig(output_image)
    print(f"Saved visualization to {output_image}")
    
    if not args.no_show:
        try:
            plt.show()
        except Exception as e:
            print(f"Warning: Could not display plot (headless env?): {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize optimization sequence clusters")
    parser.add_argument("--input", type=str, default="dataset/optimization_dataset.json", help="Input dataset")
    parser.add_argument("--k", type=int, default=5, help="Number of clusters")
    parser.add_argument("--output", type=str, default="clustering_plot.png", help="Output image file")
    parser.add_argument("--no-show", action="store_true", help="Do not display the plot window")
    
    args = parser.parse_args()
    
    dataset_file = Path(args.input)
    if not dataset_file.exists():
        print(f"Error: {dataset_file} not found. Run dataset generation first.")
    else:
        visualize_clusters(str(dataset_file), args.k, args.output)
