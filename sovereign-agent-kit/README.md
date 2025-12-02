# Sovereign Agent Kit - Quantum Swarm Intelligence

**Transform your Obsidian vault into a living quantum processor made of LLMs and markdown.**

This is the actual implementation of the quantum chip methodology described in [QUANTUM_METHODOLOGY.md](../QUANTUM_METHODOLOGY.md).

## 🎯 What Is This?

The Sovereign Agent Kit turns multiple LLM instances into a coherent quantum-like processor where:
- Each agent is a **qubit**
- Your Obsidian vault is the **quantum register**
- Wikilinks are **entangling gates**
- Multi-agent consensus is **error correction**
- The whole system operates **100% sovereignly**

## 🚀 Quick Start

```bash
# Launch 16-qubit swarm with Claude
./launch_quantum_swarm.sh --qubits 16 --model claude-3-opus

# Or use local models with Ollama
./launch_quantum_swarm.sh --qubits 32 --model llama3.1:70b --local

# Check status
./quantum_status.sh

# Recenter when needed (every 24-72h)
./quantum_recenter.sh

# Graceful shutdown
./quantum_shutdown.sh
```

## 📁 Directory Structure

```
sovereign-agent-kit/
├── swarm/
│   ├── __init__.py
│   ├── quantum_loop.py        # Core agent loop
│   └── consensus.py            # Error correction
├── config/
│   └── quantum_swarm_config.yaml
├── dashboard/
│   └── quantum_viz.py          # (Future: real-time visualization)
├── launch_quantum_swarm.sh     # Launch the swarm
├── quantum_status.sh           # Check swarm health
├── quantum_shutdown.sh         # Stop the swarm
├── quantum_recenter.sh         # Reset coherence
└── README.md                   # This file
```

## 🔧 Configuration

Edit `config/quantum_swarm_config.yaml` to customize:

```yaml
swarm:
  qubits: 16                    # Number of agents
  model: "claude-3-opus"        # LLM model
  coherence_time: 72            # Hours before recenter

quantum_loop:
  think_temperature: 0.7        # Exploration level
  consensus_threshold: 0.66     # 2/3 agreement
  sleep_min: 30                 # Seconds
  sleep_max: 300

obsidian:
  vault_path: "./obsidian_vault"
  auto_commit: true
  link_format: "wikilink"
```

## 📊 Monitoring

### Status Command
```bash
./quantum_status.sh
```

Shows:
- Active qubits vs total
- Quantum register size (notes, links)
- Gate fidelity (consensus rate)
- Recent activity

### Watch Logs
```bash
tail -f logs/qubit_*.log
```

### Watch Vault Growth
```bash
watch -n 5 'find obsidian_vault -name "*.md" | wc -l'
```

## 🎛️ Advanced Usage

### Using Different Models

**Claude:**
```bash
export ANTHROPIC_API_KEY="your-key"
./launch_quantum_swarm.sh --qubits 16 --model claude-3-opus
```

**GPT-4:**
```bash
export OPENAI_API_KEY="your-key"
./launch_quantum_swarm.sh --qubits 16 --model gpt-4-turbo-preview
```

**Grok:**
```bash
export XAI_API_KEY="your-key"
./launch_quantum_swarm.sh --qubits 16 --model grok-4-fast-reasoning
```

**Local Ollama:**
```bash
# Ensure Ollama is running
ollama pull llama3.1:70b
./launch_quantum_swarm.sh --qubits 32 --model llama3.1:70b --local
```

### Air-Gapped Operation

For maximum sovereignty:

```yaml
# In config/quantum_swarm_config.yaml
swarm:
  local_only: true

security:
  air_gapped: true              # No internet after setup
  encrypt_state: true
```

### Discord Integration

Stream quantum operations to Discord:

```yaml
discord:
  enabled: true
  webhook_url: "https://discord.com/api/webhooks/..."
  channels:
    quantum: "#quantum-channel"
    alerts: "#quantum-alerts"
```

## 🔬 Understanding the Quantum Loop

Each agent runs this loop indefinitely:

```python
while True:
    # 1. SUPERPOSITION: Generate multiple possible plans
    plan = agent.think("What should the swarm do next?")
    
    # 2. CONTROL PULSE: Execute tools
    results = agent.use_tools(plan)
    
    # 3. ENTANGLING GATE: Write note with [[links]]
    note = agent.write_to_obsidian(results)
    
    # 4. MEASUREMENT: Commit to git
    agent.obsidian_commit(f"quantum step: {note}")
    
    # 5. ERROR CORRECTION: Check consensus
    if not consensus_reached(note):
        agent.replan_and_fix()
    
    # 6. COHERENCE: Sleep 30-300 seconds
    time.sleep(random.uniform(30, 300))
```

## 📈 Success Metrics

Your quantum swarm is working when:

- ✅ **Gate Fidelity >95%**: High consensus agreement
- ✅ **Entangling Rate >1000/day**: Rich interconnected knowledge
- ✅ **Coherence >24h**: Stays aligned without intervention
- ✅ **Zero Hallucinations**: All claims backed by sources
- ✅ **Autonomous Growth**: Vault grows without human input

## 🛠️ Development

### Running Tests

```bash
# Test quantum loop
python3 -m swarm.quantum_loop

# Test consensus
python3 -m swarm.consensus
```

### Extending the System

Add new tools in `swarm/quantum_loop.py`:

```python
class QuantumAgent:
    def use_tools(self, plan):
        # Add your custom tools here
        results["custom_tool"] = my_custom_tool()
        return results
```

## 🎪 Philosophy

This isn't a metaphor. This is the **actual methodology** that quantum computers use, translated to sovereign LLM infrastructure:

| Quantum Computer | Sovereign Swarm |
|------------------|-----------------|
| Qubits in superposition | LLMs with multiple hypotheses |
| Entangling gates | [[Wikilinks]] between notes |
| Quantum register | Obsidian vault |
| Measurement | Query/commit operations |
| Error correction | Multi-agent consensus |
| Coherence time | Alignment duration |

## 📚 Further Reading

- [QUANTUM_METHODOLOGY.md](../QUANTUM_METHODOLOGY.md) - Complete theoretical framework
- [Obsidian.md](https://obsidian.md) - The knowledge base platform
- [Constitutional AI](https://www.anthropic.com/constitutional-ai) - Alignment methodology

## 🆘 Troubleshooting

### Agents not starting
```bash
# Check Python environment
python3 --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt
```

### Low gate fidelity
```bash
# Recenter the swarm
./quantum_recenter.sh

# Adjust consensus threshold in config
# Lower threshold = more tolerant
```

### High memory usage
```bash
# Reduce number of qubits
./launch_quantum_swarm.sh --qubits 8

# Or limit vault size in config
performance:
  max_vault_size_gb: 5
```

## 📄 License

MIT License - See [LICENSE](../LICENSE)

## 🎯 Support

- **Documentation**: [Full methodology](../QUANTUM_METHODOLOGY.md)
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Community**: [Discord](https://discord.gg/strategickhaos)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Your agents aren't simulating quantum mechanics. They ARE quantum mechanics, in information space."*

⚛️🧠❤️
