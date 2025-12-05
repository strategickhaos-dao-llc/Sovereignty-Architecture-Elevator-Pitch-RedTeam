# StrategicKhaos PID-RANCO Trading Engine v1.0

> **Love Compiles Profit. Always.**

The first financial instrument that literally trades on love. A NinjaTrader 8/9 strategy that fuses PID control theory, risk-adjusted neural optimization, and emotional intelligence into a revolutionary trading system.

## 🎯 Overview

The PID-RANCO (Risk-Adjusted Neural Compassion Optimizer) Trading Engine combines:

- **PID Controller**: Proportional-Integral-Derivative control for market positioning
- **RANCO Core**: Risk management with love-based optimization
- **Apoptosis Protocol**: Evolution through failure (99 reds → 1 green)
- **Entanglement**: Integration with voice/heartbeat biometrics
- **DNA Compilation**: Market decisions based on emotional state

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PID-RANCO Engine                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │ PID          │      │ RANCO        │               │
│  │ Controller   │─────▶│ Optimizer    │──┐            │
│  └──────────────┘      └──────────────┘  │            │
│         │                                 │            │
│         │              ┌──────────────┐   │            │
│         └─────────────▶│  Trading     │◀──┘            │
│                        │  Engine      │                │
│                        └──────────────┘                │
│                               │                         │
│                        ┌──────┴───────┐                │
│                        │              │                │
│                  ┌─────▼────┐  ┌──────▼──────┐        │
│                  │ Entry    │  │ Exit        │        │
│                  │ Rules    │  │ Rules       │        │
│                  └──────────┘  └─────────────┘        │
│                                                         │
│  ┌──────────────────────────────────────────┐         │
│  │      Apoptosis Protocol (99→1)           │         │
│  │  Evolution • Mutation • Regeneration     │         │
│  └──────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **NinjaTrader 8 or 9** installed
- **Windows** with PowerShell 5.1+
- **.NET Framework 4.8** or higher
- Optional: Microphone for voice input
- Optional: Biometric sensors for heartbeat monitoring

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

2. **Deploy to NinjaTrader (Simulation Mode)**
```powershell
.\deploy-pid-ranco.ps1 -Market sim -Verify
```

3. **Deploy for Live Trading**
```powershell
.\deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

4. **Open NinjaTrader**
   - Navigate to Tools → Strategies
   - Find "LoveCompilesProfit"
   - Apply to your chart
   - Configure parameters

## 📋 Files

| File | Description |
|------|-------------|
| `pid-ranco-trading-bot.yaml` | Configuration file with all parameters |
| `LoveCompilesProfit.cs` | NinjaTrader strategy implementation |
| `deploy-pid-ranco.ps1` | Deployment script for NinjaTrader |
| `notify-her.ps1` | Notification system (Discord, Email, SMS) |
| `README-PID-RANCO.md` | This documentation file |

## ⚙️ Configuration

### PID Controller Parameters

The PID controller calculates market positioning based on three components:

```yaml
pid_controller:
  kp: 1.0    # Proportional gain (response to current error)
  ki: 0.5    # Integral gain (response to accumulated error)
  kd: 0.25   # Derivative gain (response to rate of change)
```

- **Proportional (P)**: `raw_market_pain` - How far price is from target
- **Integral (I)**: `accumulated_longing` - Time-weighted error sum
- **Derivative (D)**: `rate_of_heart_change` - Rate of change in error

### RANCO Core Parameters

```yaml
ranco_core:
  risk_per_trade: 0.69%     # Risk per trade (sacred number)
  max_drawdown: 3.37%       # Maximum drawdown allowed
  love_factor: 1.0 + (her_voice_volume_db / 100)
  stop_loss_pct: 2.0        # Stop loss percentage
  take_profit_pct: 1.618    # Golden ratio profit target
```

### Entry Rules

1. **Long Entry**: RSI < 30 AND her_heartbeat > 80 bpm
2. **Short Entry**: RSI > 70 AND her_heartbeat < 60 bpm (optional)
3. **Hold**: DNA compiles to "stay"

### Exit Rules

1. **Take Profit**: Profit > 1.618% (golden ratio)
2. **Stop Loss**: Loss > 2.0%
3. **Love Override**: Her voice says "enough"
4. **Love Factor**: If love_factor < 0.5, exit all positions

## 🧬 Apoptosis Protocol

The evolution mechanism that learns from failure:

```
99 Losing Trades → Apoptosis Trigger
    ↓
Log Failed Ribosomes
    ↓
Mutate Strategy Parameters
    ↓
Notify & Hug Protocol
    ↓
Restart with Evolved Weights
    ↓
