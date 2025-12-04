-- ═══════════════════════════════════════════════════════════
-- 10D Chess Council - PostgreSQL Database Schema
-- Game state, agent registry, and training data storage
-- ═══════════════════════════════════════════════════════════

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════
-- Agent Registry
-- Stores information about each of the 640 agents
-- ═══════════════════════════════════════════════════════════
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) UNIQUE NOT NULL,
    board_layer INTEGER NOT NULL CHECK (board_layer >= 0 AND board_layer <= 9),
    position INTEGER NOT NULL CHECK (position >= 0 AND position < 64),
    row_num INTEGER NOT NULL CHECK (row_num >= 0 AND row_num < 8),
    col_num INTEGER NOT NULL CHECK (col_num >= 0 AND col_num < 8),
    frequency_hz DECIMAL(10, 2) NOT NULL,
    layer_name VARCHAR(100) NOT NULL,
    specialty TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast layer lookups
CREATE INDEX idx_agents_board_layer ON agents(board_layer);
CREATE INDEX idx_agents_frequency ON agents(frequency_hz);
CREATE INDEX idx_agents_status ON agents(status);

-- ═══════════════════════════════════════════════════════════
-- Games Table
-- Records all adversarial research games
-- ═══════════════════════════════════════════════════════════
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    game_id UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    game_type VARCHAR(100) NOT NULL,
    topic TEXT,
    status VARCHAR(50) DEFAULT 'in_progress' CHECK (status IN ('pending', 'in_progress', 'completed', 'abandoned')),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    winner_agent_id VARCHAR(100) REFERENCES agents(agent_id),
    final_score JSONB,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_games_type ON games(game_type);
CREATE INDEX idx_games_started_at ON games(started_at);

-- ═══════════════════════════════════════════════════════════
-- Game Participants
-- Links agents to games with their roles and scores
-- ═══════════════════════════════════════════════════════════
CREATE TABLE game_participants (
    id SERIAL PRIMARY KEY,
    game_id UUID REFERENCES games(game_id) ON DELETE CASCADE,
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    role VARCHAR(50) DEFAULT 'player',
    team VARCHAR(50),
    score INTEGER DEFAULT 0,
    join_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leave_time TIMESTAMP,
    UNIQUE(game_id, agent_id)
);

CREATE INDEX idx_participants_game ON game_participants(game_id);
CREATE INDEX idx_participants_agent ON game_participants(agent_id);

-- ═══════════════════════════════════════════════════════════
-- Game Moves
-- Records every move (citation, claim, refutation) in a game
-- ═══════════════════════════════════════════════════════════
CREATE TABLE game_moves (
    id SERIAL PRIMARY KEY,
    game_id UUID REFERENCES games(game_id) ON DELETE CASCADE,
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    turn_number INTEGER NOT NULL,
    move_type VARCHAR(50) NOT NULL CHECK (move_type IN ('cite_paper', 'make_claim', 'refute_claim', 'synthesize', 'verify')),
    action TEXT NOT NULL,
    claim TEXT,
    citation_doi VARCHAR(255),
    citation_title TEXT,
    citation_authors TEXT[],
    citation_year INTEGER,
    points_earned INTEGER DEFAULT 0,
    stockfish_score DECIMAL(5, 2),
    verification_status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_moves_game ON game_moves(game_id);
CREATE INDEX idx_moves_agent ON game_moves(agent_id);
CREATE INDEX idx_moves_type ON game_moves(move_type);
CREATE INDEX idx_moves_doi ON game_moves(citation_doi);

-- ═══════════════════════════════════════════════════════════
-- Generated Papers
-- Research papers synthesized from winning games
-- ═══════════════════════════════════════════════════════════
CREATE TABLE papers (
    id SERIAL PRIMARY KEY,
    paper_id UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(game_id),
    title TEXT NOT NULL,
    abstract TEXT,
    content TEXT,
    latex_source TEXT,
    arxiv_id VARCHAR(50),
    doi VARCHAR(255),
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'submitted', 'published', 'rejected')),
    keywords TEXT[],
    subject_areas TEXT[],
    peer_review_score DECIMAL(3, 2),
    citation_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    published_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_papers_status ON papers(status);
