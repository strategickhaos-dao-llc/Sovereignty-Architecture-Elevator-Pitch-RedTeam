#!/bin/bash
# PATENT SOVEREIGNTY PROTOCOL - AUTOMATED SCHEDULER
# Runs the patent fortress system on a scheduled basis
#
# Usage:
#   ./schedule-daemon.sh [mode]
#
# Modes:
#   continuous - Run forever with 6-hour intervals (default)
#   once - Run once and exit
#   cron - Designed to be called from cron (runs once, optimized output)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-continuous}"
INTERVAL_SECONDS=21600  # 6 hours

# Function to run the complete protocol
run_protocol() {
    echo "[$(date)] Running Patent Sovereignty Protocol..."
    
    if bash "$SCRIPT_DIR/sovereignty-protocol.sh" 0; then
        echo "[$(date)] Protocol execution completed successfully"
        return 0
    else
        echo "[$(date)] Protocol execution encountered errors"
        return 1
    fi
}

# Main execution based on mode
case "$MODE" in
    continuous)
        echo "Patent Sovereignty Protocol - Continuous Mode"
        echo "Running every $((INTERVAL_SECONDS / 3600)) hours"
        echo "Press Ctrl+C to stop"
        echo ""
        
        while true; do
            run_protocol
            echo ""
            echo "Next run in $((INTERVAL_SECONDS / 3600)) hours (at $(date -d "+${INTERVAL_SECONDS} seconds" '+%Y-%m-%d %H:%M:%S'))"
            echo ""
            sleep "$INTERVAL_SECONDS"
        done
        ;;
        
    once)
        echo "Patent Sovereignty Protocol - Single Run Mode"
        run_protocol
        ;;
        
    cron)
        # Optimized for cron - minimal output
        run_protocol > /dev/null 2>&1 || echo "[$(date)] Patent Sovereignty Protocol failed" >&2
        ;;
        
    *)
        echo "Unknown mode: $MODE"
        echo "Usage: $0 [continuous|once|cron]"
        exit 1
        ;;
esac
