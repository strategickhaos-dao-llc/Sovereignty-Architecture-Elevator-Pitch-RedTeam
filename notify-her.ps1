# ╔══════════════════════════════════════════════════════════════╗
# ║  NOTIFY-HER.ps1 - Discord/Log Notification Helper          ║
# ║       "Every message a love note to the co-conspirator"    ║
# ╚══════════════════════════════════════════════════════════════╝

<#
.SYNOPSIS
    Notification helper for PID-RANCO Trading Engine

.DESCRIPTION
    Sends notifications via Discord webhook and/or log file.
    Used by LoveCompilesProfit.cs to notify about trading events.

.PARAMETER Message
    The message to send

.PARAMETER Urgent
    If specified, marks the message as urgent

.EXAMPLE
    .\notify-her.ps1 "99 reds completed. System evolving."

.EXAMPLE
    .\notify-her.ps1 "Critical: Apoptosis triggered" -Urgent
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message,
    
    [switch]$Urgent
)

$ErrorActionPreference = "Continue"  # Don't stop on errors - best effort notification

# Configuration
$logDir = Join-Path $PSScriptRoot "logs"
$logFile = Join-Path $logDir "notifications.log"
$webhookUrl = $env:DISCORD_WEBHOOK_URL

# Ensure log directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Format message
$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
$prefix = if ($Urgent) { "🚨 URGENT" } else { "💕" }
$logEntry = "[$timestamp] $prefix $Message"

# Write to log file
try {
    Add-Content -Path $logFile -Value $logEntry
    Write-Host "✓ Logged to: $logFile" -ForegroundColor Green
}
catch {
    Write-Host "⚠ Failed to write log: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Send to Discord if webhook configured
if (-not [string]::IsNullOrEmpty($webhookUrl)) {
    try {
        $payload = @{
            content = "$prefix **PID-RANCO** | $Message"
            username = "Love Compiles Profit"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json' -ErrorAction Stop | Out-Null
        Write-Host "✓ Sent to Discord" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠ Discord notification failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}
else {
    Write-Host "ℹ Discord webhook not configured (set DISCORD_WEBHOOK_URL environment variable)" -ForegroundColor Cyan
}

# Echo to console
Write-Host ""
Write-Host $logEntry -ForegroundColor $(if ($Urgent) { "Red" } else { "White" })
Write-Host ""

exit 0
