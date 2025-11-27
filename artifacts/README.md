# External AI Artifacts

This directory contains archived external AI discussion links and artifacts used in the development and evolution of this repository.

## Purpose

- **Audit Trail**: Provides evidence of design decisions and evolution
- **Agent Training References**: Can be used for training and context in AI systems
- **Meta-Evolution Documentation**: Documents the recursive improvement process
- **Immutable Proof**: External contributions archived under version control

## Current Artifacts

- `claude_meta_evolution_2025-11-21.md` - Design discussion for meta-evolution and legal synthesizer engine

## Adding New Artifacts

### Manual Method

Create a markdown file with date suffix:

```bash
# Create artifact file
cat > artifacts/my_artifact_$(date +%Y-%m-%d).md << 'EOF'
# My Artifact — $(date +%Y-%m-%d)

Source: https://example.com/discussion

```json
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "type": "external_ai_discussion",
  "source": "https://example.com/discussion",
  "summary": "Brief description"
}
```
EOF

# Commit it
git add artifacts/
git commit -m "Archive new artifact"
```

### Using Archive Script

```bash
# Use the helper script
./scripts/archive_artifact.sh "https://example.com/url" "Description of artifact"
```

## Verification

All artifacts are under version control and can be verified with:

```bash
# Linux/Mac
sha256sum artifacts/*.md

# PowerShell
Get-FileHash artifacts/*.md -Algorithm SHA256

# Git history
git log artifacts/

# View specific artifact history
git log -p artifacts/claude_meta_evolution_2025-11-21.md
```

## Sovereignty Guarantees

✅ **Fully Local**: All files stored locally under your control  
✅ **No Cloud Dependencies**: No external services required  
✅ **Version Controlled**: Every change tracked in git history  
✅ **Tamper-Evident**: Any modification visible in git diff  
✅ **Auditable**: Can be verified cryptographically  
✅ **Deletable**: You own these files 100% - remove anytime  

## Integration with Verification System

Artifacts are automatically checked by the sovereignty verification system:

```bash
# Run verification
python scripts/verify_repository_sovereignty.py

# Check this repo and append to ledger
python scripts/verify_repository_sovereignty.py --append-ledger
```

## Ledger Tracking

Each artifact archive is recorded in `verification_ledger.jsonl`:

```json
{
  "timestamp": "2025-11-21T03:15:19Z",
  "type": "artifact_archived",
  "path": "artifacts/artifact_name.md",
  "source": "https://...",
  "hash": "sha256:...",
  "action": "created",
  "actor": "manual|sovereignty-verification-system"
}
```

## Best Practices

1. **Include Source URL**: Always link to original discussion
2. **Add JSON Metadata**: Structured data for programmatic access
3. **Use Descriptive Names**: Make filenames searchable
4. **Include Date**: Use YYYY-MM-DD format for chronological sorting
5. **Commit Immediately**: Don't leave artifacts uncommitted
6. **Verify Hashes**: Check SHA256 after archiving

## Example Artifact Structure

```markdown
# Discussion Topic — 2025-11-21

Source: https://claude.ai/share/abc123

Used as: audit trail, design reference, training data

```json
{
  "timestamp": "2025-11-21T10:30:00Z",
  "type": "external_ai_discussion",
  "source": "https://claude.ai/share/abc123",
  "summary": "Discussion about X feature implementation"
}
```

## Context

Detailed description of what this artifact represents...

## Sovereignty Guarantee

Standard sovereignty guarantees section...
```

---

*Part of Sovereignty Architecture Verification System*  
*See SOVEREIGNTY_VERIFICATION.md for complete documentation*
