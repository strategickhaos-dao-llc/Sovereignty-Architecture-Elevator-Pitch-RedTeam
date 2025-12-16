# Getting Started with Sovereignty Architecture

Welcome! You've just entered a repository that bridges **vision** and **execution**. This guide shows you how to navigate from idea to implementation using the foundational structure we've built.

## 🎯 The Three Pillars

### 1. INVENTORY.yaml - Single Source of Truth

**What**: Every component in this project has a unique ID, status, dependencies, and outputs.

**Why**: No more "what needs to be done?" or "where do I start?" — just check INVENTORY.yaml.

**Example**:
```yaml
- id: FL-001
  name: Lexer
  domain: flamelang
  status: missing
  depends_on: []
  outputs:
    - src/flamelang/lexer/
```

### 2. ROADMAP.md - Phase-Based View

**What**: A timeline showing how components fit into phases (Q1 2026, Q2-Q4 2026, etc.)

**Why**: Gives you context for *when* something should be done and *what depends on it*.

**Example**: Phase 1 shows that FL-001 (Lexer) must be complete before FL-002 (Parser) can begin.

### 3. benches/stats_suite/ - Benchmark Framework

**What**: Cross-language performance testing infrastructure (BM-001).

**Why**: When we say FlameLang should be "within 2x of C++," we need data to prove it.

**Try it**:
```bash
cd benches/stats_suite
./run_benchmarks.sh
```

---

## 🚀 Quick Start

### For Contributors

**1. Find something to work on:**
```bash
# Check the INVENTORY for components with status: missing or stub
grep -A 5 "status: missing" INVENTORY.yaml
```

**2. Reference the component ID in your commits:**
```bash
git commit -m "FL-001: add tokenizer unit tests"
```

**3. Update status when done:**
Edit INVENTORY.yaml to change `status: missing` → `status: in_progress` → `status: complete`

### For Project Managers

**1. Track progress:**
```bash
# Count components by status
grep "status:" INVENTORY.yaml | sort | uniq -c
```

**2. Identify blockers:**
Check `depends_on` fields in INVENTORY.yaml to see what's blocking other work.

**3. Review roadmap timing:**
Check ROADMAP.md for quarterly milestones and adjust based on velocity.

---

## 📁 Repository Structure

```
├── INVENTORY.yaml           # Single source of truth for all components
├── ROADMAP.md              # Phase-based view of development timeline
├── GETTING_STARTED.md      # This file
│
├── src/                    # Source code organized by domain
│   ├── flamelang/         # Future: FL-001 through FL-006
│   ├── kernel/            # Future: OS-001 through OS-004
│   ├── refinory/          # INF-004: AI refinement system
│   ├── bot.ts             # INF-001: Discord operations bot
│   └── event-gateway.ts   # INF-002: Webhook router
│
├── benches/               # Benchmark suites
│   ├── stats_suite/       # BM-001: Statistical benchmarks
│   └── ...                # Future: BM-002, BM-003
│
├── governance/            # GOV-001, GOV-002: DAO and legal
├── legal/                 # Legal compliance and documentation
├── monitoring/            # INF-005: Observability stack
│
└── docs/                  # DOC-001, DOC-002, DOC-003
    ├── README.md
    ├── DEPLOYMENT.md
    └── COMMUNITY.md
```

---

## 🔥 Common Workflows

### Starting a New Component

```bash
# 1. Check INVENTORY.yaml for the component ID and dependencies
# 2. Verify dependencies are complete
# 3. Create directory structure (from outputs field)
mkdir -p src/flamelang/lexer
cd src/flamelang/lexer

# 4. Create initial files
touch lexer.rs token.rs tests.rs

# 5. Commit with component ID
git add .
git commit -m "FL-001: create lexer module structure"

# 6. Update INVENTORY.yaml status to 'in_progress'
```

### Completing a Component

```bash
# 1. Ensure all tests pass
cargo test

# 2. Run relevant benchmarks (if applicable)
cd benches/stats_suite
./run_benchmarks.sh

# 3. Update INVENTORY.yaml status to 'complete'
# 4. Commit with component ID
git commit -m "FL-001: complete lexer implementation with full test coverage"

# 5. Check ROADMAP.md to see what's unblocked
```

### Adding a New Benchmark

```bash
# 1. Create benchmark in benches/
# 2. Add to INVENTORY.yaml with BM-XXX ID
# 3. Update benches/stats_suite/README.md
# 4. Add to run_benchmarks.sh
# 5. Commit with BM-XXX ID
```

---

## 🎓 Understanding Component IDs

Component IDs follow the pattern: `[DOMAIN]-[NUMBER]`

