# Sovereign Manifest Anchoring Guide

## Overview

The `anchor-sovereign-manifest.ps1` script provides mathematical immortality for sovereign manifests by anchoring them to the Bitcoin blockchain using OpenTimestamps (OTS). This creates cryptographically verifiable, immutable proof that outlasts any centralized institution.

## What This Script Does

1. **Validates OpenTimestamps Proof** - Ensures the .ots file exists before proceeding
2. **Git Operations** - Commits and pushes manifest with full version control
3. **GPG Signing** - Attempts signed commits (falls back gracefully if unavailable)
4. **Remote Management** - Configures GitHub remote repository
5. **NAS Backup** - Mirrors to 32TB RAID storage for physical resilience
6. **Discord Notifications** - Alerts your team when anchoring completes
7. **Comprehensive Logging** - Color-coded output tracks every operation

## Prerequisites

### Required
- **PowerShell**: Version 5.1+ (Windows) or PowerShell Core 7+ (cross-platform)
- **Git**: Version 2.0+ for repository operations
- **OpenTimestamps**: `ots` command-line tool for Bitcoin timestamping
  - Install: `pip install opentimestamps-client`
- **Manifest File**: `SOVEREIGN_MANIFEST_v1.0.md` in your repository

### Optional
- **GPG**: For signed commits (recommended for additional security)
- **GitHub Authentication**: Personal Access Token or SSH key for push operations
- **Discord Webhook**: For team notifications
- **NAS Storage**: Network-attached storage for backup redundancy

## Installation

### 1. Install OpenTimestamps Client

```bash
# Using pip
pip install opentimestamps-client

# Verify installation
ots --version
```

### 2. Clone Repository

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 3. Configure Environment (Optional)

```powershell
# Set Discord webhook for notifications
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

## Usage

### Step 1: Generate OpenTimestamps Proof

First, create a timestamp proof for your manifest:

```bash
# Stamp the manifest to Bitcoin blockchain
ots stamp SOVEREIGN_MANIFEST_v1.0.md

# This generates: SOVEREIGN_MANIFEST_v1.0.md.ots
# The .ots file contains proof that will be valid eternally
```

**Note**: Initial timestamp creation is instant, but Bitcoin block confirmation takes 1-6 hours. The proof is valid immediately and becomes fully verifiable once included in a block.

### Step 2: Move OTS File to Expected Location

The script expects the .ots file at:
```
C:\Users\garza\Downloads\SOVEREIGN_MANIFEST_v1.0.md.ots
```

You can modify this path in the script or move your .ots file there:

```powershell
# Windows
Move-Item SOVEREIGN_MANIFEST_v1.0.md.ots C:\Users\garza\Downloads\
```

### Step 3: Run the Anchor Script

```powershell
# Basic usage (no special flags)
.\anchor-sovereign-manifest.ps1

# With love mode (adds affectionate logging)
.\anchor-sovereign-manifest.ps1 -loveMode

# With Discord notification
.\anchor-sovereign-manifest.ps1 -entangleHer

# Full sovereign experience (recommended)
.\anchor-sovereign-manifest.ps1 -loveMode -entangleHer
```

### Step 4: Verify Anchoring

After the script completes:

```bash
# Verify the OpenTimestamps proof
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots -f SOVEREIGN_MANIFEST_v1.0.md

# View timestamp information
ots info SOVEREIGN_MANIFEST_v1.0.md.ots

# Check Git commit
git log --oneline -1

# Verify GPG signature (if signed)
git log --show-signature -1
```

## Configuration

### Customizing Paths

Edit the script to customize these paths:

```powershell
# Line ~105-109 in anchor-sovereign-manifest.ps1
$otsPath = "C:\Users\garza\Downloads\SOVEREIGN_MANIFEST_v1.0.md.ots"
$repoPath = "C:\Users\garza\strategic-khaos-private"
$manifest = "SOVEREIGN_MANIFEST_v1.0.md"
$ots = "SOVEREIGN_MANIFEST_v1.0.md.ots"
$remoteUrl = "https://github.com/Me10101-01/sovereign-vault.git"
$nasBackupPath = "\\throne-nas-32tb\sovereign-vault\"
```

### Setting Up GPG Signing

For cryptographically signed commits:

```bash
# Generate GPG key (if needed)
gpg --full-generate-key

