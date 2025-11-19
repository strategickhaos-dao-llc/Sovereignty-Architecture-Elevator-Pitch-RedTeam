# Secure Setup Guide

## Quick Start (Platform-Agnostic)

This guide helps you set up the Strategic Khaos Sovereignty Architecture project securely, without exposing local file paths or sensitive information.

### Prerequisites

- Git
- Docker & Docker Compose
- Node.js 18+ (for bot/gateway services)
- kubectl (for Kubernetes deployments)

### 1. Clone the Repository

```bash
# Clone to your preferred location
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git

# Navigate to project directory
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Set Up Environment Variables

**Never commit your `.env` file!** It's already in `.gitignore`.

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your favorite editor
# Replace placeholder values with your actual credentials
nano .env  # or vim, code, notepad, etc.
```

### 3. Configure Discord Integration

1. Create a Discord bot at https://discord.com/developers/applications
2. Enable required intents (Server Members, Message Content)
3. Get your bot token and guild/channel IDs
4. Update `.env` with these values

### 4. Launch Local Development

#### Option A: Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Option B: CloudOS Desktop Environment (Windows)

```powershell
# PowerShell
.\start-cloudos.ps1

# Or with options
.\start-cloudos.ps1 -Force -NoBuild
```

#### Option C: Individual Services

```bash
# Install dependencies
npm install

# Run bot service
npm run bot

# Run gateway service (in another terminal)
npm run gateway
```

### 5. Deploy to Kubernetes (Optional)

```bash
# Ensure kubectl is configured
kubectl config current-context

# Deploy infrastructure
./bootstrap/deploy.sh

# Verify deployment
kubectl get pods -n ops
```

## Directory Structure

Your local setup should look like this (relative to project root):

```
Sovereignty-Architecture-Elevator-Pitch-/
├── .env                    # Your local config (NOT committed)
├── .env.example           # Template (safe to commit)
├── node_modules/          # Dependencies (NOT committed)
├── data/                  # Local data (NOT committed)
│   ├── postgres/
│   ├── redis/
│   └── ...
├── bootstrap/             # Deployment scripts
├── src/                   # Source code
└── ...
```

## Security Checklist

Before committing or sharing:

- [ ] No `.env` file in commits
- [ ] No local file paths like `C:\Users\...` or `/Users/...`
- [ ] Secrets use environment variables, not hardcoded values
- [ ] Example configs use placeholders only
- [ ] Screenshots don't show file paths or sensitive info
- [ ] Log files are not committed

## Sharing Your Work

### ✅ Good: Relative Paths

```bash
# When documenting commands, use relative paths
./scripts/deploy.sh
cd bootstrap/k8s/
```

### ✅ Good: Environment Variables

```bash
export PROJECT_ROOT=$(pwd)
export DATA_DIR=$PROJECT_ROOT/data
```

### ✅ Good: Placeholders in Docs

```markdown
1. Clone the repo to your preferred location
2. Navigate to the project directory
3. Run `./bootstrap/deploy.sh`
```

### ❌ Bad: Absolute User Paths

```bash
# DON'T include paths like:
cd C:\Users\yourname\Downloads\project\
cd /Users/yourname/Desktop/project/
```

## Common Issues

### "Permission Denied" on Scripts

```bash
# Make scripts executable
chmod +x *.sh hooks/*.sh scripts/*.sh
```

### Docker Services Won't Start

```bash
# Check Docker is running
docker ps

# Clean up old containers
docker-compose down -v
docker system prune -f
```

### Environment Variables Not Loading

```bash
# Verify .env file exists
ls -la .env

# Check format (no spaces around =)
cat .env
```

## Getting Help

- 📖 [Security Guidelines](SECURITY_GUIDELINES.md)
- 📖 [Main README](README.md)
- 💬 [Discord Community](https://discord.gg/strategickhaos)
- 🐛 [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

---

**Remember**: Use relative paths, environment variables, and placeholders. Never expose your local file system structure!
