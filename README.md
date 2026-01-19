# Multi-Agent Hierarchical Reinforcement Learning for Compiler Optimization
A DeepSeek style approach to identify methods to classify compiler-level optimizations as macro/micro decisions, with an agent negotiation system to manage relative priority of performance objectives (instruction count, file size, execution time). 

I have the LLVM toolchain installed (clang version 21.1.8, opt included). Although I'd like a light and nimble C++ implementation of all scripts, making it easier(?) to interact with the LLVM API, I've made the decision to proceed with Python for lesser verbose code, and the fact that it's more easier to explain in a presentation. 

I'll be using a subset of **PolyBench + MiBench** for benchmarking the Agent. I'm planning on adding optimization agents for different DSLs, and will include benchmarks that would accurately depict performance gains in said Domain.

I'm also interested in adding support for link-time optimizations (-O4), where object files are stored in the LLVM bitcode file format and program optimization is done at link-time.

The time feature in the table below represents the overhead for applying the optimizations themselves (-O3 should have the least compilation overhead). 
For an RL agent, this is a critical metric because we want to find better ways to optimize the code without taking up too much time.

### Baseline Benchmark Results (PolyBench subset)

The following table summarizes the performance of standard LLVM optimization levels (`-O0` to `-Os`). The **Time** column represents the optimization overhead (pass application latency). **Reduct %** indicates the reduction in LLVM IR instruction count relative to `-O0`.

So from what I've read so far, 
| Benchmark | Level | Instr | Size (B) | Time (ms) | Reduct % |
|-----------|-------|-------|----------|-----------|----------|
| **3mm** | -O0 | 697 | 3113 | 0.00 | 0.0 |
| | -O1 | 514 | 3912 | 165.38 | 26.3 |
| | -O2 | 496 | 3880 | 81.55 | 28.8 |
| | -O3 | 515 | 4200 | 65.39 | 26.1 |
| | -Os | 496 | 3880 | 52.23 | 28.8 |
| **atax** | -O0 | 303 | 2135 | 0.00 | 0.0 |
| | -O1 | 275 | 2502 | 42.43 | 9.2 |
| | -O2 | 272 | 2798 | 51.97 | 10.2 |
| | -O3 | 272 | 2872 | 46.02 | 10.2 |
| | -Os | 272 | 2798 | 46.30 | 10.2 |
| **bicg** | -O0 | 329 | 2154 | 0.00 | 0.0 |
| | -O1 | 263 | 2517 | 40.33 | 20.1 |
| | -O2 | 203 | 2461 | 44.70 | 38.3 |
| | -O3 | 207 | 2527 | 48.75 | 37.1 |
| | -Os | 203 | 2461 | 50.27 | 38.3 |
| **correlation** | -O0 | 530 | 2811 | 0.00 | 0.0 |
| | -O1 | 407 | 3523 | 49.56 | 23.2 |
| | -O2 | 376 | 3525 | 49.26 | 29.1 |
| | -O3 | 512 | 4419 | 55.32 | 3.4 |
| | -Os | 376 | 3525 | 58.07 | 29.1 |
| **gemm** | -O0 | 284 | 2018 | 0.00 | 0.0 |
| | -O1 | 155 | 2071 | 40.54 | 45.4 |
| | -O2 | 182 | 2343 | 44.12 | 35.9 |
| | -O3 | 182 | 2343 | 43.53 | 35.9 |
| | -Os | 182 | 2343 | 42.06 | 35.9 |
| **gramschmidt** | -O0 | 393 | 2346 | 0.00 | 0.0 |
| | -O1 | 330 | 2912 | 44.82 | 16.0 |
| | -O2 | 414 | 3512 | 53.81 | -5.3 |
| | -O3 | 414 | 3528 | 51.39 | -5.3 |
| | -Os | 414 | 3512 | 50.88 | -5.3 |
| **jacobi-1d** | -O0 | 214 | 1888 | 0.00 | 0.0 |
| | -O1 | 205 | 1998 | 39.06 | 4.2 |
| | -O2 | 325 | 2678 | 44.79 | -51.9 |
| | -O3 | 323 | 2694 | 44.17 | -50.9 |
| | -Os | 325 | 2678 | 45.06 | -51.9 |
| **mvt** | -O0 | 333 | 2234 | 0.00 | 0.0 |
| | -O1 | 234 | 2468 | 41.72 | 29.7 |
| | -O2 | 210 | 2392 | 44.78 | 36.9 |
| | -O3 | 210 | 2408 | 44.91 | 36.9 |
| | -Os | 210 | 2392 | 49.17 | 36.9 |

Now, with all of the .ll files that are generated, I'll have to add a level in between where one could just take a glance and know that the features that have been extracted from the IR are physically there. More logging features as well. I'm using the SB3 PPO implementation.


