# DOM_010101 TrueNAS Mount Script
# Mounts the TrueNAS swarm-vault share on Windows as Z: drive

<#
.SYNOPSIS
    Mounts TrueNAS swarm-vault share as Z: drive
    
.DESCRIPTION
    Connects to TrueNAS Scale NAS and mounts the swarm-vault share
    as a persistent Z: drive on Windows for easy access
    
.PARAMETER Username
    SMB username (default: dom-cluster)
    
.PARAMETER NasIP
    TrueNAS IP address (default: 192.168.1.200)
    
.NOTES
    Requires: Administrator privileges
#>

[CmdletBinding()]
param(
    [string]$Username = "dom-cluster",
    [string]$NasIP = "192.168.1.200",
    [string]$ShareName = "swarm-vault",
    [string]$DriveLetter = "Z"
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 1
}

Write-Host "=== DOM_010101 TrueNAS Mount ===" -ForegroundColor Cyan
Write-Host "Mounting swarm-vault as ${DriveLetter}: drive..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Test connectivity
Write-Host "[1/5] Testing connectivity to TrueNAS..." -ForegroundColor Yellow
$connection = Test-NetConnection -ComputerName $NasIP -Port 445 -InformationLevel Quiet

if (!$connection) {
    Write-Error "Cannot reach TrueNAS at ${NasIP}:445 (SMB port)"
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Verify TrueNAS is powered on and network connected" -ForegroundColor Gray
    Write-Host "2. Check IP address is correct: $NasIP" -ForegroundColor Gray
    Write-Host "3. Verify SMB service is running in TrueNAS web UI" -ForegroundColor Gray
    Write-Host "4. Check firewall rules allow SMB (port 445)" -ForegroundColor Gray
    exit 1
}

Write-Host "✓ TrueNAS is reachable" -ForegroundColor Green

# Step 2: Add DNS entry
Write-Host "[2/5] Configuring DNS..." -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsEntry = "$NasIP    truenas.dom010101.local"

if (!(Select-String -Path $hostsPath -Pattern "truenas.dom010101.local" -Quiet)) {
    Add-Content -Path $hostsPath -Value "`n$hostsEntry"
    Write-Host "✓ Added DNS entry: $hostsEntry" -ForegroundColor Green
} else {
    Write-Host "✓ DNS entry already exists" -ForegroundColor Green
}

# Step 3: Remove existing drive if present
Write-Host "[3/5] Checking for existing ${DriveLetter}: drive..." -ForegroundColor Yellow
if (Test-Path "${DriveLetter}:") {
    try {
        Remove-PSDrive -Name $DriveLetter -Force -ErrorAction Stop
        Write-Host "✓ Removed existing ${DriveLetter}: drive" -ForegroundColor Green
    } catch {
        Write-Warning "Could not remove existing drive: $_"
    }
}

# Also remove persistent mapping if exists
net use "${DriveLetter}:" /delete 2>$null | Out-Null

# Step 4: Get credentials
Write-Host "[4/5] Getting credentials..." -ForegroundColor Yellow
Write-Host "Enter password for user '$Username' on TrueNAS:" -ForegroundColor Cyan
$credential = Get-Credential -UserName $Username -Message "Enter TrueNAS credentials"

if (!$credential) {
    Write-Error "Credentials are required"
    exit 1
}

Write-Host "✓ Credentials received" -ForegroundColor Green

# Step 5: Mount the share
Write-Host "[5/5] Mounting share..." -ForegroundColor Yellow
$uncPath = "\\$NasIP\$ShareName"

try {
    # Use net use for persistent mapping
    $password = $credential.GetNetworkCredential().Password
    $netUseCmd = "net use ${DriveLetter}: $uncPath /user:$Username `"$password`" /persistent:yes"
    
    Invoke-Expression $netUseCmd | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        throw "net use command failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "✓ Share mounted successfully" -ForegroundColor Green
    
} catch {
    Write-Error "Failed to mount share: $_"
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify username and password are correct" -ForegroundColor Gray
    Write-Host "2. Check SMB share is configured in TrueNAS" -ForegroundColor Gray
    Write-Host "3. Verify share permissions allow this user" -ForegroundColor Gray
    Write-Host "4. Try accessing manually: $uncPath" -ForegroundColor Gray
    exit 1
}

# Step 6: Verify mount
Write-Host ""
Write-Host "=== Verification ===" -ForegroundColor Cyan
if (Test-Path "${DriveLetter}:") {
    Write-Host "✓ ${DriveLetter}: drive is accessible" -ForegroundColor Green
    
    # Get drive info
    $drive = Get-PSDrive -Name $DriveLetter -ErrorAction SilentlyContinue
    if ($drive) {
        Write-Host ""
        Write-Host "Drive Information:" -ForegroundColor White
        Write-Host "  Name:        $($drive.Name)" -ForegroundColor Gray
        Write-Host "  Root:        $($drive.Root)" -ForegroundColor Gray
        Write-Host "  Description: $($drive.Description)" -ForegroundColor Gray
        
        # Get free space
        try {
            $volume = Get-Volume -DriveLetter $DriveLetter -ErrorAction SilentlyContinue
            if ($volume) {
                $freeTB = [math]::Round($volume.SizeRemaining / 1TB, 2)
                $totalTB = [math]::Round($volume.Size / 1TB, 2)
                Write-Host "  Free Space:  $freeTB TB / $totalTB TB" -ForegroundColor Gray
            }
        } catch {
            # Volume cmdlet may not work for network drives
        }
    }
    
    # Test write
    Write-Host ""
    Write-Host "Testing write access..." -ForegroundColor Yellow
    $testFile = "${DriveLetter}:\dom-mount-test.txt"
    try {
        "DOM_010101 mount test at $(Get-Date)" | Out-File -FilePath $testFile -Encoding UTF8
        if (Test-Path $testFile) {
            Write-Host "✓ Write test successful" -ForegroundColor Green
            Remove-Item $testFile -Force
        }
    } catch {
        Write-Warning "Write test failed: $_"
    }
    
} else {
    Write-Error "${DriveLetter}: drive is not accessible after mounting"
    exit 1
}

# Create directory structure
Write-Host ""
Write-Host "=== Creating Directory Structure ===" -ForegroundColor Cyan
$directories = @(
    "${DriveLetter}:\love",
    "${DriveLetter}:\dolm",
    "${DriveLetter}:\music",
    "${DriveLetter}:\logs",
    "${DriveLetter}:\backups"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Exists: $dir" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🎉 TrueNAS Mount Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access your sovereign storage at: ${DriveLetter}:\" -ForegroundColor White
Write-Host "UNC Path: $uncPath" -ForegroundColor Gray
Write-Host ""
Write-Host "The vault is open. 32 TB of power at your fingertips. 💾⚡" -ForegroundColor Magenta
