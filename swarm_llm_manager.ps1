# Swarm LLM Manager v1.1
# Automated VPN port management for distributed LLM swarm coordination
# Requires: powershell-yaml module (Install-Module -Name powershell-yaml)

param(
    [string]$Action = "update"  # update|list|status
)

# Configuration
$ConfigPath = Join-Path $PSScriptRoot "swarm_llm_endpoints.yaml"
$MyHostname = $env:COMPUTERNAME.ToLower()

# Check for powershell-yaml module
if (-not (Get-Module -ListAvailable -Name powershell-yaml)) {
    Write-Host "ERROR: powershell-yaml module not found" -ForegroundColor Red
    Write-Host "Install it with: Install-Module -Name powershell-yaml -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

Import-Module powershell-yaml

function Load-Yaml {
    if (-not (Test-Path $ConfigPath)) {
        Write-Host "ERROR: Configuration file not found: $ConfigPath" -ForegroundColor Red
        exit 1
    }
    
    try {
        $yamlContent = Get-Content $ConfigPath -Raw
        return ConvertFrom-Yaml $yamlContent
    } catch {
        Write-Host "ERROR: Failed to load YAML configuration: $_" -ForegroundColor Red
        exit 1
    }
}

function Save-Yaml {
    param($config)
    
    try {
        $yamlContent = ConvertTo-Yaml $config
        Set-Content -Path $ConfigPath -Value $yamlContent -Encoding UTF8
        Write-Host "Configuration saved successfully" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to save YAML configuration: $_" -ForegroundColor Red
        exit 1
    }
}

function Update-My-Endpoint {
    $config = Load-Yaml
    
    # Ensure machines section exists
    if (-not $config.machines) {
        Write-Host "ERROR: No 'machines' section found in configuration" -ForegroundColor Red
        return
    }
    
    # Check if this machine is registered
    if (-not $config.machines.$MyHostname) {
        Write-Host "ERROR: Hostname '$MyHostname' not found in configuration" -ForegroundColor Red
        Write-Host "Available machines: $($config.machines.Keys -join ', ')" -ForegroundColor Yellow
        return
    }
    
    $myEntry = $config.machines.$MyHostname

    # Step 1: Auto-detect current public (VPN) IP with fallback
    $currentIp = "OFFLINE"
    $ipServices = @(
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip"
    )
    
    foreach ($service in $ipServices) {
        try {
            $response = Invoke-WebRequest -Uri $service -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                $currentIp = $response.Content.Trim()
                break
            }
        } catch {
            continue
        }
    }

    # Step 2: If IP changed or port missing → prompt only for port
    if (-not $myEntry.proton_vpn_ip -or $myEntry.proton_vpn_ip -ne $currentIp -or -not $myEntry.forwarded_port) {
        Write-Host "`n=== Proton VPN Auto-Update for $MyHostname ===" -ForegroundColor Cyan
        Write-Host "Detected VPN IP: $currentIp" -ForegroundColor Green

        if ($currentIp -eq "OFFLINE") {
            Write-Host "No internet or not on VPN – skipping update" -ForegroundColor Yellow
            return
        }

        $port = Read-Host "Enter your current forwarded port from Proton VPN app (or press Enter to keep $($myEntry.forwarded_port))"
        if (-not $port) { $port = $myEntry.forwarded_port }

        while (-not $port -or $port -notmatch '^\d+$' -or [int]$port -lt 40000 -or [int]$port -gt 62000) {
            $port = Read-Host "Invalid port – enter the number shown in Proton VPN app (40000-62000 range)"
        }

        $myEntry.proton_vpn_ip = $currentIp
        $myEntry.forwarded_port = [int]$port
        # Both endpoints use same port - Proton VPN forwards to different local ports
        # Ollama runs on local 11434, search on local 8001
        # For separate external ports, prompt for two ports and assign separately
        $myEntry.ollama_endpoint = "http://$currentIp`:$port"
        $myEntry.search_endpoint = "http://$currentIp`:$port"

        $config.machines.$MyHostname = $myEntry
        Save-Yaml $config

        Write-Host "Locked in $MyHostname → Ollama: $($myEntry.ollama_endpoint)" -ForegroundColor Green
        if ($myEntry.search_endpoint) {
            Write-Host "Search node: $($myEntry.search_endpoint)" -ForegroundColor Green
        }
    } else {
        Write-Host "$MyHostname already locked → Ollama on port $($myEntry.forwarded_port)" -ForegroundColor Green
    }
}

function Show-Status {
    $config = Load-Yaml
    
    Write-Host "`n=== Swarm LLM Endpoints Status ===" -ForegroundColor Cyan
    Write-Host "Configuration: $ConfigPath`n" -ForegroundColor Gray
    
    foreach ($machine in $config.machines.Keys | Sort-Object) {
        $entry = $config.machines.$machine
        $isCurrent = ($machine -eq $MyHostname)
        $color = if ($isCurrent) { "Yellow" } else { "White" }
        
        Write-Host "[$machine]" -ForegroundColor $color -NoNewline
        if ($isCurrent) {
            Write-Host " (current)" -ForegroundColor Yellow
        } else {
            Write-Host ""
        }
        
        if ($entry.proton_vpn_ip) {
            Write-Host "  VPN IP: $($entry.proton_vpn_ip)" -ForegroundColor Green
            Write-Host "  Port: $($entry.forwarded_port)" -ForegroundColor Green
            Write-Host "  Ollama: $($entry.ollama_endpoint)" -ForegroundColor Cyan
            if ($entry.search_endpoint) {
                Write-Host "  Search: $($entry.search_endpoint)" -ForegroundColor Cyan
            }
        } else {
            Write-Host "  Status: Not configured" -ForegroundColor Gray
        }
        Write-Host ""
    }
}

function Show-Help {
    Write-Host @"
Swarm LLM Manager v1.1 - VPN Port Management

USAGE:
    .\swarm_llm_manager.ps1 [action]

ACTIONS:
    update    - Update current machine's VPN endpoint (default)
    status    - Show all machines in the swarm
    list      - Same as status
    help      - Show this help message

EXAMPLES:
    .\swarm_llm_manager.ps1 update
    .\swarm_llm_manager.ps1 status

REQUIREMENTS:
    - powershell-yaml module
    - Proton VPN connection with port forwarding enabled
    - Internet access to detect public IP

TIPS:
    1. Connect to a Proton VPN P2P server for best stability
    2. Enable Kill Switch and Auto-connect in Proton VPN app
    3. Never click "Regenerate port" unless necessary
    4. On reboot, script auto-detects IP and confirms port

"@ -ForegroundColor White
}

# Main execution
switch ($Action.ToLower()) {
    "update" {
        Update-My-Endpoint
    }
    "status" {
        Show-Status
    }
    "list" {
        Show-Status
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Write-Host "Use 'help' to see available actions" -ForegroundColor Yellow
        Show-Help
    }
}
