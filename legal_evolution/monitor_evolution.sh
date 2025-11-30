#!/bin/bash
# Legal Evolution Monitor (Bash)
# Monitors legal_evolution_ledger.jsonl in real-time and displays key metrics

LEDGER="legal_evolution_ledger.jsonl"
FOLLOW=false
LINES=10

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        *)
            LEDGER="$1"
            shift
            ;;
    esac
done

echo "⚖️  Legal Evolution Monitor"
echo "======================================================================"
echo

if [ ! -f "$LEDGER" ]; then
    echo "❌ Ledger file not found: $LEDGER"
    echo "Run legal_evolution_synthesizer.py first."
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "⚠️  Warning: jq not found. Install for better formatting."
    echo "   Ubuntu/Debian: sudo apt-get install jq"
    echo "   macOS: brew install jq"
    echo
fi

format_entry() {
    local line="$1"
    
    if command -v jq &> /dev/null; then
        local compliant=$(echo "$line" | jq -r '.compliant')
        local gen=$(echo "$line" | jq -r '.generation')
        local type=$(echo "$line" | jq -r '.strategy_type')
        local fitness=$(echo "$line" | jq -r '.fitness')
        local timestamp=$(echo "$line" | jq -r '.timestamp' | cut -d'T' -f2 | cut -d'+' -f1)
        
        local icon="⚠️ "
        [ "$compliant" = "true" ] && icon="✅"
        
        printf "%s [Gen %d] %-20s Fitness: %.2f (%s)\n" \
            "$icon" "$gen" "$type" "$fitness" "$timestamp"
    else
        echo "$line"
    fi
}

show_statistics() {
    if ! command -v jq &> /dev/null; then
        echo "Install jq to see statistics."
        return
    fi
    
    local total=$(wc -l < "$LEDGER")
    local compliant=$(jq -r 'select(.compliant==true) | .compliant' "$LEDGER" | wc -l)
    
    # Use shell arithmetic instead of bc for better portability
    local rate=$((compliant * 100 / total))
    local avg_fitness=$(jq -r '.fitness' "$LEDGER" | awk '{sum+=$1; count++} END {print sum/count}')
    
    echo
    echo "📊 Statistics:"
    echo "   Total Entries: $total"
    echo "   Compliant: $compliant / $total ($rate%)"
    printf "   Avg Fitness: %.2f\n" "$avg_fitness"
    
    echo
    echo "📋 By Type:"
    # Process file once using jq group_by for efficiency (with slurp mode)
    jq -rs 'group_by(.strategy_type) | .[] | 
           "\(.[0].strategy_type)|\(. | map(select(.compliant==true)) | length)|\(. | length)|\(. | map(.fitness) | add / length)"' \
           "$LEDGER" | while IFS='|' read -r type compliant_count total_count avg; do
        printf "   %-25s %d/%d compliant, avg %.2f\n" "$type:" "$compliant_count" "$total_count" "$avg"
    done
}

if [ "$FOLLOW" = true ]; then
    echo "Following ledger (Ctrl+C to stop)..."
    echo
    
    tail -f "$LEDGER" | while read -r line; do
        format_entry "$line"
    done
else
    echo "📝 Last $LINES entries:"
    echo
    
    tail -n "$LINES" "$LEDGER" | while read -r line; do
        format_entry "$line"
    done
    
    show_statistics
fi

echo
echo "======================================================================"