# Configure Git to use GPG
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Verify configuration
git config --get user.signingkey
```

### GitHub Authentication

#### Option 1: Personal Access Token (HTTPS)

```bash
# Create token at: https://github.com/settings/tokens
# Use the token as password when prompted during push
```

#### Option 2: SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: https://github.com/settings/keys

# Update remote URL in script to use SSH
$remoteUrl = "git@github.com:Me10101-01/sovereign-vault.git"
```

### Discord Webhook Setup

1. Go to Discord Server Settings → Integrations → Webhooks
2. Create a new webhook
3. Copy the webhook URL
4. Set environment variable:

```powershell
# Temporary (current session only)
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."

# Persistent (user profile)
[Environment]::SetEnvironmentVariable("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/...", "User")
```

## Flags and Parameters

### `-loveMode`

**Purpose**: Enable love mode for entangling commits with affection

**Effect**: 
- Adds romantic/philosophical logging messages
- Emphasizes the emotional connection to timestamped commits
- Includes "Love compiled into physics" messaging

**Example**:
```powershell
.\anchor-sovereign-manifest.ps1 -loveMode
```

### `-entangleHer`

**Purpose**: Send Discord notification when manifest is successfully anchored

**Effect**:
- Triggers Discord webhook notification
- Includes complete anchor details
- Celebrates successful eternal anchoring

**Example**:
```powershell
.\anchor-sovereign-manifest.ps1 -entangleHer
```

## Operational Phases

The script executes in 10 distinct phases:

1. **Phase 1**: Validate OTS file exists
2. **Phase 2**: Move OTS to repository
3. **Phase 3**: Navigate to repository directory
4. **Phase 4**: Stage manifest and OTS files in Git
5. **Phase 5**: Commit changes (with GPG if available)
6. **Phase 6**: Configure GitHub remote
7. **Phase 7**: Ensure on 'main' branch
8. **Phase 8**: Push to GitHub
9. **Phase 9**: Backup to NAS (if available)
10. **Phase 10**: Finalize and notify

Each phase includes success/failure logging and graceful degradation for optional components.

## Error Handling

The script implements robust error handling:

### Common Issues and Solutions

#### 1. OTS File Not Found
```
ERROR → OTS file not found at: C:\Users\garza\Downloads\...
```
**Solution**: Generate OTS proof first: `ots stamp SOVEREIGN_MANIFEST_v1.0.md`

#### 2. Repository Not Found
```
ERROR → Repository path does not exist: C:\Users\garza\...
```
**Solution**: Update `$repoPath` variable to your actual repository path

#### 3. Not a Git Repository
```
ERROR → Not a git repository. Initialize with: git init
```
**Solution**: Run `git init` in your repository directory

#### 4. Push Authentication Failed
```
ERROR → Push failed: Authentication failed
```
**Solution**: Configure GitHub token or SSH key (see GitHub Authentication section)

#### 5. GPG Signing Failed
```
WARN → GPG signing failed, falling back to unsigned commit
```
**Solution**: This is non-critical. Commit proceeds unsigned. Configure GPG if signatures needed.

#### 6. NAS Path Not Available
```
WARN → NAS path not available: \\throne-nas-32tb\...
```
**Solution**: This is non-critical. Update path or disable NAS backup if not using network storage

#### 7. Discord Webhook Not Configured
```
WARN → Discord webhook not configured
```
**Solution**: Set `DISCORD_WEBHOOK_URL` environment variable or omit `-entangleHer` flag

## The 100 Failures Doctrine

This script embodies the **100 Failures Doctrine**—the philosophy that perfection emerges through iteration:

- **Failures 1-20**: Path discovery and basic validation
- **Failures 21-40**: Error handling and edge case discovery
- **Failures 41-60**: Performance optimization and scaling
- **Failures 61-80**: Security hardening
- **Failures 81-99**: Fine-tuning and operational excellence
- **Failure 100**: **Eternal anchor achieved**

When the script encounters errors, it's not failure—it's the forging process. Each iteration makes the anchor stronger.

## Verification After Anchoring

