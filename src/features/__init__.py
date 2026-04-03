from .ir_parser import IRParser
from .feature_vector import extract_features, extract_scalar_features
from .ir_graph_extractor import extract_ir_graph as extract_ir_graph_v4
from .ir_graph_extractor_v5 import extract_ir_graph_v5 as extract_ir_graph
from .graph_encoder import GNNEncoder, create_default_encoder

# CANONICAL PIPELINE (use this for all new code):
#   1. extract_ir_graph(ir_path) -> PyG Data object
#   2. create_default_encoder() -> GNNEncoder
#   3. encoder(data.x, data.edge_index, data.batch, edge_type=data.edge_attr) -> [1, 128] embedding
#
# The extract_features() function is a LEGACY compatibility wrapper that returns
# a flat 128-dim vector of scalar features (no GNN). Use only for backward compat.
