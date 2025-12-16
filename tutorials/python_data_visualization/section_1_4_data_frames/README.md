# Section 1.4: Data Frames Tutorial

This tutorial module provides comprehensive examples and implementations of data frame concepts using Python and pandas, based on zyBooks section 1.4 curriculum.

## Overview

A **data frame** (DataFrame) is a two-dimensional tabular data structure with labeled columns and rows. This module teaches you how to:

- Understand DataFrame components (index, columns, values)
- Use the pandas library for data manipulation
- Subset and filter data
- Reshape data between long and wide forms

## Module Structure

```
section_1_4_data_frames/
├── __init__.py              # Module initialization
├── data_frames_intro.py     # Introduction to DataFrames
├── pandas_examples.py       # pandas library usage
├── subsetting_data.py       # Data subsetting techniques
├── reshaping_data.py        # Pivot and melt operations
└── README.md                # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install pandas seaborn matplotlib
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Running Individual Modules

Each module can be run independently to see demonstrations:

```bash
# Introduction to DataFrames
python data_frames_intro.py

# pandas Examples with Titanic Dataset
python pandas_examples.py

# Data Subsetting Techniques
python subsetting_data.py

# Reshaping Data (Pivot and Melt)
python reshaping_data.py
```

### Using as a Library

Import the module in your own Python scripts:

```python
from section_1_4_data_frames import data_frames_intro
from section_1_4_data_frames import pandas_examples
from section_1_4_data_frames import subsetting_data
from section_1_4_data_frames import reshaping_data

# Create and demonstrate a sample DataFrame
df = data_frames_intro.create_sample_tips_dataframe()
print(df)

# Load and analyze Titanic dataset
titanic = pandas_examples.load_titanic_dataset()
print(titanic.describe())

# Subset data
result = titanic[titanic['age'] < 30]
print(result)
```

## Learning Objectives

### 1. Introduction to Data Frames (`data_frames_intro.py`)

- Understand the three components of a DataFrame:
  - **Index**: Row labels
  - **Columns**: Column labels
  - **Values**: The actual data
- Create sample DataFrames
- Access DataFrame components

**Key Functions:**
- `create_sample_tips_dataframe()` - Creates sample restaurant tips data
- `demonstrate_dataframe_components()` - Shows index, columns, and values
- `create_state_income_dataframe()` - Creates state income data example

### 2. pandas Library (`pandas_examples.py`)

- Import data from various file formats (CSV, Excel, text)
- Use DataFrame attributes: `shape`, `columns`, `dtypes`, `index`, `size`, `values`
- Use DataFrame methods: `describe()`, `head()`, `tail()`, `mean()`, `min()`, `max()`
- Analyze the Titanic dataset

**Key Functions:**
- `load_titanic_dataset()` - Loads Titanic data from seaborn
- `demonstrate_dataframe_attributes()` - Shows all DataFrame attributes
- `demonstrate_dataframe_methods()` - Demonstrates statistical methods
- `example_1_4_1_titanic_dataset()` - Complete Titanic analysis example

### 3. Subsetting Data (`subsetting_data.py`)

- Select columns: `df['column']` or `df[['col1', 'col2']]`
- Select rows by position: `df[0:5]`
- Filter rows by condition: `df[df.age > 30]`
- Use `loc[]` and `iloc[]` for advanced selection
- Combine multiple conditions with `&`, `|`, `~`

**Key Functions:**
- `selecting_columns()` - Column selection techniques
- `selecting_rows()` - Row selection and filtering
- `loc_and_iloc_examples()` - Label-based and position-based indexing
- `advanced_subsetting_examples()` - Complex filtering with multiple conditions

### 4. Reshaping Data (`reshaping_data.py`)

- Understand long form vs. wide form data
- **Pivot**: Convert long form to wide form using `pd.pivot()`
- **Melt**: Convert wide form to long form using `pd.melt()`
- Specify index, columns, and values for reshaping

**Key Functions:**
- `demonstrate_pivoting()` - Long to wide conversion
- `demonstrate_melting()` - Wide to long conversion
- `participation_activity_1_4_7()` - Practice exercises

## Participation Activities

The module includes implementations of all participation activities from the zyBooks curriculum:

- **Activity 1.4.1**: Data frame components
- **Activity 1.4.2**: State income data frame
- **Activity 1.4.3**: Titanic dataset statistics
- **Activity 1.4.4**: Subsetting data exercises
- **Activity 1.4.5**: Pivoting demonstration
- **Activity 1.4.6**: Melting demonstration
- **Activity 1.4.7**: Pivot and melt practice

## Examples

### Example 1: Create and Display a DataFrame

```python
import pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
}
df = pd.DataFrame(data)
print(df)
```

### Example 2: Filter Titanic Data

```python
from section_1_4_data_frames.pandas_examples import load_titanic_dataset

