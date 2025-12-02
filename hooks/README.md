# Git Hooks for Security & Quality

This directory contains git hooks to help maintain security and code quality.

## Available Hooks

### 🔐 check_secrets.sh (Security)
Scans commits for exposed API keys, tokens, and secrets before allowing the commit.

**Features:**
- Detects common API key patterns (xAI, OpenAI, Anthropic, AWS)
- Blocks commits of .env files
- Integrates with gitleaks if installed
- Prevents accidental secret exposure

**Install:**
```bash
# Link to pre-commit hook
ln -sf ../../hooks/check_secrets.sh .git/hooks/pre-commit

# Make it executable (already done)
chmod +x hooks/check_secrets.sh
```

**Usage:**
- Automatically runs before every commit
- Blocks commits containing potential secrets
- Provides guidance on how to fix issues

**Bypass (NOT RECOMMENDED):**
```bash
# Only if you're ABSOLUTELY sure there are no secrets
git commit --no-verify
```

### ✅ require_checklist.py
Ensures commit messages follow required format with checklists.

### 📝 require_disclaimer.sh  
Enforces disclaimer requirements in specific documents.

### 🔏 require_gpg.sh
Ensures commits are GPG signed for authenticity.

---

## Installing All Hooks

```bash
# From repository root
cd .git/hooks

# Link all hooks
ln -sf ../../hooks/check_secrets.sh pre-commit
ln -sf ../../hooks/require_checklist.py prepare-commit-msg
ln -sf ../../hooks/require_gpg.sh pre-commit

# Or use a hook manager like husky or pre-commit framework
```

---

## Recommended: Install Gitleaks

For enhanced secret detection:

```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_amd64.tar.gz
tar -xzf gitleaks_linux_amd64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Verify installation
gitleaks version
```

---

## Testing Hooks

```bash
# Test secret detection
echo "XAI_API_KEY=xai-test123456789" > test.txt
git add test.txt
git commit -m "test"
# Should be blocked!

# Clean up
rm test.txt
git reset HEAD test.txt
```

---

## Troubleshooting

### Hook not running?
```bash
# Check permissions
ls -l .git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable)

# Make executable if needed
chmod +x .git/hooks/pre-commit
```

### False positives?
Edit the hook to adjust patterns or add exclusions.

### Need to commit anyway?
Use `--no-verify` (but document why in your commit message!).

---

**Security Note**: These hooks are your first line of defense against accidental secret exposure. Don't disable them unless absolutely necessary!
