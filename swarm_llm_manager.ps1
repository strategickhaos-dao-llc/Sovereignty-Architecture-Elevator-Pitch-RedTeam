# swarm_llm_manager.ps1 - Swarm LLM and Privacy Search Manager
# Strategic Khaos Distributed AI Swarm Management

param(
    [string]$ConfigPath = ".\swarm_llm_endpoints.yaml"
)

# Color definitions for PowerShell
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-ColorText "[$timestamp] $Message" -Color Cyan
}

function Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

function Error {
    param([string]$Message)
    Write-ColorText "[ERROR] $Message" -Color Red
}

# Load YAML configuration
function Load-Yaml {
    if (-not (Test-Path $ConfigPath)) {
        Error "Configuration file not found: $ConfigPath"
        exit 1
    }
    
    # Simple YAML parser for our specific structure
    $content = Get-Content $ConfigPath -Raw
    $config = @{
        swarm = @{}
        machines = @{}
    }
    
    $currentSection = $null
    $currentMachine = $null
    
    foreach ($line in ($content -split "`n")) {
        $line = $line.Trim()
        
        if ($line -match '^swarm:') {
            $currentSection = 'swarm'
            $currentMachine = $null
        }
        elseif ($line -match '^machines:') {
            $currentSection = 'machines'
            $currentMachine = $null
        }
        elseif ($currentSection -eq 'swarm' -and $line -match '^\s*(\w+):\s*["\']?([^"\']+)["\']?') {
            $config.swarm[$matches[1]] = $matches[2]
        }
        elseif ($currentSection -eq 'machines' -and $line -match '^\s*(\w+):$') {
            $currentMachine = $matches[1]
            $config.machines[$currentMachine] = @{}
        }
        elseif ($currentMachine -and $line -match '^\s*(\w+):\s*(.*)$') {
            $key = $matches[1]
            $value = $matches[2].Trim()
            
            if ($value -eq 'null' -or $value -eq '') {
                $config.machines[$currentMachine][$key] = $null
            }
            elseif ($value -match '^["\'](.+)["\']$') {
                $config.machines[$currentMachine][$key] = $matches[1]
            }
            elseif ($value -match '^\d+$') {
                $config.machines[$currentMachine][$key] = [int]$value
            }
            else {
                $config.machines[$currentMachine][$key] = $value
            }
        }
    }
    
    return $config
}

# Save YAML configuration
function Save-Yaml {
    param($Config)
    
    $yaml = "# swarm_llm_endpoints.yaml - Swarm LLM and Privacy Search Configuration`n"
    $yaml += "swarm:`n"
    foreach ($key in $Config.swarm.Keys) {
        $value = $Config.swarm[$key]
        if ($value -match '^\d+$') {
            $yaml += "  $key: $value`n"
        }
        else {
            $yaml += "  $key: `"$value`"`n"
        }
    }
    
    $yaml += "`nmachines:`n"
    foreach ($machine in $Config.machines.Keys) {
        $yaml += "  $machine`:`n"
        foreach ($key in $Config.machines[$machine].Keys) {
            $value = $Config.machines[$machine][$key]
            if ($null -eq $value) {
                $yaml += "    $key`: null`n"
            }
            elseif ($value -match '^\d+$') {
                $yaml += "    $key`: $value`n"
            }
            else {
                $yaml += "    $key`: `"$value`"`n"
            }
        }
        $yaml += "`n"
    }
    
    $yaml | Out-File -FilePath $ConfigPath -Encoding UTF8 -NoNewline
    Success "Configuration saved to $ConfigPath"
}

# Get current hostname
function Get-MyHostname {
    $hostname = $env:COMPUTERNAME.ToLower()
    # Try to match with machines in config
    $config = Load-Yaml
    foreach ($machine in $config.machines.Keys) {
        if ($hostname -like "*$machine*" -or $machine -like "*$hostname*") {
            return $machine
        }
    }
    return $hostname
}

