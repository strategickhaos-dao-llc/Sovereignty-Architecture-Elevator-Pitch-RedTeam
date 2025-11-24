# StrategicKhaos PID-RANCO Trading Engine v1.2

**Codename**: *Guardrails Around a Supernova*  
**Philosophy**: *99 crashes bloom into the 100th win. Poetry preserved, engineering hardened.*

---

## 🌟 Overview

The PID-RANCO Trading Engine is a unique blend of poetic architecture and hardened safety engineering. It combines:

- **Mythic Layer (YAML)**: Poetry-preserved configuration with emotional variable names
- **Kill-Switch Layer (C#)**: Industrial-grade NinjaTrader strategy with comprehensive safety systems
- **Fail-Loud Layer (PowerShell)**: Deployment automation that makes errors visible

The system is designed with "evolutionary apoptosis" - after 99 losing trades, it gracefully self-destructs and prepares for the next iteration, learning from failures.

---

## 📁 Files in This Implementation

| File | Size | Purpose |
|------|------|---------|
| `pid-ranco-trading-bot.yaml` | 3KB | Configuration with mythic variable names and risk parameters |
| `LoveCompilesProfit.cs` | 20KB | NinjaTrader 8/9 strategy implementation with safety guardrails |
| `deploy-pid-ranco.ps1` | 13KB | PowerShell deployment script with validation and logging |
| `notify-her.ps1` | 2.4KB | Notification helper for Discord/log notifications |
| `TRADING_ENGINE_FAILURES.md` | 16KB | Documentation of 100 potential failure modes and mitigations |
| `TRADING_ENGINE_README.md` | This file | Implementation guide and usage documentation |

---

## 🚀 Quick Start

### Prerequisites

- **NinjaTrader 8 or 9** installed on Windows
- **PowerShell 5.1+** (included with Windows)
- Optional: **Discord webhook** for notifications (set `DISCORD_WEBHOOK_URL` environment variable)

### Installation

1. **Deploy the strategy**:
   ```powershell
   # Default: Safe simulation mode
   .\deploy-pid-ranco.ps1
   
   # With love-tuned parameters
   .\deploy-pid-ranco.ps1 -loveMode
   
   # With notifications enabled
   .\deploy-pid-ranco.ps1 -loveMode -entangleHer
   ```

2. **Open NinjaTrader**:
   - Go to **Tools → Strategies**
   - Find "LoveCompilesProfit" in the list
   - Apply to a chart

3. **Configure Strategy**:
   - **Sim Only**: `true` (recommended for testing)
   - **Max Risk Per Trade**: `0.0069` (0.69%)
   - **Max Drawdown**: `0.0337` (3.37%)
   - **Entry Voice Threshold**: `80` (adjust as needed)
   - **Exit Voice Threshold**: `50` (adjust as needed)

---

## ⚙️ Configuration

### YAML Configuration (Mythic Layer)

The `pid-ranco-trading-bot.yaml` file contains the poetic architecture:

```yaml
pid_controller:
  proportional: "raw_market_pain"     # Price distance from EMA
  integral:     "accumulated_longing" # Time-weighted deviation
  derivative:   "rate_of_heart_change" # Momentum

ranco_core:
  risk_per_trade: "0.69%"   # Sacred number
  max_drawdown:   "3.37%"   # Her birthday reversed
```

### Strategy Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Sim Only | `true` | boolean | Safety mode - no real trades |
| Max Risk Per Trade | `0.0069` | 0.0001-0.05 | Maximum risk per trade (0.69%) |
| Max Drawdown | `0.0337` | 0.001-0.1 | Maximum allowed drawdown (3.37%) |
| Entry Voice Threshold | `80` | 1-200 | Minimum "voice/heartbeat" level for entry |
| Exit Voice Threshold | `50` | 1-200 | Voice level below which to exit |

---

## 🛡️ Safety Features

### 1. Sim-Only Default
- **No real trades** unless explicitly disabled
- All would-be trades are logged with `[SIM]` prefix
- Safe for crash-testing and evolution

### 2. Risk Management
- **0.69% max risk per trade** - hard-coded sacred limit
- **3.37% max drawdown** - automatic shutdown on breach
- Position sizing based on account equity and stop distance

### 3. Fail-Loud Design
- All errors logged with timestamps and stack traces
- No silent failures - every error is visible
- Console output color-coded (errors in red, success in green)

### 4. Apoptosis Protocol
- **99 losing trades** triggers "hug protocol"
- System flattens all positions and prepares for evolution
- Loss count tracked to prevent double-counting

### 5. Voice State Monitoring
- Monitors "voice/heartbeat" input (mock implementation included)
- **5-minute timeout** - flattens positions if no voice detected
- Configurable thresholds for entry/exit decisions

### 6. Comprehensive Validation
- **NaN/Infinity checks** on all indicator values
- **Zero division guards** on all calculations
- **TickSize validation** before using in formulas
- **Account equity validation** before position sizing

---

## 🔧 Development Notes

### Voice Detection (TODO)

The current implementation uses a mock voice detection function that returns `60.0`:

```csharp
private double GetHerVoiceVolumeSafe()
{
    // TODO: Replace with actual implementation
    double val = 60.0; // Neutral mock value
    return Math.Clamp(val, 0.0, 100.0);
}
```

**To implement real voice detection**:
1. Add microphone input library (e.g., NAudio)
2. Implement volume/frequency analysis
3. Replace mock value with real measurements
4. Or read from pre-recorded WAV file (`her_voice.wav`)

### Entry/Exit Logic

**Entry Conditions**:
- RSI < 30 (oversold)
- AND Voice/Heartbeat > Entry Threshold (default 80)
- AND Risk management allows trade

**Exit Conditions**:
- Profit > 1.618% (golden ratio)
- OR Voice/Heartbeat < Exit Threshold (default 50)
- OR 5 minutes without voice input
- OR Drawdown breach

### Indicators Used
- **EMA(21)**: Fast exponential moving average for trend
- **RSI(14,3)**: Relative strength index for oversold/overbought

---

## 📊 Monitoring and Logs

### Log Files

The deployment script creates timestamped log files:
- **Deploy logs**: `logs/pid-ranco-deploy-YYYYMMDD-HHmmss.log`
- **Notification logs**: `logs/notifications.log`

### Discord Notifications

Set environment variable for webhooks:
```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

Notifications sent for:
- Deployment status (success/failure)
- Apoptosis trigger (99 losses)
- Critical errors

### NinjaTrader Output Window

Watch for log messages with prefixes:
- `[SIM]` - Simulation-only actions
- `[LOSS]` - Losing trade closed
- `[SAFETY]` - Safety feature triggered
- `[ERROR]` - Error condition
- `[WARN]` - Warning
- `[NOTIFY]` - Notification sent
- `[APOPTOSIS]` - Evolution protocol triggered

---

## 🎯 Use Cases

### 1. Safe Backtesting
```powershell
.\deploy-pid-ranco.ps1 -simOnly
# Apply to historical data in NinjaTrader
# Monitor console for [SIM] entries/exits
```

### 2. Paper Trading
```powershell
.\deploy-pid-ranco.ps1 -loveMode -entangleHer
# Connect to live data feed
# No real orders placed (simOnly=true)
```

### 3. Live Trading (Advanced)
```powershell
# ⚠️ CAUTION: Real money at risk
.\deploy-pid-ranco.ps1 -loveMode -entangleHer -marketLive -simOnly:$false
# Waits 5 seconds for abort
# Enables real order execution
```

---

## 🧪 Testing

### Validate Configuration
```powershell
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('pid-ranco-trading-bot.yaml'))"

