"""
Example 1.6.3: Demonstrating pie chart misuse - too many slices.

This example shows why pie charts with more than 5-6 slices become difficult to read.
It creates a pie chart with 20 slices (representing the 20 largest economies).
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

# Sample data for 20 largest economies (simplified values for demonstration)
economies = [
    'USA', 'China', 'Japan', 'Germany', 'UK', 'India', 'France', 'Italy',
    'Brazil', 'Canada', 'South Korea', 'Russia', 'Spain', 'Australia',
    'Mexico', 'Indonesia', 'Netherlands', 'Turkey', 'Switzerland', 'Saudi Arabia'
]

# GDP values (in trillions, approximate)
gdp_values = [21.4, 14.3, 5.1, 3.8, 2.8, 2.7, 2.7, 2.0,
              1.8, 1.7, 1.6, 1.6, 1.4, 1.4,
              1.3, 1.1, 0.9, 0.8, 0.7, 0.7]

# Create the cluttered pie chart
fig, ax = plt.subplots(figsize=(12, 10))

# Use many different colors (which can also be confusing)
colors = plt.cm.Set3(range(len(economies)))

wedges, texts, autotexts = ax.pie(gdp_values, 
                                    labels=economies, 
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    colors=colors)

# Make text smaller to try to fit (but this also makes it harder to read)
for text in texts:
    text.set_fontsize(8)
    
for autotext in autotexts:
    autotext.set_fontsize(7)

ax.set_title('20 Largest Economies in the World\n(Example of TOO MANY SLICES)', 
             fontsize=14, fontweight='bold', pad=20, color='red')

ax.axis('equal')

plt.tight_layout()
plt.savefig('too_many_slices_bad_example.png', dpi=300, bbox_inches='tight')
print("Chart saved as 'too_many_slices_bad_example.png'")
# plt.show()  # Uncomment to display interactively if running in an environment with a display

print("\n" + "="*70)
print("WHY THIS CHART IS DIFFICULT TO READ:")
print("="*70)
print("1. Too many slices make it hard to visually compare relative sizes")
print("2. Labels are cluttered and overlap")
print("3. Small slices (like Switzerland, Saudi Arabia) convey little information")
print("4. Difficult to distinguish between similar-sized slices")
print("\nBETTER ALTERNATIVES:")
print("- Use a bar chart for easier comparison")
print("- Show only top 5-6 economies and group others as 'Other'")
print("- Use a table for precise values")
