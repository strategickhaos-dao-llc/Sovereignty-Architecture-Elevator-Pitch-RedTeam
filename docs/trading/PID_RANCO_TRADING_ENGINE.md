# PID-RANCO Trading Engine — Technical Design Document

**Version:** 1.0  
**Date:** 2025-11-25  
**Author:** Strategickhaos DAO LLC / Valoryield Engine  
**Status:** Research-Grade Architecture  

---

## 1. Executive Summary

The PID-RANCO Trading Engine is a **feedback controller-based** algorithmic trading system that combines:

1. **PID Control Theory** — Proportional-Integral-Derivative control adapted for market decision-making
2. **Renko/Range-Bar Price Representation** — Noise-filtered price visualization
3. **Hard Risk Guardrails** — Strict drawdown and loss constraints
4. **XAI Integration** — Explainable AI layer for regime classification and decision transparency

This document formalizes the engineering architecture and maps it against current academic research.

---

## 2. PID Controller Design

### 2.1 Core Control Terms

The trading controller adapts classical PID control theory to financial markets:

| Term | Classical Meaning | Trading Adaptation | Variable |
|------|-------------------|-------------------|----------|
| **P** (Proportional) | Current error | Raw market pain (Price − EMA) | `p_error` |
| **I** (Integral) | Accumulated error | Accumulated longing (∫ mispricing dt) | `i_accum` |
| **D** (Derivative) | Rate of change | Rate of heart change (∂Price/∂t) | `d_velocity` |

### 2.2 Mathematical Formalization

```
Control Signal: u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt)

Where:
  e(t) = Price(t) - EMA(t, period)           # Proportional error
  ∫e(τ)dτ = Σ[Price(i) - EMA(i)] for i=1..t  # Integral accumulation
  de/dt = [e(t) - e(t-1)] / Δt               # Derivative (velocity)
```

### 2.3 PID Gain Parameters

| Parameter | Symbol | Purpose | Tuning Approach |
|-----------|--------|---------|-----------------|
| Proportional Gain | `Kp` | Sensitivity to current deviation | Cross-entropy optimization on historical data |
| Integral Gain | `Ki` | Response to persistent mispricing | Bounded to prevent wind-up |
| Derivative Gain | `Kd` | Damping of rapid changes | Smoothed to reduce noise sensitivity |

### 2.4 Literature Alignment

The PID approach to trading is supported by academic research:

| Reference | Key Finding |
|-----------|-------------|
| Azhmyakov et al. (2023/2024) | CE-based PID controllers generate profitable buy/sell/hold decisions in idealized markets |
| ScienceDirect PIDD Papers | Extended PID/PIDD control for portfolio management and time series |

