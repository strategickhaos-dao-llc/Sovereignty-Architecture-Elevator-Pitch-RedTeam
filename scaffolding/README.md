# Legends of Minds Engineering Canon v1.0 - Scaffolding

**The foundation for systems that scale to nation-state level.**

This is not a course. This is not homework. This is the rebar and concrete for the skyscraper you're already building.

## What Is This?

A complete, production-ready scaffolding system that gives you:

1. **100-Point Engineering Map** (`CANON.md`) - Comprehensive reference for distributed systems, architecture, reliability, security, and performance
2. **Obsidian Knowledge Vault** - Deep-dive pages on every canonical principle with examples, patterns, and best practices
3. **Repo Templates** - Battle-tested project structure following hexagonal architecture
4. **Heir Integration** - System prompts that inject canonical knowledge into every AI agent
5. **One-Command Installation** - Deploy to all nodes via PowerShell script

## Quick Start

### Option 1: One-Command Install (Windows + Tailscale)

```powershell
# Run this ONCE from your main Nitro machine (the one with Tailscale + access to all 5 nodes)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/legendsofminds/scaffolding/main/install_c_full_map.ps1" -OutFile "$env:TEMP\install_c_full_map.ps1"; . "$env:TEMP\install_c_full_map.ps1"
```

**What this does:**
1. Clones scaffolding to `C:\legends_of_minds\scaffolding\`
2. Syncs to all 5 nodes via Tailscale + robocopy (air-gapped safe)
3. Adds vault to Obsidian RAG index
4. Injects canon prompt into every heir
5. Drops `CANON.md` in your home directory

### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/legendsofminds/scaffolding.git
cd scaffolding

# Copy Obsidian vault
cp -r obsidian-vault/* ~/Documents/Obsidian/Sovereignty/

# Copy heir prompt
cp heir_canon_prompt.txt ~/.config/heirs/prompts/canon_v1.0.txt

# Open CANON.md
open CANON.md
```

## Repository Structure

```
scaffolding/
├── CANON.md                      ← 100-point engineering map
├── heir_canon_prompt.txt         ← Inject into heir system prompts
├── install_c_full_map.ps1        ← One-command installation script
├── README.md                     ← This file
│
├── obsidian-vault/               ← Knowledge base (import to Obsidian)
│   ├── 00_Meta/                  ← Systems Thinking, Engineering Philosophy
│   │   ├── Systems_Thinking.md
│   │   └── Engineering_Philosophy.md
│   │
│   ├── 10_Distributed/           ← CAP Theorem, Consensus, Network Partitions
│   │   ├── CAP_Theorem.md
│   │   ├── Consensus_Algorithms.md
│   │   ├── Network_Fallacies.md
│   │   └── Eventual_Consistency.md
│   │
│   ├── 20_Architecture/          ← Hexagonal, CQRS, Event Sourcing, DDD
│   │   ├── Hexagonal_Architecture.md
│   │   ├── Event_Sourcing.md
│   │   ├── CQRS.md
│   │   └── Domain_Driven_Design.md
│   │
│   ├── 30_Reliability/           ← Observability, Chaos, SLOs, Deployments
│   │   ├── Observability.md
│   │   ├── Chaos_Engineering.md
│   │   ├── SRE_Practices.md
│   │   └── Deployment_Strategies.md
│   │
│   ├── 40_Security_Compliance/   ← Zero Trust, Agent Security, Encryption
│   │   ├── Zero_Trust_Architecture.md
│   │   ├── Agent_Security.md
│   │   ├── Secrets_Management.md
│   │   └── Threat_Modeling.md
│   │
│   └── 50_Templates/             ← Ready-to-use configs and templates
│       ├── pyproject.toml        ← Modern Python project setup
│       ├── docker-compose.yml    ← Full observability stack
│       ├── prometheus.yml        ← Metrics collection
│       └── github-actions.yml    ← CI/CD pipeline
│
└── repo-template/                ← Template for new projects
    ├── README.md                 ← Sovereignty-first project README
    ├── src/
    │   ├── core/                 ← Business logic (hexagonal architecture)
    │   ├── adapters/             ← External integrations
    │   └── main.ts               ← Dependency injection
    ├── tests/
    ├── docs/
    └── .github/
        └── workflows/
```

## The 100-Point Canon

The canon covers:

### 0. Meta-Principles (10 Points)
- Systems thinking, emergent behavior, feedback loops
- Sovereignty first, evolution over revolution
- Observable everything, automate toil

### 1. Distributed Systems (10 Points)
- CAP theorem, quorum protocols, BASE vs ACID
- Network fallacies, latency numbers, clock synchronization
- Paxos, Raft, 2PC/3PC, Saga pattern

### 2. Architecture Patterns (20 Points)
- Hexagonal/Onion/Clean Architecture, SOLID
- Event Sourcing, CQRS, Event Storming
- Domain-Driven Design: Bounded contexts, aggregates
- Microservices: Service mesh, circuit breaker, API gateway

### 3. Reliability & Operations (20 Points)
- Observability: Logs, metrics, traces (RED/USE metrics)
- SRE: SLIs/SLOs/SLAs, error budgets, blameless postmortems
- Chaos engineering: Failure injection, Game Days
- Deployment: Blue-green, canary, rolling, feature flags

### 4. Security & Compliance (20 Points)
- Zero trust: Never trust, always verify, least privilege
- Secure development: Threat modeling, defense in depth
- Data protection: Encryption at rest/transit, secrets management
- Agent-specific: Sandboxing, prompt injection defense, audit trails

### 5. Performance & Scalability (10 Points)
- Profiling, caching strategies, CDN/edge computing
- Horizontal vs vertical scaling, stateless services, sharding

### 6. Team & Process (10 Points)
- DevOps philosophy, psychological safety, documentation as code
- Code review culture, continuous learning

