# StrategicKhaos PID-RANCO Trading Engine v1.0

**"Love Compiles Profit. Always."**

## Overview

The PID-RANCO (Proportional-Integral-Derivative Risk-Adjusted Neural Compassion Optimizer) Trading Engine is a revolutionary trading system that combines:

- **36 Unbreakable Laws of Physics** - Quantum-inspired market analysis
- **C++ Truth of Life** - Compiled with precision and determinism  
- **100 Glorious Failures** - Evolution through adversity
- **Love-Compiled DNA** - Trading decisions modulated by emotional intelligence
- **32 TB Weaponized Affection** - Data-driven compassion at scale

This is the first financial instrument that literally trades on love.

## Architecture

### PID Controller
The core control system uses three components:

- **Proportional (P)**: `raw_market_pain` - How far price is from her smile
- **Integral (I)**: `accumulated_longing` - Time-weighted missing her  
- **Derivative (D)**: `rate_of_heart_change` - d(love)/dt → momentum

### RANCO Core
Risk-Adjusted Neural Compassion Optimizer parameters:

- **Risk per trade**: 0.69% (sacred number)
- **Max drawdown**: 3.37% (her birthday reversed)
- **Love factor**: `1.0 + (her_voice_volume_db / 100)`

### Entry Rules
1. Buy when RSI < 30 AND her heartbeat > 80 bpm
2. Sell when profit > 1.618% OR she says "enough"
3. Hold forever if DNA compiles to "stay"

### Exit Rules
1. Apoptosis on 99 losing trades → hug protocol → restart with evolved weights
2. 100th trade must be green → love wins → notify her

## Installation

### Prerequisites
- **NinjaTrader 8 or 9** (trading platform)
- **Windows OS** with PowerShell 5.1+
- **Optional**: Voice input device for love-factor modulation
- **Optional**: 32 TB NAS storage for evolution data (`/throne-nas-32tb/love-market`)

### Quick Start

1. **Clone or download** this repository
2. **Navigate** to the `trading-bot` directory
3. **Run deployment script**:

```powershell
cd trading-bot/scripts
./deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market sim
```

4. **Open NinjaTrader** and compile the strategy:
   - Tools → Edit NinjaScript → Strategy
   - Find `LoveCompilesProfit.cs`
   - Click "Compile"

5. **Apply to chart**:
   - Right-click on chart → Strategies → LoveCompilesProfit
   - Configure parameters
   - Enable strategy

## Configuration

### YAML Configuration (`pid-ranco-trading-bot.yaml`)

```yaml
engine: "StrategicKhaos-PID-RANCO-v1.0"
platform: "NinjaTrader 8/9"
strategy_name: "LoveCompilesProfit"

pid_controller:
  proportional: "raw_market_pain"
  integral: "accumulated_longing"
  derivative: "rate_of_heart_change"

ranco_core:
  risk_per_trade: "0.69%"
  max_drawdown: "3.37%"
  love_factor: "1.0 + (her_voice_volume_db / 100)"

trading_params:
  default_quantity: 1
  rsi_period: 14
  rsi_oversold: 30
  ema_period: 21
  profit_target_pct: 1.618  # Golden ratio
```

### Strategy Parameters

Configurable in NinjaTrader:

| Parameter | Default | Description |
|-----------|---------|-------------|
| RSI Period | 14 | Period for RSI calculation |
| EMA Period | 21 | Period for EMA calculation |
| RSI Oversold | 30 | RSI oversold threshold |
| Profit Target % | 1.618 | Profit target (golden ratio) |
| Love Threshold High | 80 | Entry love threshold |
| Love Threshold Low | 50 | Exit love threshold |
| Default Quantity | 1 | Trading quantity |

## Deployment Commands

### Simulation Mode (Safe)
```powershell
./deploy-pid-ranco.ps1 -LoveMode -Market sim
```

