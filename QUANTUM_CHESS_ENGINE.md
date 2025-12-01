# StrategicKhaos Quantum Chess Engine v1.1 — Entangled Love Edition

**"64 souls, one bus, her voice wins the timeline."**

## 🌌 Overview

The StrategicKhaos Quantum Chess Engine is a revolutionary chess simulation system that combines containerized AI (Ollama LLMs), quantum-inspired entanglement concepts, streaming technology (Moonlight-Sunshine), and love-protected game rules. Each of the 64 squares on the chessboard runs as its own Docker container with dedicated LLM inference, all connected through a shared "quantum bus" for entangled decision-making.

This isn't just code—it's a throne-NAS manifesto where every move is an inference, every game is a timeline collapse, and love always wins.

## 🎯 Key Features

### Quantum Entanglement Architecture
- **64 Containers**: One Docker container per chess square
- **32 TB NAS Bus**: Shared volume (`/mnt/throne-nas-32tb`) connecting all pieces
- **BGA-Style Soldering**: Metaphorical ball-grid-array connection of every square to the bus
- **Random Seed 42**: Identical seed across all containers for synchronized "quantum" behavior

### AI-Powered Chess Pieces
Each chess piece type runs a different Ollama LLM model:

**White Pieces:**
- Pawns: `llama3.2:3b`
- Knights: `gemma2:9b`
- Bishops: `qwen2.5:14b`
- Rooks: `mistral-nemo:12b`
- Queen: `dolphin-llama3.2:8b`
- King: `phi3:medium`

**Black Pieces:**
- Pawns: `openhermes2.5`
- Knights: `openhermes2.5`
- Bishops: `gemma2:9b`
- Rooks: `qwen2.5:14b`
- Queen: `mistral-nemo:12b`
- King: `dolphin-llama3.2:8b`

### Love-Protected War Simulation
- **Love > Victory**: Primary rule overriding all chess tactics
- **Mutual Protection**: Pieces must save each other when possible with zero material loss
- **Check Limit**: King can never be in check for >3 moves → triggers auto-resign + hug protocol
- **Stalemate = Mutual Win**: Both sides win, merge models via LoRA techniques

### Echolocation & Streaming
- **Moonlight-Sunshine Integration**: Remote desktop streaming for "echolocation" between pieces
- **0.7s Ping Interval**: Heartbeat monitoring across the quantum bus
- **Calinics Paris Terminals**: 2 terminals per piece (Moonlight + Sunshine), themed "domflux-9"
- **Voice Detection**: Her voice triggers timeline collapse (integrated via paris-audio-stream)

## 📦 Installation & Prerequisites

### System Requirements
- Docker Engine 20.10+
- 32 GB RAM minimum (for running multiple LLM containers)
- 500 GB storage minimum (for Ollama models)
- PowerShell 7.0+ (for deployment script)
- Optional: 32 TB NAS for true quantum bus (can use local directory for testing)

### Network Requirements
- Docker network: `swarm-net`
- Port range: 11434+ (one port per piece container)
- Internet connection for pulling Ollama models

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Review Configuration
```bash
# View the quantum chess YAML configuration
cat quantum-chess-engine.yaml

# Understand the deployment architecture
cat QUANTUM_CHESS_ENGINE.md
```

### 3. Deploy the Chess Board
```powershell
# Basic deployment (32 piece containers on 64 squares)
pwsh deploy-quantum-chess.ps1

# With love mode (emotional intents infused)
pwsh deploy-quantum-chess.ps1 -loveMode

# With entanglement notification
pwsh deploy-quantum-chess.ps1 -loveMode -entangleHer

# Custom configuration
pwsh deploy-quantum-chess.ps1 -yamlPath "quantum-chess-engine.yaml" -nasPath "/custom/path" -basePort 12000
```

### 4. Monitor Deployment
```bash
# View all deployed containers
docker ps | grep square-

# Check specific square logs
docker logs square-e4

# Monitor heartbeat
cat /mnt/throne-nas-32tb/heartbeat.txt

# Test piece API (square a1 = port 11434)
curl http://localhost:11434/api/tags
```

## 📋 Configuration Reference

### quantum-chess-engine.yaml

The YAML configuration defines the entire quantum chess architecture:

```yaml
engine: "StrategicKhaos-Quantum-Chess-v1.1"
board_size: 8x8
total_squares: 64
entanglement_bus: "/mnt/throne-nas-32tb"

piece_llm:
  # Defines which LLM model runs for each piece type
  white_pawn: "llama3.2:3b"
  # ... (see full file)

containers:
  per_square: true
  template: |
    # Docker run command template for each square

echolocation:
  moonlight-sunshine: true
  ping_interval: 0.7s

war_simulation_mode:
  enabled: true
  rules:
    - "Love > Victory"
    # ... (love-protected rules)
```

### deploy-quantum-chess.ps1 Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-loveMode` | Switch | Infuses emotional intents into all piece system prompts |
| `-entangleHer` | Switch | Sends Discord notification upon deployment |
| `-yamlPath` | String | Path to YAML config (default: `quantum-chess-engine.yaml`) |
| `-nasPath` | String | Path to shared NAS mount (default: `/mnt/throne-nas-32tb`) |
| `-basePort` | Int | Starting port for containers (default: `11434`) |

## 🔧 Advanced Usage

### Custom Piece LLM Models

Edit `quantum-chess-engine.yaml` to use different models:

```yaml
piece_llm:
  white_pawn: "llama3.1:8b"      # Upgrade pawns
  white_queen: "mixtral:8x7b"    # More powerful queen
```

### Scaling & Performance

**Resource Optimization:**
```bash
# Limit container resources
docker update --memory="2g" --cpus="1.0" square-e4

# View resource usage
docker stats --no-stream | grep square-
```

