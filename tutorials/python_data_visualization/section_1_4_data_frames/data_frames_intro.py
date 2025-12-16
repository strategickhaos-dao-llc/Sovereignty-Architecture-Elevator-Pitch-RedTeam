"""
Introduction to Data Frames

A data frame (DataFrame) is a two-dimensional tabular data structure with 
labeled columns and rows. This module demonstrates the basic components 
and structure of data frames.
"""

import pandas as pd


def create_sample_tips_dataframe():
    """
    Create a sample tips data frame as shown in the tutorial.
    
    Returns:
        pd.DataFrame: Sample tips data with columns: total_bill, tip, sex, 
                      smoker, day, time, size
    """
    data = {
        'total_bill': [16.99, 10.34, 21.01, 23.68, 24.59],
        'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
        'sex': ['Female', 'Male', 'Male', 'Male', 'Female'],
        'smoker': ['No', 'No', 'No', 'No', 'No'],
        'day': ['Sun', 'Sun', 'Sun', 'Sun', 'Sun'],
        'time': ['Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner'],
        'size': [2, 3, 3, 2, 4]
    }
    return pd.DataFrame(data)


def demonstrate_dataframe_components():
    """
    Demonstrate the three main components of a DataFrame:
    1. Index (row labels)
    2. Columns (column labels)
    3. Values (the data)
    """
    df = create_sample_tips_dataframe()
    
    print("=" * 60)
    print("DATA FRAME COMPONENTS DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. The Complete Data Frame:")
    print(df)
    
    print("\n2. Columns (column labels):")
    print(f"   {list(df.columns)}")
    print(f"   Example column label: 'tip'")
    
    print("\n3. Index (row labels):")
    print(f"   {list(df.index)}")
    print(f"   Example index label: 1")
    
    print("\n4. Values (the data):")
    print(f"   Data type of 'size' column: {df['size'].dtype}")
    print(f"   Sample values from 'size': {df['size'].tolist()}")
    
    return df


def create_state_income_dataframe():
    """
    Create the state income data frame from participation activity 1.4.2.
    
    Returns:
        pd.DataFrame: State income data for 2005 and 2006
    """
    data = {
        'State': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        'GEOID': ['04000US01', '04000US02', '04000US03', '04000US04', '04000US05'],
        '2005': [37150, 55891, 45245, 36658, 51755],
        '2006': [37952, 56418, 46657, 37057, 55319]
    }
    return pd.DataFrame(data)


def demonstrate_state_income():
    """
    Demonstrate the state income data frame and answer tutorial questions.
    """
    df = create_state_income_dataframe()
    
    print("\n" + "=" * 60)
    print("STATE INCOME DATA FRAME")
    print("=" * 60)
    print(df)
    
    print("\n1. Column labels include: 'State', 'GEOID', '2005', '2006'")
    print("2. Index labels are: 0, 1, 2, 3, 4")
    print(f"3. Data type for GEOID: {df['GEOID'].dtype} (object = string in pandas)")
    
    return df


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_dataframe_components()
    demonstrate_state_income()
