# Sovereignty Verification Guide

This guide explains how to verify and maintain **full sovereign control** over your repositories through license verification and artifact archiving.

## 🎯 What This Achieves

Two simple goals with zero cloud dependencies:

1. **License File Sovereignty** - Every repo has proper legal protection you control 100%
2. **External AI Artifact Archiving** - All external AI discussions preserved as immutable text

## 🚀 Quick Start

### Verify Current Repository

```bash
# Check this repository's sovereignty status
python3 scripts/verify_repo_sovereignty.py --repo-root . --generate-report

# Or with PowerShell
pwsh scripts/verify-repo-sovereignty.ps1 -RepoRoot . -GenerateReport
```

### Scan All Your Repositories

```bash
# Python (Linux/Mac/Windows)
python3 scripts/verify_repo_sovereignty.py \
  --repo-root ~/repos \
  --generate-report

# PowerShell (Windows/Linux/Mac)
pwsh scripts/verify-repo-sovereignty.ps1 \
  -RepoRoot "C:\repos\" \
  -GenerateReport
```

### Auto-Fix Missing Licenses

```bash
# Python
python3 scripts/verify_repo_sovereignty.py \
  --repo-root ~/repos \
  --auto-fix \
  --generate-report

# PowerShell
pwsh scripts/verify-repo-sovereignty.ps1 \
  -RepoRoot "C:\repos\" \
  -AutoFix \
  -GenerateReport
```

## 📋 What Gets Checked

The verification tools scan each repository for:

### ✅ License File Presence
- Checks for `LICENSE` file
- Detects license type (MIT, Apache, GPL, BSD, etc.)
- Reports when the license was first committed
- **Status**: `✓` if present, `⚠` if missing

### ✅ Artifact Archive
- Checks for `artifacts/` directory
- Checks for `external_discussions.md` file
- Counts archived artifacts
- **Status**: `✓` if present, `⚠` if missing

### ✅ Overall Sovereignty
- **Fully Sovereign**: Has both LICENSE and artifacts ✓
- **Licensed Only**: Has LICENSE but no artifacts ⚠
- **Needs Attention**: Missing LICENSE ✗

## 📊 Reports Generated

Both JSON and Markdown reports are created:

### JSON Report (`sovereignty_verification_report.json`)
```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "scan_root": "/home/user/repos",
  "statistics": {
    "total": 30,
    "licensed": 27,
    "has_artifacts": 18,
    "fully_sovereign": 18,
    "needs_attention": 3
  },
  "repositories": [...]
}
```

### Markdown Report (`sovereignty_verification_report.md`)
Human-readable summary with:
- Statistics table
- Per-repository details
- Issues and recommendations

## 🔧 Adding Sovereignty to a Repository

### 1. Add MIT License (Copy-Paste)

```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name / Sovereign Heir]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT license — full sovereign control retained"
```

### 2. Create Artifacts Directory

```bash
mkdir -p artifacts

cat > artifacts/README.md << 'EOF'
# Artifacts

This directory archives external AI discussions and design artifacts.
All files are version-controlled and fully sovereign.
EOF

git add artifacts/
git commit -m "Add artifacts directory for external AI archiving"
```

### 3. Archive an External Discussion

```bash
# Example: Archive a Claude discussion
cat > artifacts/claude_discussion_$(date +%Y-%m-%d).md << 'EOF'
# Claude Discussion

Source: https://claude.ai/share/[id]

## Summary
Brief summary of the discussion...

## Metadata
```json
{
  "timestamp": "2025-11-21T03:06:35Z",
  "type": "external_ai_discussion",
  "source": "https://claude.ai/share/[id]",
  "summary": "Brief description"
}
```
EOF

git add artifacts/
git commit -m "Archive Claude discussion"
```

## 🔍 Verification Methods

### Hash Verification
```bash
# Verify file integrity
sha256sum LICENSE artifacts/*.md

# Store hashes for future verification
sha256sum LICENSE artifacts/*.md > checksums.txt
git add checksums.txt
git commit -m "Add checksums for verification"
```

