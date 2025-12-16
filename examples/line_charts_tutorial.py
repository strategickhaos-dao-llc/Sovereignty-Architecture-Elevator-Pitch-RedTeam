"""
Line Charts Tutorial - Section 1.8
Educational examples demonstrating line chart creation and best practices in Python.

This module implements the concepts from zyBooks Section 1.8:
- Creating line charts to show trends over time
- Adding linear trend lines
- Displaying multiple datasets
- Understanding appropriate vs inappropriate use cases
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import List, Tuple


def example_1_apple_stock_prices():
    """
    Example 1: Apple stock prices from March 2015 to March 2016
    Demonstrates basic line chart creation with time series data.
    """
    # Data from zyBooks Table 1.8.1
    dates = [
        'Mar 2, 2015', 'Apr 1, 2015', 'May 1, 2015', 'Jun 1, 2015',
        'Jul 1, 2015', 'Aug 3, 2015', 'Sep 1, 2015', 'Oct 1, 2015',
        'Nov 2, 2015', 'Dec 1, 2015', 'Jan 4, 2016', 'Feb 1, 2016', 'Mar 1, 2016'
    ]
    
    # Sample stock prices (USD) - realistic values for the period
    prices = [127.04, 125.32, 130.28, 126.60, 121.30, 115.39, 110.38, 
              112.12, 119.30, 105.26, 96.45, 96.35, 100.53]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left plot: Scatter plot without lines
    ax1.scatter(range(len(dates)), prices, color='blue', s=50, zorder=3)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Stock price (USD)', fontsize=12)
    ax1.set_title('Apple Stock Prices (March 2015 - March 2016)\nScatter Plot', fontsize=14)
    ax1.set_xticks(range(len(dates)))
    ax1.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Line chart
    ax2.plot(range(len(dates)), prices, marker='o', color='blue', linewidth=2, markersize=6)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Stock price (USD)', fontsize=12)
    ax2.set_title('Apple Stock Prices (March 2015 - March 2016)\nLine Chart', fontsize=14)
    ax2.set_xticks(range(len(dates)))
    ax2.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/apple_stock_chart.png', dpi=300, bbox_inches='tight')
    print("✓ Created: apple_stock_chart.png")
    plt.close()


def example_2_apple_with_trendline():
    """
    Example 2: Apple stock prices with linear trend line
    Demonstrates how to add a trend line to show overall direction.
    """
    dates = [
        'Mar 2, 2015', 'Apr 1, 2015', 'May 1, 2015', 'Jun 1, 2015',
        'Jul 1, 2015', 'Aug 3, 2015', 'Sep 1, 2015', 'Oct 1, 2015',
        'Nov 2, 2015', 'Dec 1, 2015', 'Jan 4, 2016', 'Feb 1, 2016', 'Mar 1, 2016'
    ]
    
    prices = [127.04, 125.32, 130.28, 126.60, 121.30, 115.39, 110.38, 
              112.12, 119.30, 105.26, 96.45, 96.35, 100.53]
    
    x = np.arange(len(dates))
    
    # Calculate linear trend line using numpy polyfit
    z = np.polyfit(x, prices, 1)
    p = np.poly1d(z)
    trend_line = p(x)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(x, prices, marker='o', color='blue', linewidth=2, markersize=6, label='Stock Price')
    plt.plot(x, trend_line, color='red', linewidth=2, linestyle='--', label='Linear Trend')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Stock price (USD)', fontsize=12)
    plt.title('Apple Stock Prices (March 2015 - March 2016)\nwith Linear Trend Line', fontsize=14)
    plt.xticks(x, dates, rotation=45, ha='right', fontsize=9)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/apple_stock_trendline.png', dpi=300, bbox_inches='tight')
    print("✓ Created: apple_stock_trendline.png")
    plt.close()


def example_3_google_stock_prices():
    """
    Example 3: Google/Alphabet stock prices from March 2015 to March 2016
    Demonstrates line chart with increasing trend.
    """
    dates = [
        'Mar 2015', 'Apr 2015', 'May 2015', 'Jun 2015', 'Jul 2015', 
        'Aug 2015', 'Sep 2015', 'Oct 2015', 'Nov 2015', 'Dec 2015',
        'Jan 2016', 'Feb 2016', 'Mar 2016'
    ]
    
    # Google stock prices showing overall increase
    prices = [555, 545, 535, 525, 530, 665, 635, 695, 735, 760, 745, 700, 725]
    
    x = np.arange(len(dates))
    
    # Calculate linear trend line
    z = np.polyfit(x, prices, 1)
    p = np.poly1d(z)
    trend_line = p(x)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(x, prices, marker='o', color='green', linewidth=2, markersize=6, label='Stock Price')
    plt.plot(x, trend_line, color='red', linewidth=2, linestyle='--', label='Linear Trend')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Stock price (USD)', fontsize=12)
    plt.title('Alphabet (Google) Stock Prices (March 2015 - March 2016)\nwith Linear Trend Line', fontsize=14)
    plt.xticks(x, dates, rotation=45, ha='right')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/google_stock_chart.png', dpi=300, bbox_inches='tight')
    print("✓ Created: google_stock_chart.png")
    plt.close()


def example_4_multiple_datasets_temperature():
    """
    Example 4: Multiple datasets showing temperature comparison
    Los Angeles, USA vs Durban, South Africa
    Demonstrates how to display multiple datasets on one chart.
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Average high temperatures (Fahrenheit)
    # Los Angeles follows concave parabola (peaks in summer)
    la_temps = [68, 70, 72, 75, 77, 82, 85, 85, 83, 79, 73, 68]
    
    # Durban follows convex parabola (peaks in winter - opposite hemisphere)
    durban_temps = [81, 81, 80, 77, 73, 71, 71, 72, 73, 75, 77, 79]
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, la_temps, marker='s', color='orange', linewidth=2, 
             markersize=7, label='Los Angeles, USA')
    plt.plot(months, durban_temps, marker='^', color='blue', linewidth=2, 
             markersize=7, label='Durban, South Africa')
    
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Temperature (°F)', fontsize=12)
    plt.title('Average High Temperatures:\nLos Angeles, USA vs Durban, South Africa', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/temperature_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: temperature_comparison.png")
    plt.close()


def example_5_three_cities_temperature():
    """
    Example 5: Three city temperature comparison
    Pueblo (Colorado), Tianshui (China), and Asunción (Paraguay)
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Pueblo and Tianshui - northern hemisphere (concave parabola)
    pueblo_temps = [45, 48, 58, 65, 75, 85, 92, 89, 81, 68, 55, 45]
    tianshui_temps = [38, 43, 52, 62, 70, 78, 84, 82, 73, 62, 50, 40]
    
    # Asunción - southern hemisphere (convex parabola)
    asuncion_temps = [92, 91, 88, 80, 75, 72, 73, 76, 81, 85, 88, 91]
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, pueblo_temps, marker='o', color='red', linewidth=2, 
             markersize=6, label='Pueblo, Colorado, USA')
    plt.plot(months, tianshui_temps, marker='s', color='blue', linewidth=2, 
             markersize=6, label='Tianshui, China')
    plt.plot(months, asuncion_temps, marker='^', color='green', linewidth=2, 
             markersize=6, label='Asunción, Paraguay')
    
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Temperature (°F)', fontsize=12)
    plt.title('Average High Temperatures:\nPueblo, USA vs Tianshui, China vs Asunción, Paraguay', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/three_cities_temperature.png', dpi=300, bbox_inches='tight')
    print("✓ Created: three_cities_temperature.png")
    plt.close()


def example_6_unemployment_rate():
    """
    Example 6: US Unemployment rate over time (1980-2017)
    Demonstrates line chart for economic data.
    """
    # Simplified unemployment data (realistic values)
    years = list(range(1980, 2018, 2))  # Every 2 years for clarity
    unemployment_rates = [7.1, 9.7, 7.5, 5.5, 5.3, 6.8, 5.6, 4.5, 4.0, 
                         5.8, 4.7, 4.6, 5.5, 9.3, 9.6, 8.1, 6.2, 5.3, 4.4]
    
    plt.figure(figsize=(14, 6))
    plt.plot(years, unemployment_rates, marker='o', color='darkblue', 
             linewidth=2, markersize=6)
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.title('United States Unemployment Rate (1980-2017)', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/unemployment_rate.png', dpi=300, bbox_inches='tight')
    print("✓ Created: unemployment_rate.png")
    plt.close()


def example_7_inappropriate_categorical():
    """
    Example 7: Demonstrates INAPPROPRIATE use of line chart for categorical data
    Shows why line charts shouldn't be used for nominal categorical variables.
    """
    states = ['SD', 'NH', 'ND', 'UT', 'VT', 'HI', 'ID', 'ME']
    unemployment = [2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: INAPPROPRIATE line chart
    ax1.plot(states, unemployment, marker='o', color='red', linewidth=2, markersize=6)
    ax1.set_xlabel('State', fontsize=12)
    ax1.set_ylabel('Unemployment Rate (%)', fontsize=12)
    ax1.set_title('❌ INAPPROPRIATE: Line Chart for Categorical Data', fontsize=13, color='red')
    ax1.grid(True, alpha=0.3)
    ax1.text(0.5, 0.95, 'Lines suggest relationship between unrelated states!', 
             transform=ax1.transAxes, ha='center', va='top', 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Right: APPROPRIATE bar chart
    ax2.bar(states, unemployment, color='green', alpha=0.7)
    ax2.set_xlabel('State', fontsize=12)
    ax2.set_ylabel('Unemployment Rate (%)', fontsize=12)
    ax2.set_title('✓ APPROPRIATE: Bar Chart for Categorical Data', fontsize=13, color='green')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/categorical_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: categorical_comparison.png")
    plt.close()


def example_8_missing_labels():
    """
    Example 8: Demonstrates the importance of proper labels and units
    Shows a chart with missing labels (common mistake).
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    temps = [73, 73, 74, 76, 78, 80, 81, 82, 81, 80, 77, 74]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Missing labels (BAD)
    ax1.plot(months, temps, marker='o', color='blue', linewidth=2)
    ax1.set_ylabel('Temperature')  # Missing units!
    # Missing x-axis label!
    ax1.set_title('❌ Missing Labels/Units', fontsize=13, color='red')
    ax1.grid(True, alpha=0.3)
    
    # Right: Proper labels (GOOD)
    ax2.plot(months, temps, marker='o', color='green', linewidth=2)
    ax2.set_xlabel('Month', fontsize=12)
    ax2.set_ylabel('Temperature (°F)', fontsize=12)
    ax2.set_title('✓ Proper Labels and Units', fontsize=13, color='green')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Average Monthly Temperatures in Hawaii', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig('/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-RedTeam/Sovereignty-Architecture-Elevator-Pitch-RedTeam/examples/labeling_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Created: labeling_importance.png")
    plt.close()


def run_all_examples():
    """
    Run all line chart examples from Section 1.8
    """
    print("\n" + "="*60)
    print("LINE CHARTS TUTORIAL - Section 1.8")
    print("Creating Python examples for zyBooks content")
    print("="*60 + "\n")
    
    print("Generating example charts...\n")
    
    example_1_apple_stock_prices()
    example_2_apple_with_trendline()
    example_3_google_stock_prices()
    example_4_multiple_datasets_temperature()
    example_5_three_cities_temperature()
    example_6_unemployment_rate()
    example_7_inappropriate_categorical()
    example_8_missing_labels()
    
    print("\n" + "="*60)
    print("✓ All examples generated successfully!")
    print("Check the 'examples/' directory for PNG files")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_examples()
