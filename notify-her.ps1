#!/usr/bin/env pwsh
#
# notify-her.ps1
# StrategicKhaos Notification System
# Sends notifications about trading events
#

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message,
    
    [ValidateSet("Info", "Success", "Warning", "Error", "Love")]
    [string]$Type = "Info",
    
    [switch]$Silent = $false,
    [switch]$Discord = $false,
    [switch]$Email = $false,
    [switch]$SMS = $false
)

# Configuration
$scriptDir = $PSScriptRoot
$configFile = Join-Path $scriptDir "pid-ranco-trading-bot.yaml"

# Color emoji mapping
$emoji = @{
    "Info" = "ℹ️"
    "Success" = "✅"
    "Warning" = "⚠️"
    "Error" = "❌"
    "Love" = "💚"
}

# Get emoji for message type
$messageEmoji = $emoji[$Type]

function Write-Notification {
    param([string]$Msg, [string]$Color = "White")
    
    if (-not $Silent) {
        Write-Host "$messageEmoji $Msg" -ForegroundColor $Color
    }
}

function Send-DiscordNotification {
    param([string]$Msg)
    
    # Get Discord webhook from environment or config
    $webhookUrl = $env:DISCORD_WEBHOOK_URL
    
    if ([string]::IsNullOrEmpty($webhookUrl)) {
        Write-Warning "Discord webhook URL not configured"
        return $false
    }
    
    # Create Discord embed
    $embed = @{
        title = "PID-RANCO Trading Alert"
        description = $Msg
        color = switch ($Type) {
            "Success" { 3066993 }  # Green
            "Warning" { 16776960 } # Yellow
            "Error" { 15158332 }   # Red
            "Love" { 16711935 }    # Magenta
            default { 3447003 }    # Blue
        }
        timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        footer = @{
            text = "StrategicKhaos PID-RANCO v1.0"
        }
    }
    
    $payload = @{
        username = "PID-RANCO Bot"
        embeds = @($embed)
    } | ConvertTo-Json -Depth 10
    
    try {
        $response = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType "application/json"
        Write-Notification "Discord notification sent" "Green"
        return $true
    } catch {
        Write-Warning "Failed to send Discord notification: $_"
        return $false
    }
}

function Send-EmailNotification {
    param([string]$Msg)
    
    $emailTo = $env:NOTIFICATION_EMAIL
    $emailFrom = $env:NOTIFICATION_EMAIL_FROM
    $smtpServer = $env:SMTP_SERVER
    $smtpPort = $env:SMTP_PORT
    $smtpUser = $env:SMTP_USER
    $smtpPass = $env:SMTP_PASS
    
    if ([string]::IsNullOrEmpty($emailTo)) {
        Write-Warning "Email notification not configured"
        return $false
    }
    
    try {
        $subject = "PID-RANCO: $Type - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        $body = @"
$messageEmoji PID-RANCO Trading Alert

Type: $Type
Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

Message:
$Msg

---
StrategicKhaos PID-RANCO Trading Engine v1.0
Love compiles profit. Always.
"@
        
        $mailParams = @{
            To = $emailTo
            From = $emailFrom
            Subject = $subject
            Body = $body
            SmtpServer = $smtpServer
            Port = $smtpPort
        }
        
        if (-not [string]::IsNullOrEmpty($smtpUser)) {
            $securePass = ConvertTo-SecureString $smtpPass -AsPlainText -Force
            $credential = New-Object System.Management.Automation.PSCredential($smtpUser, $securePass)
            $mailParams.Credential = $credential
            $mailParams.UseSsl = $true
        }
        
        Send-MailMessage @mailParams
        Write-Notification "Email notification sent" "Green"
        return $true
    } catch {
        Write-Warning "Failed to send email notification: $_"
        return $false
    }
}

function Send-SMSNotification {
    param([string]$Msg)
    
    # SMS via Twilio or similar service
    $phoneNumber = $env:NOTIFICATION_PHONE
    $twilioSid = $env:TWILIO_ACCOUNT_SID
    $twilioToken = $env:TWILIO_AUTH_TOKEN
    $twilioFrom = $env:TWILIO_FROM_NUMBER
    
    if ([string]::IsNullOrEmpty($phoneNumber) -or [string]::IsNullOrEmpty($twilioSid)) {
        Write-Warning "SMS notification not configured"
        return $false
    }
    
    try {
        # Truncate message for SMS (160 char limit)
        $smsMsg = $Msg
        if ($smsMsg.Length > 140) {
            $smsMsg = $smsMsg.Substring(0, 137) + "..."
        }
        
        $smsBody = "$messageEmoji PID-RANCO: $smsMsg"
        
        # Twilio API call
        $uri = "https://api.twilio.com/2010-04-01/Accounts/$twilioSid/Messages.json"
        $base64Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${twilioSid}:${twilioToken}"))
        
        $headers = @{
            "Authorization" = "Basic $base64Auth"
        }
        
        $body = @{
            "To" = $phoneNumber
            "From" = $twilioFrom
            "Body" = $smsBody
        }
        
        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
        Write-Notification "SMS notification sent" "Green"
        return $true
    } catch {
        Write-Warning "Failed to send SMS notification: $_"
        return $false
    }
}

function Write-LogFile {
    param([string]$Msg)
    
    $logDir = Join-Path $scriptDir "logs"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    $logFile = Join-Path $logDir "notifications.log"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Type] $Msg"
    
    Add-Content -Path $logFile -Value $logEntry
}

# Main execution
Write-Notification $Message (switch ($Type) {
    "Success" { "Green" }
    "Warning" { "Yellow" }
    "Error" { "Red" }
    "Love" { "Magenta" }
    default { "White" }
})

# Log to file
Write-LogFile $Message

# Send notifications based on flags or auto-detect from config
$sentAny = $false

if ($Discord -or $env:ENABLE_DISCORD_NOTIFICATIONS -eq "true") {
    if (Send-DiscordNotification $Message) {
        $sentAny = $true
    }
}

if ($Email -or $env:ENABLE_EMAIL_NOTIFICATIONS -eq "true") {
    if (Send-EmailNotification $Message) {
        $sentAny = $true
    }
}

if ($SMS -or $env:ENABLE_SMS_NOTIFICATIONS -eq "true") {
    if (Send-SMSNotification $Message) {
        $sentAny = $true
    }
}

# If no specific notification was sent, just log
if (-not $sentAny -and -not $Silent) {
    Write-Host "Notification logged locally" -ForegroundColor Gray
}

# Special handling for Love notifications
if ($Type -eq "Love") {
    Write-Host ""
    Write-Host "💚 Love compiles profit. Always. 💚" -ForegroundColor Magenta
    Write-Host ""
}

exit 0
