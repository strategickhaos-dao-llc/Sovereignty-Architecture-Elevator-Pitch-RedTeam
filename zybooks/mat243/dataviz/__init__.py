"""
MAT-243 Data Visualization Module
Wrappers for seaborn/matplotlib aligned with zyBooks content
"""

from .charts import (
    create_bar_chart,
    create_pie_chart,
    create_histogram,
    create_scatter_plot
)

__all__ = [
    'create_bar_chart',
    'create_pie_chart',
    'create_histogram',
    'create_scatter_plot'
]

__version__ = '1.0.0'
