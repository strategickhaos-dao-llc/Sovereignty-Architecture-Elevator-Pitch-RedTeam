# wsl-network-vault.ps1 - WSL Network Snapshot Encrypted Vault
# Sovereignty Architecture - Omnipresent Knowledge Vault for Family Access
# Strategic Khaos DAO LLC - Domenic Garza (Node 137)
# 
# PURPOSE: Secure encrypted storage of WSL network configuration snapshots
# for authorized family member access (children's knowledge base)

param(
    [Parameter(Position = 0)]
    [ValidateSet("capture", "store", "list", "retrieve", "grant-access", "revoke-access", "status", "setup", "auto-capture")]
    [string]$Action = "status",
    
    [Parameter()]
    [string]$VaultPath = "$env:USERPROFILE\.sovereignty-vault\network-knowledge",
    
    [Parameter()]
    [string]$Username,
    
    [Parameter()]
    [string]$SnapshotId,
    
    [Parameter()]
    [switch]$Force
)

# =============================================================================
# CONFIGURATION
# =============================================================================

$script:VaultConfig = @{
    Version          = "1.0.0"
    VaultPath        = $VaultPath
    SnapshotsDir     = Join-Path $VaultPath "snapshots"
    AccessControlDir = Join-Path $VaultPath "access"
    LogsDir          = Join-Path $VaultPath "logs"
    KeysDir          = Join-Path $VaultPath "keys"
    MetadataFile     = Join-Path $VaultPath "vault-metadata.json"
    EncryptionScope  = "CurrentUser"  # Can be "LocalMachine" for shared access
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

function Write-VaultLog {
    param(
        [string]$Message,
        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    # Console output with colors
    $color = switch ($Level) {
        "INFO"    { "Cyan" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR"   { "Red" }
    }
    Write-Host $logEntry -ForegroundColor $color
    
    # File logging
    $logFile = Join-Path $script:VaultConfig.LogsDir "vault-$(Get-Date -Format 'yyyyMMdd').log"
    if (Test-Path (Split-Path $logFile -Parent)) {
        $logEntry | Out-File -FilePath $logFile -Append -Encoding UTF8
    }
}

function Initialize-VaultStructure {
    <#
    .SYNOPSIS
    Creates the vault directory structure with proper permissions
    #>
    
    Write-VaultLog "Initializing Sovereignty Network Knowledge Vault..." -Level INFO
    
    # Create directory structure
    $dirs = @(
        $script:VaultConfig.VaultPath,
        $script:VaultConfig.SnapshotsDir,
        $script:VaultConfig.AccessControlDir,
        $script:VaultConfig.LogsDir,
        $script:VaultConfig.KeysDir
    )
    
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
            Write-VaultLog "Created directory: $dir" -Level INFO
        }
    }
    
    # Set restrictive permissions (owner only by default)
    try {
        $acl = Get-Acl $script:VaultConfig.VaultPath
        $acl.SetAccessRuleProtection($true, $false)
        
        # Add owner full control
        $ownerRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            $env:USERNAME,
            "FullControl",
            "ContainerInherit,ObjectInherit",
            "None",
            "Allow"
        )
        $acl.AddAccessRule($ownerRule)
        Set-Acl -Path $script:VaultConfig.VaultPath -AclObject $acl
        Write-VaultLog "Set vault permissions for owner: $env:USERNAME" -Level SUCCESS
    }
    catch {
        Write-VaultLog "Could not set permissions: $_" -Level WARNING
    }
    
    # Initialize metadata
    if (-not (Test-Path $script:VaultConfig.MetadataFile)) {
        $metadata = @{
            created          = (Get-Date).ToUniversalTime().ToString("o")
            version          = $script:VaultConfig.Version
            owner            = $env:USERNAME
            authorizedUsers  = @($env:USERNAME)
            snapshotCount    = 0
            lastModified     = (Get-Date).ToUniversalTime().ToString("o")
            purpose          = "Family Knowledge Vault - WSL Network Configuration Archive"
            encryptionMethod = "DPAPI-AES256"
        }
        $metadata | ConvertTo-Json -Depth 10 | Out-File -FilePath $script:VaultConfig.MetadataFile -Encoding UTF8
        Write-VaultLog "Created vault metadata" -Level SUCCESS
    }
    
    Write-VaultLog "Vault initialization complete" -Level SUCCESS
    return $true
}

