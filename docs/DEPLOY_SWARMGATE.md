# SwarmGate Deployment Guide

This guide covers deploying the SwarmGate Eternal 7% Engine to testnet and mainnet.

## Prerequisites

- Node.js 18+ and npm
- Hardhat installed (`npm install --save-dev hardhat`)
- Access to RPC endpoints (Alchemy, Infura, or self-hosted)
- Funded deployer wallet
- (Mainnet) HashiCorp Vault access for key management

## Environment Variables

```bash
# Required for all deployments
export DEPLOYER_PRIVATE_KEY="your-private-key"  # Or use Vault

# Recipient addresses (must be set before deployment)
export SWARMGATE_OPS_ADDRESS="0x..."      # Operations treasury
export SWARMGATE_DEV_ADDRESS="0x..."      # Development fund
export SWARMGATE_GOV_ADDRESS="0x..."      # Governance address
export SWARMGATE_RESERVE_ADDRESS="0x..."  # Reserves address
export SWARMGATE_ADMIN_ADDRESS="0x..."    # Emergency admin

# Split parameters (default: 7%)
export SWARMGATE_SPLIT_BPS="700"          # Basis points (700 = 7%)
```

## Testnet Deployment (Goerli)

### 1. Configure Environment

```bash
# Set testnet RPC
export TESTNET_RPC_URL="https://goerli.infura.io/v3/YOUR_PROJECT_ID"

# Or use Alchemy
export TESTNET_RPC_URL="https://eth-goerli.g.alchemy.com/v2/YOUR_API_KEY"

# Set recipient addresses (use test addresses for testnet)
export SWARMGATE_OPS_ADDRESS="0x..."
export SWARMGATE_DEV_ADDRESS="0x..."
export SWARMGATE_GOV_ADDRESS="0x..."
export SWARMGATE_RESERVE_ADDRESS="0x..."
export SWARMGATE_ADMIN_ADDRESS="0x..."
```

### 2. Deploy Contract

```bash
# Navigate to contracts directory
cd contracts/

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Deploy to Goerli testnet
npx hardhat run scripts/deploy.js --network goerli

# Verify on Etherscan
npx hardhat verify --network goerli DEPLOYED_ADDRESS \
  $SWARMGATE_OPS_ADDRESS \
  $SWARMGATE_DEV_ADDRESS \
  $SWARMGATE_GOV_ADDRESS \
  $SWARMGATE_RESERVE_ADDRESS \
  $SWARMGATE_ADMIN_ADDRESS
```

### 3. Verify Deployment

```bash
# Check contract status
npx hardhat verify-deployment --network goerli

# Test distribution function
npx hardhat run scripts/test-distribute.js --network goerli
```

## Mainnet Deployment (Ethereum)

> ⚠️ **WARNING**: Mainnet deployment requires additional approvals.
> See [SWARMGATE_CHANGE_POLICY.md](../governance/SWARMGATE_CHANGE_POLICY.md)

### 1. Pre-Deployment Checklist

- [ ] Contract audited by qualified security firm
- [ ] All recipient addresses verified and confirmed
- [ ] Emergency admin wallet secured (hardware wallet recommended)
- [ ] Vault access configured for key management
- [ ] Governance approval obtained for deployment
- [ ] Gas costs budgeted and funded

### 2. Configure Vault Access

```bash
# Authenticate with Vault
export VAULT_ADDR="https://vault.strategickhaos.internal"
vault login -method=oidc

# Retrieve deployer key from Vault
export VAULT_KEY_PATH="secret/swarmgate/mainnet"
DEPLOYER_PRIVATE_KEY=$(vault kv get -field=private_key $VAULT_KEY_PATH)
```

### 3. Set Mainnet Configuration

```bash
# Set mainnet RPC
export MAINNET_RPC_URL="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"

# Or use Alchemy (recommended for reliability)
export MAINNET_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY"

# Production recipient addresses
export SWARMGATE_OPS_ADDRESS="0x..."      # Verified operations multisig
export SWARMGATE_DEV_ADDRESS="0x..."      # Verified development fund
export SWARMGATE_GOV_ADDRESS="0x..."      # Verified governance address
export SWARMGATE_RESERVE_ADDRESS="0x..."  # Verified reserves address
export SWARMGATE_ADMIN_ADDRESS="0x..."    # Verified admin (hardware wallet)

# Gas configuration (check current gas prices)
export MAX_GAS_PRICE="100000000000"  # 100 gwei max
export GAS_LIMIT="500000"
```

### 4. Deploy to Mainnet

```bash
# Final verification
echo "Deploying with the following addresses:"
echo "  Operations: $SWARMGATE_OPS_ADDRESS"
echo "  Development: $SWARMGATE_DEV_ADDRESS"
echo "  Governance: $SWARMGATE_GOV_ADDRESS"
echo "  Reserves: $SWARMGATE_RESERVE_ADDRESS"
echo "  Admin: $SWARMGATE_ADMIN_ADDRESS"
read -p "Confirm deployment? (yes/no): " confirm
[ "$confirm" != "yes" ] && exit 1

# Deploy
npx hardhat run scripts/deploy.js --network mainnet

# Verify on Etherscan
npx hardhat verify --network mainnet DEPLOYED_ADDRESS \
  $SWARMGATE_OPS_ADDRESS \
  $SWARMGATE_DEV_ADDRESS \
  $SWARMGATE_GOV_ADDRESS \
  $SWARMGATE_RESERVE_ADDRESS \
  $SWARMGATE_ADMIN_ADDRESS
```

### 5. Post-Deployment

```bash
# Update status.yaml with deployment info
# Record: contract address, tx hash, block number

# Generate checksum
sha256sum contracts/SwarmGate.sol > swarmgate/checksums.txt

# Sign deployment record
gpg --sign --armor swarmgate/status.yaml
```

## CI/CD Deployment (GitHub Actions)

For automated deployments via CI/CD, trigger the workflow manually:

```bash
# Via GitHub CLI
gh workflow run contracts-deploy.yml \
  -f environment=testnet \
  -f confirm=true

# For mainnet (requires additional approval)
gh workflow run contracts-deploy.yml \
  -f environment=mainnet \
  -f confirm=true
```

## Troubleshooting

### Common Issues

**Transaction fails with "out of gas"**
- Increase `GAS_LIMIT` environment variable
- Check current network gas prices

**Recipient address validation fails**
- Ensure all addresses are valid checksummed Ethereum addresses
- Verify addresses are not zero address

**Vault authentication fails**
- Check Vault token validity
- Verify role permissions

### Emergency Procedures

If issues occur post-deployment:

1. **Pause distributions**: Call `pause()` from admin wallet
2. **Assess situation**: Review contract state and logs
3. **Contact team**: Use emergency contacts in config
4. **Document incident**: Create incident report

## Support

- **Documentation**: [README.md](../README.md)
- **Change Policy**: [SWARMGATE_CHANGE_POLICY.md](../governance/SWARMGATE_CHANGE_POLICY.md)
- **Discord**: #swarmgate-support