### Git History Verification
```bash
# View LICENSE history
git log --follow --format="%ai %H %s" -- LICENSE

# View artifacts history
git log --follow --format="%ai %H %s" -- artifacts/

# Verify no changes since last commit
git diff HEAD -- LICENSE artifacts/
```

### Offline Verification
```bash
# Works 100% offline after first clone
cd /path/to/repo
git log --all --oneline --decorate
cat LICENSE
ls -la artifacts/

# No internet required - all data is local
```

## 🎓 100 Ways to Verify (Practical Examples)

### License File Sovereignty (30 ways)
1. ✓ `test -f LICENSE` → file exists locally
2. ✓ `wc -l LICENSE` → ~21 lines (MIT template)
3. ✓ `sha256sum LICENSE` → matches official MIT template
4. ✓ `git log --follow LICENSE` → immutable history
5. ✓ `cat LICENSE | grep "MIT License"` → confirms type
6. ✓ `stat LICENSE` → shows ownership (you)
7. ✓ `ls -la LICENSE` → readable/writable by you
8. ✓ Delete LICENSE → reverts to all rights reserved
9. ✓ Add custom clause → instantly proprietary
10. ✓ `grep -i "copyright" LICENSE` → your name
11-20. ✓ Copy to USB/NAS/backup → replicated everywhere
21-30. ✓ Push to GitHub → public proof of publication date

### External AI Artifact Archiving (30 ways)
31. ✓ `ls artifacts/` → lists all archived discussions
32. ✓ `cat artifacts/*.md` → read any artifact
33. ✓ `git log -- artifacts/` → immutable history
34. ✓ `sha256sum artifacts/*.md` → verify integrity
35. ✓ `grep -r "claude.ai" artifacts/` → find Claude links
36. ✓ `wc -l artifacts/*.md` → count lines in archives
37. ✓ Delete online link → local copy still valid
38. ✓ `rsync -av artifacts/ /backup/` → replicate
39-50. ✓ `jq . artifacts/*.json` → parse metadata

### Full Verification (40 ways)
51. ✓ Run `verify_repo_sovereignty.py` → automated check
52. ✓ Check exit code → 0 = success, 1 = needs attention
53. ✓ Read JSON report → programmatic analysis
54. ✓ Read Markdown report → human summary
55. ✓ Schedule with cron → weekly verification
56. ✓ CI/CD integration → fail build if not sovereign
57. ✓ Git hooks → pre-commit verification
58. ✓ `git status` → check for uncommitted changes
59-100. ✓ All standard git/filesystem operations work

## 🔐 Security & Legal Benefits

### What You Control
- ✓ **100% Local** - All files on your machine
- ✓ **No Cloud Lock-in** - Works offline forever
- ✓ **Version Control** - Git tracks every change
- ✓ **Hash Verification** - Tamper-evident
- ✓ **Legal Protection** - Clear license terms
- ✓ **Audit Trail** - Complete history preserved

### What You Don't Risk
- ✗ Cloud TOS changes
- ✗ Service shutdowns
- ✗ Hidden clauses
- ✗ Surprise liability
- ✗ Vendor lock-in
- ✗ Internet dependency

## 🤖 Automation & CI/CD

### GitHub Actions Example

```yaml
name: Sovereignty Verification
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Verify Sovereignty
        run: |
          python3 scripts/verify_repo_sovereignty.py \
            --repo-root . \
            --generate-report
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: sovereignty-report
          path: sovereignty_verification_report.*
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 scripts/verify_repo_sovereignty.py --repo-root .
exit $?
```

## 📚 Additional Resources

- `LICENSE` - Repository license (MIT)
- `artifacts/README.md` - Artifact archiving guide
- `scripts/verify-repo-sovereignty.ps1` - PowerShell verification tool
- `scripts/verify_repo_sovereignty.py` - Python verification tool

## 🎉 You're Good!

Two commands → every repo now has:
- ✓ Legal protection (LICENSE)
- ✓ Immutable artifact trail (artifacts/)
- ✓ No lawyers needed
- ✓ No cloud dependencies
- ✓ No surprises
- ✓ Full sovereignty

**Want more?**
- Custom license templates?
- Automated cross-repo scanning?
- Integration with your workflow?

The tools are all here - modify as needed. You own everything. 😄🧠
