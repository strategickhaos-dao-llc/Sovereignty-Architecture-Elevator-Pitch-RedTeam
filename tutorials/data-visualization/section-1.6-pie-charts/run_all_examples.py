#!/usr/bin/env python3
"""
Run all pie chart examples from Section 1.6

This script executes all the example scripts in order and provides
a summary of the outputs.
"""

import subprocess
import sys
from pathlib import Path

def run_example(script_name):
    """Run a single example script and return success/failure."""
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print('='*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Run all examples in order."""
    examples = [
        ('example_1_6_1_basic_pie_chart.py', 'Basic Pie Charts - CDC Insurance Data'),
        ('example_1_6_2_exploded_pie_chart.py', 'Exploded Pie Chart - College Student Time Use'),
        ('example_1_6_3_too_many_slices.py', 'Misuse: Too Many Slices'),
        ('example_1_6_4_3d_pie_chart.py', 'Misuse: 3D Pie Charts'),
        ('example_1_6_5_poor_colors_exploded.py', 'Misuse: Poor Colors and Over-Explosion'),
    ]
    
    print("\n" + "="*70)
    print("SECTION 1.6: PIE CHARTS - RUNNING ALL EXAMPLES")
    print("="*70)
    
    results = []
    for script, description in examples:
        success = run_example(script)
        results.append((script, description, success))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for script, description, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {description}")
        print(f"  Script: {script}")
    
    # Check for generated images
    png_files = list(Path('.').glob('*.png'))
    print(f"\n{len(png_files)} chart images generated:")
    for png_file in sorted(png_files):
        print(f"  - {png_file.name}")
    
    success_count = sum(1 for _, _, success in results if success)
    total_count = len(results)
    
    print(f"\n{'='*70}")
    if success_count == total_count:
        print(f"✅ ALL EXAMPLES COMPLETED SUCCESSFULLY ({success_count}/{total_count})")
        return 0
    else:
        print(f"⚠️  SOME EXAMPLES FAILED ({success_count}/{total_count} succeeded)")
        return 1

if __name__ == '__main__':
    sys.exit(main())
