#!/bin/bash
# Security setup script for Sovereignty Architecture
# Installs pre-commit hooks and validates security configuration

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Sovereignty Architecture - Security Setup                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    echo "Please run this script from the repository root"
    exit 1
fi

# Step 1: Install pre-commit hook
echo -e "${YELLOW}[1/5]${NC} Installing pre-commit hook for secret scanning..."
if [ -f .git/hooks/pre-commit ]; then
    echo -e "${YELLOW}⚠️  Pre-commit hook already exists${NC}"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ln -sf ../../hooks/check_secrets.sh .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
        echo -e "${GREEN}✅ Pre-commit hook installed${NC}"
    else
        echo -e "${YELLOW}⏭️  Skipped${NC}"
    fi
else
    ln -sf ../../hooks/check_secrets.sh .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}✅ Pre-commit hook installed${NC}"
fi

# Step 2: Check for .env file
echo ""
echo -e "${YELLOW}[2/5]${NC} Checking environment configuration..."
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    read -p "Create from .env.example? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env from template${NC}"
        echo -e "${YELLOW}📝 Remember to add your real API keys to .env${NC}"
    else
        echo -e "${YELLOW}⏭️  Skipped${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Step 3: Verify .env is in .gitignore
echo ""
echo -e "${YELLOW}[3/5]${NC} Verifying .env is excluded from git..."
if grep -q "^\.env$" .gitignore; then
    echo -e "${GREEN}✅ .env is in .gitignore${NC}"
else
    echo -e "${RED}❌ .env is NOT in .gitignore${NC}"
    echo -e "${YELLOW}Adding .env to .gitignore...${NC}"
    echo ".env" >> .gitignore
    echo -e "${GREEN}✅ Added .env to .gitignore${NC}"
fi

# Step 4: Check for gitleaks
echo ""
echo -e "${YELLOW}[4/5]${NC} Checking for gitleaks (enhanced secret scanning)..."
if command -v gitleaks &> /dev/null; then
    echo -e "${GREEN}✅ gitleaks is installed${NC}"
    GITLEAKS_VERSION=$(gitleaks version 2>&1 | head -1)
    echo -e "   Version: ${GITLEAKS_VERSION}"
else
    echo -e "${YELLOW}⚠️  gitleaks not found (optional but recommended)${NC}"
    echo ""
    echo "Install gitleaks for enhanced secret detection:"
    echo ""
    echo "  macOS:"
    echo "    brew install gitleaks"
    echo ""
    echo "  Linux:"
    echo "    wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_amd64.tar.gz"
    echo "    tar -xzf gitleaks_linux_amd64.tar.gz"
    echo "    sudo mv gitleaks /usr/local/bin/"
    echo ""
fi

# Step 5: Scan for existing secrets
echo ""
echo -e "${YELLOW}[5/5]${NC} Scanning repository for exposed secrets..."
echo -e "${BLUE}Running pattern-based scan...${NC}"

# Simple pattern scan
FOUND_ISSUES=false

# Check for common secret patterns in tracked files
if git ls-files | xargs grep -l -E "(xai-[a-zA-Z0-9]{32,}|sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16})" 2>/dev/null; then
    echo -e "${RED}⚠️  Potential secrets found in tracked files!${NC}"
    FOUND_ISSUES=true
fi

# Check if .env is accidentally tracked
if git ls-files | grep -q "^\.env$"; then
    echo -e "${RED}🚨 CRITICAL: .env file is tracked in git!${NC}"
    echo "To remove it:"
    echo "  git rm --cached .env"
    echo "  git commit -m 'Remove .env from version control'"
    FOUND_ISSUES=true
fi

if [ "$FOUND_ISSUES" = false ]; then
    echo -e "${GREEN}✅ No obvious secrets found in tracked files${NC}"
fi

# Run gitleaks if available
if command -v gitleaks &> /dev/null; then
    echo ""
    echo -e "${BLUE}Running gitleaks scan...${NC}"
    if gitleaks detect --no-banner --no-git 2>&1 | grep -q "No leaks found"; then
        echo -e "${GREEN}✅ Gitleaks: No secrets detected${NC}"
    else
        echo -e "${YELLOW}⚠️  Gitleaks found potential issues - review output above${NC}"
    fi
fi

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Security Setup Complete!                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Add your API keys to .env (never commit this file!)"
echo "2. Store backup keys in password manager (Bitwarden/1Password)"
echo "3. Review security documentation:"
echo "   - API_KEY_SECURITY.md - Comprehensive guide"
echo "   - EMERGENCY_API_KEY_EXPOSURE.md - Emergency procedures"
echo "   - SECURITY.md - Security policy"
echo ""
echo -e "${YELLOW}Testing the pre-commit hook:${NC}"
echo "Try committing a file with 'xai-test123456' in it - it should be blocked!"
echo ""
echo -e "${GREEN}🔐 Your repository is now protected against accidental secret exposure!${NC}"
echo ""
