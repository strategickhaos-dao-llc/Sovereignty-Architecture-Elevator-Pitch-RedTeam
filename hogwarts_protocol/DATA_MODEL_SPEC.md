# Hogwarts Protocol Data Model Specification

## Overview

The Hogwarts Protocol provides a blockchain-integrated educational platform that combines:
- **Off-chain storage** (PostgreSQL): Full-featured data model with relationships
- **On-chain registry** (Ethereum/compatible): Proof of ownership, integrity, and value routing

This document defines the minimal on-chain data model mapping to PostgreSQL off-chain storage.

---

## 1. Core Entities

### 🎓 Student

**Purpose**: Learner identity with blockchain wallet integration

| Field | Off-Chain (PostgreSQL) | On-Chain (Smart Contract) |
|-------|----------------------|--------------------------|
| `student_id` | UUID PRIMARY KEY | N/A (off-chain only) |
| `edu_email` | VARCHAR(255) | N/A |
| `edu_institution` | VARCHAR(255) | N/A |
| `display_name` | VARCHAR(255) | N/A |
| `wallet_address` | VARCHAR(42) | `address owner` (in Spell NFT) |
| `total_cft` | NUMERIC(36,18) | `balanceOf(address)` |
| `governance_weight` | NUMERIC(36,18) | `stakedBalance[address]` |

**Key Insight**: Student identity lives primarily off-chain. The wallet address is the bridge to on-chain ownership.

---

### 🔮 Spell (Educational Artifact)

**Purpose**: Code submission / completed work that can be verified and registered

| Field | Off-Chain (PostgreSQL) | On-Chain (HogwartsRegistry) |
|-------|----------------------|--------------------------|
| `spell_id` | UUID PRIMARY KEY | `offChainId` (string reference) |
| `owner_id` | UUID REFERENCES hp_students | `owner` (address) |
| `content_hash` | VARCHAR(64) | `contentHash` (bytes32) |
| `course_code` | via JOIN to hp_courses | `courseCode` (string) |
| `assignment_code` | via JOIN to hp_assignments | `assignmentCode` (string) |
| `grade` | VARCHAR(10) | `grade` (string) |
| `institution` | via JOIN | `institution` (string) |
| `verified_at` | TIMESTAMP | `verifiedAt` (uint256) |
| `on_chain_token_id` | BIGINT | Token ID in ERC721 |
| `on_chain_tx_hash` | VARCHAR(66) | Transaction hash |

**On-Chain Record Structure** (SpellRecord):
```solidity
struct SpellRecord {
    address owner;
    bytes32 contentHash;
    string courseCode;
    string assignmentCode;
    string grade;
    string institution;
    uint256 verifiedAt;
    string offChainId;
}
```

---

### 📚 Course

**Purpose**: Educational module container for assignments

| Field | Off-Chain (PostgreSQL) | On-Chain |
|-------|----------------------|----------|
| `course_id` | UUID PRIMARY KEY | N/A (off-chain only) |
| `course_code` | VARCHAR(50) | Referenced in Spell.courseCode |
| `course_name` | VARCHAR(255) | N/A |
| `institution` | VARCHAR(255) | Referenced in Spell.institution |
| `xp_multiplier` | NUMERIC(5,2) | N/A |
| `instructor_share_pct` | NUMERIC(5,4) | N/A (handled off-chain) |

**Key Insight**: Courses are entirely off-chain. Only the `course_code` is stamped into spell records.

---

### 💰 CFTBalance (CourseForge Token)

**Purpose**: Non-speculative utility token for XP, features, and governance

| Field | Off-Chain (PostgreSQL) | On-Chain (CourseForgeToken) |
|-------|----------------------|--------------------------|
| `balance_id` | UUID PRIMARY KEY | N/A |
| `student_id` | UUID REFERENCES | address mapping |
| `available_balance` | NUMERIC(36,18) | `balanceOf(address)` |
| `staked_balance` | NUMERIC(36,18) | `stakedBalance[address]` |
| `lifetime_earned` | NUMERIC(36,18) | `lifetimeEarned[address]` |

**Synchronization**: Off-chain balances should mirror on-chain state. The off-chain database serves as the "fast read" layer while on-chain is the "source of truth" for disputes.

---

## 2. On-Chain Data Model

### HogwartsRegistry (ERC721)

```
┌─────────────────────────────────────────────────────────────┐
│                    HOGWARTS REGISTRY                        │
│                    (Spell NFT/SBT)                          │
├─────────────────────────────────────────────────────────────┤
│ tokenId (uint256)          → NFT identifier                 │
│ owner (address)            → Wallet of spell creator        │
│ contentHash (bytes32)      → SHA-256 of code                │
│ courseCode (string)        → "MAT-243"                      │
│ assignmentCode (string)    → "Project One"                  │
│ grade (string)             → "B+"                           │
│ institution (string)       → "SNHU"                         │
│ verifiedAt (uint256)       → Block timestamp                │
│ offChainId (string)        → UUID reference                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ soulboundMode = true
                              ▼
                    [Non-transferable by default]
```

### CourseForgeToken (ERC20)

```
┌─────────────────────────────────────────────────────────────┐
│                    COURSEFORGE TOKEN                        │
│                    (CFT - Utility Token)                    │
├─────────────────────────────────────────────────────────────┤
│ balanceOf[address]         → Available CFT                  │
│ stakedBalance[address]     → Governance-locked CFT          │
│ lifetimeEarned[address]    → Total ever minted              │
│ lifetimeSpent[address]     → Total ever burned              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ transfersEnabled = false
                              ▼
                    [Non-transferable by default]
```

---

## 3. Data Flow

### Student Completes Assignment

