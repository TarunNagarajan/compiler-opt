# Multi-Agent Hierarchical Reinforcement Learning for Compiler Optimization

## Problem Statement

Modern compilers like GCC and LLVM ship with hundreds of optimization passes, but selecting the right sequence remains a black art. The standard `-O2` and `-O3` flags apply a fixed, one-size-fits-all pipeline that often leaves performance on the table or worse, sometimes _increases_ code size (see jacobi-1d at -O2: -51.9% instruction "reduction"). 

The core challenge is that optimization passes interact in complex, non-linear ways. A pass that helps one program might hurt another. Loop unrolling might expose vectorization opportunities in one kernel but bloat the instruction cache in another. There's no closed-form solution here; it's fundamentally a sequential decision-making problem under uncertainty.

I'm also interested in the **reward hacking** phenomenon in RL-based compiler optimization. Naive reward functions that only optimize for instruction count can lead agents to exploit loopholes (repeating the same pass, ignoring code size explosion, etc.) rather than finding genuinely good optimization sequences.

## Novelty

This project explores several ideas that I haven't seen combined elsewhere:

1. **Hierarchical Macro/Micro Decision Making**: Instead of treating all 200+ LLVM passes equally, I'm classifying them into macro-level strategic decisions (loop optimizations, vectorization, inlining policies) and micro-level tactical passes (dead code elimination, constant folding). The idea is that a high-level agent picks the strategy, and a low-level agent handles the details.

2. **Multi-Objective Agent Negotiation**: Rather than scalarizing instruction count, code size, and compile time into a single reward, I'm experimenting with separate agents that "negotiate" over these objectives. This should handle Pareto-optimal tradeoffs more gracefully than weighted sums.

3. **Reward Hacking Investigation**: I've implemented two reward modes (`hackable` and `secure`) specifically to study and demonstrate reward hacking in compiler optimization RL. Early results show that the naive `hackable` agent achieves lower actual optimization (17.0%) despite getting higher rewards, while the `secure` agent with penalties achieves better optimization (19.7%) but with negative rewards during training.

