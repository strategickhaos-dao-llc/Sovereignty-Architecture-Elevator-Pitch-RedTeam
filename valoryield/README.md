# ValorYield Engine

**Sovereign wealth platform - 100% open source, zero fees, full control**

## Overview

ValorYield Engine is a production-ready API for managing sovereign wealth portfolios. It provides:

- 🏦 Portfolio tracking across multiple sources (Thread Bank, Kraken, NinjaTrader, Fidelity)
- 💰 SwarmGate 7% protocol integration for automated deposits
- ⚖️ Automated rebalancing with configurable thresholds
- 📊 Real-time statistics and fee comparison vs traditional platforms
- 🔐 100% sovereignty - your money, your control

## Quick Start

### Deploy in 30 seconds

```bash
cd valoryield
./deploy.sh
```

Or manually:

```bash
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CORS_ORIGINS` | `*` | Comma-separated list of allowed origins. In production, set to specific domains like `https://app.example.com` |

Example for production:
```bash
CORS_ORIGINS="https://app.valoryield.com,https://admin.valoryield.com" python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Platform info and status |
| `/api/v1/health` | GET | Kubernetes health check |
| `/api/v1/portfolio` | GET | Get portfolio balance |
| `/api/v1/transactions` | GET | Get transaction history |
| `/api/v1/deposit` | POST | Receive SwarmGate deposit |
| `/api/v1/rebalance` | POST | Trigger portfolio rebalancing |
| `/api/v1/stats` | GET | Platform statistics |

## API Documentation

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Example Usage

### Get Portfolio Balance

```bash
curl http://localhost:8080/api/v1/portfolio
```

Response:
```json
{
  "balance": 207.69,
  "account": "2143",
  "allocation": "Aggressive Mix",
  "last_updated": "2025-12-04T18:27:23.123218",
  "vs_moneylion": "173% fee savings"
}
```

### Make a Deposit

```bash
curl -X POST "http://localhost:8080/api/v1/deposit?amount=50.00"
```

Response:
```json
{
  "deposited": 50.0,
  "new_balance": 257.69,
  "status": "success",
  "trigger": "rebalance_queued"
}
```

### Trigger Rebalancing

```bash
curl -X POST "http://localhost:8080/api/v1/rebalance?drift=7"
```

Response:
```json
{
  "status": "triggered",
  "message": "Legion analyzing portfolio",
  "drift": 7.0,
  "threshold": 5.0
}
```

## Running Tests

```bash
cd valoryield
python -m pytest test_main.py -v
```

## Architecture

- **FastAPI**: High-performance async API framework
- **Pydantic**: Data validation and serialization
- **uvicorn**: ASGI server for production deployment

## Fee Comparison

| Platform | Annual Fees | Your Control | Transparency |
|----------|-------------|--------------|--------------|
| ValorYield | $0 | 100% | Open Source |
| MoneyLion | $360+ | 0% | Black Box |

## Future Integrations

- [ ] Thread Bank API (cash balance)
- [ ] Kraken Pro API (crypto holdings)
- [ ] NinjaTrader API (futures/options)
- [ ] Fidelity CSV import (stocks)
- [ ] NATS messaging for Legion orchestration

## License

MIT License - 100% open source
