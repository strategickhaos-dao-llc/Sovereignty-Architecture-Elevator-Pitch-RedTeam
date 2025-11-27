# SwarmGate Contracts - Immutable 7% Charity Splitter

This directory contains the Hardhat v2.22 scaffold for the **Immutable Charity Splitter** contract - the core infrastructure that mathematically enforces the 7% charity tax for SwarmGate.

## Overview

The `ImmutableCharitySplitter` contract creates a "Legal-Engineering Moat" by:
- **Hardcoding** the 7% charity split as an immutable constant
- **Auto-splitting** all incoming ETH: 93% to operations, 7% locked for quarterly charity distribution
- **Transparently** tracking all funds via on-chain events

## Quick Start

### 1. Install Dependencies

```bash
cd swarmgate-contracts
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your PRIVATE_KEY for deployment
```

### 3. Compile Contracts

```bash
npm run compile
# or
npx hardhat compile
```

### 4. Run Tests

```bash
npm test
# or
npx hardhat test
```

### 5. Deploy to Base Sepolia Testnet

```bash
npm run deploy:base-sepolia
# or
npx hardhat run scripts/deploy.js --network baseSepolia
```

## Contract Architecture

```
swarmgate-contracts/
├── contracts/
│   └── ImmutableCharitySplitter.sol   # Main splitter contract
├── scripts/
│   └── deploy.js                       # Deployment script
├── test/
│   └── ImmutableCharitySplitter.test.js # Comprehensive test suite
├── hardhat.config.js                   # Network & compiler config
├── package.json                        # Dependencies
└── .env.example                        # Environment template
```

## Contract Details

### Constants (Immutable)

| Constant | Value | Description |
|----------|-------|-------------|
| `CHARITY_BPS` | 700 | 7% in basis points |
| `OPS_BPS` | 9300 | 93% in basis points |
| `BPS_DENOMINATOR` | 10000 | Basis point divisor |
| `DISTRIBUTION_INTERVAL` | 90 days | Quarterly charity payout |

### Key Functions

- **`receive()`** - Auto-splits incoming ETH: 93% to ops, 7% to charity pool
- **`distributeCharity()`** - Distributes accumulated 7% to charities (after 90 days)
- **`pendingCharityBalance()`** - View function showing funds awaiting distribution

### Events

- `PaymentReceived(address sender, uint256 amount, uint256 charityShare, uint256 opsShare)`
- `OpsForwarded(address recipient, uint256 amount)`
- `CharityDistributed(uint256 totalDistributed, uint256 timestamp)`

## Security Considerations

1. **Immutable Split Ratio**: The 7%/93% split is hardcoded as a constant
2. **Non-Upgradeable**: Contract cannot be modified after deployment
3. **Time-Locked Distribution**: Charity funds can only be distributed quarterly
4. **Anyone Can Trigger Distribution**: Keeper-friendly design allows any address to call `distributeCharity()`

## Test Coverage

The test suite validates:
- ✅ Exact 7%/93% split math at any scale
- ✅ Wei-level precision (no dust losses)
- ✅ Distribution timing enforcement
- ✅ Event emissions
- ✅ Edge cases (zero transfers, remainders)

## Networks

| Network | Chain ID | RPC URL |
|---------|----------|---------|
| Base Sepolia | 84532 | https://sepolia.base.org |
| Hardhat Local | 31337 | http://localhost:8545 |

## Deployment Configuration

Before deploying, update `scripts/deploy.js` with:
1. Your **Operational Multisig** address (receives 93%)
2. Your **Charity** addresses (receive quarterly 7% distributions)

## License

MIT
