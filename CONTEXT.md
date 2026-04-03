# Project Context: RL for Compiler Optimization

## 1. Project Goal
Develop a Reinforcement Learning (RL) agent capable of selecting optimal LLVM pass sequences for diverse objectives (runtime speed, code size, energy efficiency).

## 2. Technical Architecture

### World Model
The world model is a transition and metric predictor that allows the agent to simulate optimization trajectories.
- **Backbone**: GATv2 Graph Neural Network for encoding LLVM IR structure.
- **Scale Correction**: A residual pathway that adjusts predictions based on module size features (local nodes, global nodes, foveation ratio).
- **Metric Head**: Uses Two-Hot SymLog binning for numerical stability across wide-ranging targets.

### Hierarchical RL (HRL) Agent
The agent is split into two levels:
- **Strategic Manager**: Mediates between specialized objective agents (Speed, Size, Energy, Security) to select high-level macro-actions.
- **Tactical Worker**: Refines the selected macro-action by inserting micro-passes or adjusting parameters (e.g., inlining thresholds).

### Environment
- **CompilerOptEnv**: A Gymnasium-compatible environment wrapping LLVM tools (`opt`, `clang`).
- **Telemetry**: Measures instruction counts, cycles (via hardware performance counters), and estimated energy consumption.

## 3. Implementation Status
- **World Model**: Decomposed architecture with scale correction is operational.
- **Agent**: Hierarchical structure with negotiation module implemented.
- **Training**: Dyna-Dagger loop for real-time world model refinement is functional.
- **Benchmarks**: 1,300+ kernels integrated across multiple suites.
