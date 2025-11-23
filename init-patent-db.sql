-- init-patent-db.sql
-- Initialize Patent Office and Google Scholar Database

-- Create patents table
CREATE TABLE IF NOT EXISTS patents (
    id SERIAL PRIMARY KEY,
    patent_number VARCHAR(50) UNIQUE,
    title TEXT NOT NULL,
    abstract TEXT,
    filing_date DATE,
    grant_date DATE,
    status VARCHAR(50),
    office VARCHAR(20),
    inventors TEXT[],
    assignees TEXT[],
    classifications TEXT[],
    sha256_hash VARCHAR(64),
    gpg_signature TEXT,
    ots_proof TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patents_number ON patents(patent_number);
CREATE INDEX idx_patents_status ON patents(status);
CREATE INDEX idx_patents_filing_date ON patents(filing_date);

-- Create patent applications tracking
CREATE TABLE IF NOT EXISTS patent_applications (
    id SERIAL PRIMARY KEY,
    application_number VARCHAR(50) UNIQUE,
    title TEXT NOT NULL,
    abstract TEXT,
    filing_date DATE,
    status VARCHAR(50),
    office VARCHAR(20),
    inventors TEXT[],
    assignees TEXT[],
    sha256_hash VARCHAR(64),
    gpg_signature TEXT,
    ots_proof TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_applications_number ON patent_applications(application_number);
CREATE INDEX idx_applications_status ON patent_applications(status);

-- Create prior art references
CREATE TABLE IF NOT EXISTS prior_art (
    id SERIAL PRIMARY KEY,
    reference_type VARCHAR(50),
    reference_id VARCHAR(100),
    title TEXT NOT NULL,
    abstract TEXT,
    publication_date DATE,
    authors TEXT[],
    source VARCHAR(100),
    url TEXT,
    relevance_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prior_art_type ON prior_art(reference_type);
CREATE INDEX idx_prior_art_pub_date ON prior_art(publication_date);

-- Create scholar papers table
CREATE TABLE IF NOT EXISTS scholar_papers (
    id SERIAL PRIMARY KEY,
    paper_id VARCHAR(100) UNIQUE,
    doi VARCHAR(100),
    title TEXT NOT NULL,
    abstract TEXT,
    authors TEXT[],
    publication_date DATE,
    venue VARCHAR(255),
    citation_count INTEGER DEFAULT 0,
    pdf_url TEXT,
    bibtex TEXT,
    keywords TEXT[],
    research_area VARCHAR(100),
    downloaded BOOLEAN DEFAULT FALSE,
    embedded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_papers_paper_id ON scholar_papers(paper_id);
CREATE INDEX idx_papers_doi ON scholar_papers(doi);
CREATE INDEX idx_papers_pub_date ON scholar_papers(publication_date);
CREATE INDEX idx_papers_research_area ON scholar_papers(research_area);

-- Create citations table
CREATE TABLE IF NOT EXISTS citations (
    id SERIAL PRIMARY KEY,
    citing_paper_id VARCHAR(100),
    cited_paper_id VARCHAR(100),
    citation_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (citing_paper_id) REFERENCES scholar_papers(paper_id),
    FOREIGN KEY (cited_paper_id) REFERENCES scholar_papers(paper_id)
);

CREATE INDEX idx_citations_citing ON citations(citing_paper_id);
CREATE INDEX idx_citations_cited ON citations(cited_paper_id);

-- Create authors table
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    author_id VARCHAR(100) UNIQUE,
    name VARCHAR(255) NOT NULL,
    affiliation VARCHAR(255),
    h_index INTEGER,
    i10_index INTEGER,
    total_citations INTEGER,
    url TEXT,
    tracked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_authors_name ON authors(name);
CREATE INDEX idx_authors_tracked ON authors(tracked);

-- Create monitoring alerts table
CREATE TABLE IF NOT EXISTS monitoring_alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50),
    entity_type VARCHAR(50),
    entity_id VARCHAR(100),
    title TEXT,
    description TEXT,
    severity VARCHAR(20),
    status VARCHAR(20) DEFAULT 'new',
    notified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE INDEX idx_alerts_type ON monitoring_alerts(alert_type);
CREATE INDEX idx_alerts_status ON monitoring_alerts(status);
CREATE INDEX idx_alerts_created ON monitoring_alerts(created_at);

-- Create audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    entity_type VARCHAR(50),
    entity_id VARCHAR(100),
    user_id VARCHAR(100),
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);

-- Create sovereign manifest verification table
CREATE TABLE IF NOT EXISTS sovereign_verifications (
    id SERIAL PRIMARY KEY,
    manifest_hash VARCHAR(64) NOT NULL,
    verification_type VARCHAR(50),
    verification_status VARCHAR(20),
    verified_at TIMESTAMP,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default sovereign manifest record
INSERT INTO sovereign_verifications (manifest_hash, verification_type, verification_status, verified_at, details)
VALUES (
    'FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED',
    'initial',
    'verified',
    CURRENT_TIMESTAMP,
    '{"methods": ["GPG", "OpenTimestamps", "GitHub", "Obsidian"], "status": "Empire eternal"}'::JSONB
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Create view for active patents
CREATE OR REPLACE VIEW active_patents AS
SELECT 
    p.*,
    COUNT(pa.id) as prior_art_count
FROM patents p
LEFT JOIN prior_art pa ON pa.reference_id = p.patent_number
WHERE p.status IN ('granted', 'active', 'pending')
GROUP BY p.id;

-- Create view for recent papers
CREATE OR REPLACE VIEW recent_papers AS
SELECT 
    sp.*,
    a.name as first_author_name,
    a.affiliation as first_author_affiliation
FROM scholar_papers sp
LEFT JOIN authors a ON a.name = sp.authors[1]
WHERE sp.publication_date >= CURRENT_DATE - INTERVAL '2 years'
ORDER BY sp.publication_date DESC;

-- Create view for high impact papers
CREATE OR REPLACE VIEW high_impact_papers AS
SELECT 
    sp.*,
    COUNT(c.id) as incoming_citations
FROM scholar_papers sp
LEFT JOIN citations c ON c.cited_paper_id = sp.paper_id
WHERE sp.citation_count >= 5
GROUP BY sp.id
ORDER BY sp.citation_count DESC;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Patent Office & Google Scholar database initialized successfully';
    RAISE NOTICE 'Sovereign Manifest Hash: FAA198DA05318742531B6405384319563933F63DB4D91866E70AE7701FCDCDED';
    RAISE NOTICE 'Status: Empire eternal';
END $$;
