"""
Stratified Benchmark Sampler for Anti-Catastrophic Forgetting.

Problem: Uniform random sampling over all benchmarks leads to 55% synthetic,
17% synthetic-diverse, and only 1.3% PolyBench. The agent overfits to small
synthetic patterns and underperforms on real code.

Solution: Stratify by size (instruction count) and category, then sample
uniformly across strata. This ensures equal representation regardless of
pool size imbalance.
"""

import random
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

from ..passes import MetricsCollector
from ..passes.pass_executor import compile_to_ir


# Size strata by instruction count (after O0 canonicalization)
SIZE_STRATA = {
    "tiny":       (0,    50),
    "small":      (50,   200),
    "medium":     (200,  1000),
    "large":      (1000, 5000),
    "industrial": (5000, float("inf")),
}

# Category inference from path
CATEGORY_KEYWORDS = {
    "numeric":    ["linear-algebra", "datamining", "stencils", "medley", "polybench"],
    "systems":    ["mibench", "network", "large_scale", "anghaben_wrapped"],
    "synthetic":  ["synthetic", "diverse_synthetic"],
    "industrial": ["brotli", "zstd", "miniz", "lua", "lz4", "sqlite"],
    "embedded":   ["embedded", "beebs"],
    "graph":      ["graph"],
}


class StratifiedBenchmarkSampler:

    def __init__(self, benchmark_paths: List[Path], cache_dir: Optional[Path] = None):
        self.all_paths = [Path(p) for p in benchmark_paths]
        self._metrics = MetricsCollector()
        self._strata: Dict[str, List[Path]] = defaultdict(list)
        self._categories: Dict[str, List[Path]] = defaultdict(list)
        self._stratum_of: Dict[Path, str] = {}
        self._category_of: Dict[Path, str] = {}

        # Per-stratum reward tracking for adaptive sampling
        self._stratum_rewards: Dict[str, List[float]] = defaultdict(list)
        self._stratum_weight: Dict[str, float] = {}

        self._classify_all()

    def _infer_category(self, path: Path) -> str:
        path_str = str(path).lower().replace("\\", "/")
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in path_str for kw in keywords):
                return cat
        return "other"

    def _infer_stratum(self, path: Path) -> str:
        """Classify by instruction count. Falls back to file size heuristic."""
        try:
            if path.suffix in (".c", ".cpp"):
                # Quick file-size heuristic to avoid compiling everything at init
                size_kb = path.stat().st_size / 1024
                if size_kb < 1:
                    return "tiny"
                elif size_kb < 5:
                    return "small"
                elif size_kb < 30:
                    return "medium"
                elif size_kb < 150:
                    return "large"
                else:
                    return "industrial"
            else:
                # .ll file: count instructions directly
                count = self._metrics.count_instructions(str(path))
                for name, (lo, hi) in SIZE_STRATA.items():
                    if lo <= count < hi:
                        return name
                return "industrial"
        except Exception:
            return "medium"  # safe default

    def _classify_all(self):
        for p in self.all_paths:
            stratum = self._infer_stratum(p)
            category = self._infer_category(p)
            self._strata[stratum].append(p)
            self._categories[category].append(p)
            self._stratum_of[p] = stratum
            self._category_of[p] = category

        # Initialize uniform weights
        for s in self._strata:
            self._stratum_weight[s] = 1.0

    def sample(self) -> Path:
        """
        Sample one benchmark using stratified sampling.
        1. Pick a size stratum (weighted, initially uniform)
        2. Pick a benchmark uniformly from that stratum
        """
        populated = {s: paths for s, paths in self._strata.items() if paths}
        if not populated:
            return random.choice(self.all_paths)

        strata_names = list(populated.keys())
        weights = [self._stratum_weight.get(s, 1.0) for s in strata_names]
        total = sum(weights)
        probs = [w / total for w in weights]

        chosen_stratum = random.choices(strata_names, weights=probs, k=1)[0]
        return random.choice(populated[chosen_stratum])

    def report_reward(self, path: Path, reward: float):
        """Track per-stratum reward for adaptive weighting."""
        stratum = self._stratum_of.get(path)
        if stratum is None:
            return
        self._stratum_rewards[stratum].append(reward)

        # Keep rolling window of 100
        if len(self._stratum_rewards[stratum]) > 100:
            self._stratum_rewards[stratum] = self._stratum_rewards[stratum][-100:]

    def update_weights(self):
        """
        Boost sampling weight for underperforming strata.
        If a stratum's average reward drops below 50% of the best,
        double its sampling probability.
        """
        avgs = {}
        for s, rewards in self._stratum_rewards.items():
            if rewards:
                avgs[s] = sum(rewards) / len(rewards)

        if not avgs:
            return

        best_avg = max(avgs.values())
        if best_avg <= 0:
            return

        for s in self._strata:
            avg = avgs.get(s)
            if avg is not None and avg < 0.5 * best_avg:
                self._stratum_weight[s] = 2.0
            else:
                self._stratum_weight[s] = 1.0

    def get_stats(self) -> dict:
        """Return stratum/category distribution for logging."""
        return {
            "strata_counts": {s: len(paths) for s, paths in self._strata.items()},
            "category_counts": {c: len(paths) for c, paths in self._categories.items()},
            "stratum_weights": dict(self._stratum_weight),
            "stratum_avg_rewards": {
                s: (sum(r) / len(r) if r else 0.0)
                for s, r in self._stratum_rewards.items()
            },
        }
