<#
.SYNOPSIS
    Network and Webhook Diagnostic Script for Strategickhaos Sovereignty Architecture

.DESCRIPTION
    Performs comprehensive network diagnostics including:
    - Public IP detection
    - DNS resolution for critical services
    - Local webhook listener status
    - smee client process detection
    - HMAC signature computation
    - Outbound HTTPS connectivity
    - Network interface metrics

.EXAMPLE
    .\network-diagnostic.ps1
    
.EXAMPLE
    .\network-diagnostic.ps1 -WebhookPort 3001 -SmeeUrl "https://smee.io/your-channel"

.NOTES
    Author: Strategickhaos DAO LLC
    Requires: PowerShell 5.1 or higher
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [int]$WebhookPort = 3000,
    
    [Parameter(Mandatory=$false)]
    [string]$SmeeUrl = "",
    
    [Parameter(Mandatory=$false)]
    [string]$TestPayload = '{"action":"test"}',
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipHmac
)

$ErrorActionPreference = "Continue"
$script:FailedChecks = 0
$script:PassedChecks = 0

function Write-CheckResult {
    param(
        [string]$CheckName,
        [bool]$Passed,
        [string]$Details = ""
    )
    
    if ($Passed) {
        Write-Host "  [PASS] " -ForegroundColor Green -NoNewline
        $script:PassedChecks++
    } else {
        Write-Host "  [FAIL] " -ForegroundColor Red -NoNewline
        $script:FailedChecks++
    }
    Write-Host "$CheckName" -NoNewline
    if ($Details) {
        Write-Host " - $Details" -ForegroundColor Gray
    } else {
        Write-Host ""
    }
}

function Write-SectionHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "=== $Title ===" -ForegroundColor Cyan
}

# Header
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║   Strategickhaos Network & Webhook Diagnostic                  ║" -ForegroundColor Yellow
Write-Host "║   Sovereignty Architecture Control Plane                       ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Computer: $env:COMPUTERNAME"
Write-Host ""

# 1. Public IP
Write-SectionHeader "1) Public IP Detection"
try {
    $pubip = (Invoke-WebRequest -Uri "https://ifconfig.io/ip" -UseBasicParsing -TimeoutSec 10).Content.Trim()
    Write-Host "  Public IP: $pubip" -ForegroundColor Green
    
    # Reverse DNS
    $reverseDns = Resolve-DnsName -Name $pubip -ErrorAction SilentlyContinue
    if ($reverseDns) {
        Write-Host "  Reverse DNS: $($reverseDns.NameHost)" -ForegroundColor Gray
    } else {
        Write-Host "  Reverse DNS: (no PTR record)" -ForegroundColor Gray
    }
    Write-CheckResult "Public IP Detection" $true $pubip
} catch {
    Write-Host "  Failed to detect public IP: $($_.Exception.Message)" -ForegroundColor Red
    Write-CheckResult "Public IP Detection" $false $_.Exception.Message
}

# 2. DNS Resolution
Write-SectionHeader "2) DNS Resolution"
$dnsTargets = @(
    "github.com",
    "api.github.com",
    "raw.githubusercontent.com",
    "smee.io"
)

foreach ($target in $dnsTargets) {
    try {
        $dns = Resolve-DnsName $target -ErrorAction Stop | Where-Object { $_.IPAddress }
        if ($dns) {
            $ips = ($dns | Select-Object -ExpandProperty IPAddress -First 2) -join ", "
            Write-CheckResult "DNS: $target" $true $ips
        } else {
            Write-CheckResult "DNS: $target" $false "No A/AAAA records"
        }
    } catch {
        Write-CheckResult "DNS: $target" $false $_.Exception.Message
    }
}

# 3. Local Webhook Listener
Write-SectionHeader "3) Local Webhook Listener (Port $WebhookPort)"
try {
    $tcpTest = Test-NetConnection -ComputerName localhost -Port $WebhookPort -WarningAction SilentlyContinue
    if ($tcpTest.TcpTestSucceeded) {
        Write-CheckResult "TCP Connect localhost:$WebhookPort" $true "Listener active"
    } else {
        Write-CheckResult "TCP Connect localhost:$WebhookPort" $false "No listener on port $WebhookPort"
        Write-Host ""
        Write-Host "  SUGGESTION: Start the event gateway:" -ForegroundColor Yellow
        Write-Host "    npm run dev" -ForegroundColor Gray
        Write-Host "  Or check if another process is using the port:" -ForegroundColor Yellow
        Write-Host "    netstat -ano | findstr :$WebhookPort" -ForegroundColor Gray
    }
} catch {
    Write-CheckResult "TCP Connect localhost:$WebhookPort" $false $_.Exception.Message
}

# 4. Node/smee Process Detection
Write-SectionHeader "4) Node.js Process Detection"
$nodeProcesses = Get-Process -Name node -ErrorAction SilentlyContinue

if ($nodeProcesses) {
    Write-CheckResult "Node.js Process" $true "$($nodeProcesses.Count) process(es) running"
    $nodeProcesses | ForEach-Object {
        Write-Host "    PID: $($_.Id), Start: $($_.StartTime), Memory: $([math]::Round($_.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor Gray
    }
} else {
    Write-CheckResult "Node.js Process" $false "No node processes found"
    Write-Host ""
    Write-Host "  SUGGESTION: Start the smee client:" -ForegroundColor Yellow
    Write-Host "    npx smee-client --url https://smee.io/YOUR_CHANNEL --target http://localhost:$WebhookPort/webhooks/github" -ForegroundColor Gray
}

