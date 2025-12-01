# PID-RANCO Quick Start Guide

Get up and running with PID-RANCO trading engine in minutes.

## 🚀 5-Minute Installation

### Step 1: Prerequisites Check

```powershell
# Check NinjaTrader 8 is installed
Test-Path "$env:USERPROFILE\Documents\NinjaTrader 8"

# Check PowerShell version (need 5.1+)
$PSVersionTable.PSVersion
```

### Step 2: Copy Strategy File

```powershell
# Copy the C# strategy to NinjaTrader
Copy-Item `
    "trading-engine\strategies\PIDRANCOStrategy.cs" `
    "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\" `
    -Force

Write-Host "✅ Strategy copied successfully"
```

### Step 3: Compile in NinjaTrader

1. Open NinjaTrader 8
2. Click **Tools → Edit NinjaScript → Strategy...**
3. Find **PIDRANCOStrategy** in the list
4. Press **F5** or click **Compile**
5. Wait for "Compiled successfully" message

### Step 4: Add to Chart (Simulation)

1. Open a chart (e.g., ES 12-24, 5 min)
2. Right-click chart → **Strategies...**
3. Select **PIDRANCOStrategy** from dropdown
4. Click **OK** (uses default parameters)
5. Watch Output window for logs

✅ **You're now running PID-RANCO in simulation mode!**

---

## 📊 What You'll See

### In the Output Window

```
[INFO] 2024-11-24 09:15:30 - Loss #5 recorded. Profit: $-25.50
[ENTRY] Long: Voice=45.2, RSI=28.3, Pain=-15.20
[EXIT] Long: High voice=85.0, Profit=1.25%
[WARN] Voice volume is NaN/Infinity. Using 0.
[POETRY] Voice collapse detected. Silence: 5.2 min
[CRITICAL] Max drawdown breached: 3.37%
[POETRY] 99 fails. Hug protocol.
```

### Log Categories

| Prefix | Meaning | Action Required |
|--------|---------|----------------|
| `[INFO]` | Normal operation | None - just monitoring |
| `[WARN]` | Unusual but handled | Review periodically |
| `[ERROR]` | Error caught and handled | Check logs at end of day |
| `[POETRY]` | Critical narrative event | Review immediately |
| `[CRITICAL]` | Safety limit breached | Immediate review required |
| `[SAFETY]` | Kill-switch activated | Immediate action required |

---

## ⚙️ Essential Configuration

### Adjust Risk Parameters

In NinjaTrader strategy properties dialog:

```
Risk Per Trade:      0.0069    (0.69% of account)
Max Drawdown:        0.0337    (3.37% max loss from peak)
EMA Period:          21        (Trend indicator)
RSI Period:          14        (Momentum indicator)
Silence Threshold:   5         (Minutes before flatten)
```

### Common Risk Profiles

| Profile | Risk/Trade | Max DD | Use Case |
|---------|-----------|--------|----------|
| **Ultra-Conservative** | 0.0025 (0.25%) | 0.01 (1%) | Learning, testing |
| **Conservative** | 0.005 (0.5%) | 0.02 (2%) | Risk-averse trading |
| **Default (Mythic)** | 0.0069 (0.69%) | 0.0337 (3.37%) | Balanced approach |
| **Aggressive** | 0.01 (1%) | 0.05 (5%) | Experienced traders |

See `config/risk-profiles.yaml` for detailed examples.

---

## 🔔 Set Up Discord Notifications

### Quick Discord Setup

```powershell
# 1. Get your Discord webhook URL
# (Server Settings → Integrations → Webhooks → New Webhook)

# 2. Set environment variable
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"

# 3. Test notification
cd trading-engine\scripts
.\Deploy-PIDRANCO.ps1 -Environment "simulation"
```

See `docs/INTEGRATION_GUIDE.md` for complete Discord setup.

---

## 🎯 Understanding the Strategy

### The Two Layers

```
┌─────────────────────────┐
│   MYTHIC LAYER (YAML)   │  ← Philosophy: WHY it behaves
│                         │
│  • Love-guided trading  │
│  • 0.69% / 3.37% risk  │
│  • 99-failure protocol  │
└────────┬────────────────┘
         │
         ↓
