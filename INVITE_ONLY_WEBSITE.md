# Invite-Only Website with Internal LLMs

## Overview

This Sovereignty Architecture project now includes a secure, invite-only web application that provides access to internal Large Language Models (LLMs) and tools. The system is designed to run on your own servers with complete control over data and infrastructure.

## Features

### 🔐 Invite-Only Access System
- **User Invitations**: Admin users can generate unique invite codes for new users
- **Email-based Invites**: Each invite is tied to a specific email address
- **Expiration Control**: Invites can have custom expiration periods (1-30 days)
- **One-time Use**: Invite codes can only be used once
- **Audit Trail**: All invitations and registrations are logged

### 🤖 Internal LLM Integration
- **Multiple Models**: Support for GPT-4o, GPT-4o Mini, Claude 3 Sonnet, and local Llama 3
- **Chat Interface**: Clean, modern chat interface for interacting with AI assistants
- **Conversation History**: All conversations are saved and can be retrieved
- **Model Selection**: Users can choose which LLM model to use for each conversation
- **Token Tracking**: Monitor token usage across conversations

### 🛡️ Security Features
- **Session-based Authentication**: Secure cookie-based sessions
- **Password Hashing**: BCrypt password hashing with salt rounds
- **HTTPS/TLS Support**: Nginx configured for SSL/TLS (certificates required)
- **Rate Limiting**: Protection against brute force and DDoS attacks
- **Audit Logging**: Comprehensive logging of all user actions
- **Role-Based Access Control (RBAC)**: Admin and user roles with different permissions
- **Security Headers**: X-Frame-Options, X-XSS-Protection, Content-Security-Policy
- **SQL Injection Protection**: Parameterized queries throughout

### 📊 User Management
- **Profile Management**: Users can view their account information
- **Invitation Tracking**: Users can see invitations they've sent
- **Admin Dashboard**: Admins can manage all users and invitations
- **Activity Monitoring**: Track user login times and activity

## Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Server** | Express.js (Node.js) | HTTP server and API routing |
| **Database** | PostgreSQL 15 | User data, invitations, conversations |
| **Session Store** | Express-session | Session management |
| **Authentication** | BCrypt + Sessions | User authentication |
| **Frontend** | Vanilla JavaScript | Single-page application |
| **Reverse Proxy** | Nginx | Load balancing, SSL/TLS, security |
| **AI Backend** | Refinory Orchestrator | LLM integration and management |
| **Monitoring** | Prometheus + Grafana | System metrics and dashboards |

### Database Schema

The application uses the following PostgreSQL tables:

- **users**: User accounts with authentication credentials
- **invitations**: Invite codes and their status
- **user_sessions**: Active user sessions
- **audit_log**: Comprehensive audit trail of all actions
- **llm_conversations**: Chat history and conversation tracking

### Services

1. **web-app**: Main web application (port 8090)
2. **postgres**: PostgreSQL database (port 5432)
3. **redis**: Session and caching (port 6379)
4. **refinory-api**: AI orchestration service (port 8085)
5. **nginx**: Reverse proxy and SSL termination (ports 80/443)

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Your own server (VPS, dedicated server, or on-premise)
- Domain name (optional, for SSL/TLS)

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Step 2: Configure Environment Variables

Edit `.env` and set the following required variables:

```bash
# Database
POSTGRES_PASSWORD=your_secure_password_here

# Web Application
SESSION_SECRET=generate_a_random_secret_here
BASE_URL=https://your-domain.com  # or http://localhost:8090 for local

# AI/LLM Configuration
OPENAI_API_KEY=sk-your-api-key-here  # If using OpenAI models

# Optional: Discord integration
DISCORD_TOKEN=your_bot_token_here
```

### Step 3: Start the Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f web-app
```

### Step 4: Access the Website

1. Open your browser and navigate to `http://localhost:8090` (or your domain)
2. Default admin credentials:
   - Email: `admin@localhost`
   - Password: `admin123` (⚠️ **CHANGE THIS IMMEDIATELY**)

### Step 5: Generate Invite Codes

1. Login as admin
2. Navigate to the "Invitations" section
3. Enter recipient email and expiration days
4. Click "Generate Invite"
5. Share the invite URL with the recipient

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem

# Update nginx.conf to enable HTTPS server block
# Restart nginx
docker-compose restart nginx
```

### Self-Signed Certificate (Development)

```bash
# Create ssl directory
mkdir -p ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem

# Update nginx.conf to enable HTTPS server block
# Restart nginx
docker-compose restart nginx
```

## Security Best Practices

### Initial Setup

1. **Change Default Password**: Immediately change the admin password after first login
2. **Secure Database**: Use a strong password for PostgreSQL
3. **Session Secret**: Generate a strong random session secret
4. **Enable HTTPS**: Configure SSL/TLS certificates before production use
5. **Firewall Configuration**: Block all ports except 80 and 443
6. **Regular Updates**: Keep all services and dependencies updated

### Production Deployment

```bash
# Set production mode
export NODE_ENV=production

