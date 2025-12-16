"""
Example 1.6.2: U.S. Bureau of Labor Statistics time use survey.

This example creates an exploded pie chart showing time use for full-time 
college and university students with emphasis on sleeping.
Data from the American Time Use Survey (ATUS).
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

# Data for college student time use (percentages of a 24-hour day)
activities = [
    'Sleeping',
    'Leisure and sports',
    'Educational activities',
    'Work and related activities',
    'Traveling',
    'Eating and drinking',
    'Grooming',
    'Other'
]

# Percentages (should sum to 100%)
percentages = [36.2, 17.1, 13.8, 10.0, 5.8, 4.2, 3.3, 9.6]

# Colors for each slice
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', 
          '#70AD47', '#C55A11', '#7030A0']

# Explode the sleeping slice (first element)
# 0.1 means the slice is moved out by 0.1 units from the center
explode = (0.1, 0, 0, 0, 0, 0, 0, 0)

# Create the exploded pie chart
fig, ax = plt.subplots(figsize=(10, 8))

wedges, texts, autotexts = ax.pie(percentages, 
                                    labels=activities, 
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    colors=colors,
                                    explode=explode,
                                    shadow=True)

# Enhance text properties
for text in texts:
    text.set_fontsize(11)
    
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax.set_title('Average Weekday Time Use for College Students', 
             fontsize=14, fontweight='bold', pad=20)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

plt.tight_layout()
plt.savefig('college_student_time_use.png', dpi=300, bbox_inches='tight')
print("Exploded pie chart saved as 'college_student_time_use.png'")
# plt.show()  # Uncomment to display interactively if running in an environment with a display

# Additional insights
print("\nKey Insights:")
print("1. College students spend more of the non-sleeping time on Leisure and sports (17.1%)")
print("   than any other activity.")
print("2. The full pie represents 24 hours (100% of a day).")
print(f"3. Students spend {percentages[0]}% of their day sleeping, which is approximately")
print(f"   {round(percentages[0] * 24 / 100, 1)} hours per day.")
