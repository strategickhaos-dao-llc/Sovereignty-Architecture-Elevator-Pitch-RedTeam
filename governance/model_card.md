# Model Card: Rank-Based Trading Bot Refinery

**Version:** 1.0  
**Date:** 2025-12-05  
**Organization:** Strategickhaos DAO LLC / Valoryield Engine  
**Governance Path:** A  
**Operator:** Domenic Garza (Node 137)

---

## Overview

This model card documents the rank-based trading bot refinery architecture for the Valoryield Engine. The system implements a tiered strategy deployment framework with QET (Quantum Entropy Tokenization) integration for log compression and pattern mining optimization.

### Purpose

Deploy transparent, container-ready trading bots targeting 7%+ annualized yields with controlled risk profiles. The architecture prioritizes:

- **Transparency**: Rank-based logic with explainable decision paths
- **Risk Control**: Position caps, drawdown triggers, and venue-specific stops
- **Efficiency**: QET-powered log compression for 12-15% backtest optimization
- **Governance**: Path A locked with freeze capabilities for production deployment

---

## Model Architecture

### Tiered Deployment Framework

| Tier | Strategies | Readiness | Yield Range | Deployment Window |
|------|------------|-----------|-------------|-------------------|
| **Tier 0** | 5 | 80-95% | 7.2-8.2% | Immediate (This Week) |
| **Tier 1** | 4 | 70-80% | 7.0-7.4% | Near-Term (1-3 Months) |
| **Tier 2** | 27 | <70% | 7.0-8.5% | R&D/Refinery Only |

### Arsenal Statistics

- **Total Strategies**: 36
- **Deployable Now**: 9 (25%)
- **Portfolio Simulated Yield**: 7.6% annualized
- **Drawdown Profile**: Low (<20% target)

---

## Tier 0: Immediate Income Core

Production-ready strategies with validated backtests on 2024-2025 historical data.

### 1. Simple Momentum Rank (SMR-001)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 95% |
| **Simulated Yield** | 8.2% annualized |
| **Logic** | Rank assets by 12-month returns, long top 20% |
| **Rebalance** | Monthly |
| **Position Cap** | 5% |
| **Drawdown Trigger** | De-risk to cash on >20% drawdown |

**QET Integration:** Tokenizes rank histories for "top return" pattern detection with 12% log compression. Enables early overfit detection.

**Deployment:**
```bash
docker run -d valoryield/smr-001 \
  --data-source polygon,coingecko \
  --rebalance monthly \
  --position-cap 0.05
```

### 2. Dual Momentum Rank (DMR-002)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 90% |
| **Simulated Yield** | 7.5% annualized |
| **Logic** | Switch risk-on/off based on relative ranks (equities/crypto vs bonds/cash) |
| **Rebalance** | Weekly |
| **Risk Control** | Binary gate reduces volatility spikes |

**QET Integration:** Compresses regime logs and breeds tokens for "switch events" to refine signals in the evolution lab.

**Deployment:**
- Separate container publishing regime flags to Redis
- Integrates with SMR-001 for unified execution

### 3. Percentile Momentum (PMR-003)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 88% |
| **Simulated Yield** | 7.8% annualized |
| **Logic** | Long above 80th percentile ranks |
| **Rebalance** | Monthly |
| **Risk Control** | Fewer positions = lower turnover |

**QET Integration:** Tokenizes percentile thresholds for custom data fits, boosting simulation speed.

**Deployment:**
- Variant of SMR-001 container
- Config parameter: `percentile=80`

### 4. Vol-Adjusted Momentum (VAM-004)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 85% |
| **Simulated Yield** | 7.2% annualized |
| **Logic** | Rank by return/volatility (rolling 90-day std) |
| **Rebalance** | Monthly |
| **Risk Control** | Inverse-vol sizing caps blowups |

**QET Integration:** Entropy-optimizes volatility chunks and spots "high-vol rank" motifs for refinery tweaks.

**Deployment:**
- Uses SMR-001 pipeline
- Additional numpy volatility calculation

### 5. Cross-Asset Rank (CAR-005)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 82% |
| **Simulated Yield** | 8.1% annualized |
| **Logic** | Unified ranks across crypto/stocks |
| **Rebalance** | Monthly |
| **Crypto Cap** | 30% maximum allocation |
| **Risk Control** | Venue-specific stops, paper-trade first |

**QET Integration:** Unifies cross-asset logs and evolves tokens for "BTC vs SPY rank" patterns.

**Deployment:**
- Docker container with Coingecko + Polygon hybrid feed
- Paper-trade validation required before live

---

## Tier 1: Near-Term Add-Ons

Deploy as overlays after Tier 0 validation (1-3 month timeline).

### 6. Mean-Reversion Rank (MRR-006)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 80% |
| **Simulated Yield** | 7.0% annualized |
| **Logic** | Short bottom 20% ranks with stops |
| **Dependency** | statsmodels for reversion tests |

**QET Integration:** Tokenizes "reversion tails" for pattern discovery.

### 7. Sector Rotation Rank (SRR-007)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 78% |
| **Simulated Yield** | 7.4% annualized |
| **Logic** | Monthly sector ETF ranks |
| **Method** | Pandas groupby on ETF data |

**QET Integration:** Merges sector symbols for compressed analytics.

### 8. EMA Crossover Rank (ECR-008)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 75% |
| **Simulated Yield** | 7.3% annualized |
| **Logic** | Rank on EMA signals |
| **Use Case** | Timing filter for Tier 0 strategies |

