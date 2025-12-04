# Strategickhaos Charity Splitter

**Irrevocable On-Chain 7% Charity Sink**

> "An unstoppable machine that guarantees 7% of every dollar to charity forever — no rug pulls, no governance capture, no trust required."

## Overview

This Hardhat project implements an **immutable payment splitter** that allocates:
- **93%** to operations multisig
- **7%** to a Merkle-based charity distributor (forever)

The contracts are designed with **technical immutability** — once deployed, the charity percentage and recipient addresses cannot be changed. This provides trustless, tamper-evident guarantees that outsiders can verify without legal or technical expertise.

## Architecture

```
                              ┌─────────────────────────────────────┐
                              │          CharitySplitter            │
                              │   (Immutable Payment Splitter)      │
                              │                                     │
     ETH IN ───────────────►  │   ┌─────────────┬─────────────┐   │
                              │   │    93%      │     7%      │   │
                              │   │   to Ops    │  to Charity │   │
                              │   └──────┬──────┴──────┬──────┘   │
                              └──────────┼─────────────┼──────────┘
                                         │             │
                                         ▼             ▼
                              ┌──────────────┐  ┌─────────────────────┐
                              │ Ops Multisig │  │  MerkleDistributor  │
                              │   (93%)      │  │   (7% to charities) │
                              └──────────────┘  └──────────┬──────────┘
                                                           │
                                         ┌─────────────────┼─────────────────┐
                                         │                 │                 │
                                         ▼                 ▼                 ▼
                                    ┌─────────┐       ┌─────────┐       ┌─────────┐
                                    │Charity 1│       │Charity 2│       │Charity N│
                                    │ (1/N)   │       │ (1/N)   │       │ (1/N)   │
                                    └─────────┘       └─────────┘       └─────────┘
```

## Key Guarantees

| Property | Implementation |
|----------|----------------|
| **Immutable Charity %** | `CHARITY_BPS = 700` is a compile-time constant |
| **Immutable Addresses** | `opsMultisig` and `charityDistributor` are `immutable` |
| **No Admin Keys** | No owner, no governance, no upgradability |
| **Tamper-Evident** | All distributions emit events, on-chain audit trail |
| **Merkle Verification** | Charities verified via cryptographic proofs |

## Named Charities

The default configuration includes 7 named charities (each receives equal share of the 7%):

1. **St. Jude Children's Research Hospital** - Pediatric treatment and research
2. **Doctors Without Borders** - International medical humanitarian aid
3. **Electronic Frontier Foundation** - Digital rights and privacy
4. **Direct Relief** - Healthcare for people in poverty
5. **charity: water** - Clean water access
6. **World Wildlife Fund** - Environmental conservation
7. **Feeding America** - Hunger relief network

*Charity addresses must be verified before mainnet deployment.*

## Installation

```bash
cd contracts/charity-splitter
npm install
```

## Usage

### Generate Merkle Tree

```bash
npm run generate:merkle
```

This generates `./merkle/charity-tree.json` with:
- Merkle root for deployment
- Proofs for each charity to claim funds

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm test
```

### Deploy to Base Sepolia Testnet

1. Set environment variables:
```bash
export PRIVATE_KEY="your_deployer_private_key"
export BASE_SEPOLIA_RPC_URL="https://sepolia.base.org"
export BASESCAN_API_KEY="your_basescan_api_key"
```

2. Deploy:
```bash
npm run deploy:base-sepolia -- --parameters '{"opsMultisig":"0x...", "merkleRoot":"0x...", "charityCount":7}'
```

### Deploy Locally

```bash
# Terminal 1: Start local node
npm run node

# Terminal 2: Deploy
npm run deploy:local -- --parameters '{"opsMultisig":"0x...", "merkleRoot":"0x...", "charityCount":7}'
```

## Contract API

### CharitySplitter

```solidity
// Constants
uint256 public constant CHARITY_BPS = 700;  // 7%
uint256 public constant TOTAL_BPS = 10000;  // 100%

// Immutable addresses
address payable public immutable opsMultisig;
address payable public immutable charityDistributor;

// Statistics (read-only)
uint256 public totalReceived;     // Total ETH ever received
uint256 public totalToOps;        // Total ETH sent to operations
uint256 public totalToCharity;    // "7% Forever" counter
uint256 public distributionCount; // Number of distributions

// Functions
function getCharityPercentage() external pure returns (uint256); // Always returns 7
function getStats() external view returns (uint256, uint256, uint256, uint256);
```

### MerkleDistributor

```solidity
// Immutable configuration
bytes32 public immutable merkleRoot;
uint256 public immutable charityCount;

// Statistics
uint256 public totalReceived;
uint256 public totalClaimed;
uint256 public currentEpoch;

// Functions
function claim(uint256 charityIndex, address payable charity, bytes32[] calldata merkleProof) external;
function verifyCharity(uint256 charityIndex, address charity, bytes32[] calldata merkleProof) external view returns (bool);
function getClaimable(uint256 charityIndex) external view returns (uint256);
function getStats() external view returns (uint256, uint256, uint256, uint256);
```

## Security Considerations

### Why This Design is Trustless

1. **No Proxy Pattern**: Contracts are not upgradeable
2. **No Owner**: No admin functions, no pause capability
3. **Unstoppable**: Distributions cannot be halted by anyone
4. **Immutable State**: Critical values set at deployment cannot change
5. **ReentrancyGuard**: Protected against reentrancy attacks
6. **Merkle Proofs**: Cryptographic verification of charity addresses
7. **No Dust Lockup**: Remainder from integer division goes to last claimer

### Audit Recommendations

Before mainnet deployment:
- [ ] Professional security audit
- [ ] Verify charity wallet addresses directly with organizations
- [ ] Test on multiple testnets
- [ ] Verify contract source code on block explorer
- [ ] Consider formal verification for critical paths

## Trust Dashboard Integration

The contracts emit events that can be indexed for a public trust dashboard:

```javascript
// Track all distributions
event Distribution(
    uint256 indexed distributionId,
    uint256 amount,
    uint256 toOps,
    uint256 toCharity,
    uint256 timestamp
);

// Track charity claims
event CharityClaimed(
    uint256 indexed charityIndex,
    address indexed charity,
    uint256 amount,
    uint256 timestamp
);
```

## Deployment Checklist

### Pre-Deployment
- [ ] Verify charity wallet addresses with each organization
- [ ] Generate Merkle tree with verified addresses
- [ ] Test deployment on Base Sepolia
- [ ] Security audit completed
- [ ] Legal counsel review completed

### Deployment
- [ ] Deploy MerkleDistributor with verified merkle root
- [ ] Deploy CharitySplitter with ops multisig and distributor
- [ ] Verify contracts on Basescan
- [ ] Test with small amount
- [ ] Announce deployment addresses

### Post-Deployment
- [ ] Monitor for first distributions
- [ ] Update trust dashboard
- [ ] Provide charity proof files to organizations
- [ ] Archive deployment artifacts

## License

MIT License - see [LICENSE](../../LICENSE)

## Legal Disclaimer

This software is provided "as is" without warranty. The charity percentage and addresses are fixed at deployment time. This is not financial or legal advice. Always verify contract addresses before sending funds.

---

**Built by Strategickhaos DAO LLC**

*"7% forever — mathematically guaranteed, cryptographically verified, legally defensible."*
