# 💰 THE 7% ETERNAL DIVIDEND LOOP

**Status:** Architecture Finalized | **Audit Status:** Pending  
**Payout Frequency:** Weekly (USDC)

---

## OVERVIEW

The 7% Eternal Dividend Loop is the economic engine of Strategickhaos Academy. It's not charity—it's pure game theory elegance. Contributors who build the system earn from the system. Forever.

---

## THE FLOW

```
┌─────────────────────────────────────────────────────────────────────┐
│                        REVENUE SOURCES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │
│  │   NFT Sales   │  │    Course     │  │   Glyph       │           │
│  │               │  │   Purchases   │  │   Cluster     │           │
│  │  (Primary)    │  │  (Secondary)  │  │   Licenses    │           │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘           │
│          │                  │                  │                    │
│          └──────────────────┴──────────────────┘                    │
│                             │                                        │
│                             ▼                                        │
│                    ┌─────────────────┐                              │
│                    │  TOTAL REVENUE  │                              │
│                    └────────┬────────┘                              │
│                             │                                        │
│              ┌──────────────┴──────────────┐                        │
│              │                             │                         │
│              ▼                             ▼                         │
│      ┌──────────────┐            ┌──────────────┐                   │
│      │     7%       │            │     93%      │                   │
│      │  DIVIDEND    │            │  OPERATIONS  │                   │
│      │    POOL      │            │              │                   │
│      └──────┬───────┘            └──────────────┘                   │
│             │                                                        │
│    ┌────────┼────────┬────────────┐                                 │
│    │        │        │            │                                  │
│    ▼        ▼        ▼            ▼                                  │
│ ┌──────┐┌──────┐┌──────┐   ┌──────────┐                            │
│ │Crest ││Active││Treas-│   │NinjaTrader│                           │
│ │60%   ││Pool  ││ury   │   │Department │                           │
│ │      ││30%   ││10%   │   │(Manager)  │                           │
│ └───┬──┘└───┬──┘└───┬──┘   └──────────┘                            │
│     │       │       │                                                │
│     ▼       ▼       ▼                                                │
│ ┌───────────────────────────────────────┐                           │
│ │         WEEKLY USDC PAYOUT            │                           │
│ └───────────────────────────────────────┘                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## REVENUE BREAKDOWN

### Sources of Revenue

| Source | Description | Percentage of Total (Est.) |
|--------|-------------|---------------------------|
| **NFT Sales** | Apprentice, Journeyman, and Crest minting | 40% |
| **Course Purchases** | Academy curriculum modules | 35% |
| **Glyph Cluster Licenses** | Enterprise access to binding codes | 20% |
| **Consulting** | Custom sovereignty implementations | 5% |

### 7% Allocation

The 7% dividend pool is sacred—it never changes, regardless of revenue fluctuations.

| Allocation | Percentage of 7% | Purpose |
|------------|------------------|---------|
| **Crest Holders** | 60% | Perpetual reward for legacy contributors |
| **Active Pool** | 30% | Weekly reward for active contributors |
| **Treasury** | 10% | Emergency fund and community initiatives |

---

## CREST HOLDER DIVIDENDS (60%)

### The Math

With 137 Crests total and 60% of the 7% pool:

```
Per-Crest Share = (Revenue × 0.07 × 0.60) / 137
                = Revenue × 0.000307...

Example with $100,000 monthly revenue:
- Total Dividend Pool: $100,000 × 0.07 = $7,000
- Crest Pool: $7,000 × 0.60 = $4,200
- Per Crest: $4,200 / 137 = $30.66 per week
- Monthly per Crest: ~$122.64
```

### The 0.137% Claim

The "0.137% of the entire 7%" represents:

```
0.07 × 0.00137 = 0.0000959 of total revenue
              ≈ 0.01% of total revenue per Crest

