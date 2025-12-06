# Utility Scripts

This directory contains utility scripts for the Sovereignty Architecture project.

## AI Evidence Ledger Tools

### verify_ledger.py

Validates AI conversation evidence ledgers for integrity and completeness.

**Usage:**
```bash
python3 scripts/verify_ledger.py <ledger_file.yaml>
```

**Examples:**
```bash
# Verify the example ledger
python3 scripts/verify_ledger.py examples/conversation_ledger_example.yaml

# Verify your own ledger
python3 scripts/verify_ledger.py conversation_ledger.yaml
```

**What it checks:**
- ✅ YAML syntax validity
- ✅ Required metadata fields
- ✅ Hash chain integrity
- ✅ Timestamp format (ISO 8601)
- ✅ Entry structure completeness
- ✅ Evidence references (share URLs, screenshots)
- ✅ Custodian information
- ℹ️ Optional enhancements (GPG, OpenTimestamps)

**Exit codes:**
- `0` - Verification passed
- `1` - Verification failed

**Related Documentation:**
- [Appendix C: Legal Status of AI-Generated Evidence](../APPENDIX_C_LEGAL_STATUS_AI_EVIDENCE.md)
- [Conversation Evidence Schema](../templates/conversation_evidence_schema.yaml)

## DevOps Tools

### gl2discord.sh

Send notifications from GitLens to Discord channels.

**Usage:**
```bash
./scripts/gl2discord.sh <channel_id> <title> <description>
```

**Example:**
```bash
export DISCORD_TOKEN="your_token"
./scripts/gl2discord.sh "123456789" "PR Review" "Ready for review"
```

## System Configuration

### configure_sleep_mode.py

Configure system sleep/power management settings.

### run_benchmarks.py

Execute system benchmarks and performance tests.

---

**For more information, see the main [README.md](../README.md)**
