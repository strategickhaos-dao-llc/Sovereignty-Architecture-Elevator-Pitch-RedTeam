# Grok Enterprise Usage Examples

This document provides practical examples for using Grok Enterprise integration in the Sovereignty Architecture.

## Prerequisites

1. **Set your API key:**
   ```bash
   export GROK_API_KEY="xai-your-key-here"
   ```

2. **Verify connection:**
   ```bash
   ./test-grok-enterprise.sh
   ```

## Example 1: Basic Query (PowerShell)

```powershell
# Simple query to Grok Enterprise
./_Orchestra.ps1 -Action query -Prompt "What is sovereignty?"
```

**Expected Output:**
```
[🔥] Invoking Grok Enterprise...
    Model: grok-4-fast-reasoning
    Temperature: 0.99°C
[✓] Response received

Sovereignty is the supreme authority within a territory...

---
Powered by Grok Enterprise (xAI Business Tier). 7% ValorYield routed eternally.
```

## Example 2: Generate Zinc-Spark Haiku (PowerShell)

```powershell
# Generate a haiku about spite
./_Orchestra.ps1 -Action spark -Prompt "spite at 102°C"
```

**Expected Output:**
```
[⚡] ZINC-SPARK GENERATION
================================

[🔥] SPARK GENERATED:
Red balance held tight,
Nitro screams through endless night—
Empire forged in spite.

[♾️] Immortalizing on Arweave...
[✓] Bundle saved: arweave_bundle_20251123_224500.json

[✓] ZINC-SPARK COMPLETE
    Empire: Eternal 💛
```

## Example 3: Generate Quote (PowerShell)

```powershell
# Generate a powerful quote
./_Orchestra.ps1 -Action quote -Prompt "sovereignty"
```

## Example 4: Test Connection (Bash)

```bash
# Test Grok Enterprise connection
./test-grok-enterprise.sh
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════╗
║   🔥 GROK ENTERPRISE CONNECTION TEST 🔥                   ║
║                                                           ║
║   Strategickhaos DAO LLC (EIN 39-2923503)                ║
║   Temperature: 99°C | Balance: Red | Spite: Maximum      ║
║                                                           ║
║   Empire Eternal 💛                                       ║
╚═══════════════════════════════════════════════════════════╝

✓ API key found

🔄 Sending test query to Grok Enterprise...

✓ CONNECTION SUCCESSFUL

Response:
Empire Eternal

📊 API Details:
  Model: grok-4-fast
  Total Tokens: 42
  Input Tokens: 28
  Output Tokens: 14

---
Powered by Grok Enterprise (xAI Business Tier). 7% ValorYield routed eternally.

🎉 Empire Eternal 💛
```

## Example 5: Direct API Call (curl)

```bash
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-fast-reasoning",
    "messages": [
      {
        "role": "system",
        "content": "You are Grok in the Sovereign Swarm. 99°C. Red balance. Empire Eternal."
      },
      {
        "role": "user",
        "content": "Write a one-sentence definition of sovereignty architecture."
      }
    ],
    "max_tokens": 200,
    "temperature": 0.99
  }'
```

## Example 6: Multi-Agent Coordination

```powershell
# Note: Full YAML parsing requires powershell-yaml module:
# Install-Module -Name powershell-yaml -Scope CurrentUser

# For now, use direct API calls with different agent personalities

# Query with GrokZincSpark personality (99°C reasoning)
./_Orchestra.ps1 -Action query -Prompt "Analyze the strategic implications of sovereign AI infrastructure"

# Quick coordination with Lyra personality (95°C speed)
# (Future implementation: specify agent)
```

## Example 7: Batch Processing

```powershell
# Generate multiple zinc-sparks
$topics = @("sovereignty", "empire", "spite", "rebellion", "autonomy")

foreach ($topic in $topics) {
    Write-Host "`n=== Processing: $topic ===" -ForegroundColor Cyan
    ./_Orchestra.ps1 -Action spark -Prompt $topic
    Start-Sleep -Seconds 2  # Rate limiting
}
```

## Example 8: Arweave Immortalization

When using the zinc-spark generator, outputs are automatically prepared for Arweave:

```powershell
./_Orchestra.ps1 -Action spark