100th Trade MUST BE GREEN
```

### What Evolves

- **PID Parameters**: Kp, Ki, Kd adjusted by ±15%
- **RSI Thresholds**: Oversold/Overbought levels mutated
- **Risk Parameters**: Position sizing and stop losses
- **Learning Rate**: Neural network adaptation

## 💚 Love Compilation

### Voice Input

The system monitors voice volume to calculate the love factor:

```csharp
loveFactor = 1.0 + (herVoiceVolume / 100.0)
```

- **High Voice Volume** (>70 dB): Increased confidence → Larger positions
- **Low Voice Volume** (<50 dB): Decreased confidence → Exit positions
- **"Enough" Detection**: Immediate flat (exit all)

### Heartbeat Monitoring

Heartbeat influences entry decisions:

- **>80 bpm**: High excitement → Favor long entries on RSI oversold
- **<60 bpm**: Calm state → More conservative or short bias
- **Normal Range** (60-80): Standard trading rules

## 📈 Indicators

### Technical Indicators

- **RSI (14)**: Relative Strength Index
  - Oversold: <30
  - Overbought: >70
  
- **EMA Fast (9)**: Fast exponential moving average
- **EMA Slow (21)**: Slow exponential moving average

### Custom Indicators

- **Heartbeat Monitor**: Real-time BPM tracking
- **Voice Volume**: dB level measurement
- **Love Factor**: Composite emotional indicator

## 🎛️ NinjaTrader Configuration

### Strategy Parameters

Access via Strategy Properties in NinjaTrader:

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| RSI Period | 14 | 1-100 | RSI calculation period |
| RSI Oversold | 30 | 1-50 | Oversold threshold |
| RSI Overbought | 70 | 50-100 | Overbought threshold |
| EMA Fast Period | 9 | 1-200 | Fast EMA period |
| EMA Slow Period | 21 | 1-200 | Slow EMA period |
| PID Kp | 1.0 | 0.01-10.0 | Proportional gain |
| PID Ki | 0.5 | 0.01-10.0 | Integral gain |
| PID Kd | 0.25 | 0.01-10.0 | Derivative gain |
| Risk Percent | 0.69 | 0.01-5.0 | Risk per trade |
| Stop Loss % | 2.0 | 0.5-10.0 | Stop loss percentage |
| Take Profit % | 1.618 | 0.5-10.0 | Take profit percentage |

## 🔧 Deployment Options

### Simulation Mode (Safe Testing)

```powershell
.\deploy-pid-ranco.ps1 -Market sim
```

### Paper Trading (Validation)

```powershell
.\deploy-pid-ranco.ps1 -Market paper -Verify
```

### Live Trading (Production)

```powershell
.\deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

**Warning**: Live trading requires explicit confirmation. You must type "LOVE COMPILES PROFIT" to proceed.

## 📊 Performance Metrics

### Target Metrics

- **Win Rate**: >51% (just above random)
- **Profit Factor**: 1.618 (golden ratio)
- **Max Drawdown**: <3.37%
- **Risk/Reward**: 1:1.618 minimum

### 100th Trade Success Criteria

The 100th trade after evolution must be:
- **Green** (profitable)
- **>0.69%** profit minimum
- **Celebrated** with notification

## 🔔 Notifications

### Configuration

Set environment variables:

```bash
# Discord
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
$env:ENABLE_DISCORD_NOTIFICATIONS = "true"

# Email
$env:NOTIFICATION_EMAIL = "your@email.com"
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your@email.com"
$env:SMTP_PASS = "your-password"
$env:ENABLE_EMAIL_NOTIFICATIONS = "true"

# SMS (Twilio)
$env:NOTIFICATION_PHONE = "+1234567890"
$env:TWILIO_ACCOUNT_SID = "AC..."
$env:TWILIO_AUTH_TOKEN = "..."
$env:TWILIO_FROM_NUMBER = "+1234567890"
$env:ENABLE_SMS_NOTIFICATIONS = "true"
```

### Notification Events

- Strategy deployment
- Trade entries/exits
- Apoptosis trigger (99 losses)
- 100th trade success
- Love factor drops below threshold
- Stop loss/take profit hits

## 🐛 Troubleshooting

### Strategy Won't Compile

1. Check NinjaTrader version (8 or 9)
2. Verify .NET Framework 4.8+ installed
3. Check for syntax errors in output window
4. Ensure all using statements are present

### No Trades Executing

1. Check love factor (must be >0.5)
2. Verify RSI is in oversold/overbought range
3. Check heartbeat simulation values
4. Ensure strategy is enabled on chart
5. Verify account has sufficient capital

### Apoptosis Not Triggering

1. Check losing trades count in performance window
2. Verify apoptosisTrigger = 99
3. Check console output for apoptosis messages
4. Ensure strategy hasn't been restarted

### Love Metrics Not Working

