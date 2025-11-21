#!/bin/bash
#
# Archive External AI Artifact
#
# Usage: ./archive_artifact.sh <URL> <description>
# Example: ./archive_artifact.sh "https://claude.ai/share/xxx" "Meta-evolution discussion"
#

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <URL> <description>"
    echo "Example: $0 'https://claude.ai/share/xxx' 'Meta-evolution discussion'"
    exit 1
fi

URL="$1"
DESCRIPTION="$2"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Create artifacts directory if it doesn't exist
mkdir -p artifacts

# Generate filename from description
FILENAME=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd '[:alnum:]_-')
FILEPATH="artifacts/${FILENAME}_${DATE}.md"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo "⚠️  Warning: $FILEPATH already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create artifact file
cat > "$FILEPATH" << EOF
# ${DESCRIPTION} — ${DATE}

Source: ${URL}

Used as: audit trail, agent training reference, meta-evolution artifact

\`\`\`json
{
  "timestamp": "${TIMESTAMP}",
  "type": "external_ai_discussion",
  "source": "${URL}",
  "summary": "${DESCRIPTION}"
}
\`\`\`

## Context

This artifact archives an external AI discussion that contributed to the design and implementation of the Sovereignty Architecture.

## Purpose

- **Audit Trail**: Provides immutable evidence of design decisions and evolution
- **Agent Training Reference**: Can be used for training and context in AI systems
- **Meta-Evolution Artifact**: Documents the recursive improvement process

## Verification

To verify this artifact hasn't been tampered with:

\`\`\`bash
# Bash
sha256sum "${FILEPATH}"

# PowerShell
Get-FileHash "${FILEPATH}" -Algorithm SHA256
\`\`\`

## Sovereignty Guarantee

This file is:
- ✅ Fully local and under version control
- ✅ No hidden clauses or cloud TOS dependencies
- ✅ Auditable and provable in any legal/compliance context
- ✅ Can be deleted or modified at any time (you own it 100%)
- ✅ Immutable once committed to git history
EOF

echo "✅ Created: $FILEPATH"

# Calculate hash
HASH=$(sha256sum "$FILEPATH" | awk '{print $1}')
echo "📝 SHA256: $HASH"

# Append to verification ledger if it exists
if [ -f "verification_ledger.jsonl" ]; then
    echo "{\"timestamp\":\"${TIMESTAMP}\",\"type\":\"artifact_archived\",\"path\":\"${FILEPATH}\",\"source\":\"${URL}\",\"hash\":\"sha256:${HASH}\",\"action\":\"created\",\"actor\":\"manual\"}" >> verification_ledger.jsonl
    echo "📋 Appended to verification_ledger.jsonl"
fi

# Commit to git if in a git repo
if [ -d .git ]; then
    git add "$FILEPATH"
    
    # Also add ledger if it was updated
    if [ -f "verification_ledger.jsonl" ]; then
        git add verification_ledger.jsonl
    fi
    
    git commit -m "Archive artifact: ${DESCRIPTION}" || true
    echo "✅ Committed to git"
fi

echo ""
echo "🎉 Artifact archived successfully!"
echo "Location: $FILEPATH"
echo "Next steps:"
echo "  1. Review the artifact: cat $FILEPATH"
echo "  2. Push to remote: git push"
echo "  3. Verify integrity: sha256sum $FILEPATH"
