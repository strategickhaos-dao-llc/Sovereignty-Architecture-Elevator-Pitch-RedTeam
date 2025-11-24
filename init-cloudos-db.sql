-- CloudOS Database Initialization
CREATE DATABASE keycloak;
CREATE DATABASE synapse;

-- Create users for services  
CREATE USER keycloak WITH PASSWORD 'keycloak_password';
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;

CREATE USER synapse WITH PASSWORD 'synapse_password';
GRANT ALL PRIVILEGES ON DATABASE synapse TO synapse;

-- Strategic Khaos schema
\c strategickhaos;

CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS refinory;
CREATE SCHEMA IF NOT EXISTS contradictions;

-- Basic tables for AI system
CREATE TABLE IF NOT EXISTS public.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS refinory.experts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contradictions.revenue_streams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hook TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    pricing TEXT NOT NULL,
    proof TEXT,
    demo_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial contradiction data
INSERT INTO contradictions.revenue_streams (name, hook, mechanism, pricing, proof, demo_url) VALUES
('Privacy vs Personalization', 'Tailored for you — never tracked.', 'On-device embeddings + zero-knowledge sync', '$0 logs → $9/mo for cross-device sync (E2EE)', 'curl /metrics | grep logs=0', 'https://demo.strategickhaos.com/privacy'),
('Speed vs Security', 'Login in 1.2s — or we pay you.', 'WebAuthn + risk engine (IP velocity, device fingerprint)', '$0.01 per failed step-up (SLO: 99.9% <2s)', 'Grafana: login_latency_p99', 'https://demo.strategickhaos.com/speed'),
('Simple vs Powerful', 'One click. Infinite possibilities.', 'Progressive disclosure + AI intent prediction', 'Free basics → $19/mo for power features', 'Feature usage analytics dashboard', 'https://demo.strategickhaos.com/progressive')
ON CONFLICT DO NOTHING;
