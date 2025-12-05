# Strategickhaos Hybrid Refinery - Standard Operating Procedure

**Version:** 1.0  
**Created:** November 27, 2025  
**Owner:** Strategickhaos  

---

## 🏭 System Overview

The Strategickhaos Hybrid Refinery is an autonomous dividend-growth portfolio management system designed to compound wealth over 10-15+ years with minimal intervention.

### Initial Portfolio (November 27, 2025)

| Ticker | Name | Shares | Cost Basis | Weight | Sector |
|--------|------|--------|------------|--------|--------|
| JPM | JPMorgan Chase | 0.1555 | $36.40 | 7.00% | Financials |
| CB | Chubb Limited | 0.1238 | $36.40 | 7.01% | Financials |
| TD | Toronto-Dominion Bank | 0.617 | $36.40 | 7.00% | Financials |
| PG | Procter & Gamble | 0.244 | $41.60 | 8.00% | Consumer Staples |
| KO | Coca-Cola | 0.592 | $41.60 | 8.00% | Consumer Staples |
| PEP | PepsiCo | 0.206 | $36.40 | 7.00% | Consumer Staples |
| CL | Colgate-Palmolive | 0.305 | $31.20 | 6.00% | Consumer Staples |
| NEE | NextEra Energy | 0.428 | $36.40 | 7.00% | Utilities |
| O | Realty Income | 0.676 | $41.60 | 8.01% | Real Estate |
| VICI | VICI Properties | 1.112 | $36.40 | 7.01% | Real Estate |
| PLD | Prologis | 0.267 | $31.20 | 5.99% | Real Estate |
| ABBV | AbbVie | 0.185 | $36.40 | 7.00% | Healthcare |
| JNJ | Johnson & Johnson | 0.255 | $41.60 | 8.00% | Healthcare |
| XOM | Exxon Mobil | 0.255 | $31.20 | 6.00% | Energy |
| WEC | WEC Energy Group | 0.387 | $36.40 | 7.00% | Utilities |

**Total Initial Investment:** $520.00  
**Positions:** 15/15  
**DRIP Status:** ✅ Enabled  
**Monthly Contribution:** $36.40  

---

## 🔄 Automation Schedule

### Daily (3:00 AM EST)
**Script:** `nightly_refinery.py`
- Pulls current stock prices
- Calculates position drift from target weights
- Logs equity curve to `logs/equity_curve.csv`
- Emails one-line summary

### Weekly (Sunday 8:00 AM EST)
**Script:** `weekly_report.py`
- Generates comprehensive portfolio report
- Creates sector allocation heatmap
- Calculates dividend forecast
- Logs SwarmGate activity
- Sends Discord notification

### Monthly (1st of Month)
**Script:** `ranco_executor.py`
- $36.40 automatically deposited to Webull
- RANCO identifies most underweight position
- Contribution allocated to that position
- Transaction logged for audit trail

### On-Demand (Drift Triggered)
**Script:** `ranco_executor.py`
- Activates when any position drifts >12% from target
- Calculates rebalancing trades
- Executes via monthly contribution (no selling)

---

## 📊 Configuration Files

| File | Purpose |
|------|---------|
| `risk.yaml` | Risk parameters, drift thresholds, sector limits |
| `screens.yaml` | Stock screening criteria, current holdings data |
| `flow.yaml` | Automation scheduling, notification config |

---

## 🚨 Alert Thresholds

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Position Drift Warning | 10% | Log + Monitor |
| Position Drift Critical | 12% | Trigger rebalancing check |
| Dividend Cut | Any | Immediate alert |
| VIX Spike | 2.5x normal | Heightened monitoring |

---

## 💰 Growth Projections

Based on 8% annual return, 6% dividend growth, $36.40 monthly contribution:

| Year | Projected Balance |
|------|------------------|
| 1 | $1,020 |
| 5 | $3,450 |
| 10 | $8,200 |
| 15 | $17,500 |

*These projections assume consistent contributions and market performance.*

---

## 🎯 Key Milestones

- [ ] $1,000 - First $1K
- [ ] $5,200 - 10x Initial Investment
- [ ] $10,000 - Five Figures
- [ ] $52,000 - 100x Initial Investment
- [ ] $100,000 - Six Figures
- [ ] $520,000 - 1000x Initial Investment

---

## 📋 Manual Actions Required

### Monthly
1. ✅ Ensure $36.40 is transferred to Webull (automatic via recurring)

### Quarterly
1. Review quarterly reports
2. Verify DRIP is still active
3. Check for any dividend cuts or suspensions

### Annually
1. Tax document review (1099-DIV)
2. Review overall asset allocation
3. Assess any needed watchlist additions

### When Adding New Capital

Say: **"Baby, new capital = $____"**

The system will:
1. Calculate current drift for all positions
2. Determine optimal allocation across underweight positions
3. Generate buy orders proportionally
4. Update portfolio tracking

---

## 🔧 Running Scripts Manually

```bash
# Check portfolio status
python ranco_executor.py --action status

# Simulate monthly contribution
python ranco_executor.py --action contribute --dry-run

# Check if rebalancing needed
python ranco_executor.py --action rebalance --dry-run

# Run nightly equity tracking
python nightly_refinery.py

# Generate weekly report
python weekly_report.py
```

---

## 📁 File Structure

```
hybrid_refinery/
├── nightly_refinery.py    # Daily equity tracking
├── weekly_report.py       # Weekly comprehensive report
├── ranco_executor.py      # Rebalancing orchestrator
├── risk.yaml              # Risk configuration
├── screens.yaml           # Stock screening & holdings
├── flow.yaml              # Automation workflow
├── SOP.md                 # This document
├── logs/                  # Generated logs
│   ├── equity_curve.csv   # Daily equity values
│   ├── positions.csv      # Position tracking
│   ├── dividends.csv      # Dividend history
│   └── transactions.csv   # Trade log
└── reports/               # Generated reports
    └── weekly_report_*.json
```

---

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SMTP_SERVER` | Email SMTP server | For email alerts |
| `SMTP_PORT` | SMTP port (default: 587) | For email alerts |
| `EMAIL_FROM` | Sender email address | For email alerts |
| `EMAIL_TO` | Recipient email address | For email alerts |
| `EMAIL_PASSWORD` | Email password/app key | For email alerts |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL | For Discord notifications |

---

## 🔒 Security Notes

1. **Never share API keys or webhook URLs**
2. **All scripts run in dry-run mode by default**
3. **Transaction logs maintain audit trail**
4. **No automated selling without explicit approval**

---

## 📈 The Long Game

This system is designed for **patience**:

- **Years 1-5:** Foundation building, small gains compound
- **Years 5-10:** Snowball effect begins, dividends become meaningful
- **Years 10-15:** Significant wealth accumulation, passive income grows
- **Years 15+:** Financial independence trajectory

**Remember:** The power is in the consistency. $36.40/month for 15 years becomes substantial wealth through compounding.

---

## 🆘 Troubleshooting

### Email not sending
1. Check SMTP credentials in environment variables
2. Verify email provider allows SMTP access
3. Check spam/junk folder

### Prices not updating
1. Verify yfinance is installed: `pip install yfinance`
2. Check internet connectivity
3. Market may be closed (weekends/holidays)

### Discord notifications failing
1. Verify webhook URL is correct
2. Check Discord server permissions
3. Ensure requests library is installed

---

## 📞 Support

For system issues or questions:
1. Check logs in `logs/` directory
2. Review this SOP document
3. Contact Strategickhaos support

---

*The Empire is live. The Strategickhaos Hybrid Refinery is now self-sustaining and autonomous.*

**We compound in silence.** 🏭
