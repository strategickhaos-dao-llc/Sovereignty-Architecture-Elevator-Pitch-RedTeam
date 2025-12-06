<#
╔══════════════════════════════════════════════════════════════════════════════╗
║  FLAME LANG RECON PATCH - ONSIT_AI_Recon Integration                        ║
║  PowerShell integration layer for Flame Lang reconnaissance operations       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Part of the Strategic Khaos Sovereignty Architecture                        ║
║  Author: Domenic Garza / StrategicKhaos DAO LLC                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
#>

param(
    [Parameter(Position=0)]
    [string]$Action = "status",
    
    [Parameter()]
    [string]$NodeName = "default",
    
    [Parameter()]
    [string]$Bearer = "",
    
    [Parameter()]
    [switch]$Verbose,
    
    [Parameter()]
    [string]$ConfigPath = ""
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

$Script:FlameConfig = @{
    Version = "1.0.0"
    NodeTiers = @{
        1 = "Nova"      # Primary nodes
        2 = "Lyra"      # Secondary nodes
        3 = "Pulsar"    # Tertiary nodes
        4 = "Nebula"    # Reserve nodes
    }
    SealTypes = @("SHA256", "SHA512", "BLAKE2")
    ReconInterval = 30  # seconds
    OathChainFile = "$env:USERPROFILE\.flame\oath_chain.json"
    NodesFile = "$env:USERPROFILE\.flame\nodes.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# OATH MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

function New-FlameOath {
    <#
    .SYNOPSIS
        Creates a new sovereignty oath token.
    .DESCRIPTION
        Generates a cryptographically signed oath token for node authentication.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Bearer,
        
        [Parameter()]
        [string]$Seal = "SHA256"
    )
    
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $payload = "${Bearer}:${Seal}:${timestamp}"
    
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $hash = $sha256.ComputeHash($bytes)
    $signature = [System.BitConverter]::ToString($hash) -replace '-', ''
    
    $oath = @{
        Bearer = $Bearer
        Seal = $Seal
        Timestamp = $timestamp
        Signature = $signature.ToLower()
        CreatedAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    }
    
    return $oath
}

function Test-FlameOath {
    <#
    .SYNOPSIS
        Verifies a sovereignty oath token.
    #>
    param(
        [Parameter(Mandatory)]
        [hashtable]$Oath
    )
    
    $payload = "$($Oath.Bearer):$($Oath.Seal):$($Oath.Timestamp)"
    
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $hash = $sha256.ComputeHash($bytes)
    $expected = ([System.BitConverter]::ToString($hash) -replace '-', '').ToLower()
    
    return $Oath.Signature -eq $expected
}

function Save-OathChain {
    <#
    .SYNOPSIS
        Saves the oath chain to disk.
    #>
    param(
        [Parameter(Mandatory)]
        [array]$Chain
    )
    
    $dir = Split-Path $Script:FlameConfig.OathChainFile -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    
    $Chain | ConvertTo-Json -Depth 10 | Out-File $Script:FlameConfig.OathChainFile -Encoding UTF8
}

function Get-OathChain {
    <#
    .SYNOPSIS
        Loads the oath chain from disk.
    #>
    if (Test-Path $Script:FlameConfig.OathChainFile) {
        return Get-Content $Script:FlameConfig.OathChainFile | ConvertFrom-Json
    }
    return @()
}

# ═══════════════════════════════════════════════════════════════════════════════
# NODE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

function Get-FlameNodes {
    <#
    .SYNOPSIS
        Gets the list of registered Flame nodes.
    #>
    if (Test-Path $Script:FlameConfig.NodesFile) {
        return Get-Content $Script:FlameConfig.NodesFile | ConvertFrom-Json
    }
    return @()
}

function Register-FlameNode {
    <#
    .SYNOPSIS
        Registers a new Flame node.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Name,
        
        [Parameter()]
        [int]$Tier = 3,
        
        [Parameter()]
        [string]$Endpoint = ""
    )
    
    $nodes = @(Get-FlameNodes)
    
    $node = @{
        Name = $Name
        Tier = $Tier
        TierName = $Script:FlameConfig.NodeTiers[$Tier]
        Endpoint = $Endpoint
        Active = $true
        RegisteredAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        LastSeen = $null
    }
    
    $nodes += $node
    
    $dir = Split-Path $Script:FlameConfig.NodesFile -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    
    $nodes | ConvertTo-Json -Depth 10 | Out-File $Script:FlameConfig.NodesFile -Encoding UTF8
    
    return $node
}

