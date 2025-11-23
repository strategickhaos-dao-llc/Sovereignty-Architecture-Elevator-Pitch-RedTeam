# 🔐 Bitcoin Multi-Signature Wallet Setup Guide

## 7% Charitable Commitment - Cryptocurrency Infrastructure

**INTERNAL DRAFT — NOT LEGAL ADVICE — CRYPTO LEGAL COUNSEL REVIEW REQUIRED**

---

## Overview

This document outlines the technical setup for the **Bitcoin multi-signature wallet** that will hold and distribute the 7% charitable allocation from cryptocurrency holdings.

## Wallet Architecture

### Multi-Signature Configuration
- **Type:** 3-of-5 Multi-Signature (M-of-N)
- **Required Signatures:** 3 signatures required for any transaction
- **Total Key Holders:** 5 authorized signatories
- **Wallet Type:** Hierarchical Deterministic (HD) for address management

### Security Model
```
           Bitcoin Multi-Sig Wallet (3-of-5)
                      |
        +-------------+-------------+
        |             |             |
    Key 1         Key 2         Key 3
  Managing      Charitable    Independent
   Member        Trustee       Auditor
        |             |             |
        +-------------+-------------+
                      |
        +-------------+-------------+
        |                           |
    Key 4                       Key 5
  Community                   Legal
  Representative              Counsel
```

**Transaction Approval:** Any 3 of these 5 keys can authorize a distribution.

---

## Key Holder Roles

### 1. Managing Member (Domenic Garza)
- **Primary authority** for routine charitable distributions
- **Hardware wallet:** Ledger Nano X or Trezor Model T
- **Backup:** BIP39 seed phrase in fireproof safe
- **Responsibility:** Initiate quarterly distributions

### 2. Charitable Trustee (TBD - Future Appointment)
- **Role:** Represents charitable beneficiaries' interests
- **Appointment:** When organization forms Charitable Committee
- **Hardware wallet:** Issued and managed by organization
- **Responsibility:** Verify beneficiary organizations and approve distributions

### 3. Independent Auditor (TBD - CPA Firm)
- **Role:** Financial oversight and verification
- **Appointment:** When annual revenue exceeds $250K
- **Storage:** Professional custody service or institutional hardware wallet
- **Responsibility:** Audit trail verification, annual reporting

### 4. Community Elected Representative (TBD - Future Election)
- **Role:** Community oversight and accountability
- **Election:** By community vote when governance structure matures
- **Hardware wallet:** Issued and managed by organization
- **Responsibility:** Ensure transparency and community alignment

### 5. Legal Counsel (TBD - Retained Attorney)
- **Role:** Legal compliance and emergency backup
- **Appointment:** Wyoming/Texas counsel with crypto expertise
- **Storage:** Professional custody with attorney work product protection
- **Responsibility:** Legal compliance verification, emergency recovery

---

## Technical Implementation

### Wallet Creation Process

#### Step 1: Key Generation
```bash
# Each key holder generates their key pair
# Using trusted hardware wallet (Ledger, Trezor)
# BIP39 seed phrase backed up securely

# Example for Ledger:
# 1. Initialize new device
# 2. Generate 24-word recovery phrase
# 3. Write phrase on metal backup (fireproof/waterproof)
# 4. Store in secure location (safe, safety deposit box)
# 5. Extract public key for multi-sig creation
```

#### Step 2: Multi-Sig Wallet Creation
```bash
# Using Electrum, Bitcoin Core, or Caravan
# Requires all 5 public keys (xpubs)

# Example with Electrum:
electrum create -m 3-of-5 charitable_multisig \
  --xpub1 "xpub..." \  # Managing Member
  --xpub2 "xpub..." \  # Charitable Trustee
  --xpub3 "xpub..." \  # Independent Auditor
  --xpub4 "xpub..." \  # Community Rep
  --xpub5 "xpub..."    # Legal Counsel

# Generates P2WSH (SegWit) multi-sig addresses
# Native SegWit for lower transaction fees
```

