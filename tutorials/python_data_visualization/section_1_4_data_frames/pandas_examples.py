"""
pandas Library Examples

This module demonstrates the use of pandas library for working with DataFrames,
including importing data, DataFrame attributes, and DataFrame methods.
"""

import pandas as pd
import seaborn as sns


def demonstrate_importing_files():
    """
    Demonstrate different ways to import files as DataFrame objects.
    
    Note: This is a reference implementation showing the syntax.
    Actual files would be needed to run these commands.
    """
    print("=" * 60)
    print("IMPORTING FILES AS DATAFRAME OBJECTS")
    print("=" * 60)
    
    print("\n1. Import CSV file:")
    print("   data_frame1 = pd.read_csv('file.csv')")
    
    print("\n2. Import text file with space separator:")
    print("   data_frame2 = pd.read_csv('file.txt', sep=' ', header=None)")
    
    print("\n3. Import Excel file:")
    print("   data_frame3 = pd.read_excel('file.xlsx', sheetname='Sheet1')")


def load_titanic_dataset():
    """
    Load the Titanic dataset from seaborn package.
    
    Returns:
        pd.DataFrame: Titanic dataset
    """
    try:
        titanic = sns.load_dataset("titanic")
        return titanic
    except Exception as e:
        print(f"Error loading titanic dataset: {e}")
        print("Creating a sample dataset instead...")
        # Create a small sample if seaborn data is not available
        return create_sample_titanic()


def create_sample_titanic():
    """Create a small sample of titanic data for demonstration."""
    data = {
        'survived': [0, 1, 1, 1, 0],
        'pclass': [3, 1, 3, 1, 3],
        'sex': ['male', 'female', 'female', 'female', 'male'],
        'age': [22.0, 38.0, 26.0, 35.0, 35.0],
        'sibsp': [1, 1, 0, 1, 0],
        'parch': [0, 0, 0, 0, 0],
        'fare': [7.25, 71.28, 7.92, 53.10, 8.05],
        'embarked': ['S', 'C', 'S', 'S', 'S'],
        'class': ['Third', 'First', 'Third', 'First', 'Third'],
        'who': ['man', 'woman', 'woman', 'woman', 'man'],
        'adult_male': [True, False, False, False, True],
        'deck': [None, 'C', None, 'C', None],
        'embark_town': ['Southampton', 'Cherbourg', 'Southampton', 'Southampton', 'Southampton'],
        'alive': ['no', 'yes', 'yes', 'yes', 'no'],
        'alone': [False, False, True, False, True]
    }
    return pd.DataFrame(data)


def demonstrate_dataframe_attributes():
    """
    Demonstrate DataFrame attributes as shown in Table 1.4.1.
    """
    titanic = load_titanic_dataset()
    
    print("\n" + "=" * 60)
    print("DATAFRAME ATTRIBUTES (Table 1.4.1)")
    print("=" * 60)
    
    print("\n1. axes - Index and column labels:")
    print(f"   Axes: {titanic.axes}")
    
    print("\n2. columns - Column labels:")
    print(f"   Columns: {titanic.columns.tolist()}")
    
    print("\n3. dtypes - Data types of values in each column:")
    print(titanic.dtypes)
    
    print("\n4. index - Index labels:")
    print(f"   Index range: {titanic.index.min()} to {titanic.index.max()}")
    
    print("\n5. shape - Ordered pair (rows, columns):")
    print(f"   Shape: {titanic.shape}")
    print(f"   Number of rows: {titanic.shape[0]}")
    print(f"   Number of columns: {titanic.shape[1]}")
    
    print("\n6. size - Number of values in the DataFrame:")
    print(f"   Size: {titanic.size}")
    
    print("\n7. values - Values in the DataFrame:")
    print(f"   First few values:\n{titanic.values[:3]}")
    
    return titanic


def demonstrate_dataframe_methods():
    """
    Demonstrate DataFrame methods as shown in Table 1.4.2.
    """
    titanic = load_titanic_dataset()
    
    print("\n" + "=" * 60)
    print("DATAFRAME METHODS (Table 1.4.2)")
    print("=" * 60)
    
    print("\n1. describe() - Summary statistics for numerical columns:")
    print(titanic.describe())
    
    print("\n2. head() - First 5 rows in the DataFrame:")
    print(titanic.head())
    
    print("\n3. tail() - Last 5 rows in the DataFrame:")
    print(titanic.tail())
    
    print("\n4. min() - Minimum of values in numerical columns:")
    print(titanic.min(numeric_only=True))
    
    print("\n5. max() - Maximum of values in numerical columns:")
    print(titanic.max(numeric_only=True))
    
    print("\n6. mean() - Mean of values in numerical columns:")
    print(titanic.mean(numeric_only=True))
    
    print("\n7. median() - Median of values in numerical columns:")
    print(titanic.median(numeric_only=True))
    
    print("\n8. sample() - Random row:")
    print(titanic.sample())
    
    print("\n9. std() - Standard deviation of numerical columns:")
    print(titanic.std(numeric_only=True))
    
    return titanic


def example_1_4_1_titanic_dataset():
    """
    Example 1.4.1: Demonstrate finding number of rows, column names, 
    and data types in the Titanic dataset.
    """
    titanic = load_titanic_dataset()
    
    print("\n" + "=" * 60)
    print("EXAMPLE 1.4.1: TITANIC DATASET ANALYSIS")
    print("=" * 60)
    
    # Number of rows and columns
    print("\n1. Number of rows and columns:")
    print(f"   titanic.shape = {titanic.shape}")
    print(f"   Number of rows: {titanic.shape[0]}")
    print(f"   Number of columns: {titanic.shape[1]}")
    
    # Column names
    print("\n2. Column names:")
    print(f"   titanic.columns")
    print(f"   {titanic.columns.tolist()}")
    
    # Data types
    print("\n3. Data types of columns:")
    print("   titanic.dtypes")
    print(titanic.dtypes)
    
    print("\nNote: In pandas, int64 and float64 are the integer and float types.")
    print("      'object' is the string data type in pandas.")
    print("      'bool' represents boolean values (True/False or 1/0).")
    
    return titanic


def participation_activity_1_4_3():
    """
    Participation Activity 1.4.3: Answer questions about Titanic dataset.
    """
    titanic = load_titanic_dataset()
    
    print("\n" + "=" * 60)
    print("PARTICIPATION ACTIVITY 1.4.3")
    print("=" * 60)
    
    print("\n1. Mean of all numerical variables:")
    print("   Command: titanic.mean(numeric_only=True)")
    print(titanic.mean(numeric_only=True))
    
    print("\n2. Minimum values of all columns:")
    print("   Command: titanic.min(numeric_only=True)")
    print(titanic.min(numeric_only=True))
    
    print("\n3. Minimum age of all passengers:")
    age_min = titanic['age'].min()
    print(f"   Command: titanic['age'].min()")
    print(f"   Result: {age_min:.2f}")
    
    return titanic


if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_importing_files()
    demonstrate_dataframe_attributes()
    demonstrate_dataframe_methods()
    example_1_4_1_titanic_dataset()
    participation_activity_1_4_3()
