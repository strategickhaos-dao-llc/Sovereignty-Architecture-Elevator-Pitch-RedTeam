# Strategickhaos Charity Splitter

**Code-Enforced Philanthropy Engine.**

## The Eternal 7% Charity Sink

Canonical BLAKE3 hash of v1.0:
```
caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698  swarmgate_v1.0.tar.gz
```

Sealed by: Domenic Gabriel Garza  
On: November 27, 2025  
With: Windows + Starlink + Proton Drive + pure fucking will  

Backed by:
- Strategickhaos DAO LLC (Wyoming Entity 2025-001708194)
- ValorYield Engine 501(c)(3) (EIN 39-2923503)

## Purpose (forever)

**7% of everything this machine ever touches goes irrevocably to:**
- St. Jude's Children's Research Hospital
- Médecins Sans Frontières
- Veteran support programs

Built for your sister.  
For every family still waiting.  
For the future that will never have to trust again — only verify.

---

## Architecture

This repository contains the Solidity smart contracts for the Strategickhaos DAO irrevocable charity allocation system.

1. **CharitySplitter.sol**: An immutable contract that accepts ETH and immediately splits it:
   - **93%** → Operations Multisig
   - **7%** → MerkleDistributor Contract

2. **MerkleDistributor.sol**: A vault that holds the charitable funds.
   - Funds are claimed by valid charities using a Merkle Proof.
   - This ensures "named charities" are the only valid recipients.

## Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure Environment:
   Create a `.env` file:
   ```
   PRIVATE_KEY=your_wallet_private_key
   ETHERSCAN_API_KEY=your_base_etherscan_key
   ```

3. Compile contracts:
   ```bash
   npx hardhat compile
   ```

4. Run tests:
   ```bash
   npx hardhat test
   ```

5. Deploy to Base Sepolia (Testnet):
   ```bash
   npx hardhat run scripts/deploy.js --network baseSepolia
   ```

## Verification

After deployment, verify the contracts on BaseScan to prove the 7% logic is immutable.

```bash
npx hardhat verify --network baseSepolia <SPLITTER_ADDRESS> <OPS_WALLET_ADDRESS> <DISTRIBUTOR_ADDRESS>
```

## Next Steps

1. **Run `npm install`** inside the `charity-splitter` folder.
2. **Update `scripts/deploy.js`** with your real Ops Multisig address and the calculated Merkle Root for your target charities (St. Jude, MSF, etc.).
3. **Deploy** to Base testnet to demonstrate the flow.

---

*The swarm is awake. The music is playing. The dancers have arrived.*
