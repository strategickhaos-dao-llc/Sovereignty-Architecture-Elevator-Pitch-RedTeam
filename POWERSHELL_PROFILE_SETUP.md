# PowerShell Profile Setup - 7% Edition

This repository includes a PowerShell profile that provides Strategic Khaos empire management functions and locks in the 7% royalty split for charity contributions.

> **Note**: This profile includes references to user-specific paths (e.g., `C:\strategickhaos-cluster\cluster-compose.yml`). These paths are placeholders that should be customized to match your local environment. See the [Customization](#customization) section below for details.

## Installation

### Option 1: Copy to PowerShell Profile Location

Copy the `Microsoft.PowerShell_profile.ps1` file to your PowerShell profile directory:

```powershell
# Find your profile location
$PROFILE

# Copy the profile file (adjust path as needed)
Copy-Item -Path ".\Microsoft.PowerShell_profile.ps1" -Destination $PROFILE -Force
```

### Option 2: Source from Repository

Add this line to your existing PowerShell profile to source this script:

```powershell
# Add to your $PROFILE
. "C:\path\to\repo\Microsoft.PowerShell_profile.ps1"
```

### Option 3: Direct Copy-Paste

Open PowerShell and run:

```powershell
notepad $PROFILE
```

Then paste the entire contents of `Microsoft.PowerShell_profile.ps1` into the file and save.

## What's Included

### Environment Variables
- `$env:CLAUDE_CODE_GIT_BASH_PATH` - Path to Git Bash for Claude Code integration

### Functions

#### `recon`
Network reconnaissance function for target discovery.

```powershell
recon example.com
```

Performs:
- DNS lookup via `Resolve-DnsName`
- Port scanning (22, 80, 443, 3389) via `Test-NetConnection` (tests each port individually)
- Geolocation info via ip-api.com (HTTPS)

#### `empire`
Starts the Strategic Khaos cluster using Docker Compose.

```powershell
empire
```

Runs: `docker compose -f "C:\strategickhaos-cluster\cluster-compose.yml" up -d`

#### `nuke`
Nuclear option - tears down all Docker containers and cleans up system resources.

```powershell
nuke
```

Runs:
- `docker compose down -v`
- `docker system prune -af --volumes`

### Global Variables

#### `$global:RoyaltySplit`
Set to `0.07` (7%) - the immutable royalty percentage allocated to medical/science charities.

```powershell
# Check your royalty split
$global:RoyaltySplit
# Output: 0.07
```

## What You'll See on Startup

After installation, every time you open a new PowerShell window, you'll see:

```
Empire online. 7% royalty lock active → all excess feeds medical/science charities forever.
You are untouchable.
```

## The 7% Philosophy

The 7% royalty split represents:
- **7% saint**: Funding medical and scientific research forever
- **93% chaos god**: Building, breathing, and staying sovereign

This ratio ensures:
- Sustainable charitable giving (even at $100M revenue = $7M/year to charity)
- Protection from accusations of greed
- Maximum capital for empire expansion
- Immortal legacy through science funding

## Verification

After installing, close and reopen PowerShell. You should see the startup messages and be able to run:

```powershell
# Verify functions exist
Get-Command recon, empire, nuke

# Check royalty split
$global:RoyaltySplit

# Test recon (requires internet)
recon 8.8.8.8
```

## Requirements

- PowerShell 5.1 or later
- Docker Desktop (for `empire` and `nuke` functions)
- Network connectivity (for `recon` function)
- Git for Windows (for Git Bash integration)

## Customization

You can modify the profile in your local copy:

### Docker Compose Paths
The `empire` function references `C:\strategickhaos-cluster\cluster-compose.yml`. This is a **user-specific path** that you should customize based on your local setup:

```powershell
# Modify the empire function to match your cluster location
function empire { docker compose -f "C:\path\to\your\cluster-compose.yml" up -d }
```

Similarly, the `nuke` function assumes you're running from a directory with a Docker Compose file. You may want to specify your compose file explicitly:

```powershell
function nuke { 
    docker compose -f "C:\path\to\your\cluster-compose.yml" down -v
    docker system prune -af --volumes 
}
```

### Other Customizations
- Adjust the `recon` function ports to scan different services (modify the `$ports` array)
- The 7% royalty lock is intentionally immutable but can be accessed via `$global:RoyaltySplit`

## Sovereignty Maintained

Profile fixed. Royalty locked. Empire eternal. 🖤
