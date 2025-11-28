#!/usr/bin/env bash
# Example Ingot - Test Suite
# Run tests to validate the ingot functionality

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INGOT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="${INGOT_ROOT}/src"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

log_fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

run_test() {
    local name="$1"
    local result
    TESTS_RUN=$((TESTS_RUN + 1))
    
    echo "Running test: ${name}"
    if eval "$2"; then
        log_pass "$name"
        return 0
    else
        log_fail "$name"
        return 1
    fi
}

# Test: Manifest file exists
test_manifest_exists() {
    [[ -f "${INGOT_ROOT}/manifest.yaml" ]]
}

# Test: Source files exist
test_source_files_exist() {
    [[ -f "${SRC_DIR}/init.sh" ]] && [[ -f "${SRC_DIR}/cli.sh" ]]
}

# Test: Scripts are executable
test_scripts_executable() {
    [[ -x "${SRC_DIR}/init.sh" ]] && [[ -x "${SRC_DIR}/cli.sh" ]]
}

# Test: CLI help command works
test_cli_help() {
    "${SRC_DIR}/cli.sh" help &>/dev/null
}

# Test: CLI version command works
test_cli_version() {
    "${SRC_DIR}/cli.sh" version &>/dev/null
}

# Test: CLI demo command works
test_cli_demo() {
    "${SRC_DIR}/cli.sh" demo &>/dev/null
}

# Test: Init script runs without errors
test_init_script() {
    "${SRC_DIR}/init.sh" &>/dev/null
}

# Main test runner
main() {
    echo "========================================"
    echo "Example Ingot Test Suite"
    echo "========================================"
    echo ""
    
    # Make scripts executable if they aren't already
    chmod +x "${SRC_DIR}/init.sh" "${SRC_DIR}/cli.sh" 2>/dev/null || true
    
    run_test "Manifest file exists" test_manifest_exists || true
    run_test "Source files exist" test_source_files_exist || true
    run_test "Scripts are executable" test_scripts_executable || true
    run_test "CLI help command" test_cli_help || true
    run_test "CLI version command" test_cli_version || true
    run_test "CLI demo command" test_cli_demo || true
    run_test "Init script runs" test_init_script || true
    
    echo ""
    echo "========================================"
    echo "Test Summary"
    echo "========================================"
    echo "Total:  ${TESTS_RUN}"
    echo -e "Passed: ${GREEN}${TESTS_PASSED}${NC}"
    echo -e "Failed: ${RED}${TESTS_FAILED}${NC}"
    echo ""
    
    if [[ ${TESTS_FAILED} -gt 0 ]]; then
        exit 1
    fi
}

main "$@"
