# Rust Comparison Implementations

This directory contains Rust implementations for the FlameLang Statistical Operations Benchmark Suite.

## Purpose

Rust implementations provide a **memory-safe comparison** baseline, demonstrating safety without sacrificing performance.

## Standards

- **Edition**: Rust 2021
- **Compiler**: rustc with `-O` optimization
- **Libraries**: std, plotters (for chart generation)

## Structure

Each problem implementation follows the naming convention:
```
<problem-id>_<problem-name>.rs
```

Example:
```
bc_001_simple_bar_chart.rs
pc_001_simple_pie_chart.rs
bp_001_five_number_summary_box_plot.rs
```

## Building

```bash
rustc -O -o benchmark <problem-file>.rs
./benchmark
```

Or using Cargo:
```bash
cargo build --release
cargo run --release
```

## Metrics Captured

- Execution time (nanoseconds)
- Memory footprint (bytes) - with memory safety guarantees
- Lines of code
- Compilation time (milliseconds)

## Memory Safety

All Rust implementations are guaranteed memory-safe by the Rust compiler. This provides a comparison point for FlameLang's safety features.

## Status

🔥 **Ready for triplet generation** - awaiting problem-specific implementations.
