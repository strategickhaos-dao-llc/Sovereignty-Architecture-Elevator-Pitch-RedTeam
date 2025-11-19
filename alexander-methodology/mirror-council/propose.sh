#!/bin/bash

# Mirror-Generals Council - Proposal Submission
# Submit a research or policy proposal to the council

PROPOSAL_FILE="$1"

if [ -z "$PROPOSAL_FILE" ]; then
    cat <<EOF
Usage: $0 --file <proposal.yaml>

Submit a proposal to the Mirror-Generals Council for review.

Proposal Template:
  title: "Your Proposal Title"
  author: "Your Node ID or Name"
  date: "$(date +%Y-%m-%d)"
  category: "research-priority | resource-allocation | policy | strategy"
  summary: "One paragraph summary"
  
  problem_statement: |
    What issue or opportunity does this address?
  
  proposed_solution: |
    What are you proposing?
  
  impact_analysis: |
    Benefits, risks, and consequences
  
  resource_requirements: |
    What resources are needed?
  
  success_metrics: |
    How will we measure success?

Example:
  $0 --file my-proposal.yaml

EOF
    exit 1
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --file)
            PROPOSAL_FILE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ ! -f "$PROPOSAL_FILE" ]; then
    echo "Error: Proposal file not found: $PROPOSAL_FILE"
    exit 1
fi

COUNCIL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROPOSALS_DIR="$COUNCIL_DIR/proposals"
mkdir -p "$PROPOSALS_DIR"

PROPOSAL_ID="PR-$(date +%Y-%m-%d-%H%M%S)"
PROPOSAL_PATH="$PROPOSALS_DIR/$PROPOSAL_ID.yaml"

cp "$PROPOSAL_FILE" "$PROPOSAL_PATH"

echo "═══════════════════════════════════════════════════════════════"
echo "  MIRROR-GENERALS COUNCIL - PROPOSAL SUBMISSION"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✓ Proposal received: $PROPOSAL_ID"
echo "✓ Stored at: $PROPOSAL_PATH"
echo ""
echo "📋 Review Process:"
echo "  1. Council members will review your proposal"
echo "  2. Relevant Mirror-Generals will provide analysis"
echo "  3. Voting will occur at next council session"
echo "  4. Origin Node Zero will make final decision"
echo ""
echo "⏱️  Expected timeline: 7-14 days for standard proposals"
echo "    Emergency proposals: 24-48 hours"
echo ""
echo "📬 You will be notified via:"
echo "  • GitHub issue updates"
echo "  • Discord #mirror-council channel"
echo "  • Direct message to your node"
echo ""
echo "Check status: ./mirror-council/status.sh --proposal-id $PROPOSAL_ID"
echo ""
echo "═══════════════════════════════════════════════════════════════"
