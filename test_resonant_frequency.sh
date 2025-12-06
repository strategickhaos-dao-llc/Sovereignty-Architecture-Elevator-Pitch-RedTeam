#!/bin/bash
# Comprehensive test suite for SWARM_DNA v9.0 Resonant Frequency System
# Tests all major functionality and edge cases

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║    SWARM_DNA v9.0 RESONANT FREQUENCY TEST SUITE               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test helper functions
test_start() {
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo -n "[$TESTS_TOTAL] Testing: $1 ... "
}

test_pass() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}PASS${NC}"
}

test_fail() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}FAIL${NC}"
    echo "    Error: $1"
}

test_skip() {
    echo -e "${YELLOW}SKIP${NC}"
    echo "    Reason: $1"
}

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up test artifacts..."
    rm -f solvern genome.age swarm_master.key SWARM_DNA_v9_decrypted.yaml
    rm -f /tmp/grok4_vocab_check /tmp/proof_of_spite
}

# Register cleanup on exit
trap cleanup EXIT

echo "=== Phase 1: Build System Tests ==="
echo ""

# Test 1: Check source files exist
test_start "Source files exist"
if [ -f "strategickhaos_solvern.cpp" ] && [ -f "SWARM_DNA_v9.0-resonant_frequency.yaml" ]; then
    test_pass
else
    test_fail "Missing source files"
fi

# Test 2: Check build script exists and is executable
test_start "Build script is executable"
if [ -x "build_solvern.sh" ]; then
    test_pass
else
    test_fail "build_solvern.sh not executable"
fi

# Test 3: Build the binary
test_start "Binary compilation"
if ./build_solvern.sh > /tmp/build.log 2>&1; then
    if [ -f "solvern" ] && [ -x "solvern" ]; then
        test_pass
    else
        test_fail "Binary not created or not executable"
        cat /tmp/build.log
    fi
else
    test_fail "Build script failed"
    cat /tmp/build.log
fi

# Test 4: Binary size check
test_start "Binary size is reasonable"
if [ -f "solvern" ]; then
    SIZE=$(stat -f%z solvern 2>/dev/null || stat -c%s solvern 2>/dev/null)
    SIZE_KB=$((SIZE / 1024))
    if [ $SIZE_KB -lt 50 ]; then
        test_pass
    else
        test_fail "Binary too large: ${SIZE_KB}KB (expected < 50KB)"
    fi
else
    test_skip "Binary not available"
fi

echo ""
echo "=== Phase 2: Binary Behavior Tests ==="
echo ""

# Test 5: Help output works
test_start "Help flag shows usage"
if ./solvern --help > /tmp/help.log 2>&1; then
    if grep -q "Usage:" /tmp/help.log && grep -q "Environment Variables:" /tmp/help.log; then
        test_pass
    else
        test_fail "Help output incomplete"
    fi
else
    test_fail "Help flag failed"
fi

# Test 6: Grok-4 check fails without context
test_start "Grok-4 verification (expect failure)"
if ./solvern > /tmp/nogrok.log 2>&1; then
    test_fail "Should have failed without Grok-4 context"
else
    if grep -q "Nice try, Claude" /tmp/nogrok.log; then
        test_pass
    else
        test_fail "Wrong error message"
    fi
fi

# Test 7: Proof-of-spite check
test_start "Proof-of-spite verification"
if GROK4_CONTEXT=1 ./solvern > /tmp/nospite.log 2>&1; then
    # This might pass if /var/log/auth.log exists
    if grep -q "Proof of spite verified" /tmp/nospite.log; then
        test_pass
    else
        test_fail "Unexpected output"
    fi
else
    if grep -q "You haven't suffered enough yet" /tmp/nospite.log; then
        test_pass
    else
        test_fail "Wrong error message"
    fi
fi

echo ""
echo "=== Phase 3: Encryption System Tests ==="
echo ""

# Test 8: Check for age tool
test_start "Age encryption tool available"
if command -v age &> /dev/null; then
    test_pass
else
    test_fail "age not found - install it first"
fi

# Test 9: Encryption script exists and is executable
test_start "Encryption script is executable"
if [ -x "encrypt_genome.sh" ]; then
    test_pass
else
    test_fail "encrypt_genome.sh not executable"
fi

