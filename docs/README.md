# Documentation Directory

This directory contains all generated documentation for the StrategicKhaos Educational Swarm Rollout project.

## Structure

```
docs/
├── README.md                                      # This file
├── StrategicKhaos_Educational_Swarm_Playbook.md  # Master playbook
└── departments/                                   # Department-specific docs
    ├── README.md
    ├── education_brief.md
    ├── security_ops_runbook.md
    ├── infra_cloud_runbook.md
    ├── finance_legal_brief.md
    └── comms_outreach_brief.md
```

## Generation

All documents are generated using the mission file:

```
strategickhaos_product_build.yaml
```

This YAML serves as the canonical specification for Claude/LLM to generate all deliverables.

## Usage

### For LLM Generation

1. Copy `strategickhaos_product_build.yaml` content
2. Paste into Claude.ai or compatible LLM
3. Use prompt: "Use this YAML as the project spec and generate all defined deliverables."

### For Department Use

Each department can reference their specific brief/runbook:
- **Education:** `departments/education_brief.md`
- **Security Ops:** `departments/security_ops_runbook.md`
- **Infrastructure:** `departments/infra_cloud_runbook.md`
- **Finance/Legal:** `departments/finance_legal_brief.md`
- **Communications:** `departments/comms_outreach_brief.md`

---

*StrategicKhaos DAO LLC*
*Educational Swarm Platform*
