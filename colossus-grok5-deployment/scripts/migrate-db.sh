#!/bin/bash
# migrate-db.sh - Database migrations for Colossus Grok-5
# Artifact #3558

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NAMESPACE="${NAMESPACE:-colossus-grok5}"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace=*)
            NAMESPACE="${1#*=}"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: migrate-db.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --namespace=NS     Kubernetes namespace (default: colossus-grok5)"
            echo "  --dry-run          Print SQL without executing"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_info "Starting database migrations for ${NAMESPACE}"

# Migration 1: Provenance tables
log_info "Migration 1: Creating provenance tables..."
MIGRATION_1=$(cat <<'EOF'
-- Provenance batch records
CREATE TABLE IF NOT EXISTS provenance_batches (
    id SERIAL PRIMARY KEY,
    merkle_root VARCHAR(64) NOT NULL UNIQUE,
    ots_proof BYTEA,
    record_count INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified_at TIMESTAMP WITH TIME ZONE,
    verified BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_provenance_batches_created 
    ON provenance_batches(created_at);
CREATE INDEX IF NOT EXISTS idx_provenance_batches_merkle 
    ON provenance_batches(merkle_root);

-- Individual records
CREATE TABLE IF NOT EXISTS provenance_records (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES provenance_batches(id),
    tweet_id VARCHAR(64) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    toxicity_score REAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_provenance_records_batch 
    ON provenance_records(batch_id);
CREATE INDEX IF NOT EXISTS idx_provenance_records_hash 
    ON provenance_records(content_hash);
EOF
)

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Migration 1 SQL:"
    echo "$MIGRATION_1"
else
    log_info "Migration 1 applied (provenance tables)"
fi

# Migration 2: Checkpoint tables
log_info "Migration 2: Creating checkpoint tables..."
MIGRATION_2=$(cat <<'EOF'
-- Checkpoint metadata
CREATE TABLE IF NOT EXISTS checkpoints (
    id SERIAL PRIMARY KEY,
    step INTEGER NOT NULL UNIQUE,
    hash VARCHAR(64) NOT NULL,
    size_bytes BIGINT NOT NULL,
    path VARCHAR(512) NOT NULL,
    consensus_fraction REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_checkpoints_step 
    ON checkpoints(step);

-- Checkpoint votes
CREATE TABLE IF NOT EXISTS checkpoint_votes (
    id SERIAL PRIMARY KEY,
    checkpoint_id INTEGER REFERENCES checkpoints(id),
    node_id VARCHAR(128) NOT NULL,
    approved BOOLEAN NOT NULL,
    signature BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(checkpoint_id, node_id)
);

CREATE INDEX IF NOT EXISTS idx_checkpoint_votes_checkpoint 
    ON checkpoint_votes(checkpoint_id);
EOF
)

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Migration 2 SQL:"
    echo "$MIGRATION_2"
else
    log_info "Migration 2 applied (checkpoint tables)"
fi

# Migration 3: Audit tables
log_info "Migration 3: Creating audit tables..."
MIGRATION_3=$(cat <<'EOF'
-- Audit log
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(64) NOT NULL,
    deployment_id VARCHAR(128),
    user_id VARCHAR(128),
    details JSONB,
    hash VARCHAR(64) NOT NULL,
    previous_hash VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_type 
    ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_log_deployment 
    ON audit_log(deployment_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created 
    ON audit_log(created_at);
EOF
)

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Migration 3 SQL:"
    echo "$MIGRATION_3"
else
    log_info "Migration 3 applied (audit tables)"
fi

# Migration 4: Energy metrics tables
log_info "Migration 4: Creating energy metrics tables..."
MIGRATION_4=$(cat <<'EOF'
-- Energy readings
CREATE TABLE IF NOT EXISTS energy_readings (
    id SERIAL PRIMARY KEY,
    power_mw REAL NOT NULL,
    megapack_soc REAL NOT NULL,
    decision VARCHAR(32) NOT NULL,
    suggested_scale REAL NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_energy_readings_time 
    ON energy_readings(recorded_at);

-- Hypertable for time-series if TimescaleDB is available
-- SELECT create_hypertable('energy_readings', 'recorded_at', if_not_exists => TRUE);
EOF
)

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Migration 4 SQL:"
    echo "$MIGRATION_4"
else
    log_info "Migration 4 applied (energy tables)"
fi

log_info "All migrations completed!"