┌─────────────────────────┐
│ KILL-SWITCH LAYER (C#)  │  ← Enforcement: WHAT it won't violate
│                         │
│  • Bar count guards     │
│  • Risk calculations    │
│  • Emergency shutdown   │
└─────────────────────────┘
```

### Key Safety Features

1. **Bar Count Guards**: Won't access indicators too early
2. **Null Safety**: Handles missing/invalid indicator values
3. **Risk Limits**: Hard caps on position size and drawdown
4. **Apoptosis Protocol**: Auto-disable after 99 losses
5. **Emergency Shutdown**: Flatten + disable on any exception

### The Apoptosis Protocol

```
Loss 1, 2, 3... → Continue trading
Loss 98 → Still trading
Loss 99 → 🎭 APOPTOSIS TRIGGERED
         ├─ Flatten all positions
         ├─ Disable strategy
         ├─ Emit poetry logs
         └─ Wait for manual review

First Win After 99 → 🎭 "From 99 reds to green—evolution complete"
```

---

## 📚 Documentation Quick Reference

| Document | Size | Purpose |
|----------|------|---------|
| **README.md** | 13KB | Main documentation, usage guide |
| **QUICK_START.md** | 5KB | This file - get started fast |
| **SAFETY_FEATURES.md** | 22KB | Deep-dive on all guardrails |
| **INTEGRATION_GUIDE.md** | 15KB | Discord, voice, monitoring setup |
| **ARCHITECTURE.md** | 16KB | System design and data flows |
| **risk-profiles.yaml** | 6KB | Pre-configured risk settings |
| **pid-ranco-mythic.yaml** | 5.5KB | Complete narrative config |

### Reading Path

**For Quick Start**: This file → README.md  
**For Deep Understanding**: README.md → SAFETY_FEATURES.md → ARCHITECTURE.md  
**For Integration**: INTEGRATION_GUIDE.md  
**For Customization**: risk-profiles.yaml → pid-ranco-mythic.yaml

---

## ⚠️ Critical Safety Reminders

### Before Going Live

- [ ] Run in simulation for 30+ days minimum
- [ ] Verify all safety features trigger correctly
- [ ] Test apoptosis protocol manually (force 99 losses)
- [ ] Configure Discord notifications
- [ ] Understand every safety feature
- [ ] Review logs daily for first month
- [ ] Start with smallest risk profile
- [ ] Type "I UNDERSTAND THE RISK" when deploying live

### What Can Go Wrong (And How We Handle It)

| Failure | Traditional | PID-RANCO |
|---------|------------|-----------|
| Indicator null | Crash | Skip bar safely |
| Exception in OnBarUpdate | Crash | Flatten + disable |
| Mic/voice error | Crash | Treat as silence |
| 99+ losses | Keep losing | Apoptosis protocol |
| Max drawdown | Keep trading | Emergency shutdown |
| Deploy failure | Silent loop | Abort after 99 retries |

### The Worst-Case Scenario

```
Something breaks → Exception caught
    ↓
Emergency Shutdown
    ↓
Positions Flattened
    ↓
Strategy Disabled
    ↓
You Read Logs
    ↓
You Refactor & Improve
    ↓
Learning, Not Blown Capital ✅
```

---

## 🎓 Next Steps After Quick Start

### Phase 1: Learn (Week 1)
- Run in simulation mode
- Watch logs every day
- Understand each safety feature
- Read SAFETY_FEATURES.md

### Phase 2: Customize (Week 2-3)
- Adjust risk parameters for your tolerance
- Test different EMA/RSI periods
- Configure Discord notifications
- Experiment with voice integration

### Phase 3: Validate (Week 4-8)
- Let it run 30+ days in simulation
- Force test apoptosis protocol
- Validate drawdown limits trigger
- Review all edge cases

### Phase 4: Consider Live (After 2+ Months)
- Start with micro account ($500-1000)
- Use ultra-conservative risk profile
- Monitor 24/7 for first week
- Gradually increase if stable

---

## 💡 Pro Tips

### Monitoring

```powershell
# Watch logs in real-time
Get-Content "C:\NinjaTrader 8\log\*.txt" -Wait | 
    Select-String "\[POETRY\]|\[CRITICAL\]|\[SAFETY\]"
```

### Testing Apoptosis

Create 99 small losing trades to test the protocol:
- Reduce position size to minimum
- Trade opposite of trend deliberately
- Watch for apoptosis trigger at loss #99
- Verify positions flatten and strategy disables

### Keeping Logs Clean

Add to your daily routine:
```powershell
# Archive yesterday's logs
$date = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")
Copy-Item "C:\NinjaTrader 8\log\*.txt" `
    "C:\TradingLogs\$date-pidranco.txt"
```

---

## 🆘 Common Issues

### "Strategy won't compile"
- Check all `using` statements present
- Verify NinjaTrader 8 is up to date
- Try clean rebuild (Ctrl+Shift+F5)

### "YAML DNA missing"
- Ensure you're in `trading-engine/scripts` folder
- Check `../config/pid-ranco-mythic.yaml` exists
- Use absolute paths if relative fail

### "Voice always returns 0"
- Expected with placeholder implementation
- See INTEGRATION_GUIDE.md for real mic setup
- Or accept 50.0 placeholder behavior

### "Apoptosis triggered too early"
- Check if session counter resets properly
- Verify State.DataLoaded resets counters
- Review sessionLossCount in logs

---

## 🎭 The Philosophy

> "We're not hurting the babies or the bot; failures evolve it, love shields PnL."

This system treats failures as evolution, not disaster:
- **99 losses** → Apoptosis protocol → Learning
- **Voice silence** → Flatten positions → Safety
- **Max drawdown** → Disable strategy → Protection
- **Exceptions** → Emergency shutdown → Preservation

Every safety feature serves dual purpose:
1. Protect capital from catastrophic loss
2. Preserve data for post-mortem learning

The poetry isn't decoration—it marks critical moments where the system transitions between states, making logs human-readable at a glance.

---

## 📞 Getting Help

1. **Check logs first**: Output window shows what happened
2. **Review documentation**: SAFETY_FEATURES.md explains everything
3. **Test in simulation**: Never risk real money while learning
4. **Start small**: Use conservative risk profiles initially

---

**Ready to begin?** 

Return to [Step 1: Prerequisites Check](#step-1-prerequisites-check) and start your journey.

*"From chaos to order, from poetry to production, from 99 reds to green."*