**Source:** [Personales UPV - PID Trading](https://personales.upv.es/thinkmind/dl/journals/soft/soft_v16_n12_2023/soft_v16_n12_2023_10.pdf)

---

## 3. Renko/RANCO Price Representation

### 3.1 Concept

Renko charts filter market noise by:
- Building bricks only when price moves by a fixed amount
- Eliminating time-based fluctuations
- Creating cleaner trend visualization

### 3.2 RANCO Adaptation

RANCO (Range-based Controlled Oscillation) extends Renko with:

| Feature | Implementation |
|---------|---------------|
| Fixed brick size | Calibrated to asset volatility (ATR-based) |
| Direction change | Requires 2x brick movement for reversal |
| Trend persistence | Accumulates in direction until reversal |

---

## 4. Risk Management Framework

### 4.1 Core Risk Parameters

```yaml
risk_parameters:
  risk_per_trade: 0.69%         # Fixed capital risk per position
  max_drawdown: 3.37%           # Hard stop on total drawdown
  loss_counter_limit: 99        # Consecutive losses before apoptosis
  apoptosis_action: "strategy_disable"
```

### 4.2 Safety Mechanisms

| Mechanism | Trigger | Action |
|-----------|---------|--------|
| `HardPanic()` | Drawdown > max_drawdown | Flatten all positions, disable strategy |
| `SafeFlatten()` | Loss counter ≥ limit | Gradual position unwind |
| `SimOnly` Router | Environment flag | Route orders to simulation only |

### 4.3 Literature Alignment

| Standard | Recommendation | Our Implementation |
|----------|----------------|-------------------|
| 2% Rule | Risk ≤2% per trade | 0.69% ✓ |
| Max Drawdown | 8-12% typical for pros | 3.37% (more conservative) ✓ |
| Funded Account Standards | Strict drawdown caps | Full compliance ✓ |

**Source:** [Incredible Charts - 2 Percent Rule](https://www.incrediblecharts.com/trading/2_percent_rule.php)

---

## 5. C# Implementation Skeleton

### 5.1 NinjaTrader / cAlgo Compatible Structure

```csharp
public class PidRancoStrategy : Strategy
{
    // === PID Parameters ===
    private double Kp = 1.0;    // Proportional gain
    private double Ki = 0.01;   // Integral gain  
    private double Kd = 0.1;    // Derivative gain
    
    // === Risk Parameters ===
    private const double RiskPerTrade = 0.0069;   // 0.69%
    private const double MaxDrawdown = 0.0337;    // 3.37%
    private const int MaxLosses = 99;
    
    // === State Variables ===
    private double integralAccum = 0;
    private double prevError = 0;
    private int lossCounter = 0;
    private bool strategyEnabled = true;
    
    // === Integral Wind-Up Protection ===
    // Bounds derived from typical price deviation range
    // Should be calibrated per asset class volatility profile
    private const double IntegralClampMin = -100;
    private const double IntegralClampMax = 100;
    
    // === Safety Guards ===
    // MinBars ensures indicators (EMA, RSI) have sufficient data
    // 50 bars allows EMA(20) to stabilize and provides buffer for volatility calculation
    // During initialization period, strategy observes market but does not trade
    private const int MinBars = 50;  // Minimum bars before trading
    
    protected override void OnBarUpdate()
    {
        // Bar guard - prevent premature execution
        // Strategy remains in observation mode until MinBars data points collected
        if (CurrentBar < MinBars) return;
        
        // Strategy kill switch
        if (!strategyEnabled) return;
        
        // Drawdown check
        if (CheckDrawdown() > MaxDrawdown)
        {
            HardPanic();
            return;
        }
        
        // Calculate PID signal
        double signal = CalculatePidSignal();
        
        // Execute decision with XAI validation
        ExecuteDecision(signal);
    }
    
    private double CalculatePidSignal()
    {
        double ema = EMA(Close, 20)[0];
        double error = Close[0] - ema;
        
        // Proportional term
        double p_term = Kp * error;
        
        // Integral term (with configurable anti-windup bounds)
        integralAccum = Math.Clamp(integralAccum + error, IntegralClampMin, IntegralClampMax);
        double i_term = Ki * integralAccum;
        
        // Derivative term
        double d_term = Kd * (error - prevError);
        prevError = error;
        
        return p_term + i_term + d_term;
    }
    
    private void HardPanic()
    {
        // Flatten all positions immediately
        if (Position.MarketPosition != MarketPosition.Flat)
        {
            ExitLong();
            ExitShort();
        }
        strategyEnabled = false;
        Log("HARD PANIC: Strategy disabled due to max drawdown breach");
    }
    
    private void SafeFlatten()
    {
        // Gradual position unwind
        // ... implementation
    }
}
```

### 5.2 Defensive Coding Patterns

| Pattern | Purpose | Implementation |
|---------|---------|---------------|
| Bar Guards | Prevent indicator NaN | `CurrentBar >= MinBars` |
| Indicator Safety | EMA/RSI only after sufficient data | Null checks, bounds validation |
| Position Routing | Sim vs. live isolation | Environment-based router |
| Exception Handling | Graceful degradation | Try-catch with SafeFlatten |

---

## 6. Assessment vs. Research Standards

### 6.1 Engineering-Grade ✓

The architecture demonstrates:
- Solid safety shell with defined kill-switches
- Plausible controller structure based on established theory
- Defensive coding patterns for live trading

### 6.2 Research-Grade (Partial)

| Requirement | Status | Gap |
|-------------|--------|-----|
| PID structure defined | ✓ | — |
| Risk parameters specified | ✓ | — |
| Data-driven gain tuning | ✗ | Needs cross-entropy optimization on historical data |
| Feature-to-PID mapping | ✗ | "herLove/heartbeat" terms need objective definitions |

### 6.3 Patent-Ready (Not Yet)

Missing for patent filing:
1. Empirical backtest results
2. Objective signal definitions (not poetic/metaphorical)
3. Demonstrated novelty over prior art

---

## 7. Next Steps for Formalization

### 7.1 Mathematical Formalization

- [ ] Define exact equations for P, I, D terms
- [ ] Specify control law → position sizing mapping
- [ ] Define `HardPanic()` trigger conditions formally
- [ ] Prove basic stability (bounded risk under assumptions)

### 7.2 Data-Driven Optimization

- [ ] Implement cross-entropy optimization for Kp, Ki, Kd
- [ ] Backtest on multiple asset classes
- [ ] Compare with baseline strategies

### 7.3 Documentation for IP Protection

- [ ] Convert poetic inputs ("herLove", "heartbeat") to measurable signals
- [ ] Document unique aspects of combined architecture
- [ ] Prepare claims matrix

---

## 8. References

1. Azhmyakov, V. et al. (2023/2024). "An Optimal PID Based Trading Strategy under the log-..." [Personales UPV](https://personales.upv.es/thinkmind/dl/journals/soft/soft_v16_n12_2023/soft_v16_n12_2023_10.pdf)

2. "Application of a Switched PIDD Type Control Strategy to..." [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S240589632300068X)

3. "On a Data-Driven Optimization Approach to the PID Based..." [Preprints.org](https://www.preprints.org/manuscript/202305.0977/v1/download)

4. "The 2 Percent Rule" [Incredible Charts](https://www.incrediblecharts.com/trading/2_percent_rule.php)

5. "On Suitability of Renko Charts for Algorithmic Trading" [ResearchGate](https://www.researchgate.net/publication/389121504_On_Suitability_of_Renko_Charts_for_Algorithmic_Trading)

---

**Cryptographic Verification:**  
Document Hash: `SHA256(PID_RANCO_TRADING_ENGINE.md)`  
Timestamp: 2025-11-25T00:00:00Z  

**UPL Compliance Notice:**  
This is a technical design document. Not financial or legal advice. Attorney review required before implementation.
