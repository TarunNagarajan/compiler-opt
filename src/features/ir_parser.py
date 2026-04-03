import re
from pathlib import Path
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set


@dataclass
class IRStats:
    num_functions: int
    num_basic_blocks: int
    num_instructions: int
    instruction_counts: Dict[str, int]
    num_calls: int
    num_branches: int
    num_loops: int
    max_loop_depth: int
    num_edges: int
    cyclomatic_complexity: int
    functions: List[str] = field(default_factory=list)
    function_details: Dict[str, Dict] = field(default_factory=dict)
    
    def __repr__(self):
        return (
            f"IRStats(functions={self.num_functions}, "
            f"blocks={self.num_basic_blocks}, "
            f"instructions={self.num_instructions}, "
            f"loops={self.num_loops}, "
            f"depth={self.max_loop_depth}, "
            f"complexity={self.cyclomatic_complexity})"
        )


@dataclass
class BasicBlock:
    name: str
    instruction_count: int
    instructions: List[str]
    predecessors: Set[str] = field(default_factory=set)
    successors: Set[str] = field(default_factory=set)


@dataclass
class ControlFlowGraph:
    blocks: Dict[str, BasicBlock]
    entry_block: str
    
    @property
    def num_nodes(self):
        return len(self.blocks)
    
    @property
    def num_edges(self):
        return sum(len(b.successors) for b in self.blocks.values())


