# MAT-243 Statistical Benchmark Suite

**Component ID**: BM-001  
**Status**: stub  
**Purpose**: Cross-language performance benchmarking with statistical analysis

## Overview

This benchmark suite provides a rigorous statistical framework for comparing performance across C++, Rust, and FlameLang implementations. It uses the five-number summary (minimum, Q1, median, Q3, maximum) plus outlier detection to provide robust performance metrics.

## Structure

```
stats_suite/
├── README.md           # This file
├── cpp/                # C++ implementations
│   ├── five_number_summary.cpp
│   └── Makefile
├── rust/               # Rust implementations
│   ├── five_number_summary.rs
│   └── Cargo.toml
├── flame/              # FlameLang implementations (future)
│   └── five_number_summary.fl
├── datasets/           # Test datasets
│   ├── small.txt       # 100 samples
│   ├── medium.txt      # 10,000 samples
│   └── large.txt       # 1,000,000 samples
├── oracles/            # Expected results for validation
│   ├── small_oracle.txt
│   ├── medium_oracle.txt
│   └── large_oracle.txt
└── run_benchmarks.sh   # Automated benchmark runner
```

## Benchmark Description

### Five-Number Summary

The five-number summary is a descriptive statistic that provides information about a dataset:

1. **Minimum**: The smallest value in the dataset
2. **Q1 (First Quartile)**: The median of the lower half of the data (25th percentile)
3. **Median (Q2)**: The middle value (50th percentile)
4. **Q3 (Third Quartile)**: The median of the upper half of the data (75th percentile)
5. **Maximum**: The largest value in the dataset

### Outlier Detection

Outliers are identified using the Interquartile Range (IQR) method:
- IQR = Q3 - Q1
- Lower bound = Q1 - 1.5 * IQR
- Upper bound = Q3 + 1.5 * IQR
- Values outside these bounds are considered outliers

### Boxplot Visualization

The five-number summary is commonly visualized as a boxplot:
```
    min     Q1    median    Q3      max
     |------|[======|======]|-------|
         ^          ^          ^
      outliers   50% of     outliers
                  data
```

## Implementation Requirements

Each language implementation must:

1. **Read input**: Accept dataset from stdin or file
2. **Calculate statistics**: Compute five-number summary and detect outliers
3. **Output format**: Print results in consistent format:
   ```
   Min: <value>
   Q1: <value>
   Median: <value>
   Q3: <value>
   Max: <value>
   IQR: <value>
   Outliers: <count> (<percentage>%)
   ```
4. **Performance**: Report execution time for statistical calculations only (exclude I/O)
5. **Memory**: Report peak memory usage

## Running Benchmarks

### Quick Start

```bash
# Run all benchmarks
./run_benchmarks.sh

# Run specific language
./run_benchmarks.sh cpp
./run_benchmarks.sh rust
./run_benchmarks.sh flame  # When FlameLang compiler is ready
```

### Manual Execution

#### C++
```bash
cd cpp
make
./five_number_summary < ../datasets/medium.txt
```

#### Rust
```bash
cd rust
cargo build --release
cargo run --release < ../datasets/medium.txt
```

#### FlameLang (Future)
```bash
cd flame
flamec five_number_summary.fl
./five_number_summary < ../datasets/medium.txt
```

## Dataset Generation

Datasets are generated with known statistical properties for validation:

### Small Dataset (100 samples)
- Normal distribution: μ=50, σ=10
- Contains 2-3 outliers (>3σ from mean)
- Purpose: Quick validation and debugging

### Medium Dataset (10,000 samples)
- Mixed distribution: 80% normal (μ=100, σ=15) + 20% uniform [0, 200]
- Contains ~500 outliers
- Purpose: Typical workload testing

### Large Dataset (1,000,000 samples)
- Real-world skewed distribution (log-normal)
- Contains ~50,000 outliers
- Purpose: Performance and scalability testing

## Oracle Validation

Each dataset has a corresponding oracle file with expected results (±0.01% tolerance):

```
# small_oracle.txt
Min: 15.234
Q1: 42.891
Median: 49.567
Q3: 57.234
Max: 89.123
IQR: 14.343
Outliers: 3 (3.00%)
```

Implementations should produce results matching the oracle within tolerance.

## Performance Metrics

Benchmarks track multiple performance dimensions:

1. **Execution Time**:
   - Time to compute statistics (excluding I/O)
   - Measured in microseconds for small, milliseconds for medium/large
   - Average of 10 runs with standard deviation

2. **Memory Usage**:
   - Peak memory consumption
   - Measured in KB/MB
   - Should scale linearly with dataset size

3. **Throughput**:
   - Samples processed per second
   - Target: >1M samples/second for all implementations

4. **Accuracy**:
   - Deviation from oracle values
   - Must be within 0.01% for all statistics

## Comparison Criteria

Languages are compared on:

1. **Raw Performance**: Execution time (lower is better)
2. **Memory Efficiency**: Peak memory usage (lower is better)
3. **Code Size**: Lines of code and binary size (lower is better)
4. **Compilation Time**: Time to build (lower is better)
5. **Maintainability**: Code complexity metrics (lower is better)

## Expected Performance Targets

Based on similar implementations:

| Language | Small (100) | Medium (10K) | Large (1M) | Memory  |
|----------|-------------|--------------|------------|---------|
| C++      | ~50 μs      | ~2 ms        | ~150 ms    | O(n)    |
| Rust     | ~50 μs      | ~2 ms        | ~150 ms    | O(n)    |
| FlameLang| ~100 μs     | ~4 ms        | ~300 ms    | O(n)    |

**Goal**: FlameLang should be within 2x of C++/Rust performance.

## Adding New Benchmarks

To add a new benchmark to the suite:

1. Create implementations in `cpp/`, `rust/`, and `flame/`
2. Generate test datasets with known properties
3. Create oracle files with expected results
4. Update `run_benchmarks.sh` to include new benchmark
5. Document the benchmark in this README
6. Update INVENTORY.yaml with new component ID

## Next Steps (BM-001 Completion)

- [ ] Implement C++ version with reference implementation
- [ ] Implement Rust version for comparison
- [ ] Generate realistic test datasets
- [ ] Create oracle files from reference implementation
- [ ] Write automated test harness (`run_benchmarks.sh`)
- [ ] Add visualization of results (boxplot generation)
- [ ] Integrate with CI/CD pipeline
- [ ] Document performance baselines

## References

- **MAT-243**: Statistics course focusing on descriptive statistics
- **Tukey's Method**: John Tukey's work on exploratory data analysis and boxplots
- **IQR Method**: Standard statistical outlier detection technique
- **Benchmark Design**: Principles from Computer Language Benchmarks Game

## Related Components

- **BM-002**: Language Performance Benchmarks (depends on BM-001)
- **BM-003**: Memory Safety Benchmarks (depends on BM-001)
- **FL-005**: LLVM Backend (will be validated using BM-001)
- **INF-005**: Monitoring Stack (will display BM-001 results)

---

**Last Updated**: 2025-12-16  
**Next Review**: When FL-001 (Lexer) is complete
