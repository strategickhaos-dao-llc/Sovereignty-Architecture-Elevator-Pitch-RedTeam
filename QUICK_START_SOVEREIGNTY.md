# Quick Start: Sovereignty Verification

**Two commands → Full sovereignty protection**

## Immediate Actions (Copy-Paste Ready)

### 1. Verify This Repository

```bash
# Linux/Mac
python3 scripts/verify_repository_sovereignty.py

# Windows PowerShell
.\scripts\Verify-RepositorySovereignty.ps1
```

**Result**: Confirms LICENSE + artifacts/ exist and are properly configured.

### 2. Archive an AI Discussion

```bash
# Linux/Mac
./scripts/archive_artifact.sh "https://claude.ai/share/YOUR-ID" "Description"

# Manual (cross-platform)
cat > artifacts/discussion_$(date +%Y-%m-%d).md << 'EOF'
# Discussion — 2025-11-21

Source: https://claude.ai/share/YOUR-ID

```json
{
  "timestamp": "2025-11-21T03:15:19Z",
  "type": "external_ai_discussion",
  "source": "https://claude.ai/share/YOUR-ID",
  "summary": "Brief description"
}
```
EOF

git add artifacts/
git commit -m "Archive AI discussion"
```

### 3. Verify LICENSE Integrity

```bash
# Get cryptographic hash
sha256sum LICENSE

# Or PowerShell
Get-FileHash LICENSE -Algorithm SHA256

# Check commit history (immutable proof)
git log --oneline LICENSE
```

**Expected hash**: `a98152d6cf1730fe254c083ecff905e64248c5efa0548a759d0af11dd9e3404b`

### 4. Scan All Your Repositories

```bash
# Scan and report only
python3 scripts/verify_repository_sovereignty.py --repos-path ~/repos

# Auto-fix missing LICENSE/artifacts
python3 scripts/verify_repository_sovereignty.py --repos-path ~/repos --auto-fix

# PowerShell
.\scripts\Verify-RepositorySovereignty.ps1 -ReposPath "C:\repos" -AutoFix
```

## What You Get

### ✅ Legal Protection
- MIT License → Open source, no restrictions
- Timestamped in git → Proof of publication
- Cryptographically verified → Tamper-evident

### ✅ Artifact Archiving
- External AI discussions → Local copies
- JSON metadata → Machine-readable
- Version controlled → Immutable history

### ✅ Audit Trail
- `verification_ledger.jsonl` → Every action logged
- Git history → Complete timeline
- SHA256 hashes → Integrity proof

## Core Files

```
.
├── LICENSE                              # MIT license (already exists)
├── artifacts/                           # External AI artifacts
│   ├── README.md                        # How to use artifacts/
│   └── claude_meta_evolution_2025-11-21.md
├── verification_ledger.jsonl            # Tamper-evident audit log
├── scripts/
│   ├── verify_repository_sovereignty.py # Cross-platform verifier
│   ├── Verify-RepositorySovereignty.ps1 # PowerShell verifier
│   └── archive_artifact.sh              # Quick artifact archiver
├── SOVEREIGNTY_VERIFICATION.md          # Complete documentation
└── QUICK_START_SOVEREIGNTY.md           # This file
```

## 10-Second Verification

```bash
# 1. LICENSE exists?
ls -l LICENSE

# 2. Artifacts directory exists?
ls -l artifacts/

# 3. Everything under version control?
git status

# 4. Run verifier
python3 scripts/verify_repository_sovereignty.py
```

## 30-Second Archive New Discussion

```bash
# 1. Get the share URL from Claude/ChatGPT/etc.
URL="https://claude.ai/share/abc123"

# 2. Archive it
./scripts/archive_artifact.sh "$URL" "Feature X design discussion"

# 3. Push to remote
git push
```

## Common Commands

### View Verification Ledger
```bash
# Pretty print
cat verification_ledger.jsonl | jq .

# Last 5 entries
tail -5 verification_ledger.jsonl | jq .

# Count entries
wc -l verification_ledger.jsonl
```

