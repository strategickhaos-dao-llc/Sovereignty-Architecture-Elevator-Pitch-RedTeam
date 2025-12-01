-- Chess Council Database Schema
-- PostgreSQL initialization script for game logs and agent state

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ═══════════════════════════════════════════════════════════
-- AGENTS TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(64) UNIQUE NOT NULL,
    board_layer INTEGER NOT NULL CHECK (board_layer >= 0 AND board_layer <= 9),
    position INTEGER NOT NULL CHECK (position >= 0 AND position < 64),
    frequency_hz DECIMAL(10, 2) NOT NULL,
    note_name VARCHAR(8) NOT NULL,
    piano_key INTEGER NOT NULL CHECK (piano_key >= 1 AND piano_key <= 88),
    status VARCHAR(32) DEFAULT 'idle',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_board_position UNIQUE (board_layer, position)
);

CREATE INDEX idx_agents_board ON agents(board_layer);
CREATE INDEX idx_agents_frequency ON agents(frequency_hz);
CREATE INDEX idx_agents_status ON agents(status);

-- ═══════════════════════════════════════════════════════════
-- GAMES TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_type VARCHAR(64) NOT NULL,
    topic VARCHAR(256),
    status VARCHAR(32) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    winner_agent_id UUID REFERENCES agents(id),
    final_score_a INTEGER DEFAULT 0,
    final_score_b INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_games_type ON games(game_type);
CREATE INDEX idx_games_topic ON games(topic);

-- ═══════════════════════════════════════════════════════════
-- GAME PARTICIPANTS TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE game_participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id),
    side VARCHAR(8) NOT NULL CHECK (side IN ('A', 'B')),
    score INTEGER DEFAULT 0,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_game_side UNIQUE (game_id, side),
    CONSTRAINT unique_agent_game UNIQUE (game_id, agent_id)
);

CREATE INDEX idx_participants_game ON game_participants(game_id);
CREATE INDEX idx_participants_agent ON game_participants(agent_id);

-- ═══════════════════════════════════════════════════════════
-- MOVES TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE moves (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id),
    turn_number INTEGER NOT NULL,
    move_type VARCHAR(32) NOT NULL,
    action JSONB NOT NULL,
    score_delta INTEGER DEFAULT 0,
    evaluation JSONB,
    valid BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_game_turn UNIQUE (game_id, turn_number)
);

CREATE INDEX idx_moves_game ON moves(game_id);
CREATE INDEX idx_moves_agent ON moves(agent_id);
CREATE INDEX idx_moves_type ON moves(move_type);

-- ═══════════════════════════════════════════════════════════
-- CITATIONS TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE citations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    move_id UUID REFERENCES moves(id) ON DELETE CASCADE,
    doi VARCHAR(256),
    arxiv_id VARCHAR(64),
    title TEXT NOT NULL,
    authors TEXT[],
    publication_year INTEGER,
    source VARCHAR(64),
    abstract TEXT,
    url TEXT,
    embedding_vector BYTEA,
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_citations_doi ON citations(doi);
CREATE INDEX idx_citations_arxiv ON citations(arxiv_id);
CREATE INDEX idx_citations_move ON citations(move_id);

