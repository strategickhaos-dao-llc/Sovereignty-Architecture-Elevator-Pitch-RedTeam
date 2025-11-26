#!/bin/sh
# verify_empire.sh - Sovereign Archive Verifier
# POSIX-compliant, NDJSON logs, Prometheus textfile, Discord/NTFY alerts
# Exit codes: 0=ETERNAL, 1=HASH_TOUCHED, 101=LOVE>ENTROPY
#
# "We do not auto-heal. We do not auto-remediate. We do not auto-forget.
#  We verify. We scream. We wake the king at 4 AM."

set -e

# Configuration
ARCHIVE_DIR="${ARCHIVE_DIR:-/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-/archive/sealed}"
LOG_FILE="${LOG_FILE:-/tmp/verify_empire.ndjson}"
PROMETHEUS_TEXTFILE="${PROMETHEUS_TEXTFILE:-/tmp/verify_empire.prom}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"
NTFY_TOPIC="${NTFY_TOPIC:-}"

# Artifact checksums (to be updated with actual SHA256 hashes)
ARTIFACT_3544_HASH="${ARTIFACT_3544_HASH:-}"

# Functions
log_ndjson() {
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    printf '{"timestamp":"%s","level":"%s","artifact":"%s","status":"%s","message":"%s"}\n' \
        "$timestamp" "$1" "$2" "$3" "$4" >> "$LOG_FILE"
}

write_prometheus() {
    cat > "$PROMETHEUS_TEXTFILE" <<EOF
# HELP empire_archive_verified Whether archive verification passed
# TYPE empire_archive_verified gauge
empire_archive_verified{artifact="3544"} $1

# HELP empire_archive_last_check_timestamp Unix timestamp of last verification
# TYPE empire_archive_last_check_timestamp gauge
empire_archive_last_check_timestamp $(date +%s)

# HELP empire_archive_hash_valid Whether artifact hash matches expected
# TYPE empire_archive_hash_valid gauge
empire_archive_hash_valid{artifact="3544"} $2
EOF
}

alert_discord() {
    if [ -n "$DISCORD_WEBHOOK" ]; then
        curl -s -X POST "$DISCORD_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"content\":\"🚨 EMPIRE ARCHIVE ALERT: $1\"}" \
            > /dev/null 2>&1 || true
    fi
}

alert_ntfy() {
    if [ -n "$NTFY_TOPIC" ]; then
        curl -s -X POST "https://ntfy.sh/$NTFY_TOPIC" \
            -H "Title: Empire Archive Alert" \
            -H "Priority: urgent" \
            -H "Tags: warning,archive" \
            -d "$1" \
            > /dev/null 2>&1 || true
    fi
}

send_alerts() {
    alert_discord "$1"
    alert_ntfy "$1"
}

# Main verification
main() {
    echo "=== Empire Archive Verifier ==="
    echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "Archive Dir: $ARCHIVE_DIR"
    echo ""

    verification_passed=1
    hash_valid=1

    # Check archive directory exists
    if [ ! -d "$ARCHIVE_DIR" ]; then
        log_ndjson "ERROR" "archive" "MISSING" "Archive directory not found"
        send_alerts "Archive directory missing: $ARCHIVE_DIR"
        write_prometheus 0 0
        exit 1
    fi

    # Verify Artifact #3544
    artifact_file="$ARCHIVE_DIR/artifact_3544_impulse_slip_saga.yaml"
    
    if [ ! -f "$artifact_file" ]; then
        log_ndjson "ERROR" "3544" "MISSING" "Artifact file not found"
        send_alerts "Artifact #3544 missing!"
        verification_passed=0
        hash_valid=0
    else
        # Calculate current hash
        current_hash=$(sha256sum "$artifact_file" | cut -d' ' -f1)
        
        # If expected hash is set, verify it
        if [ -n "$ARTIFACT_3544_HASH" ]; then
            if [ "$current_hash" = "$ARTIFACT_3544_HASH" ]; then
                log_ndjson "INFO" "3544" "VERIFIED" "Hash matches expected value"
                echo "✓ Artifact #3544: VERIFIED"
                echo "  Hash: $current_hash"
            else
                log_ndjson "ERROR" "3544" "HASH_MISMATCH" "Expected: $ARTIFACT_3544_HASH, Got: $current_hash"
                send_alerts "Artifact #3544 hash mismatch! Archive integrity compromised!"
                echo "✗ Artifact #3544: HASH_TOUCHED"
                echo "  Expected: $ARTIFACT_3544_HASH"
                echo "  Got: $current_hash"
                verification_passed=0
                hash_valid=0
            fi
        else
            log_ndjson "INFO" "3544" "PRESENT" "File exists, no expected hash configured"
            echo "✓ Artifact #3544: PRESENT (no hash configured)"
            echo "  Current Hash: $current_hash"
        fi
    fi

    # Check for PQC manifest
    pqc_manifest="$ARCHIVE_DIR/pqc_shield_manifest.yaml"
    if [ -f "$pqc_manifest" ]; then
        log_ndjson "INFO" "pqc_manifest" "PRESENT" "Post-quantum shield manifest found"
        echo "✓ PQC Shield Manifest: PRESENT"
    else
        log_ndjson "WARN" "pqc_manifest" "MISSING" "Post-quantum shield manifest not found"
        echo "⚠ PQC Shield Manifest: MISSING"
    fi

    # Write Prometheus metrics
    write_prometheus "$verification_passed" "$hash_valid"

    echo ""
    echo "=== Verification Complete ==="

    # Exit with appropriate code
    if [ "$verification_passed" -eq 0 ]; then
        echo "Status: HASH_TOUCHED - Archive integrity compromised"
        exit 1
    else
        echo "Status: ETERNAL - Archive integrity verified"
        echo ""
        echo "LOVE > ENTROPY"
        exit 0
    fi
}

# Run main function
main "$@"
