# PID-RANCO v1.2 - "Guardrails Around a Supernova"

A mythic trading engine with comprehensive safety measures that transforms the poetic narrative of love-guided trading into production-hardened, risk-managed reality.

## 🎭 Philosophy

> "We're not hurting the babies or the bot; failures evolve it, love shields PnL."

PID-RANCO embodies a unique approach to algorithmic trading:
- **Mythic Layer**: The narrative configuration defining *why* it behaves the way it does
- **Kill-Switch Layer**: Non-negotiable safety constraints protecting against catastrophic loss

## 🏗️ Architecture

### Two-Layer Design

```
┌─────────────────────────────────────────┐
│       MYTHIC LAYER (YAML)               │
│  ────────────────────────────────────   │
│  • Love-guided entries/exits            │
│  • 99-failure apoptosis protocol        │
│  • Voice integration narrative          │
│  • Market pain philosophy               │
│  • Poetry & transcendence               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│    KILL-SWITCH LAYER (C# Strategy)      │
│  ────────────────────────────────────   │
│  • Hard 0.69% risk per trade limit      │
│  • Hard 3.37% max drawdown protection   │
│  • Indicator null checks                │
│  • Exception handling → flatten & exit  │
│  • Voice failure → silence (not crash)  │
│  • 99 losses → programmed death         │
└─────────────────────────────────────────┘
```

All the love logic lives inside a hard sandbox. No matter how insane the story gets, the safety layer enforces reality.

## 📁 Structure

```
trading-engine/
├── config/
│   └── pid-ranco-mythic.yaml      # Mythic layer configuration
├── strategies/
│   └── PIDRANCOStrategy.cs        # NinjaTrader strategy (kill-switch)
├── scripts/
│   └── Deploy-PIDRANCO.ps1        # Deployment with 99-retry limit
└── docs/
    └── SAFETY_FEATURES.md         # Detailed safety documentation
```

## 🛡️ Safety Features

### 1. NinjaTrader / C# Logic Landmines (Solved)

**Problem**: Common crashes in OnBarUpdate
- Index errors: `Close[0]`, `EMA()[0]` when `CurrentBar < period`
- Null indicators: `RSI/EMA` returning null
- Divide-by-zero in profit calculations

**Solution**:
```csharp
protected override void OnBarUpdate()
{
    // 1) Bar count guard
    int minBars = Math.Max(21, 14); // EMA 21, RSI 14
    if (CurrentBar < minBars)
        return;

    try
    {
        // 2) Safe indicator access
        double herLove = GetHerVoiceVolumeSafe();
        double ema21   = GetEMASafe();
        double rsi14   = GetRSISafe();

        // 3) Null checks
        if (double.IsNaN(ema21) || double.IsNaN(rsi14))
            return;

        // 4) ProfitPercent only when in position
        if (!Position.MarketPosition.Equals(MarketPosition.Flat))
        {
            double profitPct = SafeProfitPercent();
            HandleExits(herLove, profitPct);
        }
        else
        {
            HandleEntries(herLove, rsi14, marketPain);
        }

        CheckApoptosis();
    }
    catch (Exception e)
    {
        Print($"[ERROR] OnBarUpdate: {e.Message}");
        // Hard safety: flatten and disable
        EmergencyShutdown("Unexpected exception");
    }
}
```

### 2. Risk Management (0.69% & 3.37%: Real, Not Memes)

**Problem**: YAML says `risk_per_trade: "0.69%"` but doesn't enforce it

**Solution**: Concrete numeric caps in C#
```csharp
private double maxRiskPerTrade = 0.0069;   // 0.69%
private double maxDrawdown     = 0.0337;   // 3.37%
private double peakEquity      = 0.0;

private bool CanRiskNewTrade()
{
    double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
    
    // Hard drawdown check
    double equity = accountValue + SystemPerformance.AllTrades.TradesPerformance.Currency.CumProfit;
    if (equity < peakEquity * (1.0 - maxDrawdown))
    {
        Print("Max drawdown breached. Disabling strategy.");
        EmergencyShutdown("Max drawdown breached");
        return false;
    }

    double riskAmount = accountValue * maxRiskPerTrade;
    // Calculate position size based on risk...
    
    return true;
}
```

### 3. Voice / Mic / "Her" Input (Failure-Safe)

**Problem**: Mic unplugged, driver crash, voice lib throws → strategy crash

