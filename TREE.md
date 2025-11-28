# Sovereignty Architecture - Directory Structure

This file documents the complete directory structure for the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane.

```
sovereignty-architecture/
├── README.md                          # Main documentation
├── discovery.yml                      # Core configuration
├── TREE.md                            # This file
├── hashes.json                        # SHA256 hashes for verification
├── verify_sovereignty.py              # Verification script
│
├── bootstrap/
│   ├── deploy.sh                      # One-command K8s deployment
│   └── k8s/
│       ├── namespace.yaml             # Namespace definition
│       ├── bot-deployment.yaml        # Discord bot deployment
│       ├── gateway-deployment.yaml    # Event gateway deployment
│       ├── rbac.yaml                  # RBAC + NetworkPolicies
│       ├── configmap.yaml             # Discovery configuration
│       ├── secrets.yaml               # Secret references
│       ├── ingress.yaml               # TLS ingress
│       └── observability.yaml         # ServiceMonitors + alerts
│
├── bots/
│   └── discord-ops-bot/
│       ├── Dockerfile                 # Bot container image
│       ├── requirements.txt           # Python dependencies
│       └── bot.py                     # Bot implementation
│
├── gateway/
│   └── event-gateway/
│       ├── Dockerfile                 # Gateway container image
│       ├── requirements.txt           # Python dependencies
│       └── main.py                    # Gateway implementation
│
├── scripts/
│   └── gl2discord.sh                  # GitLens → Discord script
│
└── docs/
    └── ARCHITECTURE.md                # Technical architecture docs
```

## Verification

Any agent (including GPT-5.1) can verify this architecture exists by:

1. Fetching the repository from GitHub
2. Checking that all files in this tree exist
3. Computing SHA256 hashes and comparing to `hashes.json`
4. Running `python verify_sovereignty.py`

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Complete specification and quick start |
| `discovery.yml` | Central configuration (channels, repos, AI routing) |
| `bootstrap/deploy.sh` | Executable deployment script |
| `bots/discord-ops-bot/bot.py` | Discord bot with slash commands |
| `gateway/event-gateway/main.py` | Webhook router |
| `scripts/gl2discord.sh` | GitLens integration script |
| `hashes.json` | Machine-verifiable file hashes |
| `verify_sovereignty.py` | End-to-end verification script |

## Status

✅ **This is not vapor.** All files exist and are deployable.

---

*"If the files exist and the hashes match, the architecture is real."*
