# Artifacts Directory

This directory contains archived external AI discussions, design artifacts, and audit trail documentation for the Sovereignty Architecture project.

## Purpose

The `artifacts/` folder serves as an immutable, version-controlled archive for:

1. **External AI Discussions** - Preserved links and summaries from Claude, GPT, and other AI interactions
2. **Design Artifacts** - Key decision documents and architectural discussions
3. **Audit Trail** - Compliance and verification documentation
4. **Meta-Evolution References** - Self-improvement and recursive development artifacts

## Sovereignty Guarantees

All artifacts stored here are:

- ✓ **Fully Local** - Text files you control 100%, no cloud dependencies after initial download
- ✓ **Version Controlled** - Immutable git history with tamper-evident commits
- ✓ **Hash Verifiable** - `git log --format="%H %s" -- artifacts/` shows all changes
- ✓ **Replicated** - Can be synced across all storage nodes (NAS, backup, etc.)
- ✓ **Auditable** - Complete transparency for legal and compliance contexts
- ✓ **No Hidden Clauses** - Plain markdown/JSON, no proprietary formats

## Usage

### Adding a New Artifact

```bash
# Create artifact file
cat > artifacts/discussion_name_$(date +%Y-%m-%d).md << 'EOF'
# Discussion Title

Source: https://example.com/share/link

## Summary
Brief summary of the discussion...

## Metadata
```json
{
  "timestamp": "2025-11-21T00:00:00Z",
  "type": "external_ai_discussion",
  "source": "https://example.com/share/link",
  "summary": "Brief description"
}
```
EOF

# Add to git
git add artifacts/
git commit -m "Add artifact: discussion_name"
```

### Verifying Artifacts

```bash
# Get hash of all artifacts
find artifacts/ -type f -exec sha256sum {} \;

# Check git history
git log --follow -- artifacts/

# Verify no changes since commit
git diff HEAD -- artifacts/
```

### Searching Artifacts

```bash
# Search all artifacts for keywords
grep -r "keyword" artifacts/

# List all artifacts with metadata
find artifacts/ -name "*.md" -exec head -n 5 {} \;
```

## Archive Format

Each artifact should follow this structure:

```markdown
# Title

Source: [URL or reference]

Used as: [purpose - audit trail, training reference, etc.]

## Overview
[Brief description]

## Metadata
```json
{
  "timestamp": "ISO-8601 timestamp",
  "type": "external_ai_discussion|design_artifact|audit_trail",
  "source": "URL or reference",
  "summary": "Brief summary",
  "topics": ["tag1", "tag2"],
  "status": "archived|active|superseded"
}
```

## [Content sections as needed]
```

## Integration with Verification Tools

The sovereignty verification scripts (`scripts/verify-repo-sovereignty.ps1` and `scripts/verify_repo_sovereignty.py`) check for the presence of this directory and report on artifact archiving compliance.

Run verification:

```bash
# PowerShell
./scripts/verify-repo-sovereignty.ps1 -GenerateReport

# Python
python3 scripts/verify_repo_sovereignty.py --generate-report
```

## Legal Context

These artifacts serve as documentation for:
- Design decisions made during development
- Audit trail for compliance verification
- Training references for future AI agents
- Meta-evolution for recursive improvement
- Legal discovery and IP documentation

All artifacts are preserved under the same MIT License as the repository, ensuring full sovereign control and transparency.

---

*Part of the Sovereignty Architecture commitment to transparent, auditable, and fully sovereign artifact preservation.*
