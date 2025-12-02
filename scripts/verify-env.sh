#!/bin/bash
# Environment Verification Script
#
# Verifies that all required environment variables and configurations
# are properly set for the Sovereignty Architecture.
#
# LLM Directive: Extend this script to:
# - Add new required variables
# - Test connectivity to services
# - Validate secret formats

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo "🔍 Verifying Sovereignty Architecture Environment"
echo "=================================================="
echo ""

# Function to check required variable
check_required() {
    local var_name="$1"
    local var_value="${!var_name:-}"
    
    if [[ -z "$var_value" ]]; then
        echo -e "${RED}❌ Missing required: ${var_name}${NC}"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ Set: ${var_name}${NC}"
        return 0
    fi
}

# Function to check optional variable
check_optional() {
    local var_name="$1"
    local var_value="${!var_name:-}"
    
    if [[ -z "$var_value" ]]; then
        echo -e "${YELLOW}⚠️  Not set (optional): ${var_name}${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✅ Set: ${var_name}${NC}"
    fi
}

# Function to check file exists
check_file() {
    local file_path="$1"
    local description="$2"
    
    if [[ -f "$file_path" ]]; then
        echo -e "${GREEN}✅ Found: ${description} (${file_path})${NC}"
        return 0
    else
        echo -e "${RED}❌ Missing: ${description} (${file_path})${NC}"
        ((ERRORS++))
        return 1
    fi
}

echo "📌 Required Environment Variables"
echo "----------------------------------"
check_required "DISCORD_BOT_TOKEN" || true
check_required "DISCORD_GUILD_ID" || check_optional "DISCORD_GUILD_ID"

echo ""
echo "📌 Channel IDs"
echo "--------------"
check_optional "PRS_CHANNEL_ID"
check_optional "DEPLOYMENTS_CHANNEL_ID"
check_optional "ALERTS_CHANNEL_ID"
check_optional "CLUSTER_STATUS_CHANNEL_ID"

echo ""
echo "📌 GitHub Integration"
echo "---------------------"
check_optional "GITHUB_WEBHOOK_SECRET"
check_optional "GITHUB_TOKEN"
check_optional "GITHUB_APP_ID"

echo ""
echo "📌 API Keys"
echo "-----------"
check_optional "OPENAI_API_KEY"
check_optional "ANTHROPIC_API_KEY"

echo ""
echo "📌 Infrastructure"
echo "-----------------"
check_optional "CONTROL_API_URL"
check_optional "CTRL_API_TOKEN"
check_optional "EVENTS_HMAC_KEY"

echo ""
echo "📌 Configuration Files"
echo "----------------------"
check_file "discovery.yml" "Discovery configuration"
check_file "docker-compose.yml" "Docker Compose configuration" || true

echo ""
echo "📌 Tools"
echo "--------"

# Check kubectl
if command -v kubectl &> /dev/null; then
    echo -e "${GREEN}✅ kubectl installed${NC}"
else
    echo -e "${YELLOW}⚠️  kubectl not found${NC}"
    ((WARNINGS++))
fi

# Check docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ docker installed${NC}"
else
    echo -e "${YELLOW}⚠️  docker not found${NC}"
    ((WARNINGS++))
fi

# Check jq
if command -v jq &> /dev/null; then
    echo -e "${GREEN}✅ jq installed${NC}"
else
    echo -e "${YELLOW}⚠️  jq not found${NC}"
    ((WARNINGS++))
fi

# Check curl
if command -v curl &> /dev/null; then
    echo -e "${GREEN}✅ curl installed${NC}"
else
    echo -e "${RED}❌ curl not found (required)${NC}"
    ((ERRORS++))
fi

echo ""
echo "=================================================="
echo "Summary: ${ERRORS} errors, ${WARNINGS} warnings"

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}Environment verification failed!${NC}"
    exit 1
else
    echo -e "${GREEN}Environment verification passed!${NC}"
    exit 0
fi
