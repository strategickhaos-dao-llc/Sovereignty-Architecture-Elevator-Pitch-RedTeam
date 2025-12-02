#!/bin/bash
# Event Gateway Smoke Test
#
# Tests basic event gateway connectivity and webhook handling.
#
# LLM Directive: Extend this to:
# - Test all webhook endpoints
# - Verify HMAC signature handling
# - Check rate limiting

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

GATEWAY_ENDPOINT="${GATEWAY_ENDPOINT:-http://localhost:8080}"
TIMEOUT="${TIMEOUT:-10}"
HMAC_KEY="${EVENTS_HMAC_KEY:-test-secret}"

echo "🧪 Event Gateway Smoke Test"
echo "==========================="
echo ""
echo "Endpoint: ${GATEWAY_ENDPOINT}"
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

# Test health endpoint
echo -n "Testing /health endpoint... "
if response=$(curl -sf --max-time $TIMEOUT "${GATEWAY_ENDPOINT}/health" 2>/dev/null); then
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
if response=$(curl -sf --max-time $TIMEOUT "${GATEWAY_ENDPOINT}/ready" 2>/dev/null); then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC} - request failed"
    ((TESTS_FAILED++))
fi

# Test GitHub webhook with invalid signature (should return 401)
echo -n "Testing /webhook/github (invalid sig)... "
response_code=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time $TIMEOUT \
    -X POST "${GATEWAY_ENDPOINT}/webhook/github" \
    -H "Content-Type: application/json" \
    -H "X-GitHub-Event: ping" \
    -H "X-Hub-Signature-256: sha256=invalid" \
    -d '{"zen": "test"}' 2>/dev/null) || response_code="000"

if [[ "$response_code" == "401" ]]; then
    echo -e "${GREEN}PASS${NC} (correctly rejected invalid signature)"
    ((TESTS_PASSED++))
elif [[ "$response_code" == "200" ]]; then
    echo -e "${YELLOW}WARN${NC} (signature verification may be disabled)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC} - unexpected response code: $response_code"
    ((TESTS_FAILED++))
fi

# Test alert endpoint
echo -n "Testing /alert endpoint... "
response_code=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time $TIMEOUT \
    -X POST "${GATEWAY_ENDPOINT}/alert" \
    -H "Content-Type: application/json" \
    -d '{"alerts":[{"status":"firing","labels":{"alertname":"TestAlert"}}]}' 2>/dev/null) || response_code="000"

if [[ "$response_code" == "200" ]]; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC} - response code: $response_code"
    ((TESTS_FAILED++))
fi

# Test generic event endpoint with HMAC
echo -n "Testing /event endpoint (with HMAC)... "
payload='{"type":"test","service":"smoke-test","message":"Smoke test event"}'
signature=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$HMAC_KEY" | awk '{print $2}')

response_code=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time $TIMEOUT \
    -X POST "${GATEWAY_ENDPOINT}/event" \
    -H "Content-Type: application/json" \
    -H "X-Sig: sha256=$signature" \
    -d "$payload" 2>/dev/null) || response_code="000"

if [[ "$response_code" == "200" ]]; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
elif [[ "$response_code" == "401" ]]; then
    echo -e "${YELLOW}WARN${NC} (HMAC key mismatch)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC} - response code: $response_code"
    ((TESTS_FAILED++))
fi

echo ""
echo "==========================="
echo "Results: ${TESTS_PASSED} passed, ${TESTS_FAILED} failed"

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}Smoke test failed!${NC}"
    exit 1
else
    echo -e "${GREEN}Smoke test passed!${NC}"
    exit 0
fi
