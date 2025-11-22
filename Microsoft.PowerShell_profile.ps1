# === Strategickhaos Sovereign PowerShell Profile - 7% Edition ===
$env:CLAUDE_CODE_GIT_BASH_PATH = "C:\Program Files\Git\bin\bash.exe"

function recon {
    param([Parameter(Mandatory=$true)][string]$target)
    Write-Host "RECON → $target" -ForegroundColor Cyan
    
    # DNS Lookup
    Resolve-DnsName $target -ErrorAction SilentlyContinue | Format-Table -AutoSize
    
    # Port Scanning
    $ports = @(22, 80, 443, 3389)
    foreach ($port in $ports) {
        Test-NetConnection $target -Port $port -WarningAction SilentlyContinue | 
            Select-Object ComputerName, RemotePort, TcpTestSucceeded | 
            Format-Table -AutoSize
    }
    
    # Geolocation
    try {
        iwr "https://ip-api.com/json/$target" -UseBasicParsing -TimeoutSec 5 | 
            ConvertFrom-Json | Format-List
    }
    catch {
        Write-Host "Geolocation lookup failed: $_" -ForegroundColor Yellow
    }
}

function empire { docker compose -f "C:\strategickhaos-cluster\cluster-compose.yml" up -d }
function nuke   { docker compose down -v; docker system prune -af --volumes }

# 7% Royalty Lock - etched in stone
$global:RoyaltySplit = 0.07
Write-Host "Empire online. 7% royalty lock active → all excess feeds medical/science charities forever." -ForegroundColor Magenta
Write-Host "You are untouchable." -ForegroundColor DarkCyan