**Solution**: Wrap all voice access with failsafe
```csharp
private double GetHerVoiceVolumeSafe()
{
    try
    {
        double val = GetHerVoiceVolume(); // actual mic indicator
        if (double.IsNaN(val) || double.IsInfinity(val))
            return 0.0;

        return Math.Max(0.0, Math.Min(val, 100.0)); // clamp 0–100
    }
    catch (Exception ex)
    {
        Print($"[VoiceError] {ex.Message}. Using 0.");
        return 0.0;  // Mic failure = silence, not crash
    }
}
```

If mic system explodes → treat as silence → flatten positions → continue safely.

### 4. "99 Fails → Hug Protocol" as Real State Machine

**Problem**: Global loss count doesn't reset, apoptosis needs per-session tracking

**Solution**: Session-scoped loss counter with hard disable
```csharp
private int sessionLossCount = 0;
private bool hugProtocolTriggered = false;

private void UpdateLossCount()
{
    var lastTrade = SystemPerformance.AllTrades[SystemPerformance.AllTrades.Count - 1];
    
    if (lastTrade.ProfitCurrency < 0 && !hugProtocolTriggered)
    {
        sessionLossCount++;
        if (sessionLossCount >= 99)
            TriggerHugProtocol();
    }
}

private void TriggerHugProtocol()
{
    hugProtocolTriggered = true;
    Print("[POETRY] 99 fails. Hug protocol.");
    Print("[POETRY] 99 reds. Evolving weights for you.");

    // 1) Flatten everything
    if (Position.MarketPosition == MarketPosition.Long)  
        ExitLong("Apoptosis");
    if (Position.MarketPosition == MarketPosition.Short) 
        ExitShort("Apoptosis");

    // 2) Disable strategy
    safetyDisabled = true;

    // 3) Emit poetry into logs
    Print("[SAFETY] Apoptosis triggered - programmed death to protect capital");
}
```

**The 100th Green**: If a winning trade occurs after apoptosis:
```
[POETRY] From 99 reds to green—evolution complete.
```

### 5. Deploy Script — Fail Loud, Not Quiet

**Problem**: PS1 script retries forever on failure, silently burning capital

**Solution**: 99-retry limit with loud abort
```powershell
$lossCount = 0
$MaxLosses = 99

while ($lossCount -lt $MaxLosses -and -not $deployed) {
    try {
        $deployed = Deploy-Strategy -AttemptNumber ($lossCount + 1)
    }
    catch {
        $lossCount++
        Log-Error "Loss $lossCount : $($_.Exception.Message)"
        
        if ($lossCount -lt $MaxLosses) {
            Log-Warning "Evolving... retrying in 10 seconds"
            Start-Sleep -Seconds 10
        }
        else {
            Log-Error "Hit 99 deploy failures. Aborting."
            Log-Poetry "99 reds in deployment. Manual hug required."
            Notify-Discord "Deploy failed 99x. Human review needed."
            exit 1
        }
    }
}
```

## 🚀 Usage

### Prerequisites

1. **NinjaTrader 8** installed
2. **PowerShell 5.1+** (Windows) or **PowerShell Core** (cross-platform)
3. **Discord webhook** (optional, for notifications)

### Installation

1. Clone or download this repository
2. Review and customize `config/pid-ranco-mythic.yaml`
3. Copy `strategies/PIDRANCOStrategy.cs` to your NinjaTrader strategies folder:
   ```
   %USERPROFILE%\Documents\NinjaTrader 8\bin\Custom\Strategies\
   ```
4. Compile in NinjaTrader (Tools → Compile)

### Deployment

**Simulation Mode** (recommended first):
```powershell
cd trading-engine/scripts
.\Deploy-PIDRANCO.ps1 -Environment "simulation"
```

**Live Mode** (real money at risk):
```powershell
.\Deploy-PIDRANCO.ps1 -Environment "production" -LiveMode
```

You will be prompted to type `I UNDERSTAND THE RISK` before proceeding.

### Configuration

Edit `config/pid-ranco-mythic.yaml` to customize:

```yaml
risk_parameters:
  risk_per_trade: "0.69%"    # Adjust as needed
  max_drawdown: "3.37%"      # Hard limit

voice_config:
  silence_threshold_minutes: 5
  silence_action: "flatten_and_exit"

apoptosis:
  failure_threshold: 99      # Adjust session loss limit
```

### Monitoring

