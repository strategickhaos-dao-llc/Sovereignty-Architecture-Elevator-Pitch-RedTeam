"""
Example 1.6.4: Demonstrating pie chart misuse - 3D pie charts.

This example shows why 3D pie charts distort data and make interpretation difficult.
Data represents simplified federal spending categories.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

# Federal spending categories (simplified for example)
categories = [
    'Social programs',
    'National defense,\nveterans, and\nforeign affairs',
    'Net interest\non the debt',
    'Physical, human,\nand community\ndevelopment',
    'Law enforcement\nand general\ngovernment'
]

# Percentages (should sum to 100%)
percentages = [33, 24, 6, 9, 7]
remaining = 100 - sum(percentages)
categories.append('Other mandatory')
percentages.append(remaining)

colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47']

# Create a standard 2D pie chart for comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# 2D Pie Chart (Good practice)
ax1.pie(percentages, labels=categories, autopct='%1.0f%%',
        startangle=90, colors=colors)
ax1.set_title('2D Pie Chart (GOOD)\nFederal Spending by Category', 
             fontsize=12, fontweight='bold', color='green')
ax1.axis('equal')

# Simulated 3D effect (Bad practice)
# matplotlib doesn't have true 3D pie charts, but we can show the distortion concept
explode = (0.1, 0, 0, 0, 0, 0)  # Explode the first slice to simulate 3D front effect

wedges, texts, autotexts = ax2.pie(percentages, 
                                     labels=categories, 
                                     autopct='%1.0f%%',
                                     startangle=70,  # Different angle to show distortion
                                     colors=colors,
                                     explode=explode,
                                     shadow=True)  # Shadow simulates 3D effect

ax2.set_title('Pie Chart with 3D Effects (BAD)\nSame Data - Distorted Perception', 
             fontsize=12, fontweight='bold', color='red')
ax2.axis('equal')

plt.tight_layout()
plt.savefig('3d_pie_chart_comparison.png', dpi=300, bbox_inches='tight')
print("Chart saved as '3d_pie_chart_comparison.png'")
# plt.show()  # Uncomment to display interactively if running in an environment with a display

print("\n" + "="*70)
print("WHY 3D PIE CHARTS ARE PROBLEMATIC:")
print("="*70)
print("1. 3D perspective distorts the relative sizes of slices")
print("2. Slices in the 'front' appear larger than they actually are")
print("3. Slices in the 'back' appear smaller than they actually are")
print("4. The angle and tilt make precise comparison nearly impossible")
print("\nEXAMPLE FROM THE DATA:")
print(f"- 'Law enforcement' ({percentages[4]}%) may appear similar to")
print(f"  'Physical development' ({percentages[3]}%) in 3D view")
print(f"- But 'Physical development' is actually {percentages[3] - percentages[4]}% larger!")
print("\nBEST PRACTICE: Always use 2D pie charts (or better yet, bar charts)")
