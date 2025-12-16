# Data Visualization Guide

## Section 1.2: What is Data Visualization?

### Learning Objectives
- Interpret tables and charts
- Identify the most appropriate chart for different data types

---

## Introduction to Data Visualization

Data visualization is the display of data in a format, such as a table or chart, that seeks to achieve a goal of conveying particular information to a viewer. Data presented in a text-only format often does not convey information well.

### Example: Southern California House Prices

**Text-only format (difficult to read):**
Los Angeles $385,000; Orange $510,000; Riverside $285,000; San Bernardino $205,000; San Diego $440,000; Ventura $445,000

**Table format (better readability):**

| County | Median House Price |
|--------|-------------------|
| Los Angeles | $385,000 |
| Orange | $510,000 |
| Riverside | $285,000 |
| San Bernardino | $205,000 |
| San Diego | $440,000 |
| Ventura | $445,000 |

*Table 1.2.1: Southern California median house prices by county (2013)*

---

## Visualizing Trends with Charts

When the goal is to illustrate trends over time, such as the housing price "bubble" that grew and then burst in 2008, a chart is even better than a table.

### California House Prices (2000-2010)

| Year | California Median House Price |
|------|------------------------------|
| 2000 | $225,000 |
| 2001 | $265,000 |
| 2002 | $315,000 |
| 2003 | $370,000 |
| 2004 | $450,000 |
| 2005 | $520,000 |
| 2006 | $575,000 |
| 2007 | $575,000 |
| 2008 | $375,000 |
| 2009 | $275,000 |
| 2010 | $295,000 |

*Table 1.2.2: California median house prices, 2000-2010*

**Chart Description:**
A line chart showing California house prices with Year on the x-axis (2000-2010) and House prices on the y-axis ($0-$600,000). The chart shows a gradual increase from $225,000 in 2000 to a peak of approximately $575,000 in 2007, followed by a rapid decline to $275,000 in 2009, where prices begin to increase again.

---

## Uses of Data Visualization

### 1. Quick Comprehension
Expressing data as a table or chart allows viewers to comprehend data more quickly than data presented as a list of numbers. A chart is particularly helpful in analyzing large datasets where a list or table would be incomprehensible.

### 2. Intuitive Understanding
Visual representation is more intuitively grasped than numbers. For example, a pie chart showing milk availability categories allows viewers to quickly see that plain 2% milk has the greatest availability (35%) and gain an intuitive sense of relative proportions.

### 3. Identifying Trends
Charts help viewers see trends in data. For example:
- Gold prices from 1971 to 2019 show an overall upward trend
- Market crashes in 1981 and 2013 become visible
- Investors can use this information for timing decisions

### 4. Identifying Relationships and Patterns
Charts allow viewers to identify relationships between variables. Comparing multiple datasets (like gold prices vs. stock prices) can reveal:
- Whether variables move together or independently
- Relative pricing at different time periods
- Optimal timing for investments

---

## Considerations for Data Visualization

When choosing how to present data, several factors must be considered:

### 1. Dataset Size and Cardinality

**Cardinality** is the number of unique elements in a dataset.

- **High cardinality**: Each element is unique (e.g., student IDs)
- **Low cardinality**: Many elements share the same values (e.g., student ages)

### 2. Chart Types for Different Cardinality

**Low-Cardinality Data:**
- ✓ Pie charts
- ✓ Bar charts
- Easy to read with distinct categories

**High-Cardinality Data:**
- ✓ Scatter plots
- ✓ Line charts
- ✓ Histograms
- Better for showing distributions and relationships

### 3. Chart Selection Based on Data Type

**Single Variable Data:**
- Pie chart
- Histogram
- Box plot

**Two or More Related Variables:**
- Scatter plot
- Line chart

**Categorical Data:**
- Bar chart
- Pie chart
- Violin plot

---

## Practice Questions

### Question 1: Reading Tables
Based on the Southern California house prices table (2013), what is the median house price in San Bernardino county?

**Answer:** $205,000

### Question 2: Identifying Trends
Based on the California house prices table (2000-2010), in what year did the price bubble burst? (The year when prices were drastically lower than the previous year)

**Answer:** 2008

### Question 3: Reading Charts
Based on the California house prices chart (2000-2010), in what year was the peak of house prices?

**Answer:** 2007

### Question 4: Analyzing Relative Differences
Based on the California house prices chart (2000-2010), what was the relative difference between the highest and lowest California house prices? (double, triple, or quadruple)

**Answer:** More than double (highest: ~$575,000, lowest: ~$225,000)

---

## Key Takeaways

1. **Data visualization transforms raw data into insights** through tables, charts, and graphs
2. **Charts are valuable for all dataset sizes** and become essential for large datasets
3. **Different chart types serve different purposes** - choose based on your data and goals
4. **Cardinality matters** when selecting visualization methods
5. **Visual representations reveal patterns** that are difficult to see in raw data

---

## References

1. Moore, Karleigh, et al. "Data Presentation - Pie Charts." Brilliant.org
2. USDA Economic Research Service. "Food Availability Per Capita Data System"
3. Macrotrends. "Gold Prices - 100 Year Historical Chart"
4. Sunshine Profits. "Precious metals investment terms A to Z"

---

*This guide is designed to help understand fundamental concepts of data visualization and their practical applications in analyzing real-world data.*
