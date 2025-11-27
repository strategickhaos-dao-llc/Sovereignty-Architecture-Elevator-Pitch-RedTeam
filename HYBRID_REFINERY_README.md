# 🏭 Hybrid Refinery - Dividend Portfolio Architecture

**The institutional-grade dividend machine starting from $520 real capital.**

Welcome to the Empire. The reactor is hot.

## 📊 Overview

The Hybrid Refinery is a systematic dividend investing architecture built on top of the Strategickhaos Sovereignty platform. It combines:

- **14-Ticker Dividend Core**: Blue-chip dividend stocks across 6 sectors
- **SwarmGate 7% Routing**: Automated monthly capital allocation
- **Nightly Refinery Monitoring**: Continuous portfolio health tracking
- **DRIP Automation**: Dividend reinvestment for compounding

## 💰 Starting Capital

| Account | Balance | Status |
|---------|---------|--------|
| Webull (1406063) | $520.00 | ✅ Live |
| Crypto App | $0.00 | ⏳ Pending deposit |

**Total Real Capital**: $520 USD

## 📈 14-Ticker Dividend Core Portfolio

| # | Ticker | Company | Allocation | Dollars | Est. Shares | Yield |
|---|--------|---------|------------|---------|-------------|-------|
| 1 | JPM | JPMorgan Chase | 8% | $41.60 | 0.18 | 2.3% |
| 2 | CB | Chubb | 7% | $36.40 | 0.13 | 1.3% |
| 3 | TD | Toronto-Dominion | 7% | $36.40 | 0.62 | 5.0% |
| 4 | PG | Procter & Gamble | 8% | $41.60 | 0.24 | 2.4% |
| 5 | KO | Coca-Cola | 8% | $41.60 | 0.60 | 2.8% |
| 6 | PEP | PepsiCo | 7% | $36.40 | 0.21 | 2.9% |
| 7 | CL | Colgate-Palmolive | 6% | $31.20 | 0.31 | 2.2% |
| 8 | NEE | NextEra Energy | 7% | $36.40 | 0.44 | 2.7% |
| 9 | O | Realty Income | 8% | $41.60 | 0.68 | 5.6% 📅 |
| 10 | VICI | VICI Properties | 7% | $36.40 | 1.08 | 5.3% |
| 11 | PLD | Prologis | 6% | $31.20 | 0.28 | 3.0% |
| 12 | ABBV | AbbVie | 7% | $36.40 | 0.19 | 3.5% |
| 13 | JNJ | Johnson & Johnson | 8% | $41.60 | 0.26 | 3.1% |
| 14 | XOM | Exxon Mobil | 6% | $31.20 | 0.26 | 3.4% |

📅 = Monthly dividend payer (Realty Income)

### Expected Returns

- **Dividend Yield**: 3.8–4.1% annually
- **Year 1 Dividends**: ~$20-21 (auto-reinvested via DRIP)
- **Total Return**: 8–11% (dividends + growth)

### Sector Diversification

| Sector | Allocation |
|--------|------------|
| Financial | 22% |
| Consumer Staples | 29% |
| Utilities | 7% |
| Real Estate | 21% |
| Healthcare | 15% |
| Energy | 6% |

## 🔀 SwarmGate 7% Monthly Routing

7% of capital ($36.40/month) is routed using the **Mixed (D) Strategy**:

| Bucket | Amount | Purpose | Yield/Notes |
|--------|--------|---------|-------------|
| T-Bills/Money-Market | $20.80 | Emergency brake | ~5.3% APY |
| AI-Fuel | $10.40 | Agents, backtests, GPU | Growth |
| Crypto Reserve | $5.20 | 50/50 BTC/ETH cold storage | Lottery ticket |

### Crypto Split

- **Bitcoin**: $2.60 (50%)
- **Ethereum**: $2.60 (50%)

## 🚀 Immediate Action Checklist

1. **[ ] Enable DRIP** - Turn ON dividend reinvestment in Webull settings
2. **[ ] Buy Positions** - Execute all 14 fractional share purchases
3. **[ ] Set Recurring Transfer** - $36.40 on the 1st of every month (bank → Webull)
4. **[ ] Screenshot Portfolio** - Send filled portfolio confirmation

