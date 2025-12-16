"""
Test script for line charts tutorial
Verifies that all examples generate correctly
"""

import os
import sys

def test_chart_files_exist():
    """Test that all expected chart files were generated"""
    expected_files = [
        'apple_stock_chart.png',
        'apple_stock_trendline.png',
        'google_stock_chart.png',
        'temperature_comparison.png',
        'three_cities_temperature.png',
        'unemployment_rate.png',
        'categorical_comparison.png',
        'labeling_importance.png'
    ]
    
    print("Testing chart file generation...")
    all_exist = True
    
    for filename in expected_files:
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({file_size:,} bytes)")
        else:
            print(f"  ✗ {filename} - NOT FOUND")
            all_exist = False
    
    return all_exist


def test_import_tutorial():
    """Test that the tutorial module can be imported"""
    try:
        print("\nTesting module import...")
        import line_charts_tutorial
        print("  ✓ line_charts_tutorial module imports successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import: {e}")
        return False


def test_functions_exist():
    """Test that all expected functions exist in the tutorial"""
    try:
        print("\nTesting function definitions...")
        import line_charts_tutorial
        
        expected_functions = [
            'example_1_apple_stock_prices',
            'example_2_apple_with_trendline',
            'example_3_google_stock_prices',
            'example_4_multiple_datasets_temperature',
            'example_5_three_cities_temperature',
            'example_6_unemployment_rate',
            'example_7_inappropriate_categorical',
            'example_8_missing_labels',
            'run_all_examples'
        ]
        
        all_exist = True
        for func_name in expected_functions:
            if hasattr(line_charts_tutorial, func_name):
                print(f"  ✓ {func_name}()")
            else:
                print(f"  ✗ {func_name}() - NOT FOUND")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available"""
    print("\nTesting dependencies...")
    all_available = True
    
    try:
        import matplotlib
        print(f"  ✓ matplotlib {matplotlib.__version__}")
    except ImportError:
        print("  ✗ matplotlib - NOT INSTALLED")
        all_available = False
    
    try:
        import numpy
        print(f"  ✓ numpy {numpy.__version__}")
    except ImportError:
        print("  ✗ numpy - NOT INSTALLED")
        all_available = False
    
    try:
        import yfinance
        print(f"  ✓ yfinance {yfinance.__version__} (optional)")
    except ImportError:
        print("  ℹ yfinance - NOT INSTALLED (optional for real data examples)")
    
    return all_available


def run_all_tests():
    """Run all tests and report results"""
    print("="*70)
    print("LINE CHARTS TUTORIAL - TEST SUITE")
    print("="*70)
    
    results = {
        'Dependencies': test_dependencies(),
        'Module Import': test_import_tutorial(),
        'Function Definitions': test_functions_exist(),
        'Chart Files': test_chart_files_exist()
    }
    
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*70)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("="*70)
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