# Enable HTTPS redirect in nginx.conf
# Uncomment the HTTPS server block

# Use strong passwords
# Rotate secrets regularly
# Enable database backups
# Monitor audit logs
```

### Firewall Configuration

```bash
# Using ufw (Ubuntu/Debian)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH only
sudo ufw enable

# Using firewalld (RHEL/CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## API Documentation

### Authentication Endpoints

#### POST /api/auth/login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "role": "user"
  }
}
```

#### POST /api/auth/register
Register a new account with an invite code.

**Request:**
```json
{
  "username": "john_doe",
  "email": "user@example.com",
  "password": "password123",
  "inviteCode": "abc123def456..."
}
```

#### POST /api/auth/logout
Logout and destroy session.

#### GET /api/auth/me
Get current user information.

### Invitation Endpoints (Authenticated)

#### POST /api/invites/generate (Admin only)
Generate a new invite code.

**Request:**
```json
{
  "email": "newuser@example.com",
  "expiresInDays": 7
}
```

**Response:**
```json
{
  "success": true,
  "inviteCode": "abc123def456...",
  "email": "newuser@example.com",
  "expiresAt": "2024-01-01T00:00:00.000Z",
  "inviteUrl": "http://localhost:8090/register?invite=abc123def456..."
}
```

#### GET /api/invites/list (Admin only)
List all invitations.

#### GET /api/invites/mine
Get invitations created by current user.

#### DELETE /api/invites/:inviteId (Admin only)
Revoke an invitation.

### LLM Chat Endpoints (Authenticated)

#### POST /api/llm/chat
Send a message to the AI assistant.

**Request:**
```json
{
  "message": "What is the capital of France?",
  "conversationId": "uuid-here",
  "model": "gpt-4o-mini"
}
```

**Response:**
```json
{
  "success": true,
  "conversationId": "uuid-here",
  "message": "The capital of France is Paris.",
  "tokensUsed": 25
}
```

#### GET /api/llm/conversations
List all conversations for current user.

#### GET /api/llm/conversations/:conversationId
Get conversation history.

#### DELETE /api/llm/conversations/:conversationId
Delete a conversation.

#### GET /api/llm/models
Get available LLM models.

## Monitoring and Maintenance

### View Logs

```bash
# Application logs
docker-compose logs -f web-app

# Database logs
docker-compose logs -f postgres

# Nginx logs
docker-compose logs -f nginx

# All services
docker-compose logs -f
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres strategickhaos > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres strategickhaos < backup.sql
```

### Monitoring Dashboard

Access Grafana at `http://localhost:3000/monitoring/` (default credentials: admin/admin)

Dashboards include:
- System metrics (CPU, memory, disk)
- Application metrics (requests, errors, latency)
- Database metrics (connections, queries)
- User activity

## Troubleshooting

### Web App Not Starting

```bash
# Check logs
docker-compose logs web-app

# Common issues:
# 1. Database not ready - wait a few seconds and retry
# 2. Port 8090 already in use - change WEB_PORT in .env
# 3. Missing dependencies - rebuild: docker-compose build web-app
```

### Database Connection Errors

```bash
# Check PostgreSQL status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Cannot Login

```bash
# Reset admin password (requires database access)
docker-compose exec postgres psql -U postgres strategickhaos

# In psql:
UPDATE users SET password_hash = '$2b$10$rKvVPGYEqKN5xqKqZLR4ReJ9H.h2FXqKuHYzqLZoJqLqKtZLLLLLe' 
WHERE email = 'admin@localhost';
# (This sets password to 'admin123')
```

### LLM Service Unavailable

```bash
# Check Refinory API status
docker-compose ps refinory-api
docker-compose logs refinory-api

# Restart AI service
docker-compose restart refinory-api
```

## Maintenance Tasks

### Regular Maintenance

```bash
# Update dependencies
npm update

# Rebuild containers
docker-compose build --no-cache

# Clean up old images
docker system prune -a

# Backup database (weekly)
./scripts/backup-db.sh

# Review audit logs (daily)
docker-compose exec postgres psql -U postgres strategickhaos \
  -c "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 100;"
```

### Performance Tuning

1. **Database Optimization**:
   - Regular VACUUM and ANALYZE
   - Index optimization
   - Connection pool tuning

2. **Application Optimization**:
   - Enable response compression
   - Implement caching (Redis)
   - Rate limit adjustments

3. **Infrastructure Scaling**:
   - Increase database resources
   - Add read replicas
   - Implement load balancing

## Support and Resources

- **Documentation**: See README.md for general architecture
- **Security Issues**: Contact admin for security concerns
- **Feature Requests**: Open an issue on GitHub
- **Community**: Join the Discord server for support

## License

This project is part of the Sovereignty Architecture and follows the same MIT License.

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Empowering sovereign digital infrastructure through self-hosted AI platforms"*
