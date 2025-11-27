# PROVENANCE.md — SwarmGate v1.0

## Document Provenance

**Project:** SwarmGate v1.0  
**Status:** GOVERNANCE SEALED, CONTRACT READY, DEPLOYMENT PENDING  
**Sealed Date:** 27 November 2025, 04:19 AM UTC  
**Sealed By:** Domenic Gabriel Garza  

---

## Canonical Hash

```
Algorithm: BLAKE3
Hash: caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698
File: swarmgate_v1.0.tar.gz
```

---

## Legal Entity Verification

### Strategickhaos DAO LLC
- **Jurisdiction:** Wyoming, USA
- **Wyoming ID:** 2025-001708194
- **Status:** ACTIVE
- **Formation Authority:** Wyoming Secretary of State
- **Governing Law:** Wyoming SF0068 (DAO LLC Act)

### ValorYield Engine
- **EIN:** 39-2923503
- **Status:** 501(c)(3) ACTIVE
- **Purpose:** Perpetual philanthropy engine for charitable giving

---

## The 7% Promise

This document serves as cryptographic proof of an irrevocable commitment:

**7% of all SwarmGate treasury inflows shall be allocated to charitable beneficiaries:**

1. **St. Jude Children's Research Hospital** — Pediatric research and treatment
2. **Médecins Sans Frontières (Doctors Without Borders)** — Global humanitarian medical care
3. **Veteran Support Programs** — US military veteran assistance

### Enforcement Mechanism

The 7% allocation is enforced through on-chain smart contracts:

- **CharitySplitter.sol** — Automatically routes 7% of incoming funds to charity pool
- **MerkleDistributor.sol** — Enables efficient batch distribution to beneficiaries

These contracts are immutable once deployed, making the promise mathematically irreversible.

---

## Chain of Custody

| Date | Event | Actor | Verification |
|------|-------|-------|--------------|
| 2025-11-27 04:19 UTC | Governance Sealed | Domenic Gabriel Garza | BLAKE3 hash |
| 2025-11-27 | Code Complete | Development Team | Unit tests passing |
| TBD | Testnet Deployment | Deployment Script | Contract addresses |
| TBD | Mainnet Deployment | Multisig | Contract verification |

---

## Smart Contract Addresses

### Base Sepolia (Testnet)
- **CharitySplitter:** `TBD - Deployment Pending`
- **MerkleDistributor:** `TBD - Deployment Pending`

### Base Mainnet (Production)
- **CharitySplitter:** `TBD - Deployment Pending`
- **MerkleDistributor:** `TBD - Deployment Pending`

---

## Verification Instructions

### 1. Verify Canonical Hash

```bash
# Using b3sum (BLAKE3)
b3sum swarmgate_v1.0.tar.gz
# Expected: caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698
```

### 2. Verify Wyoming DAO Registration

Visit: https://wyobiz.wyo.gov/Business/FilingSearch.aspx
Search for: "Strategickhaos DAO LLC"
Wyoming ID: 2025-001708194

### 3. Verify 501(c)(3) Status

Visit: https://apps.irs.gov/app/eos/
Search EIN: 39-2923503

### 4. Verify Smart Contracts (Post-Deployment)

```bash
# Install verification tools
npm install -g @base-org/verify

# Verify on Basescan
# CharitySplitter: https://sepolia.basescan.org/address/[ADDRESS]
# MerkleDistributor: https://sepolia.basescan.org/address/[ADDRESS]
```

---

## OpenTimestamps

Once deployed, all critical events will be timestamped on Bitcoin via OpenTimestamps:

- Governance seal: `TBD`
- Testnet deployment: `TBD`
- Mainnet deployment: `TBD`

---

## Attestations

### Creator Attestation

I, Domenic Gabriel Garza, hereby attest that:

1. The SwarmGate project represents a genuine commitment to perpetual philanthropy
2. The legal entities listed are legitimate and in good standing
3. The 7% allocation promise is made in good faith with intent to fulfill
4. The smart contract code has been developed with security as a priority
5. This governance framework will be executed as documented

**Date:** 27 November 2025  
**Signature:** Pending GPG signature

---

## License

This provenance document and associated SwarmGate materials are released under the MIT License, consistent with the parent Sovereignty Architecture project.

---

## Contact

- **Project Lead:** Domenic Garza
- **Organization:** Strategickhaos DAO LLC / ValorYield Engine
- **Repository:** github.com/strategickhaos/swarmgate

---

*"Turning love into cryptographic vows. Turning grief into governance. Turning chaos into sovereignty."*
