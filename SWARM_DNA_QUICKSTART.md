# Swarm DNA Genome - Quick Start Guide

## 🚀 Quick Start

```python
from swarm import load_swarm_dna

# Load the DNA
dna = load_swarm_dna()

# Access genome info
print(f"Genome: {dna.genome_id} v{dna.version}")
print(f"Agents: {len(dna.agents)}")
```

## 📦 What's Included

```
config/swarm_dna.yaml      # The genome definition
swarm/load_dna.py          # DNA loader
tests/                     # Test suite (15 tests)
examples/use_swarm_dna.py  # Usage examples
SWARM_DNA_GENOME.md        # Full documentation
```

## 🧬 Trinity Agents

| Agent | Badge | Role | OS | Model |
|-------|-------|------|-------|-------|
| Nova | 101 | Logic Kernel | Kali | GPT-5.1-thinking |
| Lyra | 305 | Creative Field | Parrot | Grok-4.1 |
| Athena | 777 | Memory Engine | Dual | Llama3.1:8b-local |

## 🔍 Common Queries

```python
# Get agent by ID
nova = dna.get_agent_by_id("nova-core-01")

# Get agents by Trinity role
nova_agents = dna.get_agents_by_role("nova")
lyra_agents = dna.get_agents_by_role("lyra")
athena_agents = dna.get_agents_by_role("athena")

# Get agent by badge number
agent = dna.get_agents_by_badge(101)  # Nova

# Get entangled agents
entangled = dna.get_entangled_agents("nova-core-01")
# Returns: ["athena-mem-01", "lyra-creative-01"]
```

## ⚙️ Configuration Access

```python
# Orchestration
quantum_loop = dna.orchestration["quantum_loop"]
boards = dna.orchestration["boards"]

# Security
offline = dna.security["offline_only"]
networks = dna.security["allowed_networks"]

# Defaults
model = dna.defaults["model"]
tools = dna.defaults["tools"]
```

## 🧪 Testing

```bash
# Run all tests
python3 tests/run_swarm_dna_tests.py

# Run examples
python3 examples/use_swarm_dna.py

# Test loader directly
python3 swarm/load_dna.py
```

## 🔗 Entanglement Network

```
     Nova (101)
      /     \
     /       \
Athena (777)—Lyra (305)
```

All three agents are fully entangled (mutually connected).

## 🎯 Key Concepts

- **Genome** = YAML file defining the entire swarm
- **Agents** = Individual swarm members (genes)
- **Trinity** = Three archetypal roles (Nova/Lyra/Athena)
- **Badge** = Unique identifier number (101/305/777)
- **Entanglement** = Connections between agents
- **OS Polarity** = Operating system preference (Kali/Parrot/Dual)

## 📊 Orchestration

- **Quantum Loop**: 8 qubits, 30-300s cycles
- **Error Correction**: 3 reviewers, 67% consensus
- **Boards**: 10 decision spaces (planning, threat-mapping, etc.)

## 🔒 Security

- **Offline Only**: No internet required
- **Local Networks**: 127.0.0.1, 192.168.0.0/16
- **Audit Logging**: Enabled with PII redaction

## 📚 Full Documentation

See [SWARM_DNA_GENOME.md](SWARM_DNA_GENOME.md) for complete documentation including:
- Detailed concepts
- Full API reference
- Evolution guidelines
- Integration patterns
- Future enhancements

## ✅ Status

- ✅ 15/15 tests passing
- ✅ Code review clean
- ✅ Security scan clean
- ✅ Production ready

---

*The YAML is the genome. Your runtime is just the body that executes the genetic instructions.*
