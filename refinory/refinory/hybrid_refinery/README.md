# Strategickhaos Hybrid Refinery

**A comprehensive hybrid investment management system for the Strategickhaos ecosystem.**

## 🔵 System Architecture

The Hybrid Refinery combines two powerful investment engines:

```
┌────────────────────────────────────────────────────────────────────┐
│                    STRATEGICKHAOS HYBRID REFINERY                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐   │
│  │  DIVIDEND ENGINE    │    │   RANCO/PID TACTICAL OVERLAY    │   │
│  │  (Core - 85%)       │    │   (Attack Mode - 15% cap)       │   │
│  │                     │    │                                  │   │
│  │  • Achievers        │    │  • ATR Compression Detection     │   │
│  │  • Aristocrats      │    │  • Trend Confirmation            │   │
│  │  • Quality REITs    │    │  • RSI Sweet Spot               │   │
│  │  • Utilities        │    │  • Higher Low Structure          │   │
│  └──────────┬──────────┘    └───────────────┬─────────────────┘   │
│             │                               │                      │
│             ▼                               ▼                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    FLOW ROUTING                               │ │
│  │  70% → Core Reinvest │ 23% → Treasury Buffer │ 7% → SwarmGate │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    AUTOMATION ENGINE                          │ │
│  │  Nightly: Screen → Signal → CSV → Brief                       │ │
│  │  Weekly:  Dividend Run Rate │ Drawdown │ SwarmGate Log        │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

## 💠 Core Components

### A) Dividend Engine (Stable Yield Reactor)

**Purpose:** Slow, compounding, cannot-die machine.

**Screening Logic (Daily or Weekly):**
1. Dividend Achievers + Aristocrats + Quality REITs & regulated utilities
2. Hard filters:
   - Payout Ratio < 70% (REIT FFO Payout < 80%)
   - 5-yr Dividend CAGR > 3%
   - Interest Coverage > 4×
   - Net Debt/EBITDA < 3× (REITs < 6×)
   - ROIC − WACC > 2% (economic profit positive)

**Portfolio Construction:**
- 20–25 stocks
- Equal weight or volatility weight
- 5% max position weight

### B) RANCO/PID Tactical Overlay

**Purpose:** Small, lethal, mechanical trades.
**Cap:** 15% of entire portfolio

**Entry Rules:**
- ATR% < 6-mo median (volatility compression ready to expand)
- Uptrend: 20 > 50 > 200
- RSI 45–65 (momentum but not overbought)
- Higher low forms (structural confirmation)

**Risk & Stop:**
- Risk per trade: 0.5–1.0%
- Stop: 1.5× ATR
- Trail: 2× ATR
- Exit: Trail hit OR RSI > 75 then first lower high

**Timeframe:** Weekly candles only (less noise, more signal)

### C) SwarmGate Router (7% Flow)

Routes dividend income to optimal destinations:
- **A)** Short-term treasuries - Safe haven
- **B)** Crypto reserve - Asymmetric upside
- **C)** AI-fuel account - Fund AI operations
- **D)** Mixed - Diversified across destinations
- **E)** Auto-optimal - AI decides optimal routing

## 🚀 Quick Start

### 1. Configuration

```python
from refinory.hybrid_refinery import HybridRefineryConfig, SwarmGateDestination

# Create configuration
config = HybridRefineryConfig(
    total_capital=100000.0,  # Your total capital
    swarmgate_destination=SwarmGateDestination.AUTO_OPTIMAL,
    user_stock_picks=["KO", "MCD", "O", "VICI", "ABBV", "JNJ", "PG"],
)

# Validate configuration
errors = config.validate()
if errors:
    print(f"Config errors: {errors}")
```

### 2. Initialize Components

```python
from refinory.hybrid_refinery import (
    DividendEngine,
    RANCOPIDEngine,
    PortfolioManager,
    StockScreener,
    SwarmGateRouter,
    AutomationEngine,
)

# Initialize all components
dividend_engine = DividendEngine(config)
ranco_engine = RANCOPIDEngine(config)
portfolio_manager = PortfolioManager(config)
screener = StockScreener(config)
swarmgate = SwarmGateRouter(config)

automation = AutomationEngine(
    config,
    portfolio_manager=portfolio_manager,
    screener=screener,
    ranco_engine=ranco_engine,
    swarmgate=swarmgate,
)
```

### 3. Run Screening

```python
from refinory.hybrid_refinery.screener import create_sample_universe

# Screen universe
universe = create_sample_universe()
output = screener.run_screen(universe)

# Results
print(f"Core candidates: {output.core_count}")
print(f"Safe to add: {output.safe_add_count}")
print(f"Avoid: {output.avoid_count}")
print(f"RANCO candidates: {output.ranco_count}")
```

### 4. Execute Nightly Job

```python
# Run nightly cron job
job = automation.run_nightly_job()

# Check results
print(f"Status: {job.status.value}")
print(f"Signals: {job.signals_generated}")
print(f"CSV files generated at: {job.screener_output.output_directory}")
```

### 5. Generate Weekly Report

```python
# Generate weekly report
report = automation.generate_weekly_report()

