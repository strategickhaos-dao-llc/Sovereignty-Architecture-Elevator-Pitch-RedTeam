"""
Data Visualization Chart Functions for MAT-243
Implements seaborn/matplotlib wrappers aligned with zyBooks 1.5-1.8

References:
- Section 1.5: Bar Charts
- Section 1.6: Pie Charts  
- Section 1.7: Histograms
- Section 1.8: Scatter Plots
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple, Union


# Set default style for all charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def create_bar_chart(
    data: Union[pd.DataFrame, dict, list],
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    title: str = "Bar Chart",
    xlabel: str = "Category",
    ylabel: str = "Value",
    color: str = "steelblue",
    figsize: Tuple[int, int] = (10, 6),
    horizontal: bool = False,
    show_values: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create a bar chart for comparing categorical data.
    
    zyBooks Reference: Section 1.5 - Bar Charts
    
    Key Concepts:
    - Bar charts excel at showing RELATIVE values (not exact values)
    - Best for visual comparison between categories
    - Good for: sales by store, revenue by quarter, counts by category
    
    Args:
        data: DataFrame, dictionary, or list of values
        x_col: Column name for x-axis (categories)
        y_col: Column name for y-axis (values)
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Bar color
        figsize: Figure size as (width, height)
        horizontal: If True, create horizontal bar chart
        show_values: If True, display values on bars
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'Store': ['Walmart', 'Kroger', 'Target', 'Costco'],
        ...     'Revenue': [559, 132, 93, 166]
        ... })
        >>> create_bar_chart(data, x_col='Store', y_col='Revenue',
        ...                  title='Revenue by Store (Billions)',
        ...                  ylabel='Revenue ($B)')
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Handle different input types
    if isinstance(data, pd.DataFrame):
        if x_col and y_col:
            x_data = data[x_col]
            y_data = data[y_col]
        else:
            # Use first two columns
            x_data = data.iloc[:, 0]
            y_data = data.iloc[:, 1]
    elif isinstance(data, dict):
        x_data = list(data.keys())
        y_data = list(data.values())
    else:
        x_data = range(len(data))
        y_data = data
    
    # Create bar chart
    if horizontal:
        bars = ax.barh(x_data, y_data, color=color)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        bars = ax.bar(x_data, y_data, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Add value labels on bars if requested
    if show_values:
        for i, bar in enumerate(bars):
            if horizontal:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{y_data.iloc[i] if isinstance(y_data, pd.Series) else y_data[i]:.1f}',
                       ha='left', va='center', fontsize=10)
            else:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height,
                       f'{y_data.iloc[i] if isinstance(y_data, pd.Series) else y_data[i]:.1f}',
                       ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_pie_chart(
    data: Union[pd.DataFrame, dict, list],
    labels: Optional[List[str]] = None,
    values_col: Optional[str] = None,
    labels_col: Optional[str] = None,
    title: str = "Pie Chart",
    colors: Optional[List[str]] = None,
    explode: Optional[List[float]] = None,
    autopct: str = '%1.1f%%',
    figsize: Tuple[int, int] = (8, 8),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create a pie chart to show proportions of a whole.
    
    zyBooks Reference: Section 1.6 - Pie Charts
    
    Key Concepts:
    - Shows parts of a whole (percentages)
    - Best for: market share, budget allocation, category distribution
    - Limit to 5-7 slices for readability
    - Not ideal for precise comparisons (use bar chart instead)
    
    Args:
        data: DataFrame, dictionary, or list of values
        labels: Category labels
        values_col: Column name for values
        labels_col: Column name for labels
        title: Chart title
        colors: List of colors for each slice
        explode: List of offset values for each slice (0=no offset)
        autopct: Format string for percentage labels
        figsize: Figure size as (width, height)
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> data = {'Product A': 35, 'Product B': 28, 'Product C': 22, 'Other': 15}
        >>> create_pie_chart(data, title='Market Share by Product')
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Handle different input types
    if isinstance(data, pd.DataFrame):
        if values_col and labels_col:
            values = data[values_col]
            labels = data[labels_col]
        else:
            values = data.iloc[:, 1] if len(data.columns) > 1 else data.iloc[:, 0]
            labels = data.iloc[:, 0] if len(data.columns) > 1 else data.index
    elif isinstance(data, dict):
        labels = list(data.keys())
        values = list(data.values())
    else:
        values = data
        if labels is None:
            labels = [f"Category {i+1}" for i in range(len(data))]
    
    # Use default color palette if not provided
    if colors is None:
        colors = sns.color_palette("husl", len(values))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        explode=explode,
        autopct=autopct,
        startangle=90,
        textprops={'fontsize': 10}
    )
    
    # Make percentage text bold and white
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.axis('equal')  # Equal aspect ratio ensures circular pie
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_histogram(
    data: Union[pd.DataFrame, pd.Series, np.ndarray, list],
    column: Optional[str] = None,
    bins: Union[int, str, List[float]] = 'auto',
    title: str = "Histogram",
    xlabel: str = "Value",
    ylabel: str = "Frequency",
    color: str = "skyblue",
    edgecolor: str = "black",
    density: bool = False,
    kde: bool = False,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create a histogram to show distribution of numerical data.
    
    zyBooks Reference: Section 1.7 - Histograms
    
    Key Concepts:
    - Shows frequency distribution of continuous data
    - Bins group data into intervals
    - Shape reveals: normal, skewed, uniform, bimodal distributions
    - Best for: test scores, ages, temperatures, measurements
    
    Args:
        data: DataFrame, Series, array, or list of numerical values
        column: Column name if data is DataFrame
        bins: Number of bins, 'auto', or list of bin edges
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Bar color
        edgecolor: Edge color for bars
        density: If True, normalize to show probability density
        kde: If True, overlay kernel density estimate curve
        figsize: Figure size as (width, height)
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> import numpy as np
        >>> test_scores = np.random.normal(75, 10, 100)  # Mean=75, SD=10
        >>> create_histogram(test_scores, bins=15,
        ...                  title='Distribution of Test Scores',
        ...                  xlabel='Score', kde=True)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Handle different input types
    if isinstance(data, pd.DataFrame):
        if column:
            values = data[column].dropna()
        else:
            values = data.iloc[:, 0].dropna()
    elif isinstance(data, pd.Series):
        values = data.dropna()
    else:
        values = np.array(data)
        values = values[~np.isnan(values)]
    
    # Create histogram
    n, bins_edges, patches = ax.hist(
        values,
        bins=bins,
        color=color,
        edgecolor=edgecolor,
        density=density,
        alpha=0.7
    )
    
    # Add KDE if requested
    if kde:
        from scipy import stats
        kde_xs = np.linspace(values.min(), values.max(), 200)
        kde = stats.gaussian_kde(values)
        
        if density:
            ax.plot(kde_xs, kde(kde_xs), 'r-', linewidth=2, label='KDE')
        else:
            # Scale KDE to match histogram
            ax_twin = ax.twinx()
            ax_twin.plot(kde_xs, kde(kde_xs), 'r-', linewidth=2, label='KDE')
            ax_twin.set_ylabel('Density', color='r')
            ax_twin.tick_params(axis='y', labelcolor='r')
            ax.legend(['Histogram'], loc='upper left')
            ax_twin.legend(['KDE'], loc='upper right')
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add statistics text box
    stats_text = f'Mean: {np.mean(values):.2f}\nMedian: {np.median(values):.2f}\nStd Dev: {np.std(values):.2f}'
    ax.text(0.98, 0.97, stats_text,
            transform=ax.transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_scatter_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Scatter Plot",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "steelblue",
    size: Union[int, str] = 50,
    alpha: float = 0.6,
    trend_line: bool = False,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create a scatter plot to show relationship between two numerical variables.
    
    zyBooks Reference: Section 1.8 - Scatter Plots
    
    Key Concepts:
    - Shows correlation between two variables
    - Pattern reveals: positive, negative, or no correlation
    - Helps identify outliers and clusters
    - Best for: height vs weight, study time vs grades, price vs sales
    
    Args:
        data: DataFrame containing x and y columns
        x_col: Column name for x-axis variable
        y_col: Column name for y-axis variable
        title: Chart title
        xlabel: X-axis label (defaults to x_col)
        ylabel: Y-axis label (defaults to y_col)
        color: Point color
        size: Point size (int) or column name for size variable
        alpha: Transparency (0=transparent, 1=opaque)
        trend_line: If True, add linear regression line
        figsize: Figure size as (width, height)
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'study_hours': [2, 4, 3, 5, 1, 6, 3, 4, 5, 2],
        ...     'test_score': [65, 85, 75, 90, 60, 95, 70, 80, 88, 68]
        ... })
        >>> create_scatter_plot(data, 'study_hours', 'test_score',
        ...                     title='Study Time vs Test Score',
        ...                     trend_line=True)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set default labels
    if xlabel is None:
        xlabel = x_col
    if ylabel is None:
        ylabel = y_col
    
    # Handle size parameter
    if isinstance(size, str):
        sizes = data[size]
    else:
        sizes = size
    
    # Create scatter plot
    scatter = ax.scatter(
        data[x_col],
        data[y_col],
        s=sizes,
        c=color,
        alpha=alpha,
        edgecolors='black',
        linewidths=0.5
    )
    
    # Add trend line if requested
    if trend_line:
        # Calculate linear regression
        x = data[x_col].values
        y = data[y_col].values
        
        # Remove NaN values
        mask = ~np.isnan(x) & ~np.isnan(y)
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) > 1:
            z = np.polyfit(x_clean, y_clean, 1)
            p = np.poly1d(z)
            
            x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
            ax.plot(x_line, p(x_line), "r--", linewidth=2, label=f'y={z[0]:.2f}x+{z[1]:.2f}')
            
            # Calculate correlation coefficient
            corr = np.corrcoef(x_clean, y_clean)[0, 1]
            ax.text(0.05, 0.95, f'Correlation: {corr:.3f}',
                   transform=ax.transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                   fontsize=10)
            
            ax.legend()
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig
