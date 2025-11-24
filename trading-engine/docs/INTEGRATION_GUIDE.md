# PID-RANCO Integration Guide

This guide explains how to integrate PID-RANCO v1.2 into your trading infrastructure, connect it with Discord notifications, and customize it for your specific needs.

## Table of Contents

1. [Quick Start](#quick-start)
2. [NinjaTrader Setup](#ninjatrader-setup)
3. [Discord Integration](#discord-integration)
4. [Voice/Mic Integration](#voicemic-integration)
5. [Custom Risk Parameters](#custom-risk-parameters)
6. [Monitoring and Alerting](#monitoring-and-alerting)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Windows 10/11 (for NinjaTrader)
- NinjaTrader 8 installed and licensed
- PowerShell 5.1+ or PowerShell Core 7+
- Discord account (optional, for notifications)

### 5-Minute Setup

```powershell
# 1. Clone/download the repository
cd C:\Trading

# 2. Review the mythic configuration
notepad trading-engine\config\pid-ranco-mythic.yaml

# 3. Copy strategy to NinjaTrader
copy trading-engine\strategies\PIDRANCOStrategy.cs "%USERPROFILE%\Documents\NinjaTrader 8\bin\Custom\Strategies\"

# 4. Open NinjaTrader and compile
# Tools → Edit NinjaScript → Strategy → Compile (F5)

# 5. Deploy in simulation mode
cd trading-engine\scripts
.\Deploy-PIDRANCO.ps1 -Environment "simulation"
```

### First Test Run

1. Open NinjaTrader Control Center
2. Go to **New → Strategy**
3. Select **PIDRANCOStrategy** from the list
4. Choose a chart (e.g., ES 12-24, 5 min)
5. Click **OK** to start in simulation mode
6. Watch the Output window for logs

---

## NinjaTrader Setup

### 1. Strategy Installation

Copy `PIDRANCOStrategy.cs` to your NinjaTrader strategies folder:

```powershell
$strategyPath = "trading-engine\strategies\PIDRANCOStrategy.cs"
$ntPath = "$env:USERPROFILE\Documents\NinjaTrader 8\bin\Custom\Strategies\"
Copy-Item $strategyPath $ntPath -Force
```

### 2. Compile Strategy

In NinjaTrader:
1. Open **Tools → Edit NinjaScript → Strategy...**
2. Find **PIDRANCOStrategy** in the list
3. Press **F5** or click **Compile**
4. Check **Output** tab for compilation errors
5. If successful, you'll see: "Compiled successfully"

### 3. Configure Strategy Parameters

When adding to a chart, configure these properties:

| Property | Default | Description |
|----------|---------|-------------|
| **Risk Per Trade** | 0.0069 | 0.69% of account per trade |
| **Max Drawdown** | 0.0337 | 3.37% max loss from peak |
| **EMA Period** | 21 | Trend indicator period |
| **RSI Period** | 14 | Momentum indicator period |
| **Silence Threshold (min)** | 5 | Minutes of silence before flatten |

### 4. Monitor Output Window

Keep the **Output** window visible to see:
```
[INFO] 2024-11-24 09:15:30 - Loss #5 recorded. Profit: $-25.50
[WARN] Voice volume is NaN/Infinity. Using 0.
[ENTRY] Long: Voice=45.2, RSI=28.3, Pain=-15.20
[EXIT] Long: High voice=85.0, Profit=1.25%
[POETRY] Voice collapse detected. Silence: 5.2 min
```

---

## Discord Integration

### 1. Create Discord Webhook

1. Open your Discord server
2. Go to **Server Settings → Integrations → Webhooks**
3. Click **New Webhook**
4. Name it "PID-RANCO"
5. Select target channel (e.g., #trading-alerts)
6. Copy the **Webhook URL**

### 2. Configure PowerShell Script

Set the webhook as environment variable:

```powershell
# Temporary (current session)
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN"

# Permanent (for current user)
[Environment]::SetEnvironmentVariable(
    "DISCORD_WEBHOOK_URL", 
    "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN",
    "User"
)
```

Or pass directly to script:

```powershell
.\Deploy-PIDRANCO.ps1 `
    -Environment "simulation" `
    -DiscordWebhook "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN"
```

### 3. Test Discord Notifications

```powershell
# Test notification manually
$webhook = $env:DISCORD_WEBHOOK_URL
$payload = @{
    content = "🎭 **PID-RANCO Test** 🎭`nDiscord integration working!"
    username = "PID-RANCO v1.2"
} | ConvertTo-Json

Invoke-RestMethod -Uri $webhook -Method Post -Body $payload -ContentType 'application/json'
```

### 4. C# Discord Integration (Optional)

For real-time alerts from the strategy, add Discord webhook calls in C#:

```csharp
// Add to PIDRANCOStrategy.cs

private void NotifyDiscord(string message, string level = "INFO")
{
    try
    {
        string webhookUrl = Environment.GetEnvironmentVariable("DISCORD_WEBHOOK_URL");
        
        if (string.IsNullOrEmpty(webhookUrl))
            return;
        
        string emoji = level switch
        {
            "ERROR" => "🔴",
            "WARN" => "⚠️",
            "POETRY" => "🎭",
            _ => "ℹ️"
        };
        
        string payload = $"{{\"content\":\"{emoji} **PID-RANCO** {emoji}\\n{message}\"}}";
        
        using (var client = new System.Net.Http.HttpClient())
        {
            var content = new System.Net.Http.StringContent(
                payload, 
                System.Text.Encoding.UTF8, 
                "application/json"
            );
            
            client.PostAsync(webhookUrl, content).Wait();
        }
    }
    catch (Exception ex)
    {
        Print($"[WARN] Discord notification failed: {ex.Message}");
    }
}
```

Then call from apoptosis:

```csharp
private void TriggerHugProtocol()
{
    // ... existing code ...
    
    NotifyDiscord("99 losses reached. Apoptosis triggered. Positions flattened.", "POETRY");
}
```

---

## Voice/Mic Integration

### Current Implementation

The strategy includes placeholder voice integration that always returns `50.0`:

```csharp
private double GetHerVoiceVolumeSafe()
{
    try
    {
        // TODO: Replace with actual mic indicator
        double val = 50.0;  // Placeholder
        
        // Validation and clamping...
    }
}
```

### Real Microphone Integration Options

#### Option 1: NAudio Library

1. Add NAudio NuGet package to NinjaTrader references
2. Implement volume capture:

```csharp
using NAudio.Wave;

private WaveInEvent waveIn;
private double currentVolume = 0.0;

protected override void OnStateChange()
{
    if (State == State.DataLoaded)
    {
        InitializeMicrophone();
    }
    else if (State == State.Terminated)
    {
        DisposeMicrophone();
    }
}

private void InitializeMicrophone()
{
    try
    {
        waveIn = new WaveInEvent();
        waveIn.WaveFormat = new WaveFormat(44100, 1);
        waveIn.DataAvailable += OnAudioDataAvailable;
        waveIn.StartRecording();
        Print("[INFO] Microphone initialized");
    }
    catch (Exception ex)
    {
        Print($"[ERROR] Mic init failed: {ex.Message}");
    }
}

private void OnAudioDataAvailable(object sender, WaveInEventArgs e)
{
    try
    {
        float max = 0;
        for (int i = 0; i < e.BytesRecorded; i += 2)
        {
            short sample = BitConverter.ToInt16(e.Buffer, i);
            float val = sample / 32768f;
            max = Math.Max(max, Math.Abs(val));
        }
        currentVolume = max * 100.0;  // Scale to 0-100
    }
    catch { }
}

private void DisposeMicrophone()
{
    if (waveIn != null)
    {
        waveIn.StopRecording();
        waveIn.Dispose();
    }
}

// Then in GetHerVoiceVolumeSafe:
private double GetHerVoiceVolumeSafe()
{
    try
    {
        double val = currentVolume;  // Use captured volume
        // ... rest of validation
    }
}
```

#### Option 2: Windows Audio API

Use `NAudio.CoreAudioApi` for system audio capture:

```csharp
using NAudio.CoreAudioApi;

private MMDevice micDevice;

private void InitializeMicrophone()
{
    var enumerator = new MMDeviceEnumerator();
    micDevice = enumerator.GetDefaultAudioEndpoint(DataFlow.Capture, Role.Multimedia);
}

private double GetHerVoiceVolumeSafe()
{
    try
    {
        if (micDevice != null)
        {
            double val = micDevice.AudioMeterInformation.MasterPeakValue * 100.0;
            // ... rest of validation
        }
    }
}
```

#### Option 3: External Python Service

1. Create Python service capturing mic data
2. Expose via HTTP API
3. Call from C# strategy

```python
# voice_service.py
from flask import Flask, jsonify
import pyaudio
import numpy as np

app = Flask(__name__)

def get_mic_volume():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    volume = np.abs(data).mean() / 32768.0 * 100.0
    stream.close()
    p.terminate()
    return volume

@app.route('/volume')
def volume():
    return jsonify({'volume': get_mic_volume()})

if __name__ == '__main__':
    app.run(port=5000)
```

Then in C#:

```csharp
private double GetHerVoiceVolumeSafe()
{
    try
    {
        using (var client = new System.Net.Http.HttpClient())
        {
            var response = client.GetStringAsync("http://localhost:5000/volume").Result;
            var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(response);
            double val = json.volume;
            // ... rest of validation
        }
    }
    catch (Exception ex)
    {
        Print($"[ERROR] VoiceError: {ex.Message}. Using 0.");
        return 0.0;
    }
}
```

---

## Custom Risk Parameters

### Adjusting Risk Percentages

Edit `config/pid-ranco-mythic.yaml`:

```yaml
risk_parameters:
  risk_per_trade: "0.5%"    # More conservative
  max_drawdown: "2.0%"      # Tighter stop
```

Then update C# strategy properties:

```csharp
// In NinjaTrader strategy properties dialog
Risk Per Trade: 0.005   // 0.5%
Max Drawdown:   0.02    // 2.0%
```

### Dynamic Position Sizing

To actually calculate position size (not just validate):

```csharp
private int CalculatePositionSize(double stopDistanceTicks)
{
    try
    {
        double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
        double riskAmount = accountValue * maxRiskPerTrade;
        double tickValue = Instrument.MasterInstrument.PointValue * TickSize;
        double quantity = Math.Floor(riskAmount / (stopDistanceTicks * tickValue));
        
        // Enforce min/max
        quantity = Math.Max(1, quantity);
        quantity = Math.Min(quantity, 100);  // Max position
        
        Print($"[INFO] Position size: {quantity} contracts, risk: ${riskAmount:F2}");
        
        return (int)quantity;
    }
    catch (Exception e)
    {
        Print($"[ERROR] Position sizing failed: {e.Message}");
        return 1;  // Default to 1 contract
    }
}

// Use in entries:
private void HandleEntries(double herLove, double rsi14, double marketPain)
{
    if (herLove > 30 && rsi14 < 30 && marketPain < 0)
    {
        int qty = CalculatePositionSize(20);  // 20 tick stop
        EnterLong(qty, "LoveLong");
    }
}
```

---

## Monitoring and Alerting

### Log Analysis

PID-RANCO logs are structured for parsing:

```powershell
# Parse logs for safety events
Get-Content "C:\NinjaTrader 8\log\*.txt" | 
    Select-String "\[POETRY\]|\[CRITICAL\]|\[SAFETY\]" |
    Out-File safety_events.log

# Count losses per session
Get-Content "C:\NinjaTrader 8\log\*.txt" | 
    Select-String "Loss #\d+" | 
    Measure-Object | 
    Select-Object Count
```

### Real-Time Dashboard

Create a simple dashboard to monitor:

```powershell
# monitor.ps1
while ($true) {
    Clear-Host
    Write-Host "=== PID-RANCO Monitor ===" -ForegroundColor Cyan
    Write-Host ""
    
    # Count losses today
    $losses = (Get-Content "C:\NinjaTrader 8\log\*.txt" | 
               Select-String "Loss #\d+" | 
               Measure-Object).Count
    
    Write-Host "Session Losses: $losses / 99" -ForegroundColor $(if ($losses -lt 50) { "Green" } elseif ($losses -lt 90) { "Yellow" } else { "Red" })
    
    # Check apoptosis
    $apoptosis = Get-Content "C:\NinjaTrader 8\log\*.txt" | 
                 Select-String "\[POETRY\] 99 fails" | 
                 Select-Object -Last 1
    
    if ($apoptosis) {
        Write-Host "APOPTOSIS TRIGGERED!" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 5
}
```

### Grafana Integration

For enterprise monitoring, export logs to Grafana:

1. Install Promtail to tail NinjaTrader logs
2. Configure Loki as log aggregator
3. Create Grafana dashboard with panels:
   - Loss count gauge (0-99)
   - Apoptosis status indicator
   - Voice volume timeline
   - Profit/loss chart

---

## Troubleshooting

### Common Issues

#### 1. Strategy Won't Compile

**Error**: "CS0246: The type or namespace name 'X' could not be found"

**Solution**:
- Check that all `using` statements are present
- Verify NinjaTrader 8 SDK references
- Clean and rebuild: Tools → Edit NinjaScript → Compile (Ctrl+Shift+F5)

#### 2. "YAML DNA missing"

**Error**: "YAML DNA missing at path: ../config/pid-ranco-mythic.yaml"

**Solution**:
```powershell
# Verify YAML exists
Test-Path "trading-engine\config\pid-ranco-mythic.yaml"

# If false, check current directory
Get-Location

# Navigate to correct directory
cd trading-engine\scripts
.\Deploy-PIDRANCO.ps1
```

#### 3. Voice Always Returns 0

**Symptom**: `[WARN] Voice volume is NaN/Infinity. Using 0.`

**Solution**:
- This is expected with placeholder implementation
- Mic integration not yet active
- See [Voice/Mic Integration](#voicemic-integration) section

#### 4. Apoptosis Triggers Too Early

**Symptom**: Strategy disabled before 99 losses

**Solution**:
- Check if `sessionLossCount` persists across sessions
- Verify state reset in `OnStateChange` for new sessions
- Add counter reset logic:

```csharp
protected override void OnStateChange()
{
    if (State == State.DataLoaded)
    {
        // Reset session counters
        sessionLossCount = 0;
        hugProtocolTriggered = false;
        lastProcessedTradeCount = 0;
    }
}
```

#### 5. Max Drawdown Breached Immediately

**Symptom**: Strategy disables on first bar

**Solution**:
- Check `peakEquity` initialization
- Verify account value is correct:

```csharp
double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
Print($"[DEBUG] Account value: ${accountValue:F2}");
Print($"[DEBUG] Peak equity: ${peakEquity:F2}");
```

#### 6. Discord Notifications Not Sending

**Solution**:
```powershell
# Test webhook manually
$webhook = $env:DISCORD_WEBHOOK_URL
Test-NetConnection -ComputerName discord.com -Port 443

# Check webhook URL format
if ($webhook -notmatch "^https://discord.com/api/webhooks/\d+/[A-Za-z0-9_-]+$") {
    Write-Host "Invalid webhook URL format" -ForegroundColor Red
}
```

---

## Next Steps

1. **Simulation Testing**: Run in simulation for at least 30 days
2. **Log Analysis**: Review all safety triggers and edge cases
3. **Voice Integration**: Implement real microphone capture
4. **Discord Setup**: Configure notifications for critical events
5. **Backtesting**: Run on historical data to validate logic
6. **Live Paper**: Deploy to live paper account before real money
7. **Risk Review**: Adjust 0.69%/3.37% based on risk tolerance

## Support

For issues or questions:
- Review `SAFETY_FEATURES.md` for detailed guardrail documentation
- Check NinjaTrader Output window for error messages
- Examine `pid-ranco-mythic.yaml` for configuration errors
- Test in simulation mode first, always

---

*"From chaos to order, from poetry to production, from 99 reds to green."*
