
import re
import networkx as nx
import torch
from torch_geometric.data import Data

class IRGraphExtractor:
    def __init__(self):
        # Basic Regex Patterns for LLVM IR
        self.func_pat = re.compile(r"^define .* @(\w+)\(")
        self.label_pat = re.compile(r"^(\w+):")
        self.instr_pat = re.compile(r"^(?:%(\w+)\s+=\s+)?(\w+)\s+(.*)")
        self.operand_pat = re.compile(r"%(\w+)")
        self.call_target_pat = re.compile(r"call\s+.*@(\w+)")
        
        # Opcode embedding map (simplified for prototype)
        self.opcode_map = {
            "add": 0, "sub": 1, "mul": 2, "udiv": 3, "sdiv": 4,
            "fadd": 5, "fsub": 6, "fmul": 7, "fdiv": 8,
            "rem": 9, "shl": 10, "lshr": 11, "ashr": 12,
            "and": 13, "or": 14, "xor": 15,
            "alloca": 16, "load": 17, "store": 18, "getelementptr": 19,
            "icmp": 20, "fcmp": 21, "phi": 22, "select": 23,
            "call": 24, "ret": 25, "br": 26, "switch": 27,
            "bitcast": 28, "trunc": 29, "zext": 30, "sext": 31,
            "fptoui": 32, "fptosi": 33, "uitofp": 34, "sitofp": 35,
            "ptrtoint": 36, "inttoptr": 37, "invoke": 38
        }
        self.unknown_opcode_idx = 39
        self.block_opcode_idx = 40
        self.func_opcode_idx = 41
        
        # Type features for richer node representation
        self.type_pat = re.compile(r"(i\d+|float|double|half|ptr|void|\[.+\]|<\d+ x .+>)")

    def _extract_type_features(self, operands_str):
        """Extract type information: [is_int, is_float, is_ptr, bitwidth_norm]"""
        is_int = 0.0
        is_float = 0.0
        is_ptr = 0.0
        bitwidth = 0.0
        
        types = self.type_pat.findall(operands_str)
        for t in types:
            if t == 'ptr' or '*' in t:
                is_ptr = 1.0
            elif t in ('float', 'half'):
                is_float = 1.0; bitwidth = 32.0 / 64.0
            elif t == 'double':
                is_float = 1.0; bitwidth = 1.0
            elif t.startswith('i'):
                is_int = 1.0
                try:
                    bw = int(t[1:])
                    bitwidth = min(bw / 64.0, 1.0)
                except ValueError:
                    pass
        
        return [is_int, is_float, is_ptr, bitwidth]

    def parse_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return self.parse_text(lines)

    def parse_text(self, lines):
        G = nx.DiGraph()
        
        current_func = None
        current_block = None
        
        # Tracking Def-Use
        definitions = {}
        pointer_uses = {} # Track which nodes use a specific pointer register
        
        # Tracking Control Flow
        block_starts = {}
        block_ends = {}
        control_edges_to_resolve = []
        
        # Tracking Call Edges (inter-procedural)
        call_edges_to_resolve = []
        
        # Telescopic nodes tracking
        func_nodes = {}    # func_name -> func_node_idx
        block_nodes = {}   # (func_name, block_label) -> block_node_idx
        
        # ENHANCEMENT: Global Context Features
        global_vars = 0
        is_recursive = 0.0
        func_count = 0
        struct_ptr_count = 0
        
        # Node 0 is reserved for global graph node
        node_idx = 1
        
        for line in lines:
            line = line.split(';')[0].strip()
            if not line: continue
            
            # Global Variable Detection
            if line.startswith('@') and ' = ' in line and ('global' in line or 'constant' in line):
                global_vars += 1
                continue

            # Function Header
            m_func = self.func_pat.match(line)
            if m_func:
                current_func = m_func.group(1)
                func_count += 1
                definitions = {}
                pointer_uses = {}
                block_starts = {}
                block_ends = {}
                control_edges_to_resolve = []
                
                func_node_idx = node_idx
                G.add_node(func_node_idx, opcode="FUNCTION", result=current_func, type_feats=[0,0,0,0])
                func_nodes[current_func] = func_node_idx
                node_idx += 1
                continue
                
            if current_func is None: continue
            
            # Basic Block Label
            m_label = self.label_pat.match(line)
            if m_label:
                label = m_label.group(1)
                current_block = label
                
                block_node_idx = node_idx
                G.add_node(block_node_idx, opcode="BLOCK", result=label, type_feats=[0,0,0,0])
                block_nodes[(current_func, label)] = block_node_idx
                
                # Hierarchy Edge: Block -> Function
                G.add_edge(block_node_idx, func_nodes[current_func], type="block_to_func")
                G.add_edge(func_nodes[current_func], block_node_idx, type="func_to_block")
                
                node_idx += 1
                continue
                
            # Instruction
            m_instr = self.instr_pat.match(line)
            if m_instr:
                result_reg = m_instr.group(1)
                opcode = m_instr.group(2)
                operands_str = m_instr.group(3)
                
                # Extract type features for this instruction
                type_feats = self._extract_type_features(operands_str)
                
                # Check for struct pointers
                if "%struct." in operands_str or "{ " in operands_str:
                    struct_ptr_count += 1
                
                # ENHANCEMENT: Memory Pattern Hint
                # If GEP has more than 2 operands, it's likely a multi-dimensional or struct access
                if opcode == "getelementptr":
                    num_ops = len(operands_str.split(','))
                    if num_ops > 2:
                        type_feats[3] = -abs(type_feats[3]) # Signal complexity via negative bitwidth
                
                G.add_node(node_idx, opcode=opcode, result=result_reg, type_feats=type_feats)
                
                G.add_node(node_idx, opcode=opcode, result=result_reg, type_feats=type_feats)
                
                # Hierarchy Edge: Instruction -> Block
                if current_block and (current_func, current_block) in block_nodes:
                    b_idx = block_nodes[(current_func, current_block)]
                    G.add_edge(node_idx, b_idx, type="instr_to_block")
                    G.add_edge(b_idx, node_idx, type="block_to_instr")
                
                # Register Block Start/End
                if current_block:
                    if current_block not in block_starts:
                        block_starts[current_block] = node_idx
                    block_ends[current_block] = node_idx
                    
                    if node_idx > 0 and (node_idx - 1) == block_ends.get(current_block, -2):
                         G.add_edge(node_idx - 1, node_idx, type="control_next")
                
                # Register Definition
                if result_reg:
                    definitions[result_reg] = node_idx
                
                # MEMORY VISION: Overload Data Flow Edges
                # If this is a memory instruction, link it to previous users of the same pointer
                if opcode in ("load", "store", "getelementptr", "atomicrmw", "cmpxchg"):
                    ptr_matches = self.operand_pat.findall(operands_str)
                    if ptr_matches:
                        ptr_name = ptr_matches[-1] # Heuristic: pointer is usually the last reg
                        if ptr_name in pointer_uses:
                            for prev_node in pointer_uses[ptr_name][-3:]: # Link to last 3 uses to avoid density explosion
                                G.add_edge(prev_node, node_idx, type="data_flow")
                        
                        if ptr_name not in pointer_uses: pointer_uses[ptr_name] = []
                        pointer_uses[ptr_name].append(node_idx)

                # Find Uses (Data Flow Edges)
                for op_match in self.operand_pat.finditer(operands_str):
                    op_name = op_match.group(1)
                    if op_name in definitions:
                        def_node = definitions[op_name]
                        G.add_edge(def_node, node_idx, type="data_flow")
                        
                # Identify Control Flow (Branch targets)
                if opcode == "br":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets:
                        control_edges_to_resolve.append((node_idx, target))
                        
                # Switch targets
                elif opcode == "switch":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets:
                        control_edges_to_resolve.append((node_idx, target))
                        
                # Invoke targets (exception handling)
                elif opcode == "invoke":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets:
                        control_edges_to_resolve.append((node_idx, target))
                
                # Call edges (inter-procedural)
                if opcode in ("call", "invoke"):
                    m_call = self.call_target_pat.search(line)
                    if m_call:
                        callee = m_call.group(1)
                        # Check for direct recursion
                        if callee == current_func:
                            is_recursive = 1.0
                        call_edges_to_resolve.append((node_idx, callee))
                        
                node_idx += 1
                
        # Resolve Control Flow Edges
        for src_node, target_label in control_edges_to_resolve:
            if target_label in block_starts:
                target_node = block_starts[target_label]
                G.add_edge(src_node, target_node, type="control_branch")
                
        # Resolve Call Edges (inter-procedural)
        for src_node, callee_name in call_edges_to_resolve:
            if callee_name in func_nodes:
                target_node = func_nodes[callee_name]
                G.add_edge(src_node, target_node, type="call")

        # Attach Global Module Features to the Graph Object
        G.graph['module_feats'] = [
            min(global_vars / 20.0, 1.0),
            is_recursive,
            min(func_count / 10.0, 1.0),
            min(struct_ptr_count / max(node_idx, 1), 1.0)
        ]

        return G

    def to_pyg_data(self, G, focus_function=None):
        # Convert NetworkX to PyG Data
        
        # Determine subset of nodes if focus_function is provided
        if focus_function and focus_function in [G.nodes[n].get('result') for n in G.nodes if G.nodes[n].get('opcode') == "FUNCTION"]:
            # Find the function node
            f_node = [n for n in G.nodes if G.nodes[n].get('opcode') == "FUNCTION" and G.nodes[n].get('result') == focus_function][0]
            # Get blocks
            b_nodes = [v for u, v, d in G.edges(data=True) if u == f_node and d.get('type') == 'func_to_block']
            # Get instructions
            i_nodes = []
            for b in b_nodes:
                i_nodes.extend([v for u, v, d in G.edges(data=True) if u == b and d.get('type') == 'block_to_instr'])
            
            relevant_nodes = set([f_node] + b_nodes + i_nodes)
        else:
            relevant_nodes = set(G.nodes())

        num_extracted_nodes = len(relevant_nodes)
        num_total_nodes = num_extracted_nodes + 1  # +1 for Global node
        
        # Feature dim: one-hot opcode (42) + type features (4) = 46
        opcode_dim = 42
        type_dim = 4
        feature_dim = opcode_dim + type_dim
        
        if num_extracted_nodes == 0:
            return Data(x=torch.zeros(1, feature_dim), edge_index=torch.zeros(2, 0, dtype=torch.long))

        # Node Features: One-Hot Opcode + Type Features
        x = []
        # GLOBAL NODE (Node 0): Inject Module Features here
        # We use the first 4 slots which are normally for opcodes (Node 0 has no opcode)
        global_feat = [0] * feature_dim
        module_feats = G.graph.get('module_feats', [0, 0, 0, 0])
        for i in range(len(module_feats)):
            global_feat[i] = float(module_feats[i])
        x.append(global_feat)
        
        sorted_nodes = sorted(list(relevant_nodes))
        node_map = {n: i + 1 for i, n in enumerate(sorted_nodes)}
        
        for n in sorted_nodes:
            opcode = G.nodes[n].get('opcode', 'unknown')
            if opcode == "FUNCTION":
                idx = self.func_opcode_idx
            elif opcode == "BLOCK":
                idx = self.block_opcode_idx
            else:
                idx = self.opcode_map.get(opcode, self.unknown_opcode_idx)
                
            feat = [0] * opcode_dim
            feat[idx] = 1
            
            # Append type features
            type_feats = G.nodes[n].get('type_feats', [0, 0, 0, 0])
            feat.extend(type_feats)
            
            x.append(feat)
            
        x = torch.tensor(x, dtype=torch.float)
        
        # Edges
        edge_indices = []
        edge_types = []
        
        # Edge types mapping for Telescopic Hierarchy
        etype_map = {
            'control_next': 0,
            'control_branch': 1,
            'data_flow': 2,
            'call': 5,
            'instr_to_block': 6,
            'block_to_instr': 7,
            'block_to_func': 8,
            'func_to_block': 9
        }
        
        for u, v, data in G.edges(data=True):
            if u in node_map and v in node_map:
                src = node_map[u]
                dst = node_map[v]
                edge_indices.append([src, dst])
                edge_type_str = data.get('type', 'control_next')
                etype = etype_map.get(edge_type_str, 0)
                edge_types.append(etype)
            
        # Telescopic Global Edges (Node 0 connects ONLY to Function nodes)
        # Type 3: Global-to-Func, Type 4: Func-to-Global
        for n in sorted_nodes:
            if G.nodes[n].get('opcode') == "FUNCTION":
                f_idx = node_map[n]
                edge_indices.append([0, f_idx])
                edge_types.append(3)
                edge_indices.append([f_idx, 0])
                edge_types.append(4)
            
        if len(edge_indices) == 0:
            edge_index = torch.zeros(2, 0, dtype=torch.long)
            edge_attr = torch.zeros(0, dtype=torch.long)
        else:
            edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
            edge_attr = torch.tensor(edge_types, dtype=torch.long)
             
        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
        return data

# Singleton
extractor = IRGraphExtractor()

def extract_ir_graph(file_path, focus_function=None):
    G = extractor.parse_file(file_path)
    data = extractor.to_pyg_data(G, focus_function=focus_function)
    return data
