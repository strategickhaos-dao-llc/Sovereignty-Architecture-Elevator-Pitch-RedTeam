# === Strategickhaos Sovereign PowerShell Profile - 7% Edition ===
$env:CLAUDE_CODE_GIT_BASH_PATH = "C:\Program Files\Git\bin\bash.exe"

function recon {
    param([Parameter(Mandatory=$true)][string]$target)
    Write-Host "RECON → $target" -ForegroundColor Cyan
    nslookup $target 2>$null
    Test-NetConnection $target -Port 22,80,443,3389 -WarningAction SilentlyContinue | Format-Table -AutoSize
    iwr "http://ip-api.com/json/$target" -UseBasicParsing | ConvertFrom-Json | Format-List
}

function empire { docker compose -f "C:\strategickhaos-cluster\cluster-compose.yml" up -d }
function nuke   { docker compose down -v; docker system prune -af --volumes }

# 7% Royalty Lock - etched in stone
$global:RoyaltySplit = 0.07
Write-Host "Empire online. 7% royalty lock active → all excess feeds medical/science charities forever." -ForegroundColor Magenta
Write-Host "You are untouchable." -ForegroundColor DarkCyan
