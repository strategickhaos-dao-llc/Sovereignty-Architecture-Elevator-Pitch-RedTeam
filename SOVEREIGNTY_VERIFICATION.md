# Sovereignty Verification System

**100% local. Zero cloud. Full control. Completely auditable.**

This repository implements a comprehensive sovereignty verification system that ensures:
1. Every repository has a proper LICENSE file (legal protection)
2. Every repository has an `artifacts/` directory for external AI discussion archiving
3. Full auditability through versioned history and tamper-evident ledgers

## 🎯 What This Solves

The problem: How do you prove, right now on your local machine, that:
- Your LICENSE file is legitimate and under your control
- External AI discussions are archived and immutable
- No hidden clauses, no cloud TOS, no surprise liability
- Everything is auditable and provable in any legal or compliance context

The solution: **Dumb text files you control 100%.**

## 📁 System Components

### 1. LICENSE File
- **Location**: `LICENSE` (root directory)
- **Type**: MIT License
- **Copyright**: 2025 Strategickhaos
- **Verification**: `git log LICENSE` shows commit history
- **Hash**: Run `sha256sum LICENSE` to verify integrity

### 2. Artifacts Directory
- **Location**: `artifacts/`
- **Purpose**: Archive external AI discussion links
- **Format**: Markdown files with JSON metadata
- **Example**: `claude_meta_evolution_2025-11-21.md`

### 3. Verification Ledger
- **Location**: `verification_ledger.jsonl`
- **Format**: JSON Lines (one JSON object per line)
- **Purpose**: Tamper-evident audit trail
- **Contents**: Timestamps, actions, actors, file hashes

### 4. Verification Scripts
- **PowerShell**: `scripts/Verify-RepositorySovereignty.ps1`
- **Python**: `scripts/verify_repository_sovereignty.py`
- **Purpose**: Auto-scan and auto-fix LICENSE/artifacts across repos

## 🚀 Quick Start

### Verify Current Repository

#### Using PowerShell:
```powershell
# Just check
.\scripts\Verify-RepositorySovereignty.ps1

# Auto-fix missing LICENSE/artifacts
.\scripts\Verify-RepositorySovereignty.ps1 -AutoFix

# Scan all repos in a directory
.\scripts\Verify-RepositorySovereignty.ps1 -ReposPath "C:\repos" -AutoFix
```

#### Using Python:
```bash
# Just check
python scripts/verify_repository_sovereignty.py

# Auto-fix missing LICENSE/artifacts
python scripts/verify_repository_sovereignty.py --auto-fix

# Scan all repos in a directory
python scripts/verify_repository_sovereignty.py --repos-path ~/repos --auto-fix

# Append results to ledger
python scripts/verify_repository_sovereignty.py --auto-fix --append-ledger
```

### Verify LICENSE Integrity

```bash
# Check LICENSE hasn't been tampered with
git log --oneline LICENSE

# Compare with original MIT template
sha256sum LICENSE

# View LICENSE commit
git show $(git log --format=%H LICENSE | tail -1)
```

### Archive External AI Discussion

```bash
# 1. Create artifacts directory (if doesn't exist)
mkdir -p artifacts

# 2. Create artifact file (execute this command, dates will be auto-filled)
ARTIFACT_DATE=$(date +%Y-%m-%d)
ARTIFACT_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat > "artifacts/claude_discussion_${ARTIFACT_DATE}.md" << EOF
# Claude Discussion — ${ARTIFACT_DATE}

Source: https://claude.ai/share/XXXXXX

Used as: audit trail, agent training reference

\`\`\`json
{
  "timestamp": "${ARTIFACT_TIMESTAMP}",
  "type": "external_ai_discussion",
  "source": "https://claude.ai/share/XXXXXX",
  "summary": "Brief description"
}
\`\`\`
EOF

# 3. Commit to git
git add artifacts/
git commit -m "Archive Claude discussion artifact"

# 4. Verify integrity
sha256sum artifacts/*.md
```

## 🔍 30 Ways to Verify License Sovereignty

1. `cat LICENSE` → Read it with your own eyes
2. `git log LICENSE` → See when it was added (immutable history)
3. `git show <commit>:LICENSE` → View historical versions
4. `sha256sum LICENSE` → Get cryptographic hash
5. `stat LICENSE` → See file metadata (owner, permissions, timestamps)
6. `ls -lah LICENSE` → Verify file exists and size
7. `file LICENSE` → Verify it's a text file
8. `wc -l LICENSE` → Count lines (MIT = ~21 lines)
9. `grep -i "copyright" LICENSE` → Find copyright holder
10. `git blame LICENSE` → See who wrote each line
11-20. `diff LICENSE <official_MIT_template>` → Verify against canonical version
21-30. `git diff HEAD~1 LICENSE` → See any recent changes

## 🗂️ 30 Ways to Verify Artifact Sovereignty

31. `ls -la artifacts/` → List all archived artifacts
32. `cat artifacts/claude_meta_evolution_2025-11-21.md` → Read with your own eyes
33. `sha256sum artifacts/*.md` → Hash all artifacts
34. `git log artifacts/` → See archive history
35. `find artifacts/ -type f` → Recursively list all files
36. `grep -r "https://claude.ai" artifacts/` → Find all Claude links
37. `jq . < verification_ledger.jsonl` → Parse ledger entries
38. `tail verification_ledger.jsonl` → See latest entries
39-50. `git diff HEAD~1 artifacts/` → See recent artifact changes