class IRParser:
    
    INSTRUCTION_PATTERN = re.compile(r'^\s*(%[\w.]+\s*=\s*)?(\w+)\s+')
    BLOCK_LABEL_PATTERN = re.compile(r'^(\d+|[\w.]+):\s*')
    
    ARITHMETIC_OPS = {'add', 'sub', 'mul', 'udiv', 'sdiv', 'urem', 'srem', 'fadd', 'fsub', 'fmul', 'fdiv', 'frem'}
    MEMORY_OPS = {'load', 'store', 'alloca', 'getelementptr'}
    CONTROL_OPS = {'br', 'switch', 'ret', 'invoke', 'unreachable'}
    COMPARISON_OPS = {'icmp', 'fcmp'}
    
    def __init__(self, ir_path: str):
        self.path = Path(ir_path)
        if not self.path.exists():
            raise FileNotFoundError(f"IR file not found: {ir_path}")
        self.content = self.path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.cfg: Optional[ControlFlowGraph] = None
    
    def parse(self) -> IRStats:
        functions = self._count_functions()
        blocks = self._count_basic_blocks()
        instruction_counts = self._count_instructions()
        
        total_instructions = sum(instruction_counts.values())
        num_calls = instruction_counts.get('call', 0)
        num_branches = instruction_counts.get('br', 0) + instruction_counts.get('switch', 0)
        
        num_loops, max_depth = self._analyze_loops()
        
        # Calculate edges for complexity
        if not self.cfg:
            self.build_cfg()
        num_edges = self.cfg.num_edges
        
        complexity = num_edges - blocks + (2 * functions)
        
        # Collect function names and basic block counts per function
        func_list = []
        func_details = {}
        current_func = None
        
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith('define '):
                m = re.search(r"@(?:\"([^\"]+)\"|([\w\.\-]+))\(", stripped)
                if m:
                    current_func = m.group(1) or m.group(2)
                    func_list.append(current_func)
                    func_details[current_func] = {'blocks': 1} # Entry block
                continue
            if stripped == '}':
                current_func = None
                continue
            if current_func and self.BLOCK_LABEL_PATTERN.match(stripped):
                if not stripped.startswith('!'):
                    func_details[current_func]['blocks'] += 1

        return IRStats(
            num_functions=functions,
            num_basic_blocks=blocks,
            num_instructions=total_instructions,
            instruction_counts=instruction_counts,
            num_calls=num_calls,
            num_branches=num_branches,
            num_loops=num_loops,
            max_loop_depth=max_depth,
            num_edges=num_edges,
            cyclomatic_complexity=max(0, complexity),
            functions=func_list,
            function_details=func_details
        )
    
    def _count_functions(self) -> int:
        count = 0
        for line in self.lines:
            if line.strip().startswith('define '):
                count += 1
        return count
    
    def _count_basic_blocks(self) -> int:
        count = 0
        in_function = False
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith('define '):
                in_function = True
                count += 1
                continue
            if stripped == '}':
                in_function = False
                continue
            if in_function and self.BLOCK_LABEL_PATTERN.match(stripped):
                if not stripped.startswith('!'):
                    count += 1
        return count
    
    def _count_instructions(self) -> Dict[str, int]:
        counts = Counter()
        for line in self.lines:
            stripped = line.strip()
            if (not stripped or stripped.startswith(';') or stripped.startswith('!') or
                stripped.startswith('define ') or stripped.startswith('declare ') or
                stripped.startswith('source_filename') or stripped.startswith('target ') or
                stripped.startswith('@') or stripped.startswith('attributes ') or
                stripped == '{' or stripped == '}'):
                continue
            if self.BLOCK_LABEL_PATTERN.match(stripped):
                continue
            match = self.INSTRUCTION_PATTERN.match(stripped)
            if match:
                opcode = match.group(2)
                counts[opcode] += 1
        return dict(counts)

    def _analyze_loops(self) -> Tuple[int, int]:
        loop_count = 0
        max_depth = 0
        current_depth = 0
        for line in self.lines:
            if 'distinct !' in line and 'llvm.loop' in line:
                loop_count += 1
            if 'br label' in line and '!' in line and 'llvm.loop' in line:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            if 'ret ' in line or 'unreachable' in line:
                current_depth = 0
        return loop_count, max_depth
    
    def get_instruction_ratios(self) -> Dict[str, float]:
        stats = self.parse()
        total = max(stats.num_instructions, 1)
        arithmetic = sum(stats.instruction_counts.get(op, 0) for op in self.ARITHMETIC_OPS)
        memory = sum(stats.instruction_counts.get(op, 0) for op in self.MEMORY_OPS)
        control = sum(stats.instruction_counts.get(op, 0) for op in self.CONTROL_OPS)
        comparison = sum(stats.instruction_counts.get(op, 0) for op in self.COMPARISON_OPS)
        return {
            'pct_arithmetic': arithmetic / total,
            'pct_memory': memory / total,
            'pct_control': control / total,
            'pct_comparison': comparison / total,
            'pct_other': (total - arithmetic - memory - control - comparison) / total,
        }

    def build_cfg(self) -> ControlFlowGraph:
        if self.cfg:
            return self.cfg
            
        blocks = {}
        current_block_name = "entry"
        current_instrs = []
        in_function = False
        
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith('define '):
                in_function = True
                current_block_name = "entry"
                current_instrs = []
                continue
            if stripped == '}':
                if in_function:
                    blocks[current_block_name] = BasicBlock(current_block_name, len(current_instrs), current_instrs)
                in_function = False
                continue
            if not in_function:
                continue
            
            label_match = self.BLOCK_LABEL_PATTERN.match(stripped)
            if label_match:
                if current_block_name:
                    blocks[current_block_name] = BasicBlock(current_block_name, len(current_instrs), current_instrs)
                current_block_name = label_match.group(1)
                current_instrs = []
                continue
            
            if stripped and not stripped.startswith(';') and not stripped.startswith('!'):
                 current_instrs.append(stripped)

        if in_function and current_block_name:
             blocks[current_block_name] = BasicBlock(current_block_name, len(current_instrs), current_instrs)
            
        for name, block in blocks.items():
            if not block.instructions:
                continue
            last_instr = block.instructions[-1]
            if last_instr.startswith('br label'):
                target = last_instr.split('%')[-1].strip()
                self._add_edge(blocks, name, target)
            elif last_instr.startswith('br i1'):
                parts = last_instr.split('label %')
                if len(parts) >= 3:
                    self._add_edge(blocks, name, parts[1].split(',')[0].strip())
                    self._add_edge(blocks, name, parts[2].strip())
            elif last_instr.startswith('switch'):
                for t in re.findall(r'label %(\w+)', last_instr):
                    self._add_edge(blocks, name, t)
                    
        self.cfg = ControlFlowGraph(blocks, "entry")
        return self.cfg
    
    def _add_edge(self, blocks, src, dst):
        if src in blocks and dst in blocks:
            blocks[src].successors.add(dst)
            blocks[dst].predecessors.add(src)

    def get_graph_features(self) -> Tuple[List[List[float]], List[Tuple[int, int]]]:
        if not self.cfg:
            self.build_cfg()
        node_to_idx = {name: i for i, name in enumerate(self.cfg.blocks.keys())}
        node_features = []
        edge_index = []
        for name, block in self.cfg.blocks.items():
            feat = [min(block.instruction_count / 100.0, 1.0)]
            feat.append(1.0 if len(block.successors) > 1 else 0.0)
            feat.append(1.0 if any('ret ' in ins for ins in block.instructions) else 0.0)
            node_features.append(feat)
            for succ in block.successors:
                edge_index.append((node_to_idx[name], node_to_idx[succ]))
        return node_features, edge_index
