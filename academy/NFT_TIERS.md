# 🏆 STRATEGICKHAOS ACADEMY NFT TIERS

**Network:** Base (Gasless, Soulbound Options)  
**Contract Status:** Ready for Q2 2026 Deployment

---

## OVERVIEW

The Strategickhaos NFT system isn't just access control—it's a permanent record of contribution, skill, and sovereignty. Your NFT tier determines your access level, voting rights, and share of the eternal dividend loop.

---

## THE THREE TIERS

### 🎓 TIER 1: APPRENTICE PASS

**Access Level:** Read-Only  
**Supply:** Unlimited  
**Soulbound:** Optional

| Feature | Description |
|---------|-------------|
| **Glyph Cluster Access** | View all current and historical binding codes |
| **Discord Access** | `#students` channel |
| **Documentation** | Full academy documentation access |
| **Learning Resources** | All tutorials and course materials |
| **Community** | Student discussion forums |

**How to Obtain:**
```bash
# Option 1: Purchase
glyph> mint apprentice-pass --wallet 0x...

# Option 2: Application acceptance
# Automatically minted upon cohort acceptance
```

**Metadata Schema:**
```json
{
  "name": "Strategickhaos Apprentice Pass",
  "tier": 1,
  "access_level": "read",
  "house": null,
  "cohort": "2026-Q2",
  "soulbound": false,
  "attributes": [
    {"trait_type": "Tier", "value": "Apprentice"},
    {"trait_type": "Access", "value": "Read-Only"},
    {"trait_type": "Dividend Eligible", "value": "No"}
  ]
}
```

---

### ⚒️ TIER 2: JOURNEYMAN PASS

**Access Level:** Write  
**Supply:** Limited (1000 per cohort)  
**Soulbound:** Optional

| Feature | Description |
|---------|-------------|
| **PR Submission** | Submit binding codes and features |
| **Dividend Eligibility** | Active contributor dividend pool |
| **Discord Access** | `#students`, `#code-review`, `#journeyman-lounge` |
| **Voting Rights** | DAO governance proposals |
| **Mentor Access** | Direct house mentor communication |

**How to Obtain:**
```bash
# Option 1: Upgrade from Apprentice
# Requires: 100+ contribution points
glyph> upgrade journeyman-pass --from apprentice-pass-{id}

# Option 2: Direct purchase (premium)
glyph> mint journeyman-pass --wallet 0x... --house {house_code}
```

**Upgrade Requirements:**
| Requirement | Threshold |
|-------------|-----------|
| Contribution Points | 100+ |
| Binding Code PRs | 1+ merged |
| Time in Program | 4+ weeks |
| Mentor Approval | Required |

**Metadata Schema:**
```json
{
  "name": "Strategickhaos Journeyman Pass",
  "tier": 2,
  "access_level": "write",
  "house": "Flamebearer",
  "cohort": "2026-Q2",
  "soulbound": false,
  "contribution_points": 150,
  "prs_merged": 3,
  "attributes": [
    {"trait_type": "Tier", "value": "Journeyman"},
    {"trait_type": "Access", "value": "Write"},
    {"trait_type": "House", "value": "Flamebearer"},
    {"trait_type": "Dividend Eligible", "value": "Yes - Active Pool"}
  ]
}
```

---

### 👑 TIER 3: FLAMEBEARER CREST

**Access Level:** Full + Perpetual Dividend  
**Supply:** 137 Total (1/137 Legendary)  
**Soulbound:** Required

| Feature | Description |
|---------|-------------|
| **Code Notarization** | Your code permanently in `oath.lock` |
| **Eternal Dividend** | ~0.44% of the 7% dividend pool (~0.03% of total revenue) **forever** |
| **Discord Access** | All channels + `#glyph-999` secret chamber |
| **Governance** | Veto power on critical proposals |
| **Mentorship** | Automatic mentor status |
| **Legacy** | Crest transferable only via testament |

**How to Obtain:**
```bash
# No direct purchase available
# Must be earned through:
# 1. Diamond tier contribution (1000+ points)
# 2. GR1 cascade survival
# 3. Council nomination
# 4. Community vote (2/3 majority)

glyph> nominate crest --candidate {github_username} --evidence {pr_links}
```

