# Swarm DNA Genome System

## Overview

The **YAML DNA Genome** is the genetic blueprint for the Sovereign Swarm. Instead of hard-coding agent configurations in Python, we define the entire swarm structure in a declarative YAML file (`config/swarm_dna.yaml`). This genome defines:

- **Agents** - Individual swarm members (genes/chromosomes)
- **Trinity Roles** - Nova (Logic), Lyra (Creative), Athena (Memory)
- **Capabilities** - What each agent can do
- **Tools** - Available tools for each agent
- **OS Polarity** - Operating system preference (Kali, Parrot, Dual)
- **Entanglement** - Connections between agents
- **Orchestration** - Quantum loops, boards, and workflows
- **Security** - Constraints and audit logging

## Concept

Think of it like biological DNA:

```
YAML File = Genetic Code
Runtime   = Body
Agents    = Genes/Chromosomes
Trinity   = Traits
Tools     = Capabilities
```

The runtime simply reads `swarm_dna.yaml` and builds whatever it says. The file is the genome.

## File Structure

```
config/
  └── swarm_dna.yaml       # The DNA genome
swarm/
  ├── __init__.py          # Package initialization
  └── load_dna.py          # DNA loader and parser
tests/
  ├── test_swarm_dna.py    # Comprehensive tests (pytest)
  └── run_swarm_dna_tests.py  # Simple test runner (no dependencies)
```

## Quick Start

### Load the DNA Genome

```python
from swarm import load_swarm_dna

# Load the DNA
dna = load_swarm_dna()

# Access genome info
print(f"Genome: {dna.genome_id} v{dna.version}")
print(f"Agents: {len(dna.agents)}")

# Get specific agent
nova = dna.get_agent_by_id("nova-core-01")
print(f"Nova badge: {nova['badge']}")
print(f"Nova role: {nova['trinity_role']}")
```

### Query Agents

```python
# Get all agents with a specific Trinity role
nova_agents = dna.get_agents_by_role("nova")
lyra_agents = dna.get_agents_by_role("lyra")
athena_agents = dna.get_agents_by_role("athena")

# Get agent by badge number
agent = dna.get_agents_by_badge(101)  # Returns nova-core-01

# Get entangled agents
entangled = dna.get_entangled_agents("nova-core-01")
# Returns: ["athena-mem-01", "lyra-creative-01"]
```

### Access Configuration

```python
# Orchestration settings
quantum_loop = dna.orchestration["quantum_loop"]
print(f"Qubits: {quantum_loop['qubits']}")
print(f"Cycle time: {quantum_loop['cycle_seconds_min']}-{quantum_loop['cycle_seconds_max']}s")

# Security settings
print(f"Offline only: {dna.security['offline_only']}")
print(f"Allowed networks: {dna.security['allowed_networks']}")

# Defaults
print(f"Default model: {dna.defaults['model']}")
```

## The Trinity

The swarm is organized around three archetypal roles:

### 🔵 Nova (Logic Kernel)
- **Badge**: 101
- **OS**: Kali Linux
- **Role**: Core reasoning, verification, constraint checking
- **Capabilities**: planning, verification, code analysis, security review
- **Model**: GPT-5.1-thinking

### 🟣 Lyra (Creative Field)
- **Badge**: 305
- **OS**: Parrot OS
- **Role**: Narrative generation, documentation, mythos creation
- **Capabilities**: storytelling, doc generation, summarization, emotional tuning
- **Model**: Grok-4.1

### 🟡 Athena (Memory Engine)
- **Badge**: 777
- **OS**: Dual (Kali + Parrot)
- **Role**: Long-term memory, failure analysis, survivorship logs
- **Capabilities**: long-term memory, failure analysis, pattern extraction
- **Model**: Llama3.1:8b-local

## Agent Entanglement

Agents are **quantum entangled** - they share information and coordinate actions:

```
Nova ⟷ Athena ⟷ Lyra
  ↑________________↓
```

