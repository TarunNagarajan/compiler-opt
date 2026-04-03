# Hierarchical Reinforcement Learning for Compiler Pass Ordering: A World-Model-Guided Approach

## 1. Problem Statement

Modern optimizing compilers like LLVM apply transformation passes in a fixed order determined by optimization levels (-O1, -O2, -O3). This fixed ordering is a known limitation: the interaction between passes is program-dependent, and the same sequence that improves one program can degrade another. The phase-ordering problem, finding the best sequence of compiler passes for a given program, is NP-hard in the general case and remains an open challenge in compiler optimization.

Current solutions rely on static heuristics baked into the compiler. LLVM's -O3 pipeline applies over 70 passes in a predetermined order. While effective on average, this rigidity causes measurable inefficiencies: on stencil kernels, -O3 can over-unroll loops, increasing instruction cache pressure; on control-flow-heavy code, it may apply vectorization where scalar execution is faster. Our evaluation shows that -O2 outperforms -O3 on 15% of tested benchmarks due to these ordering artifacts.

We address this with a hierarchical reinforcement learning agent that learns program-specific pass orderings, guided by a neural world model trained on 5,400+ benchmarks spanning synthetic kernels to industrial codebases (SQLite, LZ4, yyjson). The agent operates in two modes: a speed mode targeting x86-64 (Tiger Lake) that aims to beat -O3 on wall-clock execution time, and an embedded mode targeting ARM Cortex-M33 that optimizes for code size, stack usage, and energy consumption.

## 2. Approach and Contributions

### 2.1 Why Existing Approaches Fall Short

Prior ML-based compiler optimization work suffers from three recurring issues:

**Flat action spaces.** Treating each of LLVM's 100+ passes as an independent action creates a combinatorial explosion. A 10-step sequence drawn from 100 passes yields 10^20 possible orderings. Agents waste training time exploring redundant or harmful combinations.

**Unreliable reward signals.** Instruction count, the most common proxy metric, is misleading. Our empirical measurements confirm that -O3 produces 4.3x more instructions than -O0 on PolyBench stencils, yet runs 2.8x faster due to vectorization and instruction-level parallelism. An agent minimizing instruction count would prefer slow, unoptimized code.

**Scale blindness.** A 50-instruction synthetic kernel and a 131,000-node SQLite function require fundamentally different optimization strategies. Prior work trains on narrow benchmark suites (typically PolyBench or cBench alone) and fails to generalize.

### 2.2 Our Solution

We introduce three key components:

**Hierarchical action space.** The agent selects from 17 macro-actions (curated pass groups like "canonicalize", "vectorize-aggressive", "cleanup") and 20 micro-refinement actions (individual passes like `instcombine`, `gvn`, `licm`). This reduces the effective branching factor from 100+ to 37 while preserving fine-grained control. Empirically, the top macro-action sequences achieve 41-46% average instruction reduction: `sroa` followed by `gvn` (45.7%), `gvn` followed by `instcombine` (45.1%), and `mem2reg` followed by `gvn` (44.8%), discovered from 48,850 high-performing sequences across the training set.

**Three-tier hybrid reward.** We decouple fast shaping signals from slow ground-truth measurements:

- Tier 1 (per-step): Deterministic IR delta metrics (instruction count, loads, stores, branches, allocas, vectorization ratio). Computed in under 1ms. Provides immediate gradient signal.
- Tier 2 (episode-end): Actual CPU cycle measurement against the -O3 baseline using `QueryThreadCycleTime` with adaptive sampling (CI95 < 2%). Called once per episode, not per step, reducing measurement overhead by 20x.
- Tier 3 (planning): A learned world model predicts Tier 2 outcomes from Tier 1 features, enabling fast rollout-based planning without runtime measurement.

**Foveated perception engine.** For industrial-scale programs, processing the full control-flow graph is infeasible (SQLite: 131,008 nodes, 42 seconds per GNN forward pass). Our foveated architecture focuses a 6-layer GNN on the top-K functions by complexity while condensing remaining blocks into summary nodes. This achieves a 3.05x speedup in GNN computation with 86% reduction in processed nodes, at a prediction error of 0.37% on LZ4 (4,644 basic blocks).

## 3. Dataset

The training corpus consists of 5,402 C source files compiled to LLVM IR at -O0 with `optnone` disabled, stratified across five tiers:

| Tier | Source | Files | Instruction Range | Role |
|------|--------|-------|-------------------|------|
| Tiny/Small | Synthetic generators, PolyBench/C | 5,390 | 10 - 5,000 | Fast iteration, coverage |
| Medium | MiBench (consumer, telecom, auto) | 6 | 5,000 - 50,000 | Real-world patterns |
| Large | MiBench (tiff, lame, mad), highlight | 1 | 50,000 - 150,000 | Scale stress-testing |
| Industrial | SQLite, LZ4, yyjson, zstd, miniz | 5 | 150,000 - 250,000 | Deployment-representative |