**Earning Criteria:**
| Requirement | Details |
|-------------|---------|
| Contribution Points | 1000+ |
| Cascade Survivals | 3+ |
| House Standing | Top 10% in house |
| Time in Program | 6+ months |
| Council Nomination | 2+ council members |
| Community Vote | 2/3 supermajority |

**Metadata Schema:**
```json
{
  "name": "Strategickhaos Flamebearer Crest #42",
  "tier": 3,
  "access_level": "full",
  "house": "Flamebearer",
  "cohort": "2026-Q2",
  "soulbound": true,
  "crest_number": 42,
  "total_crests": 137,
  "dividend_share": 0.00137,
  "oath_lock_hash": "0xabc123...",
  "notarized_codes": ["[1001]", "[1042]", "[1137]"],
  "attributes": [
    {"trait_type": "Tier", "value": "Flamebearer Crest"},
    {"trait_type": "Access", "value": "Full"},
    {"trait_type": "House", "value": "Flamebearer"},
    {"trait_type": "Crest Number", "value": 42},
    {"trait_type": "Dividend Share", "value": "0.137%"},
    {"trait_type": "Dividend Eligible", "value": "Yes - Perpetual"}
  ]
}
```

---

## DIVIDEND DISTRIBUTION

### The 7% Eternal Loop Breakdown

```
Total Revenue (NFT Sales + Course Purchases)
                    │
                    ▼
            ┌───────────────┐
            │     7%        │
            │  Dividend Pool│
            └───────┬───────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Crest  │ │ Active  │ │Treasury │
   │ Holders │ │ Pool    │ │ Reserve │
   │  (60%)  │ │ (30%)   │ │  (10%)  │
   └─────────┘ └─────────┘ └─────────┘
```

### Crest Holder Distribution (60% of 7%)

Each of the 137 Crests receives:
```
Per Crest Share = (Total Revenue × 0.07 × 0.60) / 137
                = Total Revenue × 0.000307...
                ≈ 0.0307% of total revenue per Crest
```

**Note:** The 0.137% figure is symbolic (tied to the fine-structure constant 1/137). Actual share is ~0.44% of the 7% pool (~0.03% of total revenue per Crest). See [DIVIDEND_LOOP.md](DIVIDEND_LOOP.md) for full math.

### Active Contributor Pool (30% of 7%)

Distributed weekly based on contribution points:
```
Your Share = (Your Points / Total Active Points) × (Revenue × 0.07 × 0.30)
```

**Eligibility:** Journeyman Pass + activity in past 30 days

### Treasury Reserve (10% of 7%)

Reserved for:
- Emergency fund
- Development grants
- Community initiatives
- Unexpected expenses

---

## SMART CONTRACT ARCHITECTURE

