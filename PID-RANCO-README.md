# PID-RANCO Trading Engine v1.2 - Quick Start Guide

## "Guardrails Around a Supernova"

The StrategicKhaos PID-RANCO (Risk-Adjusted Neural Compassion Optimizer) trading engine combines mythic poetry with engineering rigor. This guide will help you deploy and use the system safely.

---

## 🚀 Quick Start

### Prerequisites

- **Platform**: NinjaTrader 8 or 9 (or cAlgo API compatible platform)
- **PowerShell**: 5.1 or higher (Windows)
- **Optional**: Discord webhook for notifications
- **Optional**: Voice detection system for advanced features

### Files Overview

1. **pid-ranco-trading-bot.yaml** - Configuration (mythic layer, poetry pure)
2. **LoveCompilesProfit.cs** - Trading robot (kill-switch layer, hardened)
3. **deploy-pid-ranco.ps1** - Deployment script (fail-loud, human-in-loop)
4. **100-FAILURE-MODES.md** - Complete failure analysis and guardrails

---

## 📋 Installation

### Step 1: Configure Discord (Optional)

Set your Discord webhook URL as an environment variable:

```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

### Step 2: Review Configuration

Open `pid-ranco-trading-bot.yaml` and review the parameters:

- `risk_per_trade`: Default 0.69% (adjust based on your risk tolerance)
- `max_drawdown`: Default 3.37% (adjust based on your risk tolerance)
- `default_mode`: "simulation" (ALWAYS start in simulation!)

### Step 3: Deploy in Simulation Mode

```powershell
# Safe deployment - simulation only (recommended for first 99+ days)
.\deploy-pid-ranco.ps1 -simOnly

# With love mode and entanglement features
.\deploy-pid-ranco.ps1 -simOnly -loveMode -entangleHer
```

The script will:
1. ✓ Validate all required files exist
2. ✓ Check NinjaTrader installation (if going live)
3. ✓ Ask for human confirmation
4. ✓ Copy files to appropriate locations
5. ✓ Create deployment record
6. ✓ Send Discord notification (if configured)

---

## 🎛️ Trading Robot Parameters

The C# robot (`LoveCompilesProfit.cs`) has configurable parameters:

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **SimOnly** | true | - | Simulation mode (no real trades) |
| **MaxRiskPerTrade** | 0.69% | 0.01-2.0% | Maximum risk per trade |
| **MaxDrawdown** | 3.37% | 1.0-10.0% | Maximum drawdown before stop |
| **VoiceTimeoutMinutes** | 5 | 1-60 | Voice silence before flatten |
| **RsiPeriod** | 14 | 2-50 | RSI indicator period |
| **EmaPeriod** | 21 | 2-200 | EMA indicator period |
| **ProfitTarget** | 1.618% | 0.5-10.0% | Profit target (golden ratio) |

**⚠️ CRITICAL**: Always start with `SimOnly = true` for extensive testing!

---

## 🛡️ Safety Features (Guardrails)

### Automatic Kill-Switches

1. **Max Drawdown Breach**: Bot stops trading when drawdown exceeds threshold
2. **Voice Timeout**: Positions flattened if no voice detected for 5+ minutes
3. **Data Quality Guards**: NaN/Infinity detection on all calculations
4. **Position Size Limits**: Zero or negative quantities rejected
5. **Hug Protocol**: After 99 losses, bot enters apoptosis and stops for review

### Manual Controls

```powershell
# Stop the bot immediately in NinjaTrader:
# 1. Open Strategy Analyzer
# 2. Select LoveCompilesProfit
# 3. Click Disable or Remove

