# Benchmark Test Harness

This directory contains the test runner and metrics collection infrastructure for the FlameLang Statistical Operations Benchmark Suite.

## Components

### runner.rs
Main benchmark harness that:
- Loads problem specifications from `benchmark_problems.yaml`
- Compiles and executes C++, Rust, and FlameLang implementations
- Collects performance metrics
- Validates semantic equivalence (GDSS)
- Generates comparison reports

## Metrics Collected

1. **execution_time_ns**: Execution time in nanoseconds
2. **memory_footprint_bytes**: Peak memory usage in bytes
3. **lines_of_code**: Implementation size
4. **semantic_clarity_score**: GDSS-validated semantic clarity (0.0-1.0)
5. **compilation_time_ms**: Compilation time in milliseconds

## Usage

```bash
cargo run --release
```

Or with custom configuration:
```bash
cargo run --release -- --iterations 20 --warmup 5 --output results/
```

## Configuration

```rust
RunnerConfig {
    iterations: 10,              // Number of benchmark iterations
    warmup_iterations: 3,        // Warmup runs (excluded from results)
    enable_gdss_validation: true, // Enable GDSS semantic validation
    output_dir: "benchmarks/results",
}
```

## GDSS Validation

The harness implements GDSS (Glyph-Decoded Statistical Semantics) validation to ensure semantic equivalence across language implementations:

- Compares visual output for chart-based operations
- Verifies structural semantic equivalence
- Validates that operations preserve meaning across languages
- Follows the principle: "READ THE PICTURE, don't compute"

## Output Formats

- **Console**: Real-time progress and summary tables
- **JSON**: Machine-readable results (`results.json`)
- **CSV**: Spreadsheet-compatible metrics (`results.csv`)
- **HTML**: Visual comparison report (planned)

## Report Example

```
═══════════════════════════════════════════════════════════════════
FlameLang Statistical Operations Benchmark Report
═══════════════════════════════════════════════════════════════════

Problem: BC-001
─────────────────────────────────────────────────────────────────
C++   | Time:    1234567ns | Memory:     4096B | LOC:   45 | Compile:    150ms
Rust  | Time:    1198234ns | Memory:     3584B | LOC:   38 | Compile:    890ms
Flame | Time:    1156789ns | Memory:     3072B | LOC:   22 | Compile:    420ms

[GDSS] ✓ Semantic equivalence validated
```

## Status

🔥 **Skeleton complete** - ready for problem-specific implementations and full GDSS validation logic.

## Dependencies

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_yaml = "0.9"
serde_json = "1.0"
```

## Building

```bash
cargo build --release
```

## Testing

```bash
cargo test
```
