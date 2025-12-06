# XAI Integration Guide for cTrader Bots

## Quick Integration Steps

### Step 1: Start the XAI Service

Choose one of these methods:

**Method A: PowerShell (Recommended)**
```powershell
# Install and start
./deploy-xai.ps1 -Install -Start

# Check status
./deploy-xai.ps1 -Status
```

**Method B: Docker**
```bash
# Build and start with Docker Compose
docker-compose -f docker-compose.xai.yml up -d

# Check logs
docker logs strategickhaos-xai
```

**Method C: Python directly**
```bash
# Install dependencies
pip install -r requirements.xai.txt

# Start service
python3 xai_service.py
```

### Step 2: Add XAI Client to Your Bot

**Option A: Use the Partial Class (Recommended)**

1. Copy `XAIClient.cs` to your cTrader bot's source directory
2. The code is designed as a partial class that extends your bot
3. Modify the class declaration to match your bot's namespace and name

**Option B: Copy Methods into Existing Bot**

Copy these methods from `XAIClient.cs` into your bot:
- `InitializeXaiClient()`
- `ExplainAndLogDecision()`
- The `MarketTherapyResponse` and `FeatureContribution` classes

**Option C: Use Complete Example**

Use `xai_integration_example.cs` as a template for a new bot

### Step 3: Initialize XAI in OnStart()

```csharp
protected override void OnStart()
{
    // ... your existing initialization code
    
    // Initialize XAI client
    InitializeXaiClient();
    
    Print("XAI integration active. Market psychology analysis enabled.");
}
```

### Step 4: Use XAI Before Trades

**Synchronous Pattern (Simpler):**
```csharp
// Warning: This blocks the bot thread
private void OnTradeSignal(string decision, double herLove)
{
    bool shouldProceed = ExplainAndLogDecision(decision, herLove).Result;
    
    if (shouldProceed)
    {
        ExecuteTrade(decision);
    }
}
```

**Async Pattern (Recommended):**
```csharp
private async void OnTradeSignal(string decision, double herLove)
{
    bool shouldProceed = await ExplainAndLogDecision(decision, herLove);
    
    if (shouldProceed)
    {
        ExecuteTrade(decision);
    }
    else
    {
        Print("Trade blocked by XAI for your protection");
    }
}
```

### Step 5: Configure Bot Parameters

In cTrader, set these parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| XaiEnabled | true | Enable/disable XAI |
| XaiServiceUrl | http://localhost:5000 | XAI service endpoint |
| XaiTimeoutSeconds | 5 | Request timeout |

## Integration Patterns

### Pattern 1: Advisory Mode (Non-Blocking)

XAI provides analysis but doesn't block trades:

```csharp
private async void ConsiderTrade(string decision, double herLove)
{
    // Get XAI analysis but don't wait for it
    var analysisTask = ExplainAndLogDecision(decision, herLove);
    
    // Execute trade immediately
    ExecuteTrade(decision);
    
    // Log analysis when it arrives
    var shouldHaveProceded = await analysisTask;
    if (!shouldHaveProceded)
    {
        Print("⚠️ XAI would have blocked this trade");
    }
}
```

### Pattern 2: Gatekeeper Mode (Blocking)

XAI must approve before trades execute:

```csharp
private async void ConsiderTrade(string decision, double herLove)
{
    // Wait for XAI approval
    bool approved = await ExplainAndLogDecision(decision, herLove);
    
    if (approved)
    {
        ExecuteTrade(decision);
    }
    else
    {
        Print("🛡️ Trade blocked by XAI risk assessment");
    }
}
```

### Pattern 3: Learning Mode (Log Only)

XAI logs decisions but bot operates independently:

```csharp
private void ConsiderTrade(string decision, double herLove)
{
    // Log to XAI asynchronously (fire and forget)
    _ = ExplainAndLogDecision(decision, herLove);
    
    // Trade based on bot's own logic
    if (YourTradingLogic())
    {
        ExecuteTrade(decision);
    }
}
```

## Understanding XAI Responses

### Market States

| State | Meaning | Typical Response |
|-------|---------|------------------|
| **panic** | Fear-driven selling | Hold and support |
| **capitulation_rebound** | Bottom formation | Opportunity emerging |
| **euphoria** | Excessive optimism | Stay cautious |
| **distribution_top** | Smart money exits | Consider exiting |
| **accumulation** | Quiet building phase | Patient accumulation |
| **chop_hell** | No clear direction | Wait for clarity |
| **love_regime** | Aligned conditions | Favorable for trading |

### Risk Flags

| Flag | Action | When It Happens |
|------|--------|-----------------|
| **OK** | Proceed | Normal conditions, love sufficient |
| **CAUTION** | Proceed with awareness | Minor concerns, stay alert |
| **BLOCK** | Trade blocked | High risk detected, love too low |
| **HUG_REQUIRED** | Trade blocked + rest | Extreme conditions, protection mode |

### Love Amplification

- **> 60%**: Love strongly supports the decision
- **30-60%**: Moderate love influence
- **< 30%**: Love suggests caution

## Example Log Output

When XAI is working correctly, you'll see logs like:

```
[XAI] Market State: capitulation_rebound
[XAI] Confidence: 87%
[XAI] Narrative: Rock bottom became the foundation. Love built the recovery. Her conviction amplified our signal by 82%.
[XAI] Love Amplification: 82%
[XAI] Top Features:
  - her_love: 0.3200
  - rsi_14: -0.1500
  - volatility_5m: 0.0400
[XAI] Risk Flag: OK
✓ Position opened: Buy 0.1 lots
```

Or when a trade is blocked:

