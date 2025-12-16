"""
Advanced Line Charts with Real Financial Data using yfinance
Section 1.8 - Python Function 1.8.1: Financial data

This module demonstrates how to fetch real financial data from Yahoo Finance
and create line charts, as described in the zyBooks section.

Note: This requires the yfinance library:
    pip install yfinance matplotlib
"""

import matplotlib.pyplot as plt

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Install with: pip install yfinance")


def fetch_and_plot_stock(ticker: str, start_date: str, end_date: str, output_file: str):
    """
    Fetch stock data from Yahoo Finance and create a line chart.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'TGT', 'AAPL', 'GOOGL')
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        output_file: Path to save the chart image
    """
    if not YFINANCE_AVAILABLE:
        print("Error: yfinance library is required. Install with: pip install yfinance")
        return
    
    try:
        # Download stock data
        print(f"Fetching {ticker} stock data from {start_date} to {end_date}...")
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if stock_data.empty:
            print(f"Error: No data found for {ticker}")
            return
        
        # Create the line chart
        plt.figure(figsize=(14, 7))
        plt.plot(stock_data.index, stock_data['Close'], linewidth=2, color='blue')
        
        # Add title and labels
        plt.title(f'{ticker} Closing Stock Prices ({start_date} to {end_date})', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Stock price (USD)', fontsize=12)
        
        # Add grid for better readability
        plt.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Tight layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {output_file}")
        
        # Display some statistics
        print(f"\nStatistics for {ticker}:")
        print(f"  Start price: ${stock_data['Close'].iloc[0]:.2f}")
        print(f"  End price: ${stock_data['Close'].iloc[-1]:.2f}")
        print(f"  Change: ${stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]:.2f}")
        print(f"  Percent change: {((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100:.2f}%")
        print(f"  Max price: ${stock_data['Close'].max():.2f}")
        print(f"  Min price: ${stock_data['Close'].min():.2f}")
        
        plt.close()
        
    except Exception as e:
        print(f"Error fetching or plotting data: {e}")


def example_target_stock():
    """
    Example from zyBooks: Target (TGT) stock from 1983 to 2024
    This matches the example in Python Function 1.8.1
    """
    print("\n" + "="*70)
    print("Example: Target (TGT) Closing Stock Prices")
    print("="*70 + "\n")
    
    if not YFINANCE_AVAILABLE:
        print("Please install yfinance: pip install yfinance")
        return
    
    fetch_and_plot_stock(
        ticker='TGT',
        start_date='1983-01-01',
        end_date='2024-11-30',  # Use a past date to ensure data availability
        output_file='tgt_stock_yfinance.png'
    )


def example_apple_stock_2015_2016():
    """
    Example: Apple (AAPL) stock from March 2015 to March 2016
    This matches the zyBooks example in section 1.8
    """
    print("\n" + "="*70)
    print("Example: Apple (AAPL) Stock Prices (March 2015 - March 2016)")
    print("="*70 + "\n")
    
    if not YFINANCE_AVAILABLE:
        print("Please install yfinance: pip install yfinance")
        return
    
    fetch_and_plot_stock(
        ticker='AAPL',
        start_date='2015-03-01',
        end_date='2016-03-31',
        output_file='aapl_stock_yfinance.png'
    )


def example_google_stock_2015_2016():
    """
    Example: Alphabet/Google (GOOGL) stock from March 2015 to March 2016
    This matches the zyBooks example in section 1.8
    """
    print("\n" + "="*70)
    print("Example: Alphabet/Google (GOOGL) Stock (March 2015 - March 2016)")
    print("="*70 + "\n")
    
    if not YFINANCE_AVAILABLE:
        print("Please install yfinance: pip install yfinance")
        return
    
    fetch_and_plot_stock(
        ticker='GOOGL',
        start_date='2015-03-01',
        end_date='2016-03-31',
        output_file='googl_stock_yfinance.png'
    )


def compare_multiple_stocks():
    """
    Advanced example: Compare multiple stocks on one chart
    Demonstrates multiple datasets like the temperature examples
    """
    print("\n" + "="*70)
    print("Example: Comparing Multiple Tech Stocks (2015-2016)")
    print("="*70 + "\n")
    
    if not YFINANCE_AVAILABLE:
        print("Please install yfinance: pip install yfinance")
        return
    
    try:
        # Download data for multiple stocks
        tickers = ['AAPL', 'GOOGL', 'MSFT']
        start_date = '2015-03-01'
        end_date = '2016-03-31'
        
        print(f"Fetching data for {', '.join(tickers)}...")
        
        plt.figure(figsize=(14, 7))
        
        colors = ['blue', 'green', 'red']
        markers = ['o', 's', '^']
        
        for idx, ticker in enumerate(tickers):
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if not data.empty:
                # Normalize to percentage change from first day
                normalized = (data['Close'] / data['Close'].iloc[0] - 1) * 100
                plt.plot(data.index, normalized, 
                        label=ticker, 
                        color=colors[idx], 
                        linewidth=2,
                        marker=markers[idx],
                        markersize=4,
                        markevery=10)
                
                print(f"  {ticker}: {((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100:+.2f}% change")
        
        plt.title('Tech Stock Performance Comparison (March 2015 - March 2016)\nNormalized to Starting Price', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Percentage Change from Start (%)', fontsize=12)
        plt.legend(loc='best', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_file = 'tech_stocks_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Chart saved to: {output_file}")
        plt.close()
        
    except Exception as e:
        print(f"Error: {e}")


def run_all_yfinance_examples():
    """
    Run all yfinance examples
    
    Note: These examples require internet connection and the yfinance library.
    Install with: pip install yfinance
    """
    if not YFINANCE_AVAILABLE:
        print("\n" + "="*70)
        print("ERROR: yfinance library not installed")
        print("="*70)
        print("\nTo run these examples, install yfinance:")
        print("    pip install yfinance")
        print("\nOr install all requirements:")
        print("    pip install -r requirements_line_charts.txt")
        print("\n" + "="*70)
        return
    
    print("\n" + "="*70)
    print("REAL FINANCIAL DATA LINE CHARTS - Using yfinance")
    print("="*70 + "\n")
    
    print("Note: Fetching real data from Yahoo Finance...")
    print("This requires an internet connection.\n")
    
    # Run examples
    example_apple_stock_2015_2016()
    example_google_stock_2015_2016()
    compare_multiple_stocks()
    
    # Optional: Target stock (large date range, may take longer)
    # example_target_stock()
    
    print("\n" + "="*70)
    print("✓ All yfinance examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_yfinance_examples()
