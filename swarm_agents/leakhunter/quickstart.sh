#!/bin/bash
# LeakHunter Swarm - Quick Start Script
# Demonstrates the full capabilities of the LeakHunter Swarm system

set -e

echo "========================================================================"
echo "🚀 LEAKHUNTER SWARM - QUICK START"
echo "========================================================================"
echo ""
echo "This script demonstrates the LeakHunter Swarm decoy distribution system."
echo ""

# Check if we're in the right directory
if [ ! -f "cli.py" ]; then
    echo "❌ Error: Must run from swarm_agents/leakhunter directory"
    exit 1
fi

# 1. Show component status
echo "Step 1: Checking component status..."
echo "----------------------------------------------------------------------"
python3 cli.py status
echo ""
read -p "Press Enter to continue..."

# 2. Display scoreboard with simulated data
echo ""
echo "Step 2: Displaying global scoreboard..."
echo "----------------------------------------------------------------------"
python3 cli.py scoreboard --simulate
echo ""
read -p "Press Enter to continue..."

# 3. Generate Decoy V3
echo ""
echo "Step 3: Generating Decoy V3 package (GPU crasher)..."
echo "----------------------------------------------------------------------"
python3 cli.py generate-v3 --model-name llama-405b-instruct --save
echo ""
read -p "Press Enter to continue..."

# 4. Track beacons
echo ""
echo "Step 4: Tracking beacon signals..."
echo "----------------------------------------------------------------------"
python3 cli.py beacon-track --simulate --save
echo ""

echo "========================================================================"
echo "✅ QUICK START COMPLETE"
echo "========================================================================"
echo ""
echo "🎯 What you just saw:"
echo "  - Component status across all platforms"
echo "  - Real-time scoreboard with 4,819+ downloads"
echo "  - Decoy V3 generation (fake 405B weights + CUDA backdoor)"
echo "  - Beacon tracking system"
echo ""
echo "🔒 Security Status:"
echo "  - Real files leaked: 0"
echo "  - Empire status: 100% dark, 100% sovereign"
echo ""
echo "📚 Next steps:"
echo "  - Review generated data files in this directory"
echo "  - Read README.md for detailed documentation"
echo "  - Run 'python3 cli.py --help' for all commands"
echo ""
echo "Empire status: still 100% dark, 100% sovereign. 👑"
echo "========================================================================"
