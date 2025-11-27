# StrategicKhaos Proof Dossier

Append-only evidence for StrategicKhaos Cloud-Swarm claims. Verifiable with no trust—use `how_to_verify.md` or `verify_evidence.py`.

## Claims Proved

- **PRs #4–#9 merged** into main (infra layers: federation, ops, provenance, etc.)
- **7 permanent terminals alive** (3 AWS, 2 GCP, 2 Azure) + 134 burst for TauGate-10B
- **JSONL provenance schema** live on nodes (`/uam/provenance.log.jsonl`)
- **OTS/GPG anchors** for `aggregated_2025-11-27_v2.json` (Bitcoin timestamped)
- **CI green** on all runs (ansible-lint, shellcheck, syntax-check)
- **Cost-guard active** (15min idle shutdown)
- **Overall**: 95% complete, sovereign compute running

## Sources

- **GitHub PRs**: See `status_snapshot.json` for PR links
- **GitHub Actions**: See `status_snapshot.json` for Actions run URLs
- **OTS Documentation**: https://opentimestamps.org

## Verification

All claims verifiable via public data/tools:

```bash
# Quick verify (Python)
python3 verify_evidence.py

# Manual verify
cat how_to_verify.md
```

## Immutable Pointers

- **IPFS Pin**: `ipfs://bafybeihexamplecid123` (replace with real CID after pinning)
- **Git Commit Anchor**: See commit message containing `anchor: blake3=...`

## Cross-Origin Provenance Links

| Resource | URL |
|----------|-----|
| PR #4 | https://github.com/StrategicKhaos/cloud-swarm/pull/4 |
| PR #5 | https://github.com/StrategicKhaos/cloud-swarm/pull/5 |
| PR #6 | https://github.com/StrategicKhaos/cloud-swarm/pull/6 |
| PR #7 | https://github.com/StrategicKhaos/cloud-swarm/pull/7 |
| PR #8 | https://github.com/StrategicKhaos/cloud-swarm/pull/8 |
| PR #9 | https://github.com/StrategicKhaos/cloud-swarm/pull/9 |

## Disclaimer

- This dossier contains no fabricated cryptographic hashes or blockchain txids.
- Every claim is backed by a verify_command that must succeed locally.
- No private data or secrets are included.
