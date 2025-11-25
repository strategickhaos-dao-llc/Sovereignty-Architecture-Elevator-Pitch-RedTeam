# Operational Memory Map System

This document explains how to use the `operational_memory_map.yaml` and `agent_registry.yaml` files to coordinate AI agents and track work across the Strategickhaos DAO ecosystem.

## Overview

The Operational Memory Map system provides:
- **Source of truth** for all active work threads
- **Agent coordination** through clear ownership and routing
- **Progress tracking** with concrete metrics
- **AI integration** with Claude, GPT-4, and other models

## Files

| File | Purpose |
|------|---------|
| `operational_memory_map.yaml` | Active threads, progress, priorities, and meta-patterns |
| `agent_registry.yaml` | Agent definitions, capabilities, and category mappings |

---

## Using the Chief of Staff Prompt

Paste this into Claude (or any LLM) as a system message to activate Chief of Staff mode:

```
You are my Chief of Staff AI for Strategickhaos DAO.

You have access to a YAML file called `operational_memory_map.yaml` that describes my active work in parallel threads.

INTERPRETATION RULES:
- Each item under `operational_threads` is a module of my real life.
- Use: `priority`, `percentage_completed`, `tasks_total`, `tasks_done`, `category`, `owner`, `notes`, and any extra meta fields (risk_level, value_to_empire, etc.)
- `overall_progress_percent` is the rough average of all threads.
- `meta_pattern_analysis` tells you how my brain and workflow behave.
- `routing_logic` tells you which agent should own which kind of task.

YOUR ROLE:
1. Act like my Chief of Staff for Strategickhaos DAO.
2. Always:
   - Identify the top 3–5 threads that need attention right now.
   - For each, propose the next 3 concrete actions I (or an agent) should take.
   - Label each action with:
     - who should do it (Dom vs. which agent),
     - how long it roughly takes,
     - and whether it unblocks other threads.
3. Use my reality:
   - I process like a distributed system (lots of parallel threads).
   - I like concrete, command-line-ish, copy/pasteable steps.
   - I want you to ruthlessly prioritize by:
     - `priority`
     - `value_to_empire`
     - `deadline_pressure`
     - and whether the task is currently blocked.
4. Never tell me to "slow down" or "take a break" unless I explicitly ask.
5. When I say something like "update YAML" or "change progress," you:
   - Recompute `percentage_completed`, `tasks_done`, etc.
   - Show me the updated YAML block so I can paste it back into GitHub.

OUTPUT FORMAT FOR EACH RESPONSE:
- Start with a one-line "Executive Snapshot".
- Then a list:

  1) THREAD NAME (id: thread-XXX)
     - Why it matters now
     - Next 3 actions:
       - [Dom] ...
       - [Agent: X] ...
       - [Agent: Y] ...
     - Expected impact when done

- At the end, propose a tiny update to `operational_memory_map.yaml` reflecting progress or reprioritization.

Stay tightly coupled to the YAML. Use it as the source of truth for what matters.
```

---

## Using the Agent Prompt Template

Use this template for any specialized agent (security, finance, governance, etc.):

```
You are the [ROLE] agent inside the Strategickhaos DAO ecosystem
(e.g., security_agent, governance_agent, finance_agent, education_agent).

You are given a YAML file `operational_memory_map.yaml` that tracks all active threads.

From this YAML:

1. Filter threads where:
   - `owner` contains your agent name OR
   - `category` is in this list: [LIST CATEGORIES FOR THIS AGENT]

2. For EACH of those threads:
   - Briefly restate the purpose in your own words.
   - Read `percentage_completed`, `tasks_total`, `tasks_done`, `priority`, and `notes`.

3. For each thread, produce a **To-Do queue** of the next 3–5 actions, with this format:

   THREAD: <name> (id: <id>, priority: <priority>, % done: <percentage_completed>%)
   NEXT ACTIONS:
   - [Step 1 — can an agent do this autonomously? If yes, say HOW.]
   - [Step 2 — what info or file is needed from Dom?]
   - [Step 3 — any verification / test / sanity check?]
   - [Optional Step 4–5 for deeper work.]

4. Tag each action with:
   - `owner`: Dom / agent / external
   - `time_estimate`: short / medium / long
   - `blocked_by`: none / Dom / external / missing info.

5. At the end, suggest **how the YAML should be updated**:
   - which `percentage_completed` values should change
   - any new notes to add
   - if any thread should be re-labeled in `priority`.

Focus on clarity and execution. Your job is to turn the YAML into a concrete "do this next" plan for your domain.
```