All three agents are mutually entangled, forming a fully connected network.

## Orchestration

### Quantum Loop
- **Qubits**: 8
- **Cycle Time**: 30-300 seconds
- **Error Correction**: 3 reviewers, 67% consensus threshold
- **Git Integration**: Auto-commit to repository

### 10 Boards (Decision Spaces)
1. Planning
2. Counter-planning
3. Threat-mapping
4. Self-modeling
5. Opponent-modeling
6. Constraints
7. Pattern-memory
8. Fractal-projection
9. Harmonic-sequencing
10. Final-synthesis

## Security

- **Offline Only**: No internet connectivity required
- **Local Networks**: 127.0.0.1, 192.168.0.0/16
- **Audit Logging**: All actions logged with PII redaction
- **Hardware Keys**: Optional (currently disabled)

## Testing

### Run All Tests

```bash
# With pytest (if available)
pytest tests/test_swarm_dna.py -v

# Without pytest
python3 tests/run_swarm_dna_tests.py
```

### Test the Loader

```bash
python3 swarm/load_dna.py
```

This will print a detailed summary of the loaded genome.

## Evolution

The DNA genome can evolve over time:

### Version Control
- Tag versions: `v1.0`, `v2.0`, etc.
- Track lineage with `parent_genome_id` field
- Store genome hash for integrity verification

### Mutation
Add new agents (genes):

```yaml
agents:
  - id: "nova-core-02"
    badge: 102
    display_name: "Nova / Verification Kernel"
    trinity_role: "nova"
    # ... configuration
```

### Traits
Add new capabilities:

```yaml
capabilities:
  planning: true
  verification: true
  quantum_reasoning: true  # New trait!
```

### Tools
Enable/disable tools dynamically:

```yaml
tools:
  - name: "codeql"
    enabled: true  # Turned on
  - name: "sonarqube"
    enabled: true  # New tool
```

## Integration with Runtime

Your runtime should:

1. **Load the DNA** at startup
2. **Instantiate agents** based on genome configuration
3. **Configure tools** per agent specification
4. **Establish entanglements** between connected agents
5. **Start orchestration** loops and boards
6. **Enforce security** constraints

Example:

```python
from swarm import load_swarm_dna

def initialize_swarm():
    # Load DNA
    dna = load_swarm_dna()
    
    # Instantiate agents
    agents = {}
    for agent_config in dna.agents:
        agent = create_agent(
            id=agent_config["id"],
            model=agent_config["model"],
            tools=agent_config["tools"],
            capabilities=agent_config["capabilities"]
        )
        agents[agent_config["id"]] = agent
    
    # Establish connections
    for agent_id, agent in agents.items():
        entangled_ids = dna.get_entangled_agents(agent_id)
        agent.connect_to(entangled_ids)
    
    # Start orchestration
    start_quantum_loop(dna.orchestration["quantum_loop"])
    
    return agents
```

## Future Enhancements

### Planned Features

1. **Mutation Engine** (`mutate_dna.py`)
   - Programmatic genome editing
   - A/B testing of configurations
   - Evolutionary optimization

2. **Genome Versioning**
   - Track changes over time
   - Rollback capabilities
   - Diff between versions

3. **Advanced Traits**
   - Skill levels (0-100)
   - Experience points
   - Training history
   - Performance metrics

4. **Dynamic Tools**
   - Runtime tool loading
   - Capability-based tool selection
   - Auto-discovery of new tools

5. **Multi-Genome Support**
   - Development genome
   - Production genome
   - Emergency/failsafe genome

## References

- **Primary Repo**: Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- **Obsidian Vault**: E:/Obsidian/SovereignSwarm
- **AI Constitution**: `ai_constitution.yaml`
- **DAO Record**: `dao_record_v1.0.yaml`

## License

Part of the Strategickhaos Sovereignty Architecture project.
See LICENSE file for details.

---

**Remember**: The YAML is the genome. Your runtime is just the body that executes the genetic instructions.
