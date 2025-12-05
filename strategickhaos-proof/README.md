# StrategicKhaos Proof Repository

This repository contains cryptographically verifiable evidence for the StrategicKhaos project claims.

## Claims List

| Claim | Status | Evidence |
|-------|--------|----------|
| PRs Merged | ✅ | #4, #5, #6, #7, #8, #9 |
| Cloud Terminals | ✅ | AWS: 3, GCP: 2, Azure: 2, Total: 7 |
| Burst Nodes | ✅ | 134 nodes |
| Provenance Schema | ✅ | JSONL format |
| CI Status | ✅ | Green |
| Cost Guard | ✅ | Active |

## Integrity Anchors

| File | Blake3 Hash |
|------|-------------|
| `aggregated_2025-11-27_v2.json` | `48215cbeff837b9598d75f5ddf2aa2a5cfe867a2c54cedd7e1d834486c1c8434` |

## Verification

See [how_to_verify.md](how_to_verify.md) for manual verification commands.

Run the one-command verifier:
```bash
python3 verify_evidence.py
```

## File Structure

```
strategickhaos-proof/
├── README.md              # This file
├── status_snapshot.json   # Current status snapshot
├── hashes.txt             # Blake3 hashes for all files
├── how_to_verify.md       # Verification commands
├── verify_evidence.py     # One-command verifier script
└── anchors/
    ├── aggregated_2025-11-27_v2.json      # Main aggregate data
    ├── aggregated_2025-11-27_v2.json.asc  # GPG signature
    ├── aggregated_2025-11-27_v2.json.ots  # OpenTimestamps proof
    └── aggregated_2025-11-27_v2.json.prov.json  # Provenance data
```

## Commit Anchor

```
anchor: blake3=48215cbeff837b9598d75f5ddf2aa2a5cfe867a2c54cedd7e1d834486c1c8434 for aggregated_2025-11-27_v2.json
```

## Sources

- GitHub Actions: https://github.com/StrategicKhaos/cloud-swarm/actions
- Pull Requests: https://github.com/StrategicKhaos/cloud-swarm/pulls

## Timestamp

Generated: 2025-11-27T13:05:00Z
Overall Completion: 95%