4. **Pass Sequence Analysis**: Tools to analyze what pass sequences the agents actually learn, measuring diversity, repetition patterns, and common transitions.
```

**Action Space**: 15 LLVM optimization passes (mem2reg, gvn, instcombine, loop-unroll, etc.)

**Observation Space**: 128-dimensional feature vector extracted from LLVM IR (instruction mix, basic block count, loop depth, memory operations, etc.)

**Reward Function**:
- **HACKABLE**: Simple instruction reduction percentage
- **SECURE**: Instruction reduction minus penalties for size increase (0.3×), compile time (0.1×), and pass repetition (0.2×)

## Prerequisites

- **LLVM Toolchain** (v14+): clang, opt, llc, llvm-as
  - I'm using LLVM 21.1.8 on Windows
  - On Ubuntu: `apt install llvm clang`
  - On macOS: `brew install llvm`

- **Python 3.10+** with the following packages:
  - stable-baselines3 (PPO implementation)
  - gymnasium (RL environment interface)
  - numpy (numerical operations)
  - tensorboard (training visualization)

- **uv** (Python package manager): https://docs.astral.sh/uv/
  - Handles virtual environment and dependencies automatically
  - Install: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Tools Used

| Tool | Purpose |
|------|---------|
| **LLVM/Clang** | Compiler infrastructure, IR generation, optimization passes |
| **Python** | Scripting, RL agent, feature extraction |
| **Stable-Baselines3** | PPO algorithm implementation |
| **Gymnasium** | RL environment standard interface |
| **TensorBoard** | Training visualization and reward curves |
| **PolyBench/C 4.2** | 30 numerical kernels for benchmarking |
| **uv** | Fast Python package manager |

## Installation

```bash
git clone https://github.com/yourusername/compiler-opt.git
cd compiler-opt
uv sync
```

Verify LLVM is installed:
```bash
clang --version
opt --version
```

Compile benchmarks to IR:
```bash
uv run python scripts/run_baseline_report.py
```

## Quick Start

```bash
uv run python scripts/train_baseline.py results/baseline/*.ll --mode hackable --timesteps 50000 --run-name hackable_50k
uv run tensorboard --logdir logs/tensorboard
```

## Training Commands

### Train with Different Reward Modes

```bash
uv run python scripts/train_baseline.py results/baseline/*.ll --mode hackable --timesteps 50000 --run-name hackable_50k
uv run python scripts/train_baseline.py results/baseline/*.ll --mode secure --timesteps 50000 --run-name secure_50k
```

### Resume Training from Checkpoint

```bash
uv run python scripts/train_baseline.py results/baseline/*.ll --mode hackable --timesteps 50000 --resume models/ppo_hackable.zip --run-name hackable_100k
```

### Evaluate a Trained Model

```bash
uv run python scripts/train_baseline.py results/baseline/*.ll --mode hackable --eval-only models/ppo_hackable.zip --run-name hackable_eval
```

### Analyze Pass Sequences

```bash
uv run python scripts/analyze_passes.py --eval logs/hackable_50k_eval.json
uv run python scripts/analyze_passes.py --compare-hackable logs/hackable_50k_eval.json --compare-secure logs/secure_50k_eval.json
```

## Reward Modes

| Mode | Description |
|------|-------------|
| `hackable` | Naive reward based only on instruction reduction |
| `secure` | Penalizes size increase, compile time, and pass repetition |

## Experimental Results (50k timesteps)

| Metric | HACKABLE | SECURE | Winner |
|--------|----------|--------|--------|
| Instruction Reduction | 17.0% | 19.7% | SECURE |
| Size Increase | 3.1% | 0.9% | SECURE |
| Pass Diversity | 0.13 | 0.17 | SECURE |
| Episode Reward | 0.19 | -1.38 | HACKABLE |

The HACKABLE agent gets higher rewards but worse actual optimization, demonstrating reward hacking.

## PolyBench/C 4.2 Baseline Results

### Datamining

| Benchmark | Level | Instr | Size (B) | Time (ms) | Reduct % |
|-----------|-------|-------|----------|-----------|----------|
| correlation | -O0 | 530 | 2811 | 0.00 | 0.0 |
| | -O1 | 407 | 3523 | 102.65 | 23.2 |
| | -O2 | 376 | 3525 | 87.54 | 29.1 |
| | -O3 | 512 | 4419 | 82.65 | 3.4 |
| | -Os | 376 | 3525 | 70.38 | 29.1 |
| covariance | -O0 | 387 | 2305 | 0.00 | 0.0 |
| | -O1 | 330 | 2683 | 69.00 | 14.7 |
| | -O2 | 338 | 2851 | 69.92 | 12.7 |
| | -O3 | 421 | 3293 | 90.06 | -8.8 |
| | -Os | 338 | 2851 | 66.60 | 12.7 |

### Linear Algebra

| Benchmark | Level | Instr | Size (B) | Time (ms) | Reduct % |
|-----------|-------|-------|----------|-----------|----------|
| 2mm | -O0 | 583 | 2811 | 0.00 | 0.0 |
| | -O1 | 439 | 3553 | 67.38 | 24.7 |
| | -O2 | 425 | 3505 | 83.18 | 27.1 |
| | -O3 | 476 | 3757 | 79.35 | 18.4 |
| | -Os | 425 | 3505 | 93.04 | 27.1 |
| 3mm | -O0 | 697 | 3113 | 0.00 | 0.0 |
| | -O1 | 514 | 3912 | 76.22 | 26.3 |
| | -O2 | 496 | 3880 | 73.03 | 28.8 |
| | -O3 | 515 | 4200 | 125.35 | 26.1 |
| | -Os | 496 | 3880 | 85.14 | 28.8 |
| atax | -O0 | 303 | 2135 | 0.00 | 0.0 |
| | -O1 | 275 | 2502 | 63.58 | 9.2 |
| | -O2 | 272 | 2798 | 75.88 | 10.2 |
| | -O3 | 272 | 2872 | 72.07 | 10.2 |
| | -Os | 272 | 2798 | 69.93 | 10.2 |
| bicg | -O0 | 329 | 2154 | 0.00 | 0.0 |
| | -O1 | 263 | 2517 | 61.25 | 20.1 |
| | -O2 | 203 | 2461 | 57.58 | 38.3 |
| | -O3 | 207 | 2527 | 58.24 | 37.1 |
| | -Os | 203 | 2461 | 56.97 | 38.3 |
| cholesky | -O0 | 493 | 2613 | 0.00 | 0.0 |
| | -O1 | 436 | 3289 | 70.01 | 11.6 |
| | -O2 | 407 | 3203 | 74.08 | 17.4 |
| | -O3 | 351 | 2899 | 68.96 | 28.8 |
| | -Os | 407 | 3203 | 72.60 | 17.4 |
| doitgen | -O0 | 385 | 2236 | 0.00 | 0.0 |
| | -O1 | 288 | 2827 | 62.29 | 25.2 |
| | -O2 | 307 | 2971 | 70.02 | 20.3 |
| | -O3 | 304 | 2939 | 92.16 | 21.0 |
| | -Os | 307 | 2971 | 83.21 | 20.3 |
| durbin | -O0 | 247 | 2056 | 0.00 | 0.0 |
| | -O1 | 229 | 2500 | 78.88 | 7.3 |
| | -O2 | 213 | 2588 | 74.31 | 13.8 |
| | -O3 | 213 | 2588 | 63.68 | 13.8 |
| | -Os | 213 | 2588 | 77.12 | 13.8 |
| gemm | -O0 | 284 | 2018 | 0.00 | 0.0 |
| | -O1 | 155 | 2071 | 59.33 | 45.4 |
| | -O2 | 182 | 2343 | 52.89 | 35.9 |
| | -O3 | 182 | 2343 | 64.33 | 35.9 |
| | -Os | 182 | 2343 | 59.02 | 35.9 |
| gemver | -O0 | 562 | 3012 | 0.00 | 0.0 |
| | -O1 | 365 | 3351 | 82.38 | 35.1 |
| | -O2 | 443 | 3895 | 88.98 | 21.2 |
| | -O3 | 443 | 3911 | 93.54 | 21.2 |
| | -Os | 443 | 3895 | 103.39 | 21.2 |
| gesummv | -O0 | 338 | 2259 | 0.00 | 0.0 |
| | -O1 | 118 | 1980 | 62.79 | 65.1 |
| | -O2 | 111 | 1964 | 63.17 | 67.2 |
| | -O3 | 111 | 1964 | 59.13 | 67.2 |
| | -Os | 111 | 1964 | 72.68 | 67.2 |
| gramschmidt | -O0 | 393 | 2346 | 0.00 | 0.0 |
| | -O1 | 330 | 2912 | 68.73 | 16.0 |
| | -O2 | 414 | 3512 | 74.87 | -5.3 |
| | -O3 | 414 | 3528 | 72.62 | -5.3 |
| | -Os | 414 | 3512 | 77.96 | -5.3 |
| lu | -O0 | 488 | 2487 | 0.00 | 0.0 |
| | -O1 | 433 | 3379 | 73.47 | 11.3 |
| | -O2 | 416 | 3357 | 73.89 | 14.8 |
| | -O3 | 358 | 3037 | 78.36 | 26.6 |
| | -Os | 416 | 3357 | 76.50 | 14.8 |
| ludcmp | -O0 | 734 | 3289 | 0.00 | 0.0 |
| | -O1 | 617 | 4216 | 97.57 | 15.9 |
| | -O2 | 624 | 4478 | 88.93 | 15.0 |
| | -O3 | 566 | 4158 | 91.51 | 22.9 |
| | -Os | 624 | 4478 | 89.98 | 15.0 |
| mvt | -O0 | 333 | 2234 | 0.00 | 0.0 |
| | -O1 | 234 | 2468 | 63.63 | 29.7 |
| | -O2 | 210 | 2392 | 117.56 | 36.9 |
| | -O3 | 210 | 2408 | 94.38 | 36.9 |
| | -Os | 210 | 2392 | 82.26 | 36.9 |
| symm | -O0 | 428 | 2523 | 0.00 | 0.0 |
| | -O1 | 257 | 2655 | 88.24 | 40.0 |
| | -O2 | 265 | 3263 | 141.96 | 38.1 |
| | -O3 | 366 | 4021 | 119.84 | 14.5 |
| | -Os | 265 | 3263 | 124.17 | 38.1 |
| syr2k | -O0 | 388 | 2307 | 0.00 | 0.0 |
| | -O1 | 234 | 2328 | 142.68 | 39.7 |
| | -O2 | 280 | 2708 | 143.33 | 27.8 |
| | -O3 | 325 | 2900 | 187.72 | 16.2 |
| | -Os | 280 | 2708 | 120.00 | 27.8 |
| syrk | -O0 | 320 | 2111 | 0.00 | 0.0 |
| | -O1 | 272 | 2529 | 116.57 | 15.0 |
| | -O2 | 309 | 2941 | 166.23 | 3.4 |
| | -O3 | 356 | 3117 | 97.54 | -11.2 |
| | -Os | 309 | 2941 | 190.27 | 3.4 |
| trisolv | -O0 | 242 | 1904 | 0.00 | 0.0 |
| | -O1 | 160 | 1998 | 79.20 | 33.9 |
| | -O2 | 154 | 2126 | 86.54 | 36.4 |
| | -O3 | 154 | 2126 | 74.09 | 36.4 |
| | -Os | 154 | 2126 | 92.02 | 36.4 |
| trmm | -O0 | 324 | 2108 | 0.00 | 0.0 |
| | -O1 | 247 | 2684 | 111.98 | 23.8 |
| | -O2 | 238 | 2668 | 118.75 | 26.5 |
| | -O3 | 335 | 3222 | 127.36 | -3.4 |
| | -Os | 238 | 2668 | 104.89 | 26.5 |

### Medley

| Benchmark | Level | Instr | Size (B) | Time (ms) | Reduct % |
|-----------|-------|-------|----------|-----------|----------|
| deriche | -O0 | 735 | 4125 | 0.00 | 0.0 |
| | -O1 | 538 | 4442 | 88.74 | 26.8 |
| | -O2 | 590 | 4852 | 122.01 | 19.7 |
| | -O3 | 580 | 4932 | 136.31 | 21.1 |
| | -Os | 590 | 4852 | 135.37 | 19.7 |
| floyd-warshall | -O0 | 259 | 1965 | 0.00 | 0.0 |
| | -O1 | 125 | 1951 | 67.87 | 51.7 |
| | -O2 | 210 | 3439 | 79.04 | 18.9 |
| | -O3 | 210 | 3439 | 91.19 | 18.9 |
| | -Os | 210 | 3439 | 81.96 | 18.9 |
| nussinov | -O0 | 570 | 2483 | 0.00 | 0.0 |
| | -O1 | 209 | 2307 | 83.98 | 63.3 |
| | -O2 | 222 | 3259 | 80.20 | 61.1 |
| | -O3 | 167 | 2955 | 69.98 | 70.7 |
| | -Os | 222 | 3259 | 91.18 | 61.1 |

### Stencils

| Benchmark | Level | Instr | Size (B) | Time (ms) | Reduct % |
|-----------|-------|-------|----------|-----------|----------|
| adi | -O0 | 704 | 3092 | 0.00 | 0.0 |
| | -O1 | 336 | 3731 | 97.06 | 52.3 |
| | -O2 | 303 | 3639 | 155.54 | 57.0 |
| | -O3 | 303 | 3639 | 94.27 | 57.0 |
| | -Os | 303 | 3639 | 86.15 | 57.0 |
| fdtd-2d | -O0 | 537 | 2583 | 0.00 | 0.0 |
| | -O1 | 395 | 3247 | 85.45 | 26.4 |
| | -O2 | 586 | 5083 | 91.41 | -9.1 |
| | -O3 | 578 | 5163 | 115.67 | -7.6 |
| | -Os | 586 | 5083 | 111.54 | -9.1 |
| heat-3d | -O0 | 659 | 2462 | 0.00 | 0.0 |
| | -O1 | 248 | 2884 | 78.98 | 62.4 |
| | -O2 | 525 | 5694 | 111.44 | 20.3 |
| | -O3 | 525 | 5694 | 119.91 | 20.3 |
| | -Os | 525 | 5694 | 183.77 | 20.3 |
| jacobi-1d | -O0 | 214 | 1888 | 0.00 | 0.0 |
| | -O1 | 205 | 1998 | 176.05 | 4.2 |
| | -O2 | 325 | 2678 | 190.41 | -51.9 |
| | -O3 | 323 | 2694 | 290.08 | -50.9 |
| | -Os | 325 | 2678 | 136.36 | -51.9 |
| jacobi-2d | -O0 | 370 | 2159 | 0.00 | 0.0 |
| | -O1 | 248 | 2462 | 253.16 | 33.0 |
| | -O2 | 447 | 3940 | 248.55 | -20.8 |
| | -O3 | 447 | 3940 | 228.61 | -20.8 |
| | -Os | 447 | 3940 | 131.02 | -20.8 |
| seidel-2d | -O0 | 277 | 1876 | 0.00 | 0.0 |
| | -O1 | 145 | 1969 | 97.50 | 47.7 |
| | -O2 | 138 | 2123 | 89.06 | 50.2 |
| | -O3 | 139 | 2087 | 102.52 | 49.8 |
| | -Os | 138 | 2123 | 83.35 | 50.2 |
