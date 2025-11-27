# GitHub App: Strategickhaos Sovereignty Control Plane

**App ID:** [YOUR_APP_ID] *(Available in GitHub App settings after registration)*
**Installation:** https://github.com/apps/strategickhaos-sovereignty-control-plane

## Purpose
Automated provenance, governance tracking, and compliance automation for
Strategickhaos DAO LLC and ValorYield Engine operations.

## Permissions
See: https://github.com/settings/apps/strategickhaos-sovereignty-control-plane

## Integration
Webhooks are processed by the SwarmGate sovereign infrastructure.

---

## 🏛️ Legal Entity

- **Entity**: Wyoming DAO LLC §17-31-101
- **EIN**: 39-2900295
- **License**: MIT
- **Treasury**: Navy Federal Credit Union (NFCU)

## ✅ Repository Permissions

| Permission | Access | Purpose |
|------------|--------|---------|
| Contents | Read & Write | Releases, tags |
| Issues | Read & Write | Governance |
| Pull requests | Read & Write | Reviews |
| Workflows | Read & Write | CI/CD |
| Metadata | Read-only | Mandatory |

## ✅ Organization Permissions

| Permission | Access | Purpose |
|------------|--------|---------|
| Administration | Read & Write | Org management |
| Members | Read & Write | Team coordination |
| Self-hosted runners | Read & Write | Infrastructure |

## ✅ Account Permissions

| Permission | Access | Purpose |
|------------|--------|---------|
| GPG keys | Read & Write | Signing automation |

## 📡 Subscribed Events

- **Push** - Detect commits
- **Release** - Auto-provenance
- **Pull request** - Governance tracking
- **Issues** - Governance tracking
- **Workflow run** - CI/CD monitoring
- **Create** - Tag/branch creation
- **Repository** - Repo lifecycle

## 🔧 Configuration

### Callback URL (Development)
```
https://strategickhaos.github.io/Sovereignty-Architecture-Elevator-Pitch/callback
```

### Callback URL (Production)
```
https://swarmgate.strategickhaos.ai/auth/callback
```

### Webhook URL (Development)
Use [smee.io](https://smee.io/) for local development.

### Webhook URL (Production)
```
https://swarmgate.strategickhaos.ai/webhooks/github
```

## 🔐 Security Notes

- Webhook secret should be generated with: `openssl rand -hex 32`
- Store the private key securely, e.g.: `$HOME/.strategickhaos/secrets/github-app-key.pem`
- Store credentials in a secure config, e.g.: `$HOME/.strategickhaos/secrets/github-app-config.yaml`
- File permissions should be set to `600` for config files and `700` for directories

## 📋 Post-Registration Checklist

```
☐ App ID saved
☐ Client ID saved
☐ Client Secret saved
☐ Private key downloaded and secured
☐ Webhook secret generated and saved
☐ App installed on target repository
```

## ⚠️ Disclaimer

- **NOT operational** - Research/experimental only
- **NOT accepting funds** - Pure academic capstone
- **NOT investment advice** - No financial services
- AI-governed, code-enforced perpetual philanthropy research
- 7% irrevocable allocation to St. Jude, MSF, veterans (when operational)

---

*Part of the SwarmGate v1.0 sovereignty stack*