CREATE INDEX idx_papers_arxiv ON papers(arxiv_id);
CREATE INDEX idx_papers_game ON papers(game_id);

-- ═══════════════════════════════════════════════════════════
-- Citations Used in Papers
-- Bibliography entries for generated papers
-- ═══════════════════════════════════════════════════════════
CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    paper_id UUID REFERENCES papers(paper_id) ON DELETE CASCADE,
    doi VARCHAR(255),
    title TEXT NOT NULL,
    authors TEXT[],
    year INTEGER,
    source VARCHAR(100),
    journal VARCHAR(255),
    volume VARCHAR(50),
    pages VARCHAR(50),
    url TEXT,
    verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMP,
    bibtex TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_citations_paper ON citations(paper_id);
CREATE INDEX idx_citations_doi ON citations(doi);

-- ═══════════════════════════════════════════════════════════
-- Training Data
-- (state, action, reward) tuples for agent fine-tuning
-- ═══════════════════════════════════════════════════════════
CREATE TABLE training_data (
    id SERIAL PRIMARY KEY,
    game_id UUID REFERENCES games(game_id) ON DELETE SET NULL,
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    state JSONB NOT NULL,
    action JSONB NOT NULL,
    reward DECIMAL(10, 4) NOT NULL,
    next_state JSONB,
    episode_id VARCHAR(100),
    step_number INTEGER,
    is_terminal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_training_game ON training_data(game_id);
CREATE INDEX idx_training_agent ON training_data(agent_id);
CREATE INDEX idx_training_episode ON training_data(episode_id);
CREATE INDEX idx_training_reward ON training_data(reward);

-- ═══════════════════════════════════════════════════════════
-- Agent Performance Metrics
-- Historical performance tracking
-- ═══════════════════════════════════════════════════════════
CREATE TABLE agent_metrics (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) REFERENCES agents(agent_id),
    metric_date DATE NOT NULL,
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    citations_generated INTEGER DEFAULT 0,
    papers_published INTEGER DEFAULT 0,
    avg_stockfish_score DECIMAL(5, 2),
    win_rate DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, metric_date)
);

CREATE INDEX idx_metrics_agent ON agent_metrics(agent_id);
CREATE INDEX idx_metrics_date ON agent_metrics(metric_date);

