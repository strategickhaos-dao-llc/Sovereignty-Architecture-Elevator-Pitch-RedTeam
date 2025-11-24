#!/bin/bash
# Build script for strategickhaos_solvern
# Compiles the self-decrypting binary with maximum optimization

set -e

echo "=== STRATEGICKHAOS SOLVERN BUILD SYSTEM ==="
echo "Building the resonant frequency decoder..."
echo ""

# Check for required tools
if ! command -v g++ &> /dev/null; then
    echo "Error: g++ not found. Please install build-essential."
    exit 1
fi

# Compile with maximum optimization
echo "[1/3] Compiling with g++ (C++17, O3 optimization)..."
g++ -std=c++17 -O3 -march=native -flto -s -DNDEBUG \
    -o solvern strategickhaos_solvern.cpp

if [ $? -ne 0 ]; then
    echo "Error: Compilation failed."
    exit 1
fi

echo "[✓] Compilation successful"

# Strip symbols
echo "[2/3] Stripping debug symbols..."
strip solvern

if [ $? -ne 0 ]; then
    echo "Warning: Strip failed, but continuing..."
fi

echo "[✓] Binary stripped"

# Optional: Compress with UPX if available
if command -v upx &> /dev/null; then
    echo "[3/3] Compressing with UPX..."
    # Try with --quiet flag, fall back to without if unsupported
    if upx --best --quiet solvern 2>/dev/null; then
        echo "[✓] Binary compressed"
    elif upx --best solvern 2>&1; then
        echo "[✓] Binary compressed"
    else
        echo "[!] UPX compression failed, but continuing with uncompressed binary"
    fi
else
    echo "[3/3] UPX not found, skipping compression"
    echo "    Install upx for smaller binary size: apt-get install upx"
fi

# Show final binary size
BINARY_SIZE=$(stat -f%z solvern 2>/dev/null || stat -c%s solvern 2>/dev/null)
BINARY_SIZE_KB=$((BINARY_SIZE / 1024))

echo ""
echo "=== BUILD COMPLETE ==="
echo "Binary: ./solvern"
echo "Size: ${BINARY_SIZE_KB} KB"
echo ""
echo "To test: I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern"
echo ""
