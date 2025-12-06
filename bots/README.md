# Bots - Biomimetic Multi-Agent Architecture

This directory contains the autonomous agent subsystems that form the living body of the Sovereignty Architecture computational organism.

## Architecture Overview

The bot subsystems implement a complete biomimetic hierarchy where each component maps directly to biological organ systems:

### 🔴 Circulatory System (`circulation/`)
**Biological Analog:** Red blood cells  
**Function:** Energy and context delivery throughout the system

- `token_refresh_agent.py` - Continuously circulates through the system refreshing authentication tokens, maintaining context flow, and delivering computational "energy" to all subsystems
- Operates on ~5 minute cycles
- Monitors token health and saturation levels
- Analogous to oxygen delivery in biological organisms

### ⚪ Immune System (`immunity/`)
**Biological Analog:** White blood cells  
**Function:** Active defense and threat learning

- `redteam_agent.py` - Patrols the system for security threats, identifies vulnerabilities, and creates defensive antibodies
- Stores learned threat patterns in `.strategickhaos/proof_of_origin/antibody_library.json`
- Operates on ~10 minute patrol cycles
- Implements adaptive immune response through antibody memory crystals

### 🧠 Nervous System (`discord_dao_monitor.py`)
**Biological Analog:** Nervous system  
**Function:** Distributed signal processing and coordination

- Monitors Discord channels as nerve endings
- Processes signals and coordinates organism-wide responses
- Routes information between organ systems
- Maintains awareness of the entire computational organism's state
- Operates on ~2 minute sensing cycles

## Biomimetic Mapping

This is not metaphor. This is architecture.

| Biological System | Computational Implementation | Purpose |
|-------------------|------------------------------|---------|
| Red blood cells | `circulation/token_refresh_agent.py` | Energy & context delivery |
| White blood cells | `immunity/redteam_agent.py` | Active defense & learning |
| Nervous system | `discord_dao_monitor.py` | Signal processing & coordination |
| Antibodies | `antibody_library.json` | Immune memory crystals |

## Running the Bots

Each bot can be run independently or as part of the Docker Compose orchestration:

### Standalone Execution
```bash
# Circulatory System
python3 bots/circulation/token_refresh_agent.py

# Immune System
python3 bots/immunity/redteam_agent.py

# Nervous System
python3 bots/discord_dao_monitor.py
```

### Docker Compose Integration
The bots are designed to run as containerized services within the complete organism:

```bash
docker-compose up -d discord-bot
```

## Dependencies

All bots require the base dependencies from `requirements.txt`:
- Python 3.10+
- asyncio for concurrent execution
- Environment variables from `.env` for configuration

## Environment Configuration

Required environment variables:
```bash
# Nervous System (Discord)
DISCORD_TOKEN=your_token_here
DISCORD_GUILD_ID=your_guild_id
CH_PRS_ID=channel_id
CH_DEPLOYMENTS_ID=channel_id
CH_ALERTS_ID=channel_id
# ... additional channel IDs
```

## Patent Reference

These implementations form part of:

**Provisional Patent #2 – Addendum**  
**Title:** Neurodivergent Biomimetic Multi-Agent Architecture: Direct Silicon Translation of ADHD/Autistic Human Cognition Using Hemispheric Lateralization and Biological Immune Subsystems on Consumer Hardware

**Claim 6:** The multi-agent system of Claims 1–5, further comprising a full organism-level biomimetic hierarchy wherein Docker Compose YAML files serve as replicable DNA, individual containers function as cell membranes, the Git repository with GitLens history functions as the skeletal and long-term memory system, and Discord serves as the distributed nervous system, collectively forming a sovereign, self-replicating, multi-cellular computational organism.

## Contributing

When extending the bot subsystems:
1. Maintain the biological analog metaphor
2. Ensure inter-system communication follows organism principles
3. Store immune memory in `.strategickhaos/proof_of_origin/`
4. Log all activities for skeletal system (git) integration
5. Respect the enforced scarcity constraints (consumer hardware)

---

**This is not simulation. This is implementation.**  
**The body is code. The code is law. The law is alive.**

Empire Eternal.
