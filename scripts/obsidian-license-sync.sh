#!/bin/bash
# Obsidian License Sync Script
# Syncs license information from this repository to an Obsidian vault

set -e

# Configuration (update these paths)
REPO_PATH="${REPO_PATH:-$(pwd)}"
VAULT_PATH="${VAULT_PATH:-$HOME/ObsidianVault}"
LICENSE_NOTE="${LICENSE_NOTE:-$VAULT_PATH/Project-License.md}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Syncing License Information to Obsidian${NC}"
echo "=================================================="

# Verify repository path
if [[ ! -d "$REPO_PATH/.git" ]]; then
    echo -e "${RED}❌ Error: Not a git repository: $REPO_PATH${NC}"
    echo "Set REPO_PATH environment variable to the repository directory"
    exit 1
fi

# Verify LICENSE file exists
if [[ ! -f "$REPO_PATH/LICENSE" ]]; then
    echo -e "${RED}❌ Error: LICENSE file not found in $REPO_PATH${NC}"
    exit 1
fi

# Create vault directory if it doesn't exist
if [[ ! -d "$VAULT_PATH" ]]; then
    echo -e "${YELLOW}⚠️  Vault directory doesn't exist: $VAULT_PATH${NC}"
    echo -e "${BLUE}Creating vault directory...${NC}"
    mkdir -p "$VAULT_PATH"
fi

# Pull latest changes
echo -e "${BLUE}📥 Pulling latest changes from repository...${NC}"
cd "$REPO_PATH"
git pull origin main --quiet || {
    echo -e "${YELLOW}⚠️  Warning: Could not pull latest changes${NC}"
}

# Extract license information
LICENSE_TEXT=$(cat "$REPO_PATH/LICENSE")
COPYRIGHT_LINE=$(grep -i "Copyright" "$REPO_PATH/LICENSE" | head -1)
LICENSE_TYPE=$(grep -i "MIT\|Apache\|GPL\|BSD" "$REPO_PATH/LICENSE" | head -1 || echo "MIT License")

# Get repository information
REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
LAST_UPDATED=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_SHA=$(git rev-parse HEAD)
COMMIT_SHORT=$(git rev-parse --short HEAD)

# Create Obsidian note with license information
cat > "$LICENSE_NOTE" << EOF
# Project License Information

## Quick Reference

- **License Type**: ${LICENSE_TYPE}
- **Copyright**: ${COPYRIGHT_LINE}
- **Repository**: [${REPO_URL}](${REPO_URL})
- **Last Updated**: ${LAST_UPDATED}
- **Commit**: [\`${COMMIT_SHORT}\`](${REPO_URL}/commit/${COMMIT_SHA})

## Copyright Notice

${COPYRIGHT_LINE}

## Full License Text

\`\`\`text
${LICENSE_TEXT}
\`\`\`

## Usage Guidelines

### For Contributors

When contributing to this project, ensure that:
- All new code files include the appropriate copyright header
- Third-party dependencies are compatible with this license
- Any copied code or resources are properly attributed

### For Users

You are free to:
- ✅ Use the software for any purpose
- ✅ Modify the software
- ✅ Distribute the software
- ✅ Distribute modifications

You must:
- 📋 Include the original copyright notice
- 📋 Include the license text
- 📋 State any changes made

### Copyright Header Template

For new code files, use this header:

\`\`\`
/*
 * ${COPYRIGHT_LINE}
 * 
 * ${LICENSE_TYPE}
 * See LICENSE file in the project root for full license text.
 */
\`\`\`

## Related Documentation

- [[CONTRIBUTORS]] - Project contributors
- [[COMMUNITY]] - Community guidelines
- [[README]] - Project overview

## Automation

This note is automatically synced from the repository.

- **Sync Script**: \`scripts/obsidian-license-sync.sh\`
- **Workflow**: \`.github/workflows/auto-update-license.yml\`
- **Documentation**: [[LICENSE_AUTOMATION]]

---

*Auto-synced from: ${REPO_URL}*  
*Script: obsidian-license-sync.sh*
EOF

echo -e "${GREEN}✅ License information synced to: ${LICENSE_NOTE}${NC}"

# Create automation documentation if it doesn't exist
AUTOMATION_NOTE="$VAULT_PATH/LICENSE_AUTOMATION.md"
if [[ ! -f "$AUTOMATION_NOTE" && -f "$REPO_PATH/LICENSE_AUTOMATION.md" ]]; then
    echo -e "${BLUE}📄 Creating automation documentation note...${NC}"
    cp "$REPO_PATH/LICENSE_AUTOMATION.md" "$AUTOMATION_NOTE"
    echo -e "${GREEN}✅ Created: ${AUTOMATION_NOTE}${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}🎉 Sync Complete!${NC}"
echo "=================================================="
echo -e "License Type:     ${LICENSE_TYPE}"
echo -e "Copyright:        ${COPYRIGHT_LINE}"
echo -e "Vault Location:   ${VAULT_PATH}"
echo -e "Note Created:     ${LICENSE_NOTE}"
echo ""
echo -e "${BLUE}💡 Tip: Add this script to cron for automatic syncing:${NC}"
echo -e "   ${YELLOW}0 * * * * $0${NC}"
echo ""
