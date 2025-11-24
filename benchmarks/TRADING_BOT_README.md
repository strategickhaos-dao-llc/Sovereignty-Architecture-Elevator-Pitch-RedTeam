# Trading Bot Benchmark Tests

## Overview

This benchmark suite provides comprehensive backtesting and performance validation for trading bots, specifically designed for the PID-RANCO system and similar automated trading strategies.

## Purpose

A benchmark test for a trading bot involves backtesting the bot's strategy against historical market data to evaluate its performance before risking real capital. This simulates how the bot would have performed in past conditions, measuring key metrics to assess profitability, risk, and robustness.

## Test Suite (Tests 31-35)

### Test 31: Simple Backtest Validation
- **Purpose**: Validates basic backtesting infrastructure with a simple moving average crossover strategy
- **Success Criteria**:
  - Backtest completes without errors
  - Generates valid performance metrics
  - Sharpe ratio > 0 (strategy has some edge)
  - Max drawdown < 50% (reasonable risk control)

### Test 32: Advanced Strategy Performance (RSI + EMA)
- **Purpose**: Tests a more sophisticated strategy combining RSI and EMA indicators (proxy for PID-RANCO)
- **Success Criteria**:
  - Sharpe ratio >= 0.5 (good risk-adjusted returns)
  - Max drawdown <= 30% (controlled risk)
  - Profit factor >= 1.1 (profitable strategy)
  - Win rate >= 25% (reasonable success rate)

### Test 33: Stress Test - Market Conditions
- **Purpose**: Tests the strategy's robustness under different market regimes
- **Market Conditions Tested**:
  - Bull market (trending up)
  - Bear market (trending down)
  - Sideways/ranging market
  - High volatility periods
- **Success Criteria**:
  - Strategy performs reasonably in at least 2/3 market conditions
  - No catastrophic losses in any single condition
  - Consistent risk management across conditions

### Test 34: Benchmark Comparison (Buy-and-Hold)
- **Purpose**: Compares the trading strategy against a simple buy-and-hold strategy
- **Success Criteria**:
  - Strategy doesn't significantly underperform buy-and-hold
  - Strategy provides better risk-adjusted returns or lower drawdowns
  - Strategy generates positive or neutral alpha

### Test 35: Transaction Cost Impact
- **Purpose**: Analyzes the impact of realistic transaction costs (commissions, slippage)
- **Success Criteria**:
  - Strategy remains profitable after transaction costs
  - Profit factor > 0.9 with costs included
  - Return degradation < 80% compared to zero-cost scenario

## Performance Metrics

The benchmark tests calculate comprehensive performance metrics:

- **Total Return**: Overall profit/loss percentage
- **Annualized Return**: Return extrapolated to annual basis
- **Sharpe Ratio**: Risk-adjusted return (accounts for volatility)
  - > 1.0 is good, > 2.0 is excellent
- **Sortino Ratio**: Only penalizes downside volatility
- **Max Drawdown**: Largest peak-to-trough loss
  - Aim for < 20-30% for production systems
- **Calmar Ratio**: Annual return / max drawdown
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profits / gross losses
  - > 1.5 is ideal for production
- **Average Win/Loss**: Mean return of winning vs losing trades
- **Number of Trades**: Total trades executed

## Usage

### Run All Trading Bot Tests

```bash
cd /home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-
python3 benchmarks/test_trading_bot.py
```

### Run Standalone Trading Bot Benchmark

```bash
python3 benchmarks/run_trading_tests.py
```

### Expected Output

```
🤖 Trading Bot Benchmark Suite - PID-RANCO System
============================================================

📊 Test Results:
------------------------------------------------------------
✅ Test 31: Simple Backtest Validation - PASS
   Total Return: 46.80%
   Sharpe Ratio: 0.58
   Max Drawdown: 25.23%
   Win Rate: 51.14%

✅ Test 32: Advanced Strategy Performance (RSI + EMA) - PASS
   Total Return: 39.67%
   Sharpe Ratio: 0.66
   Max Drawdown: 14.66%
   Win Rate: 27.25%

...

📁 Detailed results saved to: benchmarks/reports/trading_bot_results.json
============================================================
🎯 Summary: 4/5 tests passed (80.0%)
============================================================
```