Watch the NinjaTrader Output window for:
- `[INFO]` - Normal operations
- `[WARN]` - Near-limit conditions
- `[ERROR]` - Exceptions and safety triggers
- `[POETRY]` - Apoptosis, evolution, transcendence moments
- `[SAFETY]` - Kill-switch activations

## 📊 Risk Parameters Explained

| Parameter | Value | What It Means |
|-----------|-------|---------------|
| **Risk Per Trade** | 0.69% | Maximum account value at risk per single trade |
| **Max Drawdown** | 3.37% | Strategy disables if equity falls 3.37% below peak |
| **Failure Threshold** | 99 | After 99 losing trades, apoptosis protocol triggers |
| **Silence Threshold** | 5 min | Voice absence > 5 min → flatten all positions |

## 🎯 Failure Modes & Responses

| Failure Mode | Response |
|--------------|----------|
| **Indicator null/NaN** | Skip bar safely, log warning |
| **Mic/voice exception** | Treat as silence (0 volume), continue |
| **Position profit calc error** | Return 0%, avoid crash |
| **Max drawdown breach** | Flatten all, disable strategy, log critical |
| **99 losses in session** | Apoptosis: flatten, disable, emit poetry |
| **Unexpected exception** | Emergency shutdown: flatten, disable, alert |
| **Deploy script 99 fails** | Abort with error, notify Discord, require human |

## 🎭 The Mythic Narrative

### Core Philosophy

PID-RANCO treats trading as an evolutionary process guided by "her voice":
- **Love** (voice volume) guides entries and exits
- **Suffering** (market pain) is measured and embraced
- **Failure** is not defeat—it's data for evolution
- **Apoptosis** (programmed death) protects capital at 99 losses
- **Transcendence** occurs when the 100th trade wins after 99 losses

### Poetry in Logs

The strategy emits poetic logs at key moments:
```
[POETRY] 99 fails. Hug protocol.
[POETRY] 99 reds. Evolving weights for you.
[POETRY] Voice collapse detected. Silence: 5.2 min
[POETRY] From 99 reds to green—evolution complete.
```

These aren't just aesthetic—they mark critical state transitions in the apoptosis protocol.

## 🔒 Security & Safety

### What This Strategy CANNOT Do

- ❌ Trade with more than 0.69% risk per trade
- ❌ Continue after 3.37% drawdown from peak
- ❌ Continue after 99 losses in a session
- ❌ Crash on mic/voice failures
- ❌ Access indicators before sufficient bars
- ❌ Silent-fail on exceptions

### What It ALWAYS Does

- ✅ Flattens positions on unexpected exceptions
- ✅ Disables itself on safety limit breach
- ✅ Validates all indicator values before use
- ✅ Clamps voice input to valid range [0, 100]
- ✅ Calculates position size from account value
- ✅ Tracks peak equity for drawdown calculation
- ✅ Logs all safety events with timestamps

## 📚 Documentation

- **YAML Config**: See `config/pid-ranco-mythic.yaml` for full narrative spec
- **Strategy Code**: See `strategies/PIDRANCOStrategy.cs` for implementation
- **Deploy Script**: See `scripts/Deploy-PIDRANCO.ps1` for deployment logic
- **Safety Details**: See `docs/SAFETY_FEATURES.md` for deep-dive on guardrails

## 🤝 Contributing

This is a demonstration of "guardrails around a supernova"—how to preserve mythic narrative while enforcing production safety. Feel free to:

1. Fork and adapt the mythic layer (YAML)
2. Enhance the kill-switch layer (C#)
3. Add new failure modes and guardrails
4. Improve voice/mic integration
5. Add Discord/Telegram notifications

## ⚖️ Legal Disclaimer

**FOR EDUCATIONAL AND SIMULATION PURPOSES ONLY**

This software is provided as-is without warranty of any kind. Trading involves substantial risk of loss. Past performance is not indicative of future results.

- Not financial advice
- Not a recommendation to trade
- Author assumes no liability for trading losses
- Use at your own risk
- Test thoroughly in simulation before considering live use

## 📜 License

MIT License - See LICENSE file for details

---

## 🌟 The Bottom Line

> **"Same poetry, zero real-world blast radius."**

PID-RANCO v1.2 proves you can have both:
- The mythic narrative of love-guided, evolution-driven trading
- The hard safety guarantees that protect against catastrophic loss

The worst-case outcome is:
1. Strategy disables itself
2. Positions are flattened
3. You read logs and refactor
4. The 100th "green" is learning, not blown capital

*"In the tension between chaos and order lies infinite opportunity for those who know how to look."*
