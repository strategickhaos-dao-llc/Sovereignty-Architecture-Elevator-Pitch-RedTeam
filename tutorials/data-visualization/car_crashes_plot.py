#!/usr/bin/env python3
"""
Example 1.3.2: Automobile Collisions

This script demonstrates how to create overlay bar charts using matplotlib 
to compare total collisions and speeding-related collisions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_car_crash_data():
    """Create sample car crash data by state."""
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA']
    total_collisions = [18.8, 18.1, 18.6, 22.4, 12.0, 13.6, 10.8, 16.2, 17.9, 15.6]
    speeding_collisions = [7.6, 6.4, 6.9, 9.1, 4.0, 5.0, 3.5, 5.8, 5.4, 5.1]
    
    return pd.DataFrame({
        'State': states,
        'Total': total_collisions,
        'Speeding': speeding_collisions
    })


def plot_overlay_bar_chart(data):
    """Create an overlay bar chart comparing total and speeding collisions."""
    plt.figure(figsize=(12, 6))
    
    # Set the width of bars and positions
    x_pos = np.arange(len(data['State']))
    bar_width = 0.6
    
    # Create bars - total collisions first (will be in the background)
    plt.bar(x_pos, data['Total'], bar_width, 
            label='Total Collisions', color='lightblue', alpha=0.8)
    
    # Overlay speeding collisions (will be in the foreground)
    plt.bar(x_pos, data['Speeding'], bar_width, 
            label='Speeding-Related Collisions', color='coral', alpha=0.9)
    
    # Add labels and title
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Collisions per 100,000 Population', fontsize=12)
    plt.title('Automobile Collisions by State: Total vs Speeding-Related', 
              fontsize=14, fontweight='bold')
    
    # Set x-axis labels
    plt.xticks(x_pos, data['State'])
    
    # Add legend
    plt.legend(loc='upper right')
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3, axis='y')
    
    # Display the plot
    plt.tight_layout()
    plt.show()


def calculate_speeding_percentage(data):
    """Calculate what percentage of collisions are due to speeding."""
    data['Speeding_Percentage'] = (data['Speeding'] / data['Total'] * 100).round(1)
    return data


def main():
    """Main function to run the car crashes visualization."""
    print("Loading car crash data...")
    car_crashes = create_car_crash_data()
    
    print("\nCar crash data by state:")
    print(car_crashes)
    
    print("\nCreating overlay bar chart...")
    plot_overlay_bar_chart(car_crashes)
    
    print("\nCalculating speeding percentages...")
    car_crashes = calculate_speeding_percentage(car_crashes)
    print("\nPercentage of collisions due to speeding by state:")
    print(car_crashes[['State', 'Speeding_Percentage']])
    
    print("\nVisualization complete!")
    print("\nKey Observations:")
    print("1. The bars for total collisions are overlaid with speeding-related collisions")
    print("2. The portion not covered represents collisions NOT related to speeding")


if __name__ == "__main__":
    main()