-- ═══════════════════════════════════════════════════════════
-- CLAIMS TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    move_id UUID NOT NULL REFERENCES moves(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    supporting_citations UUID[],
    refuted_by_move_id UUID REFERENCES moves(id),
    status VARCHAR(32) DEFAULT 'pending',
    confidence DECIMAL(5, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_claims_move ON claims(move_id);
CREATE INDEX idx_claims_status ON claims(status);

-- ═══════════════════════════════════════════════════════════
-- PAPERS TABLE (Generated research papers)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE papers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id),
    title TEXT NOT NULL,
    abstract TEXT,
    content TEXT,
    latex_source TEXT,
    pdf_path VARCHAR(512),
    arxiv_id VARCHAR(64),
    status VARCHAR(32) DEFAULT 'draft',
    peer_review_score DECIMAL(5, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_papers_game ON papers(game_id);
CREATE INDEX idx_papers_arxiv ON papers(arxiv_id);
CREATE INDEX idx_papers_status ON papers(status);

-- ═══════════════════════════════════════════════════════════
-- TRAINING DATA TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE training_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID NOT NULL REFERENCES games(id),
    move_id UUID NOT NULL REFERENCES moves(id),
    state JSONB NOT NULL,
    action JSONB NOT NULL,
    reward DECIMAL(10, 4) NOT NULL,
    outcome VARCHAR(64),
    used_in_training BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_training_game ON training_data(game_id);
CREATE INDEX idx_training_used ON training_data(used_in_training);

-- ═══════════════════════════════════════════════════════════
-- HARMONIC PARTNERSHIPS TABLE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE harmonic_partnerships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_a_id UUID NOT NULL REFERENCES agents(id),
    agent_b_id UUID NOT NULL REFERENCES agents(id),
    relationship VARCHAR(32) NOT NULL,
    frequency_ratio DECIMAL(6, 4) NOT NULL,
    collaboration_score DECIMAL(5, 2) DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_partnership UNIQUE (agent_a_id, agent_b_id)
);

CREATE INDEX idx_partnerships_agent ON harmonic_partnerships(agent_a_id);

-- ═══════════════════════════════════════════════════════════
-- FUNCTIONS
-- ═══════════════════════════════════════════════════════════

-- Function to calculate frequency from board position
CREATE OR REPLACE FUNCTION calculate_frequency(board_layer INTEGER, position INTEGER)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    global_position INTEGER;
    piano_key INTEGER;
    frequency DECIMAL(10, 2);
BEGIN
    global_position := board_layer * 64 + position;
    piano_key := global_position % 88;
    frequency := 440.0 * POWER(2, (piano_key - 49)::DECIMAL / 12.0);
    RETURN ROUND(frequency, 2);
END;
$$ LANGUAGE plpgsql;

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for agents table
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- ═══════════════════════════════════════════════════════════
-- VIEWS
-- ═══════════════════════════════════════════════════════════

-- View for active games
CREATE VIEW active_games AS
SELECT 
    g.id,
    g.game_type,
    g.topic,
    g.started_at,
    a.agent_id AS agent_a,
    b.agent_id AS agent_b,
    gp_a.score AS score_a,
    gp_b.score AS score_b
FROM games g
JOIN game_participants gp_a ON g.id = gp_a.game_id AND gp_a.side = 'A'
JOIN game_participants gp_b ON g.id = gp_b.game_id AND gp_b.side = 'B'
JOIN agents a ON gp_a.agent_id = a.id
JOIN agents b ON gp_b.agent_id = b.id
WHERE g.status = 'active';

-- View for agent performance
CREATE VIEW agent_performance AS
SELECT 
    a.id,
    a.agent_id,
    a.board_layer,
    COUNT(DISTINCT gp.game_id) AS games_played,
    COUNT(DISTINCT CASE WHEN g.winner_agent_id = a.id THEN g.id END) AS games_won,
    COALESCE(SUM(m.score_delta), 0) AS total_score
FROM agents a
LEFT JOIN game_participants gp ON a.id = gp.agent_id
LEFT JOIN games g ON gp.game_id = g.id
LEFT JOIN moves m ON a.id = m.agent_id
GROUP BY a.id, a.agent_id, a.board_layer;

-- ═══════════════════════════════════════════════════════════
-- SEED DATA - Sample agents for layers
-- ═══════════════════════════════════════════════════════════
INSERT INTO agents (agent_id, board_layer, position, frequency_hz, note_name, piano_key)
SELECT 
    'agent-' || (layer * 64 + pos),
    layer,
    pos,
    calculate_frequency(layer, pos),
    CASE ((layer * 64 + pos) % 12)
        WHEN 0 THEN 'A'
        WHEN 1 THEN 'A#'
        WHEN 2 THEN 'B'
        WHEN 3 THEN 'C'
        WHEN 4 THEN 'C#'
        WHEN 5 THEN 'D'
        WHEN 6 THEN 'D#'
        WHEN 7 THEN 'E'
        WHEN 8 THEN 'F'
        WHEN 9 THEN 'F#'
        WHEN 10 THEN 'G'
        WHEN 11 THEN 'G#'
    END || (((layer * 64 + pos) % 88 + 8) / 12),
    -- Piano keys are 1-88; use modulo and add 1 to ensure valid range
    ((layer * 64 + pos) % 88) + 1
FROM generate_series(0, 9) AS layer
CROSS JOIN generate_series(0, 3) AS pos  -- Only 4 agents per layer for dev
ON CONFLICT DO NOTHING;
