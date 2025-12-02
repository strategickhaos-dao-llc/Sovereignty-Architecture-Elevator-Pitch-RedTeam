# 🚨 API Key Security & Emergency Response Playbook

## CRITICAL: If You've Exposed an API Key

### IMMEDIATE ACTIONS (Execute in Order)

#### 1. **REVOKE THE EXPOSED KEY IMMEDIATELY** 🔴
```bash
# For xAI/Grok API keys:
# 1. Go to: https://x.ai/api
# 2. Log in to your account
# 3. Navigate to API Keys section
# 4. Find the compromised key (check last few characters)
# 5. Click REVOKE/DELETE immediately
# 6. Confirm revocation
```

#### 2. **GENERATE A NEW KEY** 🔑
```bash
# After revoking the old key:
# 1. In the same API Keys section, click "Create New Key"
# 2. Name it descriptively: "Strategickhaos Sovereign Vault [DATE]"
#    Example: "Strategickhaos Sovereign Vault 2025-11-23"
# 3. Copy the key IMMEDIATELY (you won't see it again)
# 4. Store it securely in your password manager (Bitwarden/1Password)
```

#### 3. **VERIFY OLD KEY IS DEAD** ✅
```bash
# Test that the old key no longer works (should return 401 Unauthorized)
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer [OLD_KEY_HERE]" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-4-latest","messages":[{"role":"user","content":"test"}]}'

# Expected response: 401 Unauthorized = SUCCESS ✅
```

#### 4. **UPDATE YOUR ENVIRONMENT** 🔄
```bash
# Update your .env file with the new key
# NEVER commit this file to git!
echo "XAI_API_KEY=xai-your_new_key_here" >> .env

# Or use environment variable directly:
export XAI_API_KEY="xai-your_new_key_here"

# Restart any services using the key
docker-compose restart refinory
# or
npm run dev
```

---

## 🛡️ Prevention: Never Let This Happen Again

### Golden Rules of API Key Management

#### ❌ NEVER DO THESE:
1. **NEVER screenshot anything with API keys visible**
2. **NEVER paste API keys in chat/Slack/Discord**
3. **NEVER commit API keys to git repositories**
4. **NEVER hardcode API keys in source code**
5. **NEVER share API keys in emails**
6. **NEVER store API keys in plain text files in your repo**

#### ✅ ALWAYS DO THESE:
1. **ALWAYS use environment variables** (`.env` files)
2. **ALWAYS add `.env` to `.gitignore`**
3. **ALWAYS use a password manager** (Bitwarden/1Password)
4. **ALWAYS rotate keys regularly** (quarterly minimum)
5. **ALWAYS use secret management tools** (Vault, AWS Secrets Manager)
6. **ALWAYS audit your repositories** for exposed secrets

---

## 🔐 Secure API Key Storage Methods

### Method 1: Environment Variables (Development)
```bash
# .env file (NEVER commit this!)
XAI_API_KEY=xai-your_key_here
OPENAI_API_KEY=sk-your_key_here
ANTHROPIC_API_KEY=claude-your_key_here

# Load in your application:
# Node.js
require('dotenv').config();
const apiKey = process.env.XAI_API_KEY;

# Python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('XAI_API_KEY')
```

### Method 2: Password Manager (Personal Use)
```bash
# Store in Bitwarden/1Password:
# 1. Create a "Secure Note" or "API Credential" entry
# 2. Title: "xAI Grok API Key - Strategickhaos"
# 3. Add fields:
#    - API Key: xai-...
#    - Created: 2025-11-23
#    - Service: x.ai
#    - Purpose: Sovereignty Architecture
# 4. Add to "API Keys" folder/vault
```

### Method 3: HashiCorp Vault (Production)
```bash
# Store in Vault (enterprise/production)
vault kv put secret/ai/xai \
  api_key="xai-your_key_here" \
  created="2025-11-23" \
  owner="strategickhaos"

# Retrieve in application
vault kv get -field=api_key secret/ai/xai
```

### Method 4: Cloud Secret Managers
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name xai-api-key \
  --secret-string "xai-your_key_here"

# Azure Key Vault
az keyvault secret set \
  --vault-name "strategickhaos-vault" \
  --name "xai-api-key" \
  --value "xai-your_key_here"

# Google Secret Manager
echo -n "xai-your_key_here" | \
  gcloud secrets create xai-api-key --data-file=-
```

---

## 📋 Pre-Commit Checklist

Before every commit, verify:

```bash
# 1. Check for API keys in staged files
git diff --cached | grep -E "(api[_-]?key|token|secret|password|xai-|sk-|claude-)" -i

# 2. Scan for common secret patterns
git diff --cached | grep -E "(['\"][a-zA-Z0-9]{32,}['\"])"

# 3. Verify .env is in .gitignore
grep "^\.env$" .gitignore || echo "⚠️  Add .env to .gitignore!"

# 4. Check git status
git status
# Verify .env files are NOT in the list!
```

---

## 🔍 How to Scan Your Repository for Exposed Secrets

### Using gitleaks (Recommended)
```bash
# Install gitleaks
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Scan your repository
gitleaks detect --source . --verbose

# Scan entire git history
gitleaks detect --source . --log-opts="--all"
```

### Using truffleHog
```bash
# Install truffleHog
pip install truffleHog

