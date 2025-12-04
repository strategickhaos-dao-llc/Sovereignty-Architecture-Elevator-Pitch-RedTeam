# Wyoming DAO Public Identifier Requirement

## Overview

Wyoming Statute (as amended by SF0068) requires all DAOs formed in Wyoming to provide a **DAO Public Identifier** within 30 days of formation. Failure to provide this identifier results in administrative dissolution.

## What is a DAO Public Identifier?

Per Wyoming Secretary of State requirements, a DAO Public Identifier is:

> **A unique identifier that links to the DAO's smart contract or blockchain-based governance system.**

### Acceptable Forms of DAO Public Identifier:

1. **Smart Contract Address** (Primary/Preferred)
   - Ethereum mainnet contract address (e.g., `0x1234...abcd`)
   - Any EVM-compatible chain contract address
   - Solana program address
   - Other blockchain smart contract identifiers

2. **Decentralized Identifier (DID)**
   - W3C-compliant DID (e.g., `did:web:strategickhaos.com`)
   - Ethereum-based DIDs (e.g., `did:ethr:0x1234...`)

3. **IPFS/Arweave Hash** (Secondary)
   - Content-addressed reference to governance documents
   - Must be immutable and verifiable

### NOT Acceptable as DAO Public Identifier:

- ❌ GitHub repository URL alone (not immutable, not on-chain)
- ❌ Traditional website URLs
- ❌ Email addresses
- ❌ Social media handles

## Why GitHub Repository URL is NOT Sufficient

While a GitHub repository URL might seem like a public identifier:

1. **Not Immutable**: Repository contents can change
2. **Not Decentralized**: Controlled by GitHub, not the DAO
3. **Not On-Chain**: Doesn't meet the blockchain governance intent of SF0068
4. **Centralized Point of Failure**: GitHub can delete or suspend repositories

## Recommended Approach for Strategickhaos DAO LLC

### Option 1: Deploy Smart Contract (Recommended)
1. Deploy a simple governance contract to Ethereum/Polygon/Base
2. Use the contract address as the DAO Public Identifier
3. Register with Wyoming SOS within 30 days

### Option 2: Use Decentralized Identifier
1. Register a `did:web` or `did:ethr` identifier
2. Link to verifiable governance documents
3. Submit as DAO Public Identifier

### Option 3: Hybrid Approach
1. Deploy governance contract
2. Store governance documents on IPFS
3. Submit contract address + IPFS hash

## Strategickhaos DAO Dissolution Context

**Status**: Administratively Dissolved (November 2025)
**Reason**: Failed to provide DAO Public Identifier within 30 days
**Implication**: Clean slate - no operational history to unwind

## Fresh Start Plan

1. **Prepare Smart Contract** - Before refiling
2. **Deploy to Testnet** - Verify functionality
3. **Deploy to Mainnet** - Obtain contract address
4. **File New Wyoming DAO LLC** - Include contract address from day one
5. **Submit DAO Public Identifier** - Within filing, not after

## References

- Wyoming SF0068 (2022) - DAO Supplement Amendments
- Wyoming Statutes Title 17, Chapter 31
- Wyoming Secretary of State Business Division

---

**Document Status**: INTERNAL REFERENCE - NOT LEGAL ADVICE  
**Last Updated**: 2025-11-25  
**Review Required**: Wyoming-licensed counsel before any filings
