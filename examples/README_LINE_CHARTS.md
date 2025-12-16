# Line Charts Tutorial - Section 1.8

This directory contains Python implementations of the line chart concepts from zyBooks Section 1.8.

## Overview

Line charts (or line graphs) depict data trends by using straight lines to connect successive data points. This tutorial demonstrates:

- Creating basic line charts in Python
- Adding linear trend lines to show overall direction
- Displaying multiple datasets for comparison
- Understanding appropriate vs inappropriate use cases
- Proper labeling and formatting

## Requirements

```bash
pip install matplotlib numpy
```

Or if using yfinance for real stock data:
```bash
pip install matplotlib numpy yfinance
```

## Running the Examples

```bash
cd examples
python line_charts_tutorial.py
```

This will generate 8 example charts as PNG files in the `examples/` directory.

## Examples Included

### 1. Apple Stock Prices (March 2015 - March 2016)
**File:** `apple_stock_chart.png`

Demonstrates the difference between a scatter plot and a line chart. Shows how lines help convey trends and suggest values between data points.

**Key Learning:**
- Steeper lines indicate more rapid increases/decreases
- Flatter lines indicate little change
- Lines suggest continuous values between discrete data points

### 2. Apple Stock with Trend Line
**File:** `apple_stock_trendline.png`

Shows how to add a linear trend line to summarize the overall direction of the data. Despite some increases, the trend line clearly shows a decreasing pattern.

**Key Learning:**
- Trend lines show general direction from first to last point
- Computed using linear regression (numpy polyfit)
- Not just a simple connection of first and last points

### 3. Google/Alphabet Stock Prices
**File:** `google_stock_chart.png`

Demonstrates an increasing trend over the same time period, with a clear upward linear trend line.

**Key Learning:**
- Compare different stocks' performance
- Identify periods of rapid growth or decline
- Use trend lines to predict future direction

### 4. Temperature Comparison (2 Cities)
**File:** `temperature_comparison.png`

Compares Los Angeles, USA and Durban, South Africa temperatures showing opposite seasonal patterns due to being in different hemispheres.

**Key Learning:**
- Multiple datasets distinguished by color and markers
- Legend to identify each dataset
- Opposite patterns clearly visible

### 5. Temperature Comparison (3 Cities)
**File:** `three_cities_temperature.png`

Shows Pueblo (Colorado), Tianshui (China), and Asunción (Paraguay) to demonstrate more complex multi-dataset visualizations.

**Key Learning:**
- Handle 3+ datasets effectively
- Find similarities (Pueblo and Tianshui both northern hemisphere)
- Identify outliers (Asunción has opposite pattern)

### 6. US Unemployment Rate (1980-2017)
**File:** `unemployment_rate.png`

Economic data showing long-term trends with notable peaks during recessions.

**Key Learning:**
- Line charts work well for economic time series
- Clear visualization of business cycles
- Long-term trend analysis

### 7. Appropriate vs Inappropriate: Categorical Data
**File:** `categorical_comparison.png`

**IMPORTANT:** Shows why line charts should NOT be used for nominal categorical data.

**Key Learning:**
- ❌ Line chart: Lines incorrectly suggest relationships between unrelated states
- ✓ Bar chart: Properly represents categorical data without false relationships
- Nominal variables have no ordering, so lines are meaningless

### 8. Importance of Labels and Units
**File:** `labeling_importance.png`

Demonstrates the critical importance of proper axis labels and units.

**Key Learning:**
- Always label both axes
- Always include units (°F, USD, %, etc.)
- Missing labels make data uninterpretable
- Temperature without units: Is it °F, °C, or K?

## When to Use Line Charts

### ✓ Appropriate Use Cases:
- **Time series data**: Stock prices, temperatures, unemployment rates
- **Continuous variables**: Values that change smoothly over time
- **Trend analysis**: When you want to show direction and rate of change
- **Ordered data**: When the x-axis represents a meaningful sequence

### ❌ Inappropriate Use Cases:
- **Nominal categorical data**: States, colors, movie ratings (no inherent order)
- **Unrelated items**: Categories with no sequential relationship
- **Discrete, unrelated categories**: When lines would suggest false relationships

## Key Concepts

### Independent vs Dependent Variables
- **Independent (x-axis)**: Typically time or another control variable
- **Dependent (y-axis)**: The measured outcome that changes

### Linear Trend Lines
- Computed using linear regression
- Shows overall direction of data
- Useful for predictions and summaries
- Not just connecting first and last points

### Multiple Datasets
- Use different colors for each dataset
- Add markers (circles, squares, triangles)
- Include a legend
- Keep it readable (avoid too many lines)

## Best Practices

1. **Always label axes** with descriptive names
2. **Include units** (USD, %, °F, etc.)
3. **Add a title** that describes what the chart shows
4. **Use a legend** when showing multiple datasets
5. **Add gridlines** for easier reading (with low alpha)
6. **Choose appropriate colors** (colorblind-friendly when possible)
7. **Don't use line charts for categorical data**
8. **Keep it simple** - don't overcrowd the chart

## Python Libraries Used

- **matplotlib.pyplot**: Main plotting library
- **numpy**: Numerical computations and trend line calculations
- **datetime**: Date handling (for real-world examples)

## Further Reading

- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Data Visualization Best Practices](https://www.tableau.com/learn/articles/data-visualization-tips)
- zyBooks Section 1.8: Line Charts

## Questions for Review

1. What does the steepness of a line indicate in a line chart?
2. When should you use a bar chart instead of a line chart?
3. How is a linear trend line calculated?
4. Why is it important to include units on axis labels?
5. What makes temperature data from different hemispheres interesting to compare?

## Answers

1. Steeper lines indicate more rapid increases or decreases; flatter lines indicate little change
2. Use bar charts for categorical (nominal) data where there's no inherent ordering or relationship between items
3. Using linear regression (e.g., numpy's polyfit function), not just connecting first and last points
4. Without units, viewers cannot interpret the data correctly (is temperature in °F or °C? is money in USD or EUR?)
5. They show opposite seasonal patterns because when it's summer in the northern hemisphere, it's winter in the southern hemisphere

---

**Created for educational purposes based on zyBooks Section 1.8 content**
