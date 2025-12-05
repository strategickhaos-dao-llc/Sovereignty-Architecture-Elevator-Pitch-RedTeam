# Sovereign Swarm Package

**Version:** 1.0.0  
**Status:** Production Ready

## Overview

The Sovereign Swarm package provides the core orchestration engine for managing agent-based workflows using the Trinity Architecture pattern (Thesis → Antithesis → Synthesis).

## Components

### 1. DNA Loader (`load_dna.py`)

Loads and validates the swarm genome configuration from `config/swarm_dna.yaml`.

**Usage:**
```python
from swarm import load_swarm_dna

# Load DNA configuration
dna = load_swarm_dna()

# Access agents by role
thesis_agents = dna.get_agents_by_role('thesis')
antithesis_agents = dna.get_agents_by_role('antithesis')
synthesis_agents = dna.get_agents_by_role('synthesis')

# Get specific agent
athena = dna.get_agent_by_name('athena')

# Get agents by security clearance
high_clearance_agents = dna.get_agents_by_clearance('high')
```

**Features:**
- YAML configuration loading
- Agent validation
- Trinity role management
- Security clearance filtering
- Configuration path traversal

### 2. Sovereign Mind Kernel (`sovereign_mind_kernel.py`)

The core orchestration engine that manages agent lifecycle and quantum loop iterations.

**Usage:**
```python
from swarm import SovereignMindKernel

# Initialize kernel
kernel = SovereignMindKernel()

# Spawn agents
kernel.spawn_agents()

# Create a task
task = kernel.create_task(
    description="Implement feature X",
    metadata={'security_clearance': 'medium'}
)

# Execute quantum loop
results = kernel.quantum_loop(task)

# Check results
print(f"Status: {task.status}")
print(f"Convergence: {results['final_convergence']:.2%}")
print(f"Decision: {results['synthesis']['decision']}")

# Shutdown
kernel.shutdown()
```

**Features:**
- Agent spawning and lifecycle management
- Quantum loop orchestration (thesis → antithesis → synthesis)
- Task queue management
- Convergence detection
- Event callbacks
- State persistence

## DNA Configuration

The swarm DNA is defined in `config/swarm_dna.yaml` and includes:

### Agent Configuration
```yaml
agents:
  - name: "athena"
    type: "memory_engine"
    trinity_role: "synthesis"
    os_polarity: "darwin"
    primary_functions:
      - "survivorship_bias_detection"
      - "institutional_memory"
    tools:
      - "vector_db"
      - "embeddings"
    security_clearance: "high"
    autonomy_level: 3
```

### Trinity Roles

- **Thesis (Creator)**: Generates proposals and solutions
- **Antithesis (Critic)**: Reviews and identifies issues
- **Synthesis (Integrator)**: Makes final decisions and integrates

### Orchestration Rules

```yaml
orchestration:
  quantum_loop:
    enabled: true
    max_iterations: 10
    convergence_threshold: 0.95
  
  consensus:
    algorithm: "weighted_voting"
    quorum_required: 0.67
```

## Quantum Loop Pattern

The quantum loop is an iterative refinement cycle:

```
1. THESIS (Proposal)
   ↓
   └─→ Agents with 'thesis' role generate solutions
       
2. ANTITHESIS (Critique)
   ↓
   └─→ Agents with 'antithesis' role identify issues
       
3. SYNTHESIS (Integration)
   ↓
   └─→ Agents with 'synthesis' role make decisions
       
4. Check Convergence
   ↓
   ├─→ Converged? → Complete
   └─→ Not converged? → Iterate (back to step 1)
```

**Convergence** is achieved when:
- Synthesis score ≥ convergence_threshold (default 95%)
- All required approvals obtained
- No blocking issues identified

## Examples

### Example 1: Simple Task Processing

```python
from swarm import SovereignMindKernel

# Initialize
kernel = SovereignMindKernel()
kernel.spawn_agents()

# Create task
task = kernel.create_task("Review security policy")

# Process with quantum loop (max 3 iterations)
results = kernel.quantum_loop(task, max_iterations=3)

# Display results
print(f"Completed in {results['iterations']} iterations")
print(f"Convergence: {results['final_convergence']:.2%}")
```

### Example 2: With Callbacks

```python
from swarm import SovereignMindKernel

# Define callbacks
def on_proposal(data):
    print(f"Proposal from: {[p['agent'] for p in data['proposals']]}")

def on_convergence(data):
    print(f"Converged in {data['iterations']} iterations!")

# Initialize with callbacks
kernel = SovereignMindKernel()
kernel.register_callback('on_proposal', on_proposal)
kernel.register_callback('on_convergence', on_convergence)

# Process
kernel.spawn_agents()
task = kernel.create_task("Deploy new feature")
results = kernel.quantum_loop(task)
```

### Example 3: Agent Status Monitoring

```python
from swarm import SovereignMindKernel

kernel = SovereignMindKernel()
kernel.spawn_agents()

# Get kernel status
status = kernel.get_kernel_status()
print(f"Active agents: {status['active_agents']}")
print(f"Queued tasks: {status['queued_tasks']}")

# Get agent health
health = kernel.get_agent_status()
for agent, info in health.items():
    print(f"{agent}: {info['tasks_completed']} tasks, {info['success_rate']:.1%} success")
```

