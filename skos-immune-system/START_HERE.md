# 🚀 START HERE - SKOS Immune System

**Welcome to the Sovereign Khaos Operating System (SKOS) Immune System!**

This package transforms potential infrastructure failures into autonomous self-healing capabilities.

## What Is This?

The SKOS Immune System is an autonomous, self-healing infrastructure monitor that:
- Detects problems before they cascade
- Heals issues without human intervention
- Gets stronger from every failure (antifragility)
- Runs entirely on YOUR hardware (sovereignty)

## 60-Second Quickstart

```bash
# 1. Deploy the immune system
./deploy.sh

# 2. Verify it's working
./test.sh

# Done! Your infrastructure now heals itself.
```

## What's In The Box?

| Component | Description |
|-----------|-------------|
| `coordinator/main.py` | The "brain" - receives alerts, decides actions |
| `agents/thermal_sentinel.py` | Monitors CPU/GPU temperatures |
| `docker-compose.yml` | Complete deployment stack |
| `deploy.sh` | One-command deployment |
| `test.sh` | Full verification suite |
| `config.yaml` | All configuration in one place |

## Architecture

```
Your Hardware (Nova/Lyra/Athena)
         ↓
Thermal Sentinel Agents (monitors temps)
         ↓ heartbeats + alerts
Antibody Coordinator (brain)
         ↓ commands
Healing Actions (throttle, redistribute, failover)
         ↓
Audit Log (immutable trail)
```

## Next Steps

1. **Read** [`QUICKSTART.md`](./docs/QUICKSTART.md) - Deploy in 60 seconds
2. **Review** [`README.md`](./docs/README.md) - Full technical documentation
3. **Customize** `config.yaml` - Adjust thresholds and policies
4. **Extend** - Add more antibody agents (storage, mesh, loops)

## Sovereignty Guaranteed

✅ **Your Hardware** - Runs on Nova/Lyra/Athena, not AWS  
✅ **Your Code** - You own every line, modify anything  
✅ **Your Data** - All logs stay on your infrastructure  
✅ **Your Rules** - Policies in config.yaml, you control  
✅ **Zero Vendor Lock-in** - No external dependencies  
✅ **Air-gap Capable** - Works completely offline

---

**Questions?** Check the [`README.md`](./docs/README.md) or open an issue.

**Welcome to SKOS v0.1.0, baby.** 💜⚡