# Check for smee in command line
$smeeProcesses = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | 
    Where-Object { $_.CommandLine -like "*smee*" }

if ($smeeProcesses) {
    Write-Host ""
    Write-Host "  smee client detected:" -ForegroundColor Green
    $smeeProcesses | ForEach-Object {
        Write-Host "    PID: $($_.ProcessId)" -ForegroundColor Gray
    }
}

# 5. HMAC Signature Test
if (-not $SkipHmac) {
    Write-SectionHeader "5) HMAC-SHA256 Signature Computation"
    
    # Check if webhook secret is set
    $webhookSecret = $env:GITHUB_WEBHOOK_SECRET
    if (-not $webhookSecret) {
        $webhookSecret = "test_secret_for_demo"
        Write-Host "  Using demo secret (set GITHUB_WEBHOOK_SECRET env var for real testing)" -ForegroundColor Yellow
    }
    
    try {
        $hmac = [System.Security.Cryptography.HMACSHA256]::new(
            [System.Text.Encoding]::UTF8.GetBytes($webhookSecret)
        )
        $hash = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($TestPayload))
        $signature = "sha256=" + [System.BitConverter]::ToString($hash).Replace('-','').ToLower()
        
        Write-Host "  Payload: $TestPayload" -ForegroundColor Gray
        Write-Host "  Signature: $signature" -ForegroundColor Green
        Write-CheckResult "HMAC Computation" $true
    } catch {
        Write-CheckResult "HMAC Computation" $false $_.Exception.Message
    }
}

# 6. Outbound HTTPS
Write-SectionHeader "6) Outbound HTTPS Connectivity"
$httpsTargets = @(
    @{Host = "api.github.com"; Port = 443},
    @{Host = "raw.githubusercontent.com"; Port = 443},
    @{Host = "smee.io"; Port = 443}
)

foreach ($target in $httpsTargets) {
    try {
        $tcpTest = Test-NetConnection -ComputerName $target.Host -Port $target.Port -WarningAction SilentlyContinue
        if ($tcpTest.TcpTestSucceeded) {
            $details = "via $($tcpTest.InterfaceAlias) → $($tcpTest.RemoteAddress)"
            Write-CheckResult "HTTPS: $($target.Host):$($target.Port)" $true $details
        } else {
            Write-CheckResult "HTTPS: $($target.Host):$($target.Port)" $false "Connection failed"
        }
    } catch {
        Write-CheckResult "HTTPS: $($target.Host):$($target.Port)" $false $_.Exception.Message
    }
}

# 7. Network Interface Metrics
Write-SectionHeader "7) Network Interface Metrics"
try {
    $interfaces = Get-NetIPInterface -ErrorAction Stop | 
        Where-Object { $_.InterfaceAlias -like '*Wi-Fi*' -or $_.InterfaceAlias -like '*Ethernet*' } |
        Sort-Object InterfaceMetric |
        Select-Object InterfaceAlias, InterfaceMetric, AddressFamily, ConnectionState
    
    if ($interfaces) {
        Write-Host "  (Lower metric = higher priority)" -ForegroundColor Gray
        $interfaces | ForEach-Object {
            $status = if ($_.ConnectionState -eq 'Connected') { "[Connected]" } else { "[$($_.ConnectionState)]" }
            Write-Host "    $($_.InterfaceAlias): Metric $($_.InterfaceMetric) ($($_.AddressFamily)) $status" -ForegroundColor Gray
        }
        Write-CheckResult "Interface Detection" $true "$($interfaces.Count) interfaces found"
    } else {
        Write-CheckResult "Interface Detection" $false "No Wi-Fi/Ethernet interfaces"
    }
} catch {
    Write-CheckResult "Interface Detection" $false $_.Exception.Message
}

# 8. WSL/Docker Status
Write-SectionHeader "8) WSL & Docker Status"
try {
    $wslList = wsl -l -v 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  WSL Distributions:" -ForegroundColor Gray
        $wslList | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
        Write-CheckResult "WSL" $true
    } else {
        Write-CheckResult "WSL" $false "WSL not available or not running"
    }
} catch {
    Write-CheckResult "WSL" $false "WSL not installed"
}

# Check Docker
try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-CheckResult "Docker" $true "Version $dockerVersion"
    } else {
        Write-CheckResult "Docker" $false "Docker not running"
    }
} catch {
    Write-CheckResult "Docker" $false "Docker not installed"
}

# Summary
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║   DIAGNOSTIC SUMMARY                                           ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Passed: $script:PassedChecks" -ForegroundColor Green
Write-Host "  Failed: $script:FailedChecks" -ForegroundColor $(if ($script:FailedChecks -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($script:FailedChecks -gt 0) {
    Write-Host "  NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "  1. Review failed checks above" -ForegroundColor Gray
    Write-Host "  2. See NETWORK_WEBHOOK_GUIDE.md for detailed solutions" -ForegroundColor Gray
    Write-Host "  3. Ensure event gateway is running: npm run dev" -ForegroundColor Gray
    Write-Host "  4. For development, set up smee.io webhook proxy" -ForegroundColor Gray
    Write-Host ""
    exit 1
} else {
    Write-Host "  All checks passed! System is ready for webhook processing." -ForegroundColor Green
    Write-Host ""
    exit 0
}
