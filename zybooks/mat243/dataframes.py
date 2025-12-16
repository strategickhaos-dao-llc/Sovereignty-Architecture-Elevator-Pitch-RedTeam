#!/usr/bin/env python3
"""
MAT-243: Data Frames Module using Pandas

zyBooks Reference: Module 1 - Introduction to Data and Visualization
FlameLang Integration: Type-safe DataFrame operations layer

This module implements DataFrame operations matching zyBooks Module 1 content:
- Reading CSV files
- Data filtering and selection
- Grouping and aggregation
- Basic data transformations

Author: Strategickhaos DAO LLC
Course: MAT-243 Applied Statistics for STEM
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple
import warnings

warnings.filterwarnings('ignore')


class DataFrameOperations:
    """
    Pandas DataFrame operations aligned with zyBooks Module 1.
    
    Provides clean, educational interface for common DataFrame operations
    with type hints for future FlameLang integration.
    
    # FlameLang Target Type Annotations:
    # 🔥 type DataFrame {
    #     rows: Int
    #     columns: List[String]
    #     data: Matrix[Float | String | Int]
    #     operations: [filter, group, aggregate, transform]
    # }
    """
    
    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize DataFrame operations.
        
        Args:
            filepath: Optional path to CSV file to load
        """
        self.df: Optional[pd.DataFrame] = None
        self.filepath = filepath
        
        if filepath:
            self.load_csv(filepath)
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        zyBooks Concept: Reading external data is the first step in analysis.
        
        # FlameLang Syntax:
        # 🔥 load_data from "data.csv" {
        #     encoding: "utf-8"
        #     headers: true
        #     infer_types: true
        # }
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        try:
            self.df = pd.read_csv(filepath)
            print(f"✅ Loaded {len(self.df)} rows from {filepath}")
            print(f"Columns: {list(self.df.columns)}")
            return self.df
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            raise
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            raise
    
    def filter_rows(
        self,
        column: str,
        operator: str,
        value: Union[int, float, str]
    ) -> pd.DataFrame:
        """
        Filter DataFrame rows based on condition.
        
        zyBooks Concept: Filtering lets you focus on specific subsets of data.
        
        # FlameLang Syntax:
        # 🔥 filter students where {
        #     gpa >= 3.5
        #     and major == "Math"
        # }
        
        Args:
            column: Column name to filter on
            operator: Comparison operator (==, !=, >, <, >=, <=)
            value: Value to compare against
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        operators = {
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y
        }
        
        if operator not in operators:
            raise ValueError(f"Invalid operator: {operator}")
        
        filtered = self.df[operators[operator](self.df[column], value)]
        print(f"✅ Filtered to {len(filtered)} rows where {column} {operator} {value}")
        
        return filtered
    
    def select_columns(self, columns: List[str]) -> pd.DataFrame:
        """
        Select specific columns from DataFrame.
        
        zyBooks Concept: Focus on relevant variables for analysis.
        
        # FlameLang Syntax:
        # 🔥 select [name, age, gpa] from students
        
        Args:
            columns: List of column names to select
            
        Returns:
            DataFrame with selected columns
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        selected = self.df[columns]
        print(f"✅ Selected {len(columns)} columns: {columns}")
        
        return selected
    
    def group_by(
        self,
        group_column: str,
        agg_column: str,
        agg_func: str = 'mean'
    ) -> pd.DataFrame:
        """
        Group data and calculate aggregates.
        
        zyBooks Concept: Grouping reveals patterns across categories.
        
        # FlameLang Syntax:
        # 🔥 group students by major {
        #     calculate: mean(gpa)
        #     calculate: count(*)
        # }
        
        Args:
            group_column: Column to group by
            agg_column: Column to aggregate
            agg_func: Aggregation function (mean, sum, count, min, max, std)
            
        Returns:
            Grouped and aggregated DataFrame
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        agg_functions = {
            'mean': 'mean',
            'sum': 'sum',
            'count': 'count',
            'min': 'min',
            'max': 'max',
            'std': 'std',
            'median': 'median'
        }
        
        if agg_func not in agg_functions:
            raise ValueError(f"Invalid aggregation function: {agg_func}")
        
        grouped = self.df.groupby(group_column)[agg_column].agg(agg_functions[agg_func])
        grouped = grouped.reset_index()
        grouped.columns = [group_column, f'{agg_func}_{agg_column}']
        
        print(f"✅ Grouped by {group_column}, calculated {agg_func} of {agg_column}")
        
        return grouped
    
    def sort_by(
        self,
        column: str,
        ascending: bool = True
    ) -> pd.DataFrame:
        """
        Sort DataFrame by column.
        
        zyBooks Concept: Sorting helps identify top/bottom values.
        
        # FlameLang Syntax:
        # 🔥 sort students by gpa descending
        
        Args:
            column: Column to sort by
            ascending: Sort direction (True=ascending, False=descending)
            
        Returns:
            Sorted DataFrame
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        sorted_df = self.df.sort_values(column, ascending=ascending)
        direction = "ascending" if ascending else "descending"
        print(f"✅ Sorted by {column} ({direction})")
        
        return sorted_df
    
    def calculate_statistics(self, column: str) -> Dict[str, float]:
        """
        Calculate descriptive statistics for a column.
        
        zyBooks Concept: Summary statistics describe data distribution.
        
        # FlameLang Syntax:
        # 🔥 statistics of gpa {
        #     mean, median, std
        #     min, max, quartiles
        # }
        
        Args:
            column: Column to analyze
            
        Returns:
            Dictionary of statistics
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        stats = {
            'count': len(self.df[column]),
            'mean': self.df[column].mean(),
            'median': self.df[column].median(),
            'std': self.df[column].std(),
            'min': self.df[column].min(),
            'max': self.df[column].max(),
            'q25': self.df[column].quantile(0.25),
            'q75': self.df[column].quantile(0.75)
        }
        
        print(f"\n📊 Statistics for {column}:")
        print(f"  Count:   {stats['count']}")
        print(f"  Mean:    {stats['mean']:.2f}")
        print(f"  Median:  {stats['median']:.2f}")
        print(f"  Std Dev: {stats['std']:.2f}")
        print(f"  Min:     {stats['min']:.2f}")
        print(f"  Max:     {stats['max']:.2f}")
        print(f"  Q1:      {stats['q25']:.2f}")
        print(f"  Q3:      {stats['q75']:.2f}")
        
        return stats
    
    def add_calculated_column(
        self,
        new_column: str,
        calculation: str,
        columns: List[str]
    ) -> pd.DataFrame:
        """
        Add a new calculated column.
        
        zyBooks Concept: Derive new variables from existing ones.
        
        # FlameLang Syntax:
        # 🔥 create column total_score {
        #     formula: midterm + final + homework
        # }
        
        Args:
            new_column: Name for new column
            calculation: Operation (add, subtract, multiply, divide, mean)
            columns: Columns to use in calculation
            
        Returns:
            DataFrame with new column
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded. Use load_csv() first.")
        
        if calculation == 'add':
            self.df[new_column] = self.df[columns].sum(axis=1)
        elif calculation == 'subtract':
            self.df[new_column] = self.df[columns[0]] - self.df[columns[1]]
        elif calculation == 'multiply':
            self.df[new_column] = self.df[columns].prod(axis=1)
        elif calculation == 'divide':
            self.df[new_column] = self.df[columns[0]] / self.df[columns[1]]
        elif calculation == 'mean':
            self.df[new_column] = self.df[columns].mean(axis=1)
        else:
            raise ValueError(f"Invalid calculation: {calculation}")
        
        print(f"✅ Added column '{new_column}' = {calculation}({', '.join(columns)})")
        
        return self.df
    
    def export_to_csv(self, output_path: str) -> None:
        """
        Export DataFrame to CSV file.
        
        Args:
            output_path: Path to save CSV file
        """
        if self.df is None:
            raise ValueError("No DataFrame loaded.")
        
        self.df.to_csv(output_path, index=False)
        print(f"✅ Exported to {output_path}")


