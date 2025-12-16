"""
Section 1.4: Data Frames Tutorial Module

This module provides examples and implementations of data frame concepts
including pandas DataFrames, subsetting, and reshaping data.
"""

__version__ = "1.0.0"
__author__ = "Sovereignty Architecture Tutorial Series"

# Import main demonstration functions
from .data_frames_intro import (
    create_sample_tips_dataframe,
    create_state_income_dataframe,
    demonstrate_dataframe_components,
    demonstrate_state_income
)

from .pandas_examples import (
    load_titanic_dataset,
    demonstrate_dataframe_attributes,
    demonstrate_dataframe_methods,
    example_1_4_1_titanic_dataset,
    participation_activity_1_4_3
)

from .subsetting_data import (
    selecting_columns,
    selecting_rows,
    loc_and_iloc_examples,
    participation_activity_1_4_4
)

from .reshaping_data import (
    create_test_scores_long,
    create_test_scores_wide,
    demonstrate_pivoting,
    demonstrate_melting,
    participation_activity_1_4_7
)

__all__ = [
    # data_frames_intro
    'create_sample_tips_dataframe',
    'create_state_income_dataframe',
    'demonstrate_dataframe_components',
    'demonstrate_state_income',
    # pandas_examples
    'load_titanic_dataset',
    'demonstrate_dataframe_attributes',
    'demonstrate_dataframe_methods',
    'example_1_4_1_titanic_dataset',
    'participation_activity_1_4_3',
    # subsetting_data
    'selecting_columns',
    'selecting_rows',
    'loc_and_iloc_examples',
    'participation_activity_1_4_4',
    # reshaping_data
    'create_test_scores_long',
    'create_test_scores_wide',
    'demonstrate_pivoting',
    'demonstrate_melting',
    'participation_activity_1_4_7',
]