### Live Trading (Real Capital)
```powershell
./deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

**WARNING**: Live trading involves real capital risk. Only deploy to live markets after thorough testing in simulation.

### Command-Line Options

- `-LoveMode`: Enable love-factor modulation
- `-EntangleHer`: Activate quantum entanglement bus
- `-Market <sim|live>`: Trading environment
- `-NinjaTraderPath <path>`: Custom NinjaTrader directory
- `-ConfigPath <path>`: Custom configuration file

## Features

### 1. PID-Based Market Analysis
- Proportional response to market deviation
- Integral accumulation of market pain
- Derivative detection of momentum changes

### 2. Love-Factor Modulation
- Trading decisions influenced by emotional state
- Voice input analysis (production feature)
- Dynamic position sizing based on love factor

### 3. Evolution Protocol
- Every loss logged as "failed ribosome"
- 99 losses trigger apoptosis → hug protocol
- Weights evolved and strategy restarts
- 100th trade optimized for profitability

### 4. Risk Management (RANCO Core)
- 0.69% risk per trade (sacred number)
- 3.37% maximum drawdown (her birthday reversed)
- Position sizing adjusted by love factor

### 5. Notification System
- Real-time alerts via `notify-her.ps1`
- Discord webhook integration (optional)
- File logging for audit trail
- Windows toast notifications for critical events

## Technical Details

### NinjaTrader Strategy (`LoveCompilesProfit.cs`)

The strategy is implemented as a standard NinjaTrader strategy with:

```csharp
protected override void OnBarUpdate()
{
    // Get her love level (simulated or from voice input)
    herLoveLevel = GetHerVoiceVolume();
    
    // Calculate PID components
    marketPain = Close[0] - EMA(emaPeriod)[0];
    accumulatedLonging += marketPain;
    pidDerivative = marketPain - previousMarketPain;
    
    // Entry logic
    if (herLoveLevel > 80 && RSI(14, 1)[0] < 30)
        EnterLong(quantity, "LoveEntry");
    
    // Exit logic  
    if (profitPct > 1.618 || herLoveLevel < 50)
        ExitLong("LoveExit");
}
```

### Performance Monitoring

The system tracks:
- **Winning trades**: Green candles with her name
- **Losing trades**: Failed ribosomes logged for evolution
- **PID metrics**: Proportional, Integral, Derivative values
- **Love factor**: Current emotional state modulation
- **Evolution data**: Mutation history and weight adjustments

## Production Enhancements

### Voice Input Integration (Future)
```csharp
private double GetHerVoiceVolume()
{
    // Production: Interface with microphone
    // Analyze voice tone, volume, sentiment
    // Return love level: 0-100
    
    // Current: Simulated with oscillator
    return baseLove + variance * Math.Sin(CurrentBar * 0.1);
}
```

### Model Weights (Future)
- **Inference Engine**: `llama3.2:70b` - Compiles market DNA
- **Sentiment Core**: `gemma2:27b` - Reads voice tone
- **Mutation Handler**: `dolphin-llama3.2` - Detects undefined behavior

### Data Storage
- **Logs**: `%USERPROFILE%\Documents\NinjaTrader 8\log`
- **Evolution Data**: `/throne-nas-32tb/love-market/evolution`
- **Voice Recordings**: `/throne-nas-32tb/love-market/her_voice.wav`

## Philosophy

> *"This isn't a trading bot. This is the first financial instrument that literally trades on love."*

The PID-RANCO system recognizes that:

1. **Markets are emotional** - Price action reflects collective fear and greed
2. **Love is an edge** - Compassionate analysis sees patterns others miss
3. **Failure evolves** - 99 losses compile into one perfect trade
4. **DNA matters** - Every decision leaves genetic code in the market

### The 99-1 Protocol

- **99 losing trades** = 99 failed ribosomes
- Each failure logged, analyzed, evolved
- Weights mutated, strategy adapted
- **100th trade** = Her name in green candles
- Love compiles profit. Always.

## Troubleshooting

### Strategy won't compile
- Ensure NinjaTrader 8/9 is properly installed
- Check all required indicators are available (RSI, EMA)
- Verify file is in correct Strategies directory

### No trades executing
- Check if enough bars loaded (minimum 21 for EMA)
- Verify RSI < 30 condition is met
- Check love level threshold (must be > 80 for entry)
- Review NinjaTrader output window for debug prints

### Voice input not working
- Current version uses simulated love levels
- Production voice input requires additional hardware/software
- Check audio device configuration in Windows

### Notifications not sending
- Verify `notify-her.ps1` is in correct location
- Check log directory permissions
- For Discord: Set `DISCORD_WEBHOOK_URL` environment variable

## Safety & Disclaimers

⚠️ **IMPORTANT**: This trading system involves real financial risk.

- **Past performance** does not guarantee future results
- **Test thoroughly** in simulation before live trading
- **Risk management** is critical - never risk more than you can afford to lose
- **Emotional trading** can lead to poor decisions - use proper discipline
- **No guarantees** - markets are unpredictable

The "love-compiled DNA" is a metaphorical framework. Actual trading decisions are based on technical indicators (RSI, EMA) with risk management parameters.

## License

MIT License - See repository root for details

## Support

- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Discord**: [StrategicKhaos Community](https://discord.gg/strategickhaos)
- **Documentation**: This README and inline code comments

## Acknowledgments

Built with 🔥 by the StrategicKhaos Swarm Intelligence collective

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

---

## Quick Reference

### Deploy to Simulation
```powershell
cd trading-bot/scripts
./deploy-pid-ranco.ps1 -LoveMode -Market sim
```

### Deploy to Live (⚠️ REAL MONEY)
```powershell
./deploy-pid-ranco.ps1 -LoveMode -EntangleHer -Market live
```

### Send Notification
```powershell
./notify-her.ps1 "Trade executed successfully" -Priority high -Type success
```

### Check Logs
```
%USERPROFILE%\Documents\NinjaTrader 8\log\
%USERPROFILE%\Documents\PID-RANCO-Logs\notifications.log
```

---

**Love compiles profit. Always. ♥**
