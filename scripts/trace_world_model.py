import sys
import torch
from pathlib import Path
from torch_geometric.data import Batch

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.world_model_v5 import WorldModelV5
from src.features.ir_graph_extractor import extract_ir_graph
from src.config import FEATURE_DIM, NUM_ACTIONS
from src.env import CompilerOptEnv

def trace_model():
    print("=== TRACING WORLD MODEL V5 ===")
    
    # Instantiate the model with the exact parameters it will use during training
    model = WorldModelV5(
        state_dim=FEATURE_DIM,
        action_dim=NUM_ACTIONS,
        gnn_layers=6,
        gnn_input_dim=46,      # NEW Telescopic graph features
        num_relations=10       # NEW Telescopic relations
    )
    print(f"[OK] Model Instantiated.")
    print(f"     gnn_encoder.input_proj: {model.gnn_encoder.input_proj}")
    print(f"     gnn_encoder.output_proj: {model.gnn_encoder.output_proj}")
    
    test_file = Path("test_ood.c").resolve()
    
    # Compile the file to LLVM IR to get a real graph
    print(f"\n[INFO] Extracting IR Graph from {test_file.name}...")
    env = CompilerOptEnv([test_file], max_steps=1)
    obs, info = env.reset(options={"ir_path": str(test_file)})
    graph1 = env.get_observation_graph()
    obs, info = env.reset(options={"ir_path": str(test_file)})
    graph2 = env.get_observation_graph()
    
    print(f"[OK] Graph extracted.")
    print(f"     Node shape: {graph1.x.shape}")
    print(f"     Edge index shape: {graph1.edge_index.shape}")
    print(f"     Edge attr shape: {graph1.edge_attr.shape}")
    
    # Test 1: Unbatched Forward Pass
    print("\n--- Test 1: Unbatched Forward Pass (MCTS Inference style) ---")
    action_onehot = torch.zeros(1, NUM_ACTIONS)
    action_onehot[0, 5] = 1.0 # arbitrary action
    try:
        next_state, metrics = model(None, action_onehot, graph_data=graph1)
        print(f"[SUCCESS] Unbatched Pass!")
        print(f"          Next State Shape: {next_state.shape}  (Expected: [1, {FEATURE_DIM}])")
        print(f"          Metrics Shape:    {metrics.shape}     (Expected: [1, 6])")
    except Exception as e:
        print(f"[FAILED] Unbatched Pass crashed:")
        import traceback
        traceback.print_exc()
        return

    # Test 2: Batched Forward Pass
    print("\n--- Test 2: Batched Forward Pass (Training style) ---")
    batch_graph = Batch.from_data_list([graph1, graph2])
    action_onehot_batch = torch.zeros(2, NUM_ACTIONS)
    action_onehot_batch[:, 5] = 1.0
    try:
        next_state, metrics = model(None, action_onehot_batch, graph_data=batch_graph)
        print(f"[SUCCESS] Batched Pass!")
        print(f"          Next State Shape: {next_state.shape}  (Expected: [2, {FEATURE_DIM}])")
        print(f"          Metrics Shape:    {metrics.shape}     (Expected: [2, 6])")
    except Exception as e:
        print(f"[FAILED] Batched Pass crashed:")
        import traceback
        traceback.print_exc()
        return

    print("\n=== ALL TRACE TESTS PASSED! ===")

if __name__ == "__main__":
    trace_model()
