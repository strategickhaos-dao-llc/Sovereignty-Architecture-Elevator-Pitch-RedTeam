# Quick Start Guide - Line Charts Tutorial

This is a 5-minute guide to get you started with the Line Charts tutorial (Section 1.8).

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation (30 seconds)

```bash
cd examples
pip install -r requirements_line_charts.txt
```

This installs:
- `matplotlib` - For creating charts
- `numpy` - For calculations and trend lines

## Run the Tutorial (2 minutes)

```bash
python line_charts_tutorial.py
```

This generates 8 educational charts demonstrating:
1. ✅ Apple stock prices (scatter vs line comparison)
2. ✅ Apple stock with trend line
3. ✅ Google stock with trend line
4. ✅ Temperature comparison (2 cities)
5. ✅ Temperature comparison (3 cities)
6. ✅ US unemployment rate
7. ✅ Appropriate vs inappropriate use cases
8. ✅ Importance of proper labels

## View the Results

All charts are saved as PNG files in the current directory:
- `apple_stock_chart.png`
- `apple_stock_trendline.png`
- `google_stock_chart.png`
- `temperature_comparison.png`
- `three_cities_temperature.png`
- `unemployment_rate.png`
- `categorical_comparison.png`
- `labeling_importance.png`

## Test Everything Works

```bash
python test_line_charts.py
```

Expected output: `✓ ALL TESTS PASSED`

## Optional: Real Financial Data

To fetch real stock data from Yahoo Finance:

```bash
pip install yfinance
python line_charts_yfinance_example.py
```

This requires an internet connection.

## Learn More

- **Full Documentation**: [README_LINE_CHARTS.md](README_LINE_CHARTS.md)
- **Examples Overview**: [README.md](README.md)
- **Source Code**: `line_charts_tutorial.py`

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'matplotlib'`
**Solution**: Run `pip install -r requirements_line_charts.txt`

**Problem**: Charts not generating
**Solution**: Make sure you're in the `examples/` directory when running the scripts

**Problem**: Permission errors
**Solution**: Use `pip install --user -r requirements_line_charts.txt`

## Key Concepts You'll Learn

✅ **Line Charts**: Show trends over time with connected data points
✅ **Trend Lines**: Linear regression to show overall direction
✅ **Multiple Datasets**: Compare different data series on one chart
✅ **Appropriate Use**: When to use (and not use) line charts
✅ **Best Practices**: Proper labeling, units, and formatting

## Next Steps

1. Open the generated PNG files to see the charts
2. Read [README_LINE_CHARTS.md](README_LINE_CHARTS.md) for detailed explanations
3. Modify `line_charts_tutorial.py` to experiment with your own data
4. Try the yfinance examples for real-world stock data

---

**Total time to complete**: ~5 minutes
**Charts generated**: 8 examples
**Lines of code**: ~300 lines of well-documented Python
**Dependencies**: matplotlib, numpy (optional: yfinance)
