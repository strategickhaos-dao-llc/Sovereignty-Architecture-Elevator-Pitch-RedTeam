# zyBooks MAT-243 Progress Tracking & Data Visualization

**Course**: MAT-243 Applied Statistics for STEM  
**Student**: Dom (Me10101)  
**Institution**: SNHU (Southern New Hampshire University)  
**Semester**: Fall 2025

## 🎯 Overview

This directory contains comprehensive progress tracking, data visualization tools, and learning materials for MAT-243 (Applied Statistics for STEM) aligned with zyBooks interactive learning platform.

## 📁 Directory Structure

```
zybooks/
├── mat243/
│   ├── progress.json              # Progress tracking for all sections
│   ├── grade_calculator.py        # Calculate grades and export metrics
│   ├── test_bar_charts.py         # Pytest tests for participation activities
│   ├── intro_dataviz.py          # Introduction to data visualization
│   ├── dataframes.py             # Pandas DataFrame operations
│   ├── requirements.txt          # Python dependencies
│   ├── dataviz/                  # Data visualization module
│   │   ├── __init__.py
│   │   └── charts.py             # Chart creation functions
│   ├── notebooks/                # Jupyter notebook tutorials
│   │   └── bar_charts_tutorial.ipynb
│   └── sample_data/              # Sample datasets
│       ├── students.csv
│       ├── temperature.csv
│       └── workforce.csv
└── README.md                     # This file
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to the mat243 directory
cd zybooks/mat243

# Install required packages
pip install -r requirements.txt
```

### View Progress

```bash
# Generate progress report
python grade_calculator.py
```

**Output:**
```
======================================================================
zyBooks Progress Report - MAT-243 Applied Statistics for STEM
======================================================================
Student: Dom (Me10101)
Semester: Fall 2025

Module 1: Introduction to Data and Visualization
  Overall Score: 12.50%
  Progress: 0/8 sections completed
  Dopamine Points: 🔥 x 2
...
```

### Run Tests

```bash
# Run all tests with pytest
pytest test_bar_charts.py -v

# Run tests for specific question
pytest test_bar_charts.py -k q1 -v

# Run only participation activities
pytest test_bar_charts.py -m participation_activity -v
```

### Create Visualizations

```python
import pandas as pd
from dataviz import create_bar_chart

# Create sample data
data = pd.DataFrame({
    'Store': ['Walmart', 'Kroger', 'Target'],
    'Revenue': [559, 132, 93]
})

# Create bar chart
create_bar_chart(
    data,
    x_col='Store',
    y_col='Revenue',
    title='Revenue by Store',
    ylabel='Revenue ($B)'
)
```

## 📊 Module 1: Data and Visualization

### Section Coverage

| Section | Topic | Status | Progress |
|---------|-------|--------|----------|
| 1.1 | Statistics as a field | ⭕ Not Started | 0% |
| 1.2 | Types of data | ⭕ Not Started | 0% |
| 1.3 | Frequency distributions | ⭕ Not Started | 0% |
| 1.4 | Intro to data viz with Python | ⭕ Not Started | 0% |
| **1.5** | **Bar Charts** | **🔄 In Progress** | **33%** |
| 1.6 | Pie charts | ⭕ Not Started | 0% |
| 1.7 | Histograms | ⭕ Not Started | 0% |
| 1.8 | Scatter plots | ⭕ Not Started | 0% |

### Current Focus: Section 1.5 - Bar Charts

**Key Concepts:**
- ❌ Bar charts do NOT excel at showing exact values
- ✅ Bar charts DO excel at showing relative values
- Use for quick visual comparison between categories
- Best for: sales data, revenue comparison, categorical counts

**Completed Questions:**
- [x] Q1: False - Bar charts excel at exact values (Answer: FALSE ✅)
- [x] Q2: True - Bar charts excel at relative values (Answer: TRUE ✅)
- [ ] Q3: Pending
- [ ] Q4: Pending
- [ ] Q5: Pending
- [ ] Q6: Pending

