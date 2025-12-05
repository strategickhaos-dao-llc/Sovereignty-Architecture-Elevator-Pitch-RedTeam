# IEEE Publication Materials

This directory contains IEEE-ready LaTeX content for academic publications related to the Sovereignty Architecture project.

## Contents

- `methods_results_ieee.tex` - Benchmark Methodology and Results sections (IEEE format)
- `figs/` - Directory for figures (radar charts, latency curves)

## Usage

### Including in Your IEEE Document

1. **Copy the content directly**: Open `methods_results_ieee.tex` and copy-paste the desired sections into your main document.

2. **Or use LaTeX input**: In your main IEEE document, include:
   ```latex
   \input{methods_results_ieee}
   ```

### Required Figures

Place the following figures in the `figs/` directory:
- `dom_radar_2025.pdf` - DOM Score radar chart comparison
- `latency_curves_2025.pdf` - Per-model latency comparison (optional)

### DOI Placeholder

Replace `doi:10.5281/zenodo.XXXXXXX` with your actual Zenodo DOI after archiving supplementary materials.

## DOM Score Methodology

The composite DOM Score weights are:
| Criterion | Weight |
|-----------|--------|
| Speed | 40% |
| Freedom from content filtering | 20% |
| Operational sovereignty | 20% |
| Cost | 20% |

## Benchmark Results Summary

| Configuration | DOM Score | Tokens/s | Notes |
|--------------|-----------|----------|-------|
| Local (Qwen2.5:14b-instruct-q6_K) | 100/100 | 298 | Perfect sovereignty |
| Local (Gemma3:1b) | - | >800 | Lightweight swarm agents |
| GPT-5.1 (Cloud) | 68/100 | 3,789 | Higher raw throughput |
| Claude Opus 4 (Cloud) | 59/100 | - | Content filtering limits |

## Citation

If you use this methodology in your research, please cite the Sovereignty Architecture project:

```bibtex
@misc{strategickhaos2025sovereignty,
  title={Sovereignty Architecture: Local-First LLM Inference Benchmarks},
  author={Strategickhaos DAO LLC},
  year={2025},
  url={https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-}
}
```

---

*Empire Eternal — now with peer-reviewed numbers.*
♫↯∞
