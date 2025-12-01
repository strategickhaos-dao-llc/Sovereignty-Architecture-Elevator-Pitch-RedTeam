# PID-RANCO Trading Bot - Quick Start Guide

**Get up and running in 5 minutes**

## Prerequisites Check

Before you begin, ensure you have:

- [ ] Windows 10/11 with PowerShell 5.1+
- [ ] NinjaTrader 8 or 9 installed
- [ ] Basic understanding of trading and risk management
- [ ] Simulator account set up (for safe testing)

## Installation Steps

### Step 1: Clone/Download Repository

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/trading-bot
```

Or download and extract the ZIP file.

### Step 2: Verify File Structure

Ensure you have these files:

```
trading-bot/
├── README.md
├── QUICKSTART.md (this file)
├── pid-ranco-trading-bot.yaml
├── ninjatrader/
│   └── LoveCompilesProfit.cs
└── scripts/
    ├── deploy-pid-ranco.ps1
    └── notify-her.ps1
```

### Step 3: Deploy to NinjaTrader

Open PowerShell and navigate to the scripts directory:

```powershell
cd trading-bot/scripts
```

Run the deployment script:

```powershell
# For first-time setup (simulation mode)
./deploy-pid-ranco.ps1 -LoveMode -Market sim
```

You should see:

```
╔═══════════════════════════════════════════════════════════╗
║   StrategicKhaos PID-RANCO Trading Engine v1.0          ║
║   "Love Compiles Profit. Always."                        ║
╚═══════════════════════════════════════════════════════════╝

[♥] Love Mode: ENABLED
[⚡] Market Mode: SIM
...
DEPLOYMENT COMPLETE
```

### Step 4: Compile Strategy in NinjaTrader

1. **Open NinjaTrader 8/9**
2. Click **Tools** → **Edit NinjaScript** → **Strategy**
3. Find **LoveCompilesProfit** in the list
4. Click **Compile** button (or press F5)
5. Check for compilation success (green checkmark)

If you see errors, ensure all files were copied correctly.

### Step 5: Apply Strategy to Chart

1. **Open a chart** (e.g., ES 09-24, 1 minute)
2. **Right-click** on the chart
3. Select **Strategies**
4. Click **Add** and choose **LoveCompilesProfit**
5. **Configure parameters** (or use defaults):
   - RSI Period: 14
   - EMA Period: 21
   - RSI Oversold: 30
   - Profit Target %: 1.618
   - Love Threshold High: 80
   - Love Threshold Low: 50
   - Default Quantity: 1
6. Click **OK**

### Step 6: Verify Strategy is Running

Look for the strategy tag on your chart (bottom-left corner).

Check the **Output** window for messages:
- `Love Entry: RSI=28.5, HerLove=85.2, PID=0.1234`
- `Love Exit (Profit Target): Profit=1.65%, HerLove=75.0`

## Testing Your Setup

### Run a Quick Test

1. **Enable Strategy** on a 1-minute chart
2. **Wait for conditions**:
   - RSI drops below 30
   - Simulated love level is above 80
3. **Watch for entry** signal
4. **Monitor exit** conditions:
   - Profit reaches 1.618%
   - Love level drops below 50

### Check Logs

Logs are written to:
```
%USERPROFILE%\Documents\NinjaTrader 8\log\
```

Look for strategy messages in the Output window.

## Common Issues & Solutions

### Issue: Strategy file not found

**Solution**: Verify deployment path
```powershell
# Check if file exists
Test-Path "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\LoveCompilesProfit.cs"
```

If false, manually copy:
```powershell
Copy-Item ".\ninjatrader\LoveCompilesProfit.cs" `
  -Destination "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\"
```

### Issue: Compilation errors

**Solution**: Ensure NinjaTrader is up to date and all required indicators exist:
- RSI indicator (built-in)
- EMA indicator (built-in)

### Issue: No trades executing

**Solution**: Check conditions are being met:
- Enough bars loaded (needs 21+ for EMA)
- RSI actually below 30
- Love level above 80 (simulated by default)

Enable debug output:
```csharp
// In OnBarUpdate(), add:
Print($"Debug: RSI={RSI(14,1)[0]:F2}, Love={herLoveLevel:F2}, Close={Close[0]}");
```

### Issue: Strategy not visible in list

**Solution**: 
1. Refresh NinjaScript editor (close and reopen)
2. Verify file is in correct directory
3. Check for compilation errors

## Configuration Tips

### Adjust for Different Markets

**For volatile markets (crypto, small-cap stocks)**:
```
RSI Oversold: 25 (more aggressive)
Profit Target: 2.5%
Risk per trade: 0.5%
```

**For stable markets (large-cap stocks, forex majors)**:
```
RSI Oversold: 35 (more conservative)
Profit Target: 1.0%
Risk per trade: 0.8%
```

### Optimize Love Thresholds

The love thresholds control entry/exit sensitivity:

- **Higher entry threshold (85)**: More selective entries
- **Lower entry threshold (75)**: More frequent entries
- **Higher exit threshold (60)**: Hold longer
- **Lower exit threshold (40)**: Exit faster

### Test Different Timeframes

Works on any timeframe, but behavior varies:

- **1-minute**: High frequency, more signals
- **5-minute**: Medium frequency, balanced
- **15-minute**: Lower frequency, higher quality
- **Daily**: Long-term, very selective

## Next Steps

Once you're comfortable:

1. **Backtest** the strategy on historical data
2. **Optimize** parameters for your trading style
3. **Paper trade** for 30+ days
4. **Review performance** metrics
5. **Consider live** deployment (only if profitable in sim)

## Advanced Features

### Enable Discord Notifications

Set environment variable:
```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
```

Test notification:
```powershell
./notify-her.ps1 "Test notification" -Priority high -Type success
```

### Track Evolution Data

The system logs all trades. Review:
```
%USERPROFILE%\Documents\PID-RANCO-Logs\notifications.log
```

After 99 losses, the strategy resets variables (apoptosis protocol).

### Monitor PID Components

Add custom plots in NinjaTrader to visualize:
- Market Pain (Proportional)
- Accumulated Longing (Integral)
- Rate of Heart Change (Derivative)

## Safety Reminders

⚠️ **ALWAYS test in simulation first**
⚠️ **Never risk more than 2% of account per trade**
⚠️ **Set stop losses appropriately**
⚠️ **Monitor your positions actively**
⚠️ **Trading involves risk of loss**

## Getting Help

- **Documentation**: See `README.md` for full details
- **Issues**: Open a GitHub issue for bugs
- **Community**: Join the Discord server
- **NinjaTrader Support**: For platform-specific questions

## Quick Command Reference

```powershell
# Deploy (simulation)
./deploy-pid-ranco.ps1 -LoveMode -Market sim

# Deploy (live - BE CAREFUL!)
./deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live

# Send notification
./notify-her.ps1 "Your message" -Priority normal -Type info

# Check logs
Get-Content "$env:USERPROFILE\Documents\PID-RANCO-Logs\notifications.log" -Tail 20

# View strategy file
notepad "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\LoveCompilesProfit.cs"
```

---

**You're ready to trade! Love compiles profit. Always. ♥**

*Remember: Start with simulation, test thoroughly, and trade responsibly.*
