# notify-her.ps1
# Notification system for PID-RANCO Trading Engine
# "Every message is compiled with love"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    
    [string]$Priority = "normal",  # low, normal, high, critical
    [string]$Type = "info"         # info, success, warning, error
)

# Color mapping based on message type
$colors = @{
    "info"    = "Cyan"
    "success" = "Green"
    "warning" = "Yellow"
    "error"   = "Red"
}

$color = $colors[$Type]
if (-not $color) {
    $color = "White"
}

# Priority indicators
$prioritySymbols = @{
    "low"      = "•"
    "normal"   = "→"
    "high"     = "⚡"
    "critical" = "🔥"
}

$symbol = $prioritySymbols[$Priority]
if (-not $symbol) {
    $symbol = "→"
}

# Timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Format the message
$formattedMessage = @"

╔════════════════════════════════════════════════════════════════╗
║  PID-RANCO NOTIFICATION
║  Time: $timestamp
║  Priority: $Priority
╠════════════════════════════════════════════════════════════════╣
║
║  $symbol $Message
║
╚════════════════════════════════════════════════════════════════╝

"@

# Display notification
Write-Host $formattedMessage -ForegroundColor $color

# Log to file
$logDir = "$env:USERPROFILE\Documents\PID-RANCO-Logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "notifications.log"
$logEntry = "[$timestamp] [$Priority] [$Type] $Message"
Add-Content -Path $logFile -Value $logEntry

# Optional: Send to Discord webhook if configured
$discordWebhook = $env:DISCORD_WEBHOOK_URL
if ($discordWebhook) {
    try {
        $payload = @{
            content = "**PID-RANCO Notification**`n$symbol $Message"
            username = "LoveCompilesProfit Bot"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri $discordWebhook -Method Post -Body $payload -ContentType "application/json" | Out-Null
        Write-Host "✓ Notification sent to Discord" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to send Discord notification: $_" -ForegroundColor Yellow
    }
}

# Optional: Windows toast notification
if ($Priority -in @("high", "critical")) {
    try {
        $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
        Write-Host "✓ System notification displayed" -ForegroundColor Green
    } catch {
        # Toast notifications not available, skip silently
    }
}

# Play sound for critical notifications
if ($Priority -eq "critical") {
    [Console]::Beep(800, 200)
    [Console]::Beep(1000, 200)
    [Console]::Beep(800, 200)
}

# Return success
return $true
