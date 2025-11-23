-- Database initialization for invite-only website

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    invited_by INTEGER REFERENCES users(id)
);

-- Create invitations table
CREATE TABLE IF NOT EXISTS invitations (
    id SERIAL PRIMARY KEY,
    invite_code VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    invited_by INTEGER REFERENCES users(id),
    used BOOLEAN DEFAULT false,
    used_by INTEGER REFERENCES users(id),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sessions table for user sessions
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create LLM conversation history table
CREATE TABLE IF NOT EXISTS llm_conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    conversation_id UUID DEFAULT gen_random_uuid(),
    message_role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    message_content TEXT NOT NULL,
    model VARCHAR(100),
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_invitations_code ON invitations(invite_code);
CREATE INDEX IF NOT EXISTS idx_invitations_email ON invitations(email);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_llm_conversations_user_id ON llm_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_llm_conversations_conversation_id ON llm_conversations(conversation_id);

-- Create initial admin user (password: admin123 - CHANGE THIS IN PRODUCTION)
-- Password hash is bcrypt hash of 'admin123'
INSERT INTO users (email, username, password_hash, role) 
VALUES ('admin@localhost', 'admin', '$2b$10$rKvVPGYEqKN5xqKqZLR4ReJ9H.h2FXqKuHYzqLZoJqLqKtZLLLLLe', 'admin')
ON CONFLICT (email) DO NOTHING;
