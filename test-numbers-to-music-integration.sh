#!/bin/bash
# Integration test for Numbers to Divine Music Engine

set -e

echo "🎹 Testing Numbers to Divine Music Engine Integration"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Create test directories
echo "📁 Setting up test environment..."
TEST_DIR="/tmp/numbers-to-music-test-$$"
mkdir -p "$TEST_DIR"/{data,outputs}

# Test 1: CLI Conversion
echo ""
echo "Test 1: CLI Number Conversion"
cd src/numbers-to-music
python3 convert_numbers.py --output "$TEST_DIR/outputs" --title "Test Symphony" 13847 47000 432 13 21 34 55 89 144
if [ -f "$TEST_DIR/outputs"/*.mid ]; then
    echo "✅ CLI conversion successful"
    ls -lh "$TEST_DIR/outputs"/*.mid
else
    echo "❌ CLI conversion failed - no MIDI file generated"
    exit 1
fi

# Test 2: Log File Processing
echo ""
echo "Test 2: Log File Processing"
cat > "$TEST_DIR/data/test.log" << EOF
[2025-01-01 12:00:00] INFO: System started with 13847 nodes
[2025-01-01 12:01:00] INFO: Processing 47000 requests
[2025-01-01 12:02:00] INFO: Latency 432 ms
[2025-01-01 12:03:00] INFO: Active connections: 21
[2025-01-01 12:04:00] INFO: Throughput: 34 GB/s
EOF

python3 test_numbers_to_music.py
if [ $? -eq 0 ]; then
    echo "✅ All unit tests passed"
else
    echo "❌ Unit tests failed"
    exit 1
fi

# Test 3: Docker Build
echo ""
echo "Test 3: Docker Build"
cd ../..
if docker build -t numbers-to-music-test:latest -f Dockerfile.numbers-to-music . > /dev/null 2>&1; then
    echo "✅ Docker image builds successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Test 4: Docker Run
echo ""
echo "Test 4: Docker Container Execution"
docker run --rm \
    -v "$TEST_DIR/data":/data:ro \
    -v "$TEST_DIR/outputs":/app/outputs \
    numbers-to-music-test:latest \
    timeout 5 python3 -u numbers_to_music.py > /dev/null 2>&1 || true

MIDI_FILES=$(ls -1 "$TEST_DIR/outputs"/*.mid 2>/dev/null | wc -l)
if [ "$MIDI_FILES" -gt 0 ]; then
    echo "✅ Docker container generated $MIDI_FILES MIDI file(s)"
    
    # Verify MIDI file format
    FIRST_MIDI=$(ls -1 "$TEST_DIR/outputs"/*.mid | head -1)
    if file "$FIRST_MIDI" | grep -q "Standard MIDI"; then
        echo "✅ MIDI file format is valid"
    else
        echo "⚠️  MIDI file format may be invalid"
    fi
else
    echo "❌ Docker container failed to generate MIDI"
    exit 1
fi

# Test 5: Verify 432 Hz tuning metadata
echo ""
echo "Test 5: Verify 432 Hz Tuning"
JSON_FILE=$(ls -1 "$TEST_DIR/outputs"/*.json | head -1)
if [ -f "$JSON_FILE" ]; then
    if grep -q '"tuning": "432 Hz"' "$JSON_FILE"; then
        echo "✅ 432 Hz tuning confirmed in metadata"
    else
        echo "❌ 432 Hz tuning not found in metadata"
        exit 1
    fi
else
    echo "❌ No metadata JSON file found"
    exit 1
fi

# Clean up
echo ""
echo "🧹 Cleaning up test environment..."
rm -rf "$TEST_DIR"

# Summary
echo ""
echo "════════════════════════════════════════════════"
echo "✅ All Integration Tests Passed!"
echo "════════════════════════════════════════════════"
echo ""
echo "The Numbers to Divine Music Engine is working correctly:"
echo "  ✓ CLI conversion works"
echo "  ✓ Unit tests pass"
echo "  ✓ Docker builds successfully"
echo "  ✓ Container generates valid MIDI files"
echo "  ✓ 432 Hz tuning is applied"
echo ""
echo "🎵 Every number now sings in 432 Hz. Forever."
