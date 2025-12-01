# Tools Directory

This directory contains utility scripts for managing the Sovereignty Architecture ecosystem.

## append_artifact.py

A tool for appending external AI discussions and artifacts to JSONL ledgers for tamper-evident tracking, RAG integration, and audit trails.

### Usage

Basic usage:
```bash
python append_artifact.py <source_url> <summary...>
```

With optional parameters:
```bash
python append_artifact.py <source_url> <summary...> \
  --notes "<additional context>" \
  --type "<artifact_type>" \
  --ledger "<path_to_ledger>"
```

### Examples

**Example 1: Add a Claude AI discussion**
```bash
python append_artifact.py \
  "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56" \
  "Design of meta-evolution and legal compliance synthesizer engine." \
  --notes "Used as upstream design context for NHES and LSEE implementations."
```

**Example 2: Add a ChatGPT conversation**
```bash
python append_artifact.py \
  "https://chat.openai.com/share/abc123" \
  "Discussion of distributed consensus mechanisms for DAO governance."
```

**Example 3: Add to a specific ledger**
```bash
python append_artifact.py \
  "https://claude.ai/share/xyz789" \
  "Legal compliance framework design." \
  --ledger "legal_evolution_ledger.jsonl" \
  --type "legal_design_discussion"
```

### Parameters

- `<source_url>` (required): URL or path to the external artifact
- `<summary...>` (required): Brief description of the artifact content
- `--notes <notes>`: Optional additional notes about usage or context
- `--type <type>`: Artifact type (default: `external_ai_discussion`)
- `--ledger <path>`: Path to ledger file (default: `external_artifacts.jsonl`)

### Output Format

The script appends a JSONL entry with the following structure:

```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "type": "external_ai_discussion",
  "source": "https://example.com/artifact",
  "summary": "Brief description of content",
  "notes": "Optional usage context"
}
```

### Integration with Evolution Engines

External artifacts can be referenced in evolution ledgers:

```json
{
  "generation": 5,
  "timestamp": "2025-11-21T04:00:00Z",
  "external_artifacts": [
    "https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56"
  ],
  "changes": ["Implemented NHES based on external design discussion"]
}
```

### Benefits

- **Machine-readable**: JSONL format for easy parsing and RAG integration
- **Tamper-evident**: Git-tracked for audit trails
- **Versioned**: Full history of when artifacts were added
- **Searchable**: Easily query by timestamp, type, or source
- **Compliant**: Supports compliance and legal audit requirements
