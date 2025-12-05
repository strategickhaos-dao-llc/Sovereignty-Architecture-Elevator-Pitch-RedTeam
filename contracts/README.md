# Contracts Directory

This directory contains the SwarmGate smart contracts for the Eternal 7% Engine.

## Structure

```
contracts/
├── SwarmGate.sol       # Main revenue split contract
├── interfaces/         # Contract interfaces
├── scripts/            # Deployment scripts
└── test/              # Contract tests
```

## Overview

SwarmGate implements an immutable 7% revenue allocation mechanism:

- **Total Split**: 7% of incoming revenue
- **Distribution**:
  - 40% → Operations (2.8% of total)
  - 30% → Development (2.1% of total)
  - 20% → Governance (1.4% of total)
  - 10% → Reserves (0.7% of total)

## Building

```bash
# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test
```

## Deployment

See [docs/DEPLOY_SWARMGATE.md](../docs/DEPLOY_SWARMGATE.md) for deployment instructions.

## Security

All contracts must be audited before mainnet deployment. See [governance/SWARMGATE_CHANGE_POLICY.md](../governance/SWARMGATE_CHANGE_POLICY.md) for change management procedures.
