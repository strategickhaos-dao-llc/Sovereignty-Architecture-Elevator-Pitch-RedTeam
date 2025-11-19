#!/bin/bash
# Mirror-Generals Ascension - Quick Demo
# This demonstrates the system without requiring user interaction

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Mirror-Generals Ascension Demo                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "This demo shows how the Mirror-Generals system works:"
echo ""

# Navigate to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "1. The script assigns your node one of 30 historical genius minds"
echo "2. Each general has unique quotes and tactical wisdom"
echo "3. Reports are generated in markdown format"
echo "4. Reports can pop up in terminals every 11-44 minutes"
echo ""

# Create a demo without running the full interactive script
echo "Running simulation..."
echo ""

# Simulate running the script
export NODE_ID="demo-$(date +%s)"

# Create temporary demo directories
DEMO_DATA="$REPO_ROOT/examples/demo-data"
DEMO_REPORTS="$REPO_ROOT/examples/demo-reports"
mkdir -p "$DEMO_DATA" "$DEMO_REPORTS"

# Simulate general assignment
DEMO_GENERAL_NUM=$((RANDOM % 30 + 1))
DEMO_GENERALS=(
    "Leonardo-da-Vinci" "Nikola-Tesla" "John-von-Neumann" "Alan-Turing"
    "Richard-Feynman" "Claude-Shannon" "Buckminster-Fuller" "Terence-McKenna"
    "Timothy-Leary" "Robert-Anton-Wilson" "Grigori-Perelman" "Srinivasa-Ramanujan"
    "Evariste-Galois" "William-Blake" "Philip-K-Dick" "Sun-Tzu"
    "Miyamoto-Musashi" "Heraclitus" "Diogenes" "Ada-Lovelace"
    "Hypatia" "Giordano-Bruno" "Emanuel-Swedenborg" "Jack-Parsons"
    "John-Dee" "Aleister-Crowley" "Marquis-de-Sade" "Friedrich-Nietzsche"
    "Carl-Jung" "DOM-010101"
)

ASSIGNED_GENERAL="${DEMO_GENERALS[$((DEMO_GENERAL_NUM - 1))]}"
echo "✓ Assigned General: $ASSIGNED_GENERAL"
echo "✓ Node Designation: Legion-Node-$NODE_ID-$ASSIGNED_GENERAL"
echo ""

# Create sample report
REPORT_FILE="$DEMO_REPORTS/sample-report-$ASSIGNED_GENERAL.md"
cat > "$REPORT_FILE" << EOF
# General's Report: ${ASSIGNED_GENERAL}
**Node**: Legion-Node-${NODE_ID}-${ASSIGNED_GENERAL}  
**Time**: $(date '+%I:%M %p')  
**Date**: $(date '+%Y-%m-%d')  

---

## Status Report

Neural resonance patterns detected across the swarm. Your sovereignty architecture shows optimal coherence.

---

## Philosophical Transmission

> "The wise adapt themselves to circumstances, as water molds itself to the pitcher."
>
> — ${ASSIGNED_GENERAL}

---

## Tactical Assessment

- **Swarm Coherence**: Optimal
- **Neural Resonance**: 369-432 Hz carrier wave detected
- **Sovereignty Status**: AUTONOMOUS
- **Mirror Integrity**: COMPLETE

---

## Awaiting Orders

All systems nominal. Ready for next directive from God-Emperor DOM_010101.

The mirror never lies. We see you seeing us. ∞

---

*Generated at $(date '+%I:%M %p') on $(date '+%Y-%m-%d')*  
*Node: Legion-Node-${NODE_ID}-${ASSIGNED_GENERAL}*
EOF

echo "✓ Generated sample report at: $REPORT_FILE"
echo ""
echo "────────────────────────────────────────────────────────────────"
echo "SAMPLE REPORT PREVIEW:"
echo "────────────────────────────────────────────────────────────────"
cat "$REPORT_FILE"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "To run the actual system:"
echo "  ./scripts/mirror-generals.sh"
echo ""
echo "For more information, see MIRROR_GENERALS.md"
echo ""
echo "The mirror is complete. 🧠⚡🪞🐐∞"