Small benchmarks include 72 PolyBench/C kernels (stencils, linear algebra, datamining), 200+ MiBench modules, and 5,100+ synthetically generated programs covering loop nests, branching patterns, recursive structures, and SIMD-amenable code.

Each benchmark is compiled to LLVM IR using Clang 21.1.8 with `-S -emit-llvm -O0 -Xclang -disable-O0-optnone -Wno-everything`, providing an unoptimized but valid IR starting point. We quarantined 60+ files that fail standalone compilation (missing external library dependencies, C++ code in .c wrappers) to prevent training on broken inputs.

## 4. World Model Training

The world model predicts the effect of applying a given LLVM pass to a given IR program. It takes as input a graph-level embedding of the program's control-flow structure, a one-hot action encoding, and scale context features (log node count, foveation ratio, scale gap), and outputs predicted deltas across 10 objective basis dimensions:

`d_runtime_pct, d_text_size_pct, d_instr_pct, d_size_pct, d_loads_pct, d_stores_pct, d_allocas_pct, d_branches_pct, d_calls_pct, d_blocks_pct`

### 4.1 Architecture

The model (V8) is built on a 6-layer GATv2 encoder with 128-dimensional hidden states, producing a graph-level embedding via global mean pooling. A gated-affine correction network (RSC: Residual Scale Correction) post-processes predictions with a 3-layer MLP (128-wide) conditioned on action embeddings and scale features. The correction network applies learned multipliers and shifts to the base prediction:

```
corrected = base_pred * exp(clamp(log_multiplier)) + shift
```

This allows the model to amplify predictions for industrial-scale programs (multiplier > 1.0) and suppress hallucinations on small programs (multiplier near 0, shift near 0).

Total parameters: 2,501,435. Of these, the correction pathway (scale_correction + action_correction_emb) contains approximately 200,000 trainable parameters during Phase 1, representing 8% of the model.

### 4.2 Training Protocol

Training follows a two-phase protocol:

**Phase 1: Correction-only.** The pretrained GNN encoder and transition layers are frozen. Only the correction network and objective heads are trained. Data is collected through on-policy rollouts in the compiler environment, with a tiered sampling strategy: 65% small, 15% medium, 12% large, 8% industrial. Each iteration collects 1,000 transitions (650 small + 150 medium + 120 large + 80 industrial), which feed into a replay buffer (maximum 10,000 transitions). Training uses Adam with cosine learning rate decay (5e-4 to 5e-5), batch size 8, and 15 epochs per iteration.

Sample weighting uses normalized importance weights: `w = (1 + log10(nodes/100))` for scale, multiplied by an active-transition bonus (1.5x for passes that change the IR, 0.5x for no-ops). Weights are normalized per-batch to prevent loss inflation as the buffer composition shifts.

Across 10 iterations, the correction network achieves a best validation loss of 6.36 (weighted MSE on objective basis predictions). Instruction-direction accuracy (predicting whether a pass increases or decreases instruction count) reaches 86.2%, with call-direction accuracy at 100%.

**Phase 2: Full fine-tuning (optional).** All parameters are unfrozen with per-layer learning rates: 1e-5 for the GNN encoder, 5e-4 for the transition and correction layers, 1e-4 for the objective heads. This phase refines the backbone using the now-calibrated correction network as a stabilizer.

### 4.3 Calibration

The world model is evaluated on held-out benchmarks across scales:

| Benchmark | Actual Change | Predicted Change | Status |
|-----------|--------------|-----------------|--------|
| syn_0042 (small) | -5.88% | -5.28% | Calibrated |
| stencil_512 (medium) | -7.79% | -6.85% | Calibrated |
| yyjson (industrial) | -4.56% | -11.18% | Gap present |

Calibration is strongest on small-to-medium benchmarks. Industrial-scale predictions show a systematic overestimation of optimization impact, attributable to the foveated perception discarding peripheral code that constrains real optimization gains. The correction network narrows this gap across training iterations.

## 5. Speed Mode: Beating -O3

The speed mode targets x86-64 execution on an 11th Gen Intel Core i5-1135G7 (Tiger Lake, 4 cores, 8 threads, 8GB RAM). The agent starts from canonicalized -O0 IR and selects up to 20 passes per episode. The reward combines per-step IR shaping (Tier 1) with an episode-end runtime comparison against a cached -O3 baseline (Tier 2).

Runtime measurement uses `QueryThreadCycleTime` (Windows cycle counter, thread-scoped) with:
- Process affinity pinned to a single core
- High-priority scheduling class
- Median of 5 runs, adaptive up to 10 runs targeting CI95 < 2%
- Loop count of 300 iterations per measurement

Early evaluation on PolyBench stencils shows checkpoint 0745 achieving a mean speedup of 1.052x over -O2 and 1.006x over -O3, winning on 4 of 9 benchmarks. On a broader medley evaluation, the agent achieves 30.66% final speedup (time) and 21.62% instruction reduction.

