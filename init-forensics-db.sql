-- Forensics Database Initialization Script
-- Strategickhaos Sovereignty Architecture - DOM_010101 Edition

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Cases table
CREATE TABLE IF NOT EXISTS cases (
    case_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_number VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    case_type VARCHAR(50) NOT NULL, -- 'criminal', 'civil', 'corporate', 'research'
    status VARCHAR(50) NOT NULL DEFAULT 'open', -- 'open', 'active', 'closed', 'archived'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    lead_investigator VARCHAR(255),
    organization VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Evidence items table
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    evidence_number VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    evidence_type VARCHAR(100) NOT NULL, -- 'phone', 'computer', 'disk', 'network', 'document', etc.
    source_location VARCHAR(255),
    collected_by VARCHAR(255) NOT NULL,
    collected_at TIMESTAMP NOT NULL,
    hash_sha256 VARCHAR(64),
    hash_md5 VARCHAR(32),
    file_size BIGINT,
    storage_location VARCHAR(500),
    status VARCHAR(50) DEFAULT 'collected', -- 'collected', 'processing', 'analyzed', 'archived'
    blockchain_tx_id VARCHAR(255), -- Reference to blockchain chain-of-custody record
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Chain of custody log
CREATE TABLE IF NOT EXISTS chain_of_custody (
    custody_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    evidence_id UUID REFERENCES evidence(evidence_id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL, -- 'collected', 'transferred', 'analyzed', 'stored', 'accessed', 'released'
    performed_by VARCHAR(255) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255),
    purpose TEXT,
    witness VARCHAR(255),
    previous_custodian VARCHAR(255),
    next_custodian VARCHAR(255),
    signature_hash VARCHAR(255), -- Cryptographic signature of the custody transfer
    blockchain_tx_id VARCHAR(255),
    notes TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Analysis results table
CREATE TABLE IF NOT EXISTS analysis_results (
    analysis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    evidence_id UUID REFERENCES evidence(evidence_id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL, -- 'memory', 'disk', 'network', 'mobile', 'ai', etc.
    tool_name VARCHAR(100),
    tool_version VARCHAR(50),
    analyst VARCHAR(255) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
    findings TEXT,
    iocs JSONB DEFAULT '[]'::jsonb, -- Indicators of compromise
    artifacts JSONB DEFAULT '[]'::jsonb, -- Extracted artifacts
    confidence_score NUMERIC(3,2), -- 0.00 to 1.00
    report_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Investigators table
CREATE TABLE IF NOT EXISTS investigators (
    investigator_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    organization VARCHAR(255),
    role VARCHAR(100), -- 'lead', 'analyst', 'technician', 'supervisor'
    certifications TEXT[],
    license_number VARCHAR(100),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Case assignments table
CREATE TABLE IF NOT EXISTS case_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    investigator_id UUID REFERENCES investigators(investigator_id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL, -- 'lead', 'analyst', 'consultant'
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    removed_at TIMESTAMP,
    active BOOLEAN DEFAULT true,
    UNIQUE(case_id, investigator_id, active)
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    report_type VARCHAR(100) NOT NULL, -- 'preliminary', 'interim', 'final', 'supplemental'
    title VARCHAR(255) NOT NULL,
    author UUID REFERENCES investigators(investigator_id),
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'review', 'approved', 'published'
    content TEXT,
    file_path VARCHAR(500),
    hash_sha256 VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    approved_at TIMESTAMP,
    published_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Audit log for all database operations
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID,
    action VARCHAR(50) NOT NULL, -- 'insert', 'update', 'delete', 'select'
    performed_by VARCHAR(255) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    changes JSONB,
    query TEXT
);

-- Tags for categorization
CREATE TABLE IF NOT EXISTS tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tag_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    color VARCHAR(7), -- Hex color code
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Case tags junction table
CREATE TABLE IF NOT EXISTS case_tags (
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, tag_id)
);

-- Evidence tags junction table
CREATE TABLE IF NOT EXISTS evidence_tags (
    evidence_id UUID REFERENCES evidence(evidence_id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (evidence_id, tag_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_created_at ON cases(created_at);
CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON evidence(case_id);
CREATE INDEX IF NOT EXISTS idx_evidence_status ON evidence(status);
CREATE INDEX IF NOT EXISTS idx_evidence_hash_sha256 ON evidence(hash_sha256);
CREATE INDEX IF NOT EXISTS idx_chain_evidence_id ON chain_of_custody(evidence_id);
CREATE INDEX IF NOT EXISTS idx_chain_performed_at ON chain_of_custody(performed_at);
CREATE INDEX IF NOT EXISTS idx_analysis_evidence_id ON analysis_results(evidence_id);
CREATE INDEX IF NOT EXISTS idx_analysis_status ON analysis_results(status);
CREATE INDEX IF NOT EXISTS idx_assignments_case_id ON case_assignments(case_id);
CREATE INDEX IF NOT EXISTS idx_assignments_investigator_id ON case_assignments(investigator_id);
CREATE INDEX IF NOT EXISTS idx_reports_case_id ON reports(case_id);
CREATE INDEX IF NOT EXISTS idx_audit_table_record ON audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_performed_at ON audit_log(performed_at);

-- Full text search indexes
CREATE INDEX IF NOT EXISTS idx_cases_fulltext ON cases USING GIN(to_tsvector('english', title || ' ' || description));
CREATE INDEX IF NOT EXISTS idx_evidence_fulltext ON evidence USING GIN(to_tsvector('english', description));
CREATE INDEX IF NOT EXISTS idx_analysis_fulltext ON analysis_results USING GIN(to_tsvector('english', findings));

-- Trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_cases_updated_at BEFORE UPDATE ON cases
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_evidence_updated_at BEFORE UPDATE ON evidence
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, performed_by, changes)
        VALUES (TG_TABLE_NAME, OLD.case_id, TG_OP, current_user, row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, performed_by, changes)
        VALUES (TG_TABLE_NAME, NEW.case_id, TG_OP, current_user, 
                jsonb_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW)));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, performed_by, changes)
        VALUES (TG_TABLE_NAME, NEW.case_id, TG_OP, current_user, row_to_json(NEW));
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply audit triggers to critical tables
CREATE TRIGGER audit_cases AFTER INSERT OR UPDATE OR DELETE ON cases
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER audit_evidence AFTER INSERT OR UPDATE OR DELETE ON evidence
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER audit_chain_of_custody AFTER INSERT OR UPDATE OR DELETE ON chain_of_custody
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

-- Insert default tags
INSERT INTO tags (tag_name, category, color) VALUES
    ('urgent', 'priority', '#FF0000'),
    ('malware', 'threat', '#FF6600'),
    ('ransomware', 'threat', '#CC0000'),
    ('insider-threat', 'threat', '#9900CC'),
    ('data-breach', 'incident', '#FF3300'),
    ('phishing', 'threat', '#FF9900'),
    ('mobile', 'device', '#0066FF'),
    ('network', 'source', '#00CC66'),
    ('cloud', 'source', '#3399FF'),
    ('completed', 'status', '#00CC00')
ON CONFLICT (tag_name) DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW active_cases AS
SELECT 
    c.case_id,
    c.case_number,
    c.title,
    c.status,
    c.priority,
    c.lead_investigator,
    COUNT(DISTINCT e.evidence_id) as evidence_count,
    COUNT(DISTINCT ca.investigator_id) as investigator_count,
    c.created_at,
    c.updated_at
FROM cases c
LEFT JOIN evidence e ON c.case_id = e.case_id
LEFT JOIN case_assignments ca ON c.case_id = ca.case_id AND ca.active = true
WHERE c.status IN ('open', 'active')
GROUP BY c.case_id;

CREATE OR REPLACE VIEW evidence_with_custody AS
SELECT 
    e.evidence_id,
    e.evidence_number,
    e.description,
    e.evidence_type,
    e.status,
    e.collected_by,
    e.collected_at,
    COUNT(coc.custody_id) as custody_transfers,
    MAX(coc.performed_at) as last_custody_transfer
FROM evidence e
LEFT JOIN chain_of_custody coc ON e.evidence_id = coc.evidence_id
GROUP BY e.evidence_id;

-- Grant appropriate permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO forensics;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO forensics;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Forensics database initialized successfully!';
    RAISE NOTICE 'DOM_010101 - Chain of custody system ready';
END $$;