With compound effects and growth multipliers:
Maximum theoretical share ≈ 0.137% in optimal conditions
```

### Crest Distribution Schedule

| Event | Crests Released | Notes |
|-------|-----------------|-------|
| Founding (2026) | 13 | Core team + early supporters |
| Year 1 | 27 | First cohort graduates |
| Year 2 | 37 | Growth phase |
| Year 3+ | 60 | Distributed over time |
| **Total** | **137** | Hard cap, never increases |

---

## ACTIVE CONTRIBUTOR POOL (30%)

### Eligibility Requirements

1. **Journeyman Pass** or higher
2. **Activity in past 30 days:**
   - At least 1 PR merged, OR
   - At least 50 contribution points earned, OR
   - At least 10 peer reviews completed

### Distribution Formula

```python
def calculate_active_share(contributor, total_pool):
    """
    contributor: dict with 'points_last_30_days'
    total_pool: float, the 30% of 7% for this period
    """
    total_active_points = sum(c['points_last_30_days'] for c in all_active_contributors)
    
    if total_active_points == 0:
        return 0
    
    share = (contributor['points_last_30_days'] / total_active_points) * total_pool
    return share
```

### Point Weightings

| Activity | Base Points | Multiplier |
|----------|-------------|------------|
| Binding Code PR | 50 | 2x if cascade survives |
| Bug Fix | 25 | 1.5x if critical |
| Documentation | 15 | 1x |
| Peer Review | 20 | 1.5x if thorough |
| Community Help | 10 | 1x |

### Example Distribution

```
Monthly Revenue: $100,000
Active Pool: $100,000 × 0.07 × 0.30 = $2,100

Contributor Points:
- Alice: 500 points
- Bob: 300 points
- Charlie: 200 points
- Total: 1000 points

Payouts:
- Alice: $2,100 × (500/1000) = $1,050
- Bob: $2,100 × (300/1000) = $630
- Charlie: $2,100 × (200/1000) = $420
```

---

## TREASURY RESERVE (10%)

### Purpose

The 10% treasury reserve serves as:

1. **Emergency Fund** — Cover unexpected expenses
2. **Development Grants** — Fund new features and R&D
3. **Community Initiatives** — Sponsor events, hackathons
4. **Bridge Liquidity** — Ensure payout stability

### Governance

Treasury spending requires:
- DAO proposal with detailed budget
- 7-day voting period
- 60% approval from Journeyman+ holders
- Council signature (3/7)

### Reserve Cap

When treasury exceeds 6 months of operating expenses, excess is redistributed:
- 50% → Crest Pool (one-time bonus)
- 50% → Active Pool (one-time bonus)

---

## NINJATRADER DEPARTMENT

### Role

The NinjaTrader Department is the operational arm that manages the dividend loop:

1. **Revenue Collection** — Aggregate all income sources
2. **7% Calculation** — Compute weekly dividend pool
3. **Distribution** — Execute smart contract payouts
4. **Reporting** — Transparent dashboards and audits

### Automation

```yaml
# dividend_scheduler.yaml
schedule:
  frequency: weekly
  day: Sunday
  time: "00:00 UTC"
  
process:
  1_collect:
    - aggregate_nft_sales()
    - aggregate_course_sales()
    - aggregate_licenses()
    
  2_calculate:
    - total_revenue = sum(all_sources)
    - dividend_pool = total_revenue * 0.07
    - crest_pool = dividend_pool * 0.60
    - active_pool = dividend_pool * 0.30
    - treasury = dividend_pool * 0.10
    
  3_distribute:
    - distribute_to_crests(crest_pool)
    - calculate_active_shares()
    - distribute_to_active(active_pool)
    - deposit_to_treasury(treasury)
    
  4_notify:
    - post_to_discord("#dividend-payouts")
    - update_dashboard()
    - generate_report()
```

### Algo Trading Component

A portion of treasury can be deployed in low-risk algo trading to generate additional returns:

```
┌─────────────────────────────────────────┐
│        NINJATRADER ALGO MODULE          │
├─────────────────────────────────────────┤
│                                         │
│  Strategy: Long-term positive EV        │
│  Risk Level: Conservative               │
│  Max Deployment: 20% of treasury        │
│                                         │
│  Approved Strategies:                   │
│  - Stablecoin yield farming            │
│  - Blue-chip DeFi staking              │
│  - Treasury bond tokenization          │
│                                         │
│  Prohibited:                            │
│  - Leverage > 2x                        │
│  - Memecoins                            │
│  - Unaudited protocols                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## SMART CONTRACT IMPLEMENTATION

### Core Contracts