# =============================================================================
# WSL NETWORK CAPTURE
# =============================================================================

function Get-WSLNetworkSnapshot {
    <#
    .SYNOPSIS
    Captures WSL network configuration using ip addr, netstat, and other tools
    #>
    
    Write-VaultLog "Capturing WSL network snapshot..." -Level INFO
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $snapshotId = "snapshot_$timestamp"
    
    # Capture network data from WSL
    $networkData = @{
        snapshotId       = $snapshotId
        captureTime      = (Get-Date).ToUniversalTime().ToString("o")
        captureTimeLocal = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
        hostname         = $env:COMPUTERNAME
        capturedBy       = $env:USERNAME
        wslDistro        = ""
        networkInfo      = @{}
    }
    
    try {
        # Get WSL distribution name
        $wslDistro = wsl -l -q 2>$null | Where-Object { $_ -match '\S' } | Select-Object -First 1
        $networkData.wslDistro = if ($wslDistro) { $wslDistro.Trim() } else { "Unknown" }
        
        # Capture ip addr output
        Write-VaultLog "Capturing ip addr..." -Level INFO
        $ipAddr = wsl ip addr 2>&1
        $networkData.networkInfo.ipAddr = $ipAddr -join "`n"
        
        # Capture netstat output
        Write-VaultLog "Capturing netstat..." -Level INFO
        $netstat = wsl netstat 2>&1
        $networkData.networkInfo.netstat = $netstat -join "`n"
        
        # Capture route info
        Write-VaultLog "Capturing routing table..." -Level INFO
        $routes = wsl ip route 2>&1
        $networkData.networkInfo.routes = $routes -join "`n"
        
        # Capture DNS configuration
        Write-VaultLog "Capturing DNS configuration..." -Level INFO
        $dns = wsl cat /etc/resolv.conf 2>&1
        $networkData.networkInfo.dns = $dns -join "`n"
        
        # Capture hostname info
        Write-VaultLog "Capturing hostname info..." -Level INFO
        $hostnameInfo = wsl hostname -I 2>&1
        $networkData.networkInfo.hostnameIPs = $hostnameInfo -join "`n"
        
        # Parse key network interfaces with more precise IPv4 regex
        $networkData.parsedInterfaces = @()
        $ipv4Pattern = '\d+:\s+(\w+):.*?inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        $interfaces = $ipAddr -join "`n" | Select-String -Pattern $ipv4Pattern -AllMatches
        foreach ($match in $interfaces.Matches) {
            $ipAddress = $match.Groups[2].Value
            # Validate IP octets are in valid range (0-255)
            $octets = $ipAddress -split '\.'
            $validIp = $true
            foreach ($octet in $octets) {
                if ([int]$octet -gt 255) { $validIp = $false; break }
            }
            if ($validIp) {
                $networkData.parsedInterfaces += @{
                    interface = $match.Groups[1].Value
                    ipv4      = $ipAddress
                }
            }
        }
        
        Write-VaultLog "Network snapshot captured successfully: $snapshotId" -Level SUCCESS
    }
    catch {
        Write-VaultLog "Error capturing network data: $_" -Level ERROR
        
        # Fallback - create snapshot with error info
        $networkData.networkInfo.error = $_.Exception.Message
        $networkData.networkInfo.ipAddr = "WSL not available or not running"
    }
    
    return $networkData
}

# =============================================================================
# ENCRYPTION FUNCTIONS
# =============================================================================

