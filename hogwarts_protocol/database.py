"""
Hogwarts Protocol Database Layer

PostgreSQL schema and operations for the educational blockchain system.
Provides off-chain storage with on-chain synchronization hooks.
"""

import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List, Optional, Any
import asyncpg
import structlog

from .models import (
    Student, Course, Assignment, Spell, CFTBalance, 
    CFTTransaction, RevenueRoute, SpellLicense,
    SpellStatus, CFTTransactionType, RevenueRouteType
)

logger = structlog.get_logger()


class HogwartsDatabase:
    """Database connection and operations for Hogwarts Protocol"""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool and schema"""
        logger.info("Initializing Hogwarts Protocol database")
        
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        
        await self._create_schema()
        logger.info("Hogwarts Protocol database initialized")
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Hogwarts Protocol database connection closed")
    
    async def health_check(self):
        """Check database connectivity"""
        if not self.pool:
            raise Exception("Database not initialized")
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval("SELECT 1")
            if result != 1:
                raise Exception("Database health check failed")
    
    async def _create_schema(self):
        """Create Hogwarts Protocol database schema"""
        schema_sql = """
        -- ============================================
        -- HOGWARTS PROTOCOL SCHEMA
        -- The Great Hall Ledger - Off-Chain Storage
        -- ============================================
        
        -- Enable required extensions
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        
        -- ============================================
        -- STUDENTS TABLE
        -- Educational identity with wallet integration
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_students (
            student_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            
            -- Educational identity
            edu_email VARCHAR(255),
            edu_institution VARCHAR(255),
            display_name VARCHAR(255),
            
            -- Blockchain identity
            wallet_address VARCHAR(42),          -- Ethereum address (0x + 40 hex chars)
            wallet_nonce INTEGER DEFAULT 0,      -- For signature verification
            
            -- Profile
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Computed stats (denormalized for performance)
            total_spells INTEGER DEFAULT 0,
            total_cft NUMERIC(36, 18) DEFAULT 0,
            governance_weight NUMERIC(36, 18) DEFAULT 0,
            
            -- Constraints
            CONSTRAINT unique_edu_email UNIQUE (edu_email),
            CONSTRAINT unique_wallet_address UNIQUE (wallet_address),
            CONSTRAINT valid_wallet_address CHECK (
                wallet_address IS NULL OR 
                wallet_address ~ '^0x[a-fA-F0-9]{40}$'
            )
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_students_wallet ON hp_students(wallet_address);
        CREATE INDEX IF NOT EXISTS idx_hp_students_edu ON hp_students(edu_email);
        
        -- ============================================
        -- COURSES TABLE
        -- Educational modules and programs
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_courses (
            course_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            
            -- Course identification
            course_code VARCHAR(50) NOT NULL,    -- e.g., "MAT-243"
            course_name VARCHAR(255) NOT NULL,
            institution VARCHAR(255),             -- e.g., "SNHU"
            
            -- Course metadata
            description TEXT,
            learning_outcomes JSONB DEFAULT '[]',
            
            -- Platform configuration
            platform VARCHAR(100) DEFAULT 'CourseQuest Hogwarts',
            xp_multiplier NUMERIC(5, 2) DEFAULT 1.0,
            
            -- Revenue configuration
            instructor_share_pct NUMERIC(5, 4) DEFAULT 0.10,  -- 10%
            
            -- Timestamps
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            start_date TIMESTAMP WITH TIME ZONE,
            end_date TIMESTAMP WITH TIME ZONE,
            is_active BOOLEAN DEFAULT TRUE,
            
            -- Constraints
            CONSTRAINT unique_course_code_institution UNIQUE (course_code, institution)
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_courses_code ON hp_courses(course_code);
        CREATE INDEX IF NOT EXISTS idx_hp_courses_institution ON hp_courses(institution);
        
        -- ============================================
        -- ASSIGNMENTS TABLE
        -- Specific tasks within courses
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_assignments (
            assignment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            course_id UUID NOT NULL REFERENCES hp_courses(course_id) ON DELETE CASCADE,
            
            -- Assignment details
            assignment_name VARCHAR(255) NOT NULL,
            assignment_code VARCHAR(50),
            description TEXT,
            
            -- Rubric
            rubric_url VARCHAR(500),
            requirements JSONB DEFAULT '[]',
            
            -- XP configuration
            base_xp INTEGER DEFAULT 100,
            max_grade_bonus NUMERIC(5, 2) DEFAULT 0.5,  -- 50% bonus for top grade
            
            -- Timestamps
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            due_date TIMESTAMP WITH TIME ZONE,
            is_active BOOLEAN DEFAULT TRUE
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_assignments_course ON hp_assignments(course_id);
        
        -- ============================================
        -- SPELLS TABLE
        -- Educational artifacts (code submissions)
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_spells (
            spell_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            
            -- Ownership
            owner_id UUID NOT NULL REFERENCES hp_students(student_id) ON DELETE CASCADE,
            
            -- Course linkage
            course_id UUID REFERENCES hp_courses(course_id),
            assignment_id UUID REFERENCES hp_assignments(assignment_id),
            
            -- Spell content
            spell_name VARCHAR(255) NOT NULL,
            spell_type VARCHAR(50) DEFAULT 'python',
            content_hash VARCHAR(64),             -- SHA-256 hash
            file_path VARCHAR(500),               -- Storage path
            
            -- Verification status
            status VARCHAR(20) DEFAULT 'draft',
            grade VARCHAR(10),                    -- e.g., "B+", "A"
            grade_numeric NUMERIC(4, 2),          -- e.g., 3.3, 4.0
            verified_at TIMESTAMP WITH TIME ZONE,
            verified_by UUID REFERENCES hp_students(student_id),
            
            -- On-chain registration
            on_chain_tx_hash VARCHAR(66),         -- Transaction hash (0x + 64 hex)
            on_chain_token_id BIGINT,             -- NFT/SBT token ID
            chain_id INTEGER,                     -- Network ID
            
            -- CFT earned
            xp_earned INTEGER DEFAULT 0,
            cft_minted NUMERIC(36, 18) DEFAULT 0,
            
            -- Marketplace
            is_licensable BOOLEAN DEFAULT FALSE,
            license_price NUMERIC(18, 2),         -- Fiat price
            total_licenses_sold INTEGER DEFAULT 0,
            total_revenue NUMERIC(18, 2) DEFAULT 0,
            
            -- Timestamps
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Metadata (extensible)
            metadata JSONB DEFAULT '{}',
            
            -- Constraints
            CONSTRAINT valid_status CHECK (
                status IN ('draft', 'submitted', 'verified', 'certified', 'revoked')
            ),
            CONSTRAINT valid_content_hash CHECK (
                content_hash IS NULL OR 
                content_hash ~ '^[a-fA-F0-9]{64}$'
            )
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_spells_owner ON hp_spells(owner_id);
        CREATE INDEX IF NOT EXISTS idx_hp_spells_course ON hp_spells(course_id);
        CREATE INDEX IF NOT EXISTS idx_hp_spells_assignment ON hp_spells(assignment_id);
        CREATE INDEX IF NOT EXISTS idx_hp_spells_status ON hp_spells(status);
        CREATE INDEX IF NOT EXISTS idx_hp_spells_content_hash ON hp_spells(content_hash);
        CREATE INDEX IF NOT EXISTS idx_hp_spells_chain ON hp_spells(chain_id, on_chain_token_id);
        
        -- ============================================
        -- CFT BALANCES TABLE
        -- CourseForge Token accounting
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_cft_balances (
            balance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            student_id UUID NOT NULL REFERENCES hp_students(student_id) ON DELETE CASCADE,
            
            -- Balances (using high precision for token accounting)
            available_balance NUMERIC(36, 18) DEFAULT 0,   -- Spendable
            staked_balance NUMERIC(36, 18) DEFAULT 0,      -- Governance locked
            lifetime_earned NUMERIC(36, 18) DEFAULT 0,     -- Total ever minted
            
            -- Timestamps
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- One balance record per student
            CONSTRAINT unique_student_balance UNIQUE (student_id),
            
            -- Non-negative balances
            CONSTRAINT non_negative_available CHECK (available_balance >= 0),
            CONSTRAINT non_negative_staked CHECK (staked_balance >= 0),
            CONSTRAINT non_negative_lifetime CHECK (lifetime_earned >= 0)
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_cft_balances_student ON hp_cft_balances(student_id);
        
        -- ============================================
        -- CFT TRANSACTIONS TABLE
        -- Token movement audit trail
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_cft_transactions (
            transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            
            -- Participants
            student_id UUID NOT NULL REFERENCES hp_students(student_id),
            from_balance UUID REFERENCES hp_cft_balances(balance_id),
            to_balance UUID REFERENCES hp_cft_balances(balance_id),
            
            -- Transaction details
            transaction_type VARCHAR(20) NOT NULL,
            amount NUMERIC(36, 18) NOT NULL,
            
            -- Reference to source event
            reference_type VARCHAR(50),           -- e.g., "spell", "governance", "fee"
            reference_id UUID,                    -- Related entity ID
            reason VARCHAR(500),                  -- Human-readable
            
            -- Timestamp
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- On-chain reference
            on_chain_tx_hash VARCHAR(66),
            
            -- Constraints
            CONSTRAINT valid_transaction_type CHECK (
                transaction_type IN ('mint', 'burn', 'transfer', 'stake', 'unstake', 'reward', 'fee')
            ),
            CONSTRAINT positive_amount CHECK (amount > 0)
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_cft_transactions_student ON hp_cft_transactions(student_id);
        CREATE INDEX IF NOT EXISTS idx_hp_cft_transactions_type ON hp_cft_transactions(transaction_type);
        CREATE INDEX IF NOT EXISTS idx_hp_cft_transactions_created ON hp_cft_transactions(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_hp_cft_transactions_reference ON hp_cft_transactions(reference_type, reference_id);
        
        -- ============================================
        -- REVENUE ROUTES TABLE
        -- How money flows for spell licensing
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_revenue_routes (
            route_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            spell_id UUID NOT NULL REFERENCES hp_spells(spell_id) ON DELETE CASCADE,
            
            -- Route configuration
            route_type VARCHAR(20) NOT NULL,
            recipient_id VARCHAR(100),            -- Student/pool ID
            recipient_address VARCHAR(42),        -- Wallet for payout
            percentage NUMERIC(5, 2) NOT NULL,    -- 0-100
            
            -- Totals
            total_received NUMERIC(18, 2) DEFAULT 0,
            pending_payout NUMERIC(18, 2) DEFAULT 0,
            
            -- Timestamps
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            
            -- Constraints
            CONSTRAINT valid_route_type CHECK (
                route_type IN ('creator', 'platform', 'charity', 'instructor', 'scholarship')
            ),
            CONSTRAINT valid_percentage CHECK (percentage >= 0 AND percentage <= 100)
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_revenue_routes_spell ON hp_revenue_routes(spell_id);
        CREATE INDEX IF NOT EXISTS idx_hp_revenue_routes_type ON hp_revenue_routes(route_type);
        
        -- ============================================
        -- SPELL LICENSES TABLE
        -- Marketplace transactions
        -- ============================================
        CREATE TABLE IF NOT EXISTS hp_spell_licenses (
            license_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            
            -- Spell being licensed
            spell_id UUID NOT NULL REFERENCES hp_spells(spell_id),
            
            -- Parties
            licensor_id UUID NOT NULL REFERENCES hp_students(student_id),  -- Owner
            licensee_id UUID NOT NULL REFERENCES hp_students(student_id),  -- Buyer
            
            -- Transaction details
            price_paid NUMERIC(18, 2) NOT NULL,
            payment_currency VARCHAR(10) DEFAULT 'USD',
            payment_processor VARCHAR(50) DEFAULT 'stripe',
            payment_reference VARCHAR(255),       -- External transaction ID
            
            -- License terms
            license_type VARCHAR(50) DEFAULT 'educational',
            expires_at TIMESTAMP WITH TIME ZONE,
            
            -- Timestamp
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_hp_spell_licenses_spell ON hp_spell_licenses(spell_id);
        CREATE INDEX IF NOT EXISTS idx_hp_spell_licenses_licensor ON hp_spell_licenses(licensor_id);
        CREATE INDEX IF NOT EXISTS idx_hp_spell_licenses_licensee ON hp_spell_licenses(licensee_id);
        
        -- ============================================
        -- TRANSCRIPT VIEW
        -- On-chain transcript representation
        -- ============================================
        CREATE OR REPLACE VIEW hp_transcript AS
        SELECT 
            s.student_id,
            st.display_name,
            st.wallet_address,
            st.edu_institution,
            c.course_code,
            c.course_name,
            a.assignment_name,
            s.spell_name,
            s.grade,
            s.grade_numeric,
            s.status,
            s.verified_at,
            s.on_chain_tx_hash,
            s.on_chain_token_id,
            s.xp_earned,
            s.cft_minted,
            s.content_hash
        FROM hp_spells s
        JOIN hp_students st ON s.owner_id = st.student_id
        LEFT JOIN hp_courses c ON s.course_id = c.course_id
        LEFT JOIN hp_assignments a ON s.assignment_id = a.assignment_id
        WHERE s.status IN ('verified', 'certified')
        ORDER BY s.verified_at DESC;
        
        -- ============================================
        -- TRIGGERS
        -- Automatic timestamp updates
        -- ============================================
        
        CREATE OR REPLACE FUNCTION hp_update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Apply to all tables with updated_at
        DROP TRIGGER IF EXISTS hp_students_updated_at ON hp_students;
        CREATE TRIGGER hp_students_updated_at
            BEFORE UPDATE ON hp_students
            FOR EACH ROW EXECUTE FUNCTION hp_update_updated_at();
        
        DROP TRIGGER IF EXISTS hp_spells_updated_at ON hp_spells;
        CREATE TRIGGER hp_spells_updated_at
            BEFORE UPDATE ON hp_spells
            FOR EACH ROW EXECUTE FUNCTION hp_update_updated_at();
        
        DROP TRIGGER IF EXISTS hp_cft_balances_updated_at ON hp_cft_balances;
        CREATE TRIGGER hp_cft_balances_updated_at
            BEFORE UPDATE ON hp_cft_balances
            FOR EACH ROW EXECUTE FUNCTION hp_update_updated_at();
        
        DROP TRIGGER IF EXISTS hp_revenue_routes_updated_at ON hp_revenue_routes;
        CREATE TRIGGER hp_revenue_routes_updated_at
            BEFORE UPDATE ON hp_revenue_routes
            FOR EACH ROW EXECUTE FUNCTION hp_update_updated_at();
        
        -- ============================================
        -- FUNCTIONS
        -- Business logic helpers
        -- ============================================
        
        -- Mint CFT to student (creates balance if not exists)
        CREATE OR REPLACE FUNCTION hp_mint_cft(
            p_student_id UUID,
            p_amount NUMERIC,
            p_reference_type VARCHAR,
            p_reference_id UUID,
            p_reason VARCHAR
        ) RETURNS UUID AS $$
        DECLARE
            v_balance_id UUID;
            v_transaction_id UUID;
        BEGIN
            -- Create or update balance
            INSERT INTO hp_cft_balances (student_id, available_balance, lifetime_earned)
            VALUES (p_student_id, p_amount, p_amount)
            ON CONFLICT (student_id) DO UPDATE
            SET available_balance = hp_cft_balances.available_balance + p_amount,
                lifetime_earned = hp_cft_balances.lifetime_earned + p_amount
            RETURNING balance_id INTO v_balance_id;
            
            -- Record transaction
            INSERT INTO hp_cft_transactions (
                student_id, to_balance, transaction_type, amount,
                reference_type, reference_id, reason
            )
            VALUES (
                p_student_id, v_balance_id, 'mint', p_amount,
                p_reference_type, p_reference_id, p_reason
            )
            RETURNING transaction_id INTO v_transaction_id;
            
            -- Update student totals
            UPDATE hp_students
            SET total_cft = (
                SELECT available_balance + staked_balance 
                FROM hp_cft_balances 
                WHERE student_id = p_student_id
            )
            WHERE student_id = p_student_id;
            
            RETURN v_transaction_id;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Stake CFT for governance
        CREATE OR REPLACE FUNCTION hp_stake_cft(
            p_student_id UUID,
            p_amount NUMERIC
        ) RETURNS UUID AS $$
        DECLARE
            v_balance_id UUID;
            v_available NUMERIC;
            v_transaction_id UUID;
        BEGIN
            -- Get current balance
            SELECT balance_id, available_balance INTO v_balance_id, v_available
            FROM hp_cft_balances
            WHERE student_id = p_student_id;
            
            IF v_balance_id IS NULL THEN
                RAISE EXCEPTION 'No CFT balance found for student';
            END IF;
            
            IF v_available < p_amount THEN
                RAISE EXCEPTION 'Insufficient available CFT balance';
            END IF;
            
            -- Move from available to staked
            UPDATE hp_cft_balances
            SET available_balance = available_balance - p_amount,
                staked_balance = staked_balance + p_amount
            WHERE student_id = p_student_id;
            
            -- Record transaction
            INSERT INTO hp_cft_transactions (
                student_id, from_balance, to_balance, transaction_type, amount,
                reference_type, reason
            )
            VALUES (
                p_student_id, v_balance_id, v_balance_id, 'stake', p_amount,
                'governance', 'Staked CFT for governance voting power'
            )
            RETURNING transaction_id INTO v_transaction_id;
            
            -- Update governance weight
            UPDATE hp_students
            SET governance_weight = (
                SELECT staked_balance 
                FROM hp_cft_balances 
                WHERE student_id = p_student_id
            )
            WHERE student_id = p_student_id;
            
            RETURN v_transaction_id;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Verify spell and mint CFT
        CREATE OR REPLACE FUNCTION hp_verify_spell(
            p_spell_id UUID,
            p_grade VARCHAR,
            p_grade_numeric NUMERIC,
            p_verifier_id UUID
        ) RETURNS TABLE(spell_id UUID, cft_minted NUMERIC, transaction_id UUID) AS $$
        DECLARE
            v_owner_id UUID;
            v_assignment_id UUID;
            v_base_xp INTEGER;
            v_multiplier NUMERIC;
            v_bonus NUMERIC;
            v_xp_earned INTEGER;
            v_cft_amount NUMERIC;
            v_transaction_id UUID;
        BEGIN
            -- Get spell and assignment info
            SELECT s.owner_id, s.assignment_id, COALESCE(a.base_xp, 100), 
                   COALESCE(c.xp_multiplier, 1.0), COALESCE(a.max_grade_bonus, 0.5)
            INTO v_owner_id, v_assignment_id, v_base_xp, v_multiplier, v_bonus
            FROM hp_spells s
            LEFT JOIN hp_assignments a ON s.assignment_id = a.assignment_id
            LEFT JOIN hp_courses c ON s.course_id = c.course_id
            WHERE s.spell_id = p_spell_id;
            
            IF v_owner_id IS NULL THEN
                RAISE EXCEPTION 'Spell not found';
            END IF;
            
            -- Calculate XP with grade bonus
            -- Grade bonus: linear scale from 0 at 0.0 to max_bonus at 4.0
            v_xp_earned := FLOOR(v_base_xp * v_multiplier * (1 + v_bonus * COALESCE(p_grade_numeric, 2.0) / 4.0));
            v_cft_amount := v_xp_earned;  -- 1:1 XP to CFT ratio
            
            -- Update spell status
            UPDATE hp_spells
            SET status = 'verified',
                grade = p_grade,
                grade_numeric = p_grade_numeric,
                verified_at = NOW(),
                verified_by = p_verifier_id,
                xp_earned = v_xp_earned,
                cft_minted = v_cft_amount
            WHERE hp_spells.spell_id = p_spell_id;
            
            -- Mint CFT to owner
            SELECT hp_mint_cft(
                v_owner_id, v_cft_amount, 'spell', p_spell_id,
                'Earned CFT for verified spell: ' || p_grade
            ) INTO v_transaction_id;
            
            -- Update student spell count
            UPDATE hp_students
            SET total_spells = (
                SELECT COUNT(*) FROM hp_spells 
                WHERE owner_id = v_owner_id AND status IN ('verified', 'certified')
            )
            WHERE student_id = v_owner_id;
            
            RETURN QUERY SELECT p_spell_id, v_cft_amount, v_transaction_id;
        END;
        $$ LANGUAGE plpgsql;
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(schema_sql)
            logger.info("Hogwarts Protocol schema created/updated")
    
    # ============================================
    # STUDENT OPERATIONS
    # ============================================
    
    async def create_student(self, student: Student) -> str:
        """Create new student record"""
        sql = """
        INSERT INTO hp_students (
            student_id, edu_email, edu_institution, display_name,
            wallet_address, wallet_nonce, is_active
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING student_id
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                sql,
                student.student_id,
                student.edu_email,
                student.edu_institution,
                student.display_name,
                student.wallet_address,
                student.wallet_nonce,
                student.is_active
            )
            logger.info(f"Created student: {result}")
            return str(result)
    
    async def get_student(self, student_id: str) -> Optional[Student]:
        """Get student by ID"""
        sql = """
        SELECT student_id, edu_email, edu_institution, display_name,
               wallet_address, wallet_nonce, is_active, created_at, updated_at,
               total_spells, total_cft, governance_weight
        FROM hp_students
        WHERE student_id = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, student_id)
            
            if not row:
                return None
            
            return Student(
                student_id=str(row['student_id']),
                edu_email=row['edu_email'],
                edu_institution=row['edu_institution'],
                display_name=row['display_name'],
                wallet_address=row['wallet_address'],
                wallet_nonce=row['wallet_nonce'],
                is_active=row['is_active'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                total_spells=row['total_spells'],
                total_cft=row['total_cft'],
                governance_weight=row['governance_weight']
            )
    
    async def get_student_by_wallet(self, wallet_address: str) -> Optional[Student]:
        """Get student by wallet address"""
        sql = """
        SELECT student_id, edu_email, edu_institution, display_name,
               wallet_address, wallet_nonce, is_active, created_at, updated_at,
               total_spells, total_cft, governance_weight
        FROM hp_students
        WHERE wallet_address = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, wallet_address.lower())
            
            if not row:
                return None
            
            return Student(
                student_id=str(row['student_id']),
                edu_email=row['edu_email'],
                edu_institution=row['edu_institution'],
                display_name=row['display_name'],
                wallet_address=row['wallet_address'],
                wallet_nonce=row['wallet_nonce'],
                is_active=row['is_active'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                total_spells=row['total_spells'],
                total_cft=row['total_cft'],
                governance_weight=row['governance_weight']
            )
    
    async def update_student_wallet(self, student_id: str, wallet_address: str):
        """Link wallet address to student"""
        sql = """
        UPDATE hp_students
        SET wallet_address = $2
        WHERE student_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(sql, student_id, wallet_address.lower())
    
    # ============================================
    # COURSE OPERATIONS
    # ============================================
    
    async def create_course(self, course: Course) -> str:
        """Create new course record"""
        sql = """
        INSERT INTO hp_courses (
            course_id, course_code, course_name, institution,
            description, learning_outcomes, platform, xp_multiplier,
            instructor_share_pct, start_date, end_date, is_active
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING course_id
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                sql,
                course.course_id,
                course.course_code,
                course.course_name,
                course.institution,
                course.description,
                json.dumps(course.learning_outcomes),
                course.platform,
                course.xp_multiplier,
                course.instructor_share_pct,
                course.start_date,
                course.end_date,
                course.is_active
            )
            logger.info(f"Created course: {result}")
            return str(result)
    
    async def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        sql = """
        SELECT course_id, course_code, course_name, institution,
               description, learning_outcomes, platform, xp_multiplier,
               instructor_share_pct, created_at, start_date, end_date, is_active
        FROM hp_courses
        WHERE course_id = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, course_id)
            
            if not row:
                return None
            
            return Course(
                course_id=str(row['course_id']),
                course_code=row['course_code'],
                course_name=row['course_name'],
                institution=row['institution'],
                description=row['description'],
                learning_outcomes=json.loads(row['learning_outcomes']) if row['learning_outcomes'] else [],
                platform=row['platform'],
                xp_multiplier=row['xp_multiplier'],
                instructor_share_pct=row['instructor_share_pct'],
                created_at=row['created_at'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                is_active=row['is_active']
            )
    
    # ============================================
    # SPELL OPERATIONS
    # ============================================
    
    async def create_spell(self, spell: Spell) -> str:
        """Create new spell record"""
        sql = """
        INSERT INTO hp_spells (
            spell_id, owner_id, course_id, assignment_id,
            spell_name, spell_type, content_hash, file_path,
            status, metadata
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING spell_id
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                sql,
                spell.spell_id,
                spell.owner_id,
                spell.course_id,
                spell.assignment_id,
                spell.spell_name,
                spell.spell_type,
                spell.content_hash,
                spell.file_path,
                spell.status.value,
                json.dumps(spell.metadata)
            )
            logger.info(f"Created spell: {result}")
            return str(result)
    
    async def get_spell(self, spell_id: str) -> Optional[Spell]:
        """Get spell by ID"""
        sql = """
        SELECT spell_id, owner_id, course_id, assignment_id,
               spell_name, spell_type, content_hash, file_path,
               status, grade, grade_numeric, verified_at, verified_by,
               on_chain_tx_hash, on_chain_token_id, chain_id,
               xp_earned, cft_minted, is_licensable, license_price,
               total_licenses_sold, total_revenue, created_at, updated_at, metadata
        FROM hp_spells
        WHERE spell_id = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, spell_id)
            
            if not row:
                return None
            
            return Spell(
                spell_id=str(row['spell_id']),
                owner_id=str(row['owner_id']),
                course_id=str(row['course_id']) if row['course_id'] else None,
                assignment_id=str(row['assignment_id']) if row['assignment_id'] else None,
                spell_name=row['spell_name'],
                spell_type=row['spell_type'],
                content_hash=row['content_hash'],
                file_path=row['file_path'],
                status=SpellStatus(row['status']),
                grade=row['grade'],
                grade_numeric=row['grade_numeric'],
                verified_at=row['verified_at'],
                verified_by=str(row['verified_by']) if row['verified_by'] else None,
                on_chain_tx_hash=row['on_chain_tx_hash'],
                on_chain_token_id=row['on_chain_token_id'],
                chain_id=row['chain_id'],
                xp_earned=row['xp_earned'],
                cft_minted=row['cft_minted'],
                is_licensable=row['is_licensable'],
                license_price=row['license_price'],
                total_licenses_sold=row['total_licenses_sold'],
                total_revenue=row['total_revenue'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                metadata=json.loads(row['metadata']) if row['metadata'] else {}
            )
    
    async def submit_spell(self, spell_id: str) -> bool:
        """Submit spell for verification"""
        sql = """
        UPDATE hp_spells
        SET status = 'submitted'
        WHERE spell_id = $1 AND status = 'draft'
        RETURNING spell_id
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(sql, spell_id)
            return result is not None
    
    async def verify_spell(
        self, 
        spell_id: str, 
        grade: str, 
        grade_numeric: Decimal,
        verifier_id: str
    ) -> Dict[str, Any]:
        """Verify spell and mint CFT"""
        sql = """
        SELECT spell_id, cft_minted, transaction_id
        FROM hp_verify_spell($1, $2, $3, $4)
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, spell_id, grade, grade_numeric, verifier_id)
            
            if not row:
                raise ValueError("Spell verification failed")
            
            return {
                "spell_id": str(row['spell_id']),
                "cft_minted": str(row['cft_minted']),
                "transaction_id": str(row['transaction_id'])
            }
    
    async def register_spell_on_chain(
        self,
        spell_id: str,
        tx_hash: str,
        token_id: int,
        chain_id: int
    ):
        """Record on-chain registration of spell"""
        sql = """
        UPDATE hp_spells
        SET status = 'certified',
            on_chain_tx_hash = $2,
            on_chain_token_id = $3,
            chain_id = $4
        WHERE spell_id = $1
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(sql, spell_id, tx_hash, token_id, chain_id)
    
    async def get_student_spells(
        self, 
        student_id: str, 
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Spell]:
        """Get spells owned by student"""
        where = "WHERE owner_id = $1"
        params = [student_id]
        
        if status:
            where += " AND status = $2"
            params.append(status)
        
        sql = f"""
        SELECT spell_id, owner_id, course_id, assignment_id,
               spell_name, spell_type, content_hash, file_path,
               status, grade, grade_numeric, verified_at, verified_by,
               on_chain_tx_hash, on_chain_token_id, chain_id,
               xp_earned, cft_minted, is_licensable, license_price,
               total_licenses_sold, total_revenue, created_at, updated_at, metadata
        FROM hp_spells
        {where}
        ORDER BY created_at DESC
        LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        
        params.extend([limit, offset])
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            
            return [
                Spell(
                    spell_id=str(row['spell_id']),
                    owner_id=str(row['owner_id']),
                    course_id=str(row['course_id']) if row['course_id'] else None,
                    assignment_id=str(row['assignment_id']) if row['assignment_id'] else None,
                    spell_name=row['spell_name'],
                    spell_type=row['spell_type'],
                    content_hash=row['content_hash'],
                    file_path=row['file_path'],
                    status=SpellStatus(row['status']),
                    grade=row['grade'],
                    grade_numeric=row['grade_numeric'],
                    verified_at=row['verified_at'],
                    verified_by=str(row['verified_by']) if row['verified_by'] else None,
                    on_chain_tx_hash=row['on_chain_tx_hash'],
                    on_chain_token_id=row['on_chain_token_id'],
                    chain_id=row['chain_id'],
                    xp_earned=row['xp_earned'],
                    cft_minted=row['cft_minted'],
                    is_licensable=row['is_licensable'],
                    license_price=row['license_price'],
                    total_licenses_sold=row['total_licenses_sold'],
                    total_revenue=row['total_revenue'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {}
                )
                for row in rows
            ]
    
    # ============================================
    # CFT BALANCE OPERATIONS
    # ============================================
    
    async def get_cft_balance(self, student_id: str) -> Optional[CFTBalance]:
        """Get CFT balance for student"""
        sql = """
        SELECT balance_id, student_id, available_balance, staked_balance,
               lifetime_earned, created_at, updated_at
        FROM hp_cft_balances
        WHERE student_id = $1
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, student_id)
            
            if not row:
                return None
            
            return CFTBalance(
                balance_id=str(row['balance_id']),
                student_id=str(row['student_id']),
                available_balance=row['available_balance'],
                staked_balance=row['staked_balance'],
                lifetime_earned=row['lifetime_earned'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
    
    async def mint_cft(
        self,
        student_id: str,
        amount: Decimal,
        reference_type: str,
        reference_id: str,
        reason: str
    ) -> str:
        """Mint CFT to student"""
        sql = """
        SELECT hp_mint_cft($1, $2, $3, $4, $5)
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                sql, student_id, amount, reference_type, reference_id, reason
            )
            return str(result)
    
    async def stake_cft(self, student_id: str, amount: Decimal) -> str:
        """Stake CFT for governance"""
        sql = """
        SELECT hp_stake_cft($1, $2)
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(sql, student_id, amount)
            return str(result)
    
    async def get_cft_transactions(
        self,
        student_id: str,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[CFTTransaction]:
        """Get CFT transaction history for student"""
        where = "WHERE student_id = $1"
        params = [student_id]
        
        if transaction_type:
            where += " AND transaction_type = $2"
            params.append(transaction_type)
        
        sql = f"""
        SELECT transaction_id, student_id, from_balance, to_balance,
               transaction_type, amount, reference_type, reference_id,
               reason, created_at, on_chain_tx_hash
        FROM hp_cft_transactions
        {where}
        ORDER BY created_at DESC
        LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        
        params.extend([limit, offset])
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            
            return [
                CFTTransaction(
                    transaction_id=str(row['transaction_id']),
                    student_id=str(row['student_id']),
                    from_balance=str(row['from_balance']) if row['from_balance'] else None,
                    to_balance=str(row['to_balance']) if row['to_balance'] else None,
                    transaction_type=CFTTransactionType(row['transaction_type']),
                    amount=row['amount'],
                    reference_type=row['reference_type'],
                    reference_id=str(row['reference_id']) if row['reference_id'] else None,
                    reason=row['reason'],
                    created_at=row['created_at'],
                    on_chain_tx_hash=row['on_chain_tx_hash']
                )
                for row in rows
            ]
    
    # ============================================
    # TRANSCRIPT OPERATIONS
    # ============================================
    
    async def get_transcript(self, student_id: str) -> List[Dict[str, Any]]:
        """Get on-chain transcript for student"""
        sql = """
        SELECT course_code, course_name, assignment_name, spell_name,
               grade, grade_numeric, status, verified_at,
               on_chain_tx_hash, on_chain_token_id, xp_earned, cft_minted, content_hash
        FROM hp_transcript
        WHERE student_id = $1
        ORDER BY verified_at DESC
        """
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, student_id)
            
            return [
                {
                    "course_code": row['course_code'],
                    "course_name": row['course_name'],
                    "assignment_name": row['assignment_name'],
                    "spell_name": row['spell_name'],
                    "grade": row['grade'],
                    "grade_numeric": str(row['grade_numeric']) if row['grade_numeric'] else None,
                    "status": row['status'],
                    "verified_at": row['verified_at'].isoformat() if row['verified_at'] else None,
                    "on_chain_tx_hash": row['on_chain_tx_hash'],
                    "on_chain_token_id": row['on_chain_token_id'],
                    "xp_earned": row['xp_earned'],
                    "cft_minted": str(row['cft_minted']),
                    "content_hash": row['content_hash']
                }
                for row in rows
            ]
