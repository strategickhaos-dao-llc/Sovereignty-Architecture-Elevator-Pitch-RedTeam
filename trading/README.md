# Trading Infrastructure

This directory contains trading automation components for the Strategickhaos sovereign architecture.

## Components

### 1. NinjaTrader Strategy (`ninjatrader/`)

`RiskHardenedStrategy.cs` - A C# NinjaScript strategy for NinjaTrader 8 with:

- **ATR-based position sizing**: Calculates position size based on volatility (Average True Range)
- **Daily loss limit**: Automatically stops trading when 2% daily drawdown is reached
- **Trade count limit**: Hard cap of 5 trades per day (configurable)
- **Risk per trade**: 1% account risk per trade (configurable)

#### Installation

1. Copy `RiskHardenedStrategy.cs` to your NinjaTrader strategy folder:
   - Windows: `Documents\NinjaTrader 8\bin\Custom\Strategies\`
2. Compile in NinjaTrader: Tools → Compile
3. Add to chart or run in Strategy Analyzer

#### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `riskPerTradePct` | 1.0 | Account % to risk per trade |
| `dailyLossLimitPct` | 2.0 | Max daily drawdown % |
| `maxTradesPerDay` | 5 | Hard cap on daily trades |
| `atrPeriod` | 14 | ATR lookback period |
| `atrStopMultiplier` | 2.0 | ATR multiplier for stop distance |

#### Verification

Test in NT Simulator with ES/MNQ data. Expected sizing for $520 balance at 1% risk:
- Risk amount: $5.20
- If ATR=20 pts, stop=40 pts, ES point=$50
- Position size: floor(5.2 / 2000) = 1 contract (minimum)

### 2. Webhook Relay (`webhook-relay/`)

`zapier_nt_relay.py` - A Flask middleware for secure Zapier-to-NinjaTrader signal relay.

#### Features

- **Ticker whitelist**: Only approved symbols pass through
- **Size caps**: Maximum position sizes enforced
- **Daily limits**: Loss and trade count limits
- **Manual approval**: Optional high-value trade approval

#### Installation

```bash
cd trading/webhook-relay
pip install -r requirements.txt
python zapier_nt_relay.py
```

#### Configuration

Environment variables:
- `NT_API_URL`: NinjaTrader API endpoint (default: `http://localhost:5001/execute`)
- `REQUIRE_APPROVAL`: Enable manual approval for high-value trades
- `RELAY_HOST`: Bind host (default: `0.0.0.0`)
- `RELAY_PORT`: Bind port (default: `5000`)

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook` | POST | Main signal endpoint |
| `/health` | GET | Health check |
| `/config` | GET | Current configuration |
| `/reset` | POST | Reset daily state |

#### Example Usage

```bash
# Send a trading signal
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"signal": "BUY 2 shares of ES @ $5200.50"}'

# Check health
curl http://localhost:5000/health
```

#### Production Deployment

1. Run behind nginx/caddy with SSL
2. Use gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 zapier_nt_relay:app`
3. Set `REQUIRE_APPROVAL=true` for high-value trade review

## Integration Flow

```
[Zapier/Grok Automation]
        ↓
   HTTP POST /webhook
        ↓
[Flask Relay - zapier_nt_relay.py]
   - Validate ticker
   - Check size limits
   - Verify daily limits
        ↓
   Forward to NT API
        ↓
[NinjaTrader - RiskHardenedStrategy.cs]
   - Calculate ATR-based size
   - Apply risk limits
   - Execute trade
```

## Security Considerations

1. **Never expose relay directly to internet** - Use SSL and auth
2. **Whitelist only needed tickers** - Reduce attack surface
3. **Set conservative limits** - Start with low daily caps
4. **Enable approval mode** - For high-value trades
5. **Monitor logs** - Review all trades and rejections

## License

Part of the Strategickhaos Sovereignty Architecture under MIT License.