function Protect-VaultData {
    <#
    .SYNOPSIS
    Encrypts data using Windows Data Protection API (DPAPI) with AES
    #>
    param(
        [Parameter(Mandatory)]
        [string]$PlainText,
        
        [Parameter()]
        [ValidateSet("CurrentUser", "LocalMachine")]
        [string]$Scope = "CurrentUser"
    )
    
    try {
        Add-Type -AssemblyName System.Security
        
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($PlainText)
        $entropy = [System.Text.Encoding]::UTF8.GetBytes("SovereigntyArchitecture-FamilyVault-2024")
        
        $protectionScope = if ($Scope -eq "CurrentUser") {
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        }
        else {
            [System.Security.Cryptography.DataProtectionScope]::LocalMachine
        }
        
        $encryptedBytes = [System.Security.Cryptography.ProtectedData]::Protect(
            $bytes,
            $entropy,
            $protectionScope
        )
        
        return [Convert]::ToBase64String($encryptedBytes)
    }
    catch {
        Write-VaultLog "Encryption error: $_" -Level ERROR
        throw
    }
}

function Unprotect-VaultData {
    <#
    .SYNOPSIS
    Decrypts data protected with DPAPI
    #>
    param(
        [Parameter(Mandatory)]
        [string]$EncryptedText,
        
        [Parameter()]
        [ValidateSet("CurrentUser", "LocalMachine")]
        [string]$Scope = "CurrentUser"
    )
    
    try {
        Add-Type -AssemblyName System.Security
        
        $encryptedBytes = [Convert]::FromBase64String($EncryptedText)
        $entropy = [System.Text.Encoding]::UTF8.GetBytes("SovereigntyArchitecture-FamilyVault-2024")
        
        $protectionScope = if ($Scope -eq "CurrentUser") {
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        }
        else {
            [System.Security.Cryptography.DataProtectionScope]::LocalMachine
        }
        
        $decryptedBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
            $encryptedBytes,
            $entropy,
            $protectionScope
        )
        
        return [System.Text.Encoding]::UTF8.GetString($decryptedBytes)
    }
    catch {
        Write-VaultLog "Decryption error: $_" -Level ERROR
        throw
    }
}

# =============================================================================
# VAULT OPERATIONS
# =============================================================================

function Save-NetworkSnapshot {
    <#
    .SYNOPSIS
    Captures and saves an encrypted WSL network snapshot to the vault
    #>
    
    Initialize-VaultStructure | Out-Null
    
    # Capture the snapshot
    $snapshot = Get-WSLNetworkSnapshot
    
    # Convert to JSON and encrypt
    $snapshotJson = $snapshot | ConvertTo-Json -Depth 10 -Compress
    $encryptedData = Protect-VaultData -PlainText $snapshotJson -Scope $script:VaultConfig.EncryptionScope
    
    # Create encrypted snapshot file
    $snapshotFile = Join-Path $script:VaultConfig.SnapshotsDir "$($snapshot.snapshotId).vault"
    
    $vaultEntry = @{
        snapshotId      = $snapshot.snapshotId
        createdAt       = $snapshot.captureTime
        encryptedData   = $encryptedData
        checksum        = (Get-FileHash -InputStream ([System.IO.MemoryStream]::new([System.Text.Encoding]::UTF8.GetBytes($snapshotJson))) -Algorithm SHA256).Hash
        encryptionScope = $script:VaultConfig.EncryptionScope
    }
    
    $vaultEntry | ConvertTo-Json -Depth 10 | Out-File -FilePath $snapshotFile -Encoding UTF8
    
    # Update metadata
    $metadata = Get-Content $script:VaultConfig.MetadataFile | ConvertFrom-Json
    $metadata.snapshotCount = (Get-ChildItem $script:VaultConfig.SnapshotsDir -Filter "*.vault").Count
    $metadata.lastModified = (Get-Date).ToUniversalTime().ToString("o")
    $metadata | ConvertTo-Json -Depth 10 | Out-File -FilePath $script:VaultConfig.MetadataFile -Encoding UTF8
    
    Write-VaultLog "Snapshot saved to encrypted vault: $($snapshot.snapshotId)" -Level SUCCESS
    
    return @{
        snapshotId   = $snapshot.snapshotId
        savedAt      = $snapshot.captureTime
        vaultFile    = $snapshotFile
        checksumSHA256 = $vaultEntry.checksum
    }
}

