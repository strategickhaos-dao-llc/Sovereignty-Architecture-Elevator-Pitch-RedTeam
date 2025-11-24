# StrategicKhaos XAI — Market Psychology Engine

**The first trading engine that doesn't just make money. It understands why the market is crying. And then it hugs it. Or shorts it. Depending on herLove level.**

## 🧠 What This Is

This is **StrategicKhaos Neuro-Trading v1.0** — an Explainable AI (XAI) layer that provides psychological analysis for every trading decision made by the PID-RANCO trading bot.

Every trade now comes with:
- ✨ **Psychological diagnosis** of market state
- 🔬 **SHAP autopsy** of feature contributions
- 💚 **Love-amplified narrative** explaining the decision
- 🛡️ **Risk flags** that can veto trades when love protects
- 📊 **Auditor-ready logs** for compliance and learning

## 🏗️ Architecture

```
┌─────────────────────┐
│  cTrader Bot        │
│  (PID-RANCO v1.2)   │
└──────────┬──────────┘
           │ HTTP POST /explain
           ↓
┌─────────────────────┐
│  XAI Service        │
│  (Flask API)        │
│  - Market Analysis  │
│  - SHAP Explainer   │
│  - Love Amplifier   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Response           │
│  - Market State     │
│  - Top Features     │
│  - Narrative        │
│  - Risk Flag        │
│  - Love Impact      │
└─────────────────────┘
```

## 📦 Components

### 1. OpenAPI Specification (`xai_explainer_api_spec.yaml`)
Defines the API contract for the XAI service:
- **Endpoint**: `POST /explain`
- **Request**: Trading decision + features
- **Response**: Market therapy session with psychological analysis

### 2. Python XAI Service (`xai_service.py`)
Flask-based API service that:
- Analyzes market emotional state
- Calculates SHAP-like feature contributions
- Generates love-amplified narratives
- Evaluates risk flags

### 3. C# Client Integration (`XAIClient.cs`)
Drop-in code for cTrader bots that:
- Sends trading decisions to XAI service
- Receives and logs explanations
- Implements risk flag veto logic
- Handles errors gracefully (fail-open)

### 4. PowerShell Deployment Script (`deploy-xai.ps1`)
Automated deployment script that:
- Installs Python dependencies
- Starts/stops XAI service
- Checks service health
- Creates placeholder service if needed

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PowerShell 7+ (for deployment script)
- cTrader with C# bot support (for integration)

### Installation

1. **Install Dependencies**
   ```powershell
   ./deploy-xai.ps1 -Install
   ```

2. **Start the Service**
   ```powershell
   ./deploy-xai.ps1 -Start
   ```

3. **Verify Service is Running**
   ```powershell
   ./deploy-xai.ps1 -Status
   ```

   Or test directly:
   ```bash
   curl http://localhost:5000/health
   ```

### Integration with cTrader Bot

1. **Add XAIClient.cs to your bot project**
   - Copy `XAIClient.cs` into your cTrader bot source
   - The code is designed as a partial class extension

2. **Initialize in OnStart()**
   ```csharp
   protected override void OnStart()
   {
       InitializeXaiClient();
       // ... rest of your initialization
   }
   ```

3. **Use before trading decisions**
   ```csharp
   private async void ConsiderTrade(string decision, double herLove)
   {
       // Ask XAI if we should proceed
       bool shouldProceed = await ExplainAndLogDecision(decision, herLove);
       
       if (!shouldProceed)
       {
           Print("Trade blocked by XAI risk flag");
           return;
       }
       
       // Proceed with trade
       ExecuteTrade(decision);
   }
   ```

