# Data Visualization Tutorial

This directory contains educational materials for learning Python data visualization techniques, based on Section 1.3 of the course materials.

## Contents

- **1.3-python-data-visualization.md** - Main tutorial document covering:
  - Introduction to Python
  - Data types and data structures
  - Importing modules (pandas, matplotlib, numpy)
  - Using matplotlib for plotting
  - Creating multiple plots and overlay charts

- **unemployment_example.ipynb** - Jupyter notebook with working example of plotting unemployment rates over time

- **car_crashes_example.ipynb** - Jupyter notebook demonstrating overlay bar charts for automobile collision data

## Prerequisites

To run the Jupyter notebooks, you need the following Python packages installed:

```bash
pip install pandas matplotlib numpy jupyter
```

Or if you're using the project's requirements file:

```bash
pip install -r ../../requirements.visualization.txt
```

## Running the Examples

1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Open either notebook file in your browser

3. Run the cells sequentially to see the visualizations

## Learning Path

1. Read through **1.3-python-data-visualization.md** to understand the concepts
2. Run **unemployment_example.ipynb** to see a simple line chart in action
3. Run **car_crashes_example.ipynb** to learn about overlay bar charts
4. Experiment with modifying the code to create your own visualizations

## Topics Covered

### Data Types and Structures
- int, float, string, boolean
- sets, lists, tuples, dictionaries

### Module Imports
- Using the `import` statement
- Creating aliases with `as`
- Common data science libraries (pandas, matplotlib, numpy, etc.)

### matplotlib Basics
- Creating plots with `plt.plot()`
- Adding labels and titles
- Displaying plots with `plt.show()`
- Saving plots with `plt.savefig()`

### Advanced Plotting
- Multiple datasets on the same axes
- Overlay bar charts
- Customizing colors and transparency

## Next Steps

After completing this tutorial, continue to Section 1.4: Data frames to learn more about organizing and analyzing data with pandas.

---

*Part of the Sovereignty Architecture educational materials*