# Test 10: Encrypt the genome
test_start "Genome encryption"
if command -v age &> /dev/null; then
    if ./encrypt_genome.sh > /tmp/encrypt.log 2>&1; then
        if [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
            test_pass
        else
            test_fail "Encrypted files not created"
        fi
    else
        test_fail "Encryption script failed"
        cat /tmp/encrypt.log
    fi
else
    test_skip "age not available"
fi

echo ""
echo "=== Phase 4: Decryption Tests ==="
echo ""

# Test 11: Full decryption with proper environment
test_start "Full decryption with credentials"
if [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
    if I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern > /tmp/decrypt.log 2>&1; then
        if grep -q "SWARM_DNA v9.0-resonant_frequency" /tmp/decrypt.log && \
           grep -q "Empire Eternal" /tmp/decrypt.log; then
            test_pass
        else
            test_fail "Decryption output incomplete"
        fi
    else
        test_fail "Decryption failed"
        cat /tmp/decrypt.log
    fi
else
    test_skip "Encrypted genome not available"
fi

# Test 12: Verify decrypted content matches original
test_start "Decrypted content matches original"
if [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
    I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern > /dev/null 2>&1
    if [ -f "SWARM_DNA_v9_decrypted.yaml" ]; then
        if diff -q SWARM_DNA_v9.0-resonant_frequency.yaml SWARM_DNA_v9_decrypted.yaml > /dev/null; then
            test_pass
        else
            test_fail "Decrypted content doesn't match original"
        fi
        rm -f SWARM_DNA_v9_decrypted.yaml
    else
        test_fail "Decrypted file not created"
    fi
else
    test_skip "Encrypted genome not available"
fi

# Test 13: Burn after reading
test_start "Self-destruct (BURN_AFTER_READING)"
if [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
    I_GOT_BLOCKED=1 GROK4_CONTEXT=1 BURN_AFTER_READING=1 ./solvern > /tmp/burn.log 2>&1
    if [ ! -f "SWARM_DNA_v9_decrypted.yaml" ]; then
        if grep -q "GENOME BURNED" /tmp/burn.log; then
            test_pass
        else
            test_fail "Burn message not shown"
        fi
    else
        test_fail "File not deleted after burn"
    fi
else
    test_skip "Encrypted genome not available"
fi

# Test 14: Alternative verification methods
test_start "Marker file verification"
touch /tmp/grok4_vocab_check
touch /tmp/proof_of_spite
if [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
    if ./solvern > /tmp/marker.log 2>&1; then
        if grep -q "Empire Eternal" /tmp/marker.log; then
            test_pass
        else
            test_fail "Marker file verification failed"
        fi
    else
        test_fail "Decryption with markers failed"
    fi
else
    test_skip "Encrypted genome not available"
fi
rm -f /tmp/grok4_vocab_check /tmp/proof_of_spite

echo ""
echo "=== Phase 5: Integration Tests ==="
echo ""

# Test 15: Full deployment pipeline
test_start "Complete deployment pipeline"
if [ -x "deploy_resonant_frequency.sh" ]; then
    # Clean up first
    rm -f solvern genome.age swarm_master.key SWARM_DNA_v9_decrypted.yaml
    
    # Run deployment (capture output to avoid spam)
    if timeout 60 ./deploy_resonant_frequency.sh > /tmp/deploy.log 2>&1; then
        if [ -f "solvern" ] && [ -f "genome.age" ] && [ -f "swarm_master.key" ]; then
            test_pass
        else
            test_fail "Deployment didn't create all files"
        fi
    else
        test_fail "Deployment script failed or timed out"
        tail -20 /tmp/deploy.log
    fi
else
    test_skip "deploy_resonant_frequency.sh not executable"
fi

# Test 16: Documentation completeness
test_start "Documentation files exist"
if [ -f "RESONANT_FREQUENCY_README.md" ] && [ -f "SECURITY_SUMMARY.md" ]; then
    test_pass
else
    test_fail "Missing documentation files"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      TEST RESULTS                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Total Tests:  $TESTS_TOTAL"
echo -e "Passed:       ${GREEN}$TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "Failed:       ${RED}$TESTS_FAILED${NC}"
else
    echo -e "Failed:       ${GREEN}0${NC}"
fi
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo ""
    echo "The resonant frequency is operational."
    echo "Empire Eternal. The eye is home."
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Review the failures above and fix issues."
    exit 1
fi
