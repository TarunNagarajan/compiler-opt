import os
from pathlib import Path

def show_config():
    print("===============================================================================")
    print("   HRL COMPILER OPTIMIZER: NEURAL NETWORK CONFIGURATION")
    print("===============================================================================")
    print("\n--- NEURAL NETWORK ARCHITECTURES ---")
    print("1. State Encoder: 4-Layer Heterogeneous GNN (GraphSAGE/GAT Conv)")
    print("   - Node Features: 44 dimensions (Instruction + Type)")
    print("   - Latent Representation: 128-dimensional program embedding")
    
    print("\n2. Manager (Macro-Policy): Multi-Head Multi-Agent MLP")
    print("   - Input: 128-dim embedding")
    print("   - Output: 18 Discrete Macro-Actions (Experts Sequences)")
    
    print("\n3. Worker (Micro-Policy): Contextual Refiner")
    print("   - Action Space: 20 Discrete Refinements (Tune/Inject)")
    
    print("\n4. World Model: Graph-to-Graph Transition Predictor")
    print("   - Hidden Dim: 256 | Action Embedding: 64")
    print("===============================================================================")

if __name__ == "__main__":
    show_config()