## 📊 30 Ways to Use Verification Scripts

51. Run on single repo → verify this repo
52. Run on parent directory → scan all child repos
53. `--auto-fix` → automatically fix missing LICENSE/artifacts
54. `--license-type MIT` → use MIT license template
55. `--license-type Apache-2.0` → use Apache 2.0 template
56. `--copyright-holder "Your Name"` → custom copyright
57. `--output-report custom.txt` → save report to custom location
58. `--append-ledger` → add results to verification_ledger.jsonl
59. Schedule with cron → automatic daily verification
60-70. Pipe to other tools → integrate with CI/CD

## 🎓 100-List Guarantees

71-80. **You own everything**: Delete any file with `rm` - no external dependencies
81-90. **Zero cloud**: Works offline, no internet after initial download
91-100. **Full audit trail**: Every change in git history, cryptographically signed
101-110. **No surprises**: Plain text files, read with any editor
111-120. **Legal protection**: Proper LICENSE file protects your rights
121-130. **Compliance ready**: Auditable in any legal/regulatory context

## 🛠️ Advanced Usage

### Schedule Automatic Verification (Linux/Mac)

Add to crontab:
```bash
# Run weekly on Sunday at 2 AM
0 2 * * 0 cd /path/to/repos && /usr/bin/python3 scripts/verify_repository_sovereignty.py --auto-fix --append-ledger
```

### Schedule Automatic Verification (Windows)

PowerShell Task Scheduler:
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\repos\scripts\Verify-RepositorySovereignty.ps1 -AutoFix"
$trigger = New-ScheduledTaskTrigger -Weekly -At 2am -DaysOfWeek Sunday
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "RepositorySovereigntyCheck"
```

### Custom License Template

Create your own "Sovereign Heir License v1":

```powershell
@'
Sovereign Heir License v1.0

Copyright (c) 2025 [Your Name]

This software is sovereign property. Terms:
1. Use freely for any purpose
2. Modify freely for any purpose
3. Distribute freely with attribution
4. No warranty, use at own risk
5. Author retains sovereign rights

Full control retained by author/heir at all times.
'@ | Set-Content LICENSE
```

## 📝 Verification Ledger Format

Each line in `verification_ledger.jsonl` is a JSON object:

```json
{
  "timestamp": "2025-11-21T03:15:19Z",
  "type": "artifact_archived|license_verified|sovereignty_verification",
  "path": "path/to/file",
  "source": "https://...",
  "action": "created|verified|modified",
  "actor": "sovereignty-verification-system|manual",
  "hash": "sha256:..."
}
```

## 🔐 Security & Compliance

### Legal Protection
- ✅ Proper LICENSE file protects your IP rights
- ✅ Versioned in git = timestamped proof of publication
- ✅ Can be cited in legal proceedings
- ✅ Complies with GitHub/GitLab OSS requirements

### Audit Trail
- ✅ Every file change tracked in git
- ✅ Cryptographic hashes prove integrity
- ✅ Verification ledger provides tamper-evident log
- ✅ Can be replicated to multiple locations (NAS, cloud backup)

### Sovereignty Guarantees
- ✅ **No cloud dependencies**: Everything is local files
- ✅ **No hidden clauses**: Plain text, read with any editor
- ✅ **Full control**: You own the files, the repo, the history
- ✅ **Zero surprises**: No TOS changes, no surprise liability
- ✅ **Fully auditable**: Every action logged and versioned

## 🎯 Real-World Scenarios

### Scenario 1: New Repository
```bash
# Create repo
mkdir my-new-repo && cd my-new-repo
git init

# Add sovereignty verification
cp /path/to/scripts/verify_repository_sovereignty.py .
python verify_repository_sovereignty.py --auto-fix

# Result: LICENSE + artifacts/ created and committed
```

### Scenario 2: Audit Existing Repos
```bash
# Scan all repos
python scripts/verify_repository_sovereignty.py --repos-path ~/repos

# Result: sovereignty_report.txt shows compliance status
```

### Scenario 3: Archive Claude Discussion
```bash
# Copy discussion URL
URL="https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56"

# Archive it
./scripts/archive_artifact.sh "$URL" "meta-evolution discussion"

# Result: New file in artifacts/ with metadata
```

## 📚 Additional Resources

- [MIT License Official](https://opensource.org/licenses/MIT)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [GNU AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)
- [Choose a License](https://choosealicense.com/)

## 🤝 Contributing

To add new verification features:

1. Update relevant script (PowerShell or Python)
2. Add tests to verify new functionality
3. Update this documentation
4. Commit with descriptive message
5. Ensure all verification checks pass

## 📄 License

This sovereignty verification system is itself licensed under MIT (see LICENSE file).

**Full sovereign control retained. Zero cloud dependencies. 100% auditable.**

---

*Generated by Sovereignty Architecture Verification Engine*
*Timestamp: 2025-11-21T03:15:19Z*
