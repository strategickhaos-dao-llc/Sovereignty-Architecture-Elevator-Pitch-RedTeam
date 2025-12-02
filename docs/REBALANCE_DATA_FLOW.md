# Portfolio Rebalance Data Flow

**Phase 1 Implementation Guide for Zapier → Grok Automated Rebalancing**

## Overview

This document describes the data flow for automated portfolio rebalancing triggered by paycheck events. The system uses Grok AI to generate execution plans that respect allocation targets and safety constraints.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Paycheck  │───▶│   Zapier    │───▶│    Grok     │───▶│  Validator  │
│   (ADP)     │    │  Normalize  │    │   Planner   │    │  (Phase 2)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                  │                  │
                          ▼                  ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                   │  portfolio  │    │  Execution  │    │  Dry-Run    │
                   │    .yaml    │    │    Plan     │    │   Summary   │
                   └─────────────┘    └─────────────┘    └─────────────┘
```

## Phase 1 Flow (Current)

### 1. Trigger: Paycheck Event

**Source:** ADP email or webhook via Zapier

```json
{
  "paycheck_gross_usd": 5000,
  "paycheck_net_usd": 3750,
  "paycheck_date": "2025-11-29T00:00:00Z",
  "source": "ADP",
  "memo": "Bi-weekly paycheck"
}
```

### 2. Normalize: Zapier Code Step

```javascript
// Parse paycheck email/webhook
const paycheckEvent = {
  paycheck_gross_usd: parseFloat(inputData.gross),
  paycheck_net_usd: parseFloat(inputData.net),
  paycheck_date: new Date().toISOString(),
  source: inputData.source || 'ADP',
  memo: inputData.memo || ''
};

// Fetch portfolio.yaml from GitHub raw URL
const portfolioYaml = await fetch(
  'https://raw.githubusercontent.com/org/repo/main/portfolio.yaml'
).then(r => r.text());

// Fetch current positions from broker API
const portfolioSnapshot = await fetchBrokerPositions();

output = { paycheckEvent, portfolioYaml, portfolioSnapshot };
```

### 3. Call Grok

**System Prompt:** See `prompts/grok_rebalance_prompt.md`

**User Content:**
```json
{
  "paycheck_event": { ... },
  "portfolio_snapshot": { ... },
  "portfolio_yaml": "..."
}
```

### 4. Output Handling (Phase 1)

- Zapier parses Grok JSON response
- Human reviews trades and treasury transfer
- Manual execution via broker UI + treasury transfer

## Phase 2 Flow (Upcoming)

### 4. Validation Layer

The validator (`src/rebalance/validator.ts`) performs:

1. **Schema Validation** - Ensures all inputs match expected types
2. **Math Verification** - Recomputes investable/treasury/rebalance amounts
3. **Constraint Checks** - No margin, no shorting, min trade sizes
4. **Direction Validation** - Trades move toward targets
5. **Hard Guards** - No negative shares, no over-spend

### 5. Dry-Run Summary

Generated markdown summary for email/Slack review:

```markdown
# Portfolio Rebalance - Dry Run Summary

**Date:** 2025-11-29T12:00:00Z
**Paycheck:** $3,750.00 (net)

## Allocation Breakdown

| Item | Amount |
|------|--------|
| Investable (15% of net) | $562.50 |
| Treasury (7%) | $39.38 |
| Available for Trades | $523.12 |

## Treasury Transfer

→ **$39.38** to `swarmgate-treasury`

## Proposed Trades

| Action | Symbol | Shares | Est. Value | Reason |
|--------|--------|--------|------------|--------|
| BUY | VTI | 1.0492 | $262.30 | Rebalance toward 35% target |
| BUY | VXUS | 2.1820 | $130.92 | Rebalance toward 20% target |

## Validation Status

✅ **All checks passed**
```

### 6. Execution (Future)

- Auto-submit to broker API (for accounts with `execution_mode: "auto"`)
- Queue for manual review (for `execution_mode: "manual-review"`)
- Notify via Discord/Slack

## Configuration Files

| File | Purpose |
|------|---------|
| `portfolio.yaml` | Single source of truth for allocations and constraints |
| `prompts/grok_rebalance_prompt.md` | System prompt for Grok API calls |
| `src/rebalance/types.ts` | TypeScript/Zod schemas for all data types |
| `src/rebalance/validator.ts` | Phase 2 validation and dry-run generation |

## Key Parameters

From `portfolio.yaml`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `meta.paycheck_rebalance_pct` | % of net paycheck to invest | 15% |
| `meta.swarmgate_treasury_pct` | % of investable to treasury | 7% |
| `meta.rebalance_threshold_pct` | Trigger if off by more than | 5% |
| `constraints.liquidity.keep_cash_buffer_pct` | Minimum cash reserve | 3% |

## SwarmGate Treasury

The 7% treasury allocation supports:

- Protocol fees
- Auto-tithe functionality
- DAO treasury accumulation

Treasury transfers go to the `swarmgate-treasury` account configured in `portfolio.yaml`.

## Security Considerations

1. **No Margin** - `forbid_margin: true` prevents over-leveraging
2. **No Shorting** - `forbid_shorting: true` prevents short positions
3. **Min Trade Sizes** - Prevents inefficient micro-trades
4. **Cash Buffer** - Maintains liquidity reserve
5. **Position Caps** - `max_single_position_pct` limits concentration risk

## Next Steps

1. ✅ Phase 1: Schema and prompt definition (this PR)
2. 🔄 Phase 2: Validator integration into Zapier
3. ⏳ Phase 3: Auto-execution for approved accounts
4. ⏳ Phase 4: Multi-account and tax-loss harvesting