function Get-VaultSnapshots {
    <#
    .SYNOPSIS
    Lists all snapshots in the vault
    #>
    
    if (-not (Test-Path $script:VaultConfig.SnapshotsDir)) {
        Write-VaultLog "Vault not initialized. Run with -Action setup first." -Level WARNING
        return @()
    }
    
    $snapshots = Get-ChildItem $script:VaultConfig.SnapshotsDir -Filter "*.vault" | ForEach-Object {
        try {
            $content = Get-Content $_.FullName | ConvertFrom-Json
            [PSCustomObject]@{
                SnapshotId = $content.snapshotId
                CreatedAt  = $content.createdAt
                File       = $_.Name
                Size       = "{0:N2} KB" -f ($_.Length / 1KB)
            }
        }
        catch {
            Write-VaultLog "Error reading snapshot: $($_.Name)" -Level WARNING
        }
    }
    
    return $snapshots | Sort-Object CreatedAt -Descending
}

function Get-VaultSnapshot {
    <#
    .SYNOPSIS
    Retrieves and decrypts a specific snapshot from the vault
    #>
    param(
        [Parameter(Mandatory)]
        [string]$SnapshotId
    )
    
    $snapshotFile = Join-Path $script:VaultConfig.SnapshotsDir "$SnapshotId.vault"
    
    if (-not (Test-Path $snapshotFile)) {
        Write-VaultLog "Snapshot not found: $SnapshotId" -Level ERROR
        return $null
    }
    
    try {
        $vaultEntry = Get-Content $snapshotFile | ConvertFrom-Json
        $decryptedJson = Unprotect-VaultData -EncryptedText $vaultEntry.encryptedData -Scope $vaultEntry.encryptionScope
        $snapshot = $decryptedJson | ConvertFrom-Json
        
        Write-VaultLog "Successfully retrieved snapshot: $SnapshotId" -Level SUCCESS
        return $snapshot
    }
    catch {
        Write-VaultLog "Error decrypting snapshot: $_" -Level ERROR
        return $null
    }
}

# =============================================================================
# ACCESS CONTROL
# =============================================================================

function Grant-VaultAccess {
    <#
    .SYNOPSIS
    Grants access to the vault for a specific Windows user (family member)
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Username
    )
    
    Initialize-VaultStructure | Out-Null
    
    # Update metadata
    $metadata = Get-Content $script:VaultConfig.MetadataFile | ConvertFrom-Json
    
    if ($metadata.authorizedUsers -notcontains $Username) {
        $metadata.authorizedUsers += $Username
        $metadata.lastModified = (Get-Date).ToUniversalTime().ToString("o")
        $metadata | ConvertTo-Json -Depth 10 | Out-File -FilePath $script:VaultConfig.MetadataFile -Encoding UTF8
        
        # Grant folder permissions
        try {
            $acl = Get-Acl $script:VaultConfig.VaultPath
            $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                $Username,
                "ReadAndExecute",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )
            $acl.AddAccessRule($accessRule)
            Set-Acl -Path $script:VaultConfig.VaultPath -AclObject $acl
            
            Write-VaultLog "Granted vault access to: $Username" -Level SUCCESS
        }
        catch {
            Write-VaultLog "Could not set permissions for $Username`: $_" -Level WARNING
        }
        
        # Create access log entry
        $accessEntry = @{
            action    = "GRANT_ACCESS"
            username  = $Username
            grantedBy = $env:USERNAME
            timestamp = (Get-Date).ToUniversalTime().ToString("o")
        }
        
        $accessLogFile = Join-Path $script:VaultConfig.AccessControlDir "access-log.json"
        $existingLog = if (Test-Path $accessLogFile) { Get-Content $accessLogFile | ConvertFrom-Json } else { @() }
        $existingLog += $accessEntry
        $existingLog | ConvertTo-Json -Depth 10 | Out-File -FilePath $accessLogFile -Encoding UTF8
    }
    else {
        Write-VaultLog "User already has access: $Username" -Level INFO
    }
    
    return @{
        username        = $Username
        status          = "ACCESS_GRANTED"
        authorizedUsers = $metadata.authorizedUsers
    }
}

