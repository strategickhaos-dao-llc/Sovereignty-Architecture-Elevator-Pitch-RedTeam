"""
Reshaping Data

This module demonstrates converting data frames between long form and wide form
using pivot() and melt() operations.
"""

import pandas as pd


def create_test_scores_long():
    """
    Create the test scores data frame in long form from participation activity 1.4.5.
    """
    data = {
        'Date': ['2018-01-03', '2018-01-03', '2018-01-03', 
                 '2018-01-13', '2018-01-13', '2018-01-13'],
        'Student': ['Michael', 'Arushi', 'Roberta', 
                    'Michael', 'Arushi', 'Roberta'],
        'Score': [90, 98, 92, 90, 98, 92]
    }
    return pd.DataFrame(data)


def create_test_scores_wide():
    """
    Create the test scores data frame in wide form from participation activity 1.4.6.
    """
    data = {
        'Student': ['Michael', 'Arushi', 'Roberta'],
        'SAT': [1480, 1520, 1460],
        'ACT': [34, 32, 32]
    }
    return pd.DataFrame(data)


def demonstrate_long_vs_wide():
    """
    Explain the difference between long form and wide form data frames.
    """
    print("=" * 60)
    print("LONG FORM VS WIDE FORM")
    print("=" * 60)
    
    print("\nLONG FORM:")
    print("- Each column is a variable")
    print("- Each row gives non-repeated data")
    print("- Also called: unstacked or record form")
    
    df_long = create_test_scores_long()
    print("\nExample (Test Scores - Long Form):")
    print(df_long)
    
    print("\n" + "-" * 60)
    print("\nWIDE FORM:")
    print("- Each data variable is in a different column")
    print("- Also called: stacked form")
    
    df_wide = create_test_scores_wide()
    print("\nExample (Test Scores - Wide Form):")
    print(df_wide)


def demonstrate_pivoting():
    """
    Demonstrate pivoting: converting from long form to wide form.
    Participation Activity 1.4.5.
    """
    print("\n" + "=" * 60)
    print("PIVOTING: LONG FORM → WIDE FORM")
    print("=" * 60)
    
    df_long = create_test_scores_long()
    print("\nOriginal Data (Long Form):")
    print(df_long)
    
    print("\nPivot Command:")
    print("pd.pivot(df, index='Date', columns='Student', values='Score')")
    
    df_wide = pd.pivot(df_long, index='Date', columns='Student', values='Score')
    print("\nResult (Wide Form):")
    print(df_wide)
    
    print("\nExplanation:")
    print("- Index labels: unique values of 'Date' column")
    print("- Column labels: unique values of 'Student' column")
    print("- Values: from the 'Score' column")
    
    return df_wide


def demonstrate_melting():
    """
    Demonstrate melting: converting from wide form to long form.
    Participation Activity 1.4.6 and Python-Function 1.4.3.
    """
    print("\n" + "=" * 60)
    print("MELTING: WIDE FORM → LONG FORM")
    print("=" * 60)
    
    df_wide = create_test_scores_wide()
    print("\nOriginal Data (Wide Form):")
    print(df_wide)
    
    print("\nMelt Command:")
    print("pd.melt(df, id_vars='Student', var_name='Test',")
    print("        value_vars=['SAT', 'ACT'], value_name='Scores')")
    
    df_long = pd.melt(df_wide, 
                      id_vars='Student', 
                      var_name='Test',
                      value_vars=['SAT', 'ACT'], 
                      value_name='Scores')
    
    print("\nResult (Long Form):")
    print(df_long)
    
    print("\nExplanation:")
    print("- id_vars: column(s) to use as identifier variable")
    print("- var_name: column label for the variable column ('Test')")
    print("- value_vars: columns to unpivot (['SAT', 'ACT'])")
    print("- value_name: column label for the value column ('Scores')")
    
    return df_long


def participation_activity_1_4_7():
    """
    Participation Activity 1.4.7: pivot() and melt() questions.
    """
    print("\n" + "=" * 60)
    print("PARTICIPATION ACTIVITY 1.4.7")
    print("=" * 60)
    
    # Question 1: Pivot example
    print("\n1. Reshape data frame using pivot():")
    df1 = pd.DataFrame({
        'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
        'baz': [1, 2, 3, 4, 5, 6],
        'foo': ['one', 'one', 'one', 'two', 'two', 'two']
    })
    print("\nOriginal DataFrame:")
    print(df1)
    
    print("\nCommand: pd.pivot(df, index='bar', columns='foo', values='baz')")
    result1 = pd.pivot(df1, index='bar', columns='foo', values='baz')
    print("\nResult:")
    print(result1)
    
    # Question 2: Melt example
    print("\n" + "-" * 60)
    print("\n2. Reshape data frame using melt():")
    df2 = pd.DataFrame({
        'A': ['a', 'b', 'c'],
        'B': [1, 3, 5],
        'C': [2, 4, 6]
    })
    print("\nOriginal DataFrame:")
    print(df2)
    
    print("\nCommand: pd.melt(df, id_vars='A', value_vars='C')")
    result2 = pd.melt(df2, id_vars='A', value_vars='C')
    print("\nResult:")
    print(result2)
    
    # Question 3: Adding value_name parameter
    print("\n" + "-" * 60)
    print("\n3. To use 'Counts' as the label for the value column:")
    print("   Add parameter: value_name='Counts'")
    print("\nFull command:")
    print("pd.melt(df, id_vars='A', value_vars='C', value_name='Counts')")
    result3 = pd.melt(df2, id_vars='A', value_vars='C', value_name='Counts')
    print("\nResult:")
    print(result3)


def advanced_reshaping_examples():
    """
    Additional reshaping examples with more complex scenarios.
    """
    print("\n" + "=" * 60)
    print("ADVANCED RESHAPING EXAMPLES")
    print("=" * 60)
    
    # Multi-index pivot
    print("\n1. Pivot with multiple values:")
    df = pd.DataFrame({
        'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
        'city': ['NYC', 'LA', 'NYC', 'LA'],
        'temp': [32, 65, 35, 68],
        'humidity': [60, 45, 65, 40]
    })
    print("\nOriginal:")
    print(df)
    
    # Using pivot_table for aggregation
    print("\nUsing pivot_table (handles duplicate entries):")
    result = df.pivot_table(index='date', columns='city', values='temp')
    print(result)
    
    # Melt multiple columns
    print("\n" + "-" * 60)
    print("\n2. Melt with multiple id_vars:")
    df2 = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Age': [25, 30],
        'Math': [90, 85],
        'Science': [95, 88]
    })
    print("\nOriginal:")
    print(df2)
    
    result = pd.melt(df2, 
                     id_vars=['Name', 'Age'], 
                     value_vars=['Math', 'Science'],
                     var_name='Subject',
                     value_name='Grade')
    print("\nMelted:")
    print(result)


if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_long_vs_wide()
    demonstrate_pivoting()
    demonstrate_melting()
    participation_activity_1_4_7()
    advanced_reshaping_examples()