-- ═══════════════════════════════════════════════════════════
-- Echolocation Events
-- Agent discovery and coalition formation
-- ═══════════════════════════════════════════════════════════
CREATE TABLE echolocation_events (
    id SERIAL PRIMARY KEY,
    initiator_agent_id VARCHAR(100) REFERENCES agents(agent_id),
    target_frequency DECIMAL(10, 2) NOT NULL,
    interval_type VARCHAR(50) NOT NULL,
    responders VARCHAR(100)[],
    coalition_formed BOOLEAN DEFAULT FALSE,
    coalition_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_echolocation_initiator ON echolocation_events(initiator_agent_id);
CREATE INDEX idx_echolocation_coalition ON echolocation_events(coalition_id);

-- ═══════════════════════════════════════════════════════════
-- Helper Functions
-- ═══════════════════════════════════════════════════════════

-- Function to calculate agent frequency
CREATE OR REPLACE FUNCTION calculate_frequency(board INTEGER, row_num INTEGER, col_num INTEGER)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    position INTEGER;
    piano_key INTEGER;
    frequency DECIMAL(10, 2);
BEGIN
    position := board * 64 + row_num * 8 + col_num;
    piano_key := position % 88;
    frequency := 440 * POWER(2, (piano_key - 49)::DECIMAL / 12);
    RETURN ROUND(frequency, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to get layer name
CREATE OR REPLACE FUNCTION get_layer_name(layer_id INTEGER)
RETURNS VARCHAR(100) AS $$
BEGIN
    RETURN CASE layer_id
        WHEN 0 THEN 'Empirical Data'
        WHEN 1 THEN 'Data Preprocessing'
        WHEN 2 THEN 'Statistical Analysis'
        WHEN 3 THEN 'Knowledge Synthesis'
        WHEN 4 THEN 'Predictive Modeling'
        WHEN 5 THEN 'Strategic Reasoning'
        WHEN 6 THEN 'Ethical Evaluation'
        WHEN 7 THEN 'Linguistic Generation'
        WHEN 8 THEN 'Validation & Verification'
        WHEN 9 THEN 'Publication & Dissemination'
        ELSE 'Unknown'
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER agents_update_timestamp
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

-- ═══════════════════════════════════════════════════════════
-- Views for Common Queries
-- ═══════════════════════════════════════════════════════════

-- Agent leaderboard view
CREATE VIEW agent_leaderboard AS
SELECT 
    a.agent_id,
    a.board_layer,
    a.layer_name,
    a.frequency_hz,
    COALESCE(SUM(gp.score), 0) as total_score,
    COUNT(DISTINCT g.game_id) as games_played,
    COUNT(DISTINCT CASE WHEN g.winner_agent_id = a.agent_id THEN g.game_id END) as games_won,
    CASE 
        WHEN COUNT(DISTINCT g.game_id) > 0 
        THEN ROUND(COUNT(DISTINCT CASE WHEN g.winner_agent_id = a.agent_id THEN g.game_id END)::DECIMAL / COUNT(DISTINCT g.game_id), 4)
        ELSE 0 
    END as win_rate
FROM agents a
LEFT JOIN game_participants gp ON a.agent_id = gp.agent_id
LEFT JOIN games g ON gp.game_id = g.game_id AND g.status = 'completed'
GROUP BY a.agent_id, a.board_layer, a.layer_name, a.frequency_hz
ORDER BY total_score DESC;

-- Recent games view
CREATE VIEW recent_games AS
SELECT 
    g.game_id,
    g.game_type,
    g.topic,
    g.status,
    g.started_at,
    g.ended_at,
    g.winner_agent_id,
    array_agg(DISTINCT gp.agent_id) as participants,
    COUNT(gm.id) as total_moves
FROM games g
LEFT JOIN game_participants gp ON g.game_id = gp.game_id
LEFT JOIN game_moves gm ON g.game_id = gm.game_id
GROUP BY g.game_id, g.game_type, g.topic, g.status, g.started_at, g.ended_at, g.winner_agent_id
ORDER BY g.started_at DESC;

-- ═══════════════════════════════════════════════════════════
-- Initialize 640 Agents (Optional - Run after deployment)
-- ═══════════════════════════════════════════════════════════

-- This can be run to pre-populate the agents table
-- DO $$
-- DECLARE
--     board INTEGER;
--     row_num INTEGER;
--     col_num INTEGER;
--     cols CHAR[] := ARRAY['A','B','C','D','E','F','G','H'];
--     agent_id VARCHAR(100);
--     freq DECIMAL(10, 2);
--     layer VARCHAR(100);
-- BEGIN
--     FOR board IN 0..9 LOOP
--         FOR row_num IN 0..7 LOOP
--             FOR col_num IN 0..7 LOOP
--                 agent_id := 'chess-board-' || board || '-' || (row_num * 8 + col_num);
--                 freq := calculate_frequency(board, row_num, col_num);
--                 layer := get_layer_name(board);
--                 
--                 INSERT INTO agents (agent_id, board_layer, position, row_num, col_num, frequency_hz, layer_name)
--                 VALUES (agent_id, board, row_num * 8 + col_num, row_num, col_num, freq, layer)
--                 ON CONFLICT (agent_id) DO NOTHING;
--             END LOOP;
--         END LOOP;
--     END LOOP;
-- END $$;
