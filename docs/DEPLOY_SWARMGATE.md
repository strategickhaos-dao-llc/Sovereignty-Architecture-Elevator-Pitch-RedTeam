# SwarmGate v1.0 Deployment Guide

This document describes how to deploy the **SwarmGate 7% Charity Engine** using Hardhat.

- Network example: **Base Sepolia** (testnet)
- Components: `CharitySplitter`, `MerkleDistributor`
- Inputs: charity addresses + amounts, ops wallet

---

## 1. Prerequisites

- Node.js 20+ installed
- `npm` available
- A funded deployer wallet on your target network
- `.env` file with:

```bash
PRIVATE_KEY=0xYOUR_PRIVATE_KEY
RPC_URL=https://sepolia.base.org
ETHERSCAN_API_KEY=YOUR_BASESCAN_API_KEY
```

Hardhat is already configured in `hardhat.config.js` to use `baseSepolia` with `PRIVATE_KEY`.

---

## 2. Install dependencies

From the repo root:

```bash
npm install
```

---

## 3. Configure beneficiaries (7% vault)

Edit `scripts/generate-merkle-root.js` and replace the placeholder addresses and amounts:

```javascript
const charities = [
  { name: "St. Jude",   address: "0xREAL_ST_JUDE_ADDR",   amount: hre.ethers.parseEther("X.Y") },
  { name: "MSF",        address: "0xREAL_MSF_ADDR",       amount: hre.ethers.parseEther("A.B") },
  { name: "Veterans",   address: "0xREAL_VETERANS_ADDR",  amount: hre.ethers.parseEther("C.D") }
];
```

> The sum of these amounts should equal the 7% allocation you intend to distribute in this drop.

---

## 4. Generate the Merkle root and proofs

Run:

```bash
npm run generate-root
```

This will:

- Compute the Merkle tree over `(index, address, amount)`.
- Print the Merkle root to the console.
- Write `merkle-data.json` containing:
  - `root`
  - `proofs[]` for each charity `(index, address, amount, proof)`

Keep `merkle-data.json` – you will use it for verification and to share proofs with beneficiaries.

---

## 5. Deploy to Base Sepolia (testnet)

With `merkle-data.json` present:

```bash
npm run deploy:base-sepolia
```

The script will:

- Read `root` from `merkle-data.json`
- Deploy `MerkleDistributor` with that root
- Deploy `CharitySplitter` pointing at:
  - your ops wallet (93% recipient)
  - the distributor (7% vault)

Output includes:

- `MerkleDistributor` address
- `CharitySplitter` address
- Basescan URL for the splitter

Record these in:

- `SWARMGATE_v1.0_STATUS.yaml` under `current_state.on_chain`
- `PROVENANCE.md` as part of the deployment log

---

## 6. Mainnet deployment (with Vault-managed keys)

For mainnet, do not store the `PRIVATE_KEY` directly in `.env`.

Instead:

- Configure your Hardhat network to use a signer loaded from Vault or HSM.
- Point `RPC_URL` at the mainnet endpoint.
- Repeat steps:

```bash
npm run generate-root            # or reuse an already verified root
npm run deploy:base-sepolia      # replace with your mainnet network script
```

> **Recommendation**: treat mainnet deployments as version bumps:
> `swarmgate/v1.0-mainnet-1`, `swarmgate/v1.0-mainnet-2`, etc.

---

## 7. Environment variables and parameters

Typical environment variables:

```bash
# Hardhat / network
PRIVATE_KEY=0x...
RPC_URL=https://sepolia.base.org
ETHERSCAN_API_KEY=...

# Strategickhaos / SwarmGate
SWARMGATE_SPLIT_PERCENT_OPS=93
SWARMGATE_SPLIT_PERCENT_CHARITY=7
SWARMGATE_STATUS_FILE=SWARMGATE_v1.0_STATUS.yaml
```

Contract-level split ratios are encoded in code for v1.0.
These env vars are for dashboards / monitoring and future versions, not for silently changing the split.

---

## 8. Verifying the deployment

1. Check the `FundsSplit` events on the `CharitySplitter` contract.

2. Confirm that sending 1 ETH yields:
   - 0.93 ETH to ops wallet
   - 0.07 ETH to distributor

3. Use `merkle-data.json` + `MerkleDistributor` to:
   - Construct a claim transaction for one charity.
   - Verify `Claimed` event emits with the expected `index/address/amount`.

When all three checks pass, SwarmGate v1.0 is operational on that network.