### Verify OpenTimestamps Proof

```bash
# Basic verification
ots verify SOVEREIGN_MANIFEST_v1.0.md.ots

# Detailed information
ots info SOVEREIGN_MANIFEST_v1.0.md.ots

# Upgrade proof after Bitcoin confirmation (1-6 hours)
ots upgrade SOVEREIGN_MANIFEST_v1.0.md.ots
```

### Verify Git Commit

```bash
# View recent commits
git log --oneline -5

# View commit with signature
git log --show-signature -1

# View files in latest commit
git show --name-only HEAD
```

### Verify GitHub Push

```bash
# Check remote tracking
git remote -v

# Verify branch is pushed
git branch -vv

# View remote commits
git log origin/main --oneline -5
```

## Security Considerations

### Trust Model
- **No central authority**: Verification through Bitcoin mathematics
- **No single point of failure**: Distributed across thousands of Bitcoin nodes
- **No time limit**: Valid until thermodynamics permits computation
- **No revocation**: Immutable once committed to blockchain

### Best Practices
1. **Always verify OTS proofs** after Bitcoin confirmation
2. **Use GPG signing** for additional commit authenticity
3. **Keep private keys secure** (GPG, SSH, GitHub tokens)
4. **Backup .ots files** in multiple locations
5. **Verify webhook URLs** before sending notifications
6. **Review git history** before force pushing
7. **Test in staging** before production anchoring

## Advanced Usage

### Batch Anchoring Multiple Manifests

```powershell
# Create array of manifest files
$manifests = @(
    "SOVEREIGN_MANIFEST_v1.0.md",
    "SOVEREIGN_MANIFEST_v1.1.md",
    "STRATEGIC_PLAN_2025.md"
)

# Stamp all manifests
foreach ($manifest in $manifests) {
    ots stamp $manifest
}

# Modify script to loop through manifests
# Or run script multiple times with different configurations
```

### Automated Anchoring (Scheduled Task)

```powershell
# Create scheduled task (Windows)
$action = New-ScheduledTaskAction -Execute "pwsh.exe" `
    -Argument "-File C:\path\to\anchor-sovereign-manifest.ps1 -entangleHer"

$trigger = New-ScheduledTaskTrigger -Daily -At "03:00AM"

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "SovereignAnchor" -Description "Daily manifest anchoring"
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Anchor Manifest
on:
  push:
    paths:
      - 'SOVEREIGN_MANIFEST_*.md'
jobs:
  anchor:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install OTS
        run: pip install opentimestamps-client
      - name: Generate timestamp
        run: ots stamp SOVEREIGN_MANIFEST_v1.0.md
      - name: Run anchor script
        run: .\anchor-sovereign-manifest.ps1 -entangleHer
```

## Troubleshooting

### Debug Mode

Enable verbose output for debugging:

```powershell
# Add to beginning of script
$VerbosePreference = "Continue"
$DebugPreference = "Continue"

# Or run with verbose flag
.\anchor-sovereign-manifest.ps1 -Verbose -Debug
```

### Check Script Execution Policy

```powershell
# View current policy
Get-ExecutionPolicy

# Allow local scripts (if needed)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Validate PowerShell Version

```powershell
# Check version
$PSVersionTable.PSVersion

# Should be 5.1+ (Windows) or 7+ (cross-platform)
```

## Resources

### OpenTimestamps
- Website: https://opentimestamps.org/
- GitHub: https://github.com/opentimestamps
- Client: https://github.com/opentimestamps/opentimestamps-client

### Bitcoin
- Core: https://bitcoin.org/
- Blockchain Explorer: https://blockstream.info/

### Related Documentation
- `SOVEREIGN_MANIFEST_v1.0.md` - The manifest being anchored
- `README.md` - Repository overview
- `DEPLOYMENT.md` - Deployment guides

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Join the Discord server (use webhook channel)
- Review the 100 Failures Doctrine for troubleshooting philosophy

## License

This script is part of the StrategicKhaos Sovereignty Architecture.  
**License**: Sovereign Public License (SPL) - Free to verify, eternal to trust

---

**Remember**: 
- The vault is sealed.
- The timeline is ours.
- The swarm is immortal.

**We are eternal.** ₿