# View key metrics
print(f"Portfolio Value: ${report.portfolio_value:,.0f}")
print(f"Dividend Run Rate: ${report.dividend_run_rate:,.0f}/year")
print(f"Current Drawdown: {report.current_drawdown:.1%}")
```

## 📊 Output Files

The screener generates 4 CSV lists nightly:

| File | Description |
|------|-------------|
| `dividends_core_YYYYMMDD.csv` | Passed all filters, ready for core portfolio |
| `safe_add_YYYYMMDD.csv` | Safe to add with minor filters failed |
| `avoid_YYYYMMDD.csv` | Failed critical filters, avoid |
| `ranco_candidates_YYYYMMDD.csv` | Suitable for tactical overlay |

## 🛡️ Guardrails

### Position Limits
- Max positions: 25
- Min positions: 20
- Max position weight: 5%
- Max sector weight: 25%

### Tactical Allocation
- Cap: 15% of entire portfolio
- Risk per trade: 0.5-1.0%

### Drawdown Management
```
If DD > 12% → Cut tactical size in half until recovery
```

## 📅 Automation Schedule

### Nightly Cron Job (10 PM)
```cron
0 22 * * * /path/to/nightly_cron.py
```

Tasks:
1. Pull market data
2. Apply screening filters
3. Generate 4 CSV lists
4. Email 1-page brief

### Weekly Report (Monday 8 AM)
```cron
0 8 * * 1 /path/to/weekly_report.py
```

Includes:
- Dividend run rate
- Drawdown and sector heatmap
- Tactical win rate
- SwarmGate 7% routing log

## 🧪 Validation & Backtesting

```python
from refinory.hybrid_refinery import ValidationEngine, StressScenario
from datetime import date

# Initialize validation engine
validator = ValidationEngine(config)

# Run backtest
backtest = validator.run_backtest(
    start_date=date(2014, 1, 1),
    end_date=date(2024, 1, 1),
    initial_capital=100000,
)
print(f"Annualized Return: {backtest.annualized_return:.1%}")
print(f"Max Drawdown: {backtest.max_drawdown:.1%}")
print(f"Sharpe Ratio: {backtest.sharpe_ratio:.2f}")

# Run stress test
stress = validator.run_stress_test(
    StressScenario.COVID_2020,
    current_portfolio_value=100000,
)
print(f"Stressed Value: ${stress['impact']['portfolio_after']:,.0f}")

# Monte Carlo simulation
monte_carlo = validator.run_monte_carlo(
    initial_capital=100000,
    years=10,
    simulations=1000,
)
print(f"Median Outcome: ${monte_carlo.median_final_value:,.0f}")
print(f"Probability of Success: {monte_carlo.prob_positive_return:.0%}")
```

## 🔧 Configuration Reference

### HybridRefineryConfig

```python
HybridRefineryConfig(
    # Capital and routing
    total_capital=100000.0,
    swarmgate_destination=SwarmGateDestination.AUTO_OPTIMAL,
    user_stock_picks=["KO", "MCD", "O"],
    
    # Screening filters
    screening=ScreeningFilters(
        max_payout_ratio=0.70,
        max_reit_ffo_payout=0.80,
        min_dividend_cagr_5yr=0.03,
        min_interest_coverage=4.0,
        max_net_debt_ebitda=3.0,
        max_reit_net_debt_ebitda=6.0,
        min_roic_wacc_spread=0.02,
        min_adv_million=1.0,
        earnings_exclusion_days=5,
    ),
    
    # Portfolio guardrails
    guardrails=PortfolioGuardrails(
        max_positions=25,
        min_positions=20,
        max_position_weight=0.05,
        max_sector_weight=0.25,
        tactical_max_allocation=0.15,
        core_reinvest_pct=0.70,
        treasury_buffer_pct=0.23,
        swarmgate_pct=0.07,
        max_drawdown_threshold=0.12,
        tactical_reduction_on_drawdown=0.50,
    ),
    
    # Tactical parameters
    tactical=TacticalParameters(
        atr_compression_threshold=1.0,
        rsi_entry_min=45.0,
        rsi_entry_max=65.0,
        require_uptrend=True,
        risk_per_trade_min=0.005,
        risk_per_trade_max=0.01,
        stop_atr_multiplier=1.5,
        trail_atr_multiplier=2.0,
        rsi_overbought_exit=75.0,
        candle_timeframe="weekly",
    ),
)
```

## 📈 Flow Routing

Dividend income is automatically routed:

| Destination | Percentage | Purpose |
|-------------|------------|---------|
| Core Reinvest | 70% | Compound the dividend engine |
| Treasury Buffer | 23% | Reserves for dislocations |
| SwarmGate | 7% | Autonomous AI routing |

## 🤖 Integration with Refinory Platform

The Hybrid Refinery integrates with the main Refinory AI Agent Orchestration Platform:

```python
from refinory import app
from refinory.hybrid_refinery import HybridRefineryConfig

# Access via FastAPI endpoints (when configured)
# POST /api/v1/hybrid-refinery/screen
# POST /api/v1/hybrid-refinery/signal
# GET /api/v1/hybrid-refinery/portfolio
# GET /api/v1/hybrid-refinery/report
```

## 📞 Support

- **Discord**: Join the Strategickhaos Discord server
- **Issues**: GitHub Issues
- **Documentation**: This README and inline code documentation

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
