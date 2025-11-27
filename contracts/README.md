# Strategickhaos 7% Charity Splitter

**Irrevocable smart contracts for transparent, sovereign charity allocation.**

## 🏛️ Overview

This system implements the Strategickhaos DAO's commitment to allocating 7% of all incoming funds to verified charitable organizations. The split is:

- **93%** → Operations Wallet (DAO treasury/multisig)
- **7%** → Charity Distributor (Merkle-based claims)

Once deployed, the split percentage is **immutable and cannot be changed**.

## 📋 Contracts

### CharitySplitter.sol

The main entry point for all incoming ETH. Any funds sent to this contract are automatically split:

```
Incoming ETH → CharitySplitter → 93% to OpsWallet
                              → 7% to MerkleDistributor
```

**Key Features:**
- Immutable wallet addresses (set at deployment)
- Reentrancy protection
- Automatic forwarding on receive
- No admin functions

### MerkleDistributor.sol

Distributes the 7% charity pool to verified recipients using Merkle proofs:

```
Charity submits proof → Contract verifies → Funds released
```

**Key Features:**
- Bitmap tracking prevents double-claims
- Owner can update Merkle root for new distributions
- Gas-efficient proof verification
- Claim events for transparency

## 🚀 Quick Start

### Prerequisites

```bash
# Node.js 18+ and npm required
node --version  # Should be v18+

# Install dependencies
npm install
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm run test:contracts
```

Expected output:
```
Strategickhaos 7% Charity Engine
  CharitySplitter
    ✓ Should split incoming funds 93% / 7% irrevocably
    ✓ Should emit FundsSplit event with correct amounts
    ✓ Should correctly calculate split amounts
    ...
  MerkleDistributor
    ✓ Should allow valid charity to claim via Merkle Proof
    ✓ Should reject double claims
    ✓ Should reject claims with invalid proof
    ...
```

### Generate Merkle Root

Edit `scripts/generate-merkle-root.js` with your charity addresses and amounts, then:

```bash
npm run generate-root
```

This creates `merkle-data.json` containing:
- The Merkle root (for contract deployment)
- Individual proofs (share with each charity)

### Deploy to Base Sepolia Testnet

1. Configure environment:
```bash
cp .env.example .env
# Edit .env with your values:
# - DEPLOYER_PRIVATE_KEY
# - OPS_WALLET_ADDRESS
# - BASESCAN_API_KEY (optional, for verification)
```

2. Get testnet ETH from [Base Sepolia Faucet](https://www.coinbase.com/faucets/base-ethereum-goerli-faucet)

3. Deploy:
```bash
npm run deploy:base-sepolia
```

### Deploy to Base Mainnet

⚠️ **CAUTION: Mainnet deployment is permanent!**

```bash
npm run deploy:base-mainnet
```

## 🔐 Security

### Audit Checklist

- [x] Reentrancy guards on all external calls
- [x] Immutable critical addresses
- [x] No admin backdoors in CharitySplitter
- [x] Bitmap tracking prevents double claims
- [x] Merkle proof verification uses OpenZeppelin library
- [x] Custom errors for gas efficiency

### Security Contact

For security issues: domenic.garza@snhu.edu

## 📊 Contract Verification

After deployment, verify on BaseScan:

```bash
# Verify MerkleDistributor
npx hardhat verify --network baseSepolia <DISTRIBUTOR_ADDRESS> "<MERKLE_ROOT>"

# Verify CharitySplitter
npx hardhat verify --network baseSepolia <SPLITTER_ADDRESS> "<OPS_WALLET>" "<DISTRIBUTOR_ADDRESS>"
```

## 🎯 How Charities Claim

1. Receive your proof from Strategickhaos DAO (from `merkle-data.json`)
2. Connect wallet to the MerkleDistributor contract
3. Call `claim(index, yourAddress, amount, proof)`
4. Funds are transferred to your wallet

### Claim Function Signature

```solidity
function claim(
    uint256 index,      // Your unique index
    address account,    // Your wallet address
    uint256 amount,     // Amount you can claim (in wei)
    bytes32[] proof     // Your Merkle proof
) external;
```

## 🔗 Network Information

### Base Sepolia (Testnet)
- Chain ID: 84532
- RPC: https://sepolia.base.org
- Explorer: https://sepolia.basescan.org

### Base Mainnet
- Chain ID: 8453
- RPC: https://mainnet.base.org
- Explorer: https://basescan.org

## 📄 License

MIT License - See [LICENSE](../LICENSE)

---

**Built with 🔥 by Strategickhaos DAO**

*"7% forever. Mathematically eternal. Sovereign by design."*