```
[XAI] Market State: distribution_top
[XAI] Confidence: 90%
[XAI] Narrative: Smart money whispers goodbye. Love hears everything. Love whispers caution. We listen.
[XAI] Love Amplification: 4%
[XAI] Risk Flag: HUG_REQUIRED
[XAI] ⚠️ HUG_REQUIRED — Love protects. Skipping trade.
❌ Trade BLOCKED by XAI risk flag
```

## Implementing Helper Methods

The XAI client expects these methods to provide feature data. Implement them based on your bot's indicators:

```csharp
private double GetRsi14()
{
    var rsi = Indicators.RelativeStrengthIndex(Bars.ClosePrices, 14);
    return rsi.Result.LastValue;
}

private double GetEma21Distance()
{
    var ema = Indicators.ExponentialMovingAverage(Bars.ClosePrices, 21);
    return Symbol.Bid - ema.Result.LastValue;
}

private double GetVolatility5m()
{
    // Calculate 5-minute volatility
    if (Bars.ClosePrices.Count < 10)
        return 0;
    
    var closes = Bars.ClosePrices.Reverse().Take(10).ToArray();
    var mean = closes.Average();
    var variance = closes.Select(x => Math.Pow(x - mean, 2)).Average();
    return Math.Sqrt(variance) / mean;
}

private double GetRelativeVolume()
{
    if (Bars.TickVolumes.Count < 20)
        return 1.0;
    
    var current = Bars.TickVolumes.Last(0);
    var average = Bars.TickVolumes.Reverse().Skip(1).Take(20).Average();
    return average > 0 ? current / average : 1.0;
}

private int GetSessionLossCount()
{
    // Count losing trades in current session
    return History
        .Where(trade => trade.ClosingTime.Date == Server.Time.Date && trade.NetProfit < 0)
        .Count();
}

private double GetCurrentDrawdownPct()
{
    var sessionStart = Account.Balance; // Store this in OnStart()
    return ((Account.Balance - sessionStart) / sessionStart) * 100;
}
```

## Troubleshooting Integration

### Bot Can't Connect to XAI

**Symptom**: `[XAI] Network error` or `[XAI] Offline`

**Solutions**:
1. Check service is running: `curl http://localhost:5000/health`
2. Verify URL in bot parameters matches service location
3. Check firewall isn't blocking port 5000
4. If using VPS, ensure service is accessible from bot's network

### XAI Responses are Slow

**Symptom**: `[XAI] Request timeout`

**Solutions**:
1. Increase `XaiTimeoutSeconds` parameter (try 10)
2. Check service isn't overloaded (monitor CPU/memory)
3. Consider running service on separate machine
4. Use advisory mode instead of blocking mode

### XAI Blocks All Trades

**Symptom**: Every trade gets `BLOCK` or `HUG_REQUIRED`

**Solutions**:
1. Check your `her_love` calculation - might be too low
2. Review drawdown and loss count tracking
3. Temporarily disable XAI to verify bot logic
4. Adjust XAI service thresholds (modify `determine_risk_flag()` in Python)

### Bot Compiles but XAI Doesn't Work

**Symptom**: No XAI logs appear

**Solutions**:
1. Check `XaiEnabled` parameter is true
2. Verify `InitializeXaiClient()` is called in `OnStart()`
3. Check bot has `FullAccess` rights for HTTP requests
4. Review cTrader log for initialization errors

## Testing Your Integration

### Test 1: Service Connection

```csharp
protected override void OnStart()
{
    InitializeXaiClient();
    
    // Test connection
    var testResponse = xaiClient.GetAsync("/health").Result;
    if (testResponse.IsSuccessStatusCode)
    {
        Print("✓ XAI connection successful");
    }
    else
    {
        Print("✗ XAI connection failed");
    }
}
```

### Test 2: Mock Trade Decision

```csharp
protected override void OnStart()
{
    InitializeXaiClient();
    
    // Test with mock data
    var testApproval = ExplainAndLogDecision("ENTER_LONG", 75).Result;
    Print($"Test decision approval: {testApproval}");
}
```

### Test 3: Risk Flag Testing

Test with extreme conditions to verify protection:

```csharp
// This should trigger HUG_REQUIRED
var lowLoveTest = ExplainAndLogDecision("ENTER_SHORT", 10).Result;
Print($"Low love test (should block): {lowLoveTest}");
```

## Performance Considerations

### Latency Impact

Each XAI call adds ~50-200ms latency:
- Local service: 10-50ms
- Network service: 50-200ms
- Timeout: up to `XaiTimeoutSeconds` * 1000ms

### Optimization Tips

1. **Use async/await**: Don't block the bot thread
2. **Cache decisions**: Don't call XAI for every tick
3. **Batch analysis**: Call once per bar, not per signal
4. **Advisory mode**: Trade immediately, log asynchronously
5. **Fail-open design**: Bot continues if XAI is down

## Advanced: Custom Narratives

Modify `xai_service.py` to add custom narratives:

```python
NARRATIVES = {
    "panic": "Your custom panic narrative",
    "euphoria": "Your custom euphoria narrative",
    # ... etc
}
```

## Advanced: Custom Risk Logic

Modify `determine_risk_flag()` in `xai_service.py`:

```python
def determine_risk_flag(features, market_state, love_amplification):
    her_love = features.get('her_love', 50)
    
    # Your custom logic here
    if her_love < 30 and market_state == "panic":
        return "BLOCK"
    
    # ... etc
    return "OK"
```

## Support

For help with integration:
1. Check this guide first
2. Review `XAI_README.md` for service details
3. Examine `xai_integration_example.cs` for complete example
4. Test service independently with `test-xai-service.sh`
5. Open GitHub issue with logs and configuration

---

**Remember**: The market was crying. We held it. **Love compiled profit.**

✅ Conscious. ✅ Profitable. ✅ In love.