# Update my endpoint configuration
function Update-My-Endpoint {
    $config = Load-Yaml
    $myHostname = Get-MyHostname
    
    if (-not $config.machines.ContainsKey($myHostname)) {
        Error "Machine '$myHostname' not found in configuration"
        Write-Host "Available machines:"
        $config.machines.Keys | ForEach-Object { Write-Host "  - $_" }
        exit 1
    }
    
    $myEntry = $config.machines[$myHostname]

    if (-not $myEntry.proton_vpn_ip) {
        Write-Host "`n=== Proton VPN Update Required for $myHostname ===" -ForegroundColor Cyan
        $ip = Read-Host "Enter current Proton VPN public IP"
        $ollama_port = Read-Host "Enter forwarded port for Ollama (default 11434 or your range)"
        $search_port = Read-Host "Enter forwarded port for Privacy Search node (e.g. 8001)"

        $myEntry.proton_vpn_ip = $ip.Trim()
        $myEntry.ollama_port = if ($ollama_port) { [int]$ollama_port } else { 11434 }
        $myEntry.search_port = [int]$search_port
        # Note: Consider using HTTPS endpoints in production for enhanced security
        $myEntry.ollama_endpoint = "http://$ip`:$($myEntry.ollama_port)"
        $myEntry.search_endpoint = "http://$ip`:$($myEntry.search_port)"

        $config.machines[$myHostname] = $myEntry
        Save-Yaml $config
        Write-Host "Fully updated $myHostname"
        Write-Host "   LLM: $($myEntry.ollama_endpoint)"
        Write-Host "   Search: $($myEntry.search_endpoint)"
    }
    else {
        Success "Machine $myHostname already configured"
        Write-Host "   LLM: $($myEntry.ollama_endpoint)"
        Write-Host "   Search: $($myEntry.search_endpoint)"
    }
}

# List all endpoints
function Show-All-Endpoints {
    $config = Load-Yaml
    
    Write-Host "`n=== Swarm Configuration ===" -ForegroundColor Yellow
    Write-Host "VPN Port Range: $($config.swarm.proton_vpn_port_forward_range)"
    Write-Host "Ollama Default Port: $($config.swarm.ollama_default_port)"
    Write-Host "Search Default Port: $($config.swarm.search_default_port)"
    
    Write-Host "`n=== Machine Endpoints ===" -ForegroundColor Yellow
    foreach ($machine in $config.machines.Keys) {
        $m = $config.machines[$machine]
        Write-Host "`n$machine`:" -ForegroundColor Cyan
        Write-Host "  Hostname: $($m.hostname)"
        Write-Host "  Local IP: $($m.local_ip)"
        Write-Host "  VPN IP: $($m.proton_vpn_ip)"
        Write-Host "  Ollama Port: $($m.ollama_port)"
        Write-Host "  Search Port: $($m.search_port)"
        Write-Host "  Ollama Endpoint: $($m.ollama_endpoint)"
        Write-Host "  Search Endpoint: $($m.search_endpoint)"
    }
}

# Prompt random LLM
function Prompt-Random-LLM {
    $config = Load-Yaml
    $availableMachines = @()
    
    foreach ($machine in $config.machines.Keys) {
        if ($config.machines[$machine].ollama_endpoint) {
            $availableMachines += $machine
        }
    }
    
    if ($availableMachines.Count -eq 0) {
        Error "No configured LLM endpoints available"
        return
    }
    
    $selectedMachine = Get-Random -InputObject $availableMachines
    $endpoint = $config.machines[$selectedMachine].ollama_endpoint
    
    Write-Host "Selected machine: $selectedMachine" -ForegroundColor Green
    Write-Host "Endpoint: $endpoint" -ForegroundColor Cyan
    
    $prompt = Read-Host "`nEnter your prompt"
    $model = Read-Host "Enter model name (default: llama2)"
    if (-not $model) { $model = "llama2" }
    
    $body = @{
        model = $model
        prompt = $prompt
        stream = $false
    } | ConvertTo-Json
    
    try {
        Log "Sending request to $endpoint..."
        $response = Invoke-RestMethod -Uri "$endpoint/api/generate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 120
        Write-Host "`nResponse:" -ForegroundColor Green
        Write-Host $response.response
    }
    catch {
        Error "Failed to connect to LLM: $_"
    }
}

# Search DuckDuckGo via random swarm node
function Search-Via-Swarm {
    $config = Load-Yaml
    $availableMachines = @()
    
    foreach ($machine in $config.machines.Keys) {
        if ($config.machines[$machine].search_endpoint) {
            $availableMachines += $machine
        }
    }
    
    if ($availableMachines.Count -eq 0) {
        Error "No configured search endpoints available"
        return
    }
    
    $selectedMachine = Get-Random -InputObject $availableMachines
    $endpoint = $config.machines[$selectedMachine].search_endpoint
    
    Write-Host "Selected machine: $selectedMachine" -ForegroundColor Green
    Write-Host "Endpoint: $endpoint" -ForegroundColor Cyan
    
    $query = Read-Host "`nEnter search query"
    $maxResults = Read-Host "Max results (default: 10)"
    if (-not $maxResults) { $maxResults = 10 }
    
    $url = "$endpoint/search?q=$([uri]::EscapeDataString($query))&max_results=$maxResults"
    
    try {
        Log "Searching via $selectedMachine..."
        $response = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 30
        Write-Host "`nSearch Results for: $($response.query)" -ForegroundColor Green
        Write-Host "Found $($response.results.Count) results`n" -ForegroundColor Cyan
        
        $i = 1
        foreach ($result in $response.results) {
            Write-Host "$i. $($result.title)" -ForegroundColor Yellow
            Write-Host "   URL: $($result.href)" -ForegroundColor Gray
            Write-Host "   $($result.body)" -ForegroundColor White
            Write-Host ""
            $i++
        }
    }
    catch {
        Error "Failed to search: $_"
    }
}