## Testing

### Test DNA Loader
```bash
python3 swarm/load_dna.py
```

**Expected output:**
```
🧬 Loading Swarm DNA...
✅ DNA loaded successfully
   Version: 1.0.0
   Agents: 5

📊 Trinity Distribution:
   thesis: 2 agents - ['prometheus', 'scribe']
   antithesis: 1 agents - ['sentinel']
   synthesis: 2 agents - ['athena', 'oracle']
```

### Test Mind Kernel
```bash
python3 swarm/sovereign_mind_kernel.py
```

**Expected output:**
```
🧠 SOVEREIGN MIND KERNEL v1.0
...
✅ Convergence achieved at iteration 1
Task Status: completed
Final Convergence: 95.00%
Decision: proceed
```

## Integration

### With GitHub Actions

```yaml
name: Swarm Task
on: [workflow_dispatch]

jobs:
  swarm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run swarm task
        run: |
          python3 -c "
          from swarm import SovereignMindKernel
          kernel = SovereignMindKernel()
          kernel.spawn_agents()
          task = kernel.create_task('${{ github.event.inputs.task }}')
          results = kernel.quantum_loop(task)
          print(f'Status: {task.status}')
          "
```

### With Discord Bot

```python
import discord
from swarm import SovereignMindKernel

kernel = SovereignMindKernel()
kernel.spawn_agents()

@bot.command()
async def swarm_task(ctx, *, description: str):
    """Create and execute a swarm task"""
    task = kernel.create_task(description)
    results = kernel.quantum_loop(task)
    
    await ctx.send(
        f"✅ Task completed!\n"
        f"Iterations: {results['iterations']}\n"
        f"Convergence: {results['final_convergence']:.2%}\n"
        f"Decision: {results['synthesis']['decision']}"
    )
```

## Configuration

### Custom DNA Path

```python
from swarm import SovereignMindKernel

kernel = SovereignMindKernel(config_path='/custom/path/to/dna.yaml')
```

### Adjust Convergence

```python
# In config/swarm_dna.yaml
orchestration:
  quantum_loop:
    max_iterations: 20        # More iterations for complex tasks
    convergence_threshold: 0.98  # Stricter convergence requirement
```

### Add New Agents

```yaml
# In config/swarm_dna.yaml
agents:
  - name: "new_agent"
    type: "custom_type"
    trinity_role: "thesis"  # or "antithesis" or "synthesis"
    os_polarity: "linux"
    primary_functions:
      - "function1"
      - "function2"
    tools:
      - "tool1"
    security_clearance: "medium"
    autonomy_level: 3
```

## Architecture

```
┌─────────────────────────────────────────┐
│      Sovereign Mind Kernel              │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Task Queue                      │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Quantum Loop Engine             │  │
│  │   ┌─────────┐                     │  │
│  │   │ Thesis  │→ Proposals          │  │
│  │   └─────────┘                     │  │
│  │        ↓                          │  │
│  │   ┌──────────────┐                │  │
│  │   │ Antithesis   │→ Critiques     │  │
│  │   └──────────────┘                │  │
│  │        ↓                          │  │
│  │   ┌───────────┐                   │  │
│  │   │ Synthesis │→ Decision         │  │
│  │   └───────────┘                   │  │
│  │        ↓                          │  │
│  │   Convergence Check               │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Agent Registry                  │  │
│  │   • athena    (synthesis)         │  │
│  │   • prometheus (thesis)           │  │
│  │   • sentinel  (antithesis)        │  │
│  │   • oracle    (synthesis)         │  │
│  │   • scribe    (thesis)            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                 ↕
┌─────────────────────────────────────────┐
│      DNA Configuration (YAML)            │
│  • Trinity roles                        │
│  • Agent definitions                    │
│  • Orchestration rules                  │
│  • Security policies                    │
└─────────────────────────────────────────┘
```

## Troubleshooting

### Issue: DNA file not found

**Solution:**
```python
# Use explicit path
from swarm import DNALoader
loader = DNALoader('/absolute/path/to/swarm_dna.yaml')
dna = loader.load()
```

### Issue: Agent not assigned to task

**Check:**
1. Agent has correct trinity_role for the stage
2. Agent has sufficient security_clearance
3. Agent is in active_agents registry

### Issue: Convergence never achieved

**Adjust:**
```yaml
orchestration:
  quantum_loop:
    convergence_threshold: 0.90  # Lower threshold
    max_iterations: 20           # More iterations
```

## API Reference

See inline documentation in:
- `load_dna.py` - DNA loading and validation
- `sovereign_mind_kernel.py` - Kernel orchestration

## License

See [LICENSE](../LICENSE) file.

## Support

For questions or issues:
1. Check [SWARM_GOVERNANCE.md](../SWARM_GOVERNANCE.md)
2. Review [config/swarm_dna.yaml](../config/swarm_dna.yaml)
3. Open an issue with label `swarm-support`
