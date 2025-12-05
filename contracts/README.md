# Strategickhaos DAO - Irrevocable 7% Charity Splitter

> **"An unstoppable, Wyoming-registered, 501(c)(3)-blessed machine that turns every dollar it touches into 7% guaranteed, eternal charity — no rug pulls, no governance capture, no trust required."**

## Overview

This smart contract system implements an **irrevocable charity sink** that guarantees 7% of all treasury inflows are permanently allocated to pre-named charities. Once deployed, this allocation **cannot be changed, stopped, or rerouted by anyone** — not the DAO, not governance, not even the original deployer.

### Key Properties

| Property | Description |
|----------|-------------|
| **Irrevocable** | No admin functions, no upgrades, no governance override |
| **Append-Only** | Charity recipients can only be added, never removed |
| **Transparent** | All allocations visible and verifiable on-chain |
| **Trustless** | No approval or signature required for distribution |
| **Permissionless** | Anyone can trigger distributions |

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │      All Treasury Inflows           │
                    │    (ETH, USDC, other ERC-20)        │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   IrrevocableCharitySplitter.sol    │
                    │                                     │
                    │   ┌──────────────────────────────┐  │
                    │   │  CHARITY_BPS = 700 (7%)      │  │
                    │   │  OPERATIONS_BPS = 9300 (93%) │  │
                    │   │  (CONSTANTS - IMMUTABLE)     │  │
                    │   └──────────────────────────────┘  │
                    └────────────┬────────────┬───────────┘
                                 │            │
                    ┌────────────┴┐          ┌┴────────────┐
                    │   7%        │          │   93%       │
                    ▼             │          │             ▼
     ┌──────────────────────────┐│          │┌──────────────────────────┐
     │ MerkleCharityDistributor ││          ││ Operations Multisig      │
     │                          ││          ││                          │
     │ • Quarterly distributions││          ││ • DAO treasury           │
     │ • Pro-rata to charities  ││          ││ • Development funding    │
     │ • Merkle proof claims    ││          ││ • Operating expenses     │
     └────────────┬─────────────┘│          │└──────────────────────────┘
                  │              │          │
                  ▼              │          │
     ┌──────────────────────────────────┐   │
     │       Named Charities            │   │
     │                                  │   │
     │  • Against Malaria Foundation    │   │
     │  • Helen Keller International    │   │
     │  • Malaria Consortium            │   │
     │  • New Incentives                │   │
     │  (GiveWell Top Charities)        │   │
     └──────────────────────────────────┘   │
```

## Contracts

### IrrevocableCharitySplitter.sol

The main splitter contract that enforces the 93/7 split.

**Immutable Properties:**
- `CHARITY_BPS = 700` (7% to charity - constant, cannot be changed)
- `OPERATIONS_BPS = 9300` (93% to operations - constant, cannot be changed)
- `operationsMultisig` - Set at deployment, immutable
- `charityTreasury` - Set at deployment, immutable

**Key Functions:**
- `receive()` - Automatically splits incoming ETH
- `splitToken(address)` - Split ERC-20 tokens
- `getEthStats()` - View all-time ETH statistics
- `verifyCharityPercentage()` - Verify 7% is still locked

### MerkleCharityDistributor.sol

The charity treasury that receives the 7% and distributes to named charities.

**Features:**
- Quarterly distribution epochs (90-day intervals)
- Merkle tree for efficient pro-rata distribution
- Append-only charity registry
- Full on-chain audit trail

**Key Functions:**
- `registerCharity()` - Add a new charity (append-only)
- `createEpoch()` - Start a new distribution period
- `claim()` - Charities claim their allocation with Merkle proof
- `getTreasuryBalance()` - View available funds

## Deployment

### Prerequisites

```bash
cd contracts
npm install
```

### Environment Variables

Create a `.env` file:

```bash
# Required for mainnet/testnet deployment
PRIVATE_KEY=your_deployer_private_key
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
BASE_RPC_URL=https://mainnet.base.org
BASESCAN_API_KEY=your_basescan_api_key

# Contract configuration
OPERATIONS_MULTISIG=0x... # Your operations multisig address
ROOT_UPDATER=0x...        # Address that can update Merkle roots
```

### Deploy to Base Sepolia (Testnet)

```bash
npm run deploy:base-sepolia
```

### Deploy to Base Mainnet

```bash
npm run deploy:base
```

### Verify Contracts

```bash
npm run verify -- --network baseSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

## Testing

```bash
# Run all tests
npm test

# Run with gas reporting
REPORT_GAS=true npm test

# Run coverage
npm run coverage
```

## Default Charities (GiveWell Top Recommendations)

| Charity | EIN | Allocation |
|---------|-----|------------|
| Against Malaria Foundation | 20-8521450 | 25% |
| Helen Keller International | 13-5562162 | 25% |
| Malaria Consortium | 98-0627052 | 25% |
| New Incentives | 45-3321264 | 25% |

*These are GiveWell's top-rated charities based on cost-effectiveness analysis.*

## Security Model

### Why This Is Trustless

1. **No Admin Keys**: The CharitySplitter has no owner, no admin, no pause function
2. **Constants, Not Variables**: `CHARITY_BPS` is a `constant`, not a storage variable
3. **Immutable Addresses**: `operationsMultisig` and `charityTreasury` are `immutable`
4. **No Upgrade Pattern**: Contract is not upgradeable - what you see is what you get
5. **Permissionless Execution**: Anyone can call `splitEthBalance()` or `splitToken()`

### What Could Go Wrong

| Risk | Mitigation |
|------|------------|
| Charity address compromised | Multiple charities with Merkle distribution |
| Operations multisig compromised | Only affects 93%, charity 7% still flows |
| Contract bugs | Comprehensive testing, audits recommended |
| Chain shutdown | Deploy on multiple chains |

## Integration with 501(c)(3)

This on-chain system is designed to integrate with a Wyoming-registered 501(c)(3) charitable organization:

1. Deploy the CharitySplitter with the 501(c)(3)'s wallet as `charityTreasury`
2. The on-chain 7% flows directly to the tax-exempt entity's wallet
3. The 501(c)(3) distributes to named charities quarterly
4. IRS receipts are hashed and published on-chain for verification

This creates a **legal-engineering moat**: any future rogue governance literally cannot stop the charity allocation without breaking IRS rules (and triggering tax fraud).

## Gas Costs (Estimated)

| Operation | Gas (approx) | Cost @ 0.001 gwei |
|-----------|--------------|-------------------|
| Deploy Splitter | 850,000 | ~$0.25 |
| Deploy Distributor | 1,200,000 | ~$0.35 |
| Receive ETH + Split | 75,000 | ~$0.02 |
| Split ERC-20 | 85,000 | ~$0.03 |
| Register Charity | 60,000 | ~$0.02 |
| Claim Distribution | 50,000 | ~$0.015 |

*Base chain has extremely low gas costs, making this economically viable.*

## License

MIT License - See [LICENSE](../LICENSE)

## Support

- **Discord**: [discord.gg/strategickhaos](https://discord.gg/strategickhaos)
- **GitHub Issues**: [Report bugs](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Making charitable giving trustless, transparent, and irrevocable.*
