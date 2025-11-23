#!/bin/bash
# Pre-commit hook to check for exposed secrets and API keys
# Install: ln -s ../../hooks/check_secrets.sh .git/hooks/pre-commit

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🔍 Scanning for exposed secrets..."

# Check if gitleaks is available
GITLEAKS_AVAILABLE=false
if command -v gitleaks &> /dev/null; then
    GITLEAKS_AVAILABLE=true
fi

# Patterns to search for
PATTERNS=(
    "xai-[a-zA-Z0-9]{32,}"
    "sk-[a-zA-Z0-9]{32,}"
    "claude-[a-zA-Z0-9]{32,}"
    "AKIA[0-9A-Z]{16}"
    "api[_-]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{20,}"
    "token['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{20,}"
    "secret['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{20,}"
    "password['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{8,}"
)

# Files to always exclude
EXCLUDE_PATTERNS=(
    "*.md"
    "*.example"
    ".gitignore"
    "package-lock.json"
    "yarn.lock"
)

# Check staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✅ No files staged for commit${NC}"
    exit 0
fi

# Build exclude pattern array for grep
EXCLUDE_ARGS=()
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    EXCLUDE_ARGS+=("--exclude=$pattern")
done

FOUND_SECRETS=false

# Quick pattern-based check on staged files
for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        # Check for common secret patterns
        for pattern in "${PATTERNS[@]}"; do
            if grep -E "$pattern" "$file" "${EXCLUDE_ARGS[@]}" &> /dev/null; then
                echo -e "${RED}⚠️  Potential secret found in: $file${NC}"
                echo -e "${YELLOW}Pattern: $pattern${NC}"
                FOUND_SECRETS=true
            fi
        done
        
        # Check for .env files (should never be committed)
        if [[ "$file" == ".env" ]] || [[ "$file" == *".env.local"* ]]; then
            echo -e "${RED}🚨 CRITICAL: Attempting to commit .env file: $file${NC}"
            echo -e "${YELLOW}This file should be in .gitignore!${NC}"
            FOUND_SECRETS=true
        fi
        
        # Check for API key files
        if [[ "$file" == *"api"*"key"* ]] || [[ "$file" == *"apikey"* ]] || [[ "$file" == *.key ]]; then
            echo -e "${RED}⚠️  API key file detected: $file${NC}"
            FOUND_SECRETS=true
        fi
    fi
done

# Run gitleaks if available (more thorough check)
if [ "$GITLEAKS_AVAILABLE" = true ]; then
    echo "🔐 Running gitleaks scan..."
    GITLEAKS_OUTPUT=$(gitleaks protect --staged --verbose --no-banner 2>&1) || GITLEAKS_EXIT=$?
    if [ ${GITLEAKS_EXIT:-0} -ne 0 ]; then
        echo -e "${RED}🚨 Gitleaks detected secrets!${NC}"
        echo "$GITLEAKS_OUTPUT"
        FOUND_SECRETS=true
    fi
fi

# Final decision
if [ "$FOUND_SECRETS" = true ]; then
    echo ""
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    echo -e "${RED}🚨 COMMIT BLOCKED: Potential secrets detected!${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}What to do:${NC}"
    echo "1. Remove the secret from the file"
    echo "2. Store it in .env or password manager"
    echo "3. Add the file to .gitignore if needed"
    echo "4. Review API_KEY_SECURITY.md for guidance"
    echo ""
    echo -e "${YELLOW}To bypass this check (NOT RECOMMENDED):${NC}"
    echo "git commit --no-verify"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ No secrets detected - commit allowed${NC}"
exit 0
