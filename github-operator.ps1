<#
╔══════════════════════════════════════════════════════════════╗
║   GITHUB OPERATOR v1.1 — PROFILE FORGE FOR STRATEGICKHAOS    ║
║     "From 6 repos to DAO signal. One commit at a time."      ║
╚══════════════════════════════════════════════════════════════╝
#>

param(
    [switch]$forge,     # Full profile upgrade: bio + README
    [switch]$status,    # Scan GitHub state
    [switch]$manifesto  # Generate + commit README manifesto in this repo
)

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$G = 'Green'; $R = 'Red'; $C = 'Cyan'; $Y = 'Yellow'

function Log { param([string]$m, [string]$c='Gray') Write-Host "[$(Get-Date -f 'HH:mm:ss')] $m" -ForegroundColor $c }
function Log-Success { param([string]$m) Log $m $G }
function Log-Error { param([string]$m) Log "ERROR → $m" $R }

# Ensure we're inside a git repo
try {
    $inRepo = git rev-parse --is-inside-work-tree 2>$null
} catch { $inRepo = $null }

if (-not $inRepo) {
    Log-Error "Not inside a git repository. cd into a repo first."
    exit 1
}

# Get authed GitHub user
$who = gh api user --jq '.login' 2>$null
if (-not $who) {
    Log-Error "GitHub CLI not authed. Run: gh auth login"
    exit 1
}

if ($status) {
    Log "Scanning GitHub account: $who" $C
    gh api user --jq '.login, .public_repos, .bio' | ForEach-Object { Log $_ $Y }
    Log "Recent repositories:" $C
    gh repo list $who --limit 10 --json name,description | ConvertFrom-Json |
        ForEach-Object { Log ("- {0}: {1}" -f $_.name, ($_.description ?? "")) $C }
    exit 0
}

if ($manifesto) {
    $manifestoPath = Join-Path $ROOT "README.md"

@"
# StrategicKhaos DAO LLC ⚔️

**Wyoming DAO LLC §17-31-101 | EIN 39-2900295**

AI-governed perpetual philanthropy: code-enforced benevolence at planetary scale.

## Mission

- **Core Engine**: Sovereign AI swarm with irrevocable 7% allocation to:
  - St. Jude Children's Research Hospital
  - Doctors Without Borders
  - Veteran Debt Relief initiatives
  - Ethical hacker education
  - Rare disease research

- **Status**: Active, EIN-issued, treasury online. Research mode only — no public fundraising, no financial advice.

## This Repository

This vault is part of the StrategicKhaos sovereignty stack:
- Cryptographically signed manifests (GPG)
- GitHub-notarized commits
- Optional Bitcoin timestamp proofs (OpenTimestamps)

## Other Work

- GPT_Vim_DevHub — AI + Vim development lab
- Sk-thetaBXpi-AI — terminal-native AI orchestration
- More: k8s swarms, Ollama operators, nonprofit automation frameworks.

**Code-woven. Legally grounded. Sovereign on purpose.**  
"Code is law. Love is protocol."
"@ | Out-File -FilePath $manifestoPath -Encoding utf8

    Log "README.md written at $manifestoPath" $Y

    git add README.md
    git commit -m "Forge README: StrategicKhaos DAO manifesto v1.0" 2>$null
    git push 2>$null

    Log-Success "Manifesto committed and pushed for repo $(Split-Path $ROOT -Leaf)."
    Log "If this is your profile repo (e.g. $who/$who), GitHub will show it on your profile automatically." $C
    exit 0
}

if ($forge) {
    Log "Forging GitHub profile for $who..." $Y

    # 1) Update bio
    $bio = "StrategicKhaos DAO LLC · Wyoming §17-31-101 · EIN 39-2900295 · AI-governed perpetual philanthropy. Code is law. Love is protocol. ⚔️"
    gh api user -X PATCH -f bio="$bio" 1>$null 2>$null
    Log-Success "Bio updated."

    # 2) Drop manifesto in current repo
    & $PSCommandPath -manifesto

    Log "Next (manual but fast):" $C
    Log "- Go to https://github.com/$who" $C
    Log "- Click "Customize your pins" → pin this repo + your compliance vault." $C
    Log-Success "Forge complete. Refresh your GitHub profile to see the glow-up."
    exit 0
}

# Default: status scan
& $PSCommandPath -status
