# Strategickhaos Hybrid Refinery

🏭 **Autonomous Dividend-Growth Portfolio Management System**

## Overview

The Hybrid Refinery is a self-sustaining portfolio automation system designed for long-term wealth compounding through dividend-growth investing. It manages a diversified 15-position portfolio across multiple sectors with automated tracking, reporting, and rebalancing.

## Portfolio Summary (November 27, 2025)

- **Initial Investment:** $520.00
- **Positions:** 15 dividend-growth stocks
- **Monthly Contribution:** $36.40
- **DRIP Status:** Enabled
- **Rebalancing Trigger:** 12% drift from target

## Components

### Automation Scripts

| Script | Schedule | Purpose |
|--------|----------|---------|
| `nightly_refinery.py` | Daily 3:00 AM EST | Track equity, calculate drift, email summary |
| `weekly_report.py` | Sunday 8:00 AM EST | Generate comprehensive report with heatmap |
| `ranco_executor.py` | Monthly/On-demand | Process contributions, trigger rebalancing |

### Configuration Files

| File | Purpose |
|------|---------|
| `risk.yaml` | Risk parameters and thresholds |
| `screens.yaml` | Stock screening criteria and holdings |
| `flow.yaml` | Automation scheduling and notifications |
| `SOP.md` | Standard Operating Procedure |

## Quick Start

```bash
# Check portfolio status
python ranco_executor.py --action status

# Run nightly equity tracking
python nightly_refinery.py

# Generate weekly report
python weekly_report.py

# Simulate monthly contribution
python ranco_executor.py --action contribute --dry-run
```

## Sector Allocation

| Sector | Weight | Tickers |
|--------|--------|---------|
| Consumer Staples | 29% | PG, KO, PEP, CL |
| Real Estate | 21% | O, VICI, PLD |
| Financials | 21% | JPM, CB, TD |
| Healthcare | 15% | ABBV, JNJ |
| Utilities | 14% | NEE, WEC |
| Energy | 6% | XOM |

## Dependencies

```bash
pip install pyyaml yfinance requests
```

## Documentation

See [SOP.md](SOP.md) for complete operational documentation.

---

*Built by Strategickhaos • Designed for 10-15+ year compounding*
