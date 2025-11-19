#!/usr/bin/env bash
# Pre-commit hook to detect and prevent accidental exposure of local file paths
# This hook scans staged files for common patterns that might expose user-specific paths

set -euo pipefail

# ANSI color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Patterns that indicate local paths (case-insensitive)
# These are intentionally broad to catch potential issues
SUSPICIOUS_PATTERNS=(
    'C:\\Users\\[^/\\]*\\(Downloads|Documents|Desktop)'
    '/Users/[^/]+/(Downloads|Documents|Desktop)'
    '/home/[^/]+/(Downloads|Documents|Desktop)'
    'C:\\Users\\[^/\\]*\\AppData'
)

# Files to scan (only text files)
FILES_TO_CHECK=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|txt|yaml|yml|json|sh|py|js|ts|env|conf|config|toml)$' || true)

if [ -z "$FILES_TO_CHECK" ]; then
    echo -e "${GREEN}✓${NC} No text files to check for local paths"
    exit 0
fi

echo "🔍 Scanning staged files for local file paths..."

ISSUES_FOUND=0

while IFS= read -r file; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
        # Use grep with Perl-compatible regex for better pattern matching
        if grep -qiP "$pattern" "$file" 2>/dev/null; then
            if [ $ISSUES_FOUND -eq 0 ]; then
                echo -e "${RED}⚠️  WARNING: Potential local file paths detected!${NC}"
                echo ""
            fi
            
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
            
            echo -e "${YELLOW}File:${NC} $file"
            echo -e "${YELLOW}Pattern:${NC} $pattern"
            
            # Show the matching lines (with line numbers)
            grep -niP "$pattern" "$file" | while IFS= read -r match; do
                echo -e "  ${RED}→${NC} $match"
            done
            echo ""
        fi
    done
done <<< "$FILES_TO_CHECK"

if [ $ISSUES_FOUND -gt 0 ]; then
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}COMMIT BLOCKED${NC}"
    echo ""
    echo "Found $ISSUES_FOUND potential local file path(s) in staged files."
    echo ""
    echo "Local file paths can expose:"
    echo "  • Your operating system username"
    echo "  • Your computer's file structure"
    echo "  • Potentially sensitive information"
    echo ""
    echo "Please:"
    echo "  1. Replace user-specific paths with generic placeholders"
    echo "  2. Use environment variables or relative paths instead"
    echo "  3. Review SECURITY_GUIDELINES.md for best practices"
    echo ""
    echo "Examples of safe alternatives:"
    echo "  ❌ C:\\Users\\john\\Downloads\\project"
    echo "  ✅ C:\\projects\\project-name"
    echo "  ✅ \$PROJECT_ROOT or ./relative-path"
    echo ""
    echo "To bypass this check (only if you're certain):"
    echo "  git commit --no-verify"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} No local file paths detected in staged files"
exit 0
