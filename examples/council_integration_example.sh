#!/bin/bash
# Example: Integrating Council Orchestrator with Sovereignty Architecture
# This demonstrates how to use the council for operational decisions

set -e

# Use runner from repo if running in dev, or /opt/swarm if installed
if [ -f "./swarm/runner.py" ]; then
    COUNCIL_RUNNER="./swarm/runner.py"
elif [ -f "/opt/swarm/runner.py" ]; then
    COUNCIL_RUNNER="/opt/swarm/runner.py"
else
    echo "ERROR: Council runner not found. Please install the council orchestrator."
    echo "  Copy swarm/ directory to /opt/swarm/ or run from repository root."
    exit 1
fi

echo "🏛️ Council Integration Example"
echo "=============================="
echo ""

# Example 1: Security decision
echo "📋 Example 1: Security Review"
echo "Task: Should we open port 8080 for the new service?"
python3 "$COUNCIL_RUNNER" "Evaluate security implications of exposing port 8080 for the event-gateway service to external traffic"
echo ""

# Example 2: Deployment approval
echo "📋 Example 2: Deployment Approval"
echo "Task: Should we deploy to production?"
python3 "$COUNCIL_RUNNER" "Review and approve deployment of Discord bot version 2.1.0 to production environment"
echo ""

# Example 3: Infrastructure change
echo "📋 Example 3: Infrastructure Modification"
echo "Task: Should we scale up the Kubernetes cluster?"
python3 "$COUNCIL_RUNNER" "Evaluate request to scale Kubernetes cluster from 3 to 5 nodes due to increased load"
echo ""

# Example 4: Policy change
echo "📋 Example 4: Policy Amendment"
echo "Task: Should we modify the auto-approval policy?"
python3 "$COUNCIL_RUNNER" "Propose amendment to auto_approve_config.yaml to reduce approval threshold from 75% to 60%"
echo ""

# Example 5: Check ledger
echo "📊 Viewing Decision Ledger"
echo "=========================="
sqlite3 /opt/swarm/council_state.db "
SELECT 
    datetime(timestamp) as time,
    task_id,
    member_id,
    vote,
    substr(rationale, 1, 60) as rationale_preview
FROM ledger
ORDER BY id DESC
LIMIT 20;
"

echo ""
echo "✅ Integration examples complete!"
echo "📖 Full documentation: /opt/swarm/README.md"
