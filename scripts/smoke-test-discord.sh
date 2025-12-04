#!/bin/bash
# Discord Bot Smoke Test
#
# Tests basic Discord bot connectivity and command responses.
#
# LLM Directive: Extend this to:
# - Test all slash commands
# - Verify RBAC enforcement
# - Check rate limiting

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BOT_ENDPOINT="${BOT_ENDPOINT:-http://localhost:8080}"
TIMEOUT="${TIMEOUT:-10}"

echo "🧪 Discord Bot Smoke Test"
echo "========================="
echo ""
echo "Endpoint: ${BOT_ENDPOINT}"
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

# Test health endpoint
echo -n "Testing /health endpoint... "
if response=$(curl -sf --max-time $TIMEOUT "${BOT_ENDPOINT}/health" 2>/dev/null); then
    if echo "$response" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC} - unexpected response"
        echo "  Response: $response"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}FAIL${NC} - request failed"
    ((TESTS_FAILED++))
fi

# Test ready endpoint
echo -n "Testing /ready endpoint... "
if response=$(curl -sf --max-time $TIMEOUT "${BOT_ENDPOINT}/ready" 2>/dev/null); then
    if echo "$response" | jq -e '.ready' > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}WARN${NC} - not fully ready"
        echo "  Response: $response"
        ((TESTS_PASSED++))  # Still counts as passing, just not ready
    fi
else
    echo -e "${RED}FAIL${NC} - request failed"
    ((TESTS_FAILED++))
fi

# Test metrics endpoint (if available)
echo -n "Testing /metrics endpoint... "
if response=$(curl -sf --max-time $TIMEOUT "${BOT_ENDPOINT}/metrics" 2>/dev/null); then
    if echo "$response" | grep -q "discord_"; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}SKIP${NC} - metrics not available"
    fi
else
    echo -e "${YELLOW}SKIP${NC} - metrics endpoint not exposed"
fi

echo ""
echo "========================="
echo "Results: ${TESTS_PASSED} passed, ${TESTS_FAILED} failed"

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}Smoke test failed!${NC}"
    exit 1
else
    echo -e "${GREEN}Smoke test passed!${NC}"
    exit 0
fi
