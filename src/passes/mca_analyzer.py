"""
llvm-mca Diagnostic Analyzer.

NOT used for reward computation (llvm-mca Total Cycles is invalid for cross-optimization
comparison due to loop unrolling differences). Used for:
- Post-training analysis: per-BB port pressure, bottleneck identification
- Debugging: understanding WHY a pass sequence beats/loses to O3
- Evaluation reporting: detailed microarchitecture breakdown
"""

import subprocess
import tempfile
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from ..config import LLC, LLVM_MCA


@dataclass
class MCAResult:
    total_cycles: int
    ipc: float
    block_rthroughput: float
    uops_per_cycle: float
    raw_output: str


class MCAAnalyzer:
    """Wraps llc + llvm-mca for diagnostic analysis of IR."""

    def __init__(self, mcpu: str = "tigerlake"):
        self._llc = str(LLC)
        self._mca = str(LLVM_MCA)
        self._mcpu = mcpu
        self._temp_dir = Path(tempfile.mkdtemp())

    def analyze(self, ir_path: str) -> Optional[MCAResult]:
        """IR -> assembly -> llvm-mca -> parsed metrics."""
        asm_path = self._temp_dir / "analysis.s"

        # Step 1: IR -> assembly
        llc_cmd = [
            self._llc, "-O2", f"-mcpu={self._mcpu}",
            "-filetype=asm", str(ir_path), "-o", str(asm_path)
        ]
        try:
            result = subprocess.run(llc_cmd, capture_output=True, timeout=30)
            if result.returncode != 0:
                return None
        except Exception:
            return None

        # Step 2: assembly -> llvm-mca
        mca_cmd = [self._mca, f"-mcpu={self._mcpu}", str(asm_path)]
        try:
            result = subprocess.run(mca_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return None
        except Exception:
            return None

        return self._parse_output(result.stdout)

    def _parse_output(self, output: str) -> MCAResult:
        total_cycles = 0
        ipc = 0.0
        block_rt = 0.0
        uops_per_cycle = 0.0

        m = re.search(r'Total Cycles:\s+(\d+)', output)
        if m:
            total_cycles = int(m.group(1))

        m = re.search(r'Block RThroughput:\s+([\d.]+)', output)
        if m:
            block_rt = float(m.group(1))

        m = re.search(r'IPC:\s+([\d.]+)', output)
        if m:
            ipc = float(m.group(1))

        m = re.search(r'uOps Per Cycle:\s+([\d.]+)', output)
        if m:
            uops_per_cycle = float(m.group(1))

        return MCAResult(
            total_cycles=total_cycles,
            ipc=ipc,
            block_rthroughput=block_rt,
            uops_per_cycle=uops_per_cycle,
            raw_output=output,
        )