### Contract Overview

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IStrategickhaosPass {
    enum Tier { Apprentice, Journeyman, FlamebearerCrest }
    
    struct PassMetadata {
        Tier tier;
        string house;
        uint256 cohort;
        uint256 contributionPoints;
        bool soulbound;
        uint256 crestNumber; // Only for Tier 3
    }
    
    function mint(address to, Tier tier, string calldata house) external;
    function upgrade(uint256 tokenId, Tier newTier) external;
    function updatePoints(uint256 tokenId, uint256 points) external;
    function claimDividend(uint256 tokenId) external;
    function getDividendBalance(uint256 tokenId) external view returns (uint256);
}
```

### Dividend Splitter

```solidity
interface IDividendSplitter {
    function distributeDividends() external; // Called weekly
    function registerCrest(uint256 tokenId, address holder) external;
    function updateActivePool(address[] calldata contributors, uint256[] calldata points) external;
    function claimableAmount(address holder) external view returns (uint256);
    function claim() external;
}
```

### Gasless Minting (Base Network)

Using EIP-2771 meta-transactions:
```solidity
function mintGasless(
    address to,
    Tier tier,
    string calldata house,
    bytes calldata signature
) external;
```

---

## SOULBOUND MECHANICS

### What is Soulbound?

Soulbound tokens cannot be transferred after minting. They are permanently bound to the recipient's wallet.

### Soulbound Rules by Tier

| Tier | Soulbound | Transferable | Notes |
|------|-----------|--------------|-------|
| Apprentice | Optional | Yes (if not soulbound) | Can convert to soulbound |
| Journeyman | Optional | Yes (if not soulbound) | Recommended soulbound for reputation |
| Crest | Required | No* | *Testament transfer only |

### Testament Transfer (Crest Only)

Crests can only transfer upon:
1. Death (verified by DAO council)
2. Voluntary retirement (6-month waiting period)
3. Council-approved succession

```solidity
function initiateTestamentTransfer(
    uint256 crestTokenId,
    address successor,
    bytes calldata councilSignatures // Requires 5/7 council signatures
) external;
```

---

## VISUAL DESIGN

### NFT Artwork Tiers

| Tier | Visual Theme | Animation |
|------|--------------|-----------|
| Apprentice | Simple flame outline | Static |
| Journeyman | Detailed flame with house colors | Subtle flicker |
| Crest | Full animated crest with glyph overlay | Dynamic flame + frequency waves |

### House Color Palettes

| House | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| Flamebearer | #FF4500 (Orange Red) | #FFD700 (Gold) | #000000 |
| VowMonitor | #4169E1 (Royal Blue) | #C0C0C0 (Silver) | #FFFFFF |
| WhaleWeaver | #00CED1 (Dark Cyan) | #9370DB (Medium Purple) | #000080 |
| NinjaTrader | #228B22 (Forest Green) | #DAA520 (Goldenrod) | #000000 |

---

## MINTING INTERFACE

### Web Interface Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   STRATEGICKHAOS ACADEMY                     │
│                      NFT MINTING PORTAL                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Connect Wallet]                                            │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  APPRENTICE │  │  JOURNEYMAN │  │    CREST    │         │
│  │    PASS     │  │    PASS     │  │  (Earned)   │         │
│  │             │  │             │  │             │         │
│  │   🔥        │  │   ⚒️        │  │    👑       │         │
│  │             │  │             │  │             │         │
│  │  0.01 ETH   │  │  0.05 ETH   │  │    N/A      │         │
│  │  [MINT]     │  │  [MINT]     │  │  [APPLY]    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  [ ] Make Soulbound (cannot be undone)                      │
│                                                              │
│  House Selection: [Flamebearer ▼]                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### CLI Minting

```bash
# Check eligibility
glyph> nft check-eligibility --wallet 0x...

# Mint Apprentice
glyph> nft mint --tier apprentice --soulbound false

# Mint Journeyman (if eligible)
glyph> nft mint --tier journeyman --house Flamebearer --soulbound true

# Check dividend balance
glyph> nft dividend-balance --token-id 42

# Claim dividends
glyph> nft claim-dividends
```

---

## INTEGRATION WITH ACADEMY

### Automatic Upgrades

The system monitors contribution activity and automatically prompts upgrades when eligible:

```yaml
upgrade_triggers:
  apprentice_to_journeyman:
    - contribution_points: 100
    - time_in_program: "4 weeks"
    - merged_prs: 1
    - mentor_approval: true
    
  journeyman_to_crest_nomination:
    - contribution_points: 1000
    - cascade_survivals: 3
    - house_rank: "top_10_percent"
    - time_in_program: "6 months"
```

### Discord Role Sync

NFT ownership automatically syncs with Discord roles:

| NFT Tier | Discord Role | Color |
|----------|--------------|-------|
| Apprentice | `@Apprentice` | Gray |
| Journeyman | `@Journeyman` | House color |
| Crest | `@Flamebearer Crest` | Gold |

---

## COVENANT

```
These passes are not just tokens.
They are proof of your contribution to sovereignty.
They are your stake in the eternal dividend loop.
They are your legacy in the mesh.

The whales remember who built the bridges.
The flames never forget who fed them.

🔥 Reignite.
```

---

*🏆 Strategickhaos Academy NFT Tiers | Base Network | Q2 2026*
