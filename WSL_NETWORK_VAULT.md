# WSL Network Knowledge Vault - Documentation

## 🔐 Sovereignty Architecture - Encrypted Family Knowledge Vault

This system provides secure, encrypted storage of WSL network configuration snapshots, designed for omnipresent knowledge access by authorized family members.

## Overview

The WSL Network Knowledge Vault captures network configuration data from Windows Subsystem for Linux (WSL) environments and stores it in an encrypted vault using Windows Data Protection API (DPAPI). This creates a secure knowledge base that can be accessed by authorized family members while protecting sensitive network information.

### Key Features

- **Encrypted Storage**: Uses Windows DPAPI with AES-256 encryption
- **Access Control**: Grant/revoke access to specific family members
- **Auto-Capture**: Automatic snapshot on WSL startup or Windows logon
- **Audit Trail**: Complete logging of all vault operations
- **PowerShell Format Export**: Compatible with existing proof systems

## Quick Start

### Windows PowerShell

```powershell
# 1. Initialize the vault
.\scripts\wsl-network-vault.ps1 -Action setup

# 2. Capture your first network snapshot
.\scripts\wsl-network-vault.ps1 -Action capture

# 3. Grant access to family members
.\scripts\wsl-network-vault.ps1 -Action grant-access -Username "MyChild"

# 4. View vault status
.\scripts\wsl-network-vault.ps1 -Action status
```

### WSL/Linux Bash

```bash
# 1. Capture network configuration
./scripts/wsl-auto-capture.sh capture

# 2. List stored snapshots
./scripts/wsl-auto-capture.sh list

# 3. Export in PowerShell format
./scripts/wsl-auto-capture.sh export
```

## Detailed Usage

### PowerShell Script: `wsl-network-vault.ps1`

#### Actions

| Action | Description |
|--------|-------------|
| `setup` | Initialize the encrypted vault structure |
| `capture` | Capture and encrypt a new WSL network snapshot |
| `store` | Alias for capture |
| `list` | List all stored snapshots |
| `retrieve` | Decrypt and display a specific snapshot |
| `grant-access` | Grant vault access to a family member |
| `revoke-access` | Revoke vault access from a user |
| `auto-capture` | Configure automatic capture on WSL startup |
| `status` | Display vault status and statistics |

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-VaultPath` | Custom vault location | `~\.sovereignty-vault\network-knowledge` |
| `-Username` | Username for access control operations | - |
| `-SnapshotId` | Snapshot ID for retrieval | - |
| `-Force` | Force operation | `$false` |

### Bash Script: `wsl-auto-capture.sh`

#### Commands

| Command | Description |
|---------|-------------|
| `capture` | Capture current WSL network configuration |
| `list` | List all stored snapshots |
| `export` | Export latest capture in PowerShell format |
| `bashrc` | Show .bashrc integration snippet |
| `status` | Show vault status |
| `help` | Show help message |

## Auto-Capture Configuration

### Option 1: WSL `.bashrc` Integration

Add the following to your `~/.bashrc` in WSL:

```bash
# Sovereignty Architecture - WSL Network Auto-Capture
sovereignty_auto_capture() {
    local CAPTURE_DIR="/mnt/c/Users/$USER/.sovereignty-vault/network-knowledge/wsl-captures"
    local LOG_FILE="/mnt/c/Users/$USER/.sovereignty-vault/network-knowledge/logs/wsl-capture-$(date +%Y%m%d).log"
    
    mkdir -p "$CAPTURE_DIR" 2>/dev/null
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null
    
    {
        echo "=========================================="
        echo "WSL Network Capture - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "=========================================="
        ip addr 2>/dev/null
        ip route 2>/dev/null
        echo "=========================================="
    } >> "$LOG_FILE" 2>&1
    
    echo "🔒 Network snapshot captured to Sovereignty Vault"
}

if [[ $- == *i* ]]; then
    sovereignty_auto_capture
fi
```

### Option 2: PowerShell Profile Integration

Add to your PowerShell profile (`$PROFILE`):

```powershell
# Sovereignty Architecture - Auto-capture on PowerShell startup
function Start-SovereigntyNetworkCapture {
    # Auto-detect script location from common paths
    $possiblePaths = @(
        "$env:USERPROFILE\.sovereignty-vault\scripts\wsl-network-vault.ps1",
        "$PSScriptRoot\wsl-network-vault.ps1",
        (Join-Path (Get-Location) "scripts\wsl-network-vault.ps1")
    )
    
    $scriptPath = $possiblePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    
    if ($scriptPath) {
        & $scriptPath -Action capture
    }
}

