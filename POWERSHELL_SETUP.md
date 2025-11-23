# ⚡ POWERSHELL SOVEREIGNTY SETUP

**30 Second Installation Guide**

---

## 🚀 QUICK INSTALL (Copy-Paste This)

Open PowerShell and run:

```powershell
# Install the sovereignty profile
Copy-Item .\PowerShellProfile.ps1 $PROFILE -Force
. $PROFILE
```

**That's it!** You now have:
- `recon <target>` - Network reconnaissance
- `empire` - Launch sovereignty cluster  
- `nuke` - Complete teardown

---

## 📋 WHAT EACH FUNCTION DOES

### `recon <target>`

Performs comprehensive reconnaissance on any target:

```powershell
recon google.com
recon 8.8.8.8
```

**Features:**
- DNS lookup (nslookup)
- Port scanning (22, 80, 443, 3389, 8080, 8443)
- Geolocation information
- Color-coded output

### `empire`

Launches the complete Strategickhaos sovereignty cluster:

```powershell
empire
```

**What it does:**
1. Looks for cluster compose files in order:
   - `C:\strategickhaos-cluster\cluster-compose.yml`
   - `.\docker-compose-cloudos.yml`
   - `.\docker-compose.yml`
2. Starts all services via docker compose
3. Shows service status
4. Displays "7% sovereign lock active. You are untouchable."

### `nuke`

Nuclear option - complete teardown and cleanup:

```powershell
nuke
```

**What it does:**
1. Asks for confirmation (type `NUKE`)
2. Stops all docker compose stacks
3. Removes all volumes
4. Performs `docker system prune -af --volumes`
5. **WARNING: This is destructive and cannot be undone!**

---

## 🎨 CUSTOM STARTUP BANNER

When you load PowerShell, you'll see:

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          STRATEGICKHAOS SOVEREIGNTY ARCHITECTURE           ║
║                                                            ║
║  Empire online. 7% sovereign lock active.                 ║
║  You are untouchable.                                     ║
║                                                            ║
║  Commands:                                                ║
║    recon <target>  - Network reconnaissance               ║
║    empire          - Launch sovereignty cluster           ║
║    nuke            - Nuclear teardown & cleanup           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🔧 CUSTOMIZATION

### Find Your Profile Location

```powershell
echo $PROFILE
```

Typical locations:
- Current User, Current Host: `~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
- Current User, All Hosts: `~\Documents\WindowsPowerShell\profile.ps1`

### Edit Your Profile

```powershell
notepad $PROFILE
```

### Add Your Own Functions

Add custom functions to the profile:

```powershell
function mycommand {
    Write-Host "My custom command!" -ForegroundColor Green
}
```

### Change Compose File Location

Edit the `$composeFiles` array in `PowerShellProfile.ps1`:

```powershell
$composeFiles = @(
    "C:\your\custom\path\cluster-compose.yml",
    ".\docker-compose-cloudos.yml",
    ".\docker-compose.yml"
)
```

---

## 🛠️ TROUBLESHOOTING

### Profile Not Loading?

**Check execution policy:**
```powershell
Get-ExecutionPolicy
```

If it shows `Restricted`, change it:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then reload:
```powershell
. $PROFILE
```

### Functions Not Working?

**Reload the profile:**
```powershell
. $PROFILE
```

**Or restart PowerShell entirely**

### Docker Not Found?

Install Docker Desktop:
```powershell
# Using winget
winget install Docker.DockerDesktop

# Or download from
# https://www.docker.com/products/docker-desktop/
```

### Empire Command Fails?

**Check if Docker is running:**
```powershell
docker ps
```

**Check if compose file exists:**
```powershell
Test-Path .\cluster-compose.yml
```

**Manual start:**
```powershell
docker compose -f cluster-compose.yml up -d
```

---

## 📦 INCLUDED ALIASES

The profile also sets up helpful aliases:

- `ll` → `Get-ChildItem` (like `ls -la` in Linux)
- `k` → `kubectl` (if kubectl is installed)
- `dc` → `docker-compose` (for quick access)

---

## 🎯 USAGE EXAMPLES

### Network Reconnaissance

```powershell
# Check a domain
recon strategickhaos.com

# Check an IP
recon 8.8.8.8

# Check local network
recon 192.168.1.1
```

### Launch Empire

```powershell
# Start everything
empire

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Emergency Shutdown

```powershell
# Complete cleanup
nuke
# (type NUKE when prompted)

# Or just stop services
docker compose down
```

---

## 🌟 BONUS FEATURES

### UTF-8 Encoding

Automatically sets UTF-8 encoding for proper character display:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### TLS 1.2 Support

Ensures secure web requests:
```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### Optional Custom Prompt

Uncomment in `PowerShellProfile.ps1` for a custom prompt with git branch display.

---

## 📚 ADDITIONAL RESOURCES

- **Main Guide:** `INSTALL_SOVEREIGNTY.md`
- **Manifest:** `SOVEREIGN_MANIFEST_v1.0-m.md`
- **Cluster Config:** `cluster-compose.yml`
- **Bitcoin Timestamp:** `bitcoin-timestamp.ps1`

---

## 💡 PRO TIPS

1. **Use Tab Completion:** Type `rec` and press Tab to autocomplete `recon`
2. **Check History:** `Get-History` to see your command history
3. **Clear Screen:** `cls` or `Clear-Host`
4. **Profile Path:** Save `$PROFILE` value for quick access
5. **Backup Profile:** Keep a copy of your profile in version control

---

## 🎉 YOU'RE READY

Your PowerShell is now sovereign.

Empire at your fingertips.  
Reconnaissance on demand.  
Nuclear option available.

**7% royalty lock active.**  
**You are untouchable.**

---

*Empire online. Sovereignty achieved. Dream eternal. 🖤*
