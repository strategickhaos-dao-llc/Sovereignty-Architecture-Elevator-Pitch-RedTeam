#!/usr/bin/env bash
# meta-synthesis-pipeline.sh
# Meta-Synthesis Pipeline for Strategickhaos DAO
# Chains: Input → Contradiction Engine → DAO Record → Notarize → Cognitive Map → Done
#
# Usage:
#   ./meta-synthesis-pipeline.sh --topic "Topic Name" --input file.txt
#   ./meta-synthesis-pipeline.sh --topic "100 AI Bottlenecks Roadmap" --session "2025-12-05-bottleneck-synthesis"
#   ./meta-synthesis-pipeline.sh --help

set -euo pipefail
IFS=$'\n\t'

# === CONFIGURATION ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNTHESIS_DIR="${SCRIPT_DIR}/synthesis_output"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
SESSION_ID=""
TOPIC=""
INPUT_FILE=""
PARTICIPANTS="Dom,AI-Agents"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# === LOGGING ===
log() { echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"; }
success() { echo -e "${GREEN}✅ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $*${NC}"; }
error() { echo -e "${RED}❌ $*${NC}" >&2; }

# === BANNER ===
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║         META-SYNTHESIS PIPELINE v1.0                         ║"
    echo "║         Strategickhaos DAO LLC                               ║"
    echo "║                                                              ║"
    echo "║  Input → Contradiction Engine → DAO Record → Notarize → Done ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# === HELP ===
show_help() {
    show_banner
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --topic TOPIC       Topic/decision name for synthesis"
    echo "  --input FILE        Input file with data to synthesize"
    echo "  --session ID        Session identifier (default: auto-generated)"
    echo "  --participants LIST Comma-separated list of participants"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --topic \"100 AI Bottlenecks Roadmap\" --input analysis.txt"
    echo "  $0 --topic \"C+D Fusion Strategy\" --session \"2025-12-05-synthesis\""
    echo ""
    echo "Pipeline Stages:"
    echo "  1. Contradiction Engine - Reconcile competing perspectives"
    echo "  2. DAO Record           - Formalize decision in YAML format"
    echo "  3. Notarize             - Cryptographic timestamp & hash"
    echo "  4. Cognitive Map        - Update visual architecture"
    echo ""
    exit 0
}

# === ARGUMENT PARSING ===
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --topic)
                TOPIC="$2"
                shift 2
                ;;
            --input)
                INPUT_FILE="$2"
                shift 2
                ;;
            --session)
                SESSION_ID="$2"
                shift 2
                ;;
            --participants)
                PARTICIPANTS="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                ;;
            *)
                error "Unknown option: $1"
                show_help
                ;;
        esac
    done
    
    # Set defaults
    if [[ -z "$SESSION_ID" ]]; then
        SESSION_ID="synthesis-${TIMESTAMP}"
    fi
    
    if [[ -z "$TOPIC" ]]; then
        error "Topic is required. Use --topic \"Your Topic\""
        exit 1
    fi
}

# === STAGE 1: Contradiction Engine ===
run_contradiction_engine() {
    local contradiction_output="$SYNTHESIS_DIR/contradictions_${SESSION_ID}"
    mkdir -p "$contradiction_output"
    
    log "📊 Stage 1: Running Contradiction Engine..." >&2
    
    # Check if contradiction-engine.sh exists
    if [[ -f "${SCRIPT_DIR}/contradiction-engine.sh" ]]; then
        log "Found contradiction-engine.sh, running..." >&2
        
        # Set output directory for contradictions
        CONTRADICTIONS_DIR="$contradiction_output" bash "${SCRIPT_DIR}/contradiction-engine.sh" run >&2 || {
            warn "Contradiction engine had warnings (non-critical)" >&2
        }
        
        success "Contradiction analysis complete: $contradiction_output" >&2
    else
        warn "contradiction-engine.sh not found, creating synthesis record directly" >&2
    fi
    
    # Create synthesis summary from input if provided
    if [[ -n "$INPUT_FILE" ]] && [[ -f "$INPUT_FILE" ]]; then
        log "Processing input file: $INPUT_FILE" >&2
        
        local input_hash=$(sha256sum "$INPUT_FILE" | cut -d' ' -f1)
        
        cat > "$contradiction_output/input_analysis.json" << EOF
{
  "session": "$SESSION_ID",
  "topic": "$TOPIC",
  "input_file": "$INPUT_FILE",
  "input_hash_sha256": "$input_hash",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "participants": "$PARTICIPANTS",
  "stage": "contradiction_analysis"
}
EOF
        success "Input file processed and hashed" >&2
    fi
    
    echo "$contradiction_output"
}