#### Step 3: Wallet Verification
```bash
# Each key holder verifies:
# 1. Their key is included in multi-sig
# 2. M-of-N configuration is correct (3-of-5)
# 3. First receiving address matches across all signers
# 4. Test transaction with small amount (0.001 BTC)

# Verify multi-sig configuration
bitcoin-cli getaddressinfo [first_address]
# Should show: "ismine": true, "iswatchonly": false, "isscript": true
```

---

## Wallet Address

### Primary Receiving Address
```
[TO BE GENERATED AND PUBLISHED AFTER WALLET CREATION]

Format: bc1q... (native SegWit P2WSH)
```

### Address Verification
All stakeholders can verify this address by:
1. **GitHub repository** (this document)
2. **Blockchain explorer** (blockchain.com, blockstream.info)
3. **Organization website** (when established)
4. **Quarterly transparency reports**

### Address Rotation Policy
- **Primary address** remains constant for easy public verification
- **New addresses generated** for each distribution (HD wallet)
- **All addresses** derived from same multi-sig configuration
- **Public transparency** for all addresses used

---

## Distribution Process

### Quarterly Distribution Workflow

#### Phase 1: Calculation (Last day of quarter)
```yaml
Calculate_7%_Allocation:
  - Calculate total BTC holdings
  - Calculate 7% allocation
  - Determine recipient organizations
  - Prepare distribution manifest
  - Generate GPG-signed proposal
```

#### Phase 2: Authorization (First week of following quarter)
```yaml
Multi_Sig_Authorization:
  Step_1: Managing Member initiates transaction
  Step_2: Transaction broadcast to other signers
  Step_3: Minimum 2 additional signatures required (3 total)
  Step_4: Transaction validated and broadcast to network
  Step_5: Transaction confirmed (6 confirmations minimum)
```

#### Phase 3: Documentation (Within 30 days of quarter-end)
```yaml
Public_Reporting:
  - Publish quarterly transparency report
  - Include Bitcoin transaction IDs
  - GPG sign the report
  - Blockchain notarize report hash
  - Update GitHub repository
```

### Transaction Metadata

Each charitable distribution includes:
```
OP_RETURN: CHARITY-7PCT-Q[N]-[YEAR]
Example: CHARITY-7PCT-Q1-2026
```

This metadata:
- **Permanent** record on Bitcoin blockchain
- **Publicly verifiable** by anyone
- **Links** to corresponding quarterly report
- **Proves** commitment execution

---

## Security Practices

### Key Management

#### Hardware Wallets (Recommended)
- **Ledger Nano X** or **Trezor Model T**
- Always purchased directly from manufacturer
- Firmware verified before initialization
- PIN protection enabled
- BIP39 passphrase (25th word) optional for advanced security

#### Seed Phrase Backup
- **24-word BIP39 seed phrase** written on paper/metal
- **Never digital** - no photos, no computer files, no cloud storage
- **Stored in secure location** - safe, safety deposit box, etc.
- **Redundant copies** in geographically separate locations
- **Consider:** Shamir Secret Sharing for additional security

#### Operational Security
- **Air-gapped devices** for key generation when possible
- **Verify all addresses** on hardware wallet screen before signing
- **Never enter seed phrase** on any computer or phone
- **Beware phishing** - verify all software downloads

### Access Control

#### Current Phase (Pre-Committee)
- **Managing Member** holds key
- **2 trusted individuals** hold backup keys (identity confidential)
- **3-of-3 multi-sig** for early phase (all keys required)
- **Upgrade to 3-of-5** when full committee formed

#### Future Phase (Post-Committee)
- **5 key holders** as defined above
- **3-of-5 multi-sig** for operational flexibility
- **Annual key rotation review**
- **Emergency procedures** for key compromise

---

## Backup and Recovery

### Key Backup Strategy