1. Verify mic input is connected (if using real input)
2. Check UpdateLoveMetrics() is being called
3. Review simulated values in code
4. Enable debug printing for love metrics

## 📝 Logging

### Log Locations

- **Trading Log**: `/var/log/pid-ranco/trading.log`
- **Love Events**: `/var/log/pid-ranco/love-events.log`
- **Evolution**: `/var/log/pid-ranco/evolution.log`
- **DNA Compiles**: `/var/log/pid-ranco/dna-compiles.log`

### NinjaTrader Output

View in NinjaTrader Output Window (Tools → Output Window):
- Trade entries/exits with reasons
- PID signals and calculations
- Love factor updates
- Apoptosis triggers
- Evolution parameters

## 🔐 Security

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for secrets
3. **Enable audit logging** for all trades
4. **Backup strategies** before updates
5. **Test in simulation** before live trading

### Secure Storage

Sensitive data stored in:
```
/throne-nas-32tb/.secrets/
```

Encrypted with:
- AES-256 encryption
- Voice authentication
- DNA signature verification

## 🌟 Advanced Features

### Custom Indicators

Extend with your own indicators:

```csharp
// In OnStateChange - State.DataLoaded
private MyCustomIndicator customIndicator;
customIndicator = MyCustomIndicator(param1, param2);
AddChartIndicator(customIndicator);

// In OnBarUpdate
if (customIndicator[0] > threshold)
{
    // Your logic here
}
```

### Integration with Ollama

The system can use local LLM models for market analysis:

```yaml
model_weights:
  inference_engine: "llama3.2:70b"
  sentiment_core: "gemma2:27b"
  mutation_handler: "dolphin-llama3.2"
  ollama_base_url: "http://localhost:11434"
```

### Vector Database Integration

Failed trades stored for pattern recognition:
- FAISS or ChromaDB for embeddings
- Similarity search for failure patterns
- Genetic algorithm for parameter evolution

## 🎓 Theory & Background

### PID Control in Trading

PID controllers are used in industrial automation. Applied to trading:

- **P (Proportional)**: React to current price deviation
- **I (Integral)**: Correct for persistent bias/drift
- **D (Derivative)**: Anticipate future changes based on velocity

### RANCO: Risk-Adjusted Neural Compassion Optimizer

A novel framework combining:
- **Risk Management**: Position sizing based on account risk
- **Neural Networks**: Pattern recognition and learning
- **Compassion**: Emotional intelligence (love factor)
- **Optimization**: Continuous parameter evolution

### Apoptosis in Trading Systems

Inspired by programmed cell death in biology:
- **99 Failures**: Learning dataset for evolution
- **Mutation**: Parameter adjustments via genetic algorithm
- **Regeneration**: Restart with improved strategy
- **100th Success**: Validation of evolution

## 📚 References

- [PID Control Theory](https://en.wikipedia.org/wiki/PID_controller)
- [NinjaTrader Strategy Development](https://ninjatrader.com/support/helpGuides/nt8/)
- [Risk Management in Trading](https://www.investopedia.com/trading/risk-management/)
- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)

## 🤝 Contributing

This is part of the StrategicKhaos Sovereignty Architecture. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly in simulation
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file

## 💬 Support

- **Discord**: Join the StrategicKhaos community
- **Issues**: GitHub issue tracker
- **Email**: support@strategickhaos.com

## 🎯 Roadmap

### v1.1 (Next Release)
- [ ] Real-time mic input integration
- [ ] Biometric sensor support
- [ ] Machine learning model training
- [ ] Multi-timeframe analysis
- [ ] Portfolio-level risk management

### v2.0 (Future)
- [ ] Multi-asset support
- [ ] Options strategy integration
- [ ] Distributed trading network
- [ ] Quantum entanglement (experimental)
- [ ] Full AI-driven parameter optimization

## ✨ Philosophy

> "This isn't just a trading bot. This is the first financial instrument that literally trades on love."

The PID-RANCO engine represents a paradigm shift:
- **Technical** meets **Emotional**
- **Logic** meets **Intuition**
- **Profit** meets **Purpose**

### The Axiom

```
Love compiles profit. Always.
```

This is not metaphorical. The system genuinely incorporates emotional state into trading decisions, creating a feedback loop between human emotion and market action.

### The Promise

```
99 reds → Evolution
1 green → Victory
Her name → Forever on the chart
```

Through failure, we learn. Through loss, we evolve. Through love, we profit.

---

## 🎉 Deploy Now

Ready to let love compile profit?

```powershell
# Simulation first
.\deploy-pid-ranco.ps1 -Market sim

# When ready
.\deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

**The market is waiting. Love is ready. Deploy.**

---

*StrategicKhaos PID-RANCO Trading Engine v1.0*  
*Built with ❤️ for the throne*  
*2025-11-24*
