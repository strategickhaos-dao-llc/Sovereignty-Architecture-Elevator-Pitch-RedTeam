# Examples Directory

This directory contains various examples and tutorials for the Sovereignty Architecture project.

## Contents

### Line Charts Tutorial (Section 1.8)

A comprehensive Python tutorial implementing line chart concepts from zyBooks Section 1.8.

**Files:**
- `line_charts_tutorial.py` - Main tutorial with 8 complete examples
- `line_charts_yfinance_example.py` - Advanced examples using real financial data
- `README_LINE_CHARTS.md` - Detailed documentation for line charts tutorial
- `requirements_line_charts.txt` - Python dependencies for the tutorial
- `*.png` - Generated chart images (8 examples)

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements_line_charts.txt

# Run the tutorial
python line_charts_tutorial.py

# (Optional) Run real financial data examples
pip install yfinance
python line_charts_yfinance_example.py
```

**What You'll Learn:**
- Creating line charts to visualize trends over time
- Adding linear trend lines to show overall direction
- Displaying multiple datasets for comparison
- Understanding when line charts are appropriate vs inappropriate
- Proper labeling, formatting, and best practices

**Examples Generated:**
1. ✅ Apple stock prices (scatter plot vs line chart comparison)
2. ✅ Apple stock with linear trend line
3. ✅ Google/Alphabet stock prices with trend line
4. ✅ Temperature comparison (2 cities - opposite hemispheres)
5. ✅ Temperature comparison (3 cities)
6. ✅ US unemployment rate (1980-2017)
7. ✅ Appropriate vs inappropriate use (categorical data)
8. ✅ Importance of proper labels and units

For more details, see [README_LINE_CHARTS.md](README_LINE_CHARTS.md)

---

### Java Hello CloudOS

A Java development example for the CloudOS workspace.

**Location:** `java-hello-cloudos/`

See the README in that directory for more information.

---

## Contributing

When adding new examples to this directory:

1. Create a dedicated subdirectory or use descriptive filenames
2. Include a README or documentation explaining the example
3. Add any dependencies to a requirements file
4. Include comments and docstrings in your code
5. Generate output files in appropriate formats (PNG for images, etc.)
6. Test your examples before committing

## Requirements

Different examples may have different requirements. Check the specific README files for each example.

**Common dependencies:**
- Python 3.7+
- matplotlib (for data visualization)
- numpy (for numerical operations)

## License

See the main repository LICENSE file.
