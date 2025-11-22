#!/bin/bash
# Verification script for Gaming Console Infrastructure
# Validates all components are properly configured

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Gaming Console Infrastructure Verification              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

ERRORS=0
WARNINGS=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

echo -e "${YELLOW}Checking Kubernetes manifests...${NC}"

# Check if files exist
REQUIRED_FILES=(
    "bootstrap/k8s/gaming-console-namespace.yaml"
    "bootstrap/k8s/gaming-console-rbac.yaml"
    "bootstrap/k8s/gaming-console-network-policy.yaml"
    "bootstrap/k8s/gaming-console-statefulset.yaml"
    "bootstrap/k8s/playstation-remote-play-deployment.yaml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "File exists: $file"
        
        # Validate YAML syntax
        if python3 -c "import yaml; list(yaml.safe_load_all(open('$file').read()))" 2>/dev/null; then
            check_pass "  YAML syntax valid"
        else
            check_fail "  YAML syntax invalid"
        fi
    else
        check_fail "File missing: $file"
    fi
done

echo ""
echo -e "${YELLOW}Checking deployment scripts...${NC}"

SCRIPTS=(
    "deploy-gaming-consoles.sh"
    "manage-gaming-consoles.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        check_pass "Script exists: $script"
        
        if [ -x "$script" ]; then
            check_pass "  Executable permissions set"
        else
            check_fail "  Missing executable permissions"
        fi
        
        # Check bash syntax
        if bash -n "$script" 2>/dev/null; then
            check_pass "  Bash syntax valid"
        else
            check_fail "  Bash syntax errors"
        fi
    else
        check_fail "Script missing: $script"
    fi
done

echo ""
echo -e "${YELLOW}Checking documentation...${NC}"

DOCS=(
    "GAMING_CONSOLE_INFRASTRUCTURE.md"
    "GAMING_CONSOLE_QUICK_START.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "Documentation exists: $doc"
        
        # Check if file is not empty
        if [ -s "$doc" ]; then
            check_pass "  File has content"
        else
            check_warn "  File is empty"
        fi
    else
        check_fail "Documentation missing: $doc"
    fi
done

echo ""
echo -e "${YELLOW}Verifying Kubernetes manifest content...${NC}"

# Check namespace configuration
if grep -q "gaming-consoles" bootstrap/k8s/gaming-console-namespace.yaml; then
    check_pass "Namespace 'gaming-consoles' configured"
else
    check_fail "Namespace 'gaming-consoles' not found"
fi

# Check for 4 console services
if grep -q "ps5-console-4" bootstrap/k8s/gaming-console-statefulset.yaml; then
    check_pass "All 4 gaming console services defined"
else
    check_fail "Not all 4 console services found"
fi

# Check for scholarly resources
if grep -q "scholarly-resources.txt" bootstrap/k8s/playstation-remote-play-deployment.yaml; then
    check_pass "Scholarly resources ConfigMap defined"
    
    # Count number of resources (should be 36)
    RESOURCE_COUNT=$(grep -E -c "^    [0-9]+\." bootstrap/k8s/playstation-remote-play-deployment.yaml || echo "0")
    if [ "$RESOURCE_COUNT" -ge 36 ]; then
        check_pass "  36+ web resources documented"
    else
        check_warn "  Only $RESOURCE_COUNT resources found (expected 36)"
    fi
else
    check_fail "Scholarly resources not found"
fi

# Check for Remote Play configuration
if grep -q "remoteplay.dl.playstation.net" bootstrap/k8s/playstation-remote-play-deployment.yaml; then
    check_pass "PlayStation Remote Play endpoint configured"
else
    check_warn "PlayStation Remote Play endpoint not found"
fi

# Check network policies
if grep -q "gaming-console-isolation" bootstrap/k8s/gaming-console-network-policy.yaml; then
    check_pass "Closed-loop network policy configured"
else
    check_fail "Network isolation policy not found"
fi

# Check RBAC
if grep -q "gaming-console-operator" bootstrap/k8s/gaming-console-rbac.yaml; then
    check_pass "RBAC service account configured"
else
    check_fail "RBAC service account not found"
fi

echo ""
echo -e "${YELLOW}Checking README integration...${NC}"

if [ -f "README.md" ]; then
    if grep -q "Gaming Console Infrastructure" README.md; then
        check_pass "README.md updated with gaming console section"
    else
        check_warn "Gaming console section not found in README.md"
    fi
else
    check_fail "README.md not found"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Verification Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Gaming Console Infrastructure is ready for deployment!"
    echo ""
    echo "Next steps:"
    echo "  1. Review documentation: cat GAMING_CONSOLE_INFRASTRUCTURE.md"
    echo "  2. Deploy to Kubernetes: ./deploy-gaming-consoles.sh"
    echo "  3. Manage infrastructure: ./manage-gaming-consoles.sh status"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    echo ""
    echo "Gaming Console Infrastructure is mostly ready."
    echo "Review warnings above and proceed if acceptable."
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) and $WARNINGS warning(s) found${NC}"
    echo ""
    echo "Please fix the errors above before deploying."
    exit 1
fi
