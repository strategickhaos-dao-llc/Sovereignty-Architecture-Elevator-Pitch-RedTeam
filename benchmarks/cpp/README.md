# C++ Baseline Implementations

This directory contains C++ baseline implementations for the FlameLang Statistical Operations Benchmark Suite.

## Purpose

C++ implementations serve as the **performance baseline** for comparison with Rust and FlameLang implementations.

## Standards

- **Language**: C++17
- **Compiler**: g++ with `-O3` optimization
- **Libraries**: Standard library (iostream, vector, algorithm, cmath)

## Structure

Each problem implementation follows the naming convention:
```
<problem-id>_<problem-name>.cpp
```

Example:
```
BC-001_simple_bar_chart.cpp
PC-001_simple_pie_chart.cpp
BP-001_five_number_summary_box_plot.cpp
```

## Building

```bash
g++ -std=c++17 -O3 -o benchmark <problem-file>.cpp
./benchmark
```

## Metrics Captured

- Execution time (nanoseconds)
- Memory footprint (bytes)
- Lines of code
- Compilation time (milliseconds)

## Status

🔥 **Ready for triplet generation** - awaiting problem-specific implementations.
