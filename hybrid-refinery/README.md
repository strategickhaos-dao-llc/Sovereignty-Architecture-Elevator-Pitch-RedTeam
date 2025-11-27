# Hybrid Refinery - Portfolio Automation Suite

**Live Snapshot: 27 Nov 2025**

A complete portfolio automation system for the 15-ticker dividend growth strategy with DRIP enabled and monthly SwarmGate capital injection.

## Portfolio Overview

| Ticker | Shares  | Cost Basis | Target % | Current % | Under/Over |
|--------|---------|------------|----------|-----------|------------|
| JPM    | 0.1555  | $36.40     | 7%       | 7.00%     | 0.00%      |
| CB     | 0.1238  | $36.40     | 7%       | 7.01%     | +0.01%     |
| TD     | 0.617   | $36.40     | 7%       | 7.00%     | 0.00%      |
| PG     | 0.244   | $41.60     | 8%       | 8.00%     | 0.00%      |
| KO     | 0.592   | $41.60     | 8%       | 8.00%     | 0.00%      |
| PEP    | 0.206   | $36.40     | 7%       | 7.00%     | 0.00%      |
| CL     | 0.305   | $31.20     | 6%       | 6.00%     | 0.00%      |
| NEE    | 0.428   | $36.40     | 7%       | 7.00%     | 0.00%      |
| O      | 0.676   | $41.60     | 8%       | 8.01%     | +0.01%     |
| VICI   | 1.112   | $36.40     | 7%       | 7.01%     | +0.01%     |
| PLD    | 0.267   | $31.20     | 6%       | 5.99%     | -0.01%     |
| ABBV   | 0.185   | $36.40     | 7%       | 7.00%     | 0.00%      |
| JNJ    | 0.255   | $41.60     | 8%       | 8.00%     | 0.00%      |
| XOM    | 0.255   | $31.20     | 6%       | 6.00%     | 0.00%      |
| WEC    | 0.387   | $36.40     | 7%       | 7.00%     | 0.00%      |

**Total Equity: $520.10 | DRIP: ON | Monthly SwarmGate: $36.40**

## Files

- `risk.yaml` - Risk management configuration
- `flow.yaml` - Portfolio positions and target allocations
- `nightly_refinery.py` - Daily equity and drift monitoring script
- `ranco_executor.py` - Monthly rebalance execution script
- `requirements.txt` - Python dependencies

## Installation

```bash
cd hybrid-refinery
pip install -r requirements.txt
```

## Usage

### Nightly Equity Check
```bash
python nightly_refinery.py
```
Output: `2025-11-27 | Equity: $520.10 | Drift max: 0.1%`

### Monthly Rebalance (1st of Month)
```bash
python ranco_executor.py
```
Outputs buy recommendations for positions underweight by more than `MIN_BUY_THRESHOLD` (default: $3, configurable in script).

## Buy / Add-on Zones

Use these price zones for opportunistic additions:

| Ticker | Strong Add Zone | Mild Add Zone |
|--------|-----------------|---------------|
| JPM    | ≤ $210          | $220–225      |
| CB     | ≤ $250          | $260–270      |
| TD     | ≤ $54           | $56–58        |
| PG     | ≤ $155          | $160–165      |
| KO     | ≤ $62           | $64–66        |
| PEP    | ≤ $160          | $165–170      |
| CL     | ≤ $92           | $96–98        |
| NEE    | ≤ $75           | $80–82        |
| O      | ≤ $56           | $58–60        |
| VICI   | ≤ $30           | $31–32        |
| PLD    | ≤ $105          | $110–115      |
| ABBV   | ≤ $165          | $175–180      |
| JNJ    | ≤ $150          | $155–160      |
| XOM    | ≤ $105          | $110–115      |
| WEC    | ≤ $85           | $88–90        |

## Standard Operating Procedure

1. **Every 1st** → $36.40 auto-transfers in
2. **ranco_executor.py** decides what to buy (usually 2–3 names)
3. You place those fractional buys manually (30 seconds)
4. **DRIP stays ON** forever
5. **Tactical sleeve stays OFF** until equity ≥ $1,000
6. When you add lump sums → say "new capital = $X" → rescale instantly

## SwarmGate Distribution

Monthly $36.40 breakdown:
- **$20.80** → SGOV or Webull cash sweep (T-Bill)
- **$10.40** → AI-Fuel investments
- **$5.20** → Crypto ($2.60 BTC / $2.60 ETH cold storage)

## Risk Parameters

- Max single position: 9%
- Max sector exposure: 30%
- Rebalance threshold: 12% drift
- Tactical sleeve: Activates at $1,000 equity
