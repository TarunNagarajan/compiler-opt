
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from pathlib import Path

def find_elbow(dataset_path: str, max_k: int = 50, output_image: str = "elbow_plot.png"):
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, 'r') as f:
        data = json.load(f)
        
    sequences = [" ".join(entry['passes']) for entry in data if 'passes' in entry]
    
    print(f"Vectorizing {len(sequences)} sequences...")
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(sequences).toarray()
    
    inertias = []
    ks = range(5, max_k + 1, 5)
    
    print(f"Calculating inertia for K in {list(ks)}...")
    for k in ks:
        print(f"  Testing K={k}...")
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        
    plt.figure(figsize=(10, 6))
    plt.plot(ks, inertias, 'bo-')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia (Sum of Squared Distances)')
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    
    plt.savefig(output_image)
    print(f"Saved elbow plot to {output_image}")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find optimal K using the Elbow Method")
    parser.add_argument("--input", type=str, default="dataset/optimization_dataset.json", help="Input dataset")
    parser.add_argument("--max_k", type=int, default=50, help="Maximum K to test")
    parser.add_argument("--output", type=str, default="elbow_plot.png", help="Output plot filename")
    
    args = parser.parse_args()
    
    dataset_file = Path(args.input)
    if not dataset_file.exists():
        print(f"Error: {dataset_file} not found.")
    else:
        find_elbow(str(dataset_file), args.max_k, args.output)