| Prefix | Domain            | Examples                    |
|--------|-------------------|-----------------------------|
| FL     | FlameLang         | FL-001 (Lexer), FL-002 (Parser) |
| OS     | Operating System  | OS-001 (Bootloader), OS-002 (Kernel) |
| BM     | Benchmarks        | BM-001 (Stats Suite), BM-002 (Perf Suite) |
| INF    | Infrastructure    | INF-001 (Discord Bot), INF-005 (Monitoring) |
| GOV    | Governance        | GOV-001 (DAO Constitution) |
| DOC    | Documentation     | DOC-001 (Architecture Docs) |

---

## 📊 Tracking Progress

### Component Status Tags

- **missing**: Not started
- **stub**: Basic structure, minimal functionality
- **partial**: Core functionality exists, needs completion
- **in_progress**: Actively being developed
- **complete**: Fully implemented and tested

### Phase Status (from ROADMAP.md)

- **Phase 0 (Current)**: Foundation - Infrastructure and benchmarks
- **Phase 1 (Q2-Q4 2026)**: Minimum Viable Language - FlameLang compiler
- **Phase 2 (2027 H1-H2)**: Language Maturity & OS Bootstrap
- **Phase 3 (2027 H2-2028)**: Production Ready - Complete OS stack
- **Phase 4 (2028+)**: Ecosystem Growth - Tools and libraries

---

## 🤝 Integration with Existing Systems

### Discord Bot Integration

The Discord bot (INF-001) can query component status:

```
/status FL-001      # Check status of FlameLang Lexer
/roadmap phase1     # Show Phase 1 components
/inventory missing  # List all missing components
```

*(Note: These commands are planned for INF-001 enhancement)*

### CI/CD Integration

Commits that reference component IDs can trigger:
- Status checks for related components
- Automated tests for dependent components
- Dashboard updates showing progress

### Monitoring Integration

The monitoring stack (INF-005) can track:
- Component completion percentage by domain
- Velocity metrics (components completed per sprint)
- Dependency graph visualization

---

## 🎯 Next Steps

### Immediate (This Week)
1. Complete BM-001 actual implementation (five-number summary calculation)
2. Add component status query to INF-001 (Discord bot)
3. Review and validate all component IDs in INVENTORY.yaml

### Short Term (This Month)
1. Start FL-001 (Lexer) implementation
2. Complete INF-004 (Refinory) expert integration
3. Add INVENTORY-aware monitoring to INF-005

### Medium Term (Q1 2026)
1. Complete Phase 0 components
2. Begin Phase 1 (Language development)
3. Establish weekly progress reviews using INVENTORY metrics

---

## 📚 Key Documents

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| INVENTORY.yaml | Component tracking | Every commit |
| ROADMAP.md | Phase planning | Monthly |
| README.md | Project overview | As needed |
| DEPLOYMENT.md | Ops guides | When infrastructure changes |
| COMMUNITY.md | Contributor guidelines | Quarterly |

---

## 🆘 Getting Help

### Finding Information

1. **What component should I work on?**
   - Check ROADMAP.md for current phase
   - Filter INVENTORY.yaml by `status: missing` or `status: stub`

2. **What does component X depend on?**
   - Look at `depends_on` field in INVENTORY.yaml

3. **How do I run tests/benchmarks?**
   - Check component's `outputs` field for test location
   - See benches/stats_suite/README.md for benchmark instructions

4. **Who's working on what?**
   - Check recent commits with component IDs: `git log --grep="FL-001"`

### Communication Channels

- **Discord**: #prs, #deployments, #agents (see README.md)
- **GitHub Issues**: Tag with component IDs (e.g., `[FL-001]`)
- **Pull Requests**: Reference component IDs in title and description

---

## ✅ Validation Checklist

Before submitting a PR, ensure:

- [ ] Commit messages reference component IDs (e.g., "FL-001: add tests")
- [ ] INVENTORY.yaml updated with current status
- [ ] Tests pass for your component and dependencies
- [ ] Benchmarks run successfully (if applicable)
- [ ] Documentation updated (if interface changed)
- [ ] No build artifacts committed (check .gitignore)

---

## 🌟 Philosophy

This structure exists because:

1. **Elevator pitches are easy, execution is hard**
   - We need more than vision; we need a dependency graph

2. **Everything gets an ID and a status**
   - No more "where are we?" conversations
   - Just check INVENTORY.yaml

3. **Roadmaps are views, not truth**
   - ROADMAP.md is generated from INVENTORY.yaml
   - Change INVENTORY, roadmap updates follow

4. **Benchmarks prove claims**
   - "Fast" means data, not vibes
   - BM-001 provides that data

---

**Welcome to the team. Pick a component, reference its ID, and start building.**

The vision is set. The spine is installed. Now we grow.

---

*Last Updated: 2025-12-16*  
*Next Review: When Phase 0 is complete*
