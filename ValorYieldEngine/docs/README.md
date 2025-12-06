# ValorYield Engine

> **Sovereign Wealth-Building Platform – 100% Open Source, $0 Fees**

ValorYield Engine is an AI-orchestrated investment platform that runs entirely on YOUR infrastructure. No middlemen. No hidden fees. Complete sovereignty over your wealth.

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     ValorYield Engine                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│   │   Web UI     │    │  Mobile App  │    │  AI Legion   │    │
│   │  (React)     │    │   (Expo)     │    │ (Claude/GPT) │    │
│   │   :8009      │    │              │    │              │    │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    │
│          │                   │                   │            │
│          └───────────────────┼───────────────────┘            │
│                              │                                 │
│                    ┌─────────▼─────────┐                      │
│                    │   FastAPI         │                      │
│                    │   (Portfolio)     │                      │
│                    │   :8080           │                      │
│                    └─────────┬─────────┘                      │
│                              │                                 │
│          ┌───────────────────┼───────────────────┐            │
│          │                   │                   │            │
│   ┌──────▼──────┐    ┌───────▼───────┐   ┌──────▼──────┐     │
│   │ SwarmGate   │    │  TimescaleDB  │   │   NATS      │     │
│   │ (Events)    │◄───┤  (Data)       │◄──┤  (Pub/Sub)  │     │
│   └──────┬──────┘    └───────────────┘   └─────────────┘     │
│          │                                                    │
│   ┌──────▼──────────────────────────────────────────┐        │
│   │              Broker Integrations                 │        │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │        │
│   │  │Thread  │ │Kraken  │ │Ninja   │ │Fidelity│   │        │
│   │  │Bank    │ │Pro     │ │Trader  │ │(Manual)│   │        │
│   │  └────────┘ └────────┘ └────────┘ └────────┘   │        │
│   └─────────────────────────────────────────────────┘        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for web/mobile)
- NATS Server (optional, for event-driven features)

### Deploy Everything

```bash
cd ValorYieldEngine
chmod +x deploy.sh
./deploy.sh start
```

This starts:
- **API** at http://localhost:8080
- **Web UI** at http://localhost:8009
- **SwarmGate** for NATS event processing

### Manual Start (Development)

```bash
# Terminal 1: API
cd ValorYieldEngine/api
pip install -r requirements.txt
python main.py

# Terminal 2: Web UI
cd ValorYieldEngine/web
npm install
npm run dev

# Terminal 3: SwarmGate
cd ValorYieldEngine/swarmgate
pip install -r requirements.txt
python integration.py
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info and health check |
| `/health` | GET | Kubernetes health probe |
| `/api/v1/portfolio` | GET | Aggregated portfolio balance |
| `/api/v1/transactions` | GET | Transaction history |
| `/api/v1/transactions` | POST | Add transaction |
| `/api/v1/rebalance` | POST | Trigger rebalancing |
| `/api/v1/allocation` | GET | Target allocation percentages |

### Example: Get Portfolio

```bash
curl -H "Authorization: Bearer mock_token" \
  http://localhost:8080/api/v1/portfolio
```

Response:
```json
{
  "balance": 207.69,
  "account": "2143",
  "allocation": "Aggressive Mix",
  "last_updated": "2025-12-04T21:30:00Z"
}
```

## 🤖 SwarmGate Events

SwarmGate uses NATS pub/sub for event-driven automation:

### Topics

| Topic | Description |
|-------|-------------|
| `swarmgate.paycheck.detected` | Triggers 7% auto-allocation |
| `swarmgate.treasury.allocated` | New funds added to portfolio |
| `legion.rebalance.trigger` | Initiates dialectical rebalancing |
| `valoryield.deposit` | Deposit confirmation |
| `valoryield.rebalanced` | Rebalance complete notification |

### Simulate Paycheck

```bash
# Using NATS CLI
nats pub swarmgate.paycheck.detected '{"amount": 1000, "id": "pay_001"}'
```

This automatically:
1. Calculates 7% ($70) for treasury
2. Posts deposit to portfolio API
3. Triggers Legion AI analysis

## 🎯 Dialectical Rebalancer

Our Hegel-approved rebalancing algorithm:

- **Thesis**: Current portfolio allocation
- **Antithesis**: Target allocation (40% stocks, 30% crypto, 30% futures)
- **Synthesis**: Calculated trades to restore balance

Trades are only executed when drift exceeds 5% threshold.

## 🔧 Configuration

### Environment Variables

```bash
# Broker APIs
export THREAD_API_KEY="your_thread_bank_key"
export KRAKEN_KEY="your_kraken_api_key"
export KRAKEN_SECRET="your_kraken_secret"
export NT_API_TOKEN="your_ninjatrader_token"

# NATS
export NATS_URL="nats://localhost:4222"

# AI Legion (optional)
export OPENAI_API_KEY="sk-..."
export XAI_API_KEY="..."  # For Grok
export ANTHROPIC_API_KEY="..."  # For Claude
```

### Web UI API URL

Set in `web/.env`:
```
VITE_API_URL=http://localhost:8080/api/v1
```

## 📱 Mobile App

The mobile app uses Expo for cross-platform support:

```bash
cd ValorYieldEngine/mobile
npm install
npx expo start --tunnel
```

Scan the QR code with Expo Go app on your phone.

## 🏗️ Production Deployment

### GCP GKE

```bash
# Create cluster
gcloud container clusters create valoryield \
  --zone=us-central1-a \
  --num-nodes=3

# Apply manifests
kubectl apply -f k8s/
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      - NATS_URL=nats://nats:4222
  
  web:
    build: ./web
    ports:
      - "8009:8009"
    environment:
      - VITE_API_URL=http://api:8080/api/v1
  
  nats:
    image: nats:latest
    ports:
      - "4222:4222"
```

## 🔐 Security

- **No external data collection**: Your data stays on your infrastructure
- **Open source**: Audit the code yourself
- **API authentication**: Bearer token (upgrade to JWT/OAuth for production)
- **CORS configurable**: Lock down origins for production

## 📊 Roadmap

- [ ] Real broker API integrations (Thread, Kraken, NinjaTrader)
- [ ] PostgreSQL/TimescaleDB persistence
- [ ] Full AI Legion integration (Claude, GPT, Grok)
- [ ] Valor Pools DAO governance (Aragon)
- [ ] Prometheus metrics dashboard
- [ ] Mobile push notifications

## 🤝 Contributing

This is a sovereign project - contributions welcome!

1. Fork the repo
2. Create feature branch
3. Submit PR

## 📄 License

MIT License - See [LICENSE](../LICENSE)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Sovereignty is not given. It is claimed."*
