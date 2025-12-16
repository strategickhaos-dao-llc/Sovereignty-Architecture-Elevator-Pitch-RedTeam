#!/usr/bin/env python3
"""
Example 1.3.1: Unemployment Rates

This script demonstrates how to load and visualize unemployment data using matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt


def create_unemployment_data():
    """Create sample unemployment data for 1980-2017."""
    years = list(range(1980, 2018))
    # Simulated unemployment rates with some variation
    unemployment_rate = [
        7.2, 7.6, 9.7, 9.6, 7.5, 7.2, 7.0, 6.2, 5.5, 5.3,
        5.6, 6.8, 7.5, 6.9, 6.1, 5.6, 5.4, 4.9, 4.5, 4.2,
        4.0, 4.7, 5.8, 6.0, 5.5, 5.1, 4.6, 4.6, 5.8, 9.3,
        9.6, 8.9, 8.1, 7.4, 6.2, 5.3, 4.9, 4.4
    ]
    
    return pd.DataFrame({
        'Year': years,
        'Unemployment_Rate': unemployment_rate
    })


def plot_unemployment_data(data):
    """Create a line plot of unemployment rates over time."""
    plt.figure(figsize=(12, 6))
    plt.plot(data['Year'], data['Unemployment_Rate'], 
             marker='o', linewidth=2, markersize=4, color='steelblue')
    
    # Add labels and title
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.title('U.S. Unemployment Rate (1980-2017)', fontsize=14, fontweight='bold')
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Display the plot
    plt.tight_layout()
    plt.show()


def main():
    """Main function to run the unemployment visualization."""
    print("Loading unemployment data...")
    unemployment_data = create_unemployment_data()
    
    print("\nFirst few rows of data:")
    print(unemployment_data.head())
    
    print("\nCreating visualization...")
    plot_unemployment_data(unemployment_data)
    
    print("\nVisualization complete!")


if __name__ == "__main__":
    main()
