# Charitable Contributions Framework

**Strategickhaos DAO LLC / Valoryield Engine**

## INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED

This document outlines the framework for irrevocable charitable assignments aligned with IRS rules and proper legal instruments.

---

## Important Corrections

### CRUT Clarification (26 U.S.C. §664)

A Charitable Remainder Unitrust (CRUT) **cannot simply "assign 7% of gross royalties to charities."** CRUTs pay a yearly percentage (5–50%) of trust value to noncharitable beneficiaries; the charity receives the remainder later.

For an **immediate, irrevocable 7% charitable skim from all present/future royalties**, use either:

1. **Charitable Lead Trust (CLAT/CLUT)** — For a lead interest to charity now
2. **Direct Irrevocable Assignment** — Simplest and fastest audit trail (RECOMMENDED)

### Filing Clarifications

- Filing a trust with Wyoming SOS does **not** make it a CRUT nor "irrevocable" by itself
- Irrevocability comes from the **executed trust/assignment instrument**
- CRUTs require compliance with §664 terms and IRS filings

### Deduction Requirements

For IP/royalty assignments, you must meet substantiation rules:
- **IRS Publication 526** — Charitable Contributions
- **Form 8283** — Noncash Charitable Contributions (if >$500)
- **Form 8899** — Donee Information Return (charity files for donated IP income)
- **Form 1041** — Annual filing if a trust is created

---

## Recommended Approach: Direct Irrevocable Assignment

### What It Does

Permanently assigns 7% of gross royalties from defined IP/works to named 501(c)(3) charities, proportionally or in fixed splits.

### Why This Approach

- **Fastest execution** — No trust administration overhead
- **Simplest audit trail** — Clear chain of custody
- **Lower ongoing costs** — No annual trust filings
- **Immediate effect** — Assignment completes upon delivery

### Implementation Steps

1. **Identify Property**
   - Precisely list works, codebases, patents, future derivatives
   - Define revenue streams (copyrights, licensing, SaaS, token royalties)

2. **Draft Assignment**
   - Include irrevocability clause
   - Present assignment of future royalties
   - Governing law specification
   - Split schedule
   - Audit rights
   - Notice addresses

3. **Execute**
   - Sign and notarize
   - Deliver executed copies to each charity
   - Delivery completes the gift
   - Obtain written acknowledgments

4. **Substantiate Tax**
   - Follow Pub 526 rules if taking deduction
   - File Form 8283 if >$500 noncash
   - Qualified appraisal if >$5,000
   - Charities may file Form 8899 for IP income

---

## Templates

The following templates are provided in the `templates/` subdirectory:

| Template | Purpose |
|----------|---------|
| `irrevocable_assignment_template.txt` | Main assignment document |
| `charity_acknowledgment_template.txt` | Charity acknowledgment letter |
| `evidence_ledger_template.yaml` | Cryptographic proof chain |
| `irs_compliance_checklist.md` | IRS substantiation checklist |

---

## Cryptographic Proof Chain

### Steps for Public, Verifiable Proof

1. **Hash and Timestamp**
   ```powershell
   Get-FileHash .\Assignment_2025-11-28.pdf -Algorithm SHA256
   ```

2. **OpenTimestamps**
   ```powershell
   python -m pip install opentimestamps-client
   ots stamp Assignment_2025-11-28.pdf
   ```

3. **GPG Sign**
   ```powershell
   gpg --detach-sign --armor Assignment_2025-11-28.pdf
   ```

4. **IPFS Upload**
   ```powershell
   ipfs add Assignment_2025-11-28.pdf Assignment_2025-11-28.pdf.ots Assignment_2025-11-28.pdf.asc
   ```

5. **Evidence Ledger**
   - Commit YAML ledger to Git repository
   - Include SHA256 hashes, GPG signatures, OTS proofs, IPFS CIDs

---

## Quarterly Process

1. Run revenue report; compute 7% due per beneficiary
2. Pay within 30 days; attach payment statement
3. Append entry to ledger.csv; hash and stamp; commit signed
4. Email statement to beneficiaries; archive receipts

---

## Alternative: Charitable Lead Unitrust (CLUT)

If you want a trust wrapper:

- Draft a CLUT paying 7% of annual trust asset value to charities for X years
- Remainder goes to your LLC after term
- Fund by transferring royalty rights into the trust
- Requires formal trust document meeting §170(f)(2)(B) and §664 regs
- Requires appraisals upon funding, Form 1041 filings, trustee administration
- **Slower and costlier than direct assignment**

---

## IRS References

- **Publication 526** — Charitable Contributions (Last reviewed Apr 2, 2025)
- **Form 8283 and Instructions** — Noncash Charitable Contributions (Last reviewed Dec 3, 2024)
- **Form 8899** — Donee Information Return (for IP income reporting)
- **26 U.S.C. §170** — Charitable Contributions deduction rules
- **26 U.S.C. §664** — Trust approaches (CRUT/CLUT)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | Strategickhaos DAO | Initial framework |

---

*This document contains internal drafts only and does not constitute legal advice. All legal matters must be reviewed by qualified counsel.*

© 2025 Strategickhaos DAO LLC. Internal use only.
