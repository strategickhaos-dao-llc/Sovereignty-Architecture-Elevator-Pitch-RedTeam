# Hybrid Refinery Financial System

## Strategickhaos Sovereign Income Architecture

> *"This is NOT gambling. This is ARCHITECTURE."*

---

## 🟣 Overview

The Hybrid Refinery Financial System is a **structured, rule-based, zero-emotion** approach to building sovereign income. It combines:

1. **Dividend Engine** - Safe, boring, passive income
2. **Refinery Overlay** - Algorithmic filtering and signal generation
3. **RANCO/PID Tactical Sleeve** - Mechanical structured trading
4. **Risk Management** - Non-negotiable guardrails

This system is designed to:
- Build permanent income
- Create sustainable cashflow
- Build systems that survive you
- Support philanthropic goals (ValorYield, SwarmGate)
- Achieve financial independence through **ENGINEERING, not speculation**

---

## 🔒 Non-Negotiable Guardrails

These rules are **ABSOLUTE** and cannot be bypassed:

| Rule | Limit | Description |
|------|-------|-------------|
| **Leverage** | FORBIDDEN | No exceptions, ever |
| **Options** | FORBIDDEN | No exceptions, ever |
| **Margin** | FORBIDDEN | No exceptions, ever |
| **Single Position** | ≤ 5% | Maximum allocation per stock |
| **Sector Allocation** | ≤ 20% | Maximum per sector |
| **Cash Buffer** | 10-20% | Minimum safety reserve |
| **Hard Stop Loss** | 8-12% | Below entry for non-dividend |
| **Max Drawdown** | 12% | Portfolio-wide alert threshold |

---

## 📈 1. Dividend Engine (Base Income Layer)

### What It Is

The Dividend Engine is **NOT gambling**. It's:
- Companies sharing their profits with you
- Slow, steady, extremely low risk
- Perfect for long-term security
- Like owning a vending machine that pays quarterly

### Screening Criteria

| Metric | Requirement | Notes |
|--------|-------------|-------|
| Payout Ratio | < 70% | REITs/MLPs: < 80% FFO |
| Dividend Growth | > 3% CAGR (5yr) | Consistent growth track record |
| Interest Coverage | > 4x | Financial safety margin |
| Net Debt/EBITDA | < 3x | REITs: < 6x |
| ROIC vs WACC | ROIC > WACC + 2% | Quality metric |
| ADV | > $1M | Liquidity requirement |

### Universe

- **Dividend Achievers** - 10+ years of dividend growth
- **Dividend Aristocrats** - 25+ years of dividend growth
- **High-quality REITs** - Diversified property income
- **Regulated Utilities** - Stable regulated cash flows

### Portfolio Construction

```
Target Positions: 20-30 names
Weighting: Risk-weighted (or equal-weight)
Max per Stock: 5%
Max per Sector: 20%
```

### Cash Flow Allocation

When dividends are received:
- **70%** → Reinvest in dividend holdings
- **23%** → Treasury buffer
- **7%** → SwarmGate (sovereign infrastructure)

---

## 📊 2. Refinery Overlay (Signals Layer)

### What It Is

The Refinery Overlay is **machine intelligence**, not gambling:
- Algorithms and filters
- Data processing
- Structured decision trees
- Predictive signal extraction

### Inputs

- Price and volume data
- ATR(14) volatility metrics
- Moving averages (20/50/200)
- RSI(14) momentum
- Fundamental data

### Outputs

| Watchlist | Purpose |
|-----------|---------|
| `dividends_core.csv` | Qualified dividend stocks |
| `safe_add.csv` | Attractive entry opportunities |
| `ranco_candidates.csv` | RANCO entry signals |
| `avoid_list.csv` | Stocks to avoid |

### Signal Types

#### Safe Add Signal (Dividend Dips)
- Price near 200MA (within 5%)
- ATR in downtrend (volatility compressed)
- Fundamentals intact

#### Avoid Signal
- Payout ratio stretched (> 80%)
- Earnings revisions trending down

#### RANCO Entry Signal
- All entry criteria met (see Section 3)

### Exclusions

- Within ±5 days of earnings
- ADV below $1M

---

## 📐 3. RANCO/PID Tactical Sleeve (10-20% of Capital)

### What It Is

RANCO/PID trading is **ENGINEERING**, not speculation:
- PID control loops applied to markets
- Probability cones and volatility compression
- Zero-emotion execution
- Strict rules that override human impulses

### Entry Rules (ALL must be met)

| Criterion | Requirement |
|-----------|-------------|
| Volatility | ATR% below 6-month median (compression) |
| Trend | 20MA > 50MA > 200MA (alignment) |
| Momentum | RSI(14) between 45-65 |
| Pattern | Higher low formed |
| Frequency | Weekly only (NO intraday) |

### Position Sizing

```python
# Kelly Fraction Method (Kelly / 5)
position_size = (kelly_criterion / 5) * portfolio_value

# Or Fixed Risk Method
max_risk_per_trade = 0.5% to 1% of equity
```

### Exit Rules

