# 10-Dimensional Chess Council

## AI Research Super-Collider Architecture

**640 Containerized LLM Agents in Adversarial Strategy Games**

## Overview

The 10D Chess Council is an unprecedented AI research system where 640 LLM agents play adversarial strategy games to synthesize peer-reviewed knowledge. Each agent runs in a full OS container (Parrot/Kali Linux) with terminal access, research tools, and frequency-tuned harmonic communication.

## Architecture

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    10-DIMENSIONAL CHESS COUNCIL                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Layer 10: Publication & Dissemination (C9-C10: 8372-16744 Hz)        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: arXiv submitters, patent drafters, GitHub publishers │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 9: Validation & Verification (C8-C9: 4186-8372 Hz)             ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: reproducibility testers, fact checkers, peer reviewers │ ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 8: Linguistic Generation (C7-C8: 2093-4186 Hz)                 ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: academic writers, citation formatters, translators   │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 7: Ethical Evaluation (C6-C7: 1046-2093 Hz)                    ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: bias auditors, risk assessors, compliance checkers   │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 6: Strategic Reasoning (C5-C6: 523-1046 Hz)                    ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: game theorists, Nash equilibrium solvers, allocators │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 5: Predictive Modeling (C4-C5: 261-523 Hz)                     ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: model trainers, hyperparameter optimizers, simulators │  ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 4: Knowledge Synthesis (C3-C4: 130-261 Hz)                     ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: meta-analysts, systematic reviewers, contradiction    │  ║
║  │            resolvers, cross-domain linkers                       │  ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 3: Statistical Analysis (C2-C3: 65-130 Hz)                     ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: statistical testers, regression analysts, forecasters │  ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 2: Data Preprocessing (C1-C2: 32-65 Hz)                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: text cleaners, embedding generators, outlier detectors│  ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                              ↕                                         ║
║  Layer 1: Empirical Data (C0-C1: 16-32 Hz)                            ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ 64 Agents: data scrapers, sensor fusion, OCR parsers, DB optimizers║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Quick Start

### Local Development

```bash
# Start local environment with Docker Compose
./deploy-chess-council.sh local

# Services available at:
# - Ollama:       http://localhost:11434
# - Qdrant:       http://localhost:6333
# - Orchestrator: http://localhost:8081
# - Agent (dev):  http://localhost:8082
# - Prometheus:   http://localhost:9090
# - Grafana:      http://localhost:3001
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes cluster
./deploy-chess-council.sh deploy

# Check status
./deploy-chess-council.sh status

# View logs from a specific agent
./deploy-chess-council.sh logs chess-board-4-27

# Scale agents (per board)
./deploy-chess-council.sh scale 128
```

## Game Types

### 1. Bibliographic Synthesis Chess

Agents compete to synthesize the best research paper from a corpus of academic papers.

**Scoring:**
- +10 points: Novel insight
- +5 points: Cross-domain link
- -5 points: Contradicted claim
- -10 points: Invalid citation

### 2. Adversarial Hypothesis Testing

Agents propose hypotheses and try to disprove each other's claims.

**Scoring:**
- +10 points: Surviving challenge
- +15 points: Falsifying opponent's hypothesis
- +20 points: Synthesizing better hypothesis

### 3. Multi-Agent Literature Review Race

Agents compete to produce the most comprehensive systematic review.

**Rules:**
- 24-hour time limit
- Must scrape Google Scholar + .gov + arXiv
- Must generate citation network graph
- Must identify research gaps

## Frequency-Tuned Communication

Each agent is assigned a frequency based on its position using the Circle of 5ths:

```python
# Agent at board B, row R, column C:
position = B * 64 + R * 8 + C
piano_key = position % 88
frequency = 440 * 2^((piano_key - 49) / 12)
```

Agents at harmonically related frequencies (perfect 5ths, 4ths, major 3rds) communicate more easily and form research coalitions.