function Update-FlameNodeStatus {
    <#
    .SYNOPSIS
        Updates a node's status and last seen time.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Name,
        
        [Parameter()]
        [bool]$Active = $true
    )
    
    $nodes = @(Get-FlameNodes)
    
    for ($i = 0; $i -lt $nodes.Count; $i++) {
        if ($nodes[$i].Name -eq $Name) {
            $nodes[$i].Active = $Active
            $nodes[$i].LastSeen = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        }
    }
    
    $nodes | ConvertTo-Json -Depth 10 | Out-File $Script:FlameConfig.NodesFile -Encoding UTF8
}

# ═══════════════════════════════════════════════════════════════════════════════
# RECONNAISSANCE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

function Start-FlameRecon {
    <#
    .SYNOPSIS
        Starts reconnaissance operations for the node network.
    #>
    param(
        [Parameter()]
        [int]$Interval = 30,
        
        [Parameter()]
        [switch]$Once
    )
    
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  FLAME RECON - Starting Reconnaissance                       ║
╠══════════════════════════════════════════════════════════════╣
║  Interval: $Interval seconds                                        
║  Mode: $(if ($Once) { "Single Scan" } else { "Continuous" })
╚══════════════════════════════════════════════════════════════╝
"@

    do {
        $nodes = @(Get-FlameNodes)
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        Write-Host "`n[$timestamp] Scanning $($nodes.Count) nodes..." -ForegroundColor Cyan
        
        foreach ($node in $nodes) {
            $status = if ($node.Active) { "✓ Active" } else { "✗ Inactive" }
            $color = if ($node.Active) { "Green" } else { "Red" }
            Write-Host "  $($node.TierName)::$($node.Name) - $status" -ForegroundColor $color
        }
        
        if (-not $Once) {
            Start-Sleep -Seconds $Interval
        }
    } while (-not $Once)
}

function Get-FlameStatus {
    <#
    .SYNOPSIS
        Gets the current Flame system status.
    #>
    $nodes = @(Get-FlameNodes)
    $oaths = @(Get-OathChain)
    
    $activeNodes = @($nodes | Where-Object { $_.Active }).Count
    
    @{
        Version = $Script:FlameConfig.Version
        TotalNodes = $nodes.Count
        ActiveNodes = $activeNodes
        OathChainLength = $oaths.Count
        Timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    }
}

function Invoke-FlameSeal {
    <#
    .SYNOPSIS
        Seals data with cryptographic signature.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Data,
        
        [Parameter()]
        [string]$SealType = "SHA256"
    )
    
    switch ($SealType) {
        "SHA256" {
            $algo = [System.Security.Cryptography.SHA256]::Create()
        }
        "SHA512" {
            $algo = [System.Security.Cryptography.SHA512]::Create()
        }
        default {
            $algo = [System.Security.Cryptography.SHA256]::Create()
        }
    }
    
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Data)
    $hash = $algo.ComputeHash($bytes)
    return ([System.BitConverter]::ToString($hash) -replace '-', '').ToLower()
}

# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

