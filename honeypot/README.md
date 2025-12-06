# 🎣 Honeypot Deployment Architecture

**Offensive Sovereignty: Learn by being attacked**

This system deploys an intentionally vulnerable Signal Routing Authority (SRA) as a honeypot for red team training and attack pattern learning.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTION (BLUE)                        │
│                   Sovereign Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  ✅ Event Gateway (self-hosted)                             │
│  ✅ NATS JetStream (distributed)                            │
│  ✅ Discord Bot (hardened)                                  │
│  ✅ SovereignPRManager (full Legion review)                 │
│  🛡️ Zero external dependencies                              │
│  🛡️ Cryptographic verification everywhere                   │
│  🛡️ 100% sovereignty                                        │
└─────────────────────────────────────────────────────────────┘

                           VS

┌─────────────────────────────────────────────────────────────┐
│                      HONEYPOT (RED)                          │
│              Deliberately Vulnerable Target                  │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ Signal Routing Authority (Vulnerable)                   │
│     - Centralized routing                                   │
│     - No HMAC verification                                  │
│     - No rate limiting                                      │
│     - Unauthenticated endpoints                             │
│  🎣 Honeytrap (Attack Logger)                               │
│     - Logs every attack                                     │
│     - Classifies attack types                               │
│     - Feeds data to Legion                                  │
│  🧠 Legion Analyzer                                         │
│     - AI-powered attack analysis                            │
│     - Generates defenses                                    │
│     - Updates PR rules                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
honeypot/
├── README.md                          # This file
├── k8s/
│   ├── honeypot-sra-deployment.yaml   # Vulnerable SRA deployment
│   ├── honeytrap-deployment.yaml      # Attack logging service
│   └── legion-analyzer-deployment.yaml # AI analysis service
├── legion/
│   └── honeypot_analyzer.py           # Legion AI analyzer module
└── scripts/
    ├── deploy-honeypot-sra.sh         # Main deployment script
    └── red-team-attacks.sh            # Attack scenario generator
```

## 🚀 Quick Start

### Prerequisites

- Kubernetes cluster with `kubectl` configured
- (Optional) NATS for real-time event streaming
- (Optional) Anthropic or OpenAI API key for AI analysis

### Deploy the Honeypot

```bash
# 1. Deploy everything
./honeypot/scripts/deploy-honeypot-sra.sh deploy

# 2. Check status
./honeypot/scripts/deploy-honeypot-sra.sh status

# 3. Run red team attacks
./honeypot/scripts/red-team-attacks.sh

# 4. Watch attack logs
kubectl logs -f deployment/honeytrap -n red-team-honeypot

# 5. Watch Legion analysis
kubectl logs -f deployment/legion-analyzer -n red-team-honeypot

# 6. Cleanup when done
./honeypot/scripts/deploy-honeypot-sra.sh cleanup
```

## 🔴 Red Team Attack Scenarios

The `red-team-attacks.sh` script includes:

| Attack Type | Description |
|------------|-------------|
| **Unauthenticated Access** | Testing access without authentication |
| **XSS Injection** | Cross-site scripting attempts |
| **SQL Injection** | Database manipulation attempts |
| **Path Traversal** | Directory escape attempts |
| **Rate Limit Testing** | DoS simulation |
| **HTTP Method Tampering** | Unauthorized method usage |
| **Header Injection** | IP spoofing, host override |
| **Config Disclosure** | Sensitive file access attempts |
| **Command Injection** | OS command execution attempts |
| **SSRF** | Server-side request forgery |
| **Credential Probing** | Admin/token discovery |
| **Buffer Overflow** | Oversized payload attacks |

### Custom Attack Testing

```bash
# Set custom honeypot URL
export HONEYPOT_URL="http://honeypot-sra.strategickhaos.com"

# Set delay between attacks (seconds)
export ATTACK_DELAY=1