def create_sample_datasets():
    """
    Create sample datasets for learning and testing.
    
    zyBooks Alignment: Provides realistic data matching course examples.
    """
    datasets_dir = Path(__file__).parent / "sample_data"
    datasets_dir.mkdir(exist_ok=True)
    
    # Sample 1: Temperature data (zyBooks example)
    temperature_data = pd.DataFrame({
        'City': ['Phoenix', 'Las Vegas', 'Tucson', 'Albuquerque', 'El Paso'] * 4,
        'Month': ['June'] * 5 + ['July'] * 5 + ['August'] * 5 + ['September'] * 5,
        'Temperature': [104, 106, 100, 92, 96,  # June
                       107, 109, 103, 94, 98,  # July
                       105, 107, 101, 92, 96,  # August
                       99, 102, 95, 85, 90]    # September
    })
    temperature_data.to_csv(datasets_dir / "temperature.csv", index=False)
    
    # Sample 2: Workforce data
    workforce_data = pd.DataFrame({
        'Department': ['Sales', 'Engineering', 'Marketing', 'HR', 'Finance',
                      'Sales', 'Engineering', 'Marketing', 'HR', 'Finance'] * 2,
        'Employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve',
                    'Frank', 'Grace', 'Henry', 'Iris', 'Jack'] * 2,
        'Years_Experience': [5, 8, 3, 6, 7, 2, 10, 4, 5, 9,
                            6, 9, 4, 7, 8, 3, 11, 5, 6, 10],
        'Salary': [65000, 95000, 58000, 62000, 75000,
                  52000, 110000, 60000, 64000, 85000,
                  68000, 98000, 61000, 65000, 78000,
                  55000, 115000, 63000, 67000, 88000]
    })
    workforce_data = workforce_data.head(10)  # Keep unique employees
    workforce_data.to_csv(datasets_dir / "workforce.csv", index=False)
    
    # Sample 3: Student performance data
    student_data = pd.DataFrame({
        'Student_ID': range(1, 51),
        'Major': np.random.choice(['Math', 'CS', 'Stats', 'Data Science'], 50),
        'Midterm': np.random.normal(75, 10, 50),
        'Final': np.random.normal(78, 12, 50),
        'Homework': np.random.normal(85, 8, 50),
        'Participation': np.random.choice([0, 1], 50, p=[0.2, 0.8])
    })
    student_data.to_csv(datasets_dir / "students.csv", index=False)
    
    print(f"✅ Created sample datasets in {datasets_dir}/")
    return datasets_dir


