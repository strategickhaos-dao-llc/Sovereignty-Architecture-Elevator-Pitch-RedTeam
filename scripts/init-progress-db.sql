-- ============================================
-- Academic Progress Tracker Database
-- StrategicKhaos DAO LLC / SNHU Degree Path
-- ============================================

-- Create tables for tracking academic progress

-- Student profile
CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    student_id VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    gpa DECIMAL(3,2) DEFAULT 0.00,
    total_credits_needed INT DEFAULT 120,
    credits_completed INT DEFAULT 0,
    enrollment_date DATE,
    target_graduation DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    credits INT DEFAULT 3,
    department VARCHAR(50),
    phase VARCHAR(50),
    prerequisites TEXT[],
    spellbook_path VARCHAR(255),
    docker_department VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Course enrollment and progress
CREATE TABLE IF NOT EXISTS course_progress (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    course_id INT REFERENCES courses(id),
    status VARCHAR(20) DEFAULT 'not_started', -- not_started, in_progress, completed, transferred
    grade VARCHAR(5),
    grade_points DECIMAL(3,2),
    semester VARCHAR(20),
    year INT,
    start_date DATE,
    completion_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id)
);

-- Spellbook progress
CREATE TABLE IF NOT EXISTS spellbook_progress (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    course_id INT REFERENCES courses(id),
    chapter_completed INT DEFAULT 0,
    total_chapters INT DEFAULT 5,
    labs_completed INT DEFAULT 0,
    total_labs INT DEFAULT 3,
    quiz_score DECIMAL(5,2),
    mastery_level VARCHAR(20) DEFAULT 'apprentice', -- apprentice, journeyman, expert, master
    last_activity TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Milestones
CREATE TABLE IF NOT EXISTS milestones (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    milestone_name VARCHAR(100) NOT NULL,
    milestone_level INT, -- 1-7
    achieved BOOLEAN DEFAULT FALSE,
    achievement_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial student record
INSERT INTO student (name, student_id, gpa, credits_completed, enrollment_date)
VALUES ('Domenic Garza', 'DG-2024', 3.732, 45, CURRENT_DATE)
ON CONFLICT DO NOTHING;

-- Insert CS courses
INSERT INTO courses (course_code, course_name, credits, department, phase, spellbook_path, docker_department) VALUES
('CS210', 'Programming Languages', 3, 'Computer Science', 'core', '/spellbooks/cs-core/cs210-programming-languages.md', 'core-programming'),
('CS230', 'Operating Platforms', 3, 'Computer Science', 'core', '/spellbooks/cs-core/cs230-operating-platforms.md', 'core-programming'),
('CS250', 'Software Development Lifecycle', 3, 'Computer Science', 'core', '/spellbooks/cs-core/cs250-sdlc.md', 'core-programming'),
('CS319', 'UI/UX Design', 3, 'Computer Science', 'engineering', '/spellbooks/software-engineering/cs319-ui-ux.md', 'software-engineering'),
('CS340', 'Client/Server Development', 3, 'Computer Science', 'core', '/spellbooks/cs-core/cs340-client-server.md', 'core-programming'),
('CS350', 'Emerging Systems Architecture', 3, 'Computer Science', 'engineering', '/spellbooks/software-engineering/cs350-emerging-tech.md', 'software-engineering'),
('CS405', 'Software Reverse Engineering', 3, 'Computer Science', 'engineering', '/spellbooks/software-engineering/cs405-reverse-engineering.md', 'software-engineering'),
('CS410', 'Software Security', 3, 'Computer Science', 'engineering', '/spellbooks/software-engineering/cs410-software-security.md', 'software-engineering'),
('CS465', 'Full-Stack Development', 3, 'Computer Science', 'fullstack', '/spellbooks/fullstack/cs465-fullstack.md', 'fullstack'),
('CS499', 'Computer Science Capstone', 6, 'Computer Science', 'capstone', '/spellbooks/capstone/cs499-capstone.md', 'capstone')
ON CONFLICT DO NOTHING;

-- Insert CYB courses
INSERT INTO courses (course_code, course_name, credits, department, phase, spellbook_path, docker_department) VALUES
('CYB200', 'Cybersecurity Foundations', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb200-foundations.md', 'cybersecurity'),
('CYB210', 'Network Security', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb210-network-security.md', 'cybersecurity'),
('CYB220', 'Security Risk Management', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb220-risk-management.md', 'cybersecurity'),
('CYB240', 'Security Operations', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb240-operations.md', 'cybersecurity'),
('CYB300', 'Digital Forensics', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb300-forensics.md', 'cybersecurity'),
('CYB320', 'Penetration Testing', 3, 'Cybersecurity', 'security', '/spellbooks/cybersecurity/cyb320-pentesting.md', 'cybersecurity')
ON CONFLICT DO NOTHING;

-- Insert foundation courses (currently in progress)
INSERT INTO courses (course_code, course_name, credits, department, phase, spellbook_path, docker_department) VALUES
('MAT243', 'Applied Statistics for STEM', 3, 'Mathematics', 'foundation', '/spellbooks/foundation/mat243-statistics.md', 'foundation'),
('IT145', 'Foundation in Application Development', 3, 'Information Technology', 'foundation', '/spellbooks/foundation/it145-java-foundations.md', 'foundation'),
('PHY150', 'Physics I with Lab', 3, 'Science', 'foundation', '/spellbooks/foundation/phy150-physics.md', 'foundation')
ON CONFLICT DO NOTHING;

-- Insert initial mastery milestones
INSERT INTO milestones (student_id, milestone_name, milestone_level) VALUES
(1, 'Foundation Apprentice', 1),
(1, 'Programming Sorcerer', 2),
(1, 'Security Warlock', 3),
(1, 'Advanced Cyber Knight', 4),
(1, 'Software Engineering Wizard', 5),
(1, 'Full-Stack Archmage', 6),
(1, 'Sovereignty Master', 7)
ON CONFLICT DO NOTHING;

-- Create views for reporting

-- Course completion summary
CREATE OR REPLACE VIEW course_completion_summary AS
SELECT 
    s.name as student_name,
    s.gpa,
    s.credits_completed,
    s.total_credits_needed,
    ROUND((s.credits_completed::decimal / s.total_credits_needed) * 100, 2) as completion_percentage,
    COUNT(CASE WHEN cp.status = 'completed' THEN 1 END) as courses_completed,
    COUNT(CASE WHEN cp.status = 'in_progress' THEN 1 END) as courses_in_progress,
    COUNT(CASE WHEN cp.status = 'not_started' THEN 1 END) as courses_remaining
FROM student s
LEFT JOIN course_progress cp ON s.id = cp.student_id
GROUP BY s.id, s.name, s.gpa, s.credits_completed, s.total_credits_needed;

-- Phase progress
CREATE OR REPLACE VIEW phase_progress AS
SELECT 
    c.phase,
    c.docker_department,
    COUNT(*) as total_courses,
    COUNT(CASE WHEN cp.status = 'completed' THEN 1 END) as completed,
    SUM(c.credits) as total_credits
FROM courses c
LEFT JOIN course_progress cp ON c.id = cp.course_id
GROUP BY c.phase, c.docker_department
ORDER BY 
    CASE c.phase 
        WHEN 'foundation' THEN 1
        WHEN 'core' THEN 2
        WHEN 'security' THEN 3
        WHEN 'engineering' THEN 4
        WHEN 'fullstack' THEN 5
        WHEN 'capstone' THEN 6
    END;

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_student_updated_at
    BEFORE UPDATE ON student
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_course_progress_updated_at
    BEFORE UPDATE ON course_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spellbook_progress_updated_at
    BEFORE UPDATE ON spellbook_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO student;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO student;
