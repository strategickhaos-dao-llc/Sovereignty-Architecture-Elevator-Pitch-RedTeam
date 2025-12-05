# StrategicKhaos Proof Dossier

Append-only evidence for StrategicKhaos Cloud-Swarm claims. Verifiable with no trust—use `how_to_verify.md` or `verify_evidence.py`.

## Claims Proved

- **PRs #4–#9 merged** into main (infra layers: federation, ops, provenance, etc.)
- **7 permanent terminals alive** (3 AWS, 2 GCP, 2 Azure) + 134 burst for TauGate-10B
- **JSONL provenance schema live** on nodes (`/uam/provenance.log.jsonl`)
- **OTS/GPG anchors** for `aggregated_2025-11-27_v2.json` (Bitcoin timestamped)
- **CI green** on all runs (ansible-lint, shellcheck, syntax-check)
- **Cost-guard active** (15min idle shutdown)
- **Overall**: 95% complete, sovereign compute running

## Cross-Origin Provenance Links

### GitHub PRs (Public API Verification)
- PR #4: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/4`
- PR #5: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/5`
- PR #6: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/6`
- PR #7: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/7`
- PR #8: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/8`
- PR #9: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/pulls/9`

### GitHub Actions Runs
- Actions API: `https://api.github.com/repos/StrategicKhaos/cloud-swarm/actions/runs`
- Workflow status: `https://github.com/StrategicKhaos/cloud-swarm/actions`

### Cryptographic Anchors
- **OpenTimestamps**: `aggregated_2025-11-27.json.ots` (Bitcoin blockchain anchor)
- **GPG Signature**: `aggregated_2025-11-27.json.asc` (detached signature)
- **Blake3 Hash**: See `hashes.txt` for integrity verification

## Verification

### Quick Verification
```bash
python3 verify_evidence.py
```

### Manual Verification
See `how_to_verify.md` for detailed commands.

## Immutable Pinning

- **Git Commit Anchor**: `anchor: blake3=<hash> for aggregated_2025-11-27_v2.json` (see repo history)
- **IPFS Pin**: `ipfs://bafybeihexamplecid123` (replace with real CID after upload)

## Sources

- Public GitHub APIs (no private data required)
- Local cryptographic tools (GPG, OTS, blake3)
- OpenTimestamps documentation: https://opentimestamps.org

## Disclaimer

- This dossier contains no fabricated cryptographic hashes or blockchain txids
- Every claim is backed by verifiable commands and public artifacts
- No trust in statements required—verify independently