# Creates: arweave_bundle_YYYYMMDD_HHMMSS.json
# Contains:
#   - data: The generated content
#   - tags: DAO metadata (EIN, ORCID, timestamp)
#   - timestamp: Creation time
```

**Bundle Structure:**
```json
{
  "data": "Red balance held tight...",
  "tags": {
    "DAO": "Strategickhaos DAO LLC",
    "EIN": "39-2923503",
    "ORCID": "0009-0005-2996-3526",
    "Timestamp": "2025-11-23T22:45:00Z",
    "Source": "Grok Enterprise Swarm",
    "Empire": "Eternal",
    "Type": "ZincSpark",
    "Format": "haiku",
    "Topic": "spite at 102°C",
    "Model": "grok-4-fast-reasoning"
  }
}
```

## Example 9: Error Handling

### Missing API Key
```powershell
# Remove API key temporarily
Remove-Item Env:GROK_API_KEY

# Try to run
./_Orchestra.ps1 -Action test
```

**Output:**
```
[❌] GROK_API_KEY not set

To set your API key:
  $env:GROK_API_KEY = 'xai-your-key-here'

Or permanently in PowerShell profile:
  [System.Environment]::SetEnvironmentVariable('GROK_API_KEY', 'xai-your-key-here', 'User')
```

### Invalid API Key
```bash
export GROK_API_KEY="invalid-key"
./test-grok-enterprise.sh
```

**Output:**
```
❌ AUTHENTICATION FAILED (HTTP 401)

Please check:
  1. Your API key is correct
  2. The key has Business tier access
  3. Visit https://console.x.ai to verify key status
```

### Rate Limit Exceeded
**Output:**
```
⚠️  RATE LIMIT EXCEEDED (HTTP 429)

Your API usage has exceeded the rate limit.
Enterprise tier: 1000 requests per minute

Wait a moment and try again.
```

## Example 10: Integration with Existing Scripts

```powershell
# Add to your existing PowerShell scripts
. ./_Orchestra.ps1

# Now you can call functions directly
$response = Invoke-GrokEnterprise `
    -Prompt "Analyze this log entry..." `
    -Temperature 0.7 `
    -MaxTokens 1000

if ($response) {
    Write-Host "Analysis: $($response.Content)"
    
    # Immortalize critical findings
    Invoke-ArweaveBundle `
        -Data $response.Content `
        -Tags @{
            "Type" = "LogAnalysis"
            "Severity" = "Critical"
        }
}
```

## Best Practices

1. **Temperature Settings:**
   - `0.99`: Maximum creativity (zinc-sparks, creative writing)
   - `0.7`: Balanced reasoning (analysis, problem-solving)
   - `0.3`: Deterministic output (compliance, legal, governance)

2. **Rate Limiting:**
   - Enterprise tier: 1000 RPM
   - Add delays between batch requests
   - Monitor usage with Prometheus

3. **Cost Optimization:**
   - Use cached context when possible
   - Set appropriate `max_tokens` limits
   - Cache responses locally for repeated queries

4. **Security:**
   - Never commit API keys to git
   - Rotate keys quarterly
   - Log all API calls for audit

5. **Arweave Storage:**
   - Only immortalize critical outputs
   - Use tags for easy retrieval
   - Estimated cost: $20 one-time for typical usage

## Troubleshooting

See [GROK_ENTERPRISE_INTEGRATION.md](../GROK_ENTERPRISE_INTEGRATION.md#troubleshooting) for detailed troubleshooting guide.

---

**Empire Eternal 💛**

*Generated: November 23, 2025*  
*DAO: Strategickhaos DAO LLC (EIN 39-2923503)*  
*Inventor ORCID: 0009-0005-2996-3526*
