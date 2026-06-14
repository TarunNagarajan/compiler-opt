# Multi-Agent Hierarchical Reinforcement Learning for Compiler Optimization

This repository contains a research framework for learning LLVM optimization
policies with a multi-agent hierarchical reinforcement learning (MA-HRL)
stack. The project studies whether an agent can choose compiler pass sequences
that improve code size, instruction count, runtime, and energy-sensitive proxy
metrics beyond fixed optimization pipelines such as `-O2` and `-O3`.

The core idea is to avoid treating compiler optimization as a flat sequence
prediction problem. The system separates high-level objective selection from
low-level pass choice, uses graph encoders over LLVM IR, and trains a world
model that estimates the consequences of candidate actions before the policy
commits to them.

## What This Project Builds

- A Gymnasium-compatible LLVM optimization environment that applies passes,
  recompiles IR, and reports code-size, instruction-count, runtime, and
  structural metrics.
- A graph world model for predicting optimization effects from LLVM IR graphs,
  including scale-aware correction for large modules.
- A hierarchical policy with strategic macro-action selection and tactical
  pass refinement.
- Runtime measurement utilities with repeated runs, median aggregation,
  outlier filtering, confidence intervals, and denoised runtime rewards.
- Evaluation and audit scripts for comparing learned policies against compiler
  baselines and for checking whether policies behave differently under speed,
  size, and embedded-system objectives.

## Architecture

The system has three main layers.

**Compiler environment.** `src/env/compiler_env.py` wraps LLVM IR files as RL
episodes. Each action applies one compiler pass or macro action, refreshes
static metrics, and optionally measures runtime with configurable repetition,
loop count, timeout, aggregation, and confidence thresholds. Runtime rewards are
noise-aware: small changes inside the confidence interval are discounted rather
than treated as real improvements.

**World model.** `src/models/world_model.py` implements the current V8.5-style
world model. It uses a graph encoder over LLVM IR, action conditioning, and a
residual scale-correction path so predictions can account for local graph size,
full module size, and foveation ratio. This lets the model keep structure-aware
predictions while correcting scale-sensitive failures on larger programs.

**Hierarchical policy.** `src/models/hrl_agent.py` combines a strategic manager,
a tactical worker, and a GRU pass-history encoder. The manager reasons over
macro objectives and pass families, while the worker selects concrete
refinements. This reduces the effective search depth compared with flat pass
selection and makes long optimization episodes easier to learn.

## Repository Layout

```text
src/
  actions/          Macro and micro action definitions
  env/              LLVM optimization environment and hardware profiling
  features/         Scalar and graph feature extraction
  models/           World model, HRL agent, calibration, and graph encoders
  passes/           Pass execution, metric collection, correctness checks
scripts/
  train_world_model.py       World-model correction and fine-tuning
  train_hrl.py               HRL policy training
  eval_custom.py             Single-file world-model diagnostic evaluation
  eval_vs_o3.py              Agent-vs-compiler baseline evaluation
  audit_mode_behavior.py     Objective-mode behavior audit
benchmarks/
  Benchmark inputs and benchmark notes
```

Large checkpoints, logs, rendered media, local tool drops, and temporary
analysis files are intentionally ignored. Keep reproducible source code,
benchmark definitions, and concise result summaries in Git; store heavy model
artifacts elsewhere.

## Setup

The project expects Python 3.12 or newer, an LLVM toolchain visible through the
configuration in `src/config.py`, and the PyTorch/PyG stack used by the graph
encoders. Install the PyTorch and `torch-geometric` wheels that match your CUDA
or CPU environment before running model training.

```bash
uv sync
```

If you are not using `uv`, install the project dependencies from
`pyproject.toml` in a virtual environment, then add the repository root to
`PYTHONPATH` when running scripts.

## Basic Usage

Train or fine-tune the world model:

```bash
python scripts/train_world_model.py \
  --phase v8_action_fix \
  --iterations 3 \
  --epochs 2 \
  --steps_per_iter 512
```

Run a targeted single-file diagnostic:

```bash
python scripts/eval_custom.py \
  --file benchmarks/example.ll \
  --checkpoint models/world_model_v8.5_best.pth \
  --meta_calibrator models/meta_calibrator_best.pth \
  --reward_mode size
```

Audit policy behavior across objective modes:

```bash
python scripts/audit_mode_behavior.py \
  --agent_ckpt models/hrl_agent.pth \
  --world_model_ckpt models/world_model_v8.5_best.pth \
  --meta_calibrator models/meta_calibrator_best.pth \
  --out results/mode_behavior_audit.json
```

Run compiler-baseline evaluation:

```bash
python scripts/eval_vs_o3.py --agent models/hrl_agent.pth
```

## Measurement Discipline

Compiler optimization rewards are noisy if runtime is measured naively. The
current environment exposes:

- `runtime_measure_runs`
- `runtime_measure_loop_count`
- `runtime_measure_timeout_seconds`
- `runtime_measure_aggregation`
- `runtime_target_rel_ci95_pct`
- `runtime_max_measure_runs`

`MetricsCollector.measure_runtime` records raw samples, filtered samples,
coefficient of variation, confidence intervals, timeouts, failed runs, and a
reliability flag. The environment uses those statistics to report raw runtime
gain, noise floor, denoised gain, and confidence for each action.

## Research Status

This is an active research codebase, not a packaged compiler product. The
current direction emphasizes three engineering goals:

1. Make world-model predictions useful across normal and large-module scales.
2. Make the HRL policy sensitive to the chosen objective instead of learning one
   generic pass sequence.
3. Make runtime claims defensible by measuring and exposing noise rather than
   hiding it inside a single timing number.

The repository is set up to support reproducible experiments, but large
checkpoints and raw training logs are excluded from Git to keep the project
reviewable.
