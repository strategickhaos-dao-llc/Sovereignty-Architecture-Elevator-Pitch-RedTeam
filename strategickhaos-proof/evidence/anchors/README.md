# Anchor Files Directory

This directory contains cryptographic anchors for the StrategicKhaos Evidence Dossier.

## 📁 Expected Contents

| File Type | Purpose | How to Create |
|-----------|---------|---------------|
| `*.json` | Aggregated status snapshots | Export from monitoring systems |
| `*.asc` | GPG/PGP signatures | `gpg --armor --sign <file>` |
| `*.ots` | OpenTimestamps proofs | `ots stamp <file>` |

## 🔐 Adding New Anchors

### 1. Create a Snapshot Anchor

```bash
# Export current state
python ../verify_evidence.py --export-snapshot > snapshot_$(date +%Y%m%d).json

# Sign with GPG
gpg --armor --sign snapshot_$(date +%Y%m%d).json

# Create OTS timestamp
ots stamp snapshot_$(date +%Y%m%d).json
```

### 2. PID-RANCO Run Anchors

For PID-RANCO (Process ID - Random Nonce Correlation) runs:

```bash
# After a successful deployment/operation run:
# 1. Export the run log
# 2. Compute hash
# 3. Create OTS timestamp

echo '{"run_id": "PID-RANCO-001", "timestamp": "...", "result": "..."}' > pid_ranco_001.json
ots stamp pid_ranco_001.json
```

### 3. Infrastructure State Anchors

For multi-cloud infrastructure snapshots:

```bash
# AWS
aws sts get-caller-identity > aws_identity.json

# GCP
gcloud config list --format=json > gcp_config.json

# Azure
az account show > azure_account.json

# Combine and timestamp
cat aws_identity.json gcp_config.json azure_account.json | jq -s '.' > infra_snapshot.json
ots stamp infra_snapshot.json
```

## 📋 File Naming Convention

```
<type>_<identifier>_<date>.<extension>

Examples:
- snapshot_weekly_20241202.json
- pid_ranco_deployment_20241201.json
- infra_state_20241130.json
- governance_vote_001.json.asc
- governance_vote_001.json.ots
```

## ✅ Verification

```bash
# Verify OTS timestamp
ots verify <filename>.ots

# Verify GPG signature
gpg --verify <filename>.asc
```

## ⚠️ Important Notes

1. **OTS Pending**: OpenTimestamps may show "pending" until Bitcoin confirmation (~hours)
2. **GPG Keys**: Ensure signing keys are published to keyservers
3. **JSON Validity**: Always validate JSON before anchoring

---

*Part of the StrategicKhaos Proof Evidence Dossier*