function Revoke-VaultAccess {
    <#
    .SYNOPSIS
    Revokes vault access for a specific user
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Username
    )
    
    if ($Username -eq $env:USERNAME) {
        Write-VaultLog "Cannot revoke access for vault owner" -Level ERROR
        return
    }
    
    $metadata = Get-Content $script:VaultConfig.MetadataFile | ConvertFrom-Json
    $metadata.authorizedUsers = @($metadata.authorizedUsers | Where-Object { $_ -ne $Username })
    $metadata.lastModified = (Get-Date).ToUniversalTime().ToString("o")
    $metadata | ConvertTo-Json -Depth 10 | Out-File -FilePath $script:VaultConfig.MetadataFile -Encoding UTF8
    
    # Attempt to revoke folder permissions
    try {
        $acl = Get-Acl $script:VaultConfig.VaultPath
        $accessRules = $acl.Access | Where-Object { $_.IdentityReference -like "*$Username*" }
        foreach ($rule in $accessRules) {
            $acl.RemoveAccessRule($rule) | Out-Null
        }
        Set-Acl -Path $script:VaultConfig.VaultPath -AclObject $acl
    }
    catch {
        Write-VaultLog "Could not revoke permissions: $_" -Level WARNING
    }
    
    Write-VaultLog "Revoked vault access for: $Username" -Level SUCCESS
}

# =============================================================================
# AUTO-CAPTURE CONFIGURATION
# =============================================================================

function Enable-AutoCapture {
    <#
    .SYNOPSIS
    Configures automatic WSL network snapshot capture on WSL startup
    #>
    
    Write-VaultLog "Configuring auto-capture for WSL network snapshots..." -Level INFO
    
    # Create WSL .bashrc snippet
    $bashrcSnippet = @'
# ============================================================================
# Sovereignty Architecture - WSL Network Vault Auto-Capture
# Auto-captures network configuration on WSL startup
# ============================================================================
sovereignty_network_capture() {
    local CAPTURE_LOG="/mnt/c/Users/$USER/.sovereignty-vault/network-knowledge/logs/wsl-capture-$(date +%Y%m%d).log"
    local CAPTURE_DIR="/mnt/c/Users/$USER/.sovereignty-vault/network-knowledge/wsl-captures"
    
    # Create capture directory if needed
    mkdir -p "$CAPTURE_DIR" 2>/dev/null
    
    # Capture network snapshot
    {
        echo "=========================================="
        echo "WSL Network Capture - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "=========================================="
        echo ""
        echo "[IP ADDRESS CONFIGURATION]"
        ip addr 2>/dev/null || echo "ip addr not available"
        echo ""
        echo "[NETWORK STATISTICS]"
        netstat 2>/dev/null | head -100 || echo "netstat not available"
        echo ""
        echo "[ROUTING TABLE]"
        ip route 2>/dev/null || echo "ip route not available"
        echo ""
        echo "[DNS CONFIGURATION]"
        cat /etc/resolv.conf 2>/dev/null || echo "resolv.conf not available"
        echo ""
        echo "=========================================="
    } >> "$CAPTURE_LOG" 2>&1
    
    echo "🔒 Network snapshot captured to Sovereignty Vault"
}

# Run capture on interactive shell startup (not in scripts)
if [[ $- == *i* ]]; then
    sovereignty_network_capture
fi
'@

    # Create PowerShell auto-capture script
    $psAutoCapture = @'
# Sovereignty Architecture - WSL Network Vault Auto-Capture Launcher
# Add this to your PowerShell profile or scheduled task
# Update SCRIPT_PATH to match your installation location

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
    else {
        Write-Warning "Sovereignty vault script not found. Please set SCRIPT_PATH manually."
    }
}