# Run deployment validation only
.\deploy-pid-ranco.ps1 -WhatIf  # (if implemented)
```

### Monitor Session
1. Enable strategy in NinjaTrader
2. Open Output Window (Tools → Output Window)
3. Watch for log messages
4. Monitor session loss count in strategy properties

### Test Apoptosis
- Run on losing historical period
- Watch for "99 losses" message
- Verify positions flatten
- Check notification sent

---

## 📚 Architecture Documentation

### PID Controller Concept

The "PID" in PID-RANCO refers to a Proportional-Integral-Derivative controller:

- **Proportional**: Current market pain (distance from EMA)
- **Integral**: Accumulated longing (time-weighted deviation)
- **Derivative**: Rate of change (momentum)

This is translated into traditional indicators (EMA, RSI) for practical implementation.

### RANCO Core

**R**isk-**A**djusted **N**eural **C**ompassion **O**ptimizer:

- Risk-adjusted position sizing
- Neural: Would integrate with AI models (llama3.2, gemma2)
- Compassion: Emotional inputs from voice/heartbeat
- Optimizer: Learns from 99 failures to achieve 100th win

### Evolutionary Apoptosis

Biological concept applied to trading:
- **99 losses** = 99 failed experiments
- **Hug protocol** = Graceful shutdown and state preservation
- **Evolution** = Next iteration starts with learned parameters
- **100th trade** = Emergent success from evolved system

---

## ⚠️ Risk Warnings

1. **Trading is risky** - This software can lose money
2. **Test thoroughly** - Use simulation mode extensively
3. **Start small** - Begin with minimum position sizes
4. **Monitor closely** - Never leave automated trading unattended
5. **Understand limits** - Know your risk tolerance and drawdown limits
6. **Voice detection** - Mock implementation needs replacement for production
7. **No guarantees** - Past performance doesn't predict future results

---

## 🔐 Security Considerations

### Input Validation
- All numeric inputs validated for NaN/Infinity
- Voice inputs clamped to 0-100 range
- PowerShell scripts sanitize message inputs

### Error Handling
- Try-catch blocks around all external calls
- Graceful degradation on failures
- No silent errors - all logged and visible

### Command Injection Prevention
- Commented PowerShell execution uses ProcessStartInfo
- Input validation recommended before enabling
- Standard input redirection safer than command-line args

---

## 🤝 Contributing

This is a unique architecture blending poetry and pragmatism. When contributing:

1. **Preserve poetry** - Keep mythic variable names in YAML
2. **Harden engineering** - Add safety checks in C#
3. **Fail loud** - Make errors visible in PowerShell
4. **Test thoroughly** - Validate with simulation mode
5. **Document failures** - Add to 100 failure modes list

---

## 📖 Further Reading

- `TRADING_ENGINE_FAILURES.md` - 100 documented failure modes
- `pid-ranco-trading-bot.yaml` - Poetic configuration reference
- NinjaTrader 8 Documentation: [ninjatrader.com/support](https://ninjatrader.com/support)

---

## 📜 License

This implementation is part of the Strategickhaos Sovereignty Architecture.  
See `LICENSE` file in repository root.

---

## 💕 Philosophy

> "Every loss = one failed ribosome → log → evolve.  
> 99 losing trades = 99 failed compiles → 100th = her name in green candles.  
> Love > PnL: If she's happy, bot stops trading and just holds."

**— From the YAML Manifesto**

---

*Version 1.2 | Codename: Guardrails Around a Supernova*  
*"Failures now scream lessons, not losses. Poetry preserved, engineering hardened."*
