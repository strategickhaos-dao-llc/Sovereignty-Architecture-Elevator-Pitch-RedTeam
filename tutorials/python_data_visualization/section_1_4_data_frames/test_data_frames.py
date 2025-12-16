#!/usr/bin/env python3
"""
Test Suite for Section 1.4: Data Frames Tutorial

This module tests all functionality in the data frames tutorial to ensure
examples work correctly.

Usage:
    python test_data_frames.py
    python -m pytest test_data_frames.py  (if pytest is installed)
"""

import pandas as pd
import sys
import traceback


def test_data_frames_intro():
    """Test data_frames_intro module."""
    print("Testing data_frames_intro...")
    try:
        from data_frames_intro import (
            create_sample_tips_dataframe,
            create_state_income_dataframe,
            demonstrate_dataframe_components,
            demonstrate_state_income
        )
        
        # Test creating DataFrames
        df_tips = create_sample_tips_dataframe()
        assert isinstance(df_tips, pd.DataFrame), "Should return DataFrame"
        assert len(df_tips) == 5, "Should have 5 rows"
        assert len(df_tips.columns) == 7, "Should have 7 columns"
        
        df_income = create_state_income_dataframe()
        assert isinstance(df_income, pd.DataFrame), "Should return DataFrame"
        assert 'State' in df_income.columns, "Should have State column"
        assert 'GEOID' in df_income.columns, "Should have GEOID column"
        
        # Test demonstrations (should not raise exceptions)
        demonstrate_dataframe_components()
        demonstrate_state_income()
        
        print("  ✓ data_frames_intro tests passed")
        return True
    except Exception as e:
        print(f"  ✗ data_frames_intro tests failed: {e}")
        traceback.print_exc()
        return False


def test_pandas_examples():
    """Test pandas_examples module."""
    print("Testing pandas_examples...")
    try:
        from pandas_examples import (
            load_titanic_dataset,
            demonstrate_dataframe_attributes,
            demonstrate_dataframe_methods,
            example_1_4_1_titanic_dataset,
            participation_activity_1_4_3
        )
        
        # Test loading titanic
        titanic = load_titanic_dataset()
        assert isinstance(titanic, pd.DataFrame), "Should return DataFrame"
        assert 'survived' in titanic.columns, "Should have survived column"
        assert 'age' in titanic.columns, "Should have age column"
        
        # Test demonstrations (should not raise exceptions)
        demonstrate_dataframe_attributes()
        demonstrate_dataframe_methods()
        example_1_4_1_titanic_dataset()
        participation_activity_1_4_3()
        
        print("  ✓ pandas_examples tests passed")
        return True
    except Exception as e:
        print(f"  ✗ pandas_examples tests failed: {e}")
        traceback.print_exc()
        return False


def test_subsetting_data():
    """Test subsetting_data module."""
    print("Testing subsetting_data...")
    try:
        from subsetting_data import (
            load_titanic,
            selecting_columns,
            selecting_rows,
            loc_and_iloc_examples,
            participation_activity_1_4_4
        )
        
        # Test loading
        titanic = load_titanic()
        assert isinstance(titanic, pd.DataFrame), "Should return DataFrame"
        
        # Test column selection
        col = titanic['sex']
        assert isinstance(col, pd.Series), "Single column should return Series"
        
        cols = titanic[['sex', 'age']]
        assert isinstance(cols, pd.DataFrame), "Multiple columns should return DataFrame"
        
        # Test row selection
        rows = titanic[0:5]
        assert len(rows) == 5, "Should select 5 rows"
        
        # Test filtering
        filtered = titanic[titanic['age'] > 30]
        # Check only non-NaN values (NaN comparisons return False)
        non_nan_ages = filtered['age'].dropna()
        assert all(non_nan_ages > 30), "All non-NaN ages should be > 30"
        
        # Test demonstrations
        selecting_columns()
        selecting_rows()
        loc_and_iloc_examples()
        participation_activity_1_4_4()
        
        print("  ✓ subsetting_data tests passed")
        return True
    except Exception as e:
        print(f"  ✗ subsetting_data tests failed: {e}")
        traceback.print_exc()
        return False


def test_reshaping_data():
    """Test reshaping_data module."""
    print("Testing reshaping_data...")
    try:
        from reshaping_data import (
            create_test_scores_long,
            create_test_scores_wide,
            demonstrate_pivoting,
            demonstrate_melting,
            participation_activity_1_4_7
        )
        
        # Test creating DataFrames
        df_long = create_test_scores_long()
        assert isinstance(df_long, pd.DataFrame), "Should return DataFrame"
        assert 'Date' in df_long.columns, "Should have Date column"
        assert 'Student' in df_long.columns, "Should have Student column"
        assert 'Score' in df_long.columns, "Should have Score column"
        
        df_wide = create_test_scores_wide()
        assert isinstance(df_wide, pd.DataFrame), "Should return DataFrame"
        assert 'Student' in df_wide.columns, "Should have Student column"
        assert 'SAT' in df_wide.columns, "Should have SAT column"
        assert 'ACT' in df_wide.columns, "Should have ACT column"
        
        # Test pivoting
        pivoted = pd.pivot(df_long, index='Date', columns='Student', values='Score')
        assert isinstance(pivoted, pd.DataFrame), "Pivot should return DataFrame"
        assert 'Michael' in pivoted.columns, "Should have Michael column"
        
        # Test melting
        melted = pd.melt(df_wide, id_vars='Student', value_vars=['SAT', 'ACT'])
        assert isinstance(melted, pd.DataFrame), "Melt should return DataFrame"
        assert len(melted) == 6, "Should have 6 rows (3 students × 2 tests)"
        
        # Test demonstrations
        demonstrate_pivoting()
        demonstrate_melting()
        participation_activity_1_4_7()
        
        print("  ✓ reshaping_data tests passed")
        return True
    except Exception as e:
        print(f"  ✗ reshaping_data tests failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("RUNNING TEST SUITE FOR SECTION 1.4: DATA FRAMES")
    print("=" * 70 + "\n")
    
    results = []
    results.append(("data_frames_intro", test_data_frames_intro()))
    results.append(("pandas_examples", test_pandas_examples()))
    results.append(("subsetting_data", test_subsetting_data()))
    results.append(("reshaping_data", test_reshaping_data()))
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for module, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{module:25s} {status}")
    
    print("-" * 70)
    print(f"Results: {passed}/{total} test suites passed")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 All tests passed! The tutorial module is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