def demo_dataframe_operations():
    """
    Demonstrate DataFrame operations with sample data.
    """
    print("\n" + "=" * 70)
    print("PANDAS DATAFRAME OPERATIONS DEMO")
    print("=" * 70)
    
    # Create sample datasets
    datasets_dir = create_sample_datasets()
    
    # Load and demonstrate operations
    df_ops = DataFrameOperations()
    
    print("\n1. LOADING DATA")
    print("-" * 70)
    df_ops.load_csv(datasets_dir / "students.csv")
    print(df_ops.df.head())
    
    print("\n2. FILTERING DATA")
    print("-" * 70)
    high_performers = df_ops.filter_rows('Midterm', '>=', 80)
    print(high_performers.head())
    
    print("\n3. SELECTING COLUMNS")
    print("-" * 70)
    selected = df_ops.select_columns(['Major', 'Midterm', 'Final'])
    print(selected.head())
    
    print("\n4. GROUPING AND AGGREGATION")
    print("-" * 70)
    by_major = df_ops.group_by('Major', 'Midterm', 'mean')
    print(by_major)
    
    print("\n5. CALCULATING STATISTICS")
    print("-" * 70)
    stats = df_ops.calculate_statistics('Midterm')
    
    print("\n6. ADDING CALCULATED COLUMN")
    print("-" * 70)
    df_ops.add_calculated_column('Average', 'mean', ['Midterm', 'Final', 'Homework'])
    print(df_ops.df[['Student_ID', 'Midterm', 'Final', 'Homework', 'Average']].head())
    
    print("\n7. SORTING DATA")
    print("-" * 70)
    top_students = df_ops.sort_by('Average', ascending=False)
    print(top_students[['Student_ID', 'Major', 'Average']].head(10))
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_dataframe_operations()