## Using the Canon

### For Humans

1. **Start with CANON.md** - High-level overview of all 100 principles
2. **Deep dive in Obsidian** - Each principle has detailed page with examples
3. **Use templates** - Don't start from scratch, use battle-tested configs
4. **Reference during design** - "How do I make this survive node death?" → Check canon #11-25

### For AI Heirs

The `heir_canon_prompt.txt` injects canonical knowledge into every heir:

```
You are operating under the Legends of Minds Engineering Canon v1.0.

When addressing scaling, distributing, or hardening:
- Reference canon principles by number (e.g., "Per canon #46, implement structured logging")
- Explain trade-offs using canon concepts (e.g., "This is a CAP theorem decision")
- Consider failure modes (chaos engineering mindset)
```

**How to inject:**

```python
# In your heir initialization
base_prompt = load_file("heir_base_prompt.txt")
canon_addon = load_file("heir_canon_prompt.txt")
full_prompt = base_prompt + "\n\n" + canon_addon

heir = Heir(system_prompt=full_prompt)
```

### For New Projects

Use the repo template:

```bash
# Create new project from template
cp -r repo-template my-new-service
cd my-new-service

# Customize
sed -i 's/your-project-name/my-new-service/g' pyproject.toml
sed -i 's/your-service/my-new-service/g' docker-compose.yml

# Start coding with best practices built-in
```

## Examples

### Example 1: Designing a Distributed System

**Question:** "How do I build a system that survives node failures?"

**Canon References:**
- #11-15: CAP Theorem - Choose CP or AP based on requirements
- #21-25: Consensus algorithms - Use Raft for strongly consistent data
- #56-60: Chaos engineering - Test node failures regularly
- #46-50: Observability - Know when nodes fail

**Obsidian Path:** `10_Distributed/CAP_Theorem.md` → Full explanation with code examples

### Example 2: Implementing Authentication

**Question:** "How do I secure API access?"

**Canon References:**
- #66-70: Zero trust - Never trust based on network location
- #69: Strong authentication - Use WebAuthn/FIDO2
- #67: Least privilege - Minimal permissions only
- #84: Audit trails - Log all access

**Obsidian Path:** `40_Security_Compliance/Zero_Trust_Architecture.md` → Complete implementation guide

### Example 3: Debugging Production Issues

**Question:** "Service is slow, how do I find the bottleneck?"

**Canon References:**
- #46: Three pillars - Use logs, metrics, traces
- #48-49: RED/USE metrics - Identify slow components
- #50: Distributed tracing - See request flow
- #86: Profiling - Find CPU/memory bottlenecks

**Obsidian Path:** `30_Reliability/Observability.md` → Detailed troubleshooting guide

## From This Moment Forward

- ✅ Every new heir is born with the canon in its DNA
- ✅ Every new repo starts with the template (hexagonal architecture, observability, security)
- ✅ Every question you ask yourself has a page in the vault
- ✅ Every time you hit a wall, the answer is one Obsidian search away

**You are still 100% sovereign.**
**You are still moving at mach 3 with your hair on fire.**
**You just poured titanium foundations under the launch pad.**

## Installation Details

### System Requirements

- **OS:** Windows 10/11 or Linux
- **PowerShell:** 5.1+ (for Windows installation)
- **Tailscale:** For multi-node sync (optional)
- **Obsidian:** For vault access (optional but recommended)

### Installation Script Options

```powershell
# Basic installation
.\install_c_full_map.ps1

# Custom paths
.\install_c_full_map.ps1 -TargetPath "D:\scaffolding" -ObsidianVaultPath "D:\Obsidian\Canon"

# Skip certain steps
.\install_c_full_map.ps1 -SkipNodeSync  # Don't sync to remote nodes
.\install_c_full_map.ps1 -SkipObsidian  # Don't install Obsidian vault
.\install_c_full_map.ps1 -SkipHeirPrompt  # Don't inject heir prompt

# Specify custom nodes
.\install_c_full_map.ps1 -Nodes @("node1", "node2", "node3")
```

## Air-Gapped Deployment

For fully air-gapped environments:

1. **Download** scaffolding on internet-connected machine
2. **Transfer** via USB/physical media to air-gapped network
3. **Run** installation script with `-SkipNodeSync` (sync manually via robocopy)
4. **Distribute** to nodes using local network shares

```powershell
# On air-gapped network
.\install_c_full_map.ps1 -SkipNodeSync

# Manually sync to nodes
robocopy "C:\legends_of_minds\scaffolding" "\\node1\c$\legends_of_minds\scaffolding" /E /Z
robocopy "C:\legends_of_minds\scaffolding" "\\node2\c$\legends_of_minds\scaffolding" /E /Z
```

## Updating the Canon

As you 100× your systems, you'll discover new principles:

1. **Update CANON.md** - Add new principles (maintain numbering)
2. **Create Obsidian pages** - Deep-dive on new concepts
3. **Update heir prompt** - Include new principles in system prompt
4. **Share** - Contribute back to the community

## Contributing

This is a living canon. Improvements welcome:

1. Fork repository
2. Add/improve content in Obsidian vault
3. Update CANON.md with new principles
4. Submit PR with clear description
5. Share knowledge with the legion

## Support & Community

- **Issues:** [GitHub Issues](https://github.com/legendsofminds/scaffolding/issues)
- **Discussions:** [GitHub Discussions](https://github.com/legendsofminds/scaffolding/discussions)
- **Discord:** [Legends of Minds Server](https://discord.gg/legendsofminds)

## License

MIT License - Use freely, commercially or non-commercially. Attribution appreciated but not required.

---

**Welcome to the next order of magnitude.** 🧠🔥

**Now go build something that scares nation-states.**
