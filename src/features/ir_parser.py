import re
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class IRStats:
    num_functions: int
    num_basic_blocks: int
    num_instructions: int
    instruction_counts: Dict[str, int]
    num_calls: int
    num_branches: int
    num_loops: int
    
    def __repr__(self):
        return (
            f"IRStats(functions={self.num_functions}, "
            f"blocks={self.num_basic_blocks}, "
            f"instructions={self.num_instructions}, "
            f"calls={self.num_calls})"
        )


class IRParser:
    
    INSTRUCTION_PATTERN = re.compile(
        r'^\s*(%[\w.]+\s*=\s*)?'
        r'(\w+)'
        r'\s+'
    )
    
    FUNCTION_PATTERN = re.compile(
        r'^define\s+.*@([\w.]+)\s*\('
    )
    
    BLOCK_LABEL_PATTERN = re.compile(
        r'^(\d+|[\w.]+):\s*'
    )
    
    ARITHMETIC_OPS = {'add', 'sub', 'mul', 'udiv', 'sdiv', 'urem', 'srem',
                      'fadd', 'fsub', 'fmul', 'fdiv', 'frem'}
    MEMORY_OPS = {'load', 'store', 'alloca', 'getelementptr'}
    CONTROL_OPS = {'br', 'switch', 'ret', 'invoke', 'unreachable'}
    COMPARISON_OPS = {'icmp', 'fcmp'}
    
    def __init__(self, ir_path: str):
        self.path = Path(ir_path)
        if not self.path.exists():
            raise FileNotFoundError(f"IR file not found: {ir_path}")
        
        self.content = self.path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
    
    def parse(self) -> IRStats:
        functions = self._count_functions()
        blocks = self._count_basic_blocks()
        instruction_counts = self._count_instructions()
        
        total_instructions = sum(instruction_counts.values())
        num_calls = instruction_counts.get('call', 0)
        num_branches = instruction_counts.get('br', 0) + instruction_counts.get('switch', 0)
        
        num_loops = self._estimate_loops()
        
        return IRStats(
            num_functions=functions,
            num_basic_blocks=blocks,
            num_instructions=total_instructions,
            instruction_counts=instruction_counts,
            num_calls=num_calls,
            num_branches=num_branches,
            num_loops=num_loops,
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
            
            if (not stripped or 
                stripped.startswith(';') or 
                stripped.startswith('!') or
                stripped.startswith('define ') or
                stripped.startswith('declare ') or
                stripped.startswith('source_filename') or
                stripped.startswith('target ') or
                stripped.startswith('@') or
                stripped.startswith('attributes ') or
                stripped == '{' or stripped == '}'):
                continue
            
            if self.BLOCK_LABEL_PATTERN.match(stripped):
                continue
            
            match = self.INSTRUCTION_PATTERN.match(stripped)
            if match:
                opcode = match.group(2)
                counts[opcode] += 1
        
        return dict(counts)
    
    def _estimate_loops(self) -> int:
        loop_count = 0
        for line in self.lines:
            if '!llvm.loop' in line:
                loop_count += 1
        return loop_count
    
    def get_instruction_ratios(self) -> Dict[str, float]:
        stats = self.parse()
        total = max(stats.num_instructions, 1)
        
        arithmetic = sum(stats.instruction_counts.get(op, 0) for op in self.ARITHMETIC_OPS)
        memory = sum(stats.instruction_counts.get(op, 0) for op in self.MEMORY_OPS)
        control = sum(stats.instruction_counts.get(op, 0) for op in self.CONTROL_OPS)
        comparison = sum(stats.instruction_counts.get(op, 0) for op in self.COMPARISON_OPS)
        other = total - arithmetic - memory - control - comparison
        
        return {
            'pct_arithmetic': arithmetic / total,
            'pct_memory': memory / total,
            'pct_control': control / total,
            'pct_comparison': comparison / total,
            'pct_other': other / total,
        }


def load_ir(path: str) -> IRParser:
    return IRParser(path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ir_parser.py <path_to_ir_file.ll>")
        sys.exit(1)
    
    parser = IRParser(sys.argv[1])
    stats = parser.parse()
    
    print(f"\n=== IR Statistics for {sys.argv[1]} ===")
    print(f"Functions:        {stats.num_functions}")
    print(f"Basic blocks:     {stats.num_basic_blocks}")
    print(f"Instructions:     {stats.num_instructions}")
    print(f"Calls:            {stats.num_calls}")
    print(f"Branches:         {stats.num_branches}")
    print(f"Loops:            {stats.num_loops}")
    
    print(f"\n=== Top 10 Instructions ===")
    sorted_instrs = sorted(stats.instruction_counts.items(), key=lambda x: -x[1])
    for opcode, count in sorted_instrs[:10]:
        print(f"  {opcode:20s} {count}")
    
    print(f"\n=== Instruction Ratios ===")
    ratios = parser.get_instruction_ratios()
    for name, ratio in ratios.items():
        print(f"  {name:20s} {ratio:.1%}")
