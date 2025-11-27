# SwarmGate v1.0 - Perpetual Philanthropy Engine

**Status:** GOVERNANCE SEALED, CONTRACT READY, DEPLOYMENT PENDING  
**Sealed Date:** 27 November 2025, 04:19 AM UTC  
**Sealed By:** Domenic Gabriel Garza

## 🌟 Overview

SwarmGate is the first AI-governed perpetual philanthropy engine, designed to make charitable giving mathematically irreversible through on-chain smart contracts.

### The 7% Promise

**7% of all SwarmGate treasury inflows are irrevocably allocated to charity:**

- 🏥 **St. Jude Children's Research Hospital** - Pediatric research and treatment
- 🌍 **Médecins Sans Frontières** - Global humanitarian medical care
- 🎖️ **Veteran Support Programs** - US military veteran assistance

This allocation is enforced by immutable smart contracts - once deployed, it cannot be changed.

## 📋 Smart Contracts

### CharitySplitter.sol

Automatically splits incoming ETH:
- **7%** → Charity Pool
- **93%** → Treasury

Features:
- Immutable 7% allocation ratio (700 basis points)
- Reentrancy protection
- Event emission for transparency
- Statistics tracking

### MerkleDistributor.sol

Enables efficient batch distribution to beneficiaries:
- Merkle proof verification for claims
- Multi-round distribution support
- Gas-efficient bulk payments
- Full audit trail

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn
- Base network wallet with ETH for gas

### Installation

```bash
cd swarmgate
npm install
```

### Configuration

Create a `.env` file:

```env
# Required for deployment
PRIVATE_KEY=your_private_key_here

# RPC URLs (defaults provided for Base)
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
BASE_MAINNET_RPC_URL=https://mainnet.base.org

# For contract verification
BASESCAN_API_KEY=your_basescan_api_key

# Contract configuration
CHARITY_POOL_ADDRESS=0x...
TREASURY_ADDRESS=0x...
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm run test
```

### Deploy to Base Sepolia (Testnet)

```bash
npm run deploy:sepolia
```

### Deploy to Base Mainnet

```bash
npm run deploy:mainnet
```

### Verify on Basescan

```bash
npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

## 📊 Contract Addresses

### Base Sepolia (Testnet)
| Contract | Address |
|----------|---------|
| CharitySplitter | `TBD - Deployment Pending` |
| MerkleDistributor | `TBD - Deployment Pending` |

### Base Mainnet (Production)
| Contract | Address |
|----------|---------|
| CharitySplitter | `TBD - Deployment Pending` |
| MerkleDistributor | `TBD - Deployment Pending` |

## 🔒 Security

### Audits
- Internal security review: ✅ Complete
- External audit: Pending

### Security Features
- OpenZeppelin contracts (battle-tested)
- Reentrancy guards on all external calls
- Owner-only administrative functions
- Zero address validation
- Event emission for full transparency

### Bug Bounty
Contact: security@strategickhaos.com

## 📈 How It Works

```
                    ┌──────────────────┐
                    │   Incoming ETH   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  CharitySplitter │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌──────────────────┐         ┌──────────────────┐
    │   7% → Charity   │         │  93% → Treasury  │
    │      Pool        │         │                  │
    └────────┬─────────┘         └──────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ MerkleDistributor│
    └────────┬─────────┘
             │
    ┌────────┴────────┬────────────────┐
    ▼                 ▼                ▼
┌────────┐      ┌──────────┐     ┌──────────┐
│St Jude │      │   MSF    │     │ Veterans │
└────────┘      └──────────┘     └──────────┘
```

## 🏛️ Legal Entities

### Strategickhaos DAO LLC
- **Jurisdiction:** Wyoming, USA
- **Wyoming ID:** 2025-001708194
- **Status:** ACTIVE
- **Governing Law:** Wyoming SF0068 (DAO LLC Act)

### ValorYield Engine
- **EIN:** 39-2923503
- **Status:** 501(c)(3) ACTIVE
- **Purpose:** Perpetual philanthropy engine

## 📜 License

MIT License - See [LICENSE](../LICENSE)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Contact

- **Project Lead:** Domenic Garza
- **Organization:** Strategickhaos DAO LLC / ValorYield Engine
- **Repository:** github.com/strategickhaos/swarmgate

---

*"Turning love into cryptographic vows. Turning grief into governance. Turning chaos into sovereignty."*

**The swarm is with you. Forever.**
