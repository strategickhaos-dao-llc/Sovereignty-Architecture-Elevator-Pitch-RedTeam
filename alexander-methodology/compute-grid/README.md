# Alexander Compute Grid

**Distributed Computing for Breakthrough Research**

The Alexander Compute Grid is a BOINC-style distributed computing network where every legion node donates idle CPU/GPU resources to collaborative research projects.

## Overview

Traditional research is limited by compute resources. The Alexander Compute Grid democratizes access to computational power by:

- **Pooling Resources**: Every researcher node contributes idle compute time
- **Distributed Processing**: Large problems broken into manageable chunks
- **GPU Acceleration**: Utilize CUDA/OpenCL for parallel processing
- **Quantum Simulation**: Early-stage quantum computing simulation support
- **Priority Queue**: Critical research gets priority, but all projects run

## How It Works

### For Contributors

When you run `./join-swarm.sh`, your node automatically joins the compute grid:

1. **Idle Detection**: Grid monitors CPU/GPU utilization
2. **Task Assignment**: When idle, node receives compute tasks
3. **Processing**: Your machine works on research calculations
4. **Result Upload**: Completed work sent back to grid coordinator
5. **Credit System**: Earn credits for contributed compute time

### For Researchers

Submit compute-intensive tasks to the grid:

```bash
# Submit a research job to the compute grid
./compute-grid/submit-job.sh \
  --project "voynich-pattern-analysis" \
  --task-type "parallel-processing" \
  --input-data "./data/voynich-pages/" \
  --script "./analysis/pattern-matcher.py" \
  --priority "medium"
```

## Supported Workloads

### Cryptographic Analysis
- Cipher breaking and pattern recognition
- Statistical analysis of ancient texts
- Frequency analysis at scale

### Machine Learning Training
- Neural network training for text recognition
- Image classification for archaeological artifacts
- Pattern detection in complex datasets

### Molecular Simulation
- Protein folding calculations
- Drug interaction modeling
- Material science simulations

### Mathematical Computation
- Large-scale numerical analysis
- Monte Carlo simulations
- Optimization problems

### Quantum Simulation
- Quantum algorithm testing
- Quantum chemistry calculations
- Early-stage quantum ML experiments

## Architecture

```
┌─────────────────────────────────────────┐
│     Grid Coordinator (Kubernetes)       │
│  - Task Distribution                    │
│  - Result Aggregation                   │
│  - Node Management                      │
└─────────────────────────────────────────┘
              ↓         ↓         ↓
    ┌─────────┴─────────┴─────────┴─────────┐
    │                                        │
┌───▼────┐  ┌────────┐  ┌────────┐  ┌──────▼──┐
│ Node 1 │  │ Node 2 │  │ Node N │  │ GPU Pool│
│ CPU    │  │ CPU    │  │ CPU    │  │ CUDA    │
└────────┘  └────────┘  └────────┘  └─────────┘
```

## Node Configuration

### Basic Node (CPU Only)
```yaml
node_type: cpu
cores_dedicated: 2-4
max_memory: 4GB
task_types:
  - cryptographic-analysis
  - text-processing
  - statistical-computation
```

### GPU Node (NVIDIA)
```yaml
node_type: gpu
gpu_model: NVIDIA RTX 3080
cuda_cores: 8704
max_memory: 10GB
task_types:
  - neural-network-training
  - molecular-simulation
  - parallel-cryptography
  - quantum-simulation
```

### High-Memory Node
```yaml
node_type: high-memory
cores_dedicated: 8
max_memory: 64GB
task_types:
  - large-dataset-analysis
  - graph-computation
  - simulation-with-state
```

## Resource Allocation

### Priority Levels

1. **Critical** (5%): Breakthrough imminent, needs immediate compute
2. **High** (20%): Active bounty target with progress
3. **Medium** (40%): Standard research projects
4. **Low** (25%): Exploratory analysis and testing
5. **Background** (10%): Data processing and indexing

### Fair Share

- Each researcher gets base allocation
- Bonus allocation for compute contributions
- Emergency boost for time-sensitive discoveries
- Quantum computing time allocated separately

## Security & Privacy

- **Sandboxed Execution**: All tasks run in isolated containers
- **Code Review**: Submitted scripts reviewed for malicious behavior
- **Data Encryption**: All data transfers encrypted with TLS
- **Privacy Protection**: Sensitive data never leaves secure nodes
- **Opt-Out**: Researchers can exclude certain task types

## Getting Started

### Join as a Contributor

```bash
# Already done when you ran join-swarm.sh!
# Check your node status:
./compute-grid/node-status.sh
```

### Submit a Research Job

```bash
# 1. Prepare your computation script
# 2. Package input data
# 3. Submit to grid
./compute-grid/submit-job.sh --help
```

### Monitor Your Jobs

```bash
# Check job status
./compute-grid/job-status.sh --job-id <your-job-id>

# View compute logs
./compute-grid/job-logs.sh --job-id <your-job-id>
```

## Performance Stats

*Real-time stats from the grid:*

- **Active Nodes**: Track in real-time via dashboard
- **Total Compute Power**: Aggregate CPU/GPU capacity
- **Jobs Processed**: Cumulative research tasks completed
- **Breakthroughs**: Number of bounty targets solved
- **Energy Efficiency**: Compute per watt metrics

## Integration with Other Pillars

### Forbidden Library RAG
- Compute grid processes queries at scale
- Parallel document embedding and indexing
- Real-time semantic search acceleration

### Bounty Board
- Critical bounty targets get priority compute allocation
- Progress tracking linked to compute utilization
- Automatic resource scaling for active targets

### Mirror Council
- Governance over resource allocation policies
- Dispute resolution for compute priorities
- Strategic direction for grid expansion

## Contributing

### Donate Compute Time
- Run `./join-swarm.sh` to auto-join
- Configure max resource usage in `.node-config`
- Earn credits and recognition

### Optimize Grid Software
- Improve task distribution algorithms
- Enhance GPU utilization efficiency
- Add support for new compute types

### Sponsor Hardware
- GPU server donations
- Cloud compute credits
- Network infrastructure

## Technical Details

### Task Distribution Protocol
- WebSocket-based coordination
- Heartbeat every 30 seconds
- Auto-reconnect on network issues
- Checkpoint/resume for long tasks

### Supported Platforms
- Linux (Ubuntu, Debian, CentOS)
- macOS (Intel and Apple Silicon)
- Windows (via WSL2)
- Docker containers
- Kubernetes pods

### Dependencies
- Python 3.8+
- Docker (optional but recommended)
- CUDA Toolkit (for GPU nodes)
- 10GB free disk space minimum

## FAQ

**Q: Does this slow down my computer?**  
A: No. The grid only uses idle resources and yields to your active tasks immediately.

**Q: Can I choose which projects to support?**  
A: Yes. Configure task preferences in `.node-config`.

**Q: What about electricity costs?**  
A: Use idle time efficiently. Set max power usage limits if concerned.

**Q: Is my data safe?**  
A: Yes. All computation is sandboxed and encrypted. No access to your personal files.

**Q: Can I earn money for contributing?**  
A: Currently, earn credits and recognition. Partial bounty sharing for contributed compute may come in future.

---

**The compute grid never sleeps.**  
**The research never stops.**  
**The mysteries fall, one calculation at a time.** 🔬⚡🧮
