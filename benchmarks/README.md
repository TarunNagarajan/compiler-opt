# Compiler Optimization Benchmark Suite

This directory contains a diverse collection of benchmarks used for training and evaluating reinforcement learning agents for compiler optimization. The suite includes numerical kernels, synthetic code patterns, and real-world algorithms.

## Benchmark Categories

| Category | Description |
|----------|-------------|
| **PolyBench/C 4.2** | 30 numerical kernels (linear algebra, datamining, stencils, medley). |
| **MiBench** | Real-world embedded benchmarks (network, security, automotive, etc.). |
| **Synthetic** | Procedurally generated code patterns to stress-test specific optimizations. |
| **Diverse Synthetic** | Larger, more complex synthetic modules with varying control-flow density. |
| **Large Scale** | Industrial-sized modules for evaluating foveated perception and scaling. |
| **Adversarial** | Hand-crafted cases designed to trigger optimization regressions or edge cases. |
| **Graphs** | Benchmarks focused on pointer-heavy graph traversal and manipulation. |

## PolyBench/C 4.2 (Numerical Kernels)

- **datamining**: correlation, covariance
- **linear-algebra**: 2mm, 3mm, atax, bicg, cholesky, doitgen, durbin, gemm, gemver, gesummv, gramschmidt, lu, ludcmp, mvt, symm, syr2k, syrk, trisolv, trmm
- **medley**: deriche, floyd-warshall, nussinov
- **stencils**: adi, fdtd-2d, heat-3d, jacobi-1d, jacobi-2d, seidel-2d

## Advanced & Synthetic Suites

- **diverse_synthetic**: Focuses on deep loop nesting and complex conditional branching.
- **large_scale**: Includes modules with 1000+ basic blocks to evaluate GNN scalability.
- **mibench**: Subset of the MiBench suite including `bitcount`, `qsort`, and `sha`.
- **adversarial**: Specifically targets "O2-regressions" like `jacobi-1d` where standard flags increase code size.

## Usage

### Compile to LLVM IR
All benchmarks should be compiled with `-O0` and `-Xclang -disable-O0-optnone` to produce a clean baseline for the RL agent.

```bash
clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone benchmarks/linear-algebra/gemm.c -o gemm.ll
```

### Batch Processing
Use the provided script to generate IR for all registered benchmarks:
```bash
python scripts/run_baseline_report.py
```

## Dataset Configuration
The dataset used for training the World Model and HRL agents consists of 60,000+ optimization sequences collected across these suites.
