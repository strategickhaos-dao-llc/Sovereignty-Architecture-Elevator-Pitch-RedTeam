# Tools Directory

This directory contains utility scripts for managing the Sovereignty Architecture ecosystem.

## append_artifact.py

A tool for tracking external AI discussions and artifacts as first-class entities in the system.

### Purpose

This script appends entries to a JSONL ledger file (`external_artifacts.jsonl`) that tracks:
- External AI conversations (e.g., Claude, ChatGPT)
- Design discussions
- Compliance artifacts
- Any external resources that influenced system design

### Usage

```bash
# Basic usage
python append_artifact.py <source_url> <summary...>

# Example: Adding a Claude discussion
python append_artifact.py \
  "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56" \
  "Design of meta-evolution and legal compliance synthesizer engine."
```

### JSONL Entry Format

Each entry in the ledger follows this structure:

```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "type": "external_ai_discussion",
  "source": "https://claude.ai/share/...",
  "summary": "Brief description of the artifact",
  "notes": "Optional additional context or usage information"
}
```

The `notes` field is optional and can be added manually to entries when additional context is needed.

### Integration with Evolution Engines

These artifacts can serve as:
- **Seed DNA** for Neural Heir Evolution System (NHES)
- **Design evidence** for Legal Strategy Evolution Engine (LSEE)
- **Training material** for future AI agents
- **Audit trail** for design decisions

### Template Files

See `templates/external_ai_discussion_template.md` for creating human-readable notes that complement the machine-readable ledger entries.

See `templates/external_ai_discussion_example.md` for a concrete example.

### Default Ledger Location

By default, artifacts are appended to `external_artifacts.jsonl` in the repository root. This can be changed by modifying the `DEFAULT_LEDGER` constant in the script or passing a custom path.