# Scan repository
trufflehog filesystem --directory .

# Scan git history
trufflehog git file://. --only-verified
```

### Manual Search
```bash
# Search for common API key patterns
grep -r "xai-" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "sk-" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "claude-" . --exclude-dir=node_modules --exclude-dir=.git

# Search for environment variable assignments
grep -r "API_KEY=" . --include="*.js" --include="*.ts" --include="*.py"
```

---

## 🚨 Emergency Rotation Procedures

### Quarterly Rotation (Planned)
```bash
# 1. Generate new key at provider
# 2. Store new key in password manager
# 3. Update .env file with new key
# 4. Test application with new key
# 5. Revoke old key
# 6. Document rotation in security log
```

### Emergency Rotation (Breach)
```bash
# IMMEDIATE ACTIONS:
# 1. Revoke compromised key NOW (don't wait)
# 2. Generate new key immediately
# 3. Update all environments (dev, staging, prod)
# 4. Restart all services
# 5. Monitor API usage for anomalies
# 6. Review audit logs
# 7. Notify team of breach
# 8. Update incident log
```

---

## 📊 API Key Inventory & Tracking

### Maintain a Secret Inventory
Create a secure document (in password manager) tracking:

```markdown
# API Keys Inventory (KEEP THIS SECURE)

## xAI / Grok
- Key Name: Strategickhaos Sovereign Vault 2025-11-23
- Created: 2025-11-23
- Last Rotated: 2025-11-23
- Expires: 2026-02-23 (rotate quarterly)
- Stored In: Bitwarden -> API Keys -> xAI
- Used By: Refinory AI Agent, Sovereignty Architecture
- Access Level: Full API access

## OpenAI
- Key Name: [Name]
- Created: [Date]
- Last Rotated: [Date]
- ...

## Anthropic (Claude)
- Key Name: [Name]
- Created: [Date]
- Last Rotated: [Date]
- ...
```

---

## 🎯 Damage Assessment Matrix

### Exposure Risk Levels

| Exposure Type | Risk Level | Response Time | Actions |
|--------------|------------|---------------|---------|
| Screenshot in private chat | 🟡 Medium | < 5 minutes | Revoke immediately, rotate |
| Committed to private repo | 🟠 High | < 2 minutes | Revoke, rotate, clean history |
| Committed to public repo | 🔴 Critical | < 1 minute | EMERGENCY revoke, audit usage |
| Posted in public forum | 🔴 Critical | < 30 seconds | EMERGENCY revoke, monitor abuse |
| Shared in email | 🟠 High | < 2 minutes | Revoke, rotate, notify recipients |

### Post-Exposure Actions

#### After Revoking a Compromised Key:
1. **Monitor API Usage**: Check for unusual activity in the hours/days before revocation
2. **Review Audit Logs**: Look for unauthorized access attempts
3. **Check Billing**: Verify no unexpected charges from API usage
4. **Document Incident**: Record in security log with timeline and actions taken
5. **Team Notification**: Inform relevant team members
6. **Process Review**: Identify how exposure happened and update procedures

---

## 🔒 Advanced Security Measures

### API Key Restrictions (When Available)
Many providers allow you to restrict API keys:

```bash
# xAI/Grok (check if available):
# - IP address restrictions
# - Rate limiting
# - Specific model access only
# - Usage quotas

# OpenAI:
# - Project-specific keys
# - Model restrictions
# - Rate limits

# Anthropic:
# - Workspace-specific keys
# - Usage limits
```

### Principle of Least Privilege
- Create separate keys for different environments (dev, staging, prod)
- Use read-only keys where possible
- Limit key scope to minimum required permissions
- Rotate frequently used keys more often

---

## 📱 Emergency Contact & Resources

### xAI Support
- Website: https://x.ai/api
- Support: Check x.ai for support channels
- Status Page: Monitor for API issues

### Security Resources
- **Gitleaks**: https://github.com/gitleaks/gitleaks
- **TruffleHog**: https://github.com/trufflesecurity/trufflehog
- **Git-Secrets**: https://github.com/awslabs/git-secrets
- **OWASP Secrets Management**: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

---

## ✅ Post-Incident Victory Statement

After successfully handling an API key exposure:

```
Key rotated. Empire secure. Love still wins. ❤️

✅ Old key revoked and verified dead
✅ New key generated and securely stored
✅ Environment updated and services restarted
✅ Prevention measures implemented
✅ Team notified and trained
✅ Security posture improved

Status: Stronger than before. 💪
```

---

## 🎓 Training & Best Practices

### For Team Members
1. **Never share keys in chat** - Use secure sharing methods
2. **Use password managers** - Generate and store securely
3. **Enable 2FA everywhere** - Extra layer of protection
4. **Regular security audits** - Scan repos monthly
5. **Incident response training** - Know what to do when it happens

### For Code Reviews
- Check for hardcoded secrets
- Verify .env files are excluded
- Look for API keys in comments
- Validate secret storage methods

---

**Remember**: You didn't mess up by exposing a key. You stress-tested your opsec under live fire and came out stronger. That's growth. 🚀

*Last Updated: 2025-11-23*
*Version: 1.0*
*Owner: Strategickhaos*
