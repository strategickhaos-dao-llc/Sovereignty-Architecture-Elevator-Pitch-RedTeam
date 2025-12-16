#!/usr/bin/env python3
"""
Complete Tutorial Runner for Section 1.4: Data Frames

This script runs all tutorial demonstrations in sequence, providing a complete
walkthrough of data frame concepts from the zyBooks curriculum.

Usage:
    python complete_tutorial.py
"""

import sys
from data_frames_intro import (
    demonstrate_dataframe_components,
    demonstrate_state_income
)
from pandas_examples import (
    demonstrate_importing_files,
    demonstrate_dataframe_attributes,
    demonstrate_dataframe_methods,
    example_1_4_1_titanic_dataset,
    participation_activity_1_4_3
)
from subsetting_data import (
    selecting_columns,
    selecting_rows,
    loc_and_iloc_examples,
    participation_activity_1_4_4,
    advanced_subsetting_examples
)
from reshaping_data import (
    demonstrate_long_vs_wide,
    demonstrate_pivoting,
    demonstrate_melting,
    participation_activity_1_4_7,
    advanced_reshaping_examples
)


def print_section_header(title, section_num=None):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    if section_num:
        print(f"SECTION {section_num}: {title}")
    else:
        print(title)
    print("=" * 70 + "\n")


def main():
    """Run the complete tutorial."""
    print_section_header("SECTION 1.4: DATA FRAMES - COMPLETE TUTORIAL", "1.4")
    print("Welcome to the comprehensive Data Frames tutorial!")
    print("This tutorial covers all concepts from zyBooks Section 1.4.")
    print("\nPress Enter to begin, or Ctrl+C to exit...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nTutorial cancelled.")
        sys.exit(0)
    
    # Part 1: Introduction to Data Frames
    print_section_header("PART 1: INTRODUCTION TO DATA FRAMES", "1.4.1-1.4.2")
    print("Learning about DataFrame components: index, columns, and values")
    input("\nPress Enter to continue...")
    
    demonstrate_dataframe_components()
    demonstrate_state_income()
    
    input("\n\nPress Enter to continue to Part 2...")
    
    # Part 2: pandas Library
    print_section_header("PART 2: PANDAS LIBRARY", "1.4.3")
    print("Exploring pandas DataFrame attributes and methods")
    input("\nPress Enter to continue...")
    
    demonstrate_importing_files()
    demonstrate_dataframe_attributes()
    demonstrate_dataframe_methods()
    example_1_4_1_titanic_dataset()
    participation_activity_1_4_3()
    
    input("\n\nPress Enter to continue to Part 3...")
    
    # Part 3: Subsetting Data
    print_section_header("PART 3: SUBSETTING DATA", "1.4.4")
    print("Learning to select and filter data from DataFrames")
    input("\nPress Enter to continue...")
    
    selecting_columns()
    selecting_rows()
    loc_and_iloc_examples()
    participation_activity_1_4_4()
    advanced_subsetting_examples()
    
    input("\n\nPress Enter to continue to Part 4...")
    
    # Part 4: Reshaping Data
    print_section_header("PART 4: RESHAPING DATA", "1.4.5-1.4.7")
    print("Converting between long form and wide form using pivot and melt")
    input("\nPress Enter to continue...")
    
    demonstrate_long_vs_wide()
    demonstrate_pivoting()
    demonstrate_melting()
    participation_activity_1_4_7()
    advanced_reshaping_examples()
    
    # Summary
    print_section_header("TUTORIAL COMPLETE!")
    print("🎉 Congratulations! You've completed Section 1.4: Data Frames")
    print("\nYou've learned:")
    print("  ✓ DataFrame structure (index, columns, values)")
    print("  ✓ pandas library attributes and methods")
    print("  ✓ Subsetting data with loc[], iloc[], and conditions")
    print("  ✓ Reshaping data with pivot() and melt()")
    print("\nNext steps:")
    print("  • Practice with your own datasets")
    print("  • Try the exercises in each module")
    print("  • Explore the pandas documentation")
    print("  • Move on to Section 1.5: Bar charts")
    print("\nThank you for using this tutorial!")


if __name__ == "__main__":
    main()
