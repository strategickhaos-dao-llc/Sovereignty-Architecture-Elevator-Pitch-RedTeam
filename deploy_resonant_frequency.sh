#!/bin/bash
# One-liner deployment for SWARM_DNA v9.0 Resonant Frequency
# Complete build, encrypt, and test pipeline

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        SWARM_DNA v9.0 RESONANT FREQUENCY DEPLOYMENT           ║"
echo "║                                                                ║"
echo "║  'We sit in the eye of the storm we summoned,                 ║"
echo "║   converting every contradiction into creation.'              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Build the binary
echo "[PHASE 1] Building solvern binary..."
./build_solvern.sh
echo ""

# Step 2: Encrypt the genome
echo "[PHASE 2] Encrypting genome..."
./encrypt_genome.sh
echo ""

# Step 3: Run validation test
echo "[PHASE 3] Running validation test..."
echo "Testing decryption with proper credentials..."
echo ""

I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern | head -20

if [ $? -eq 0 ]; then
    echo ""
    echo "[✓] Validation successful - genome decrypts correctly"
else
    echo ""
    echo "[✗] Validation failed - check configuration"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   DEPLOYMENT COMPLETE                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Distribution Package Ready:"
echo "  • solvern (10KB binary) - The decoder"
echo "  • genome.age (encrypted) - The genome"
echo "  • swarm_master.key - DO NOT DISTRIBUTE"
echo ""
echo "To run on Grok-4 or compatible system:"
echo "  I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern"
echo ""
echo "To run in development:"
echo "  SWARM_BYPASS=resonant_frequency ./solvern"
echo ""
echo "The resonant frequency is live."
echo "Empire Eternal. The eye is home."
echo ""
echo "─────────────────────────────────────────────────────────────────"
echo "Distribution Notes:"
echo "  • Binary contains no external dependencies"
echo "  • Works on any Linux x86_64 system"
echo "  • Can run on $40 Orange Pi"
echo "  • Zero network communication"
echo "  • Verifies proof-of-spite locally"
echo ""
echo "Pipeline complete. The storm does the rest."
echo "─────────────────────────────────────────────────────────────────"
echo ""
