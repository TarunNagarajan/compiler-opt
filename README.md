# Multi-Agent Hierarchical Reinforcement Learning for Compiler Optimization

A framework for training and evaluating hierarchical reinforcement learning (HRL) agents to optimize LLVM IR. The system uses a decomposed world model with residual scale correction to predict the impact of optimization passes across varying module sizes.

## Architecture

The system consists of three primary components:

1.  **World Model**: A structure-aware transition and metric prediction model built on GATv2 graph neural networks. It incorporates a scale correction pathway to maintain prediction accuracy for large-scale industrial modules.
2.  **HRL Agent**: A hierarchical policy comprising a strategic manager and a tactical worker. The manager negotiates over optimization objectives (e.g., speed, size, energy) to select macro-actions, which the worker then refines with tactical passes.
3.  **Compiler Environment**: A high-fidelity environment for LLVM IR manipulation, featuring hardware-aware profiling and robust runtime measurement.

## Installation

```bash
uv sync
```

## Usage

### Training the World Model

```bash
python scripts/train_world_model.py --dataset path/to/dataset.json
```

### Training the HRL Agent

```bash
python scripts/train_hrl.py --world_model path/to/model.pth --meta_calibrator path/to/calibrator.pth
```

### Evaluation

```bash
python scripts/eval_vs_o3.py --agent path/to/agent.pth
```

## Dataset

The training data includes 60,000+ optimization sequences collected from PolyBench, MiBench, and synthetic benchmark suites.