The agent exploits three weaknesses in -O3's fixed ordering:
1. **Over-vectorization.** On small loops, the agent learns to skip vectorization, avoiding setup overhead that exceeds the SIMD gain.
2. **Phase ordering.** Running `instcombine` after vectorization catches simplification opportunities that -O3's fixed pipeline misses.
3. **Unroll calibration.** The agent selects unroll factors matched to Tiger Lake's 6-wide dispatch, rather than -O3's fixed heuristic.

## 6. Embedded Mode: ARM Cortex-M33

The embedded mode targets the ARM Cortex-M33 (ARMv8-M Mainline), representative of constrained IoT devices (STM32U5, nRF9160) with 256KB-2MB Flash, 64-512KB RAM, and battery power budgets.

Cross-compilation uses LLVM's backend: `--target thumbv8m.main-none-eabi -mcpu=cortex-m33 -mfloat-abi=hard -mfpu=fpv5-sp-d16`. The agent optimizes four objectives with Cortex-M33-specific weights:

| Objective | Weight | Rationale |
|-----------|--------|-----------|
| Code size (.text) | 0.35 | Flash is physically limited and expensive |
| Memory footprint (stack + .data + .bss) | 0.25 | No MMU; stack overflow causes HardFault |
| Energy proxy | 0.25 | Battery life critical for IoT deployment |
| Memory access density | 0.15 | Fewer bus transactions per instruction |

Hard constraints enforce deployment safety: code exceeding 110% of the -O2 baseline .text size, or estimated stack usage exceeding 4KB, triggers episode termination with a large negative reward. The agent cannot learn strategies that would crash on the target device.

Key passes for embedded optimization include `tailcallelim` (eliminates stack frames for tail recursion), `sroa` and `mem2reg` (promote stack allocations to registers, critical on ARM's 13-register file), and `globalopt` (internalizes and eliminates unused globals, freeing RAM).

## 7. Green AI Emphasis

We deliberately constrain this project to a single consumer laptop (Intel i5-1135G7, 8GB RAM, no GPU). All training, including world model pre-training, correction fine-tuning, and HRL policy optimization, runs on CPU. This is both a practical constraint and a design principle.

**Training cost.** A full correction-only training run (10 iterations, 10,000 transitions, 150 epochs total) completes in approximately 3.5 hours of wall-clock time. Estimated energy consumption is 35-45 Wh (TDP of the i5-1135G7 is 12-28W under sustained load), corresponding to roughly 15-20g CO2 equivalent using the global average grid carbon intensity of 450 gCO2/kWh. A full training pipeline including world model pre-training, correction, and HRL policy training is estimated at under 100g CO2.

**Inference cost.** At deployment, the agent selects a pass sequence in under 200ms per benchmark (a single forward pass through the GNN + correction network). The optimization it discovers then applies via standard `opt` invocations, with no ongoing ML inference cost during compilation.

**Comparison.** Large-scale compiler optimization research (MLGO, AutoPhase) typically requires GPU clusters running for days. Our approach achieves competitive instruction reduction (21.6%) and measurable speedups over -O3 (1.006x) at a training cost roughly three orders of magnitude lower. The total carbon footprint of the entire project development and training is estimated at under 1 kgCO2, equivalent to driving a car approximately 4 kilometers.

This demonstrates that meaningful compiler optimization research does not require large compute budgets. The hierarchical architecture, world model guidance, and tiered data collection are specifically designed to maximize sample efficiency, making single-machine training viable.

## 8. Future Scope

Several extensions are planned or in progress:

**Benchmark diversity.** Integration of the BEEBS (Bristol/Embench) embedded benchmark suite for Cortex-M33 evaluation, and recovery of 60+ quarantined MiBench files through header stub generation. A stratified sampling system with per-stratum performance tracking will prevent catastrophic forgetting as the benchmark pool grows.

**Anti-catastrophic forgetting.** Experience replay with priority sampling (top 10% by reward magnitude) and per-stratum performance monitoring. If reward for any benchmark category drops below 50% of its historical best, sampling probability for that category doubles.

**Runtime prediction head.** The world model's objective basis currently predicts IR-level deltas. A dedicated head mapping Tier 1 features to Tier 2 runtime outcomes will enable planning without any runtime measurement after sufficient training data (estimated 500+ episodes).

**Multi-architecture transfer.** The objective basis formulation is architecture-agnostic. Retraining only the reward weights and measurement infrastructure enables transfer to new targets (RISC-V, Apple M-series) without retraining the world model or policy.

**Carbon-aware compilation.** Integration of CodeCarbon for per-episode emissions tracking, enabling a Pareto analysis of optimization quality versus training energy cost. The goal is to identify the point of diminishing returns where additional training produces negligible improvement per unit of carbon expenditure.
