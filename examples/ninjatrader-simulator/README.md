# BabySolvernMACross - NinjaTrader 8 Trading Simulator

A custom NinjaTrader 8 NinjaScript strategy implementing a simple Moving Average Crossover Simulator (our "solvern"). This strategy runs simulation trades on historical or live market data to test trading ideas without risking real capital.

## 🎯 What This Does

The **BabySolvernMACross** strategy is a complete automated trading simulator that:

- Tracks two EMAs (Exponential Moving Averages): Fast (9-period) and Slow (21-period)
- **Buy Signal**: When the fast EMA crosses above the slow EMA (bullish signal)
- **Sell Signal**: When the fast EMA crosses below the slow EMA (bearish signal)
- Logs all trades to the NinjaTrader Output window
- Plots both MA lines on your chart for visual analysis
- Runs entirely in simulation mode - no live money at risk

## 🚀 Quick Setup (5 Minutes)

### Prerequisites

1. **NinjaTrader 8 Desktop** - [Download Free](https://ninjatrader.com/Free)
2. **Data Feed** - Free CME simulation feed works great

### Step 1: Enable Simulation Mode

1. Open NinjaTrader 8
2. Go to `Tools > Options > Simulator` tab
3. Check **"Start in Simulation Mode"** for safety
4. Or select `Sim101` account from any chart/SuperDOM dropdown

### Step 2: Get Historical Data (for Backtesting)

1. Go to `Tools > Historical Data Manager`
2. Select instrument (e.g., ES, NQ futures)
3. Download 6-12 months of daily/intraday bars
4. Wait for download to complete

### Step 3: Install the Strategy

1. Open NinjaTrader Control Center
2. Go to `New > NinjaScript Editor`
3. Right-click `Strategies` folder > `New Strategy`
4. Name it: `BabySolvernMACross`
5. Click through the wizard (defaults are fine)
6. **Unlock the code pane** (button at top)
7. Replace all code with contents of `BabySolvernMACross.cs`
8. Press `F5` to compile (green checkmark = success!)
9. Close the editor

## 📊 Running the Simulation

### Method 1: Live Chart Simulation

1. Open a chart: `New > Chart`
2. Select ES or NQ, 5-minute timeframe
3. Right-click chart > `Strategies`
4. Select `BabySolvernMACross` > OK
5. Set parameters:
   - Fast Period: `9`
   - Slow Period: `21`
   - Quantity: `1` contract
6. Watch it trade in real-time on sim data!

### Method 2: Backtest (Recommended First)

1. Go to `Tools > Strategy Analyzer`
2. Load `BabySolvernMACross` strategy
3. Select instrument and date range (e.g., ES, last 6 months)
4. Click **Backtest**
5. Review reports:
   - P&L Summary
   - Trade list
   - Equity curve
   - Win rate & drawdown stats

### Method 3: Market Replay

1. Go to `Tools > Market Replay`
2. Load historical data for your instrument
3. Apply the strategy to a replay chart
4. Play at 1x, 2x, or faster speed
5. Watch the strategy auto-trade through history

### Method 4: Fake Data Testing

1. Go to `Connections > Configure`
2. Add **Simulated Data Feed**
3. Connect to it
4. Use sliders to create fake up/down trends
5. Test "what if" scenarios

## ⚙️ Strategy Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Fast MA Period | 9 | Period for the fast EMA (signal line) |
| Slow MA Period | 21 | Period for the slow EMA (trend line) |
| Quantity | 1 | Number of contracts per trade |

## 🔧 Customization Ideas

### Add RSI Filter

In `OnBarUpdate()`, skip overbought conditions:

```csharp
if (RSI(14, 3)[0] > 70) 
    return;  // Skip buy signals when overbought
```

### Add Stop Loss

Add risk management in `OnBarUpdate()`:

```csharp
SetStopLoss(CalculationMode.Percent, 1);  // 1% stop loss
```

### Add Visual Arrows

Show buy/sell arrows on chart:

```csharp
if (CrossAbove(fastMA, slowMA, 1))
{
    Draw.ArrowUp(this, "Buy"+CurrentBar, false, 0, Low[0] - 2*TickSize, Brushes.Green);
    EnterLong(Quantity, "BabyLong");
}
```

### Change to SMA Instead of EMA

```csharp
// In OnStateChange() DataLoaded section:
fastMA = SMA(Close, FastPeriod);  // Simple Moving Average
slowMA = SMA(Close, SlowPeriod);
```

## 📈 Expected Outputs

When running, you'll see in the **NinjaScript Output** window:

```
11/28/2025 09:35:00: Baby BUY at 5925.50
11/28/2025 10:15:00: Baby SELL at 5932.25
11/28/2025 11:20:00: Baby BUY at 5928.75
...
```

### Strategy Analyzer Reports

After backtesting, you'll get:
- **Net Profit**: Total P&L
- **Win Rate**: Percentage of winning trades
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return metric
- **Profit Factor**: Gross profit / Gross loss

## 🛠 Troubleshooting

### Compile Errors

- Check for missing semicolons
- Ensure all `using` statements are present
- Verify NinjaTrader 8 assemblies are referenced

### Strategy Not Appearing

1. Verify compilation succeeded (green checkmark)
2. Restart NinjaTrader
3. Check `Documents\NinjaTrader 8\bin\Custom\Strategies\`

### No Trades Executing

- Ensure enough historical bars (min 21 for slow MA)
- Verify you're connected to a data feed
- Check that strategy is enabled on the chart

### Data Issues

- Use `Tools > Historical Data Manager` to verify data exists
- Try downloading fresh data for your instrument

## 📚 Learn More

- **NinjaTrader 8 Documentation**: [ninjatrader.com/support](https://ninjatrader.com/support)
- **NinjaScript Reference**: [Help Guide](https://ninjatrader.com/support/helpGuides/nt8/)
- **Community Forums**: [forum.ninjatrader.com](https://forum.ninjatrader.com)
- **Recommended Book**: "NinjaTrader 8 Programming" (~$20-30 on Amazon)

## 🎓 Next Steps

1. **Run backtests** on ES/NQ with different MA periods
2. **Add filters** (RSI, volume, time of day)
3. **Implement stop losses** and profit targets
4. **Try different instruments** (stocks, forex, crypto)
5. **Explore Strategy Builder** for no-code strategy creation

## ⚠️ Disclaimer

This is a **simulation-only** educational tool. No live trading functionality is enabled by default. Always:

- Test thoroughly in simulation before any live trading
- Understand the risks of futures/options trading
- Never risk money you can't afford to lose
- Past performance does not guarantee future results

---

*Built as part of the Strategickhaos Sovereignty Architecture ecosystem* 🔥
