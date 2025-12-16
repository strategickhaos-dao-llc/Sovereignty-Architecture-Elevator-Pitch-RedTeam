"""
Example 1.6.5: Demonstrating pie chart misuse - poor color choices and over-exploded charts.

This example shows why similar colors and excessive exploding make charts hard to read.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

# Sample data for revenue sources
categories = ['Music', 'Videos', 'Apps', 'Books', 'Movies', 'Podcasts', 'Other']
values = [25, 20, 18, 15, 12, 6, 4]

# Create figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Good example - clear colors, no explosion
good_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
ax1.pie(values, labels=categories, autopct='%1.1f%%',
        startangle=90, colors=good_colors)
ax1.set_title('GOOD: Clear Colors,\nNo Explosion', 
             fontsize=12, fontweight='bold', color='green')
ax1.axis('equal')

# Bad example 1 - similar colors that are hard to distinguish
similar_colors = ['#3498DB', '#2E86C1', '#2874A6', '#21618C', '#1B4F72', '#154360', '#0E3449']
ax2.pie(values, labels=categories, autopct='%1.1f%%',
        startangle=90, colors=similar_colors)
ax2.set_title('BAD: Similar Colors\n(Hard to Distinguish)', 
             fontsize=12, fontweight='bold', color='red')
ax2.axis('equal')

# Bad example 2 - over-exploded chart
explode = (0.15, 0.1, 0.2, 0.05, 0.1, 0.15, 0.1)  # Multiple slices exploded at different amounts
ax3.pie(values, labels=categories, autopct='%1.1f%%',
        startangle=90, colors=good_colors, explode=explode, shadow=True)
ax3.set_title('BAD: Over-Exploded\n(Disorienting)', 
             fontsize=12, fontweight='bold', color='red')
ax3.axis('equal')

plt.suptitle('Revenue Sources Comparison: Good vs. Bad Design', 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('color_and_explosion_comparison.png', dpi=300, bbox_inches='tight')
print("Chart saved as 'color_and_explosion_comparison.png'")
# plt.show()  # Uncomment to display interactively if running in an environment with a display

print("\n" + "="*70)
print("COMMON PIE CHART DESIGN MISTAKES:")
print("="*70)
print("\n1. POOR COLOR CHOICES:")
print("   - Using colors that are too similar makes slices hard to distinguish")
print("   - Example: Multiple shades of blue can confuse readers")
print("   - Solution: Use contrasting colors with good visual separation")

print("\n2. OVER-EXPLODED CHARTS:")
print("   - Exploding multiple slices reduces readability")
print("   - Varying explosion distances creates visual confusion")
print("   - Uneven spacing makes size comparison difficult")
print("   - Solution: Explode only ONE slice (if any) to emphasize it")

print("\n3. BEST PRACTICES:")
print("   - Use distinct, contrasting colors")
print("   - Limit to 5-6 categories maximum")
print("   - Explode at most one slice")
print("   - Consider accessibility (colorblind-friendly palettes)")
print("   - When in doubt, use a bar chart instead!")
