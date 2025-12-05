# PID-RANCO Quick Start Guide

> **Deploy in 5 minutes. Love compiles profit in 99 trades.**

## Prerequisites Check

- [ ] Windows with PowerShell 5.1+
- [ ] NinjaTrader 8 or 9 installed
- [ ] .NET Framework 4.8+
- [ ] (Optional) Microphone for voice input
- [ ] (Optional) Biometric sensors

## Step 1: Get the Files (30 seconds)

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

## Step 2: Deploy to NinjaTrader (2 minutes)

### For Testing (Simulation Mode) ✅ RECOMMENDED FIRST

```powershell
.\deploy-pid-ranco.ps1 -Market sim -Verify
```

### For Live Trading ⚠️ REAL MONEY

```powershell
.\deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

You'll be asked to type: `LOVE COMPILES PROFIT` to confirm.

## Step 3: Configure in NinjaTrader (2 minutes)

1. **Open NinjaTrader**
2. **Tools → Strategies**
3. **Find "LoveCompilesProfit"**
4. **Right-click → Apply to Chart**
5. **Configure Parameters** (or use defaults):
   - RSI Period: 14
   - Risk Percent: 0.69
   - Stop Loss: 2.0%
   - Take Profit: 1.618%
6. **Enable Strategy**

## Step 4: Monitor (Ongoing)

Watch for these events:
- 💚 **Trade Entries**: Based on RSI + Love Factor
- 📈 **Exits**: Take profit at 1.618% (golden ratio)
- 🔄 **Evolution**: After 99 losses, strategy mutates
- 🎉 **100th Trade**: Must be green (profitable)

## Configuration Files

| File | Purpose |
|------|---------|
| `pid-ranco-trading-bot.yaml` | All parameters and settings |
| `LoveCompilesProfit.cs` | NinjaTrader strategy code |
| `deploy-pid-ranco.ps1` | Deployment automation |
| `notify-her.ps1` | Notification system |

## Key Parameters

Edit in NinjaTrader Strategy Properties:

```
RSI Oversold: 30       # Buy signal threshold
RSI Overbought: 70     # Sell signal threshold
Risk Percent: 0.69     # Risk per trade (sacred number)
Stop Loss %: 2.0       # Maximum loss per trade
Take Profit %: 1.618   # Golden ratio profit target
```

## Safety Features

✅ **Default to Simulation**: Never trades live without confirmation  
✅ **Auto Backup**: Creates backup before deployment  
✅ **Stop Loss**: Always enabled at 2%  
✅ **Love Override**: Exits if emotional state is low  
✅ **Evolution Protocol**: Learns from 99 failures  

## Notifications Setup (Optional)

### Discord Webhook

```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
$env:ENABLE_DISCORD_NOTIFICATIONS = "true"
```

### Email

```powershell
$env:NOTIFICATION_EMAIL = "your@email.com"
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your@email.com"
$env:SMTP_PASS = "your-app-password"
$env:ENABLE_EMAIL_NOTIFICATIONS = "true"
```

### SMS (Twilio)

```powershell
$env:NOTIFICATION_PHONE = "+1234567890"
$env:TWILIO_ACCOUNT_SID = "ACxxxxx"
$env:TWILIO_AUTH_TOKEN = "your-token"
$env:TWILIO_FROM_NUMBER = "+1234567890"
$env:ENABLE_SMS_NOTIFICATIONS = "true"
```

## Common Issues

### "Strategy won't compile"
- Check NinjaTrader version (must be 8 or 9)
- Verify .NET Framework 4.8+ installed
- Look for errors in NinjaTrader Output Window

### "No trades executing"
- Check RSI values (must be <30 for long entry)
- Verify love factor >0.5 (simulated by default)
- Ensure strategy is enabled on chart
- Check account has sufficient capital

### "Deployment failed"
- Run PowerShell as Administrator
- Check NinjaTrader path is correct
- Verify files exist in repository

## Understanding the System

### PID Controller
Calculates optimal position based on:
- **P**: Current price distance from target
- **I**: Accumulated error over time
- **D**: Rate of change in error

### RANCO Optimizer
Risk-adjusted position sizing:
- Calculates position size based on account risk
- Applies love factor multiplier
- Enforces stop loss and take profit

### Apoptosis Protocol
Evolution through failure:
```
99 losing trades → Mutation → Evolved strategy → 100th trade must be green
```

### Love Factor
Emotional state influences trading:
- **High** (>0.8): Aggressive entries
- **Medium** (0.5-0.8): Normal trading
- **Low** (<0.5): Exit all positions

## Testing Checklist

Before going live:

- [ ] Deployed in simulation mode
- [ ] Strategy compiles without errors
- [ ] Can see strategy in NinjaTrader
- [ ] Applied strategy to chart
- [ ] Enabled strategy
- [ ] Observed at least 10 trades
- [ ] Verified stop loss works
- [ ] Checked take profit executes
- [ ] Reviewed logs and output
- [ ] Comfortable with parameters

## Performance Targets

| Metric | Target | Purpose |
|--------|--------|---------|
| Win Rate | >51% | Just above random chance |
| Profit Factor | 1.618 | Golden ratio efficiency |
| Max Drawdown | <3.37% | Her birthday reversed |
| Risk/Reward | 1:1.618 | Asymmetric advantage |

## Next Steps

1. **Read Full Docs**: [README-PID-RANCO.md](README-PID-RANCO.md)
2. **Join Community**: Discord server for support
3. **Optimize Parameters**: Tune for your market/timeframe
4. **Monitor Evolution**: Track the 99→1 cycle
5. **Share Results**: Contribute back to the project

## Philosophy

> "This isn't just a trading bot. This is the first financial instrument that literally trades on love."

### The Axiom
```
Love compiles profit. Always.
```

### The Promise
```
99 reds → Evolution
1 green → Victory
Her name → Forever on the chart
```

## Emergency Stop

To stop trading immediately:

1. **In NinjaTrader**: Click "Disable" on strategy
2. **In PowerShell**: 
   ```powershell
   .\notify-her.ps1 "Emergency stop requested" -Type Warning
   ```
3. **Flat All Positions**: Tools → Account → Flatten Everything

## Support

- **Documentation**: [README-PID-RANCO.md](README-PID-RANCO.md)
- **Issues**: GitHub issue tracker
- **Discord**: StrategicKhaos community
- **Email**: support@strategickhaos.com

## One-Liner Deploy

```powershell
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git && cd Sovereignty-Architecture-Elevator-Pitch- && .\deploy-pid-ranco.ps1 -Market sim -Verify
```

---

**Ready?**

```powershell
.\deploy-pid-ranco.ps1 -Market sim
```

**Let love compile profit. Always.**

---

*StrategicKhaos PID-RANCO Trading Engine v1.0*  
*Built with 💚 for the throne*  
*2025-11-24*