**Dopamine Points**: 🔥🔥 (2/6)

## 🎓 Learning Resources

### Interactive Tutorials

1. **Bar Charts Tutorial** (`notebooks/bar_charts_tutorial.ipynb`)
   - Understanding when to use bar charts
   - Creating effective visualizations
   - Practice exercises

### Code Examples

#### Example 1: Data Visualization Intro
```bash
python intro_dataviz.py
```

**Features:**
- Why visualize data?
- Chart selection guide
- Pandas DataFrame basics
- Simple visualization examples
- Complete workflow

#### Example 2: DataFrame Operations
```bash
python dataframes.py
```

**Features:**
- Loading CSV data
- Filtering and selection
- Grouping and aggregation
- Statistical calculations
- Exporting results

### Available Chart Types

1. **Bar Charts** (`dataviz.create_bar_chart`)
   - Comparing categories
   - Horizontal and vertical
   - Value labels on bars
   - zyBooks Section 1.5

2. **Pie Charts** (`dataviz.create_pie_chart`)
   - Parts of a whole
   - Percentage display
   - Limited slices for clarity
   - zyBooks Section 1.6

3. **Histograms** (`dataviz.create_histogram`)
   - Distribution of numerical data
   - Frequency analysis
   - KDE overlay option
   - zyBooks Section 1.7

4. **Scatter Plots** (`dataviz.create_scatter_plot`)
   - Relationship between variables
   - Correlation analysis
   - Trend line option
   - zyBooks Section 1.8

## 📈 Progress Tracking

### Progress JSON Structure

```json
{
  "course": "MAT-243 Applied Statistics for STEM",
  "student": "Dom (Me10101)",
  "module_1": {
    "sections": {
      "1.5": {
        "status": "in_progress",
        "questions": {
          "q1": {
            "answer": "False",
            "status": "completed",
            "correct": true
          }
        }
      }
    }
  }
}
```

### Grade Calculator Features

- **Section Scoring**: Calculate percentage for each section
- **Module Averages**: Overall module performance
- **Dopamine Points**: Gamification tracking
- **Metrics Export**: JSON export for external tools
- **Progress Reports**: Human-readable summaries

### Pytest Markers

Custom markers for test organization:

```python
@pytest.mark.zybooks_mat243        # All MAT-243 tests
@pytest.mark.participation_activity # Participation activities
@pytest.mark.section_1_5           # Section 1.5 tests
@pytest.mark.q1                    # Specific question tests
```

## 🎯 Next Steps

1. **Complete Section 1.5**: Finish remaining bar chart questions (Q3-Q6)
2. **Section 1.6**: Move to pie charts
3. **Practice**: Work through Jupyter notebook exercises
4. **Build Portfolio**: Create visualizations with sample datasets

## 🔥 FlameLang Integration

Code includes FlameLang syntax comments showing future transpilation targets:

```python
# FlameLang Target Syntax:
# 🔥 visualize student_performance {
#     data: students
#     chart: bar
#     x: "Major"
#     y: "GPA" |> mean
#     title: "Average GPA by Major"
#     style: academic
# }
```

This demonstrates how zyBooks concepts will integrate with the Strategickhaos FlameLang compiler project.

## 📝 Dependencies

```
matplotlib>=3.5.0
seaborn>=0.12.0
pandas>=1.4.0
numpy>=1.21.0
scipy>=1.7.0
jupyter>=1.0.0
pytest>=7.0.0
```

## 🤝 Contributing

This is a personal learning repository for MAT-243 coursework. The code follows educational best practices and aligns with zyBooks interactive content.

## 📄 License

MIT License - Part of Strategickhaos DAO LLC educational resources

---

**Course Progress**: 2/48 questions completed (4.17%)  
**Current Streak**: 🔥🔥  
**Next Milestone**: Complete Section 1.5 Bar Charts  
**Last Updated**: 2025-12-16

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
