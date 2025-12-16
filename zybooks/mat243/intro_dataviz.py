#!/usr/bin/env python3
"""
MAT-243 Section 1.4: Introduction to Data Visualization with Python

zyBooks Reference: Module 1.4
FlameLang Target: Data visualization DSL layer

This module provides a comprehensive introduction to data visualization
using Python, pandas, and matplotlib. It aligns with zyBooks Module 1.4-1.5
content and includes FlameLang syntax comments showing future transpilation.

Author: Strategickhaos DAO LLC
Course: MAT-243 Applied Statistics for STEM
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional, Union


class DataVisualizationIntro:
    """
    Introduction to data visualization concepts and techniques.
    
    Key Topics:
    - Why visualize data?
    - Types of charts and when to use them
    - Basic pandas DataFrame operations
    - Creating simple visualizations
    
    zyBooks Reference: Section 1.4
    """
    
    def __init__(self):
        """Initialize the data visualization introduction module."""
        self.examples = {}
        
    @staticmethod
    def why_visualize():
        """
        Explain the importance of data visualization.
        
        zyBooks Concept: Data visualization makes patterns obvious that
        would be hidden in raw data or tables.
        
        # FlameLang Target Syntax:
        # 🔥 visualize_importance {
        #     concept: "patterns emerge visually"
        #     power: human_visual_processing >> text_processing
        #     insight: "see trends instantly"
        # }
        """
        principles = {
            "Pattern Recognition": "Humans process visual information 60,000x faster than text",
            "Comparison": "Bar charts instantly show which values are larger",
            "Trends": "Line charts reveal changes over time at a glance",
            "Distribution": "Histograms show data spread and central tendency",
            "Relationships": "Scatter plots expose correlations between variables",
            "Proportions": "Pie charts display parts of a whole"
        }
        
        print("=" * 70)
        print("WHY VISUALIZE DATA?")
        print("=" * 70)
        for principle, explanation in principles.items():
            print(f"\n{principle}:")
            print(f"  → {explanation}")
        print("\n" + "=" * 70)
        
        return principles
    
    @staticmethod
    def chart_selection_guide() -> Dict[str, Dict]:
        """
        Guide for selecting the right chart type.
        
        zyBooks Sections: 1.5 (Bar), 1.6 (Pie), 1.7 (Histogram), 1.8 (Scatter)
        
        # FlameLang Target Syntax:
        # 🔥 chart_selector {
        #     if data_type == "categorical_comparison" -> bar_chart
        #     if data_type == "proportions" -> pie_chart
        #     if data_type == "distribution" -> histogram
        #     if data_type == "correlation" -> scatter_plot
        # }
        """
        guide = {
            "Bar Chart": {
                "when": "Comparing categories or groups",
                "best_for": "Showing RELATIVE values (not exact)",
                "example": "Revenue by store, sales by quarter",
                "zybooks_section": "1.5",
                "key_insight": "Instant visual comparison"
            },
            "Pie Chart": {
                "when": "Showing parts of a whole",
                "best_for": "Percentages and proportions",
                "example": "Market share, budget allocation",
                "zybooks_section": "1.6",
                "key_insight": "Limit to 5-7 slices for clarity"
            },
            "Histogram": {
                "when": "Showing distribution of numerical data",
                "best_for": "Understanding data spread and shape",
                "example": "Test scores, ages, temperatures",
                "zybooks_section": "1.7",
                "key_insight": "Reveals normal, skewed, or uniform distributions"
            },
            "Scatter Plot": {
                "when": "Showing relationship between two variables",
                "best_for": "Detecting correlations and patterns",
                "example": "Height vs weight, study time vs grades",
                "zybooks_section": "1.8",
                "key_insight": "Identifies positive, negative, or no correlation"
            }
        }
        
        print("\n" + "=" * 70)
        print("CHART SELECTION GUIDE")
        print("=" * 70)
        for chart_type, info in guide.items():
            print(f"\n{chart_type} (zyBooks {info['zybooks_section']}):")
            print(f"  When: {info['when']}")
            print(f"  Best For: {info['best_for']}")
            print(f"  Example: {info['example']}")
            print(f"  💡 Key Insight: {info['key_insight']}")
        print("\n" + "=" * 70)
        
        return guide
    
    @staticmethod
    def pandas_basics_demo():
        """
        Demonstrate basic pandas DataFrame operations.
        
        zyBooks Concept: DataFrames are the foundation for data analysis in Python.
        
        # FlameLang Target Syntax:
        # 🔥 dataframe students {
        #     load: "students.csv"
        #     columns: [name, age, grade, gpa]
        #     operations: [filter, sort, group, aggregate]
        # }
        """
        print("\n" + "=" * 70)
        print("PANDAS DATAFRAME BASICS")
        print("=" * 70)
        
        # Create sample student data
        students = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
            'Age': [20, 22, 21, 20, 23, 21],
            'Major': ['Math', 'CS', 'Math', 'Stats', 'CS', 'Stats'],
            'GPA': [3.8, 3.6, 3.9, 3.7, 3.5, 3.8]
        })
        
        print("\n1. Creating a DataFrame:")
        print(students)
        
        print("\n2. Basic Statistics:")
        print(students['GPA'].describe())
        
        print("\n3. Filtering (GPA >= 3.7):")
        high_gpa = students[students['GPA'] >= 3.7]
        print(high_gpa[['Name', 'GPA']])
        
        print("\n4. Grouping by Major:")
        by_major = students.groupby('Major')['GPA'].mean()
        print(by_major)
        
        print("\n5. Sorting by GPA (descending):")
        sorted_students = students.sort_values('GPA', ascending=False)
        print(sorted_students[['Name', 'GPA']])
        
        print("\n" + "=" * 70)
        
        return students
    
    @staticmethod
    def simple_visualization_example():
        """
        Create a simple visualization example combining concepts.
        
        zyBooks Integration: Combines 1.4 (intro) and 1.5 (bar chart)
        
        # FlameLang Target Syntax:
        # 🔥 visualize student_performance {
        #     data: students
        #     chart: bar
        #     x: "Major"
        #     y: "GPA" |> mean
        #     title: "Average GPA by Major"
        #     style: academic
        # }
        """
        print("\n" + "=" * 70)
        print("SIMPLE VISUALIZATION EXAMPLE")
        print("=" * 70)
        
        # Create sample data
        majors = ['Mathematics', 'Computer Science', 'Statistics', 'Data Science']
        avg_gpa = [3.75, 3.62, 3.81, 3.70]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(majors, avg_gpa, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        
        # Customize
        plt.xlabel('Major', fontsize=12, fontweight='bold')
        plt.ylabel('Average GPA', fontsize=12, fontweight='bold')
        plt.title('Average GPA by Major', fontsize=14, fontweight='bold')
        plt.ylim(3.5, 4.0)
        
        # Add value labels on bars
        for i, (bar, gpa) in enumerate(zip(bars, avg_gpa)):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{gpa:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Save figure
        output_path = 'simple_viz_example.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Visualization saved to: {output_path}")
        print("\nKey Observations:")
        print("  • Statistics majors have highest average GPA (3.81)")
        print("  • Computer Science majors have lowest (3.62)")
        print("  • All majors maintain GPA above 3.60")
        print("  • Difference between highest and lowest is 0.19")
        
        plt.close()
        
        print("\n" + "=" * 70)
    
    @staticmethod
    def data_visualization_workflow():
        """
        Outline the complete data visualization workflow.
        
        zyBooks Concept: Structured approach to creating effective visualizations.
        
        # FlameLang Target Syntax:
        # 🔥 workflow data_viz {
        #     step1: understand_data |> explore |> clean
        #     step2: choose_chart |> match_to_question
        #     step3: create_viz |> customize |> enhance
        #     step4: interpret |> communicate |> iterate
        # }
        """
        workflow = {
            "Step 1: Understand Your Data": [
                "What type of data do you have? (categorical, numerical, time-series)",
                "How many variables are you analyzing?",
                "What is the size of your dataset?",
                "Are there missing values or outliers?"
            ],
            "Step 2: Define Your Question": [
                "What do you want to learn from the data?",
                "Are you comparing groups?",
                "Looking for trends over time?",
                "Examining relationships between variables?"
            ],
            "Step 3: Choose Appropriate Chart": [
                "Match chart type to your question",
                "Bar chart → comparisons",
                "Line chart → trends",
                "Scatter plot → relationships",
                "Histogram → distributions"
            ],
            "Step 4: Create and Customize": [
                "Use clear, descriptive titles",
                "Label axes with units",
                "Choose appropriate colors",
                "Add legends when necessary",
                "Remove unnecessary elements"
            ],
            "Step 5: Interpret and Communicate": [
                "What patterns do you see?",
                "What story does the data tell?",
                "Are there unexpected findings?",
                "How does this answer your question?"
            ]
        }
        
        print("\n" + "=" * 70)
        print("DATA VISUALIZATION WORKFLOW")
        print("=" * 70)
        for step, guidelines in workflow.items():
            print(f"\n{step}:")
            for guideline in guidelines:
                print(f"  • {guideline}")
        print("\n" + "=" * 70)
        
        return workflow


def main():
    """
    Main demonstration of data visualization introduction.
    
    Runs through all key concepts from zyBooks Section 1.4
    """
    print("\n" + "🔥" * 35)
    print("MAT-243: Introduction to Data Visualization with Python")
    print("zyBooks Module 1.4")
    print("🔥" * 35)
    
    intro = DataVisualizationIntro()
    
    # Run demonstrations
    intro.why_visualize()
    intro.chart_selection_guide()
    intro.pandas_basics_demo()
    intro.simple_visualization_example()
    intro.data_visualization_workflow()
    
    print("\n✅ Introduction to Data Visualization Complete!")
    print("\n📚 Next Steps:")
    print("  1. Continue to Section 1.5: Bar Charts")
    print("  2. Practice with provided Jupyter notebooks")
    print("  3. Complete participation activities in zyBooks")
    print("\n" + "🔥" * 35 + "\n")


if __name__ == "__main__":
    main()
