# Execution Checklist — Irrevocable 7% Charitable Assignment

**Strategickhaos DAO LLC / Valoryield Engine**

## INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

---

## One-Day Execution Checklist

This checklist guides the execution of an irrevocable 7% royalty assignment to charitable beneficiaries. Complete all items in sequence.

---

### Phase 1: Preparation (Morning)

#### Legal Instrument
- [ ] Review `irrevocable_assignment_template.txt`
- [ ] Fill in all placeholders:
  - [ ] Execution date
  - [ ] Beneficiary names, EINs, and percentage shares
  - [ ] Complete Exhibit A (IP enumeration)
  - [ ] Complete Exhibit B (contact/payment details)
- [ ] Verify all beneficiaries are qualified 501(c)(3) organizations
- [ ] Print two copies for signing (original + notarized copy)

#### Notarization Preparation
- [ ] Locate nearest notary public
- [ ] Bring valid government-issued photo ID
- [ ] Schedule notary appointment if required

---

### Phase 2: Execution (Midday)

#### Signing and Notarization
- [ ] Sign assignment document (both copies)
- [ ] Have notary witness signature
- [ ] Notary completes acknowledgment section
- [ ] Notary applies seal
- [ ] Retain original; use copy for scans

#### Scanning and Digital Preservation
- [ ] Scan notarized document to PDF/A format
- [ ] Filename format: `Assignment_YYYY-MM-DD.pdf`
- [ ] Verify scan quality (readable, complete)

---

### Phase 3: Cryptographic Proof Chain (Afternoon)

#### Compute SHA-256 Hash
```powershell
# Windows PowerShell
Get-FileHash .\Assignment_2025-11-28.pdf -Algorithm SHA256
```

```bash
# Linux/Mac
sha256sum Assignment_2025-11-28.pdf
```

- [ ] Record hash value in evidence ledger

#### OpenTimestamps
```powershell
# Install if needed
python -m pip install opentimestamps-client

# Create timestamp proof
ots stamp Assignment_2025-11-28.pdf
```

- [ ] Verify `.ots` file created
- [ ] Note: Bitcoin confirmation may take hours/days

#### GPG Signature
```powershell
# Windows - add GnuPG to path if needed
$env:Path += ";C:\Program Files (x86)\GnuPG\bin"

# Verify key availability
gpg --list-keys

# Create detached signature
gpg --detach-sign --armor Assignment_2025-11-28.pdf
```

- [ ] Verify `.asc` file created

#### IPFS Upload (Optional but Recommended)
```powershell
# Upload all artifacts
ipfs add Assignment_2025-11-28.pdf
ipfs add Assignment_2025-11-28.pdf.ots
ipfs add Assignment_2025-11-28.pdf.asc
```

- [ ] Record all CIDs in evidence ledger

---

### Phase 4: Delivery (Same Day)

#### Deliver to Beneficiaries
- [ ] **Email delivery** (fastest):
  - [ ] Compose email with executed PDF attached
  - [ ] Request written acknowledgment
  - [ ] Use read receipt if available
  
- [ ] **Certified mail** (strongest proof):
  - [ ] Mail executed copy to each charity
  - [ ] Request return receipt (green card)
  - [ ] Retain tracking numbers

- [ ] **Both methods recommended** for maximum protection

#### Request Acknowledgments
- [ ] Include `charity_acknowledgment_template.txt` for charity reference
- [ ] Specify deadline for acknowledgment (30 days recommended)
- [ ] Provide contact information for questions

---

### Phase 5: Documentation (Evening)

#### Evidence Ledger
- [ ] Complete `evidence_ledger_template.yaml` with:
  - [ ] All hash values
  - [ ] GPG signature metadata
  - [ ] OTS file references
  - [ ] IPFS CIDs
  - [ ] Execution timestamp
  - [ ] Delivery records

#### Git Repository
```powershell
# Create or update repository
git add ledger/evidence_ledger.yaml
git add proofs/*.ots proofs/*.asc

# Sign commit
git commit -S -m "Execute irrevocable 7% charitable assignment"

# Push to remote
git push origin main
```

- [ ] Commit evidence ledger to Git
- [ ] GPG-sign the commit
- [ ] Push to remote repository

---

### Phase 6: Tax Substantiation (Within 30 Days)

#### If Taking Deduction
- [ ] Review IRS Publication 526
- [ ] Determine if Form 8283 required (>$500 noncash)
- [ ] Determine if qualified appraisal required (>$5,000)
- [ ] Schedule appraisal if needed
- [ ] Complete `irs_compliance_checklist.md`

#### Acknowledgment Collection
- [ ] Track acknowledgment receipt from each charity
- [ ] Verify acknowledgments meet IRS requirements:
  - [ ] Description of property
  - [ ] Statement re: goods/services
- [ ] File acknowledgments with tax records

---

## Post-Execution Verification

### Immediate (Day 1)
- [ ] All documents signed and notarized
- [ ] Hash computed and recorded
- [ ] OTS proof created
- [ ] GPG signature created
- [ ] Delivery initiated to all beneficiaries
- [ ] Evidence ledger committed to Git

### Short-term (Days 2-7)
- [ ] IPFS pins confirmed (if used)
- [ ] Delivery receipts received
- [ ] OpenTimestamps Bitcoin confirmation pending

### Medium-term (Days 7-30)
- [ ] Written acknowledgments received from all charities
- [ ] Form 8283 prepared (if applicable)
- [ ] Appraisal scheduled/completed (if applicable)

### Long-term (Quarterly)
- [ ] First quarterly payment prepared
- [ ] Payment statements distributed
- [ ] Ledger updated with payment records

---

## File Checklist

After execution, you should have:

```
sovereign-vault/
├── README.md
├── docs/
│   └── assignment/
│       └── Assignment_2025-11-28_redacted.pdf
├── proofs/
│   ├── Assignment_2025-11-28.pdf.ots
│   ├── Assignment_2025-11-28.pdf.asc
│   └── SHA256SUMS.txt
├── ledger/
│   ├── evidence_ledger.yaml
│   └── ledger.csv
└── acknowledgments/
    ├── StJude/
    │   └── ack_2025-11-28.pdf
    └── MSF/
        └── ack_2025-11-28.pdf
```

---

## Troubleshooting

### GPG Issues on Windows
```powershell
# Add to PATH
$env:Path += ";C:\Program Files\Git\bin;C:\Program Files (x86)\GnuPG\bin"

# Import key if needed
gpg --import "$env:USERPROFILE\.gnupg\private-keys-v1.d\YOURKEY.key"

# Verify Git GPG configuration
git config --global commit.gpgsign true
git config --global gpg.program "gpg"
```

### OpenTimestamps Issues
```powershell
# Upgrade pip and reinstall
python -m pip install --upgrade pip
python -m pip install --force-reinstall opentimestamps-client

# Verify installation
ots --version
```

### IPFS Connection Issues
```powershell
# Start daemon if not running
ipfs daemon &

# Check connection
ipfs id
```

---

## Emergency Contacts

| Role | Contact |
|------|---------|
| Managing Member | Domenic Garza |
| Wyoming Attorney | [To be retained] |
| Notary | [Local notary] |
| Tax Advisor | [CPA/Tax professional] |

---

## Certification

I certify that all execution steps have been completed as documented.

**Executed by:** _______________________

**Date:** _______________________

**Witness/Notary:** _______________________

---

*This checklist is an internal planning tool only and does not constitute legal advice.*

© 2025 Strategickhaos DAO LLC. Internal use only.