# Register for WSL startup (optional - runs before WSL)
# Start-SovereigntyNetworkCapture
'@

    # Save configuration files
    $configDir = Join-Path $script:VaultConfig.VaultPath "auto-capture-config"
    New-Item -Path $configDir -ItemType Directory -Force | Out-Null
    
    $bashrcSnippet | Out-File -FilePath (Join-Path $configDir "bashrc-snippet.sh") -Encoding UTF8
    $psAutoCapture | Out-File -FilePath (Join-Path $configDir "ps-profile-snippet.ps1") -Encoding UTF8
    
    # Create Windows Task Scheduler XML - use vault path for portable script location
    $vaultScriptPath = Join-Path $script:VaultConfig.VaultPath "scripts\wsl-network-vault.ps1"
    $taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Sovereignty Architecture - Capture WSL network configuration on logon/unlock</Description>
  </RegistrationInfo>
  <Triggers>
    <SessionStateChangeTrigger>
      <Enabled>true</Enabled>
      <StateChange>SessionUnlock</StateChange>
    </SessionStateChangeTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -WindowStyle Hidden -Command "&amp; { `$vaultBase = '$($script:VaultConfig.VaultPath)'; `$script = Join-Path `$vaultBase 'auto-capture-config\ps-profile-snippet.ps1'; if (Test-Path `$script) { . `$script; Start-SovereigntyNetworkCapture } }" -Action capture</Arguments>
    </Exec>
  </Actions>
</Task>
"@
    
    $taskXml | Out-File -FilePath (Join-Path $configDir "scheduled-task.xml") -Encoding Unicode
    
    Write-VaultLog "Auto-capture configuration created" -Level SUCCESS
    Write-Host ""
    Write-Host "📋 AUTO-CAPTURE SETUP INSTRUCTIONS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. For WSL (.bashrc):" -ForegroundColor Yellow
    Write-Host "   Add the following to your ~/.bashrc in WSL:"
    Write-Host "   cat $configDir/bashrc-snippet.sh >> ~/.bashrc" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. For PowerShell Profile:" -ForegroundColor Yellow
    Write-Host "   Add the snippet from: $configDir/ps-profile-snippet.ps1"
    Write-Host "   To your profile: $PROFILE"
    Write-Host ""
    Write-Host "3. For Windows Task Scheduler:" -ForegroundColor Yellow
    Write-Host "   Import the task: $configDir/scheduled-task.xml"
    Write-Host "   Command: schtasks /create /tn 'SovereigntyNetworkCapture' /xml '$configDir\scheduled-task.xml'"
    Write-Host ""
    
    return @{
        bashrcConfig = Join-Path $configDir "bashrc-snippet.sh"
        psConfig     = Join-Path $configDir "ps-profile-snippet.ps1"
        taskConfig   = Join-Path $configDir "scheduled-task.xml"
    }
}

# =============================================================================
# STATUS AND REPORTING
# =============================================================================