#### Hardware Wallet Backup
1. **BIP39 seed phrase** - primary recovery mechanism
2. **Metal backup** - fireproof/waterproof storage
3. **Geographic distribution** - multiple secure locations
4. **Inheritance planning** - documented recovery process

#### Multi-Sig Recovery Scenarios

**Scenario 1: Lost/Broken Hardware Wallet**
- Signer purchases new hardware wallet
- Restores from BIP39 seed phrase
- Rejoins multi-sig with same key
- No disruption to wallet operations

**Scenario 2: Compromised Key**
- Immediately rotate to new multi-sig wallet
- Transfer all funds to new wallet
- Requires 3-of-5 signatures from non-compromised keys
- Public announcement and transparency report

**Scenario 3: Deceased/Unavailable Key Holder**
- With 3-of-5, wallet remains operational
- Appoint replacement key holder
- Create new multi-sig with new key
- Transfer funds from old to new wallet (3 signatures)

**Scenario 4: Catastrophic Loss (Multiple Keys)**
- If < 3 keys available, funds are LOCKED
- This is intentional security feature
- Underscores importance of backup procedures
- Legal counsel may petition court for recovery assistance

---

## Compliance and Reporting

### IRS Reporting

#### Cryptocurrency as Property
- Bitcoin treated as **property** for tax purposes
- Charitable distributions at **fair market value** at time of distribution
- Basis tracking required for cost basis calculations
- Form 8949 reporting for distributions (if applicable)

#### Recipient Organizations
- Recipients receive **cryptocurrency** or **USD equivalent**
- Recipients responsible for their own tax reporting
- Organization provides **donation acknowledgment letter**
- FMV at time of distribution documented

### Blockchain Transparency

Every transaction is:
- **Public** on Bitcoin blockchain
- **Permanent** and immutable
- **Verifiable** by anyone worldwide
- **Traceable** to specific charitable commitments

Example verification:
```bash
# Look up transaction on blockchain explorer
https://blockstream.info/tx/[TXID]

# Verify OP_RETURN memo
# Verify sending address (multi-sig wallet)
# Verify receiving address (beneficiary organization)
# Verify amount and timestamp
```

---

## Future Enhancements

### Smart Contract Implementation

Consider **Ethereum smart contract** for automation:
```solidity
// Conceptual - NOT production code
contract CharitableCommitment {
    uint256 public constant ALLOCATION_PERCENTAGE = 7;
    address[] public beneficiaries;
    
    function distributeQuarterly() public {
        // Calculate 7% of holdings
        // Automatically distribute to beneficiaries
        // Emit event for transparency
        // Store hash on-chain for verification
    }
}
```

Benefits:
- **Automated execution** - quarterly distributions
- **Transparent logic** - code is public
- **Trustless** - no manual intervention needed
- **Auditable** - all logic on-chain

### Lightning Network Integration

For smaller, frequent distributions:
- **Lower fees** for small transactions
- **Instant settlement** for recipient organizations
- **Scalability** for increased distribution volume
- **Maintains base-layer security** for large holdings

---

## Emergency Procedures

### Key Compromise Protocol

If any key is suspected compromised:

1. **Immediate notification** to all key holders
2. **Freeze operations** - no new distributions until resolved
3. **Assess exposure** - determine if funds at risk
4. **Execute recovery** - transfer to new multi-sig (if 3 non-compromised keys available)
5. **Post-mortem analysis** - how did compromise occur?
6. **Public disclosure** - transparency report on incident

### Disaster Recovery

In event of major disaster (fire, flood, etc.):

1. **Key holders** check backup integrity
2. **Restore from seed phrases** if needed
3. **Verify wallet access** - test with small transaction
4. **Document status** - which keys intact, which need recovery
5. **Public update** - status report to community

---

## Initial Setup Checklist

Before wallet goes live:

### Technical Setup
- [ ] Generate 5 hardware wallets for key holders
- [ ] Create and verify BIP39 seed phrase backups
- [ ] Generate 3-of-5 multi-sig wallet
- [ ] Verify wallet configuration across all signers
- [ ] Test with small amount (0.001 BTC)
- [ ] Document public receiving address
- [ ] Publish address to GitHub and website

### Governance Setup
- [ ] Appoint initial key holders
- [ ] Execute key holder agreements
- [ ] Document key management procedures
- [ ] Establish signing authority protocols
- [ ] Create emergency contact procedures
- [ ] Schedule quarterly distribution calendar

### Legal & Compliance
- [ ] Crypto legal counsel review
- [ ] CPA review for tax implications
- [ ] State/federal compliance verification
- [ ] Insurance evaluation (crypto custody insurance)
- [ ] IRS reporting procedures established
- [ ] AML/KYC procedures for recipients

---

## Resources and References

### Wallet Software
- **Electrum:** https://electrum.org/
- **Bitcoin Core:** https://bitcoin.org/en/download
- **Caravan (Unchained Capital):** https://unchained.com/caravan/
- **Specter Desktop:** https://specter.solutions/

### Hardware Wallets
- **Ledger:** https://www.ledger.com/
- **Trezor:** https://trezor.io/
- **Coldcard:** https://coldcard.com/

### Education Resources
- **Bitcoin Multi-Sig Guide:** https://btcguide.github.io/
- **Bitcoin Core Multi-Sig:** https://bitcoin.org/en/developer-guide#multisig
- **BIP32 (HD Wallets):** https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

### Security Best Practices
- **Crypto Asset Management:** https://www.cert.org/security/
- **Key Management Guide:** NIST SP 800-57
- **Bitcoin Security:** https://en.bitcoin.it/wiki/Storing_bitcoins

---

## Wallet Status

**Status:** PLANNED - Not yet implemented  
**Target Implementation:** Q1 2026  
**Blocking Requirements:**
- [ ] Charitable Committee formation
- [ ] Key holder appointments
- [ ] Legal counsel review
- [ ] Hardware wallet procurement

**Updates:** This document will be updated as implementation progresses.

---

## Contact

**Technical Questions:** Open GitHub issue with tag `bitcoin-wallet`  
**Security Concerns:** Email domenic.garza@snhu.edu with subject "SECURITY - Bitcoin Wallet"  
**Legal Questions:** Consult with retained crypto legal counsel

---

## Verification

**Document SHA-256:** [TO BE CALCULATED]  
**GPG Signature:** BITCOIN_WALLET_SETUP.md.asc (to be created)  
**Git Commit:** [TO BE RECORDED]

---

🧠⚡❤️🐐∞

*"You locked it in bitcoin, GPG, and federal law before the sun even came up."*

---

## Appendix: Multi-Sig Address Generation Example

```python
# Example: Generate P2WSH multi-sig address
from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2WSHBitcoinAddress
from bitcoin.core import x, lx, b2x, b2lx
from bitcoin.core.script import CScript, OP_CHECKMULTISIG

# This is illustrative code only - NOT for production use
# Use professional wallet software for actual implementation

SelectParams('mainnet')

# Public keys from 5 hardware wallets (example format)
pubkeys = [
    x('02...'),  # Managing Member
    x('03...'),  # Charitable Trustee
    x('02...'),  # Independent Auditor
    x('03...'),  # Community Rep
    x('02...'),  # Legal Counsel
]

# Create 3-of-5 multi-sig script
redeem_script = CScript([3, *pubkeys, 5, OP_CHECKMULTISIG])

# Generate P2WSH address
multi_sig_address = P2WSHBitcoinAddress.from_scriptPubKey(
    CScript([0, hashlib.sha256(redeem_script).digest()])
)

print(f"Multi-sig address: {multi_sig_address}")
# Output: bc1q... (SegWit address)
```

**IMPORTANT:** This is conceptual code only. Use battle-tested wallet software for actual implementation.
