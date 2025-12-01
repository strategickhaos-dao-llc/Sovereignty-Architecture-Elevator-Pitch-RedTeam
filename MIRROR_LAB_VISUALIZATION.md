# 🔬 MIRROR LAB - Real-Time Research Visualization

**DOM. NOW YOU CAN WATCH THE AGENTS WORK.**

Moonlight/Sunshine streams their terminals. OBS shows the network graph. Quantum sims run in real-time on your screens.

---

## 🖥️ WHAT YOU GET

**7 screens showing:**

| Screen | Name | Description | URL |
|--------|------|-------------|-----|
| 1 | 🎯 **Mission Control** | Progress bars for all 10 departments | `http://localhost:3001` |
| 2 | 🤖 **Agent Grid** | 80 agents visible, click any to watch their screen | `http://localhost:3002` |
| 3 | 🧬 **Molecular Viewer** | 3D proteins rotating, drugs docking | `http://localhost:3003` |
| 4 | 💻 **Live Terminal** | Agent typing commands, downloading papers | `http://localhost:7681` |
| 5 | 📊 **Progress Graphs** | Papers analyzed, drugs found, costs estimated | `http://localhost:3005` |
| 6 | 🔬 **Discovery Feed** | Real-time log of breakthroughs | `http://localhost:3006` |
| 7 | ⚛️ **Quantum Sim** | Actual quantum circuit solving her protein structure | `http://localhost:3007` |

---

## 🚀 QUICK START

### Option 1: Full Mirror Lab

```bash
# Start everything
./start-mirror-lab.sh start

# Or with custom settings
SUNSHINE_USER=dom SUNSHINE_PASS=your_pass ./start-mirror-lab.sh start
```

### Option 2: Visualization Only

```bash
# Just the dashboards, no streaming infrastructure
./start-mirror-lab.sh show-me
```

### Option 3: Quantum Only

```bash
# Just quantum simulation
./start-mirror-lab.sh quantum
```

---

## 🎮 STREAMING WITH MOONLIGHT/SUNSHINE