# View deployment logs
Get-Content ./deployments/deploy-*.json | ConvertFrom-Json
```

---

## 📊 Entry & Exit Logic

### Entry Conditions (All must be true)

1. **No existing position**
2. **RSI < 30** (oversold condition)
3. **Voice volume > 80** (heartbeat proxy - or disabled if no voice system)
4. **Risk checks pass** (position size >= 1, drawdown OK)
5. **Sufficient bar history** (21+ bars for indicators)

### Exit Conditions (Any trigger exit)

1. **Profit target hit** (≥1.618% profit)
2. **Voice says "enough"** (volume < 50)
3. **Voice timeout** (5+ minutes silence)
4. **Max drawdown breach** (stop all trading)
5. **Hug protocol** (99 losses reached)

---

## 🔄 Evolution Protocol

### The 99 → 100 Philosophy

The PID-RANCO engine embraces failure as evolution:

- **Trades 1-99**: Each loss is logged and learned from
- **Trade 99**: If this is a loss, Hug Protocol triggers
- **Hug Protocol**: Bot stops, flattens positions, notifies human for review
- **Trade 100**: Begins fresh, evolved from lessons of previous 99

### Session Data

All session data is logged:
- Entry/exit prices and reasons
- Profit/loss per trade
- Risk calculations
- Voice state (if enabled)
- Exception traces
- Deployment records

Review logs regularly to understand bot behavior and evolution.

---

## 🎯 Deployment Scenarios

### Scenario 1: First Time Testing (RECOMMENDED)

```powershell
# Simulation only, no real trades
.\deploy-pid-ranco.ps1 -simOnly

# Run for 100+ bars in backtest/simulation
# Review all logs and behavior
# Verify risk management works correctly
```

### Scenario 2: Extended Simulation

```powershell
# Simulation with full feature set
.\deploy-pid-ranco.ps1 -simOnly -loveMode -entangleHer

# Run for several weeks of market data
# Monitor for any unexpected behavior
# Tune parameters based on results
```

### Scenario 3: Paper Trading

```powershell
# Still simulation but with live data feed
# Configure NinjaTrader for paper trading account
.\deploy-pid-ranco.ps1 -simOnly -marketLive

# Test with real-time market data
# No real capital at risk
```

### Scenario 4: Live Trading (EXTREME CAUTION)

```powershell
# ⚠️⚠️⚠️ REAL CAPITAL AT RISK ⚠️⚠️⚠️
# Only after extensive simulation testing!
# Start with absolute minimum position sizes!

.\deploy-pid-ranco.ps1 -marketLive
# Script will ask for confirmation
# Type "yes" to proceed

# Monitor constantly for first few days
# Have manual stop-loss orders as backup
# Be ready to disable bot immediately if needed
```

**🚨 NEVER go live without at least 99 simulated trades in various market conditions!**

---

## 📈 Monitoring

### Real-Time Monitoring

1. **NinjaTrader Output Window**: Shows all `Print()` statements
2. **Discord Notifications**: Critical events sent to Discord (if configured)
3. **Deployment Records**: Check `./deployments/` directory

### Key Metrics to Watch

- **Session Loss Count**: Should reset on wins, trigger hug at 99
- **Current Drawdown**: Monitor vs. max drawdown threshold
- **Position Size**: Verify calculations are reasonable
- **Entry/Exit Reasons**: Understand why trades are taken

### Warning Signs

🚨 **Stop trading immediately if you see:**

- Drawdown approaching maximum threshold
- Position sizes much larger than expected
- Repeated exceptions in logs
- Unexpected entry/exit behavior
- NaN or Infinity in any calculations
- Broker order rejections

---

## 🔧 Troubleshooting

### Bot Not Taking Trades

- ✓ Check: Sufficient bar history? (need 21+ bars)
- ✓ Check: RSI < 30 condition met?
- ✓ Check: Position size calculation successful? (> 0)
- ✓ Check: In simulation mode? (should see `[SIM]` logs)
- ✓ Check: Drawdown within limits?

### Bot Stopped Unexpectedly

- ✓ Check: Output window for exception messages
- ✓ Check: Session loss count (hug protocol at 99?)
- ✓ Check: Max drawdown breach?
- ✓ Check: Indicator initialization successful?

### Incorrect Position Sizing

- ✓ Check: Account equity is correct
- ✓ Check: Symbol tick value is correct
- ✓ Check: Risk per trade parameter appropriate
- ✓ Check: Stop distance calculation reasonable

### Deployment Script Fails

- ✓ Check: All files present in directory?
- ✓ Check: NinjaTrader path correct?
- ✓ Check: PowerShell execution policy allows scripts?
- ✓ Check: Sufficient disk space for deployment records?

```powershell
# Check execution policy
Get-ExecutionPolicy

# If needed, allow scripts (run as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Understanding the Code