**Example:**
- Agent A at C4 (261.63 Hz)
- Agent B at G4 (392.00 Hz) - Perfect 5th
- Agent C at E4 (329.63 Hz) - Major 3rd
- **Result:** A, B, C form triad → collaborate on synthesis

## Agent Container

Each of 640 agents runs in a containerized environment with:

- **OS:** Parrot Security / Kali Linux
- **LLM:** Qwen2.5:72b (via Ollama)
- **Tools:**
  - Terminal (bash, zsh, fish, tmux)
  - Networking (curl, nmap, wireshark)
  - Research (Jupyter, R, LaTeX)
  - Scraping (BeautifulSoup, Selenium)
  - Data Science (pandas, PyTorch, scikit-learn)
- **Streaming:** Moonlight/Sunshine (H.265, 1080p@60fps)

## API Reference

### Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/ready` | GET | Readiness check |
| `/metrics` | GET | Prometheus metrics |
| `/info` | GET | Agent information |
| `/research` | POST | Perform research on topic |
| `/game/start` | POST | Start new game |
| `/game/move` | POST | Make a move |
| `/echolocate` | POST | Find compatible agents |
| `/harmonics` | GET | Get harmonic frequencies |

### Research Request

```json
POST /research
{
  "topic": "quantum computing cryptography",
  "sources": ["arxiv", "scholar", "pubmed"],
  "max_papers": 20
}
```

### Game Start Request

```json
POST /game/start
{
  "game_type": "bibliographic_synthesis_chess",
  "opponent_id": "chess-board-6-15",
  "topic": "climate change policy"
}
```

## Training Loop

The system improves through adversarial self-play:

1. **Play Games** - Agents play bibliographic synthesis chess (24h/game)
2. **Record Moves** - Log citations, claims, refutations to PostgreSQL
3. **Evaluate** - Stockfish referee scores each move
4. **Generate Training Data** - Convert to JSONL (state, action, reward)
5. **Fine-tune** - Apply LoRA adapters to Qwen2.5 base
6. **Deploy** - Canary deployment (10% → 50% → 100%)

Training runs daily at 03:00 UTC via GitHub Actions.

## Resource Requirements

### Minimum (Development)
- 4 CPU cores
- 16 GB RAM
- 1 GPU (optional)
- 100 GB storage

### Production (640 agents)
- 80+ CPU cores
- 640+ GB RAM
- 8+ GPUs (shared via MIG/MPS)
- 10 TB storage

### Cost Estimate (Cloud)
- **Optimized:** ~$3.5K/month (spot instances, local Ollama)
- **Full Scale:** ~$22-27K/month (GPU nodes, API calls)

## Discord Integration

The Chess Council integrates with Discord for command & control:

```
!research <topic>     - Assign research topic to Layer 4 agents
!game <a> <b>         - Start chess match between agents
!replay <game_id>     - Show move-by-move analysis
!publish <game_id>    - Upload winning paper to arXiv
```

## Files Structure

```
├── chess_council_10d.yaml           # Main architecture specification
├── deploy-chess-council.sh          # Deployment script
├── generate-chess-boards.sh         # Generate K8s manifests
├── Dockerfile.chess-agent           # Agent container image
├── requirements-agent.txt           # Python dependencies
├── docker-compose.chess-council.yml # Local dev environment
├── src/
│   └── chess-agent/
│       ├── agent.py                 # Agent application
│       └── entrypoint.sh            # Container entrypoint
├── bootstrap/k8s/chess-council/
│   ├── namespace-and-config.yaml    # Namespace and ConfigMaps
│   ├── board-{0-9}-statefulset.yaml # Agent StatefulSets
│   ├── supporting-services.yaml     # Ollama, Qdrant, PostgreSQL
│   └── hpa-and-policies.yaml        # Autoscaling and network policies
├── .github/workflows/
│   ├── train-agent.yml              # Daily training workflow
│   └── build-paper.yml              # Paper compilation workflow
└── monitoring/
    └── prometheus-chess-council.yml # Prometheus config
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Something the world has never seen."*