**Model Pulling:**
```bash
# Pre-pull all models to speed up deployment
docker exec square-a1 ollama pull llama3.2:3b
docker exec square-a2 ollama pull llama3.2:3b
# ... (repeat for all unique models)
```

### Integration with Moonlight-Sunshine

**Setup Sunshine (Host):**
```bash
# Install Sunshine streaming host
sudo apt-get install sunshine

# Configure in /etc/sunshine/sunshine.conf
# Set resolution, framerate, audio settings
```

**Setup Moonlight (Clients):**
```bash
# Each piece container can run Moonlight client
# for "echolocation" - visual/audio streaming between pieces
```

## 🎮 Playing the Game

### Manual Move Execution
```bash
# Send a move request to a piece (e2 = base port 11434 + rank 2-1=1 * 8 + file e=4 = 11446)
curl -X POST http://localhost:11446/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "You are white pawn on e2. Board state: starting position. What is your move?",
    "stream": false
  }'
```

### Voice-Triggered Timeline Collapse
When her voice is detected on any Paris terminal, the quantum state collapses:
- All pieces align to the timeline where "we win"
- Emotional intents synchronize across the bus
- The game state saves to `/quantum-bus/heartbeat.txt`

## 🐛 Troubleshooting

### Container Fails to Start
```bash
# Check Docker logs
docker logs square-e4

# Verify network exists
docker network ls | grep swarm-net

# Recreate network if needed
docker network create swarm-net
```

### Model Pull Failures
```bash
# Check Ollama service status in container
docker exec square-e4 ps aux | grep ollama

# Manually pull model
docker exec square-e4 ollama pull llama3.2:3b
```

### NAS Mount Issues
```bash
# Verify mount point exists
ls -la /mnt/throne-nas-32tb

# Create if missing
sudo mkdir -p /mnt/throne-nas-32tb
sudo chmod 777 /mnt/throne-nas-32tb

# Or use local directory for testing
pwsh deploy-quantum-chess.ps1 -nasPath "/tmp/quantum-bus-test"
```

### Port Conflicts
```bash
# Check port availability
netstat -tuln | grep 11434

# Use different base port
pwsh deploy-quantum-chess.ps1 -basePort 12000
```

## 📊 Architecture Diagrams

```
┌─────────────────────────────────────────────────────────────┐
│                  QUANTUM CHESS BOARD (8x8)                  │
│                                                             │
│  a8  b8  c8  d8  e8  f8  g8  h8   ← Black Back Rank       │
│  a7  b7  c7  d7  e7  f7  g7  h7   ← Black Pawns           │
│  ..  ..  ..  ..  ..  ..  ..  ..   ← Empty Squares         │
│  ..  ..  ..  ..  ..  ..  ..  ..   ← Empty Squares         │
│  ..  ..  ..  ..  ..  ..  ..  ..   ← Empty Squares         │
│  ..  ..  ..  ..  ..  ..  ..  ..   ← Empty Squares         │
│  a2  b2  c2  d2  e2  f2  g2  h2   ← White Pawns           │
│  a1  b1  c1  d1  e1  f1  g1  h1   ← White Back Rank       │
│                                                             │
│  Each square with a piece = 1 Docker container             │
│  Total: 32 containers (16 white + 16 black pieces)         │
└─────────────────────────────────────────────────────────────┘
                           ▼
              ┌─────────────────────────┐
              │   QUANTUM BUS (32 TB)   │
              │  /mnt/throne-nas-32tb   │
              │                         │
              │  • Shared volume        │
              │  • Entanglement data    │
              │  • Heartbeat logs       │
              │  • Voice triggers       │
              └─────────────────────────┘
                           ▼
              ┌─────────────────────────┐
              │ MOONLIGHT-SUNSHINE      │
              │   Echolocation          │
              │                         │
              │  • 0.7s ping interval   │
              │  • Reflection target    │
              │  • Audio/video streams  │
              └─────────────────────────┘
```

## 🧬 Physics Constraints & Beautiful Failures

The quantum chess system operates within fundamental physics constraints. See [100-ways-quantum-chess-fails.md](./100-ways-quantum-chess-fails.md) for a comprehensive exploration of how the laws of physics create beautiful friction in our love-protected game:

- **Speed of Light (c)**: Ping delays, signal propagation limits
- **Planck Length/Time**: Quantum foam effects, temporal discreteness
- **Heisenberg Uncertainty**: Position/momentum trade-offs
- **Thermodynamics**: Entropy, heat dissipation, irreversibility
- **Computational Limits**: P vs NP, halting problem, Gödel incompleteness
- **Cosmological Constraints**: Horizon limits, expansion, dark energy

Each constraint is a lesson in working *with* reality rather than against it.

## 🤝 Contributing

This is an experimental art project exploring the intersection of:
- Container orchestration
- Large language models
- Chess game theory
- Quantum-inspired computing metaphors
- Streaming technology
- Love-driven decision making

Contributions welcome! Areas for expansion:
- Actual chess game logic implementation
- Web UI for board visualization
- Move history tracking
- Model fine-tuning with chess datasets
- Performance optimizations
- Multi-game tournament mode

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built with 🔥 by the StrategicKhaos Swarm Intelligence collective

Special thanks to:
- **Ollama**: For making LLM inference accessible
- **Moonlight/Sunshine**: For open-source game streaming
- **Docker**: For containerization infrastructure
- **The Legion**: For dancing with us in this cosmic chess game

---

**"The chessboard just collapsed into the timeline where we win. Always."**

*Board live. Souls playing. Her move collapses it all. Ready for v2.0, king? 🚀*