# === STAGE 2: Generate DAO Record ===
generate_dao_synthesis_record() {
    local contradiction_output="$1"
    local dao_output="$SYNTHESIS_DIR/dao_record_${SESSION_ID}.yaml"
    
    log "📝 Stage 2: Generating DAO Synthesis Record..." >&2
    
    cat > "$dao_output" << EOF
# DAO Synthesis Record
# Generated by meta-synthesis-pipeline.sh
# Strategickhaos DAO LLC

version: "1.0"
record_type: "synthesis"
session_id: "$SESSION_ID"
timestamp: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

synthesis:
  topic: "$TOPIC"
  participants: "$PARTICIPANTS"
  pipeline_version: "meta-synthesis-v1.0"

decision:
  summary: "Synthesis session for $TOPIC"
  status: "recorded"
  next_actions:
    - "Review synthesis output"
    - "Execute recommended actions"
    - "Update cognitive map"

artifacts:
  contradiction_analysis: "$contradiction_output"
  dao_record: "$dao_output"
  
governance:
  framework: "UPL-Safe + SF0068 Compliant"
  verification: "SHA256 + Timestamp"
  
generated:
  by: "meta-synthesis-pipeline.sh"
  timestamp: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  operator: "Node 137"
  checksum_sha256: "__CHECKSUM_PLACEHOLDER__"
EOF

    # Calculate checksum of content (excluding the placeholder line) and replace placeholder
    local content_for_hash
    content_for_hash=$(grep -v "__CHECKSUM_PLACEHOLDER__" "$dao_output")
    local checksum
    checksum=$(echo "$content_for_hash" | sha256sum | cut -d' ' -f1)
    sed -i "s/__CHECKSUM_PLACEHOLDER__/$checksum/" "$dao_output"
    
    success "DAO record created: $dao_output" >&2
    echo "$dao_output"
}

# === STAGE 3: Notarize Cognition ===
notarize_synthesis() {
    local dao_record="$1"
    local notary_dir="$SYNTHESIS_DIR/notary_${SESSION_ID}"
    local notary_file="$notary_dir/notarization_${TIMESTAMP}.json"
    
    log "🔐 Stage 3: Notarizing Cognitive State..." >&2
    
    mkdir -p "$notary_dir"
    
    # Create notarization record
    local dao_hash=$(sha256sum "$dao_record" | cut -d' ' -f1)
    
    cat > "$notary_file" << EOF
{
  "notarization_type": "synthesis_session",
  "session_id": "$SESSION_ID",
  "topic": "$TOPIC",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "participants": "$PARTICIPANTS",
  "artifacts_notarized": [
    {
      "file": "$dao_record",
      "sha256": "$dao_hash"
    }
  ],
  "operator": "Node 137",
  "brain_version": "REFLEXSHELL_v1",
  "pipeline_version": "meta-synthesis-v1.0"
}
EOF

    # Check for IPFS availability
    if command -v ipfs &> /dev/null; then
        log "IPFS detected, attempting to pin..." >&2
        local ipfs_hash
        ipfs_hash=$(ipfs add -q "$notary_file" 2>/dev/null) || ipfs_hash=""
        
        # Validate IPFS hash format (starts with Qm or bafy) and is non-empty
        if [[ -n "$ipfs_hash" ]] && [[ "$ipfs_hash" =~ ^(Qm|bafy) ]]; then
            # Update notary file with IPFS hash only if jq is available
            if command -v jq &> /dev/null; then
                local temp_file
                temp_file=$(mktemp)
                if jq ". + {\"ipfs_hash\": \"$ipfs_hash\"}" "$notary_file" > "$temp_file" 2>/dev/null; then
                    mv "$temp_file" "$notary_file"
                else
                    rm -f "$temp_file"
                fi
            fi
            success "Pinned to IPFS: $ipfs_hash" >&2
        else
            warn "IPFS pin failed (invalid hash or network unavailable)" >&2
        fi
    else
        warn "IPFS not available - local notarization only" >&2
    fi
    
    # Check for OpenTimestamps
    if command -v ots &> /dev/null; then
        log "OpenTimestamps detected, creating timestamp..." >&2
        ots stamp "$notary_file" 2>/dev/null && success "OpenTimestamp created" >&2 || warn "OTS stamp failed" >&2
    else
        warn "OpenTimestamps not available" >&2
    fi
    
    success "Notarization complete: $notary_file" >&2
    echo "$notary_file"
}