| Rule | Implementation |
|------|----------------|
| Initial Stop | 1.5× ATR below entry |
| Trailing Stop | 2× ATR trail |
| Profit Taking | RSI > 75, then first lower high |

### Execution

- **Staged Entry**: Enter in 3 tranches
- **Human Confirmation**: Required for all orders
- **Frequency**: Weekly evaluation only

---

## 🏦 4. Account Structure

### Core Account (70%)
- Long-term dividend holdings
- No active trading
- Quarterly rebalancing only

### Tactical Account (20%)
- RANCO positions only
- Maximum 5 open positions
- Strict stop management

### Treasury (10%)
- Cash safety buffer
- Replenished from dividends
- Used for rebalancing

### SwarmGate Allocation
- 7% of dividends flow to SwarmGate
- Supports sovereign infrastructure

---

## 🔄 5. Automation Rules

### Safe Add Staged Buy
```yaml
trigger: "core_name_dips_to_buy_zone"
conditions:
  - price_near_200ma
  - fundamentals_intact
  - cash_available
action: "place_staged_buys"
tranches: 3
requires_confirmation: true
```

### RANCO Entry
```yaml
trigger: "ranco_entry_signal"
conditions:
  - all_entry_criteria_met
  - tactical_allocation_available
action: "place_with_stop"
stop: "1.5x_atr_below_entry"
requires_confirmation: true
```

### Drawdown Risk Cut
```yaml
trigger: "portfolio_drawdown_exceeds_12pct"
action: "cut_tactical_risk_50pct"
requires_confirmation: false  # Auto-execute for safety
```

---

## 📊 6. Reporting

### Weekly Report Contents

- **Portfolio P&L**: Week-over-week performance
- **Dividend Run-Rate**: Projected annual income
- **Risk Heatmap**: Position and sector concentrations
- **SwarmGate Flow Log**: 7% allocation tracking

### Alert Types

| Alert | Trigger | Action |
|-------|---------|--------|
| Position Concentration | > 5% in single stock | Review for trimming |
| Sector Concentration | > 20% in sector | Diversify |
| Drawdown Warning | > 12% portfolio | Cut tactical 50% |
| Cash Buffer Low | < 10% | Raise cash |

---

## ✅ 7. Validation

### Backtesting

- Test rules on 5-10 years of historical data
- Validate dividend strategy through recessions
- Confirm RANCO rules with walk-forward analysis

### Monte Carlo Simulation

- 1,000+ simulations
- Model dividend cuts (10% probability, 25% magnitude)
- Recession scenarios
- Rate spike scenarios

### Drawdown Alert System

```
At 12% portfolio drawdown:
→ Cut tactical risk by 50%
→ Alert generated
→ Review positions
```

---

## 🎯 Quick Start

### Option A: Pure Dividend
- Safe, boring, passive
- Monthly/quarterly income
- Zero active trading

### Option B: Hybrid Refinery (Recommended)
- Dividends + RANCO signals
- No leverage, no gambling
- Best balance of income and growth

### Option C: Full PID-RANCO
- AI-automated trading
- Strict risk limits
- Statistically optimized

### Option D: No Trading
- Earn through software/AI contracts
- DAO treasury tools
- Completely passive

---

## 🛡️ This is NOT:

❌ High leverage  
❌ YOLO trades  
❌ Guessing or gambling  
❌ Casino trading  
❌ "Hope and pray"  
❌ Emotional decisions  

## This IS:

✅ Industrial-grade decision science  
✅ Structured rules  
✅ Automated guardrails  
✅ Zero-emotion execution  
✅ Sovereign income architecture  

---

*"You're not cheating, baby. You're building a future."*

---

## Files Reference

| File | Purpose |
|------|---------|
| `finance_models.py` | Data models for all components |
| `finance_services.py` | Service implementations |
| `finance_expert.py` | AI expert integration |
| `discovery.yml` | Configuration |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                HYBRID REFINERY SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   DIVIDEND   │    │   REFINERY   │    │    RANCO     │  │
│  │    ENGINE    │────│   OVERLAY    │────│   TACTICAL   │  │
│  │  (70% Core)  │    │  (Signals)   │    │ (20% Tactical)│  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         └─────────────┬─────┴─────────────┬─────┘           │
│                       │                   │                 │
│              ┌────────▼────────┐  ┌───────▼────────┐       │
│              │      RISK       │  │   PORTFOLIO    │       │
│              │   MANAGEMENT    │  │   ANALYTICS    │       │
│              │  (Guardrails)   │  │  (Reporting)   │       │
│              └────────┬────────┘  └───────┬────────┘       │
│                       │                   │                 │
│                       └─────────┬─────────┘                 │
│                                 │                           │
│                    ┌────────────▼────────────┐              │
│                    │    CASH FLOW ROUTING    │              │
│                    │  70% Reinvest           │              │
│                    │  23% Treasury           │              │
│                    │   7% SwarmGate          │              │
│                    └─────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Built with 🔥 by Strategickhaos Swarm Intelligence**

*Empowering sovereign financial independence through engineering, not gambling.*