The Mirror Lab uses [Sunshine](https://github.com/LizardByte/Sunshine) for game streaming, compatible with [Moonlight](https://moonlight-stream.org/).

### Setup Moonlight Client

1. Install Moonlight on your viewing device (phone, tablet, another PC)
2. Open Moonlight and add host: `your-server-ip`
3. Pair with the code shown in Sunshine Web UI
4. Connect and watch agents work!

### Sunshine Configuration

Access the Sunshine Web UI at `http://localhost:47990`

Default credentials:
- Username: `dom` (or set via `SUNSHINE_USER`)
- Password: Set via `SUNSHINE_PASS`

---

## 🖥️ THE 7 SCREENS

### Screen 1: Mission Control 🎯

**Real-time progress tracking for all 10 research departments:**

- 📚 Literature Review
- 💊 Drug Discovery
- 🧬 Molecular Modeling
- ⚛️ Quantum Computing
- 🏥 Clinical Analysis
- 💰 Cost Estimation
- 🛡️ Safety Analysis
- 📋 Regulatory Pathway
- 📊 Data Synthesis
- 📝 Report Generation

**Features:**
- LCD-style progress bars
- Active agent count
- Papers analyzed counter
- Drugs identified counter
- Real-time activity graphs

### Screen 2: Agent Grid 🤖

**80 agents in an 8x10 grid. Click any agent to watch their work.**

**What you see:**
- Agent name and department
- Current task
- Activity status (working/idle)
- Performance metrics

**Click an agent to:**
- See their live terminal output
- Watch them scrape papers
- Observe them run simulations

### Screen 3: Molecular Viewer 🧬

**3D visualization powered by Mol* Viewer**

**Capabilities:**
- Protein structure rotation
- Drug docking visualization
- Binding site highlighting
- Electron density maps

### Screen 4: Live Terminal 💻

**Watch agents type commands in real-time**

**What you'll see:**
```
Agent D4: Scraping PubMed for "NMDA receptor chronic pain"
Agent F6: Running AlphaFold3 prediction...
Agent Q2: Submitting quantum circuit to IBM backend...
```

### Screen 5: Progress Graphs 📊

**Grafana dashboards showing:**

- Papers analyzed over time (by source: PubMed, arXiv, bioRxiv)
- Drugs found by category (repurposing, novel, combination)
- Compute cost tracking ($0-4K/month budget)
- Quantum simulation progress

### Screen 6: Discovery Feed 🔬

**Real-time breakthrough notifications:**

```
🌟 BREAKTHROUGH: Combination therapy protocol identified with 3x efficacy
💊 DRUG CANDIDATE: Memantine repurposing candidate identified
⚛️ QUANTUM RESULT: Binding energy converged: -42.3 kcal/mol
🧬 PROTEIN STRUCTURE: AlphaFold3 prediction complete at 1.2Å resolution
```

### Screen 7: Quantum Sim ⚛️

**Actual quantum circuits running VQE for binding energy calculation**

**Features:**
- Real-time convergence plot
- Circuit visualization
- Qubit count and depth
- Energy vs. iteration graph

**Backends supported:**
- Local (Qiskit Aer simulator) - Free
- IBM Quantum - Free tier available
- Azure Quantum - Credit-based

---

## 💰 COST

| Component | Monthly Cost |
|-----------|--------------|
| Compute (agents) | $0-3,500 |
| Streaming (Moonlight/Sunshine) | $0 (free) |
| Quantum (IBM free tier) | $0 |
| Quantum (Azure credits) | $0-500 |
| **TOTAL** | **$0-4,000/month max** |

---

## ⚛️ QUANTUM COMPUTING SETUP

### IBM Quantum (Free Tier)

1. Create account at [quantum-computing.ibm.com](https://quantum-computing.ibm.com)
2. Get your API token from account settings
3. Set environment variable:
   ```bash
   export IBM_QUANTUM_TOKEN="your_token_here"
   ```

### Azure Quantum

1. Create Azure account with Quantum credits
2. Set environment variables:
   ```bash
   export AZURE_QUANTUM_WORKSPACE="your-workspace"
   export AZURE_QUANTUM_RESOURCE_GROUP="your-rg"
   export AZURE_QUANTUM_SUBSCRIPTION="your-subscription-id"
   ```

---

## 🛠️ COMMANDS

```bash
./start-mirror-lab.sh start      # Start all services
./start-mirror-lab.sh stop       # Stop all services
./start-mirror-lab.sh status     # Show service status
./start-mirror-lab.sh logs       # Tail all logs
./start-mirror-lab.sh quantum    # Start quantum sim only
./start-mirror-lab.sh show-me    # Start visualization only
./start-mirror-lab.sh urls       # Show all URLs
./start-mirror-lab.sh help       # Show help
```

---

## 🔧 CONFIGURATION

### Environment Variables

```bash
# Streaming
SUNSHINE_USER=dom
SUNSHINE_PASS=your_secure_password

# Dashboards  
GRAFANA_PASSWORD=your_grafana_password

# Quantum
IBM_QUANTUM_TOKEN=your_ibm_token
QUANTUM_MODE=local  # local|ibm|azure

# Azure Quantum (optional)
AZURE_QUANTUM_WORKSPACE=your-workspace
AZURE_QUANTUM_RESOURCE_GROUP=your-rg
AZURE_QUANTUM_SUBSCRIPTION=your-subscription
```

### Docker Compose Override

Create `docker-compose.mirror-lab.override.yml` for custom settings:

```yaml
services:
  quantum-sim:
    environment:
      SIMULATION_MODE: ibm
      IBM_QUANTUM_TOKEN: ${IBM_QUANTUM_TOKEN}
```

---

## 🔌 ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    MIRROR LAB                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐    │
│  │ Screen 1│   │ Screen 2│   │ Screen 3│   │ Screen 4│    │
│  │ Mission │   │  Agent  │   │Molecular│   │  Live   │    │
│  │ Control │   │  Grid   │   │ Viewer  │   │Terminal │    │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘    │
│       │             │             │             │          │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                  │
│  │ Screen 5│   │ Screen 6│   │ Screen 7│                  │
│  │Progress │   │Discovery│   │ Quantum │                  │
│  │ Graphs  │   │  Feed   │   │   Sim   │                  │
│  └────┬────┘   └────┬────┘   └────┬────┘                  │
│       │             │             │                        │
│       └─────────────┼─────────────┘                        │
│                     │                                      │
│              ┌──────┴──────┐                               │
│              │    Redis    │ (pub/sub)                     │
│              └──────┬──────┘                               │
│                     │                                      │
│              ┌──────┴──────┐                               │
│              │  Sunshine   │ → Moonlight Clients           │
│              │  Streaming  │                               │
│              └─────────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 WHY THIS MATTERS

**You're not just waiting for results.**

**You're WATCHING:**
- Agent D4 scrape PubMed for "NMDA receptor chronic pain"
- Agent F6 run AlphaFold3 on her disease protein
- Quantum computer converge on binding energy
- Discovery log say: "Memantine repurposing candidate identified"

**And you KNOW it's real because you SAW it happen.**

---

## 🚦 WHEN YOU'RE READY

Just say:
- **"START"** → Activate Primary + Mirror Labs
- **"SHOW ME"** → Deploy just the visualization layer first
- **"QUANTUM"** → Set up quantum computing access

---

**For her. Always.** 🟠🧬∞

---

## 📚 Related Documentation

- [Main README](README.md) - Sovereignty Architecture Overview
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [Docker Compose Reference](docker-compose.mirror-lab.yml) - Full service definitions

---

*Built with love by the Strategickhaos Swarm Intelligence collective*
