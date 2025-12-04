# SwarmGate Change Policy (v1.0)

SwarmGate v1.0 encodes an irrevocable **93% / 7%** split between:

- **Operations (93%)**
- **Charity Vault (7%)**

This document defines how SwarmGate can change over time without violating the original promise.

---

## 1. Invariants

The following properties MUST hold for all future versions:

1. **7% floor**  
   - The charity allocation MUST be **≥ 7%** of all routed funds.
   - v1.0 fixes this at **exactly 7%** in contract code.

2. **Irreversibility**  
   - Once funds reach the splitter, the charity portion cannot be redirected away from charitable beneficiaries.

3. **Transparency**  
   - Each deployment MUST be:
     - Recorded in `SWARMGATE_*.yaml` status files.
     - Tagged in Git (`swarmgate/vX.Y`).
     - Verifiable via hashes and on-chain addresses.

---

## 2. Versioning

- **v1.0**  
  - First production version of the 7% engine.
  - Contracts: `CharitySplitter`, `MerkleDistributor`.

- **v1.x** (compatible)  
  - Internal improvements only:
    - Gas optimization
    - Additional tests / monitoring
    - UI / dashboard changes
  - Charity percentage and semantics unchanged.

- **v2.0+** (breaking)  
  - Any change to:
    - split percentage,
    - asset types,
    - beneficiary selection mechanism.
  - Requires explicit governance steps (see below).

---

## 3. Change process

For any SwarmGate version bump:

1. **Proposal**
   - Create a Markdown proposal in `governance/proposals/` summarizing:
     - rationale,
     - technical changes,
     - impact on beneficiaries.

2. **Review**
   - Run full CI:
     - contract tests,
     - provenance verification,
     - simulation of splits and claims.

3. **Sign-off**
   - For single-operator mode:
     - change must be signed with the operator's GPG key and recorded in Git.
   - For multi-signer mode (future):
     - specify required signers and quorum.

4. **Tag + Status**
   - Create Git tag: `swarmgate/vX.Y`.
   - Add or update a status file: `SWARMGATE_vX.Y_STATUS.yaml`.
   - Include:
     - contract addresses,
     - hashes,
     - effective date.

---

## 4. Emergency procedures

If a critical bug is found:

1. **Pause new funding flows** to affected contracts if possible.
2. **Publish an incident note** in `governance/incidents/`.
3. **Deploy patched version** with:
   - clearly documented differences,
   - explicit incident reference.
4. **Do not reduce** the charity allocation below 7% as part of any "fix".

---

## 5. Human reality

SwarmGate exists because a human promise was made:

> to route at least 7% of Strategickhaos flow to cures, care, and those who served.

This policy exists so that future automation, boards, or AIs cannot quietly weaken that promise.