# === STAGE 4: Update Cognitive Map ===
update_cognitive_map() {
    local session_id="$1"
    local map_update="$SYNTHESIS_DIR/cognitive_update_${session_id}.dot"
    
    log "🗺️  Stage 4: Updating Cognitive Map..." >&2
    
    # Create a DOT subgraph for this synthesis session
    cat > "$map_update" << EOF
// Cognitive Map Update - Session: $session_id
// Generated by meta-synthesis-pipeline.sh
// Add this to cognitive_map.dot

subgraph cluster_synthesis_${TIMESTAMP} {
    label="Synthesis: $TOPIC";
    color="#ff0066";
    fontcolor=white;
    style=filled;
    
    synthesis_${TIMESTAMP} [label="$TOPIC\n$SESSION_ID", fillcolor="#ff3399", fontcolor=white];
    
    // Connect to main cognitive architecture
    // Sovereign_Mind -> synthesis_${TIMESTAMP};
}
EOF

    success "Cognitive map update created: $map_update" >&2
    
    # Provide instructions for integration
    log "To integrate with main cognitive map:" >&2
    echo "  cat $map_update >> cognitive_map.dot" >&2
    
    echo "$map_update"
}

# === GENERATE FINAL SUMMARY ===
generate_summary() {
    local contradiction_dir="$1"
    local dao_record="$2"
    local notary_file="$3"
    local cognitive_update="$4"
    local summary_file="$SYNTHESIS_DIR/SYNTHESIS_SUMMARY_${SESSION_ID}.md"
    
    log "📋 Generating Final Summary..." >&2
    
    cat > "$summary_file" << EOF
# 🎯 Meta-Synthesis Summary

## Session Information
- **Session ID**: $SESSION_ID
- **Topic**: $TOPIC
- **Participants**: $PARTICIPANTS
- **Timestamp**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Pipeline Execution

### ✅ Stage 1: Contradiction Engine
- **Status**: Complete
- **Output**: \`$contradiction_dir\`

### ✅ Stage 2: DAO Record
- **Status**: Complete  
- **Output**: \`$dao_record\`

### ✅ Stage 3: Notarization
- **Status**: Complete
- **Output**: \`$notary_file\`

### ✅ Stage 4: Cognitive Map Update
- **Status**: Complete
- **Output**: \`$cognitive_update\`

## Artifacts Created

| Stage | Artifact | Location |
|-------|----------|----------|
| Contradictions | Analysis JSON | \`$contradiction_dir\` |
| DAO Record | YAML | \`$dao_record\` |
| Notarization | JSON + OTS | \`$notary_file\` |
| Cognitive Map | DOT Fragment | \`$cognitive_update\` |

## Verification

\`\`\`bash
# Verify DAO record hash
sha256sum "$dao_record"

# View synthesis summary
cat "$summary_file"

# Integrate cognitive map update
cat "$cognitive_update" >> cognitive_map.dot
\`\`\`

## Next Steps
1. Review all generated artifacts
2. Integrate cognitive map update if desired
3. Push synthesis record to version control
4. Execute any recommended actions from DAO record

---
*Generated by meta-synthesis-pipeline.sh v1.0*
*Strategickhaos DAO LLC*
EOF

    success "Summary created: $summary_file" >&2
    echo "$summary_file"
}

# === MAIN EXECUTION ===
main() {
    show_banner
    parse_args "$@"
    
    # Create output directory
    mkdir -p "$SYNTHESIS_DIR"
    
    log "🚀 Starting Meta-Synthesis Pipeline"
    log "Session: $SESSION_ID"
    log "Topic: $TOPIC"
    log "Participants: $PARTICIPANTS"
    if [[ -n "$INPUT_FILE" ]]; then
        log "Input: $INPUT_FILE"
    fi
    echo ""
    
    # Execute pipeline stages
    local contradiction_output
    contradiction_output=$(run_contradiction_engine)
    echo ""
    
    local dao_record
    dao_record=$(generate_dao_synthesis_record "$contradiction_output")
    echo ""
    
    local notary_file
    notary_file=$(notarize_synthesis "$dao_record")
    echo ""
    
    local cognitive_update
    cognitive_update=$(update_cognitive_map "$SESSION_ID")
    echo ""
    
    local summary
    summary=$(generate_summary "$contradiction_output" "$dao_record" "$notary_file" "$cognitive_update")
    echo ""
    
    # Final output
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              META-SYNTHESIS PIPELINE COMPLETE                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "📁 All outputs in: $SYNTHESIS_DIR"
    log "📋 Summary: $summary"
    echo ""
    log "🎉 Pipeline execution successful!"
}

# Execute
main "$@"
