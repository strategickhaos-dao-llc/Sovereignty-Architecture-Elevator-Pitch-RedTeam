# GitHub Operator v1.1 - Usage Guide

**A PowerShell tool for managing GitHub profile and repository metadata for StrategicKhaos DAO LLC.**

## Overview

The GitHub Operator script (`github-operator.ps1`) provides three main operations for managing your GitHub presence:

1. **Status Check** - Scan your GitHub account state
2. **Manifesto Generation** - Create and commit a README with StrategicKhaos DAO mission
3. **Profile Forge** - Complete profile upgrade with bio update and README creation

## Prerequisites

- **PowerShell** - Windows PowerShell 5.1+ or PowerShell Core 7+
- **GitHub CLI** - Must be installed and authenticated (`gh auth login`)
- **Git Repository** - Must be run from within a git repository

## Installation

1. Clone this repository or download `github-operator.ps1`
2. Navigate to your repository directory
3. Ensure GitHub CLI is authenticated:
   ```powershell
   gh auth login
   gh auth status
   ```

## Usage

### Check GitHub Account Status

Displays your GitHub login, number of public repositories, bio, and lists your recent repositories:

```powershell
.\github-operator.ps1 -status
```

**Example Output:**
```
[09:04:43] Scanning GitHub account: Strategickhaos
[09:04:43] Strategickhaos
[09:04:43] 6
[09:04:43] StrategicKhaos DAO LLC...
[09:04:43] Recent repositories:
[09:04:43] - Sovereignty-Architecture: Discord DevOps control plane
[09:04:43] - GPT_Vim_DevHub: AI + Vim development lab
...
```

### Generate README Manifesto

Creates a `README.md` file in the current repository with the StrategicKhaos DAO LLC mission statement, commits, and pushes it:

```powershell
.\github-operator.ps1 -manifesto
```

**What it does:**
1. Generates a comprehensive README.md with:
   - StrategicKhaos DAO LLC header
   - Wyoming DAO LLC legal information
   - EIN number (39-2900295)
   - Mission statement with philanthropic commitments
   - Repository sovereignty stack information
   - Links to other projects
2. Commits with message: "Forge README: StrategicKhaos DAO manifesto v1.0"
3. Pushes to remote repository

**Note:** If this is your profile repository (e.g., `Strategickhaos/Strategickhaos`), GitHub will automatically display this README on your profile page.

### Full Profile Forge

Performs a complete profile upgrade by updating your GitHub bio and creating the manifesto:

```powershell
.\github-operator.ps1 -forge
```

**What it does:**
1. Updates your GitHub bio to:
   ```
   StrategicKhaos DAO LLC · Wyoming §17-31-101 · EIN 39-2900295 · AI-governed perpetual philanthropy. Code is law. Love is protocol. ⚔️
   ```
2. Runs the `-manifesto` operation to create and commit README.md
3. Provides instructions for manually pinning repositories

**Manual Steps After Forge:**
1. Go to your GitHub profile (e.g., `https://github.com/Strategickhaos`)
2. Click "Customize your pins"
3. Select this repository and your compliance vault to pin them

## Default Behavior

If no parameters are specified, the script defaults to running the `-status` check:

```powershell
.\github-operator.ps1
# Equivalent to: .\github-operator.ps1 -status
```

## Error Handling

The script includes built-in validation:

- **Not in Git Repository**: Will exit with error if not run from within a git repository
- **GitHub CLI Not Authenticated**: Will exit with error and prompt you to run `gh auth login`

## Examples

### Example 1: Initial Setup in New Repository

```powershell
# Navigate to your repository
cd C:\repos\my-strategickhaos-repo

# Check current GitHub status
.\github-operator.ps1 -status

# Create manifesto README
.\github-operator.ps1 -manifesto
```

### Example 2: Complete Profile Setup

```powershell
# Navigate to your profile repository (e.g., Strategickhaos/Strategickhaos)
cd C:\repos\Strategickhaos

# Perform full forge operation
.\github-operator.ps1 -forge

# Then manually pin repositories via GitHub UI
```

### Example 3: Update Existing Profile

```powershell
# Navigate to any repository you want to add manifesto to
cd C:\Users\garza\strategic-khaos-private

# Add manifesto to this repo
.\github-operator.ps1 -manifesto
```

## Technical Details

### README Template

The generated README includes:
- Legal entity information (Wyoming DAO LLC §17-31-101)
- EIN: 39-2900295
- AI-governed perpetual philanthropy mission
- 7% irrevocable allocation to:
  - St. Jude Children's Research Hospital
  - Doctors Without Borders
  - Veteran Debt Relief initiatives
  - Ethical hacker education
  - Rare disease research
- Sovereignty stack features (GPG signatures, GitHub notarization, OpenTimestamps)
- Links to other projects

### Color-Coded Logging

The script uses color-coded output for better readability:
- **Green**: Success messages
- **Red**: Error messages
- **Cyan**: Informational messages
- **Yellow**: Status updates
- **Gray**: Standard log entries

## Troubleshooting

### "Not inside a git repository"
**Solution**: Navigate to a git repository before running the script.

### "GitHub CLI not authed"
**Solution**: Run `gh auth login` to authenticate with GitHub.

### README not appearing on profile
**Solution**: Ensure your repository name matches your username (e.g., `Strategickhaos/Strategickhaos`).

### Changes not pushed
**Solution**: Check git remote configuration with `git remote -v` and ensure you have push permissions.

## Security Considerations

- The script uses GitHub CLI authentication, which is secure and token-based
- Bio updates use the GitHub API with proper authentication
- All git operations (commit, push) use your configured git credentials
- No hardcoded credentials or secrets in the script

## Future Enhancements

Potential future additions mentioned in the documentation:
- **-pin mode**: Automatically pin repositories using GitHub GraphQL API
- **-proof mode**: Sovereign Proof Scanner that walks repos for .gpg, .ots, and EIN references

## Support

For issues or questions:
- GitHub Issues: [Sovereignty-Architecture-Elevator-Pitch Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- Review the script source code for detailed implementation

---

**Built for StrategicKhaos DAO LLC**  
*"Code is law. Love is protocol."* ⚔️
