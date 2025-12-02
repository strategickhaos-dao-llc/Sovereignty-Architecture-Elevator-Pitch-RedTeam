#!/usr/bin/env pwsh
<#
.SYNOPSIS
    100 Practical Verification Methods - Prove the Assessment is Accurate
.DESCRIPTION
    This script provides 100 real, practical, boringly safe, and completely legitimate
    ways to verify that the current state is "fast-learning experimental builder missing
    only the minimum scaffolding."
.NOTES
    Run this on your local 5-node cluster to validate the grounded assessment.
#>

param(
    [switch]$Verbose,
    [switch]$Summary
)

$results = @()

function Test-Assessment {
    param($Name, $Category, $TestBlock)
    
    Write-Host "Testing: $Name..." -NoNewline
    try {
        $result = & $TestBlock
        $results += [PSCustomObject]@{
            Category = $Category
            Test = $Name
            Result = $result
            Status = if ($result) { "✓ PASS" } else { "✗ FAIL" }
        }
        Write-Host " $($results[-1].Status)" -ForegroundColor $(if ($result) { "Green" } else { "Red" })
    } catch {
        Write-Host " ✗ ERROR" -ForegroundColor Red
        $results += [PSCustomObject]@{
            Category = $Category
            Test = $Name
            Result = $_.Exception.Message
            Status = "✗ ERROR"
        }
    }
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ASSESSMENT VERIFICATION - 100 PRACTICAL METHODS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# CATEGORY 1: Proof the Assessment Matches Reality (20 ways)
Write-Host "[1-20] Proving Speed & Experimentation..." -ForegroundColor Yellow

Test-Assessment "1. Recent commit activity (last month)" "Speed" {
    $commits = git log --since="1 month ago" --oneline 2>$null
    $count = ($commits | Measure-Object).Count
    Write-Host "    → $count commits" -ForegroundColor Gray
    $count -gt 10
}

Test-Assessment "2. Working departments exist" "Speed" {
    $dirs = @("refinory", "legal", "recon", "monitoring")
    $existing = $dirs | Where-Object { Test-Path $_ }
    Write-Host "    → $($existing.Count)/$($dirs.Count) departments" -ForegroundColor Gray
    $existing.Count -ge 3
}

Test-Assessment "3. Python files count (chaos metric)" "Chaos" {
    $pyFiles = Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    $count = ($pyFiles | Measure-Object).Count
    Write-Host "    → $count Python files" -ForegroundColor Gray
    $count -gt 10
}

Test-Assessment "4. Lines of code without structure" "Chaos" {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $lines = git ls-files "*.py" | ForEach-Object { (Get-Content $_ 2>$null | Measure-Object -Line).Lines } | Measure-Object -Sum
        Write-Host "    → $($lines.Sum) lines of Python" -ForegroundColor Gray
        $lines.Sum -gt 100
    } else { $false }
}

Test-Assessment "5. Docker containers defined" "Works" {
    $dockerFiles = Get-ChildItem -Filter "Dockerfile*" -ErrorAction SilentlyContinue
    $count = ($dockerFiles | Measure-Object).Count
    Write-Host "    → $count Dockerfiles" -ForegroundColor Gray
    $count -gt 0
}

Test-Assessment "6. Docker compose configurations" "Works" {
    $composeFiles = Get-ChildItem -Filter "docker-compose*.yml" -ErrorAction SilentlyContinue
    $count = ($composeFiles | Measure-Object).Count
    Write-Host "    → $count compose files" -ForegroundColor Gray
    $count -gt 0
}

Test-Assessment "7. No formal test infrastructure" "Chaos" {
    $testDirs = @("tests", "test", "__tests__")
    $hasFormalTests = $testDirs | Where-Object { Test-Path $_ } | Measure-Object | Select-Object -ExpandProperty Count
    Write-Host "    → $hasFormalTests formal test directories" -ForegroundColor Gray
    $hasFormalTests -eq 0
}