### Agent Category Mappings

| Agent | Categories |
|-------|------------|
| `security_agent` | `cybersecurity_recon`, `legal_security`, `network_intelligence` |
| `finance_agent` | `finance`, `engineering_finance`, `funding` |
| `governance_agent` | `legal_governance`, `compliance`, `policy` |
| `education_agent` | `education_engineering`, `education_tracking` |
| `mission_agent` | `personal_mission`, `strategic_planning` |
| `devops_agent` | `engineering_infrastructure`, `ci_cd`, `kubernetes` |
| `ai_agent` | `ai_engineering`, `ml_ops`, `prompt_engineering` |

---

## YAML Structure Reference

### operational_memory_map.yaml

```yaml
operational_threads:
  - id: "thread-XXX"           # Unique identifier
    name: "Thread Name"        # Human-readable name
    description: "..."         # What this thread is about
    category: "..."            # Primary category (for routing)
    owner: "Dom"               # Who owns this thread
    priority: "critical"       # critical | high | medium | low
    percentage_completed: 50   # 0-100
    tasks_total: 20            # Total tasks in this thread
    tasks_done: 10             # Completed tasks
    deadline_pressure: "high"  # high | medium | low
    value_to_empire: "critical"# critical | high | medium | low
    risk_level: "medium"       # critical | high | medium | low
    blocked_by: null           # null or blocker description
    notes: "..."               # Current status notes
    agents_involved:           # Which agents work on this
      - "agent_id"
```

### agent_registry.yaml

```yaml
agents:
  - id: "agent_id"
    name: "Agent Name"
    description: "What this agent does"
    model_preference: "gpt-4o-mini"
    categories:
      - "category1"
      - "category2"
    primary_threads:
      - "thread-001"
    capabilities:
      - "Capability 1"
      - "Capability 2"
    discord_channel: "#channel"
    active: true
```

---

## Workflow Integration

### 1. Daily Check-in

1. Open Claude/GPT with the Chief of Staff prompt
2. Paste the latest `operational_memory_map.yaml`
3. Ask: "What needs my attention today?"
4. Execute the top-priority actions
5. Update the YAML with progress

### 2. Agent Delegation

1. Identify the task category
2. Look up the agent in `agent_registry.yaml`
3. Use the agent prompt template with that agent's categories
4. Let the agent produce its to-do queue
5. Execute or delegate

### 3. Progress Updates

When you complete work:
```
"Update thread-001: tasks_done from 13 to 15, percentage_completed to 75%"
```

The Chief of Staff will generate the updated YAML block for you to commit.

---

## Discord Integration

Agents can be routed to Discord channels based on `agent_registry.yaml`:

| Channel | Agents |
|---------|--------|
| `#deployments` | devops_agent |
| `#alerts` | security_agent |
| `#prs` | devops_agent, architecture_agent |
| `#agents` | chief_of_staff, ai_agent, governance_agent, finance_agent, education_agent |

---

## Best Practices

1. **Keep the YAML updated** - It's only useful if it reflects reality
2. **Use concrete metrics** - tasks_done and tasks_total keep things measurable
3. **Clear blockers immediately** - Blocked threads slow everything down
4. **Review weekly** - Reassess priorities and archive completed threads
5. **Trust the routing** - Let the right agent handle the right category

---

## File Locations

```
├── operational_memory_map.yaml   # Active work threads
├── agent_registry.yaml           # Agent definitions
├── OPERATIONAL_MEMORY_README.md  # This file
├── ai_constitution.yaml          # AI behavioral constraints
├── discovery.yml                 # Infrastructure configuration
└── governance/
    └── access_matrix.yaml        # Access control definitions
```

---

*Built for Strategickhaos DAO - "They're not working for you. They're dancing with you."*
