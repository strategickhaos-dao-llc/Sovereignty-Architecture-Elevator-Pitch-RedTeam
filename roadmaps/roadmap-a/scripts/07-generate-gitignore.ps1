#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Generate comprehensive .gitignore file
.DESCRIPTION
    Creates a .gitignore file covering Python, Node, Docker, and OS-specific files
    tailored to the Sovereignty Architecture project.
.PARAMETER Force
    Overwrite existing .gitignore
#>

param(
    [switch]$Force
)

$gitignorePath = ".gitignore"

if ((Test-Path $gitignorePath) -and -not $Force) {
    Write-Host "⚠ .gitignore already exists. Use -Force to overwrite." -ForegroundColor Yellow
    Write-Host "Current file: $gitignorePath" -ForegroundColor Gray
    exit 0
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  GENERATE .gitignore - Roadmap A" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$gitignoreContent = @"
# ═══════════════════════════════════════════════════════════
# Sovereignty Architecture - Generated .gitignore
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ═══════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────
# Python
# ───────────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.mypy_cache/
.dmypy.json
dmypy.json
.coverage
.coverage.*
htmlcov/
*.cover
*.log
.pytype/

# ───────────────────────────────────────────────────────────
# JavaScript / Node.js
# ───────────────────────────────────────────────────────────
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.npm
.eslintcache
.node_repl_history
*.tgz
.yarn-integrity
.next/
.nuxt/
dist/
.cache/
.parcel-cache/
out/
.vuepress/dist
*.tsbuildinfo

# ───────────────────────────────────────────────────────────
# Environment & Secrets
# ───────────────────────────────────────────────────────────
.env
.env.local
.env.*.local
.env.development.local
.env.test.local
.env.production.local
*.pem
*.key
*.crt
secrets/
.secrets/

# ───────────────────────────────────────────────────────────
# Docker
# ───────────────────────────────────────────────────────────
.dockerignore
docker-compose.override.yml

# ───────────────────────────────────────────────────────────
# IDEs
# ───────────────────────────────────────────────────────────
.vscode/settings.json
.vscode/launch.json
.idea/
*.swp
*.swo
*~
.project
.classpath
.c9/
*.launch
.settings/
*.sublime-workspace
.history/

# ───────────────────────────────────────────────────────────
# OS
# ───────────────────────────────────────────────────────────
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini

# ───────────────────────────────────────────────────────────
# Temporary Files
# ───────────────────────────────────────────────────────────
tmp/
temp/
*.tmp
*.bak
*.swp
*.log
*.pid

# ───────────────────────────────────────────────────────────
# Build Artifacts
# ───────────────────────────────────────────────────────────
*.o
*.a
*.so
*.dylib
*.exe
*.dll
*.class

# ───────────────────────────────────────────────────────────
# Sovereignty Architecture Specific
# ───────────────────────────────────────────────────────────
mastery_results/
moc_trial_results/
benchmarks/results/
*.db
*.sqlite
*.sqlite3
recon/repos/*/
!recon/repos/.gitkeep

# ───────────────────────────────────────────────────────────
# RAG / Vector Stores
# ───────────────────────────────────────────────────────────
*.faiss
*.index
embeddings/
vector-store/

# ───────────────────────────────────────────────────────────
# Kubernetes
# ───────────────────────────────────────────────────────────
kubeconfig
*.kubeconfig

# ───────────────────────────────────────────────────────────
# Keep Important Files
# ───────────────────────────────────────────────────────────
!.gitkeep
!.env.example
!README.md
"@

# Write .gitignore
$gitignoreContent | Set-Content $gitignorePath -Encoding UTF8

Write-Host "✓ .gitignore generated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "File created: $gitignorePath" -ForegroundColor Cyan
Write-Host "Lines: $(($gitignoreContent -split "`n").Count)" -ForegroundColor Gray
Write-Host ""

# Show what will be newly ignored
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "Checking for files that will now be ignored..." -ForegroundColor Yellow
    Write-Host ""
    
    $ignored = git ls-files -i --exclude-standard 2>$null
    if ($ignored) {
        Write-Host "Files that will be ignored:" -ForegroundColor Red
        $ignored | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
        Write-Host ""
        Write-Host "To remove these from git:" -ForegroundColor Yellow
        Write-Host "  git rm --cached <file>" -ForegroundColor Gray
    } else {
        Write-Host "No new files will be ignored." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the .gitignore file" -ForegroundColor Gray
Write-Host "  2. Commit it: git add .gitignore && git commit -m 'Add .gitignore'" -ForegroundColor Gray
Write-Host "  3. Clean up ignored files: ./scripts/02-clean-artifacts.ps1" -ForegroundColor Gray
Write-Host ""
