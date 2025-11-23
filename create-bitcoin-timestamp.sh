#!/bin/bash
# Bitcoin Timestamp Creation Script for SOVEREIGN_MANIFEST_v1.0.md
# This script creates an OpenTimestamps .ots file anchoring the manifest to Bitcoin

set -e

MANIFEST_FILE="SOVEREIGN_MANIFEST_v1.0.md"
OTS_FILE="${MANIFEST_FILE}.ots"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 SOVEREIGNTY ARCHITECTURE - BITCOIN TIMESTAMP CREATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if manifest exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "❌ ERROR: $MANIFEST_FILE not found!"
    echo "   Please run this script from the repository root directory."
    exit 1
fi

# Display manifest info
echo "📄 Manifest File: $MANIFEST_FILE"
echo "📊 File Size: $(wc -c < "$MANIFEST_FILE") bytes"
echo "🔑 SHA256 Hash: $(sha256sum "$MANIFEST_FILE" | cut -d' ' -f1)"
echo ""

# Method selection
echo "Select timestamp creation method:"
echo "  1) OpenTimestamps CLI (ots stamp - recommended)"
echo "  2) Catallaxy Calendar Server (curl)"
echo "  3) OTS BTC Catallaxy (curl alternative)"
echo "  4) Alice Calendar (opentimestamps.org)"
echo ""
read -p "Enter choice [1-4] (default: 1): " method
method=${method:-1}

echo ""
echo "🚀 Creating Bitcoin timestamp..."
echo ""

case $method in
    1)
        # Check if ots is installed
        if ! command -v ots &> /dev/null; then
            echo "📦 OpenTimestamps CLI not found. Installing..."
            pip3 install --user opentimestamps-client
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        echo "Using: ots stamp $MANIFEST_FILE"
        ots stamp "$MANIFEST_FILE"
        ;;
    
    2)
        echo "Using: https://btc.calendar.catallaxy.com"
        curl -X POST https://btc.calendar.catallaxy.com \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@$MANIFEST_FILE" \
            -o "$OTS_FILE" \
            -w "\nHTTP Status: %{http_code}\n"
        ;;
    
    3)
        echo "Using: https://ots.btc.catallaxy.com/timestamp"
        curl -X POST https://ots.btc.catallaxy.com/timestamp \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@$MANIFEST_FILE" \
            -o "$OTS_FILE" \
            -w "\nHTTP Status: %{http_code}\n"
        ;;
    
    4)
        echo "Using: https://alice.btc.calendar.opentimestamps.org/timestamp"
        curl -X POST https://alice.btc.calendar.opentimestamps.org/timestamp \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@$MANIFEST_FILE" \
            -o "$OTS_FILE" \
            -w "\nHTTP Status: %{http_code}\n"
        ;;
    
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac

echo ""

# Verify creation
if [ -f "$OTS_FILE" ]; then
    echo "✅ SUCCESS: Bitcoin timestamp created!"
    echo ""
    echo "📋 Timestamp Details:"
    echo "   File: $OTS_FILE"
    echo "   Size: $(wc -c < "$OTS_FILE") bytes"
    echo "   Type: $(file -b "$OTS_FILE")"
    echo ""
    
    # Try to get info if ots is available
    if command -v ots &> /dev/null; then
        echo "🔍 Timestamp Information:"
        ots info "$OTS_FILE" || echo "   (Info will be available after Bitcoin confirmation)"
        echo ""
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 SOVEREIGNTY: 100% COMPLETE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Next steps:"
    echo "  1. Verify timestamp: ots verify $OTS_FILE"
    echo "  2. Commit to repository: git add $OTS_FILE && git commit -m 'Add Bitcoin timestamp'"
    echo "  3. Push to GitHub: git push"
    echo ""
    echo "⏰ Note: Bitcoin confirmation takes 10-60 minutes on average."
    echo "        The timestamp is valid immediately but gains more security with each block."
    echo ""
    echo "🖤 You are sovereignty. Forever."
    echo ""
else
    echo "❌ ERROR: Failed to create timestamp file!"
    echo "   Please check network connectivity and try again."
    exit 1
fi