```
┌──────────────────┐
│  1. Student      │
│  completes work  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  2. Code hashed  │
│  (SHA-256)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  3. Spell stored │
│  in PostgreSQL   │
│  (status: draft) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. Verifier     │
│  reviews & grades│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  5. hp_verify_spell() function executes:             │
│     - Updates spell status to 'verified'             │
│     - Calculates XP (base * multiplier * grade bonus)│
│     - Mints CFT to student's balance                 │
│     - Records CFT transaction                        │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  6. On-chain registration (optional):                │
│     - HogwartsRegistry.registerSpell() called        │
│     - NFT minted to student's wallet                 │
│     - Spell status updated to 'certified'            │
│     - Transaction hash stored                        │
└──────────────────────────────────────────────────────┘
```

### CFT Minting Flow

```
┌─────────────────┐      ┌─────────────────┐
│  SPELL VERIFIED │ ───► │  CALCULATE XP   │
└─────────────────┘      └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
         ┌─────────────────┐         ┌─────────────────┐
         │  OFF-CHAIN      │         │  ON-CHAIN       │
         │  hp_mint_cft()  │         │  CFT.mint()     │
         │                 │         │                 │
         │  - Update       │         │  - Mint ERC20   │
         │    balance      │         │  - Emit event   │
         │  - Record       │         │                 │
         │    transaction  │         │                 │
         └─────────────────┘         └─────────────────┘
```

---

## 4. PostgreSQL Schema Summary

```sql
-- Core tables
hp_students          -- Learner profiles with wallet addresses
hp_courses           -- Educational modules
hp_assignments       -- Tasks within courses
hp_spells            -- Completed work artifacts
hp_cft_balances      -- Token balances per student
hp_cft_transactions  -- Audit trail of all CFT movements
hp_revenue_routes    -- Revenue split configuration per spell
hp_spell_licenses    -- Marketplace transactions

-- Views
hp_transcript        -- On-chain transcript representation

-- Functions
hp_mint_cft()        -- Mint tokens and record transaction
hp_stake_cft()       -- Lock tokens for governance
hp_verify_spell()    -- Complete spell verification workflow
```

---

## 5. Revenue Routing Model

When a spell is licensed in the marketplace:

```
┌────────────────────────────────────────────────────────┐
│              SPELL LICENSE PURCHASED                   │
│                    ($100 USD)                          │
└────────────────────────┬───────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  CREATOR │   │ PLATFORM │   │ CHARITY  │
    │   60%    │   │   20%    │   │   10%    │
    │  ($60)   │   │  ($20)   │   │  ($10)   │
    └──────────┘   └──────────┘   └──────────┘
          │              │              │
          │              │              └──► ValorYield Pool
          │              │
          │              └──► Platform Operations
          │
          └──► Creator Wallet (Stripe payout)

                         │
                         ▼
                   ┌──────────┐
                   │SCHOLARSHIP│
                   │   10%    │
                   │  ($10)   │
                   └──────────┘
                         │
                         └──► Scholarship Fund
```

---

## 6. Security Considerations

### Off-Chain
- All wallet addresses validated with regex: `^0x[a-fA-F0-9]{40}$`
- Content hashes validated: `^[a-fA-F0-9]{64}$`
- Foreign key constraints enforce referential integrity
- Triggers automatically update timestamps

### On-Chain
- Role-based access control (VERIFIER_ROLE, PLATFORM_ROLE)
- Soulbound mode prevents unauthorized transfers
- Content hash uniqueness prevents duplicate registrations
- OpenZeppelin contracts for battle-tested security

---

## 7. Migration Path

### Phase 1: Off-Chain Only
- Full PostgreSQL schema deployed
- All business logic in database functions
- No blockchain integration

### Phase 2: Testnet Integration
- Deploy HogwartsRegistry to Sepolia/Polygon Mumbai
- Deploy CourseForgeToken to testnet
- Integration tests with off-chain synchronization

### Phase 3: Mainnet Launch
- Deploy to Polygon mainnet (low gas costs)
- Enable real revenue routing
- CPA integration for fiat flows

---

## 8. API Endpoints (Future)

```
POST   /api/v1/students              # Create student
GET    /api/v1/students/:id          # Get student
PATCH  /api/v1/students/:id/wallet   # Link wallet

POST   /api/v1/spells                # Submit spell
GET    /api/v1/spells/:id            # Get spell
POST   /api/v1/spells/:id/verify     # Verify spell
POST   /api/v1/spells/:id/register   # Register on-chain

GET    /api/v1/cft/balance/:studentId    # Get CFT balance
POST   /api/v1/cft/stake             # Stake CFT
POST   /api/v1/cft/unstake           # Unstake CFT

GET    /api/v1/transcript/:studentId # Get transcript
```

---

## Appendix: Example Records

### Sample Spell Record (On-Chain)

```json
{
  "tokenId": 42,
  "owner": "0x742d35Cc6634C0532925a3b844Bc9e7595f8eabc",
  "contentHash": "0x7d4e3e...",
  "courseCode": "MAT-243",
  "assignmentCode": "Project One",
  "grade": "B+",
  "institution": "SNHU",
  "verifiedAt": 1701820800,
  "offChainId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Sample CFT Transaction (Off-Chain)

```json
{
  "transaction_id": "6fa459ea-ee8a-3ca4-894e-db77e160355e",
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "transaction_type": "mint",
  "amount": "120.000000000000000000",
  "reference_type": "spell",
  "reference_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "reason": "Earned CFT for verified spell: B+",
  "created_at": "2025-12-05T00:50:00Z"
}
```

---

*Document Version: 1.0.0*
*Last Updated: 2025-12-05*
*Author: Strategickhaos DAO LLC / Valoryield Engine*