### Check All Artifact Hashes
```bash
# Linux/Mac
sha256sum artifacts/*.md

# PowerShell
Get-ChildItem artifacts/*.md | Get-FileHash -Algorithm SHA256
```

### View Git History
```bash
# LICENSE history
git log --oneline LICENSE

# Artifacts history
git log --oneline artifacts/

# Full diff of artifact
git log -p artifacts/claude_meta_evolution_2025-11-21.md
```

## Sovereignty Guarantees

### What This System Provides
1. ✅ **Legal Protection**: Proper LICENSE file
2. ✅ **Artifact Archive**: External discussions preserved
3. ✅ **Audit Trail**: Every action logged
4. ✅ **Version Control**: Immutable history
5. ✅ **Cryptographic Proof**: SHA256 hashes
6. ✅ **Full Control**: 100% local, no cloud

### What This System Does NOT Do
1. ❌ Does not upload anything to cloud
2. ❌ Does not require internet (after first clone)
3. ❌ Does not have hidden dependencies
4. ❌ Does not modify existing licenses
5. ❌ Does not auto-push to remote

### Delete Everything?
```bash
# Remove artifacts
rm -rf artifacts/

# Remove verification system
rm -f verification_ledger.jsonl
rm -f scripts/verify_repository_sovereignty.py
rm -f scripts/Verify-RepositorySovereignty.ps1
rm -f scripts/archive_artifact.sh
rm -f SOVEREIGNTY_VERIFICATION.md
rm -f QUICK_START_SOVEREIGNTY.md

# Commit removal
git add -A
git commit -m "Remove sovereignty verification system"
```

**You own it 100%. No strings attached.**

## Automation Examples

### Schedule Weekly Verification (Linux/Mac)
```bash
# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * 0 cd ~/repos && python3 scripts/verify_repository_sovereignty.py --auto-fix --append-ledger") | crontab -
```

### Schedule Weekly Verification (Windows)
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\repos\scripts\Verify-RepositorySovereignty.ps1 -AutoFix"
$trigger = New-ScheduledTaskTrigger -Weekly -At 2am -DaysOfWeek Sunday
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "RepoSovereignty"
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 scripts/verify_repository_sovereignty.py || exit 1
```

## Troubleshooting

### "python3: command not found"
Use `python` instead of `python3`, or install Python 3.

### "Permission denied" on scripts
```bash
chmod +x scripts/*.sh scripts/*.py
```

### PowerShell execution policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Git not found
Install git: https://git-scm.com/downloads

## Next Steps

1. ✅ Read this file (you're here)
2. ⬜ Run verification: `python3 scripts/verify_repository_sovereignty.py`
3. ⬜ Check LICENSE hash: `sha256sum LICENSE`
4. ⬜ View ledger: `cat verification_ledger.jsonl`
5. ⬜ Read full docs: `cat SOVEREIGNTY_VERIFICATION.md`
6. ⬜ Archive a discussion: `./scripts/archive_artifact.sh <url> <desc>`
7. ⬜ Scan all repos: `python3 scripts/verify_repository_sovereignty.py --repos-path ~/repos --auto-fix`

## Questions?

- **What if I want Apache 2.0 instead of MIT?**  
  Use `--license-type Apache-2.0` flag

- **Can I use this on private repos?**  
  Yes! It works on any git repository.

- **Does this work offline?**  
  Yes! Zero internet required after initial clone.

- **Is this compatible with GitHub/GitLab?**  
  Yes! Standard git + text files work everywhere.

- **Can I modify the scripts?**  
  Yes! You own them 100%. Fork, modify, redistribute.

## Full Documentation

See `SOVEREIGNTY_VERIFICATION.md` for:
- 100 ways to verify sovereignty
- Advanced usage examples
- Compliance and legal details
- Complete API reference

---

**Status**: ✅ Fully operational  
**Dependencies**: Python 3.6+ or PowerShell 5.1+  
**Internet Required**: No (after initial clone)  
**License**: MIT (see LICENSE)  
**Control**: 100% yours  

*Generated: 2025-11-21*