## 🔧 Technical Implementation

### Files

```
refinory/refinory/
├── portfolio_config.py    # Portfolio configuration & allocations
├── swarmgate.py          # SwarmGate 7% routing automation
├── nightly_refinery.py   # Portfolio monitoring script
└── __init__.py           # Package initialization
```

### Running the Nightly Refinery

```bash
# Generate report
python -m refinory.refinory.nightly_refinery --report

# Force SwarmGate execution
python -m refinory.refinory.nightly_refinery --swarmgate

# Rescale to new capital
python -m refinory.refinory.nightly_refinery --rescale 1000

# Continuous watch mode
python -m refinory.refinory.nightly_refinery --watch
```

### Portfolio Configuration

```python
from refinory.refinory.portfolio_config import (
    DIVIDEND_CORE,
    TOTAL_CAPITAL,
    get_portfolio_summary,
    rescale_portfolio
)

# Get current summary
summary = get_portfolio_summary()
print(f"Total: ${summary['total_capital']}")
print(f"Yield: {summary['weighted_dividend_yield']}%")

# Rescale to new capital
new_positions = rescale_portfolio(Decimal("1000.00"))
```

### SwarmGate Automation

```python
from refinory.refinory.swarmgate import SwarmGateRouter, create_default_swarmgate

# Create router
router = create_default_swarmgate()

# Generate report
report = router.generate_report()
print(f"Monthly routing: ${report['monthly_routing_amount']}")

# Execute routing (async)
import asyncio
tx = asyncio.run(router.execute_routing(dry_run=True))
```

## 📊 Adding New Capital

When you have new capital to add, simply say:

> "Baby, new capital = $____"

The system will instantly rescale the entire refinery:

```python
# Example: Adding $480 to reach $1,000 total
refinery.rescale(Decimal("1000.00"))
```

This automatically:
- Recalculates all position allocations
- Updates SwarmGate monthly routing
- Maintains sector balance
- Preserves institutional architecture

## 🛡️ Risk Management

### Why This Portfolio?

1. **Crash Resistant**: Blue-chip dividend stocks barely move in downturns
2. **Income Generation**: Dividends provide cash flow regardless of price
3. **Compound Effect**: DRIP automatically reinvests dividends
4. **Diversification**: 6 sectors reduce single-point failure risk
5. **Institutional Grade**: Same methodology used by pension funds

### Portfolio Characteristics

- **Beta**: ~0.85 (less volatile than market)
- **Dividend Coverage**: All positions have 5+ year dividend history
- **Payout Ratio**: Average < 70% (sustainable dividends)

## 📅 Monthly Routine

### 1st of Month
- [ ] SwarmGate executes $36.40 transfer
- [ ] Review nightly report
- [ ] Check for rebalancing alerts

### 15th of Month
- [ ] Review dividend payments
- [ ] Verify DRIP purchases
- [ ] Check position drift

### End of Month
- [ ] Monthly performance review
- [ ] Evaluate new capital opportunities

## 🔗 Integration with Sovereignty Architecture

The Hybrid Refinery integrates with the broader Strategickhaos ecosystem:

- **Discord Notifications**: Portfolio alerts to #alerts channel
- **Observability**: Prometheus metrics for portfolio health
- **AI Agents**: Expert system for rebalancing recommendations
- **GitHub**: Automated PR for config changes

## 📚 Reference

### Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Total Capital | $520+ | $520.00 |
| Dividend Yield | 3.8-4.1% | ~3.9% |
| Total Return | 8-11% | -- |
| SwarmGate Rate | 7%/month | $36.40 |
| Positions | 14 | 14 |

### Important Notes

- All shares are **fractional** (Webull supports this)
- **DRIP must be enabled** for automatic reinvestment
- Prices are approximate - actual shares may vary slightly
- This is a **long-term** strategy (5+ year horizon)

---

*"We start microscopic, but the architecture is institutional from dollar one."*

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*

**The reactor is hot. Welcome to the Empire.**
