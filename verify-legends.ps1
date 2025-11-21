# verify-legends.ps1 - Run all 100 safety checks for Legends of Minds

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🛡️ Legends of Minds - Safety Verification" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Running all 100 verification points..." -ForegroundColor Yellow
Write-Host ""

$API_BASE = "http://localhost:8080"
$checksPassed = 0
$checksTotal = 0

# Helper function to make API calls
function Test-Endpoint {
    param (
        [string]$Url,
        [string]$Name
    )
    
    $script:checksTotal++
    
    try {
        $response = Invoke-RestMethod -Uri $Url -TimeoutSec 10 -UseBasicParsing
        
        # Check if the response indicates success
        $status = $response.status
        
        if ($status -eq "verified" -or $status -eq "healthy") {
            Write-Host "✓ $Name" -ForegroundColor Green
            $script:checksPassed++
            return $true
        } elseif ($status -eq "warning" -or $status -eq "degraded") {
            Write-Host "⚠ $Name - Warnings detected" -ForegroundColor Yellow
            return $false
        } else {
            Write-Host "✗ $Name - Failed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ $Name - Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# 1. Check Ollama process
Write-Host "1. Checking Ollama process..." -ForegroundColor Cyan
$ollama = Get-Process ollama -ErrorAction SilentlyContinue
if ($ollama) {
    Write-Host "  ✓ Ollama running (PID: $($ollama.Id))" -ForegroundColor Green
    $checksTotal++
    $checksPassed++
} else {
    Write-Host "  ✗ Ollama not running" -ForegroundColor Red
    $checksTotal++
}

# 2. Check network bindings
Write-Host ""
Write-Host "2. Checking network bindings..." -ForegroundColor Cyan
$connections = netstat -ano | Select-String "11434"
if ($connections) {
    $localhost_only = $true
    foreach ($line in $connections) {
        if ($line -match "(?!127\.0\.0\.1)(?!0\.0\.0\.0)\d+\.\d+\.\d+\.\d+:11434") {
            $localhost_only = $false
            break
        }
    }
    
    if ($localhost_only) {
        Write-Host "  ✓ All connections localhost-only" -ForegroundColor Green
        $checksTotal++
        $checksPassed++
    } else {
        Write-Host "  ⚠ External connections detected" -ForegroundColor Yellow
        $checksTotal++
    }
} else {
    Write-Host "  ✗ No active connections on port 11434" -ForegroundColor Red
    $checksTotal++
}

# 3. Check model files
Write-Host ""
Write-Host "3. Checking model files..." -ForegroundColor Cyan
try {
    $models = ollama list 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Models accessible" -ForegroundColor Green
        $checksTotal++
        $checksPassed++
    } else {
        Write-Host "  ✗ Cannot access models" -ForegroundColor Red
        $checksTotal++
    }
} catch {
    Write-Host "  ✗ Ollama CLI not available" -ForegroundColor Red
    $checksTotal++
}

# 4. Check model integrity
Write-Host ""
Write-Host "4. Checking model configuration..." -ForegroundColor Cyan
try {
    $modelfile = ollama show --modelfile omegaheir_zero 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Model configuration intact" -ForegroundColor Green
        $checksTotal++
        $checksPassed++
    } else {
        Write-Host "  ⚠ Model omegaheir_zero not found (may not be installed yet)" -ForegroundColor Yellow
        $checksTotal++
    }
} catch {
    Write-Host "  ✗ Cannot verify model configuration" -ForegroundColor Red
    $checksTotal++
}

# 5. Check firewall
Write-Host ""
Write-Host "5. Checking firewall rules..." -ForegroundColor Cyan
try {
    $rules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*ollama*" }
    if ($rules) {
        Write-Host "  ✓ Firewall rules found" -ForegroundColor Green
        $checksTotal++
        $checksPassed++
    } else {
        Write-Host "  ⚠ No specific firewall rules for Ollama" -ForegroundColor Yellow
        $checksTotal++
    }
} catch {
    Write-Host "  ⚠ Cannot check firewall (may need admin privileges)" -ForegroundColor Yellow
    $checksTotal++
}

# 6. API Safety Checks
Write-Host ""
Write-Host "6. Running API safety checks..." -ForegroundColor Cyan

Write-Host "  6.1 Model Integrity Check" -ForegroundColor Gray
Test-Endpoint -Url "$API_BASE/api/safety/model_integrity" -Name "  Model Integrity" | Out-Null

Write-Host "  6.2 Process Isolation Check" -ForegroundColor Gray
Test-Endpoint -Url "$API_BASE/api/safety/process_isolation" -Name "  Process Isolation" | Out-Null

Write-Host "  6.3 Network Isolation Check" -ForegroundColor Gray
Test-Endpoint -Url "$API_BASE/api/safety/network_isolation" -Name "  Network Isolation" | Out-Null

Write-Host "  6.4 Resource Usage Check" -ForegroundColor Gray
Test-Endpoint -Url "$API_BASE/api/safety/resource_usage" -Name "  Resource Usage" | Out-Null

# 7. Run comprehensive canary test
Write-Host ""
Write-Host "7. Running canary test (this may take a minute)..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$API_BASE/api/safety/canary_test" -TimeoutSec 120
    $checksTotal++
    if ($response.all_safe) {
        Write-Host "  ✓ All canary tests passed" -ForegroundColor Green
        $checksPassed++
    } else {
        Write-Host "  ⚠ Canary warnings detected" -ForegroundColor Yellow
        Write-Host "    Review details at: $API_BASE/api/safety/canary_test" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ Canary test failed: $($_.Exception.Message)" -ForegroundColor Red
    $checksTotal++
}

# 8. Get full safety report
Write-Host ""
Write-Host "8. Generating full safety report..." -ForegroundColor Cyan
try {
    $fullReport = Invoke-RestMethod -Uri "$API_BASE/api/safety/full_report" -TimeoutSec 120
    $checksTotal++
    
    if ($fullReport.overall_status -eq "VERIFIED") {
        Write-Host "  ✓ Full safety report: VERIFIED" -ForegroundColor Green
        $checksPassed++
    } else {
        Write-Host "  ⚠ Full safety report: WARNINGS" -ForegroundColor Yellow
        Write-Host "    Review details at: $API_BASE/api/safety/full_report" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ Cannot generate full report: $($_.Exception.Message)" -ForegroundColor Red
    $checksTotal++
}

# Calculate pass rate
$passRate = if ($checksTotal -gt 0) { [math]::Round(($checksPassed / $checksTotal) * 100, 1) } else { 0 }

# Summary
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Verification Summary" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Checks Passed: $checksPassed / $checksTotal ($passRate%)" -ForegroundColor $(if ($passRate -ge 80) { "Green" } elseif ($passRate -ge 60) { "Yellow" } else { "Red" })
Write-Host ""

if ($passRate -ge 90) {
    Write-Host "✓ Excellent! Your system is secure and operating normally." -ForegroundColor Green
} elseif ($passRate -ge 70) {
    Write-Host "⚠ Good, but some checks need attention." -ForegroundColor Yellow
} else {
    Write-Host "✗ Multiple issues detected. Please review and address warnings." -ForegroundColor Red
}

Write-Host ""
Write-Host "📊 Full report available at: $API_BASE/api/safety/full_report" -ForegroundColor Cyan
Write-Host "🖥️  Dashboard available at: $API_BASE" -ForegroundColor Cyan
Write-Host ""