function Get-VaultStatus {
    <#
    .SYNOPSIS
    Displays the current status of the Sovereignty Network Knowledge Vault
    #>
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Magenta
    Write-Host "  🔐 SOVEREIGNTY NETWORK KNOWLEDGE VAULT - STATUS              " -ForegroundColor Magenta
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Magenta
    Write-Host ""
    
    if (-not (Test-Path $script:VaultConfig.MetadataFile)) {
        Write-Host "  ⚠️  Vault not initialized" -ForegroundColor Yellow
        Write-Host "  Run: .\wsl-network-vault.ps1 -Action setup" -ForegroundColor Gray
        return
    }
    
    $metadata = Get-Content $script:VaultConfig.MetadataFile | ConvertFrom-Json
    
    Write-Host "  📍 Vault Location:    $($script:VaultConfig.VaultPath)" -ForegroundColor Cyan
    Write-Host "  📊 Version:           $($metadata.version)" -ForegroundColor Cyan
    Write-Host "  👤 Owner:             $($metadata.owner)" -ForegroundColor Cyan
    Write-Host "  🔑 Encryption:        $($metadata.encryptionMethod)" -ForegroundColor Cyan
    Write-Host "  📅 Created:           $($metadata.created)" -ForegroundColor Cyan
    Write-Host "  📅 Last Modified:     $($metadata.lastModified)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  📸 Snapshots Stored:  $($metadata.snapshotCount)" -ForegroundColor Green
    Write-Host ""
    Write-Host "  👥 Authorized Users:" -ForegroundColor Yellow
    foreach ($user in $metadata.authorizedUsers) {
        Write-Host "      • $user" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "  💡 Purpose:" -ForegroundColor Yellow
    Write-Host "      $($metadata.purpose)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Magenta
    Write-Host ""
    
    return $metadata
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

switch ($Action.ToLower()) {
    "setup" {
        Initialize-VaultStructure
        Get-VaultStatus
    }
    
    "capture" {
        $result = Save-NetworkSnapshot
        Write-Host ""
        Write-Host "📸 SNAPSHOT CAPTURED" -ForegroundColor Green
        Write-Host "   ID:       $($result.snapshotId)" -ForegroundColor Cyan
        Write-Host "   File:     $($result.vaultFile)" -ForegroundColor Gray
        Write-Host "   Checksum: $($result.checksumSHA256)" -ForegroundColor Gray
        Write-Host ""
    }
    
    "store" {
        # Alias for capture
        $result = Save-NetworkSnapshot
        Write-Host ""
        Write-Host "📸 SNAPSHOT STORED" -ForegroundColor Green
        Write-Host "   ID:       $($result.snapshotId)" -ForegroundColor Cyan
        Write-Host "   File:     $($result.vaultFile)" -ForegroundColor Gray
        Write-Host ""
    }
    
    "list" {
        $snapshots = Get-VaultSnapshots
        Write-Host ""
        Write-Host "📋 VAULT SNAPSHOTS" -ForegroundColor Cyan
        Write-Host ""
        if ($snapshots) {
            $snapshots | Format-Table -AutoSize
        }
        else {
            Write-Host "   No snapshots found. Run with -Action capture to create one." -ForegroundColor Gray
        }
        Write-Host ""
    }
    
    "retrieve" {
        if (-not $SnapshotId) {
            Write-VaultLog "SnapshotId required. Use -SnapshotId parameter." -Level ERROR
            $snapshots = Get-VaultSnapshots
            Write-Host "Available snapshots:" -ForegroundColor Yellow
            $snapshots | Format-Table -AutoSize
        }
        else {
            $snapshot = Get-VaultSnapshot -SnapshotId $SnapshotId
            if ($snapshot) {
                Write-Host ""
                Write-Host "📦 SNAPSHOT DATA" -ForegroundColor Cyan
                Write-Host ""
                $snapshot | ConvertTo-Json -Depth 10
            }
        }
    }
    
    "grant-access" {
        if (-not $Username) {
            Write-VaultLog "Username required. Use -Username parameter." -Level ERROR
        }
        else {
            Grant-VaultAccess -Username $Username
        }
    }
    
    "revoke-access" {
        if (-not $Username) {
            Write-VaultLog "Username required. Use -Username parameter." -Level ERROR
        }
        else {
            Revoke-VaultAccess -Username $Username
        }
    }
    
    "auto-capture" {
        Enable-AutoCapture
    }
    
    "status" {
        Get-VaultStatus
    }
    
    default {
        Write-Host @"

🔐 WSL Network Vault - Sovereignty Architecture
   Encrypted Knowledge Storage for Family Access

USAGE:
    .\wsl-network-vault.ps1 -Action <action> [options]

ACTIONS:
    setup           Initialize the encrypted vault structure
    capture         Capture and encrypt a new WSL network snapshot
    store           Alias for capture
    list            List all stored snapshots
    retrieve        Decrypt and display a specific snapshot
    grant-access    Grant vault access to a family member
    revoke-access   Revoke vault access from a user
    auto-capture    Configure automatic capture on WSL startup
    status          Display vault status and statistics

OPTIONS:
    -VaultPath      Custom vault location (default: ~\.sovereignty-vault\network-knowledge)
    -Username       Username for access control operations
    -SnapshotId     Snapshot ID for retrieval
    -Force          Force operation (e.g., reinitialize)

EXAMPLES:
    .\wsl-network-vault.ps1 -Action setup
    .\wsl-network-vault.ps1 -Action capture
    .\wsl-network-vault.ps1 -Action list
    .\wsl-network-vault.ps1 -Action retrieve -SnapshotId snapshot_20241201_143022
    .\wsl-network-vault.ps1 -Action grant-access -Username "MyChild"
    .\wsl-network-vault.ps1 -Action auto-capture

"@
    }
}