titanic = load_titanic_dataset()

# Find all passengers younger than 18
children = titanic[titanic['age'] < 18]
print(f"Number of children: {len(children)}")

# Find first-class survivors
first_class_survivors = titanic[(titanic['pclass'] == 1) & (titanic['survived'] == 1)]
print(f"First class survivors: {len(first_class_survivors)}")
```

### Example 3: Reshape Data

```python
import pandas as pd

# Create long form data
df_long = pd.DataFrame({
    'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
    'metric': ['sales', 'costs', 'sales', 'costs'],
    'value': [1000, 600, 1200, 650]
})

# Pivot to wide form
df_wide = pd.pivot(df_long, index='date', columns='metric', values='value')
print(df_wide)
```

## Data Types in pandas

- **int64**: Integer numbers
- **float64**: Decimal numbers
- **object**: Strings or mixed types
- **bool**: Boolean values (True/False)
- **datetime64**: Date and time values
- **category**: Categorical data

## Common DataFrame Operations Reference

```python
# Basic Information
df.shape          # (rows, columns)
df.columns        # Column names
df.dtypes         # Data types
df.info()         # Summary info

# Statistics
df.describe()     # Summary statistics
df.mean()         # Column means
df.median()       # Column medians
df.std()          # Standard deviation

# Selection
df['col']         # Select one column (Series)
df[['col1', 'col2']]  # Select columns (DataFrame)
df[0:5]          # Select rows 0-4
df.loc[0:5, ['col1', 'col2']]  # Label-based
df.iloc[0:5, 0:3]               # Position-based

# Filtering
df[df['age'] > 30]              # Simple condition
df[(df['age'] > 30) & (df['city'] == 'NYC')]  # Multiple conditions

# Reshaping
pd.pivot(df, index='row_col', columns='col_col', values='value_col')
pd.melt(df, id_vars=['id_col'], value_vars=['val1', 'val2'])
```

## Troubleshooting

### Module Import Errors

If you encounter import errors, ensure you're in the correct directory:

```bash
cd tutorials/python_data_visualization
python -c "from section_1_4_data_frames import data_frames_intro"
```

### Missing seaborn Data

If the Titanic dataset fails to load, the module will automatically create sample data for demonstration purposes.

### Pandas Version Issues

This module requires pandas >= 1.0.0. Update if needed:

```bash
pip install --upgrade pandas
```

## Additional Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [seaborn Datasets](https://github.com/mwaskom/seaborn-data)

## Contributing

To add more examples or improve documentation:

1. Add your examples to the appropriate module file
2. Update this README with usage instructions
3. Ensure all code is well-commented and follows PEP 8 style guidelines
4. Test your changes by running the module directly

## License

This tutorial module is part of the Sovereignty Architecture project and follows the project's license terms.

## Questions and Support

For questions about this tutorial:
- Review the inline documentation in each module
- Run the examples to see output
- Check the pandas documentation for detailed API reference