Test-Assessment "8. Scripts directory exists" "Works" {
    $hasScripts = Test-Path "scripts"
    if ($hasScripts) {
        $scriptCount = (Get-ChildItem scripts -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "    → $scriptCount scripts" -ForegroundColor Gray
    }
    $hasScripts
}

Test-Assessment "9. Configuration files present" "Works" {
    $configs = Get-ChildItem -Filter "*.yml" -ErrorAction SilentlyContinue
    $count = ($configs | Measure-Object).Count
    Write-Host "    → $count YAML configs" -ForegroundColor Gray
    $count -gt 0
}

Test-Assessment "10. Multiple markdown docs" "Speed" {
    $docs = Get-ChildItem -Filter "*.md" -ErrorAction SilentlyContinue
    $count = ($docs | Measure-Object).Count
    Write-Host "    → $count markdown files" -ForegroundColor Gray
    $count -gt 5
}

Test-Assessment "11. Bootstrap/deployment scripts" "Works" {
    $hasBootstrap = (Test-Path "bootstrap") -or ((Get-ChildItem -Filter "deploy*.sh" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
    $hasBootstrap
}

Test-Assessment "12. Multiple language polyglot" "Speed" {
    $langs = @(
        @{Ext="*.py"; Name="Python"},
        @{Ext="*.js"; Name="JavaScript"},
        @{Ext="*.ts"; Name="TypeScript"},
        @{Ext="*.sh"; Name="Shell"}
    )
    $found = $langs | Where-Object { (Get-ChildItem -Recurse -Filter $_.Ext -ErrorAction SilentlyContinue).Count -gt 0 }
    Write-Host "    → $($found.Count) languages: $($found.Name -join ', ')" -ForegroundColor Gray
    $found.Count -ge 2
}

Test-Assessment "13. Package managers present" "Works" {
    $pkgMgrs = @("package.json", "requirements*.txt", "Pipfile")
    $found = $pkgMgrs | Where-Object { Test-Path $_ }
    Write-Host "    → $($found.Count) package managers" -ForegroundColor Gray
    $found.Count -gt 0
}

Test-Assessment "14. Git history depth" "Speed" {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $commits = git rev-list --count HEAD 2>$null
        Write-Host "    → $commits total commits" -ForegroundColor Gray
        [int]$commits -gt 1
    } else { $false }
}

Test-Assessment "15. Recent file modifications" "Speed" {
    $recent = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | 
              Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
    $count = ($recent | Measure-Object).Count
    Write-Host "    → $count files modified in last week" -ForegroundColor Gray
    $count -gt 5
}

Test-Assessment "16. Shell scripts for automation" "Works" {
    $scripts = Get-ChildItem -Recurse -Filter "*.sh" -ErrorAction SilentlyContinue
    $count = ($scripts | Measure-Object).Count
    Write-Host "    → $count shell scripts" -ForegroundColor Gray
    $count -gt 3
}

Test-Assessment "17. Environment configuration" "Works" {
    $envFiles = Get-ChildItem -Filter ".env*" -ErrorAction SilentlyContinue
    $count = ($envFiles | Measure-Object).Count
    Write-Host "    → $count environment files" -ForegroundColor Gray
    $count -gt 0
}

Test-Assessment "18. Multiple sub-projects" "Speed" {
    $subProjects = Get-ChildItem -Directory -ErrorAction SilentlyContinue | 
                   Where-Object { Test-Path (Join-Path $_.FullName "*.py") -or Test-Path (Join-Path $_.FullName "*.js") }
    $count = ($subProjects | Measure-Object).Count
    Write-Host "    → $count sub-projects detected" -ForegroundColor Gray
    $count -ge 3
}

Test-Assessment "19. README documentation exists" "Works" {
    Test-Path "README.md"
}

Test-Assessment "20. GitHub Actions or CI/CD" "Works" {
    Test-Path ".github/workflows"
}

# CATEGORY 2: Distributed Infrastructure (21-40)
Write-Host ""
Write-Host "[21-40] Proving Distributed Infrastructure..." -ForegroundColor Yellow

Test-Assessment "21. Multi-node configuration hints" "Infrastructure" {
    $clusterFiles = Get-ChildItem -Recurse -Filter "*cluster*" -ErrorAction SilentlyContinue
    ($clusterFiles | Measure-Object).Count -gt 0
}

Test-Assessment "22. Kubernetes manifests" "Infrastructure" {
    $k8s = Get-ChildItem -Recurse -Filter "*k8s*" -ErrorAction SilentlyContinue
    ($k8s | Measure-Object).Count -gt 0
}

Test-Assessment "23. Service discovery configs" "Infrastructure" {
    Test-Path "discovery*.yml"
}

Test-Assessment "24. Network/VPN references" "Infrastructure" {
    $networkFiles = Get-ChildItem -Recurse -Filter "*tailscale*","*vpn*","*network*" -ErrorAction SilentlyContinue
    ($networkFiles | Measure-Object).Count -gt 0
}

Test-Assessment "25. Monitoring setup" "Infrastructure" {
    Test-Path "monitoring"
}

Test-Assessment "26. Grafana configurations" "Infrastructure" {
    $grafana = Get-ChildItem -Recurse -Filter "*grafana*" -ErrorAction SilentlyContinue
    ($grafana | Measure-Object).Count -gt 0
}

Test-Assessment "27. Prometheus configs" "Infrastructure" {
    $prom = Get-ChildItem -Recurse -Filter "*prometheus*" -ErrorAction SilentlyContinue
    ($prom | Measure-Object).Count -gt 0
}

Test-Assessment "28. Discord integration" "Infrastructure" {
    $discord = Get-ChildItem -Recurse -Filter "*discord*" -ErrorAction SilentlyContinue
    ($discord | Measure-Object).Count -gt 0
}

Test-Assessment "29. Event gateway or webhook handler" "Infrastructure" {
    $gateway = Get-ChildItem -Recurse -Filter "*gateway*","*webhook*" -ErrorAction SilentlyContinue
    ($gateway | Measure-Object).Count -gt 0
}

Test-Assessment "30. API endpoints defined" "Infrastructure" {
    $content = Get-ChildItem -Recurse -Filter "*.py","*.js","*.ts" -ErrorAction SilentlyContinue | 
               Select-Object -First 50 | Get-Content -ErrorAction SilentlyContinue | Select-String "app\." -Quiet
    $content
}

Test-Assessment "31. Database configurations" "Infrastructure" {
    $dbs = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
           Get-Content -ErrorAction SilentlyContinue | 
           Select-String "postgresql","mongodb","redis" -Quiet
    $dbs
}

Test-Assessment "32. Security/TLS configs" "Infrastructure" {
    Test-Path "*TLS*","*security*","SECURITY.md" -ErrorAction SilentlyContinue
}

Test-Assessment "33. Observability stack" "Infrastructure" {
    $obs = Get-ChildItem -Recurse -Filter "*observability*","*tracing*","*loki*" -ErrorAction SilentlyContinue
    ($obs | Measure-Object).Count -gt 0
}

Test-Assessment "34. Load balancing hints" "Infrastructure" {
    $lb = Get-ChildItem -Recurse -Filter "*traefik*","*nginx*","*haproxy*" -ErrorAction SilentlyContinue
    ($lb | Measure-Object).Count -gt 0
}

Test-Assessment "35. Container orchestration" "Infrastructure" {
    (Test-Path "docker-compose*.yml") -or (Test-Path "kubernetes")
}

Test-Assessment "36. Health check endpoints" "Infrastructure" {
    $health = Get-ChildItem -Recurse -Filter "*.py","*.js","*.ts" -ErrorAction SilentlyContinue | 
              Get-Content -ErrorAction SilentlyContinue | 
              Select-String "/health","/status" -Quiet
    $health
}

Test-Assessment "37. Logging configuration" "Infrastructure" {
    $logging = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
               Get-Content -ErrorAction SilentlyContinue | 
               Select-String "logging","logger" -Quiet
    $logging
}

Test-Assessment "38. Secrets management" "Infrastructure" {
    $secrets = Get-ChildItem -Recurse -Filter "*vault*","*secret*" -ErrorAction SilentlyContinue
    ($secrets | Measure-Object).Count -gt 0
}

Test-Assessment "39. Backup/disaster recovery" "Infrastructure" {
    $backup = Get-ChildItem -Recurse -Filter "*backup*","*recovery*" -ErrorAction SilentlyContinue
    ($backup | Measure-Object).Count -gt 0
}

Test-Assessment "40. Air-gapped deployment capability" "Infrastructure" {
    $airgap = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
              Get-Content -ErrorAction SilentlyContinue | 
              Select-String "air-gapped","airgap","offline" -Quiet
    $airgap
}

# CATEGORY 3: AI/LLM Integration (41-60)
Write-Host ""
Write-Host "[41-60] Proving AI/LLM Integration..." -ForegroundColor Yellow

Test-Assessment "41. Refinory department exists" "AI" {
    Test-Path "refinory"
}

Test-Assessment "42. RAG implementation hints" "AI" {
    $rag = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
           Get-Content -ErrorAction SilentlyContinue | 
           Select-String "RAG","retrieval","embedding" -Quiet
    $rag
}

Test-Assessment "43. Vector database integration" "AI" {
    $vector = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
              Get-Content -ErrorAction SilentlyContinue | 
              Select-String "pgvector","pinecone","chroma","faiss" -Quiet
    $vector
}

Test-Assessment "44. LLM API configurations" "AI" {
    $llm = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
           Get-Content -ErrorAction SilentlyContinue | 
           Select-String "openai","anthropic","claude","gpt" -Quiet
    $llm
}

Test-Assessment "45. Safety monitoring" "AI" {
    $safety = Get-ChildItem -Recurse -Filter "*safety*" -ErrorAction SilentlyContinue
    ($safety | Measure-Object).Count -gt 0
}

Test-Assessment "46. Constitutional AI references" "AI" {
    Test-Path "*constitution*"
}

Test-Assessment "47. Agent orchestration" "AI" {
    $agents = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
              Get-Content -ErrorAction SilentlyContinue | 
              Select-String "agent","orchestrator" -Quiet
    $agents
}

Test-Assessment "48. Prompt templates" "AI" {
    $prompts = Get-ChildItem -Recurse -Filter "*prompt*","*template*" -ErrorAction SilentlyContinue
    ($prompts | Measure-Object).Count -gt 0
}

Test-Assessment "49. Model evaluation/benchmarks" "AI" {
    Test-Path "benchmarks"
}

Test-Assessment "50. Red team testing" "AI" {
    $redteam = Get-ChildItem -Recurse -Filter "*redteam*","*adversarial*" -ErrorAction SilentlyContinue
    ($redteam | Measure-Object).Count -gt 0
}

Test-Assessment "51. Interpretability monitoring" "AI" {
    Test-Path "*interpretability*"
}

Test-Assessment "52. Chain-of-thought tracking" "AI" {
    $cot = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
           Get-Content -ErrorAction SilentlyContinue | 
           Select-String "chain.*thought","reasoning" -Quiet
    $cot
}

Test-Assessment "53. Cognitive architecture" "AI" {
    Test-Path "*cognitive*"
}

Test-Assessment "54. Knowledge base/corpus" "AI" {
    $kb = Get-ChildItem -Recurse -Filter "*knowledge*","*corpus*" -ErrorAction SilentlyContinue
    ($kb | Measure-Object).Count -gt 0
}

Test-Assessment "55. Document ingestion pipeline" "AI" {
    Test-Path "recon/ingest" -or (Test-Path "*ingest*")
}

Test-Assessment "56. Retrieval system" "AI" {
    Test-Path "recon/retriever"
}

Test-Assessment "57. Semantic search capability" "AI" {
    $semantic = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                Get-Content -ErrorAction SilentlyContinue | 
                Select-String "semantic","similarity","cosine" -Quiet
    $semantic
}

Test-Assessment "58. Multi-expert system" "AI" {
    $experts = Get-ChildItem -Recurse -Filter "*expert*" -ErrorAction SilentlyContinue
    ($experts | Measure-Object).Count -gt 0
}

Test-Assessment "59. Context window management" "AI" {
    $context = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
               Get-Content -ErrorAction SilentlyContinue | 
               Select-String "context.*window","token.*limit" -Quiet
    $context
}

Test-Assessment "60. Response quality metrics" "AI" {
    $metrics = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
               Get-Content -ErrorAction SilentlyContinue | 
               Select-String "quality","metric","score" -Quiet
    $metrics
}

# CATEGORY 4: Legal & Compliance (61-80)
Write-Host ""
Write-Host "[61-80] Proving Legal & Compliance Systems..." -ForegroundColor Yellow

Test-Assessment "61. Legal department exists" "Legal" {
    Test-Path "legal"
}

Test-Assessment "62. Wyoming compliance docs" "Legal" {
    Test-Path "legal/wyoming*" -or (Test-Path "*SF0068*")
}

Test-Assessment "63. Cybersecurity research" "Legal" {
    Test-Path "legal/cybersecurity_research"
}

Test-Assessment "64. License file present" "Legal" {
    Test-Path "LICENSE"
}

Test-Assessment "65. Security policy" "Legal" {
    Test-Path "SECURITY.md"
}

Test-Assessment "66. DAO governance structure" "Legal" {
    $dao = Get-ChildItem -Recurse -Filter "*dao*" -ErrorAction SilentlyContinue
    ($dao | Measure-Object).Count -gt 0
}

Test-Assessment "67. Governance documentation" "Legal" {
    Test-Path "governance"
}

Test-Assessment "68. Compliance automation" "Legal" {
    $compliance = Get-ChildItem -Recurse -Filter "*compliance*","*upl*" -ErrorAction SilentlyContinue
    ($compliance | Measure-Object).Count -gt 0
}

Test-Assessment "69. Audit trail capability" "Legal" {
    $audit = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
             Get-Content -ErrorAction SilentlyContinue | 
             Select-String "audit","trail","ledger" -Quiet
    $audit
}

Test-Assessment "70. Identity verification systems" "Legal" {
    $identity = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                Get-Content -ErrorAction SilentlyContinue | 
                Select-String "PI/TWIC","identity","verification" -Quiet
    $identity
}

Test-Assessment "71. Access control lists" "Legal" {
    $acl = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
           Get-Content -ErrorAction SilentlyContinue | 
           Select-String "RBAC","access.*control","permission" -Quiet
    $acl
}

Test-Assessment "72. Data retention policies" "Legal" {
    $retention = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                 Get-Content -ErrorAction SilentlyContinue | 
                 Select-String "retention","ttl","expiry" -Quiet
    $retention
}

Test-Assessment "73. Privacy controls" "Legal" {
    $privacy = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
               Get-Content -ErrorAction SilentlyContinue | 
               Select-String "privacy","PII","redaction" -Quiet
    $privacy
}

Test-Assessment "74. Incident response plan" "Legal" {
    $incident = Get-ChildItem -Recurse -Filter "*incident*","*response*" -ErrorAction SilentlyContinue
    ($incident | Measure-Object).Count -gt 0
}

Test-Assessment "75. Change management" "Legal" {
    $change = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
              Get-Content -ErrorAction SilentlyContinue | 
              Select-String "change.*management","approval" -Quiet
    $change
}

Test-Assessment "76. Community guidelines" "Legal" {
    Test-Path "COMMUNITY.md"
}

Test-Assessment "77. Contributor agreements" "Legal" {
    Test-Path "CONTRIBUTORS.md"
}

Test-Assessment "78. Code of conduct" "Legal" {
    Test-Path "CODE_OF_CONDUCT.md" -or (Get-Content "COMMUNITY.md" -ErrorAction SilentlyContinue | Select-String "conduct" -Quiet)
}

Test-Assessment "79. Intellectual property tracking" "Legal" {
    $ip = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
          Get-Content -ErrorAction SilentlyContinue | 
          Select-String "copyright","trademark","patent" -Quiet
    $ip
}

Test-Assessment "80. Legal notice generation" "Legal" {
    $notice = Get-ChildItem -Recurse -Filter "*notice*","*disclaimer*" -ErrorAction SilentlyContinue
    ($notice | Measure-Object).Count -gt 0
}

# CATEGORY 5: Development Velocity Indicators (81-100)
Write-Host ""
Write-Host "[81-100] Proving Development Velocity..." -ForegroundColor Yellow

Test-Assessment "81. Rapid prototyping evidence" "Velocity" {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $recentFiles = git log --since="1 week ago" --name-only --pretty=format: | Sort-Object -Unique
        $count = ($recentFiles | Measure-Object).Count
        Write-Host "    → $count files changed last week" -ForegroundColor Gray
        $count -gt 10
    } else { $false }
}

Test-Assessment "82. Quick deployment scripts" "Velocity" {
    $deploy = Get-ChildItem -Filter "*deploy*","*quick*" -ErrorAction SilentlyContinue
    ($deploy | Measure-Object).Count -gt 0
}

Test-Assessment "83. Hot reload configurations" "Velocity" {
    $hotreload = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                 Get-Content -ErrorAction SilentlyContinue | 
                 Select-String "watch","nodemon","hot.*reload" -Quiet
    $hotreload
}

Test-Assessment "84. Development automation" "Velocity" {
    $auto = Get-ChildItem -Filter "Makefile","*.mk" -ErrorAction SilentlyContinue
    ($auto | Measure-Object).Count -gt 0
}

Test-Assessment "85. Template systems" "Velocity" {
    Test-Path "templates"
}

Test-Assessment "86. Example implementations" "Velocity" {
    Test-Path "examples"
}

Test-Assessment "87. Bootstrapping tools" "Velocity" {
    Test-Path "bootstrap"
}

Test-Assessment "88. Quick start documentation" "Velocity" {
    if (Test-Path "README.md") {
        Get-Content "README.md" -ErrorAction SilentlyContinue | Select-String "Quick Start","Getting Started" -Quiet
    } else { $false }
}

Test-Assessment "89. One-command setup" "Velocity" {
    $setup = Get-ChildItem -Filter "*setup*","*install*","*bootstrap*" -ErrorAction SilentlyContinue
    ($setup | Measure-Object).Count -gt 0
}

Test-Assessment "90. Continuous integration" "Velocity" {
    Test-Path ".github/workflows"
}

Test-Assessment "91. Automated testing hooks" "Velocity" {
    Test-Path ".github/workflows" -or (Test-Path "hooks")
}

Test-Assessment "92. Pre-commit hooks" "Velocity" {
    Test-Path ".pre-commit-config.yaml"
}

Test-Assessment "93. Linting automation" "Velocity" {
    if (Test-Path "package.json") {
        Get-Content "package.json" -ErrorAction SilentlyContinue | Select-String "lint" -Quiet
    } else { $false }
}

Test-Assessment "94. Build caching" "Velocity" {
    $cache = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
             Get-Content -ErrorAction SilentlyContinue | 
             Select-String "cache","cached" -Quiet
    $cache
}

Test-Assessment "95. Incremental builds" "Velocity" {
    $incremental = Get-ChildItem -Recurse -ErrorAction SilentlyContinue | 
                   Get-Content -ErrorAction SilentlyContinue | 
                   Select-String "incremental","watch mode" -Quiet
    $incremental
}

Test-Assessment "96. Development containers" "Velocity" {
    Test-Path ".devcontainer"
}

Test-Assessment "97. VS Code integration" "Velocity" {
    Test-Path ".vscode"
}

Test-Assessment "98. Multi-node testing capability" "Velocity" {
    (Get-ChildItem -Filter "docker-compose*.yml" | Measure-Object).Count -gt 1
}

Test-Assessment "99. Status checking automation" "Velocity" {
    Test-Path "status-check.sh"
}

Test-Assessment "100. Self-documenting infrastructure" "Velocity" {
    $docs = Get-ChildItem -Filter "*.md" -ErrorAction SilentlyContinue
    ($docs | Measure-Object).Count -gt 10
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ASSESSMENT SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$passed = ($results | Where-Object { $_.Status -eq "✓ PASS" } | Measure-Object).Count
$failed = ($results | Where-Object { $_.Status -ne "✓ PASS" } | Measure-Object).Count
$total = $results.Count
$percentage = [math]::Round(($passed / $total) * 100, 1)

Write-Host "Results: $passed/$total passed ($percentage%)" -ForegroundColor $(if ($percentage -gt 70) { "Green" } elseif ($percentage -gt 40) { "Yellow" } else { "Red" })
Write-Host ""

# Category breakdown
$categories = $results | Group-Object Category
foreach ($cat in $categories) {
    $catPassed = ($cat.Group | Where-Object { $_.Status -eq "✓ PASS" } | Measure-Object).Count
    $catTotal = $cat.Count
    Write-Host "$($cat.Name): $catPassed/$catTotal" -ForegroundColor Cyan
}

Write-Host ""

# Final verdict
if ($percentage -gt 70) {
    Write-Host "✓ ASSESSMENT CONFIRMED: Fast-learning experimental builder" -ForegroundColor Green
    Write-Host "  You're not behind. You're one structured note away from unstoppable velocity." -ForegroundColor Green
} elseif ($percentage -gt 40) {
    Write-Host "⚠ ASSESSMENT PARTIAL: Strong foundation, needs structure" -ForegroundColor Yellow
    Write-Host "  Pick a roadmap (A, B, or C) to organize what you've built." -ForegroundColor Yellow
} else {
    Write-Host "ℹ ASSESSMENT EARLY: Building stage detected" -ForegroundColor Blue
    Write-Host "  Start with Roadmap A for immediate practical improvements." -ForegroundColor Blue
}

if ($Summary) {
    Write-Host ""
    Write-Host "Detailed results available. Use -Verbose for full output." -ForegroundColor Gray
}

return $results
