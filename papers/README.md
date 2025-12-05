# IEEE Benchmark Documentation

This directory contains IEEE-ready LaTeX content and supporting materials for the Sovereignty Architecture benchmark methodology.

## Contents

### LaTeX Subsections (`sovereignty_benchmarks.tex`)

Contains two IEEE-formatted subsections ready for inclusion in your paper:

1. **Benchmark Methodology** - Details the experimental setup including:
   - Hardware specifications (heterogeneous local cluster)
   - Software versions (Ollama, CUDA, model hashes)
   - Measurement methodology (warmup runs, trial runs, confidence intervals)
   - DOM Score weighting formula

2. **Results** - Presents benchmark findings:
   - Local inference performance (Qwen2.5:14b, Gemma3:1b)
   - Cloud baseline comparison (GPT-5.1, Claude Opus 4, Grok 4)
   - DOM Score rankings

### Figure Generation

Figures are generated using the benchmark scripts in `../benchmarks/`:

```bash
# Generate demo figures (IEEE reference data)
python benchmarks/generate_benchmark_figures.py --demo --output-dir papers/figs/

# Generate from actual benchmark results
python benchmarks/generate_benchmark_figures.py --input results.ndjson --output-dir papers/figs/
```

Generated figures:
- `figs/dom_radar_2025.pdf` - DOM Score radar chart
- `figs/latency_curves_2025.pdf` - Latency vs context length curves
- `figs/benchmark_table_2025.pdf` - Summary table (optional)

## Usage in Your Paper

### Prerequisites

Add these packages to your LaTeX preamble:

```latex
\usepackage{graphicx}
\usepackage{siunitx}
\usepackage{booktabs}
```

### Including the Content

```latex
% In your Methods section
\input{papers/sovereignty_benchmarks}

% Or copy-paste the individual subsections
```

### Figure Paths

Update figure paths in the LaTeX if needed:

```latex
\includegraphics[width=\columnwidth]{papers/figs/dom_radar_2025.pdf}
```

## Reproducibility

### Running Benchmarks

```bash
# Full benchmark with NDJSON output
python benchmarks/sovereignty_benchmark.py \
    --trials 10 \
    --warmup 3 \
    --output sovereignty_benchmark_results.ndjson

# Dry run to verify configuration
python benchmarks/sovereignty_benchmark.py --dry-run
```

### Environment Metadata

The benchmark script automatically captures:
- Hardware specifications (CPU, GPU, RAM)
- Software versions (Python, Ollama, CUDA)
- Model SHA-256 hashes
- Timestamp and hostname

All metadata is included in the NDJSON output for full reproducibility.

## DOM Score Formula

```
DOM Score = Speed × 0.40 + Freedom × 0.20 + Sovereignty × 0.20 + Cost × 0.20
```

Where:
- **Speed (40%)**: Normalized tokens/second, latency-adjusted
- **Freedom (20%)**: Content filtering restrictions (0=heavy, 100=none)
- **Sovereignty (20%)**: Data locality, no external API dependencies
- **Cost (20%)**: Operational cost per 1M tokens

## Zenodo Archive

For official publication, archive your benchmark data:

1. Run benchmarks with full metadata logging
2. Include the NDJSON results file
3. Upload to Zenodo and update the DOI in the LaTeX

---

**Strategickhaos DAO LLC** - Sovereign Infrastructure Benchmarks  
Generated: 2025-11-25
