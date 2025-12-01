#!/usr/bin/env bash
# Test script for GitLens to Mind OS distribution system
set -euo pipefail

echo "🧪 Testing GitLens to Mind OS Distribution System"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
GITLENS_URL="${GITLENS_URL:-http://localhost:8086}"
MINDOS_URL="${MINDOS_URL:-http://localhost:8090}"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
test_passed() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

test_failed() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
}

test_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: GitLens Aggregator Health Check
echo ""
echo "Test 1: GitLens Aggregator Health Check"
echo "----------------------------------------"
if curl -f -s "${GITLENS_URL}/health" > /dev/null 2>&1; then
    test_passed "GitLens Aggregator is healthy"
else
    test_failed "GitLens Aggregator health check failed"
fi

# Test 2: Mind OS Orchestrator Health Check
echo ""
echo "Test 2: Mind OS Orchestrator Health Check"
echo "------------------------------------------"
if curl -f -s "${MINDOS_URL}/health" > /dev/null 2>&1; then
    test_passed "Mind OS Orchestrator is healthy"
else
    test_failed "Mind OS Orchestrator health check failed"
fi

# Test 3: Mind OS Status Check
echo ""
echo "Test 3: Mind OS Status Check"
echo "-----------------------------"
STATUS=$(curl -s "${MINDOS_URL}/status" 2>/dev/null || echo "{}")
if echo "$STATUS" | grep -q "total_generals"; then
    TOTAL_GENERALS=$(echo "$STATUS" | grep -o '"total_generals":[0-9]*' | grep -o '[0-9]*' || echo "0")
    test_passed "Mind OS has $TOTAL_GENERALS LLM Generals configured"
else
    test_failed "Could not retrieve Mind OS status"
fi

# Test 4: GitLens Aggregator Stats
echo ""
echo "Test 4: GitLens Aggregator Stats"
echo "---------------------------------"
if curl -f -s "${GITLENS_URL}/stats" > /dev/null 2>&1; then
    test_passed "GitLens Aggregator stats endpoint responding"
else
    test_warning "GitLens Aggregator stats endpoint not available (may be empty)"
fi

# Test 5: Send Test Event to GitLens Aggregator
echo ""
echo "Test 5: Send Test Event to GitLens Aggregator"
echo "----------------------------------------------"
TEST_EVENT=$(cat <<EOF
{
  "type": "pr_created",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "repository": "strategickhaos/test-repo",
  "user": "test-user",
  "metadata": {
    "pr_number": 999,
    "title": "Test PR from integration test",
    "description": "This is a test event"
  }
}
EOF
)

RESPONSE=$(curl -s -X POST "${GITLENS_URL}/events" \
  -H "Content-Type: application/json" \
  -d "$TEST_EVENT" 2>/dev/null || echo "{}")

if echo "$RESPONSE" | grep -q "Event received"; then
    test_passed "Test event accepted by GitLens Aggregator"
else
    test_failed "GitLens Aggregator did not accept test event"
fi

# Test 6: Verify Event Distribution (wait a moment)
echo ""
echo "Test 6: Verify Event Distribution"
echo "----------------------------------"
sleep 2

DISTRIBUTIONS=$(curl -s "${MINDOS_URL}/distributions" 2>/dev/null || echo "{}")
if echo "$DISTRIBUTIONS" | grep -q "total"; then
    TOTAL_DIST=$(echo "$DISTRIBUTIONS" | grep -o '"total":[0-9]*' | grep -o '[0-9]*' || echo "0")
    if [ "$TOTAL_DIST" -gt 0 ]; then
        test_passed "Mind OS has processed $TOTAL_DIST distributions"
    else
        test_warning "Mind OS has not processed any distributions yet"
    fi
else
    test_warning "Could not retrieve distribution history"
fi

# Test 7: Check Prometheus Metrics
echo ""
echo "Test 7: Check Prometheus Metrics"
echo "---------------------------------"
METRICS=$(curl -s "${MINDOS_URL}/metrics" 2>/dev/null || echo "")
if echo "$METRICS" | grep -q "mindos_llm_generals_total"; then
    test_passed "Prometheus metrics endpoint is working"
else
    test_warning "Prometheus metrics not available"
fi

# Test 8: Test Different Event Types
echo ""
echo "Test 8: Test Different Event Types"
echo "-----------------------------------"

EVENT_TYPES=("review_started" "review_submitted" "needs_attention" "pr_merged")
for event_type in "${EVENT_TYPES[@]}"; do
    EVENT=$(cat <<EOF
{
  "type": "$event_type",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "repository": "strategickhaos/test-repo",
  "user": "test-user",
  "metadata": {}
}
EOF
    )
    
    RESPONSE=$(curl -s -X POST "${GITLENS_URL}/events" \
      -H "Content-Type: application/json" \
      -d "$EVENT" 2>/dev/null || echo "{}")
    
    if echo "$RESPONSE" | grep -q "Event received"; then
        test_passed "Event type '$event_type' accepted"
    else
        test_failed "Event type '$event_type' rejected"
    fi
done

# Test 9: Verify GitLens Stats After Events
echo ""
echo "Test 9: Verify GitLens Stats After Events"
echo "------------------------------------------"
sleep 1
STATS=$(curl -s "${GITLENS_URL}/stats" 2>/dev/null || echo "{}")
if echo "$STATS" | grep -q "total_events"; then
    TOTAL_EVENTS=$(echo "$STATS" | grep -o '"total_events":[0-9]*' | grep -o '[0-9]*' || echo "0")
    test_passed "GitLens Aggregator has processed $TOTAL_EVENTS total events"
else
    test_warning "Could not retrieve event stats"
fi

# Summary
echo ""
echo "=================================================="
echo "Test Summary"
echo "=================================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check the logs.${NC}"
    exit 1
fi