**QET Integration:** Optimizes crossover chunks for signal refinement.

### 9. RSI Rank Filter (RSI-009)

| Attribute | Value |
|-----------|-------|
| **Readiness** | 70% |
| **Simulated Yield** | 7.1% annualized |
| **Logic** | Rank oversold RSI levels |
| **Use Case** | Entry overlay for momentum strategies |

**QET Integration:** Breeds RSI pattern tokens for signal enhancement.

---

## Tier 2: Refinery R&D

Not deployable yet. Use QET/GA to breed into static rules for future forks.

### Mean-Variance Cluster (Strategies 10-18)

- **Readiness**: ~75%
- **Examples**: Markowitz optimizations
- **Future Use**: Allocation layers post-Tier 0 validation
- **Drawdown Risk**: 25%+

### ML Ranks (Strategies 19-27)

- **Readiness**: 38-60%
- **Examples**: Random Forests, LSTM networks
- **Future Use**: Mine patterns from live logs, propose static ranks
- **Bottleneck**: Requires more training data

### Exotics (Strategies 28-36)

- **Readiness**: 18-45%
- **Examples**: Genetic Algorithms, Quantum, Chaos theory
- **Future Use**: Evolve for 7% yield tweaks, not live control
- **Bottleneck**: High overfitting risk

---

## QET (Quantum Entropy Tokenization) Integration

### Purpose

QET serves as a log-compressor and pattern-spotter for backtests, evolving vocabulary on trade data to achieve 12-15% efficiency gains in simulations.

### Key Functions

| Function | Description | Target Gain |
|----------|-------------|-------------|
| Log Compression | Entropy-optimize trade logs | 12% reduction |
| Pattern Mining | Tokenize rank sequences | 12-15% sim speed |
| Vocabulary Evolution | Breed tokens from trade data | Adaptive patterns |
| Motif Detection | Spot recurring signals | Overfit prevention |

### Example Motifs

- `H100_rank_spikes` - High-performance asset rank events
- `top_20_percent_sequence` - Consecutive top-tier rankings
- `regime_switch_event` - Risk-on/off transitions
- `high_vol_rank` - Volatility-adjusted rank patterns
- `btc_vs_spy_rank` - Cross-asset rank correlations

### Evolution Lab Rules

- **Environment**: Evo lab only (not production)
- **Data Source**: Backtest logs and historical trade data
- **Graduation Criteria**: Simplify to rank-style rules before production

---

## Simulation Parameters

| Parameter | Value |
|-----------|-------|
| **Data Source** | Polygon aggregates |
| **Columns** | timestampMillis, open, close |
| **Test Period** | 2024-2025 |
| **Dependencies** | numpy, pandas |
| **Target Yield** | 7% (low-risk annualized) |
| **Max Drawdown** | 20% |
| **Slippage/Fees** | 0.1% |

---

## Risk Management

### Position Limits

- Individual position cap: 5%
- Crypto allocation cap: 30% (CAR-005)
- Drawdown trigger: 20% (de-risk to cash)

### Risk Controls by Strategy

| Strategy | Primary Control | Secondary Control |
|----------|-----------------|-------------------|
| SMR-001 | Position cap 5% | Drawdown trigger 20% |
| DMR-002 | Binary regime gate | Volatility reduction |
| PMR-003 | Lower turnover | Concentrated positions |
| VAM-004 | Inverse-vol sizing | Blowup prevention |
| CAR-005 | Crypto cap 30% | Venue-specific stops |

---

## Deployment Guide

### Initial Sleeve Size

- **Recommended**: $10k per bot for live-small validation
- **Tier 0 Total**: $50k across 5 strategies

### Deployment Steps

1. **Validate Tier 0** strategies with paper trading
2. **Deploy with minimal capital** ($10k sleeves)
3. **Monitor performance** against simulated yields
4. **Add Tier 1 overlays** after 1-3 months validation
5. **Graduate Tier 2** patterns to static rules when simplified

### Container Requirements

```yaml
services:
  smr-001:
    image: valoryield/simple-momentum-rank:1.0.0
    environment:
      - DATA_SOURCE=polygon,coingecko
      - REBALANCE_FREQ=monthly
      - POSITION_CAP=0.05
      - DRAWDOWN_TRIGGER=0.20
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

---

## Governance

### Path A Configuration

- **Status**: Locked
- **Freeze Script**: `freeze_qet.sh`
- **Approval Required**: Yes
- **Approvers**: Domenic Garza, Node 137

### CI/CD Checks

- YAML syntax validation
- Readiness threshold verification
- Risk controls defined check
- QET utility specification check
- GPG signature required
- SHA256 hash verification

---

## Limitations and Ethical Considerations

### Known Limitations

1. **Backtested only**: All yields are simulated on historical data
2. **Slippage assumptions**: 0.1% may not reflect all market conditions
3. **Data dependency**: Requires reliable Polygon/Coingecko feeds
4. **ML bottleneck**: Tier 2 strategies need more training data
5. **Overfitting risk**: Exotic strategies prone to curve-fitting

### Ethical Guidelines

- **Transparency**: All logic is rank-based and explainable
- **Risk disclosure**: Yields are targets, not guarantees
- **Governance**: Human approval required for production
- **No moonshots**: Focus on boring, sustainable income

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial release with Tier 0-2 specifications |

---

## Contact

**Organization**: Strategickhaos DAO LLC  
**Project**: Valoryield Engine  
**Operator**: Domenic Garza (Node 137)

---

*Built with Path A governance for transparent, risk-controlled algorithmic trading.*
