# Deployment Instructions

## ⚠️ STATUS: PENDING DEPLOYMENT

**This document provides step-by-step instructions for deploying the Strategickhaos 7% Charity Splitter smart contract.**

---

## Prerequisites

Before deployment, ensure you have:

1. **Node.js 18+ LTS** installed
2. **A wallet with testnet ETH** (Base Sepolia)
3. **Basescan API key** (optional, for verification)

---

## Step 1: Install Node.js (5 minutes)

### Windows (PowerShell)
```powershell
# Download and install Node.js LTS from https://nodejs.org/
# Or use winget:
winget install OpenJS.NodeJS.LTS

# Verify installation
node --version
npm --version
```

### macOS
```bash
# Using Homebrew
brew install node@18

# Verify installation
node --version
npm --version
```

### Linux (Ubuntu/Debian)
```bash
# Using NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

---

## Step 2: Set Up Hardhat Project (10 minutes)

```bash
# Create project directory
mkdir charity-splitter
cd charity-splitter

# Initialize npm project
npm init -y

# Install Hardhat and dependencies
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npm install @openzeppelin/contracts dotenv

# Initialize Hardhat
npx hardhat init
# Select: "Create a JavaScript project"
```

---

## Step 3: Create Contract Files

### Create `contracts/CharitySplitter.sol`

Copy the Solidity code from `CHARITY_SPLITTER_CODE.md` into this file.

### Create `scripts/deploy.js`

Copy the deployment script from `CHARITY_SPLITTER_CODE.md` into this file.

### Update `hardhat.config.js`

Copy the Hardhat configuration from `CHARITY_SPLITTER_CODE.md` into this file.

---

## Step 4: Configure Environment

Create `.env` file:

```bash
# .env
PRIVATE_KEY=your_wallet_private_key_here
BASE_SEPOLIA_RPC=https://sepolia.base.org
BASESCAN_API_KEY=your_basescan_api_key
```

⚠️ **NEVER commit `.env` with real private keys!**

---

## Step 5: Get Testnet ETH

1. Go to [Base Sepolia Faucet](https://www.coinbase.com/faucets/base-ethereum-goerli-faucet)
2. Enter your wallet address
3. Request testnet ETH

---

## Step 6: Compile Contract (2 minutes)

```bash
npx hardhat compile
```

Expected output:
```
Compiled 1 Solidity file successfully
```

---

## Step 7: Deploy to Base Sepolia (5 minutes)

```bash
# Update deploy.js with your wallet addresses first!
npx hardhat run scripts/deploy.js --network baseSepolia
```

Expected output:
```
Deploying CharitySplitter...
Charity Wallet: 0x...
Operations Wallet: 0x...
CharitySplitter deployed to: 0x...
Split Config: 7% charity, 93% operations

✅ The 7% charitable split is now immutable on-chain!
```

---

## Step 8: Verify Contract (Optional, 5 minutes)

```bash
npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS> <CHARITY_WALLET> <OPS_WALLET>
```

---

## Step 9: Update Documentation

After successful deployment:

1. Update `SWARMGATE_STATUS.md` with:
   - Contract address
   - Deployment transaction hash
   - Change status from ❌ to ✅

2. Create deployment record:
```yaml
deployment:
  network: Base Sepolia
  contract_address: "0x..."
  tx_hash: "0x..."
  block_number: ...
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"
  status: DEPLOYED ✅
```

---

## Troubleshooting

### "Cannot find module 'hardhat'"
```bash
npm install --save-dev hardhat
```

### "Insufficient funds"
- Get more testnet ETH from faucet
- Check wallet balance: `npx hardhat balance --network baseSepolia`

### "Invalid private key"
- Ensure `.env` has correct private key
- Key should be 64 hex characters (no 0x prefix)

### "Network not configured"
- Check `hardhat.config.js` has correct network configuration
- Verify RPC URL is accessible

---

## Post-Deployment Checklist

- [ ] Contract deployed to Base Sepolia
- [ ] Contract verified on Basescan
- [ ] Test receive function with small amount
- [ ] Verify charity wallet received 7%
- [ ] Verify operations wallet received 93%
- [ ] Update `SWARMGATE_STATUS.md`
- [ ] Update `PROVENANCE.md` with deployment TX

---

## Mainnet Deployment (Future)

⚠️ **Before mainnet deployment:**

1. Complete full audit
2. Test extensively on testnet
3. Review gas optimization
4. Prepare multi-sig for ownership
5. Document upgrade path (if needed)

```bash
# ONLY AFTER THOROUGH TESTING
npx hardhat run scripts/deploy.js --network baseMainnet
```

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Install Node.js | 5 min |
| 2 | Set up Hardhat | 10 min |
| 3 | Create contract files | 5 min |
| 4 | Configure .env | 2 min |
| 5 | Get testnet ETH | 5 min |
| 6 | Compile | 2 min |
| 7 | Deploy | 5 min |
| 8 | Verify | 5 min |
| **Total** | | **~40 min** |

---

*"The code is ready. The deployment is just execution."*

💙🔥⚔️∞
