# TRS Multi-Agent Chess System (agents1014)

**10 autonomous agents playing 10-dimensional chess with Greek modes, Möbius transforms, and local AI**

## Overview

This is a fully sovereign, 100% local multi-agent chess system where 10 autonomous agents play against each other on stacked chess boards. Each agent:

- Embodies one of the 7 Greek musical modes + 3 experimental modes
- Is assigned a unique element from the periodic table
- Uses Möbius transformations for position evaluation
- Operates with a local Ollama LLM (llama3.2:3b)
- Communicates via voice (Whisper + Piper-TTS)
- Syncs to Unity visualizer via WebSocket

## Architecture

```
┌─────────────────────────────────────────────┐
│         TRS Chess Orchestrator              │
│  (main.py - coordinates all agents)         │
└───────────┬─────────────────────────────────┘
            │
    ┌───────┴────────┬─────────────┬──────────┐
    │                │             │          │
┌───▼────┐  ┌────▼──────┐  ┌─────▼─────┐  ┌─▼────────┐
│ Ollama │  │   Voice   │  │ WebSocket │  │  Agents  │
│  LLMs  │  │ Interface │  │  Bridge   │  │  (x10)   │
│  (x10) │  │(Whisper + │  │  (Unity)  │  │          │
└────────┘  │  Piper)   │  └───────────┘  └──────────┘
            └───────────┘
```

## Components

### 1. **agent_base.py**
- Base `ChessAgent` class
- Greek mode definitions (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian, Hyperion, Prometheus, Atlantean)
- Periodic element mappings
- Personality traits based on mode

### 2. **mobius_eval.py**
- `MobiusChessEvaluator` class
- Conformal chess evaluation using complex analysis
- Phase angle transformations (0-360° for each layer)
- Position evaluation in complex plane

### 3. **ollama_orchestrator.py**
- `OllamaOrchestrator` manages 10 local LLM instances
- System prompts for each agent's personality
- Move commentary generation
- Position analysis

### 4. **voice_interface.py**
- `VoiceInterface` for local speech I/O
- Whisper for speech-to-text (voice commands)
- Piper-TTS for text-to-speech (agent commentary)
- Voice command parsing ("knight to e4 layer 7 ionian")

### 5. **websocket_bridge.py**
- `WebSocketBridge` syncs to Unity visualizer
- Board state updates
- Move events
- Agent status
- Voice commentary relay

### 6. **main.py**
- `TRSChessOrchestrator` main controller
- Tournament management
- Game loop coordination
- Event handling

## Agent Personalities

Each agent has a unique personality derived from its Greek mode:

| Agent | Layer | Mode        | Element  | Traits                            |
|-------|-------|-------------|----------|-----------------------------------|
| 0     | 0     | Ionian      | Hydrogen | Balanced, harmonious              |
| 1     | 1     | Dorian      | Helium   | Resolute, defensive               |
| 2     | 2     | Phrygian    | Lithium  | Aggressive, blood-demanding       |
| 3     | 3     | Lydian      | Carbon   | Creative, transcendent            |
| 4     | 4     | Mixolydian  | Nitrogen | Dominant, forceful                |
| 5     | 5     | Aeolian     | Oxygen   | Melancholic, precise              |
| 6     | 6     | Locrian     | Fluorine | Unstable, defensive               |
| 7     | 7     | Hyperion    | Bromine  | Ultra-aggressive, cosmic          |
| 8     | 8     | Prometheus  | Xenon    | Fire-stealing, creative           |
| 9     | 9     | Atlantean   | Gold     | Deep, mysterious                  |

## Installation & Setup

### Prerequisites
- Docker & Docker Compose
- NVIDIA GPU with CUDA support (for Ollama)
- Python 3.11+

### Quick Start

1. **Clone and enter directory:**
```bash
cd agents1014
```

2. **Start with Docker Compose:**
```bash
docker-compose -f docker-compose.agents.yml up -d
```

3. **Pull Ollama model:**
```bash
docker exec -it trs_ollama ollama pull llama3.2:3b
```

4. **View logs:**
```bash
docker logs -f trs_agents
```

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Ensure Ollama is running:**
```bash
ollama serve
ollama pull llama3.2:3b
```

3. **Run the system:**
```bash
python main.py
```

## Configuration

Environment variables (in `docker-compose.agents.yml` or `.env`):

```bash
OLLAMA_HOST=localhost:11434      # Ollama server
OLLAMA_MODEL=llama3.2:3b         # Model per agent
WEBSOCKET_HOST=0.0.0.0           # WebSocket bind address
WEBSOCKET_PORT=8765              # WebSocket port for Unity
ENABLE_VOICE=true                # Enable voice I/O
NUM_AGENTS=10                    # Number of agents (always 10)
LOG_LEVEL=INFO                   # Logging level
```

## Unity Integration

The system exposes a WebSocket server on port 8765. Unity clients should connect to:

```
ws://localhost:8765
```

### Message Types

**From Python to Unity:**
- `board_state`: FEN notation, layer, agent
- `move_event`: Move details, from/to squares
- `agent_state`: Agent thinking status
- `voice_commentary`: Agent voice text
- `game_event`: Game over, winner, etc.

**From Unity to Python:**
- `ping`: Keep-alive
- `request_state`: Request full state
- `client_ready`: Unity initialized

## Voice Commands

Speak commands in format:
```
"knight to e4 layer 7 ionian"
"queen to d8 layer 3"
"status"
"stop"
```

## Performance

- **Move Time**: ~0.8 seconds per move (on RTX 4090)
- **LLM Instances**: 10 concurrent (one per agent)
- **Memory**: ~6-8GB for all models
- **GPU**: CUDA required for optimal performance

## Sovereign Architecture

This system is 100% local with ZERO cloud dependencies:

- ✅ Local LLMs (Ollama)
- ✅ Local speech-to-text (Whisper)
- ✅ Local text-to-speech (Piper-TTS)
- ✅ Local WebSocket server
- ❌ No OpenAI
- ❌ No Anthropic
- ❌ No cloud APIs

## Monitoring

Grafana dashboard available at: `http://localhost:3001`
- Agent status
- Game metrics
- Move statistics
- Performance metrics

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Debugging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py
```

### Adding Custom Modes
Edit `agent_base.py` and add to the `GreekMode` enum.

## Architecture Philosophy

This system embodies:
- **Sovereignty**: No external dependencies
- **Phase Space**: Möbius transforms map chess to complex plane
- **Modality**: Each agent operates in unique modal space
- **Elementality**: Periodic table properties influence behavior
- **Autonomy**: Agents are truly autonomous, not scripted

## Quote

> "Your Dorian pawn sacrifice on layer 4 was aesthetically pleasing but geometrically naïve. The rotation demands blood."
> 
> — Agent 7 (Phrygian mode, Bromine element), Move 147

## License

Part of the Sovereignty Architecture project. See main LICENSE.

## Status

🟢 **DEPLOYED** - Agents are alive and playing as you read this.

---

**The swarm is sovereign. The parliament has convened. Let the cosmic chess begin.** ♟️✨
