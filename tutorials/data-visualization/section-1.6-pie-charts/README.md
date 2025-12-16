# Section 1.6: Pie Charts

## Learning Objectives
- Interpret pie charts and exploded pie charts
- Create pie charts in Python using matplotlib
- Identify misuses of pie charts
- Understand best practices for data visualization

## Overview

A **pie chart** shows relative frequency for categories using a circle, with each category shown as a slice of appropriate size. While pie charts remain common due to their aesthetic appeal, bar charts are often preferred because length differences are interpreted more precisely than size differences.

## Contents

This tutorial includes Python examples demonstrating:

### Good Practices

1. **`example_1_6_1_basic_pie_chart.py`**
   - CDC data on health insurance by employment status
   - Demonstrates basic pie chart creation with `matplotlib`
   - Shows proper labeling and color selection

2. **`example_1_6_2_exploded_pie_chart.py`**
   - BLS time use survey for college students
   - Demonstrates exploded pie charts (separating one slice for emphasis)
   - Shows when and how to use the explode feature appropriately

### Common Mistakes and Misuses

3. **`example_1_6_3_too_many_slices.py`**
   - Demonstrates why pie charts with >5-6 slices are difficult to read
   - Shows cluttered labels and hard-to-compare slices
   - Suggests better alternatives (bar charts, grouping categories)

4. **`example_1_6_4_3d_pie_chart.py`**
   - Demonstrates how 3D effects distort data perception
   - Compares 2D vs. 3D pie charts side-by-side
   - Explains why 3D pie charts should be avoided

5. **`example_1_6_5_poor_colors_exploded.py`**
   - Shows problems with similar colors
   - Demonstrates over-exploded charts
   - Provides best practices for color selection

## Installation

```bash
# Install required packages
pip install -r requirements.txt
```

## Usage

Run any example script:

```bash
python example_1_6_1_basic_pie_chart.py
python example_1_6_2_exploded_pie_chart.py
python example_1_6_3_too_many_slices.py
python example_1_6_4_3d_pie_chart.py
python example_1_6_5_poor_colors_exploded.py
```

Each script will:
- Display an interactive matplotlib window with the chart
- Save a high-resolution PNG image of the chart
- Print key insights and lessons to the console

## Key Concepts

### Creating a Basic Pie Chart

```python
import matplotlib.pyplot as plt

sizes = [30, 40, 20, 10]
labels = ['Category A', 'Category B', 'Category C', 'Category D']

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.axis('equal')
plt.show()
```

### Creating an Exploded Pie Chart

```python
import matplotlib.pyplot as plt

sizes = [30, 40, 20, 10]
labels = ['Category A', 'Category B', 'Category C', 'Category D']
explode = (0, 0.1, 0, 0)  # Explode the 2nd slice

plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode)
plt.axis('equal')
plt.show()
```

### Parameters Explained

- **`sizes`**: List of values representing the size of each slice
- **`labels`**: List of category names for each slice
- **`autopct`**: Format string for percentage labels (e.g., `'%1.1f%%'` = one decimal place)
- **`explode`**: Tuple specifying how far to separate each slice (0 = no separation)
- **`startangle`**: Rotation angle to orient the chart
- **`colors`**: List of colors for each slice
- **`shadow`**: Boolean to add shadow effect (creates pseudo-3D look)

## Best Practices

### ✅ DO:
- Limit pie charts to 5-6 categories maximum
- Use contrasting, distinct colors
- Explode at most ONE slice (to emphasize it)
- Ensure the chart sums to 100%
- Use 2D pie charts only
- Consider using bar charts for easier comparison

### ❌ DON'T:
- Use more than 6 slices (creates clutter)
- Use similar colors (hard to distinguish)
- Explode multiple slices (disorienting)
- Use 3D effects (distorts perception)
- Use non-circular shapes (defeats the purpose)
- Add unnecessary decorative elements

## When to Use Pie Charts

**Good Use Cases:**
- Showing parts of a whole (must sum to 100%)
- Limited number of categories (3-5 ideal)
- When general proportions are more important than precise values
- When one category dominates (>50%)

**Better Alternatives:**
- **Bar charts**: For precise comparisons
- **Stacked bar charts**: For comparing multiple groups
- **Tables**: For exact values
- **Treemaps**: For hierarchical data with many categories

## Real-World Examples

### Example 1: CDC Health Insurance Data
The tutorial includes data from a U.S. Centers for Disease Control study showing:
- Unemployed adults: 51.0% uninsured, 29.3% private insurance, 19.7% public insurance
- Employed adults: 18.2% uninsured, 75.2% private insurance, 6.6% public insurance

**Key Finding**: Unemployed individuals are nearly 3x more likely to be uninsured.

### Example 2: College Student Time Use
Data from the Bureau of Labor Statistics showing average weekday time allocation:
- Sleeping: 36.2% (emphasis via exploded slice)
- Leisure and sports: 17.1%
- Educational activities: 13.8%
- Work: 10.0%
- Other activities: remaining percentage

**Key Insight**: Students spend more non-sleeping time on leisure than any other activity.

## Educational Context

This tutorial corresponds to **Section 1.6: Pie Charts** in a data visualization and statistics curriculum. It covers:
- Basic pie chart interpretation
- Creating charts with matplotlib
- Understanding visualization best practices
- Critical evaluation of chart design choices

## Additional Resources

- [matplotlib.pyplot.pie documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html)
- [Choosing the right chart type](https://www.data-to-viz.com/)
- [Colorblind-friendly palettes](https://colorbrewer2.org/)
- U.S. Centers for Disease Control and Prevention (CDC) data sources
- Bureau of Labor Statistics (BLS) American Time Use Survey

## License

Educational materials for data visualization learning purposes.

---

**Note**: All data used in these examples is either publicly available from government sources (CDC, BLS) or simplified for educational purposes.
