"""
Subsetting Data

Subsetting is the process of retrieving parts of a data frame. This module
demonstrates various ways to select columns and rows from a DataFrame.
"""

import pandas as pd
import seaborn as sns


def load_titanic():
    """Load or create titanic dataset."""
    try:
        return sns.load_dataset("titanic")
    except:
        # Create sample data if seaborn is not available
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


def selecting_columns():
    """
    Demonstrate selecting columns from a DataFrame.
    Python-Function 1.4.1: Selecting columns and rows.
    """
    titanic = load_titanic()
    
    print("=" * 60)
    print("SELECTING COLUMNS")
    print("=" * 60)
    
    print("\n1. Select a single column (returns Series):")
    print("   Command: titanic['sex']")
    print(titanic['sex'].head())
    print(f"   Type: {type(titanic['sex'])}")
    
    print("\n2. Alternative syntax for single column:")
    print("   Command: titanic.sex")
    print(titanic.sex.head())
    
    print("\n3. Select multiple columns (returns DataFrame):")
    print("   Command: titanic[['sex', 'survived']]")
    result = titanic[['sex', 'survived']]
    print(result.head())
    print(f"   Type: {type(result)}")
    
    return titanic


def selecting_rows():
    """
    Demonstrate selecting rows from a DataFrame.
    """
    titanic = load_titanic()
    
    print("\n" + "=" * 60)
    print("SELECTING ROWS")
    print("=" * 60)
    
    print("\n1. Select rows by position (first 5 rows):")
    print("   Command: titanic[0:5]")
    result = titanic[0:5]
    print(result)
    
    print("\n2. Select rows where a column has a specific value:")
    print("   Command: titanic[titanic.pclass == 3]")
    result = titanic[titanic.pclass == 3]
    print(f"   Result: {len(result)} rows where pclass == 3")
    print(result.head())
    
    print("\n3. Select rows using comparison operators:")
    print("   Command: titanic[titanic.fare < 10.0]")
    result = titanic[titanic.fare < 10.0]
    print(f"   Result: {len(result)} rows where fare < 10.0")
    print(result.head())
    
    return titanic


def loc_and_iloc_examples():
    """
    Demonstrate loc() and iloc() methods.
    Python-Function 1.4.2: loc() and iloc().
    """
    titanic = load_titanic()
    
    print("\n" + "=" * 60)
    print("LOC() AND ILOC() METHODS")
    print("=" * 60)
    
    print("\n1. loc() - Select rows and columns by labels:")
    print("   Command: titanic.loc[0:5, ['pclass', 'age']]")
    result = titanic.loc[0:5, ['pclass', 'age']]
    print(result)
    
    print("\n2. iloc() - Select rows and columns by position:")
    print("   Command: titanic.iloc[0:5, 0:5]")
    result = titanic.iloc[0:5, 0:5]
    print(result)
    
    print("\n3. loc() with specific rows and all columns:")
    print("   Command: titanic.loc[0:2, :]")
    result = titanic.loc[0:2, :]
    print(result)
    
    print("\n4. iloc() with all rows and specific columns:")
    print("   Command: titanic.iloc[:, 0:3]")
    result = titanic.iloc[:, 0:3]
    print(result.head())
    
    return titanic


def participation_activity_1_4_4():
    """
    Participation Activity 1.4.4: Subsetting data questions.
    """
    titanic = load_titanic()
    
    print("\n" + "=" * 60)
    print("PARTICIPATION ACTIVITY 1.4.4: SUBSETTING DATA")
    print("=" * 60)
    
    print("\n1. Select 'age' column and return a DataFrame:")
    print("   Command: titanic[['age']]")
    result = titanic[['age']]
    print(f"   Type: {type(result)}")
    print(result.head())
    
    print("\n2. Command titanic[['age', 'fare', 'alive']] returns:")
    result = titanic[['age', 'fare', 'alive']]
    print(f"   Type: {type(result)} (DataFrame)")
    print(result.head())
    
    print("\n3. First 10 rows of the titanic DataFrame:")
    print("   Command: titanic[0:10] or titanic.head(10)")
    result = titanic[0:10]
    print(result)
    
    print("\n4. First 10 rows with columns age, fare, and class:")
    print("   Command: titanic.loc[0:9, ['age', 'fare', 'class']]")
    result = titanic.loc[0:9, ['age', 'fare', 'class']]
    print(result)
    
    print("\n5. Rows where age equals 22:")
    print("   Command: titanic[titanic.age == 22]")
    result = titanic[titanic.age == 22]
    print(f"   Found {len(result)} rows where age == 22")
    print(result.head())
    
    return titanic


def advanced_subsetting_examples():
    """
    Additional subsetting examples with multiple conditions.
    """
    titanic = load_titanic()
    
    print("\n" + "=" * 60)
    print("ADVANCED SUBSETTING EXAMPLES")
    print("=" * 60)
    
    print("\n1. Multiple conditions with & (and):")
    print("   Command: titanic[(titanic.pclass == 3) & (titanic.fare < 10)]")
    result = titanic[(titanic.pclass == 3) & (titanic.fare < 10)]
    print(f"   Result: {len(result)} rows")
    print(result.head())
    
    print("\n2. Multiple conditions with | (or):")
    print("   Command: titanic[(titanic.pclass == 1) | (titanic.pclass == 2)]")
    result = titanic[(titanic.pclass == 1) | (titanic.pclass == 2)]
    print(f"   Result: {len(result)} rows")
    print(result.head())
    
    print("\n3. Using isin() for multiple values:")
    print("   Command: titanic[titanic.embarked.isin(['C', 'Q'])]")
    result = titanic[titanic.embarked.isin(['C', 'Q'])]
    print(f"   Result: {len(result)} rows")
    print(result.head())
    
    print("\n4. Negation with ~ (not):")
    print("   Command: titanic[~(titanic.sex == 'male')]")
    result = titanic[~(titanic.sex == 'male')]
    print(f"   Result: {len(result)} rows (females)")
    print(result.head())
    
    return titanic


if __name__ == "__main__":
    # Run all demonstrations
    selecting_columns()
    selecting_rows()
    loc_and_iloc_examples()
    participation_activity_1_4_4()
    advanced_subsetting_examples()