# Browse URL via random swarm node
function Browse-Via-Swarm {
    $config = Load-Yaml
    $availableMachines = @()
    
    foreach ($machine in $config.machines.Keys) {
        if ($config.machines[$machine].search_endpoint) {
            $availableMachines += $machine
        }
    }
    
    if ($availableMachines.Count -eq 0) {
        Error "No configured search endpoints available"
        return
    }
    
    $selectedMachine = Get-Random -InputObject $availableMachines
    $endpoint = $config.machines[$selectedMachine].search_endpoint
    
    Write-Host "Selected machine: $selectedMachine" -ForegroundColor Green
    Write-Host "Endpoint: $endpoint" -ForegroundColor Cyan
    
    $targetUrl = Read-Host "`nEnter URL to browse"
    
    $url = "$endpoint/browse?url=$([uri]::EscapeDataString($targetUrl))"
    
    try {
        Log "Fetching page via $selectedMachine..."
        $response = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 60
        Write-Host "`nPage Retrieved:" -ForegroundColor Green
        Write-Host "URL: $($response.url)" -ForegroundColor Cyan
        Write-Host "Title: $($response.title)" -ForegroundColor Yellow
        Write-Host "`nContent Preview:" -ForegroundColor White
        Write-Host $response.text_preview
    }
    catch {
        Error "Failed to browse: $_"
    }
}

# Check health of all nodes
function Check-All-Health {
    $config = Load-Yaml
    
    Write-Host "`n=== Health Check ===" -ForegroundColor Yellow
    
    foreach ($machine in $config.machines.Keys) {
        $m = $config.machines[$machine]
        Write-Host "`n$machine`:" -ForegroundColor Cyan
        
        # Check search endpoint
        if ($m.search_endpoint) {
            try {
                $response = Invoke-RestMethod -Uri "$($m.search_endpoint)/health" -Method Get -TimeoutSec 10
                Success "  Search Node: Healthy (Exit IP: $($response.exit_ip))"
            }
            catch {
                Error "  Search Node: Unhealthy or unreachable"
            }
        }
        else {
            Write-Host "  Search Node: Not configured" -ForegroundColor Gray
        }
        
        # Check Ollama endpoint
        if ($m.ollama_endpoint) {
            try {
                $response = Invoke-RestMethod -Uri "$($m.ollama_endpoint)/api/tags" -Method Get -TimeoutSec 10
                Success "  Ollama: Healthy ($($response.models.Count) models available)"
            }
            catch {
                Error "  Ollama: Unhealthy or unreachable"
            }
        }
        else {
            Write-Host "  Ollama: Not configured" -ForegroundColor Gray
        }
    }
}

# Show menu and handle user input
function Show-Menu {
    while ($true) {
        Write-Host "`n========================================" -ForegroundColor Magenta
        Write-Host "  Strategic Khaos Swarm Manager" -ForegroundColor Magenta
        Write-Host "========================================" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "1) Update my machine's endpoint configuration"
        Write-Host "2) Show all endpoints"
        Write-Host "3) Prompt random LLM"
        Write-Host "4) Search DuckDuckGo via random swarm node"
        Write-Host "5) Browse URL via random swarm node"
        Write-Host "6) Check health of all nodes"
        Write-Host "7) Exit"
        Write-Host ""
        
        $choice = Read-Host "Select an option (1-7)"
        
        switch ($choice) {
            "1" { Update-My-Endpoint }
            "2" { Show-All-Endpoints }
            "3" { Prompt-Random-LLM }
            "4" { Search-Via-Swarm }
            "5" { Browse-Via-Swarm }
            "6" { Check-All-Health }
            "7" { 
                Success "Exiting Swarm Manager"
                exit 0
            }
            default {
                Error "Invalid option. Please select 1-7."
            }
        }
    }
}

# Main execution
function Main {
    Write-ColorText "`n🎯 Strategic Khaos Swarm LLM & Privacy Search Manager" -Color Magenta
    Write-ColorText "   Distributed AI Intelligence Layer`n" -Color Cyan
    
    Show-Menu
}

# Execute main function
Main