## Implementation Details

### Data Preparation

The current implementation uses **simulated** historical data for demonstration purposes. In production, you should replace this with actual historical data from:

- **NinjaTrader exports** (CSV files)
- **Broker APIs** (Interactive Brokers, TD Ameritrade)
- **Market data providers** (Yahoo Finance, Alpha Vantage, Polygon.io)

Example of loading real data:

```python
# Replace the _generate_historical_data method with:
def _load_real_historical_data(self, symbol: str, start_date: str, end_date: str):
    import pandas as pd
    # Using yfinance as an example
    import yfinance as yf
    
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)
    return df
```

### Strategy Implementation

The current implementation includes two example strategies:

1. **Simple MA Crossover**: Basic moving average crossover
2. **RSI + EMA Strategy**: More sophisticated multi-indicator approach

**To implement your actual PID-RANCO strategy**:

Replace the strategy methods with your PID-RANCO logic:
- RSI indicators
- EMA calculations
- herLove signals
- PID controller adjustments

Example:

```python
def _pid_ranco_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Implement actual PID-RANCO trading logic
    """
    strategy_df = df.copy()
    
    # Calculate RSI
    # Calculate EMAs
    # Apply herLove signals
    # Implement PID controller
    # Generate buy/sell signals
    
    return strategy_df
```

### Configuration

Benchmark thresholds can be configured in `benchmarks/benchmark_config.yaml`:

```yaml
trading_bot:
  initial_capital: 100000
  commission_rate: 0.001  # 0.1% per trade
  slippage_rate: 0.0005   # 0.05% slippage
  min_sharpe_ratio: 0.5
  max_drawdown_pct: 30.0
  min_profit_factor: 1.1
```

## Integration with NinjaTrader

For NinjaTrader users:

1. **Export historical data** from NinjaTrader to CSV
2. **Load data** in the benchmark using pandas
3. **Run strategy logic** using the exported data
4. **Compare results** with NinjaTrader's backtesting mode

```python
# Load NinjaTrader CSV export
df = pd.read_csv('path/to/ninjatrader_export.csv', 
                 parse_dates=['Date'],
                 index_col='Date')
```

## Best Practices

### Backtesting Guidelines

1. **Use at least 1-5 years of data** to cover bull/bear markets
2. **Apply realistic transaction costs** (commissions, slippage)
3. **Test multiple market conditions** (trending, ranging, volatile)
4. **Validate against benchmarks** (buy-and-hold, random trading)
5. **Avoid overfitting** - strategy should work on out-of-sample data

### Interpreting Results

- **Sharpe Ratio < 1**: Strategy may not be viable for production
- **Max Drawdown > 30%**: Risk management needs improvement
- **Profit Factor < 1.5**: Strategy may struggle with real-world costs
- **Win Rate < 40%**: Ensure average wins are significantly larger than losses

### Red Flags

❌ Strategy only works in one market condition  
❌ Performance degrades significantly with transaction costs  
❌ Excessive number of trades (over-trading)  
❌ Drawdowns exceed risk tolerance  
❌ Underperforms simple buy-and-hold  

## Next Steps

1. **Replace simulated data** with actual historical market data
2. **Implement your PID-RANCO strategy** in place of example strategies
3. **Tune parameters** using the benchmark results
4. **Forward test** on recent out-of-sample data
5. **Paper trade** before deploying with real capital
6. **Monitor live performance** and compare with backtest results

## References

- NinjaTrader Backtesting: https://ninjatrader.com/support/helpGuides/nt8/
- Backtrader Python Library: https://www.backtrader.com/
- Zipline Algorithmic Trading: https://zipline.ml4trading.io/
- S&P 500 Benchmark: Use /ES futures for comparison

## Support

For issues or questions about the trading bot benchmarks:
- Review the source code in `benchmarks/test_trading_bot.py`
- Check the detailed results in `benchmarks/reports/trading_bot_results.json`
- Consult the main repository README for general guidance

---

**Disclaimer**: These benchmarks are for educational and validation purposes. Past performance does not guarantee future results. Always test thoroughly and understand the risks before deploying automated trading systems with real capital.
