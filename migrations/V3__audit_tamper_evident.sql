-- V3__audit_tamper_evident.sql
ALTER TABLE audit_log
    ADD COLUMN IF NOT EXISTS policy_version TEXT DEFAULT 'v1',
    ADD COLUMN IF NOT EXISTS previous_hash TEXT,
    ADD COLUMN IF NOT EXISTS current_hash TEXT;

CREATE INDEX IF NOT EXISTS idx_audit_chain ON audit_log (current_hash);
