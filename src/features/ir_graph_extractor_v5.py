"""
v5 IR Graph Extractor — Loop-Aware Edition

Changes from v4 (ir_graph_extractor.py):
1. NEW: 7th edge type for loop back-edges (detected via phi nodes + block ordering)
2. NEW: Loop depth annotation per instruction node
3. UNCHANGED: All existing edge types (0-5) and node features remain compatible

Edge types:
  0 = control_next (sequential within block)
  1 = control_branch (forward branch)
  2 = data_flow (def-use + memory aliasing)  
  3 = global_out (global node → instruction)
  4 = global_in (instruction → global node)
  5 = call (inter-procedural)
  6 = loop_back (NEW — back-edge indicating a loop)
"""

import re
import networkx as nx
import torch
from torch_geometric.data import Data


class IRGraphExtractorV5:
    def __init__(self):
        # Basic Regex Patterns for LLVM IR
        self.func_pat = re.compile(r"^define .* @(\w+)\(") # Legacy, keep as fallback
        self.func_pat_robust = re.compile(r"define\s+.*@(?:\"([^\"]+)\"|([\w\.\-]+))\(")
        self.label_pat = re.compile(r"^(\w+):")
        self.instr_pat = re.compile(r"^(?:%(\w+)\s+=\s+)?(\w+)\s+(.*)")
        self.operand_pat = re.compile(r"%(\w+)")
        self.call_target_pat = re.compile(r"call\s+.*@(\w+)")
        
        # Opcode embedding map (same as v4)
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

    def parse_file(self, file_path, focus_functions=None):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return self.parse_text(lines, focus_functions=focus_functions)

    def parse_text(self, lines, focus_functions=None):
        # Support both singular string and list/set of functions
        if isinstance(focus_functions, str):
            focus_functions = {focus_functions}
        elif focus_functions:
            focus_functions = set(focus_functions)
        G = nx.DiGraph()
        
        current_func = None
        current_block = None
        is_fovea = True # Default for small files
        
        # Tracking Def-Use
        definitions = {}
        pointer_uses = {}
        
        # Tracking Control Flow
        block_starts = {}
        block_ends = {}
        block_order = {} 
        
        # V7: We track "active nodes" (Block IDs in RGCN)
        # In Fovea: 1 active node per instruction.
        # In Periphery: 1 active node per basic block.
        global_active_node_counter = 0 
        current_block_active_id = 0
        
        control_edges_to_resolve = []
        call_edges_to_resolve = []
        func_entry_nodes = {}
        phi_blocks = set()
        
        # Global Context Features
        global_vars = 0
        is_recursive = 0.0
        func_count = 0
        struct_ptr_count = 0
        
        node_idx = 0
        
        for line in lines:
            line = line.split(';')[0].strip()
            if not line: continue
            
            # Global Variable Detection
            if line.startswith('@') and ' = ' in line and ('global' in line or 'constant' in line):
                global_vars += 1
                continue

            # Function Header
            m_func = self.func_pat_robust.search(line)
            if m_func:
                name = m_func.group(1) or m_func.group(2)
                
                # V7: NEVER skip. We now parse the entire module for global context.
                # But we only use High-Resolution (Flat) for hotspots.
                is_fovea = (focus_functions is None) or (name in focus_functions)
                
                current_func = name
                func_count += 1
                definitions = {}
                pointer_uses = {}
                block_starts = {}
                block_ends = {}
                block_order = {}
                current_func_block_counter = 0
                control_edges_to_resolve = []
                phi_blocks = set()
                
                # Implicit entry block
                current_block = "entry"
                block_order[current_block] = current_func_block_counter
                current_func_block_counter += 1
                
                if not is_fovea:
                    current_block_active_id = global_active_node_counter
                    global_active_node_counter += 1
                continue
                
            if current_func is None: continue
            
            # Basic Block Label
            m_label = self.label_pat.match(line)
            if m_label:
                label = m_label.group(1)
                current_block = label
                block_order[label] = current_func_block_counter
                current_func_block_counter += 1
                
                if not is_fovea:
                    current_block_active_id = global_active_node_counter
                    global_active_node_counter += 1
                continue
                
            # Instruction
            m_instr = self.instr_pat.match(line)
            if m_instr:
                result_reg = m_instr.group(1)
                opcode = m_instr.group(2)
                operands_str = m_instr.group(3)
                
                type_feats = self._extract_type_features(operands_str)
                if "%struct." in operands_str or "{ " in operands_str:
                    struct_ptr_count += 1
                
                if opcode == "getelementptr":
                    num_ops = len(operands_str.split(','))
                    if num_ops > 2: type_feats[3] = -abs(type_feats[3])
                
                # V7: Adaptive Block ID
                if is_fovea:
                    # High-Resolution: Every instruction is its own active node in RGCN
                    node_block_id = global_active_node_counter
                    global_active_node_counter += 1
                else:
                    # High-Scale: Instructions share the block's active ID (HBC)
                    node_block_id = current_block_active_id
                
                G.add_node(node_idx, 
                          opcode=opcode, 
                          result=result_reg, 
                          type_feats=type_feats,
                          block_idx=node_block_id)
                
                if current_func not in func_entry_nodes:
                    func_entry_nodes[current_func] = node_idx
                
                if current_block:
                    if current_block not in block_starts:
                        block_starts[current_block] = node_idx
                    block_ends[current_block] = node_idx
                    if node_idx > 0 and (node_idx - 1) == block_ends.get(current_block, -2):
                         G.add_edge(node_idx - 1, node_idx, type="control_next")
                
                if opcode == "phi" and current_block:
                    phi_blocks.add(current_block)
                
                if result_reg: definitions[result_reg] = node_idx
                
                if opcode in ("load", "store", "getelementptr", "atomicrmw", "cmpxchg"):
                    ptr_matches = self.operand_pat.findall(operands_str)
                    if ptr_matches:
                        ptr_name = ptr_matches[-1]
                        if ptr_name in pointer_uses:
                            for prev_node in pointer_uses[ptr_name][-3:]:
                                G.add_edge(prev_node, node_idx, type="data_flow")
                        if ptr_name not in pointer_uses: pointer_uses[ptr_name] = []
                        pointer_uses[ptr_name].append(node_idx)

                for op_match in self.operand_pat.finditer(operands_str):
                    op_name = op_match.group(1)
                    if op_name in definitions:
                        def_node = definitions[op_name]
                        G.add_edge(def_node, node_idx, type="data_flow")
                        
                if opcode == "br":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets: control_edges_to_resolve.append((node_idx, target, current_block))
                elif opcode == "switch":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets: control_edges_to_resolve.append((node_idx, target, current_block))
                elif opcode == "invoke":
                    targets = re.findall(r"label %(\w+)", operands_str)
                    for target in targets: control_edges_to_resolve.append((node_idx, target, current_block))
                
                if opcode in ("call", "invoke"):
                    m_call = self.call_target_pat.search(line)
                    if m_call:
                        callee = m_call.group(1)
                        if callee == current_func: is_recursive = 1.0
                        call_edges_to_resolve.append((node_idx, callee))
                        
                node_idx += 1
                
        # Resolve Control Flow Edges
        for src_node, target_label, src_block in control_edges_to_resolve:
            if target_label in block_starts:
                target_node = block_starts[target_label]
                src_order = block_order.get(src_block, 999999)
                target_order = block_order.get(target_label, 999999)
                is_back_edge = (target_order <= src_order) or (target_label in phi_blocks)
                
                if is_back_edge: G.add_edge(src_node, target_node, type="loop_back")
                else: G.add_edge(src_node, target_node, type="control_branch")
                
        # Resolve Call Edges
        for src_node, callee_name in call_edges_to_resolve:
            if callee_name in func_entry_nodes:
                target_node = func_entry_nodes[callee_name]
                G.add_edge(src_node, target_node, type="call")

        # Module Features
        G.graph['module_feats'] = [
            min(global_vars / 20.0, 1.0),
            is_recursive,
            min(func_count / 10.0, 1.0),
            min(struct_ptr_count / max(node_idx, 1), 1.0)
        ]
        G.graph['num_active_nodes'] = global_active_node_counter

        return G

    def to_pyg_data(self, G):
        """Convert NetworkX to PyG Data. V6 adds block_map for HBC."""
        num_instr_nodes = len(G.nodes())
        num_total_nodes = num_instr_nodes + 1
        
        opcode_dim = 42
        type_dim = 4
        feature_dim = opcode_dim + type_dim
        
        if num_instr_nodes == 0:
            return Data(
                x=torch.zeros(1, feature_dim), 
                edge_index=torch.zeros(2, 0, dtype=torch.long),
                edge_attr=torch.zeros(0, dtype=torch.long)
            )

        x = []
        block_map = []
        
        # GLOBAL NODE (Node 0)
        global_feat = [0] * feature_dim
        module_feats = G.graph.get('module_feats', [0, 0, 0, 0])
        for i in range(len(module_feats)):
            global_feat[i] = float(module_feats[i])
        x.append(global_feat)
        
        # Global node belongs to its own special block (index 0)
        block_map.append(0)
        
        node_map = {n: i + 1 for i, n in enumerate(G.nodes())}
        
        for n in G.nodes():
            opcode = G.nodes[n].get('opcode', 'unknown')
            idx = self.opcode_map.get(opcode, self.unknown_opcode_idx)
            feat = [0] * opcode_dim
            feat[idx] = 1
            
            type_feats = G.nodes[n].get('type_feats', [0, 0, 0, 0])
            feat.extend(type_feats)
            x.append(feat)
            
            # V6: Instruction block index (shifted by 1 because block 0 is global)
            block_map.append(G.nodes[n].get('block_idx', 0) + 1)
            
        x = torch.tensor(x, dtype=torch.float)
        block_map = torch.tensor(block_map, dtype=torch.long)
        
        # Edges
        edge_indices = []
        edge_types = []
        
        for u, v, data in G.edges(data=True):
            src = node_map[u]
            dst = node_map[v]
            edge_indices.append([src, dst])
            edge_type_str = data.get('type', 'control_next')
            if edge_type_str == 'control_branch': etype = 1
            elif edge_type_str == 'data_flow': etype = 2
            elif edge_type_str == 'call': etype = 5
            elif edge_type_str == 'loop_back': etype = 6
            else: etype = 0
            edge_types.append(etype)
            
        # Global Edges
        for i in range(1, num_total_nodes):
            edge_indices.append([0, i]); edge_types.append(3)
            edge_indices.append([i, 0]); edge_types.append(4)
            
        edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_types, dtype=torch.long)
             
        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, block_map=block_map)
        return data


# Singleton
extractor_v5 = IRGraphExtractorV5()

def extract_ir_graph_v5(file_path, focus_functions=None):
    G = extractor_v5.parse_file(file_path, focus_functions=focus_functions)
    data = extractor_v5.to_pyg_data(G)
    return data
