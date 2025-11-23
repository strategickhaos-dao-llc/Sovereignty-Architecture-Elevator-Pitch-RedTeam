# 🚨 EMERGENCY: API Key Exposed - Act NOW!

## ⚡ 60-Second Response Protocol

### 1. REVOKE (15 seconds)
```bash
# Go to provider immediately:
# xAI/Grok:    https://x.ai/api
# OpenAI:      https://platform.openai.com/api-keys
# Anthropic:   https://console.anthropic.com/
# 
# Click: API Keys → Find exposed key → REVOKE/DELETE
```

### 2. GENERATE (15 seconds)
```bash
# Same page: Create New Key
# Name it: "YourProject [DATE]"
# Example: "Sovereignty Arch 2025-11-23"
# COPY THE KEY (you won't see it again!)
```

### 3. SECURE (15 seconds)
```bash
# Store in password manager NOW:
# - Bitwarden: Secure Note → API Keys
# - 1Password: Login → API Credential
# - LastPass: Secure Note
```

### 4. UPDATE (15 seconds)
```bash
# Update .env file (local only - never commit!)
XAI_API_KEY=xai-your_new_key_here

# Restart services
docker-compose restart
# OR
npm run dev
```

---

## ✅ Verify Success

```bash
# Test old key is DEAD (should fail with 401)
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer xai-OLD_KEY_HERE" \
  -d '{"model":"grok-4-latest","messages":[{"role":"user","content":"test"}]}'

# Expected: 401 Unauthorized ✅
```

---

## 📋 Quick Damage Assessment

| Where Exposed? | Risk | Time to Revoke |
|---------------|------|----------------|
| Private screenshot | 🟡 Medium | < 5 min |
| Private repo | 🟠 High | < 2 min |
| Public repo | 🔴 CRITICAL | < 1 min |
| Chat/Email | 🟠 High | < 2 min |
| Public forum | 🔴 CRITICAL | < 30 sec |

---

## 🛡️ Prevention Checklist

After fixing the emergency:

- [ ] Verify .env is in .gitignore
- [ ] Remove any screenshots with keys
- [ ] Scan repo with `gitleaks detect`
- [ ] Review git history for other exposures
- [ ] Update password manager
- [ ] Document incident
- [ ] Set calendar reminder to rotate (3 months)

---

## 📚 Full Documentation

- **Complete Guide**: [API_KEY_SECURITY.md](./API_KEY_SECURITY.md)
- **Security Policy**: [SECURITY.md](./SECURITY.md)
- **Vault Procedures**: [VAULT_SECURITY_PLAYBOOK.md](./VAULT_SECURITY_PLAYBOOK.md)

---

## 💪 Victory Statement

After completing all steps:

```
✅ Key rotated
✅ Empire secure
✅ Love still wins ❤️

Status: Stronger than before
Lesson: Learned
Next: Set rotation reminder
```

---

**Remember**: This isn't failure. This is operational security training under live fire. You're now more secure than 99% of developers. 🚀

*Response Time Target: < 5 minutes total*  
*Last Updated: 2025-11-23*