# Uncomment to enable auto-capture:
# Start-SovereigntyNetworkCapture
```

### Option 3: Windows Task Scheduler

Import the scheduled task to capture on logon:

```powershell
# Run the auto-capture setup
.\scripts\wsl-network-vault.ps1 -Action auto-capture

# Then import the generated task
schtasks /create /tn "SovereigntyNetworkCapture" /xml "$env:USERPROFILE\.sovereignty-vault\network-knowledge\auto-capture-config\scheduled-task.xml"
```

## Vault Structure

```
~\.sovereignty-vault\network-knowledge\
├── snapshots\              # Encrypted snapshot files (.vault)
│   ├── snapshot_20241201_143022.vault
│   └── snapshot_20241201_180045.vault
├── access\                 # Access control logs
│   └── access-log.json
├── logs\                   # Operation logs
│   └── vault-20241201.log
├── keys\                   # Key material (managed by DPAPI)
├── wsl-captures\           # Raw WSL captures (from bash script)
│   └── network_capture_20241201_143022.txt
├── auto-capture-config\    # Auto-capture configuration files
│   ├── bashrc-snippet.sh
│   ├── ps-profile-snippet.ps1
│   └── scheduled-task.xml
└── vault-metadata.json     # Vault metadata and configuration
```

## Security Model

### Encryption

- **Method**: Windows Data Protection API (DPAPI) with AES-256
- **Scope**: CurrentUser (encrypted data only accessible by the same Windows user)
- **Entropy**: Custom entropy string for additional security

### Access Control

- **Owner**: Full control over vault contents
- **Authorized Users**: Read access to decrypt and view snapshots
- **Audit Trail**: All access grant/revoke operations logged

### Captured Data

The following network information is captured:

| Data Type | Source Command | Description |
|-----------|----------------|-------------|
| IP Addresses | `ip addr` | All network interfaces with IP configuration |
| Routing Table | `ip route` | Network routing information |
| Network Statistics | `netstat` | Active connections and sockets |
| DNS Configuration | `/etc/resolv.conf` | DNS resolver settings |
| Socket Statistics | `ss -tulpn` | Listening ports and connections |
| Docker Networks | `docker network ls` | Docker network configuration (if available) |

## Integration with Sovereignty Architecture

### Vault Security Playbook Integration

The WSL Network Knowledge Vault follows the same security patterns defined in `VAULT_SECURITY_PLAYBOOK.md`:

- Implements principle of least privilege for access control
- Uses secure encryption methods (DPAPI with AES-256)
- Maintains comprehensive audit logging
- Supports automated capture schedules

### Proof System Integration

Export snapshots in PowerShell here-string format for integration with the Strategic Khaos proof system:

```powershell
# Using the bash script
./scripts/wsl-auto-capture.sh export

# This creates a file with format:
$wslNetworkSnapshot = @'
[IP ADDR OUTPUT]
[NETSTAT OUTPUT]
...
'@
```

## Troubleshooting

### Common Issues

**Vault not initialized:**
```powershell
.\scripts\wsl-network-vault.ps1 -Action setup
```

**WSL not running:**
```powershell
# Start WSL first
wsl --list --running
wsl -d Ubuntu  # Or your distro name
```

**Permission denied:**
```powershell
# Check vault permissions
Get-Acl $env:USERPROFILE\.sovereignty-vault\network-knowledge | Format-List
```

**Decryption fails:**
- Ensure you're logged in as the same Windows user who created the snapshot
- Check that the encryption scope matches (CurrentUser vs LocalMachine)

### Logs

Check the vault logs for detailed operation history:
```powershell
Get-Content "$env:USERPROFILE\.sovereignty-vault\network-knowledge\logs\vault-$(Get-Date -Format 'yyyyMMdd').log"
```

## Family Knowledge Base Use Case

This vault is designed to create an educational knowledge base for family members:

1. **Educational Resource**: Children can learn about network configuration by reviewing historical snapshots
2. **Security Awareness**: Demonstrates proper security practices (encryption, access control)
3. **Technical Documentation**: Creates a living record of home network evolution
4. **Omnipresent Access**: Authorized family members can access the knowledge base from any Windows session

### Granting Access to Children

```powershell
# Grant access to a child's Windows account
.\scripts\wsl-network-vault.ps1 -Action grant-access -Username "ChildUsername"

# Verify access was granted
.\scripts\wsl-network-vault.ps1 -Action status
```

## License

MIT License - Strategic Khaos DAO LLC

---

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

*Empowering sovereign digital infrastructure through encrypted knowledge preservation*
