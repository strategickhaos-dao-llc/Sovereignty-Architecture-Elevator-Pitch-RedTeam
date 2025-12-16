"""
Example 1.6.1: CDC data on health and access to care among employed and unemployed adults.

This example creates pie charts showing insurance status and type according to employment status.
Data from the U.S. Centers for Disease Control study (2009-2010).
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

# Data for employed adults
employed_labels = ['Private Insurance', 'Uninsured', 'Public Insurance']
employed_sizes = [75.2, 18.2, 6.6]
employed_colors = ['#4472C4', '#ED7D31', '#A5A5A5']

# Data for unemployed adults
unemployed_labels = ['Uninsured', 'Private Insurance', 'Public Insurance']
unemployed_sizes = [51.0, 29.3, 19.7]
unemployed_colors = ['#ED7D31', '#4472C4', '#A5A5A5']

# Create figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Employed adults pie chart
ax1.pie(employed_sizes, labels=employed_labels, autopct='%1.1f%%',
        startangle=90, colors=employed_colors)
ax1.set_title('Employed Adults\nInsurance Status', fontsize=12, fontweight='bold')

# Unemployed adults pie chart
ax2.pie(unemployed_sizes, labels=unemployed_labels, autopct='%1.1f%%',
        startangle=90, colors=unemployed_colors)
ax2.set_title('Unemployed Adults\nInsurance Status', fontsize=12, fontweight='bold')

# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')
ax2.axis('equal')

plt.suptitle('Health Insurance Status by Employment (2009-2010)', 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('cdc_insurance_status.png', dpi=300, bbox_inches='tight')
print("Pie charts saved as 'cdc_insurance_status.png'")
# plt.show()  # Uncomment to display interactively if running in an environment with a display

# Key findings from the data
print("\nKey Findings:")
print(f"1. {unemployed_sizes[2]}% of unemployed individuals had public insurance.")
print(f"2. The percentage of uninsured among unemployed ({unemployed_sizes[0]}%) was nearly three times")
print(f"   as high as those who are employed ({employed_sizes[1]}%).")
print(f"3. Unemployed individuals are less likely to have private insurance ({unemployed_sizes[1]}%)")
print(f"   compared to employed individuals ({employed_sizes[0]}%).")