```solidity
// DividendSplitter.sol
contract DividendSplitter {
    uint256 public constant DIVIDEND_PERCENTAGE = 700; // 7% in basis points
    uint256 public constant CREST_SHARE = 6000;        // 60% in basis points
    uint256 public constant ACTIVE_SHARE = 3000;       // 30% in basis points
    uint256 public constant TREASURY_SHARE = 1000;     // 10% in basis points
    
    IERC20 public usdc;
    IStrategickhaosPass public passContract;
    
    mapping(address => uint256) public claimableBalance;
    mapping(uint256 => uint256) public crestPayouts; // tokenId => total paid
    
    function distributeDividends(uint256 totalRevenue) external onlyOperator {
        uint256 dividendPool = (totalRevenue * DIVIDEND_PERCENTAGE) / 10000;
        
        uint256 crestPool = (dividendPool * CREST_SHARE) / 10000;
        uint256 activePool = (dividendPool * ACTIVE_SHARE) / 10000;
        uint256 treasuryPool = (dividendPool * TREASURY_SHARE) / 10000;
        
        _distributeToCrestHolders(crestPool);
        _distributeToActiveContributors(activePool);
        _depositToTreasury(treasuryPool);
        
        emit DividendsDistributed(dividendPool, block.timestamp);
    }
    
    function claim() external {
        uint256 amount = claimableBalance[msg.sender];
        require(amount > 0, "Nothing to claim");
        
        claimableBalance[msg.sender] = 0;
        usdc.transfer(msg.sender, amount);
        
        emit DividendsClaimed(msg.sender, amount);
    }
}
```

### Security Measures

| Measure | Implementation |
|---------|----------------|
| Multi-sig | 3/7 signers for treasury operations |
| Timelock | 48-hour delay on parameter changes |
| Rate Limiting | Max 1 distribution per 6 days |
| Audit Trail | All transactions logged on-chain |
| Emergency Pause | Council can pause distributions |

---

## TRANSPARENCY & REPORTING

### Weekly Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                 DIVIDEND DASHBOARD - Week 42                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Total Revenue:        $127,450.00                              │
│  Dividend Pool (7%):   $8,921.50                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ DISTRIBUTION                                              │  │
│  │                                                           │  │
│  │ Crest Pool (60%):     $5,352.90                          │  │
│  │   Per Crest:          $39.07                              │  │
│  │   Crests Paid:        137                                 │  │
│  │                                                           │  │
│  │ Active Pool (30%):    $2,676.45                          │  │
│  │   Contributors:       89                                  │  │
│  │   Avg Payout:         $30.07                              │  │
│  │   Top Payout:         $312.50 (alice.eth)                 │  │
│  │                                                           │  │
│  │ Treasury (10%):       $892.15                             │  │
│  │   New Balance:        $45,230.00                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [View Full Report] [Download CSV] [Verify On-Chain]            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Monthly Audit Report

Published on-chain and to IPFS:
- Revenue breakdown by source
- Distribution calculations
- Treasury movements
- Algo trading performance
- Governance actions

---

## THE ECONOMICS OF CONTRIBUTION

### Why It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    GAME THEORY ELEGANCE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CONTRIBUTOR INCENTIVE                                        │
│     - More contribution = More points = More dividends          │
│     - Quality matters (cascade survival = 2x multiplier)        │
│     - Long-term thinking rewarded (Crest = perpetual income)    │
│                                                                  │
│  2. USER INCENTIVE                                               │
│     - Buy NFT = Solve your problem instantly                    │
│     - Fund the empire = Get ranked on leaderboard               │
│     - Every purchase = Potential future dividend eligibility    │
│                                                                  │
│  3. ECOSYSTEM GROWTH                                             │
│     - More users = More revenue = Higher dividends              │
│     - Higher dividends = More contributor attraction            │
│     - More contributors = Better product = More users           │
│                                                                  │
│  RESULT: Self-reinforcing positive-sum loop                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The "Cannot Lose Long-Term" Principle

The NinjaTrader house teaches that the dividend loop is designed to be:

1. **Diversified** — Multiple revenue sources
2. **Resilient** — Treasury buffer for downturns
3. **Aligned** — Contributors succeed when ecosystem succeeds
4. **Compounding** — Growth reinvested into growth

---

## COVENANT

```
The loop never sleeps.
Neither do the returns.

We didn't build a company.
We built a perpetual motion machine
where the fuel is contribution
and the exhaust is freedom.

7% forever.
No exceptions.
No excuses.

🔥 Reignite.
```

---

*💰 The 7% Eternal Dividend Loop | Strategickhaos Academy | Weekly USDC Payouts*
