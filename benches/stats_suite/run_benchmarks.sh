#!/bin/bash
# BM-001: Automated benchmark runner for statistical suite
# Compares C++, Rust, and FlameLang implementations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}BM-001: Statistical Benchmark Suite${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Function to run C++ benchmark
run_cpp() {
    echo -e "${GREEN}Building C++ implementation...${NC}"
    cd cpp
    make clean > /dev/null 2>&1 || true
    make
    echo ""
    
    echo -e "${GREEN}Running C++ benchmark...${NC}"
    echo "10 20 30 40 50 60 70 80 90 100" | ./five_number_summary
    echo ""
    
    cd ..
}

# Function to run Rust benchmark
run_rust() {
    echo -e "${GREEN}Building Rust implementation...${NC}"
    cd rust
    
    # Check if Rust is installed
    if ! command -v cargo &> /dev/null; then
        echo -e "${YELLOW}Rust/Cargo not found. Skipping Rust benchmark.${NC}"
        cd ..
        return
    fi
    
    cargo build --release > /dev/null 2>&1
    echo ""
    
    echo -e "${GREEN}Running Rust benchmark...${NC}"
    echo "10 20 30 40 50 60 70 80 90 100" | cargo run --release
    echo ""
    
    cd ..
}

# Function to run FlameLang benchmark
run_flame() {
    echo -e "${YELLOW}FlameLang compiler not yet available (waiting for FL-005)${NC}"
    echo -e "${YELLOW}Placeholder implementation exists in flame/five_number_summary.fl${NC}"
    echo ""
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    # No arguments, run all benchmarks
    run_cpp
    run_rust
    run_flame
elif [ "$1" == "cpp" ]; then
    run_cpp
elif [ "$1" == "rust" ]; then
    run_rust
elif [ "$1" == "flame" ]; then
    run_flame
else
    echo -e "${RED}Unknown language: $1${NC}"
    echo "Usage: $0 [cpp|rust|flame]"
    exit 1
fi

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Benchmarks complete!${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "Next steps:"
echo "1. Implement actual five-number summary calculation (currently stubs)"
echo "2. Generate test datasets (small, medium, large)"
echo "3. Create oracle files with expected results"
echo "4. Add performance comparison and visualization"
echo "5. Integrate with CI/CD pipeline (INF-002, INF-005)"
