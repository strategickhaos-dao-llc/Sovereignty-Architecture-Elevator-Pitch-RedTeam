# Figures Directory

Place benchmark figures here:

## Required Files

1. **dom_radar_2025.pdf** - DOM Score radar chart
   - Axes: Speed, Freedom, Sovereignty, Cost
   - Compare: Local stack vs GPT-5.1 vs Claude Opus 4

2. **latency_curves_2025.pdf** - Latency comparison curves (optional)
   - X-axis: Token count (input → output)
   - Y-axis: Latency (seconds)
   - Series: Each model configuration

## Figure Generation

Figures can be generated using:
- Python: matplotlib, plotly
- R: ggplot2
- Export to PDF for IEEE compatibility

## Example Radar Chart Data

```python
# DOM Score components
categories = ['Speed', 'Freedom', 'Sovereignty', 'Cost']

# Scores (normalized 0-100)
local_stack = [75, 100, 100, 100]  # DOM Score: 100
gpt_5_1 = [95, 60, 40, 30]         # DOM Score: 68
claude_opus_4 = [90, 40, 40, 25]   # DOM Score: 59
```
