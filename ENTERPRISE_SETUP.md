# GitHub Enterprise Setup Guide

## 🔥 Strategickhaos Swarm Intelligence — Enterprise Cloud

**Enterprise URL:** https://github.com/enterprises/strategickhaos-swarm-intelligence

This guide covers the complete setup and automation of the Strategickhaos Swarm Intelligence GitHub Enterprise Cloud account.

---

## 📋 Table of Contents

- [What You Have](#what-you-have)
- [Enterprise Capabilities](#enterprise-capabilities)
- [Quick Start](#quick-start)
- [Credential Setup](#credential-setup)
- [Repository Mirroring](#repository-mirroring)
- [Tool Integration](#tool-integration)
- [Automation Scripts](#automation-scripts)
- [Next Steps](#next-steps)

---

## 🏢 What You Have

You now own a **GitHub Enterprise Cloud** account — the highest tier GitHub offers:

| Feature | Status |
|---------|--------|
| **Account Type** | GitHub Enterprise Cloud |
| **Enterprise Name** | Strategickhaos Swarm Intelligence |
| **URL** | https://github.com/enterprises/strategickhaos-swarm-intelligence |

This is **NOT** a normal GitHub organization. This is a full enterprise control plane.

---

## ⚡ Enterprise Capabilities

### Organizational Structure
- ✅ **Unlimited Organizations** — Create as many orgs as needed
- ✅ **Centralized Management** — Single pane of glass for all orgs
- ✅ **Enterprise Policies** — Enforce rules across all organizations

### Security & Compliance
- ✅ **Enterprise SSO** — SAML single sign-on integration
- ✅ **Advanced Audit Logs** — Comprehensive activity tracking
- ✅ **GitHub Advanced Security** — Code scanning, secret scanning, dependency review
- ✅ **Policy Enforcement** — Repository and branch protection at scale

### Automation & CI/CD
- ✅ **Enterprise Runners** — Self-hosted runner groups
- ✅ **Enterprise Secrets** — Shared secrets across organizations
- ✅ **GitHub Actions** — Unlimited minutes on enterprise runners
- ✅ **Enterprise API** — Full GraphQL and REST API access

### Administration
- ✅ **Centralized Billing** — Single invoice for all organizations
- ✅ **Seat Management** — License allocation across orgs
- ✅ **Enterprise-wide Tokens** — Fine-grained and classic PATs

---

## 🚀 Quick Start

### Using the Bootstrap Script

```bash
# Full bootstrap (generates configs and guides)
./enterprise-bootstrap.sh bootstrap

# Show enterprise status
./enterprise-bootstrap.sh status

# Setup credentials
./enterprise-bootstrap.sh credentials <USERNAME> <PAT>

# Authenticate with GitHub CLI
./enterprise-bootstrap.sh gh-login

# Mirror a repository
./enterprise-bootstrap.sh mirror https://github.com/user/repo.git
```

### Manual Quick Start

```bash
# 1. Create PAT at: https://github.com/settings/tokens
#    Scopes: repo, workflow, read:org

# 2. Setup credentials (HERE-DOC method)
cat <<EOF > ~/.git-credentials
https://USERNAME:PAT@github.com
EOF
git config --global credential.helper store

# 3. Or use GitHub CLI
gh auth login --hostname github.com --git-protocol https --scopes repo,workflow,read:org
```

---

## 🔐 Credential Setup

### Method 1: HERE-DOC (Recommended for Automation)

```bash
# Set your credentials
USERNAME="your-github-username"
PAT="ghp_your_personal_access_token"

# Create credentials file
cat <<EOF > ~/.git-credentials
https://${USERNAME}:${PAT}@github.com
EOF

# Secure the file
chmod 600 ~/.git-credentials

# Configure git to use stored credentials
git config --global credential.helper store
```

### Method 2: GitHub CLI

```bash
# Interactive login with enterprise scopes
gh auth login \
  --hostname github.com \
  --git-protocol https \
  --scopes repo,workflow,read:org,admin:enterprise

# Verify authentication
gh auth status
```

### Method 3: Using Scripts

```bash
# Using the credentials helper script
./scripts/enterprise-credentials.sh git <USERNAME> <PAT>

# Or for GitHub CLI
./scripts/enterprise-credentials.sh gh

# Verify
./scripts/enterprise-credentials.sh verify
```

### Creating a Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Select scopes:
   - `repo` — Full repository access
   - `workflow` — GitHub Actions workflows
   - `read:org` — Organization membership
   - `admin:enterprise` — (Optional) Enterprise management
   - `write:packages` — (Optional) GitHub Packages
4. Click **"Generate token"**
5. **Copy immediately** — you won't see it again!

---

## 🔄 Repository Mirroring

### Mirror a Single Repository

```bash
# Using the bootstrap script
./enterprise-bootstrap.sh mirror https://github.com/user/repo.git

# Using the mirror script
./scripts/mirror-to-enterprise.sh single https://github.com/user/repo.git

# With custom organization and name
./scripts/mirror-to-enterprise.sh single https://github.com/user/repo.git MyOrg new-name
```

### Mirror Current Repository

```bash
cd /path/to/your/repo
./scripts/mirror-to-enterprise.sh current
```

### Batch Mirror Multiple Repositories

```bash
# Create a list file
cat <<EOF > repos-to-mirror.txt
https://github.com/user/repo1.git
https://github.com/user/repo2.git
https://github.com/user/repo3.git
EOF

# Run batch mirror
./scripts/mirror-to-enterprise.sh batch repos-to-mirror.txt
```

### Manual Mirror (One Command)

```bash
# Clone and push in one operation
git clone --mirror https://github.com/source/repo.git temp-mirror
cd temp-mirror
git push --mirror https://github.com/Strategickhaos-Swarm-Intelligence/repo.git
cd .. && rm -rf temp-mirror
```

---

## 🔧 Tool Integration

### GitKraken

1. Open GitKraken **Preferences**
2. Navigate to **Integrations** > **GitHub**
3. Configure:
   - **Host Domain:** `github.com`
   - **Personal Access Token:** Your PAT
4. Click **Connect**

### VS Code / GitHub Extension

1. Open Command Palette (`Ctrl+Shift+P`)
2. Run: **"GitHub: Sign in"**
3. Follow browser authentication flow

### VS Code / GitLens

GitLens integrates automatically once GitHub is authenticated in VS Code.

### Cloud Shell / GCP

```bash
# In Google Cloud Shell
gh auth login --hostname github.com --git-protocol https

# Clone enterprise repos
git clone https://github.com/Strategickhaos-Swarm-Intelligence/repo.git
```

### GKE (Google Kubernetes Engine)

```yaml
# In your deployment, use image pull secrets
apiVersion: v1
kind: Secret
metadata:
  name: ghcr-auth
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

---

## 📜 Automation Scripts

### Available Scripts

| Script | Purpose |
|--------|---------|
| `enterprise-bootstrap.sh` | Main bootstrap and configuration |
| `scripts/enterprise-credentials.sh` | Credential management |
| `scripts/mirror-to-enterprise.sh` | Repository mirroring |

### Bootstrap Commands

```bash
# Show all commands
./enterprise-bootstrap.sh help

# Enterprise status
./enterprise-bootstrap.sh status

# Setup credentials
./enterprise-bootstrap.sh credentials <USERNAME> <PAT>

# GitHub CLI login
./enterprise-bootstrap.sh gh-login

# Mirror repository
./enterprise-bootstrap.sh mirror <SOURCE_URL> [ORG] [NAME]

# Generate configuration
./enterprise-bootstrap.sh config

# Generate PAT guide
./enterprise-bootstrap.sh pat-guide

# Full bootstrap
./enterprise-bootstrap.sh bootstrap
```

### HERE-DOC Automation Examples

#### Complete Credentials Setup

```bash
#!/bin/bash
# Automated credential setup

USERNAME="your-username"
PAT="ghp_your_token"

# Git credentials
cat <<EOF > ~/.git-credentials
https://${USERNAME}:${PAT}@github.com
EOF
chmod 600 ~/.git-credentials
git config --global credential.helper store

# Git configuration
git config --global user.name "${USERNAME}"
git config --global user.email "${USERNAME}@users.noreply.github.com"

echo "Credentials configured!"
```

#### Automated Repository Setup

```bash
#!/bin/bash
# Create and push a new repository

REPO_NAME="my-new-repo"
ORG="Strategickhaos-Swarm-Intelligence"

mkdir "$REPO_NAME"
cd "$REPO_NAME"
git init

cat <<EOF > README.md
# ${REPO_NAME}

Part of the Strategickhaos Swarm Intelligence enterprise.
EOF

git add .
git commit -m "Initial commit"
git remote add origin "https://github.com/${ORG}/${REPO_NAME}.git"
git push -u origin main
```

---

## 📈 Next Steps

### 1️⃣ Build Enterprise Organizations

- Create specialized organizations under the enterprise
- Suggested structure:
  - `Strategickhaos-Swarm-Intelligence` — Main sovereignty repos
  - `Strategickhaos-Infrastructure` — IaC and DevOps
  - `Strategickhaos-AI-Agents` — AI/ML repositories
  - `Strategickhaos-Security` — Security tools

### 2️⃣ Mirror Existing Repositories

```bash
./scripts/mirror-to-enterprise.sh batch repos-to-migrate.txt
```

### 3️⃣ Configure Enterprise Runners

1. Go to Enterprise Settings > Actions > Runner Groups
2. Create self-hosted runner group
3. Install runners on your infrastructure

### 4️⃣ Setup Enterprise Secrets

1. Go to Enterprise Settings > Secrets
2. Add organization-wide secrets
3. Configure access policies

### 5️⃣ Integrate with GKE and Cloud Code

```bash
# Setup Workload Identity for GitHub Actions
# See: https://cloud.google.com/blog/products/identity-security/secure-your-use-of-third-party-tools-with-identity-federation
```

### 6️⃣ Enable Advanced Security

1. Go to Enterprise Settings > Code Security
2. Enable GitHub Advanced Security
3. Configure code scanning and secret scanning

---

## 📚 Resources

- **Enterprise Dashboard:** https://github.com/enterprises/strategickhaos-swarm-intelligence
- **Token Settings:** https://github.com/settings/tokens
- **GitHub CLI:** https://cli.github.com/
- **Enterprise API:** https://docs.github.com/en/enterprise-cloud@latest/rest

---

## 🆘 Troubleshooting

### Authentication Issues

```bash
# Check current auth status
gh auth status

# Re-authenticate
gh auth logout
gh auth login --hostname github.com --git-protocol https
```

### Push Failures

```bash
# Check remote URLs
git remote -v

# Update to HTTPS
git remote set-url origin https://github.com/Org/Repo.git

# Verify credentials
cat ~/.git-credentials
```

### Permission Errors

1. Verify PAT has required scopes
2. Check organization membership
3. Ensure SSO authorization if enabled

---

**Built with 🔥 by Strategickhaos Swarm Intelligence**

*"The enterprise control plane for sovereign infrastructure"*