function Show-FlameHelp {
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  FLAME LANG RECON PATCH v$($Script:FlameConfig.Version)                            ║
║  Strategic Khaos Sovereignty Architecture                    ║
╠══════════════════════════════════════════════════════════════╣
║  USAGE:                                                      ║
║    .\flamelang_recon_patch.ps1 <action> [options]           ║
║                                                              ║
║  ACTIONS:                                                    ║
║    status    - Show current system status                    ║
║    nodes     - List registered nodes                         ║
║    register  - Register a new node (-NodeName, -Bearer)      ║
║    oath      - Create new oath token (-Bearer)               ║
║    verify    - Verify oath chain                             ║
║    recon     - Start reconnaissance                          ║
║    seal      - Seal data (pipe data | .\script.ps1 seal)     ║
║    help      - Show this help message                        ║
║                                                              ║
║  OPTIONS:                                                    ║
║    -NodeName <name>  - Node identifier                       ║
║    -Bearer <id>      - Bearer identity                       ║
║    -Verbose          - Enable verbose output                 ║
╚══════════════════════════════════════════════════════════════╝
"@
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

switch ($Action.ToLower()) {
    "status" {
        $status = Get-FlameStatus
        Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  FLAME SYSTEM STATUS                                         ║
╠══════════════════════════════════════════════════════════════╣
  Version:          $($status.Version)
  Total Nodes:      $($status.TotalNodes)
  Active Nodes:     $($status.ActiveNodes)
  Oath Chain:       $($status.OathChainLength) tokens
  Timestamp:        $($status.Timestamp)
╚══════════════════════════════════════════════════════════════╝
"@
    }
    
    "nodes" {
        $nodes = @(Get-FlameNodes)
        Write-Host "╔══════════════════════════════════════════════════════════════╗"
        Write-Host "║  REGISTERED FLAME NODES                                      ║"
        Write-Host "╠══════════════════════════════════════════════════════════════╣"
        
        if ($nodes.Count -eq 0) {
            Write-Host "  No nodes registered. Use 'register' to add nodes."
        } else {
            foreach ($node in $nodes) {
                $status = if ($node.Active) { "✓" } else { "✗" }
                Write-Host "  $status [$($node.TierName)] $($node.Name)"
            }
        }
        Write-Host "╚══════════════════════════════════════════════════════════════╝"
    }
    
    "register" {
        if (-not $NodeName -or $NodeName -eq "default") {
            Write-Host "Error: -NodeName required for registration" -ForegroundColor Red
            exit 1
        }
        
        $node = Register-FlameNode -Name $NodeName -Bearer $Bearer
        Write-Host "✓ Node '$($node.Name)' registered as $($node.TierName)" -ForegroundColor Green
    }
    
    "oath" {
        if (-not $Bearer) {
            $Bearer = $env:USERNAME
        }
        
        $oath = New-FlameOath -Bearer $Bearer
        $chain = @(Get-OathChain)
        $chain += $oath
        Save-OathChain -Chain $chain
        
        Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  NEW OATH TOKEN CREATED                                      ║
╠══════════════════════════════════════════════════════════════╣
  Bearer:     $($oath.Bearer)
  Seal:       $($oath.Seal)
  Signature:  $($oath.Signature.Substring(0, 16))...
  Created:    $($oath.CreatedAt)
╚══════════════════════════════════════════════════════════════╝
"@
    }
    
    "verify" {
        $chain = @(Get-OathChain)
        $valid = 0
        $invalid = 0
        
        Write-Host "╔══════════════════════════════════════════════════════════════╗"
        Write-Host "║  OATH CHAIN VERIFICATION                                     ║"
        Write-Host "╠══════════════════════════════════════════════════════════════╣"
        
        foreach ($oath in $chain) {
            $oathHash = @{
                Bearer = $oath.Bearer
                Seal = $oath.Seal
                Timestamp = $oath.Timestamp
                Signature = $oath.Signature
            }
            
            if (Test-FlameOath -Oath $oathHash) {
                Write-Host "  ✓ Bearer: $($oath.Bearer) - VALID" -ForegroundColor Green
                $valid++
            } else {
                Write-Host "  ✗ Bearer: $($oath.Bearer) - INVALID" -ForegroundColor Red
                $invalid++
            }
        }
        
        Write-Host "╠══════════════════════════════════════════════════════════════╣"
        Write-Host "  Total: $($chain.Count) | Valid: $valid | Invalid: $invalid"
        Write-Host "╚══════════════════════════════════════════════════════════════╝"
    }
    
    "recon" {
        Start-FlameRecon -Once
    }
    
    "seal" {
        $data = $input | Out-String
        if ($data) {
            $sealed = Invoke-FlameSeal -Data $data.Trim()
            Write-Host $sealed
        } else {
            Write-Host "Error: No data to seal. Pipe data to this command." -ForegroundColor Red
        }
    }
    
    "help" {
        Show-FlameHelp
    }
    
    default {
        Show-FlameHelp
    }
}
