# SKOS Quickstart Guide

Deploy the autonomous immune system in 60 seconds.

## Prerequisites

- Docker installed
- Docker Compose installed
- Linux/macOS (Windows via WSL2)

## Deploy

```bash
# 1. Navigate to the package
cd skos-immune-system

# 2. Make scripts executable
chmod +x deploy.sh test.sh

# 3. Deploy!
./deploy.sh
```

## Verify

```bash
./test.sh
```

Expected output:
```
╔══════════════════════════════════════════════════════════════╗
║           SKOS IMMUNE SYSTEM TEST SUITE v0.1.0              ║
╚══════════════════════════════════════════════════════════════╝

[1/4] Infrastructure Tests
  Testing: Docker available... PASS
  Testing: NATS container running... PASS
  Testing: Coordinator container running... PASS
  Testing: Thermal Sentinel container running... PASS

[2/4] NATS Tests
  Testing: NATS health endpoint... PASS
  Testing: NATS server info... PASS
  Testing: JetStream enabled... PASS

[3/4] Service Health Tests
  Testing: Coordinator healthy... PASS
  Testing: Thermal Sentinel healthy... PASS
  Testing: Coordinator started... PASS
  Testing: Thermal Sentinel started... PASS

[4/4] Communication Tests
  Testing: Heartbeats flowing... PASS
  Testing: Coordinator receiving heartbeats... PASS

All tests passed! (13/13)

Your sovereign immune system is healthy! 🛡️✅
```

## Monitor

```bash
# View all logs
docker compose logs -f

# View coordinator logs
docker compose logs -f coordinator

# View thermal sentinel logs
docker compose logs -f thermal-sentinel

# NATS monitoring dashboard
open http://localhost:8222
```

## Deploy to Remote Node

```bash
# Copy to Nova
scp -r skos-immune-system/ nova.local:~/

# SSH and deploy
ssh nova.local "cd skos-immune-system && ./deploy.sh"
```

## Stop

```bash
docker compose down
```

## Clean Restart

```bash
./deploy.sh --clean --build
```

## Configuration

Edit `config.yaml` to customize:
- Temperature thresholds
- Healing actions
- Alert policies
- Node configuration

## Troubleshooting

### Containers not starting?
```bash
docker compose logs
```

### NATS connection issues?
```bash
curl http://localhost:8222/healthz
```

### Need a clean slate?
```bash
./deploy.sh --clean --build
```

---

**Done.** Your infrastructure now heals itself. 🛡️