# Run attacks
./honeypot/scripts/red-team-attacks.sh
```

## 🧠 Legion Analysis

The Legion Honeypot Analyzer:

1. **Captures** attack events from Honeytrap
2. **Analyzes** patterns using AI (Claude or GPT-4)
3. **Classifies** attacks by type and severity
4. **Generates** defensive countermeasures:
   - Detection code (Python)
   - Security configuration
   - Kubernetes NetworkPolicies
   - SovereignPRManager rules
5. **Updates** production defenses automatically

### Attack Classification

| Category | Attack Types |
|----------|-------------|
| **Injection** | XSS, SQL Injection, Command Injection |
| **Access Control** | Path Traversal, Method Tampering |
| **Authentication** | Credential Probing, Session Hijacking |
| **SSRF** | Internal service access, Metadata service |
| **DoS** | Buffer Overflow, Rate Limit Bypass |
| **Reconnaissance** | Config Disclosure, Information Gathering |

## 📊 Complete Feedback Loop

```
1. COPILOT generates vulnerable code (PR #7)
        ↓
2. YOU recognize sovereignty violation
        ↓
3. DEPLOY to honeypot (Red cluster)
        ↓
4. RED TEAM attacks honeypot
        ↓
5. HONEYTRAP logs all attacks
        ↓
6. LEGION analyzes attack patterns (Claude/GPT-4)
        ↓
7. GENERATE defenses automatically
        ↓
8. UPDATE SovereignPRManager rules
        ↓
9. BLUE TEAM production is hardened
        ↓
10. REPEAT: Copilot generates code → checked by smarter SPM

RESULT: Your system learns by being attacked
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HONEYPOT_URL` | Target honeypot URL | `http://localhost:8080` |
| `NATS_URL` | NATS server URL | `nats://localhost:4222` |
| `AI_PROVIDER` | AI backend (`anthropic`, `openai`, `none`) | `anthropic` |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ATTACK_LOG_FILE` | Path to attack log | `/var/log/honeytrap/attacks.jsonl` |
| `POLL_INTERVAL` | Log polling interval (seconds) | `5` |

### Kubernetes Secrets

```bash
# Create AI secrets (optional, for AI-powered analysis)
kubectl create secret generic ai-secrets \
  -n red-team-honeypot \
  --from-literal=ANTHROPIC_API_KEY=sk-your-key \
  --from-literal=OPENAI_API_KEY=sk-your-key
```

## 🔒 Security Considerations

### ⚠️ This is an INTENTIONALLY VULNERABLE system

- **DO NOT** deploy in production environments
- **DO NOT** expose to public internet without proper isolation
- **DO** deploy in isolated red team clusters only
- **DO** use network policies to prevent lateral movement
- **DO** monitor for unauthorized access

### Network Isolation

The deployment includes a NetworkPolicy that:
- Allows all ingress (honeypot purpose)
- Restricts egress to internal logging only
- Prevents access to production namespaces

## 📈 Metrics

Honeytrap exposes Prometheus metrics at `/metrics`:

```
honeytrap_attacks_total          # Total attacks captured
honeytrap_attacks_by_type{type}  # Attacks by classification
```

View stats at `/stats` endpoint:
```bash
curl http://honeypot:8080/stats | jq
```

## 🛠️ Development

### Local Testing

```bash
# Start honeytrap locally
cd honeypot/legion
python -m http.server 8080

# In another terminal, run attacks
export HONEYPOT_URL=http://localhost:8080
./honeypot/scripts/red-team-attacks.sh
```

### Building Container Images

```bash
# Build honeytrap image
docker build -t honeytrap:latest -f - . << 'EOF'
FROM python:3.11-slim
COPY honeypot/k8s/honeytrap-code.py /app/trap_server.py
CMD ["python", "/app/trap_server.py"]
EOF

# Build analyzer image
docker build -t legion-analyzer:latest -f - . << 'EOF'
FROM python:3.11-slim
RUN pip install anthropic openai nats-py
COPY honeypot/legion/honeypot_analyzer.py /app/
CMD ["python", "/app/honeypot_analyzer.py"]
EOF
```

## 📄 License

MIT License - See [LICENSE](../LICENSE)

---

**"The best defense is attacking yourself first."**

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
