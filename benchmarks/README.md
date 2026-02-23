# PolyBench/C 4.2 Benchmark Suite

This directory contains the complete **PolyBench/C 4.2** benchmark suite (30 kernels) organized for compiler optimization research.

## Categories

| Category | Benchmarks | Description |
|----------|------------|-------------|
| **datamining** | 2 | Statistical computations (correlation, covariance) |
| **linear-algebra** | 20 | BLAS-like kernels and solvers |
| **medley** | 3 | Miscellaneous algorithms (edge detection, shortest path, RNA) |
| **stencils** | 5 | Iterative stencil computations |

## Benchmark List

### Datamining
- `correlation.c` - Correlation computation
- `covariance.c` - Covariance computation

### Linear-Algebra
- `2mm.c` - 2 matrix multiplications (D=α·A·B·C+β·D)
- `3mm.c` - 3 matrix multiplications
- `atax.c` - Matrix transpose and vector mult
- `bicg.c` - BiCG sub kernel
- `cholesky.c` - Cholesky decomposition
- `doitgen.c` - Multi-resolution analysis kernel
- `durbin.c` - Toeplitz system solver
- `gemm.c` - Matrix multiplication
- `gemver.c` - Vector mult and matrix addition
- `gesummv.c` - Scalar, vector, matrix mult
- `gramschmidt.c` - Gram-Schmidt orthogonalization
- `lu.c` - LU decomposition
- `ludcmp.c` - LU decomposition with forward/back substitution
- `mvt.c` - Matrix vector product and transpose
- `symm.c` - Symmetric matrix multiplication
- `syr2k.c` - Symmetric rank-2k update
- `syrk.c` - Symmetric rank-k update
- `trisolv.c` - Triangular solver
- `trmm.c` - Triangular matrix multiplication

### Medley
- `deriche.c` - Deriche edge detection filter
- `floyd-warshall.c` - All-pairs shortest path
- `nussinov.c` - RNA secondary structure prediction

### Stencils
- `adi.c` - Alternating Direction Implicit solver
- `fdtd-2d.c` - 2D Finite Difference Time Domain
- `heat-3d.c` - 3D heat equation
- `jacobi-1d.c` - 1D Jacobi stencil
- `jacobi-2d.c` - 2D Jacobi stencil
- `seidel-2d.c` - 2D Gauss-Seidel stencil

## Usage

Compile to LLVM IR:
```bash
clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone benchmarks/linear-algebra/gemm.c -o gemm.ll
```

Run baseline report:
```bash
python scripts/run_baseline_report.py
```

## Dataset Sizes

Array sizes are configurable via preprocessor macros (default: 128-512). Example:
```bash
clang -DN=1024 -S -emit-llvm ...
```