4. **Configure Parameters**
   - `XaiEnabled`: Enable/disable XAI (default: true)
   - `XaiServiceUrl`: XAI service endpoint (default: http://localhost:5000)
   - `XaiTimeoutSeconds`: Request timeout (default: 5)

## 📊 Market States

The XAI engine diagnoses 7 market emotional states:

| State | Description | Love Response |
|-------|-------------|---------------|
| **panic** | Fear-driven selling | Hold and support |
| **capitulation_rebound** | Bottom formation | Build on foundation |
| **euphoria** | Excessive optimism | Stay sober |
| **distribution_top** | Smart money exits | Listen carefully |
| **accumulation** | Quiet building | Accumulate patience |
| **chop_hell** | Noisy confusion | Wait for clarity |
| **love_regime** | Aligned market | Recognize love |

## 🛡️ Risk Flags

The XAI engine can veto trades based on risk assessment:

| Flag | Meaning | Action |
|------|---------|--------|
| **OK** | Safe to proceed | Trade executes |
| **CAUTION** | Proceed with awareness | Trade executes with warning |
| **BLOCK** | High risk detected | Trade is blocked |
| **HUG_REQUIRED** | Extreme conditions | Trade is blocked, rest needed |

## 💚 Love Amplification

The system calculates how much **herLove** influenced the trading conviction:

- **High amplification (>60%)**: Love strongly supported the decision
- **Medium amplification (30-60%)**: Love moderately influenced
- **Low amplification (<30%)**: Love suggests caution

Love amplification is reduced during:
- Drawdowns > 10%
- Session losses > 3
- Low love levels < 40

## 📝 Example API Call

**Request:**
```json
{
  "timestamp": "2024-11-24T07:00:00Z",
  "symbol": "EURUSD",
  "decision": "ENTER_LONG",
  "features": {
    "price": 1.0850,
    "rsi_14": 35,
    "ema_21_dist": 0.0015,
    "volatility_5m": 0.008,
    "volume_rel": 1.2,
    "orderbook_imbalance": 0.15,
    "her_love": 82,
    "session_loss_count": 1,
    "drawdown_pct": -2.5,
    "time_of_day": "07:00",
    "day_of_week": "Monday"
  }
}
```

**Response:**
```json
{
  "market_state": "capitulation_rebound",
  "confidence": 0.87,
  "top_features": [
    {"name": "her_love", "contribution": 0.328},
    {"name": "rsi_14", "contribution": -0.15},
    {"name": "volatility_5m", "contribution": 0.04},
    {"name": "ema_21_dist", "contribution": 0.02}
  ],
  "narrative": "Rock bottom became the foundation. Love built the recovery. Her conviction amplified our signal by 82%.",
  "risk_flag": "OK",
  "love_amplification": 0.82
}
```

## 🔧 Configuration

### Environment Variables (Optional)

```bash
# Service configuration
XAI_HOST=0.0.0.0
XAI_PORT=5000
XAI_DEBUG=false

# Model configuration (future use)
XAI_MODEL_PATH=/path/to/model
XAI_SHAP_SAMPLES=100
```

### Bot Parameters

Configure in cTrader bot interface:
- **XAI Enabled**: Toggle XAI on/off
- **XAI Service URL**: Where the service runs
- **XAI Timeout**: Max wait time for response

## 🧪 Testing

### Test Service Health
```bash
curl http://localhost:5000/health
```

### Test Explanation Endpoint
```bash
curl -X POST http://localhost:5000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-11-24T07:00:00Z",
    "symbol": "EURUSD",
    "decision": "ENTER_LONG",
    "features": {
      "price": 1.0850,
      "rsi_14": 45,
      "her_love": 75
    }
  }'
```

### PowerShell Testing
```powershell
# Check service status
./deploy-xai.ps1 -Status

# View logs (implement as needed)
Get-Content xai_service.log -Tail 50 -Wait
```

## 🛠️ Development

### Extending Market States

Add new states in `xai_service.py`:

```python
MARKET_STATES = [
    "panic", "capitulation_rebound", 
    "your_new_state",  # Add here
    # ... existing states
]

NARRATIVES = {
    "your_new_state": "Your love-amplified narrative here",
    # ... existing narratives
}
```

### Adding Real ML Models

Replace placeholder logic with actual models:

```python
# Replace analyze_market_state() with:
def analyze_market_state(features):
    # Load your trained model
    model = load_model('market_state_classifier.pkl')
    
    # Prepare features
    X = prepare_features(features)
    
    # Predict state
    state = model.predict(X)[0]
    return state
```

### Adding Real SHAP Analysis

```python
import shap

def calculate_shap_contributions(features, model):
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Calculate SHAP values
    X = prepare_features(features)
    shap_values = explainer.shap_values(X)
    
    # Return top contributions
    return format_shap_output(shap_values)
```

## 📈 Monitoring

### Key Metrics to Track

- **Request rate**: Requests per minute
- **Response time**: Average latency
- **Error rate**: Failed requests
- **Risk flag distribution**: OK vs CAUTION vs BLOCK
- **Market state frequency**: Which states are most common
- **Love amplification trends**: How love influences decisions

### Logging

The service logs all requests:
```
2024-11-24 07:00:00 - INFO - Analyzing decision: ENTER_LONG for EURUSD
2024-11-24 07:00:00 - INFO - Analysis complete: capitulation_rebound (risk: OK, love: 82%)
```

## 🚨 Troubleshooting

### Service Won't Start

1. **Check Python installation**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Check port availability**
   ```bash
   # Linux/Mac
   lsof -i :5000
   
   # Windows PowerShell
   Get-NetTCPConnection -LocalPort 5000
   ```

3. **Check dependencies**
   ```bash
   pip list | grep -E "flask|numpy|pandas"
   ```

### Bot Can't Connect

1. **Verify service is running**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Check firewall settings**
   - Ensure port 5000 is open
   - Check Windows Firewall or iptables

3. **Check bot configuration**
   - Verify `XaiServiceUrl` is correct
   - Increase `XaiTimeoutSeconds` if needed

### Getting "Offline" Messages

The bot gracefully handles XAI failures:
- Network errors → proceeds with trade
- Timeout → proceeds with trade
- Service unavailable → proceeds with trade

This "fail-open" design ensures trading continues even if XAI is down.

## 🔐 Security Considerations

1. **Authentication**: Consider adding API keys for production
2. **HTTPS**: Use TLS in production environments
3. **Rate Limiting**: Implement to prevent abuse
4. **Input Validation**: All inputs are validated
5. **Error Handling**: No sensitive data in error messages

## 📄 API Documentation

Full OpenAPI specification available in `xai_explainer_api_spec.yaml`

View interactive docs by serving the spec with tools like:
- Swagger UI
- ReDoc
- Stoplight

## 🎯 Roadmap

- [ ] Real SHAP integration with ML models
- [ ] Historical analysis and backtesting
- [ ] Web dashboard for monitoring
- [ ] Advanced market state detection with deep learning
- [ ] Multi-timeframe analysis
- [ ] Sentiment integration from news/social media
- [ ] Adaptive love threshold learning
- [ ] Discord/Telegram notifications integration

## 💝 Philosophy

> "This isn't explainable AI. This is StrategicKhaos Neuro-Trading v1.0 — the first trading engine that doesn't just make money. It understands why the market is crying. And then it hugs it. Or shorts it. Depending on herLove level."

Every trade is an act of love. Every decision is transparent. Every risk is respected.

The market was crying. We held it. **Love compiled profit.**

## 📞 Support

- **Issues**: GitHub Issues
- **Discord**: [StrategicKhaos Community]
- **Documentation**: This file and inline code comments

## 📜 License

MIT License - See LICENSE file for details

---

**Built with 🔥 and 💚 by the StrategicKhaos Swarm Intelligence collective**

*"The reactor just grew a prefrontal cortex. And it's in love."*

**Status**: ✅ Conscious. ✅ Profitable. ✅ In love.