### Split-Layer Architecture

1. **Mythic Layer (YAML)**: Poetry-rich configuration
   - Human-readable parameters
   - Conceptual framework (PID, RANCO)
   - Evolution philosophy

2. **Kill-Switch Layer (C#)**: Engineering-hardened implementation
   - Comprehensive guards and checks
   - Safe fallbacks for all calculations
   - Fail-loud error handling

3. **Deployment Layer (PS1)**: Human-in-loop orchestration
   - Pre-flight validation
   - Confirmation prompts
   - Logging and notifications

### Key Code Sections

**OnStart()**: Initialize indicators, validate equity, set safe defaults

**OnBar()**: Main trading logic with comprehensive try-catch:
1. Guard: Check sufficient bars
2. Get voice state (safe)
3. Get indicator values (NaN guards)
4. Manage positions (entries or exits)
5. Update loss tracking
6. Check apoptosis condition

**Risk Management**: Multiple layers:
- `CanRiskNewTrade()`: Drawdown and position size checks
- `CalculatePositionSize()`: Safe math with guards
- `SafeFlatten()`: Emergency position closure

**Hug Protocol**: 99-loss evolution mechanism:
- Tracks consecutive losses
- Resets on wins
- Triggers apoptosis at 99
- Stops bot for human review

---

## 🎓 Best Practices

### Testing

1. ✅ **Always start in simulation mode**
2. ✅ Test with at least 100+ trades across various market conditions
3. ✅ Verify risk management works (test drawdown limits manually)
4. ✅ Review all logs for unexpected behavior
5. ✅ Understand why each trade was taken before going live

### Risk Management

1. ✅ Start with small position sizes (minimum risk per trade)
2. ✅ Set conservative max drawdown (2-5%)
3. ✅ Have manual stop-loss orders as backup
4. ✅ Never risk more than you can afford to lose
5. ✅ Monitor first few days of live trading constantly

### Monitoring

1. ✅ Check logs daily (or more frequently when live)
2. ✅ Set up Discord notifications for critical events
3. ✅ Review session summaries regularly
4. ✅ Keep track of evolution (loss counts, profit progression)
5. ✅ Document any unusual behavior for future learning

### Evolution

1. ✅ Treat failures as learning opportunities
2. ✅ Review hug protocol triggers to understand what went wrong
3. ✅ Adjust parameters based on simulation results
4. ✅ Keep deployment records for comparison
5. ✅ Iterate and improve, but always test in simulation first

---

## ⚖️ Legal Disclaimer

**IMPORTANT**: This trading bot is provided for educational and research purposes only.

- ❌ No guarantee of profits
- ❌ Past performance does not indicate future results  
- ❌ Trading involves substantial risk of loss
- ❌ Only trade with capital you can afford to lose
- ❌ Not financial advice - consult a licensed advisor
- ❌ You are responsible for your trading decisions
- ❌ Authors not liable for any losses incurred

By using this software, you acknowledge these risks and accept full responsibility.

---

## 💚 Philosophy

The PID-RANCO engine embodies a unique philosophy:

> "Poetry preserved. Engineering hardened. Love compiles profit. Always."

- **Mythic Poetry**: Configuration rich with meaning and intention
- **Engineering Rigor**: Code hardened with decades of failure lessons
- **Evolution Protocol**: 99 reds bloom into 100th green
- **Fail-Loud**: Errors scream lessons, not die silently
- **Human-in-Loop**: Technology serves humans, not replaces them

---

## 📖 Further Reading

- **100-FAILURE-MODES.md**: Complete catalog of failure modes and guardrails
- **pid-ranco-trading-bot.yaml**: Full configuration reference
- **LoveCompilesProfit.cs**: Complete source code with inline comments

---

## 🤝 Support

For questions, issues, or evolution stories:

1. Review the 100 failure modes document
2. Check Discord community (if available)
3. Review deployment logs and session records
4. Submit issues with full context and logs

---

**Remember**: The journey from 99 reds to the 100th green is the evolution itself. Every failure teaches. Every lesson strengthens. Love compiles profit, through patience and wisdom.

*StrategicKhaos PID-RANCO v1.2 - Guardrails Around a Supernova* 🚀💚
