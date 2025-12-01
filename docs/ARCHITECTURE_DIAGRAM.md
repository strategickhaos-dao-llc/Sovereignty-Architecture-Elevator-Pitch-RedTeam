# System Architecture & Security Boundaries

This document provides visual representations of the Strategickhaos Sovereignty Architecture, showing what agents can access vs. what they cannot.

---

## 🏗️ High-Level Architecture

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          GITHUB ECOSYSTEM                         ┃
┃                     (Agent-Accessible Zone)                       ┃
┃                                                                   ┃
┃  ┌─────────────────────────────────────────────────────────┐    ┃
┃  │              GitHub Copilot Agents                      │    ┃
┃  │  • Read repository contents                             │    ┃
┃  │  • Create branches (copilot/*, agent/*)                 │    ┃
┃  │  • Open pull requests                                   │    ┃
┃  │  • Add comments and request reviews                     │    ┃
┃  │  ❌ CANNOT merge PRs                                    │    ┃
┃  │  ❌ CANNOT access secrets                               │    ┃
┃  │  ❌ CANNOT trigger deployments                          │    ┃
┃  └────────────────────┬────────────────────────────────────┘    ┃
┃                       │                                           ┃
┃                       ▼                                           ┃
┃  ┌─────────────────────────────────────────────────────────┐    ┃
┃  │              Repository (Source Code)                    │    ┃
┃  │  • Application code (.ts, .py, .js)                     │    ┃
┃  │  • Kubernetes manifests (YAML)                          │    ┃
┃  │  • Docker configurations                                │    ┃
┃  │  • CI/CD workflows (.github/workflows/)                 │    ┃
┃  │  • Documentation (Markdown)                             │    ┃
┃  │  ❌ NO secrets or credentials                           │    ┃
┃  └────────────────────┬────────────────────────────────────┘    ┃
┃                       │                                           ┃
┃                       ▼                                           ┃
┃  ┌─────────────────────────────────────────────────────────┐    ┃
┃  │              Pull Request Review                         │    ┃
┃  │  • Branch protection enforced                           │    ┃
┃  │  • CODEOWNERS approval required                         │    ┃
┃  │  • Status checks must pass                              │    ┃
┃  │  • Agent PR validation runs                             │    ┃
┃  └────────────────────┬────────────────────────────────────┘    ┃
┃                       │                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                        │
            ╔═══════════▼═══════════╗
            ║   HUMAN APPROVAL      ║ ◀─── YOU control this gate
            ║   • Review code       ║
            ║   • Approve PR        ║
            ║   • Merge to main     ║
            ╚═══════════╤═══════════╝
                        │
┏━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                       │          CI/CD LAYER                      ┃
┃                       ▼          (Automated)                      ┃
┃  ┌─────────────────────────────────────────────────────────┐    ┃
┃  │              GitHub Actions Workflows                    │    ┃
┃  │  • Build Docker images                                  │    ┃
┃  │  • Run tests and security scans                         │    ┃
┃  │  • Push to container registry                           │    ┃
┃  │  • Inject secrets from GitHub Secrets                   │    ┃
┃  │  • Trigger deployments to environments                  │    ┃
┃  └────────────────────┬────────────────────────────────────┘    ┃
┃                       │                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                        │
                        ├────────────────┬──────────────────┐
                        │                │                  │
            ╔═══════════▼═══════╗   ╔════▼══════╗   ╔══════▼═══════╗
            ║  DEPLOYMENT GATES ║   ║  STAGING  ║   ║  PRODUCTION  ║
            ║  • Wait timers    ║   ║   GATE    ║   ║     GATE     ║
            ║  • Approvals req  ║   ║ 2-min wait║   ║ 5-min wait   ║
            ║  • Env. secrets   ║   ║ Optional  ║   ║ Required     ║
            ║  • Access control ║   ║  approval ║   ║  approval    ║
            ╚═══════════╤═══════╝   ╚════╤══════╝   ╚══════╤═══════╝
                        │                │                  │
┏━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━┿━━━━━━┓
┃                       │  INFRASTRUCTURE│                  │       ┃
┃                       ▼      LAYER     ▼                  ▼       ┃
┃  ┌──────────────────────┐  ┌───────────────┐  ┌──────────────┐  ┃
┃  │   LAB / LOCAL        │  │  DEV CLUSTER  │  │ PROD CLUSTER │  ┃
┃  │   • K8s Desktop      │  │  (Cloud K8s)  │  │ (Cloud K8s)  │  ┃
┃  │   • Docker Desktop   │  │               │  │              │  ┃
┃  │   • Your laptop      │  │ • ops-dev ns  │  │ • ops-prod   │  ┃
┃  │                      │  │ • Auto-deploy │  │ • Manual     │  ┃
┃  │  ❌ NO kubeconfig   │  │   optional    │  │   only       │  ┃
┃  │     in GitHub       │  │ • Test data   │  │ • Customer   │  ┃
┃  │  ✅ Manual kubectl  │  │               │  │   facing     │  ┃
┃  │     apply           │  │               │  │              │  ┃
┃  └──────────────────────┘  └───────────────┘  └──────────────┘  ┃
┃           ▲                        ▲                   ▲          ┃
┃           │                        │                   │          ┃
┃      YOUR CONTROL              CI/CD DEPLOY       CI/CD DEPLOY    ┃
┃      (kubectl)                 (w/ DEV_KUBECONFIG) (w/ approval)  ┃
┃                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

KEY:
┏━━━┓ = Security boundary
╔═══╗ = Human gate / control point
┌───┐ = System component
  ▼   = Automated flow
  │   = Manual control
  ❌  = Forbidden / not allowed
  ✅  = Allowed / recommended
```

---

## 🔐 Agent Access Boundaries

### What Agents Can Access ✅

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ACCESSIBLE ZONE                     │
│                                                              │
│  GitHub Repository:                                          │
│  ├── Source code (read/edit via PR)                         │
│  ├── Issues (read/comment)                                  │
│  ├── Pull requests (create/update)                          │
│  ├── Branches (create copilot/*, agent/*)                   │
│  ├── Documentation (read/edit via PR)                       │
│  └── Configuration files (read/edit via PR)                 │
│                                                              │
│  Allowed Actions:                                            │
│  ├── Create feature branches                                │
│  ├── Commit to non-protected branches                       │
│  ├── Open pull requests                                     │
│  ├── Request reviews                                        │
│  ├── Add PR comments                                        │
│  └── Label issues/PRs                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### What Agents CANNOT Access ❌

```
┌─────────────────────────────────────────────────────────────┐
│                  AGENT FORBIDDEN ZONE                        │
│                                                              │
│  Local Systems:                                              │
│  ├── ❌ Kubernetes Desktop / k3s / Docker Desktop           │
│  ├── ❌ Local kubeconfig files (~/.kube/config)             │
│  ├── ❌ Your laptop/desktop machines                        │
│  ├── ❌ Network devices (routers, switches)                 │
│  └── ❌ Gaming consoles / IoT devices                       │
│                                                              │
│  Cloud Infrastructure:                                       │
│  ├── ❌ Kubernetes clusters (prod, staging, dev)            │
│  ├── ❌ Cloud provider accounts (AWS, GCP, Azure)           │
│  ├── ❌ Databases and data stores                           │
│  ├── ❌ Load balancers and networking                       │
│  └── ❌ Storage buckets and volumes                         │
│                                                              │
│  Secrets & Credentials:                                      │
│  ├── ❌ GitHub Secrets                                      │
│  ├── ❌ HashiCorp Vault                                     │
│  ├── ❌ API keys and tokens                                 │
│  ├── ❌ TLS certificates and private keys                   │
│  └── ❌ Kubeconfig files with cluster access                │
│                                                              │
│  Git Operations:                                             │
│  ├── ❌ Merge pull requests                                 │
│  ├── ❌ Push to main/develop/release/* branches             │
│  ├── ❌ Delete branches                                     │
│  ├── ❌ Modify repository settings                          │
│  └── ❌ Manage webhooks or GitHub Apps                      │
│                                                              │
│  Deployments:                                                │
│  ├── ❌ Trigger GitHub Actions workflows                    │
│  ├── ❌ Deploy to any environment                           │
│  ├── ❌ Run kubectl commands                                │
│  ├── ❌ Scale deployments                                   │
│  └── ❌ Restart pods or services                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛣️ Data Flow: Agent PR to Production

```
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 1: Agent Edits Code                                 │
     │ • Agent analyzes issue or feature request                │
     │ • Creates branch: copilot/add-feature-x                  │
     │ • Edits files, adds tests, updates docs                  │
     │ • Commits changes to feature branch                      │
     └──────────────────────┬──────────────────────────────────┘
                            │
                            ▼
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 2: Agent Opens Pull Request                         │
     │ • PR title: "Add feature X"                              │
     │ • PR description: Explains changes                       │
     │ • Requests review from @Strategickhaos                   │
     │ • Agent CANNOT merge this PR                             │
     └──────────────────────┬──────────────────────────────────┘
                            │
                            ▼
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 3: Automated Checks Run                             │
     │ • Agent PR validation workflow                           │
     │ • Build and test workflow                                │
     │ • Security scan (Gitleaks)                               │
     │ • CodeQL analysis (if configured)                        │
     └──────────────────────┬──────────────────────────────────┘
                            │
                 ┌──────────┴──────────┐
                 │  ❌ Checks fail?    │
                 │  • PR blocked       │
                 │  • Cannot merge     │
                 │  • Fix required     │
                 └─────────────────────┘
                            │
                            ▼ ✅ All checks pass
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 4: Human Review                                     │
     │ • @Strategickhaos reviews code                          │
     │ • Checks logic, security, impact                         │
     │ • Requests changes OR approves                           │
     │ • This is the CRITICAL CONTROL POINT                     │
     └──────────────────────┬──────────────────────────────────┘
                            │
                            ▼ ✅ Approved
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 5: Human Merges PR                                  │
     │ • Human clicks "Merge pull request"                      │
     │ • Changes merged to main branch                          │
     │ • Feature branch deleted (optional)                      │
     └──────────────────────┬──────────────────────────────────┘
                            │
                            ▼
     ┌─────────────────────────────────────────────────────────┐
     │ STEP 6: CI/CD Triggered                                  │
     │ • GitHub Actions workflow runs automatically             │
     │ • Builds Docker images                                   │
     │ • Runs full test suite                                   │
     │ • Pushes images to registry                              │
     └──────────────────────┬──────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
     ┌─────────────────────┐ ┌─────────────────────────┐
     │ Deploy to DEV       │ │ Deploy to PROD          │
     │ • Automatic         │ │ • Manual trigger only   │
     │ • On push to develop│ │ • Requires approval     │
     │ • No approval needed│ │ • Wait timer: 5 min     │
     └─────────────────────┘ └─────────────────────────┘
```

**Key Insight:** Agents edit → Humans approve → Automation deploys

---

## 🏰 The Three Gates Model

```
╔══════════════════════════════════════════════════════════════════╗
║                        THE THREE GATES                            ║
║                                                                   ║
║  Think of your infrastructure as a castle with three gates.       ║
║  Agents can knock on Gate 1, but cannot pass through any gate.   ║
╚══════════════════════════════════════════════════════════════════╝

                         🏰 THE CASTLE

    ┌─────────────────────────────────────────────────┐
    │                   GATE 1                        │
    │              The Repository                     │
    │                                                 │
    │  🚪 Door: Pull Request                         │
    │  🔑 Key Holder: YOU (human maintainer)        │
    │                                                 │
    │  Agent Action:                                 │
    │    ✅ Can knock (open PR)                     │
    │    ❌ Cannot enter (cannot merge)             │
    │                                                 │
    │  Protection:                                   │
    │    • Branch protection rules                   │
    │    • CODEOWNERS requirements                   │
    │    • Status checks must pass                   │
    └────────────────┬────────────────────────────────┘
                     │ Human approves & merges
                     ▼
    ┌─────────────────────────────────────────────────┐
    │                   GATE 2                        │
    │              The CI/CD Pipeline                 │
    │                                                 │
    │  🚪 Door: Merge Event                          │
    │  🔑 Key Holder: GitHub Actions (with secrets) │
    │                                                 │
    │  Agent Action:                                 │
    │    ❌ Cannot see (outside the castle)         │
    │    ❌ Cannot trigger                           │
    │                                                 │
    │  Protection:                                   │
    │    • Workflow permissions                      │
    │    • Environment secrets                       │
    │    • Build/test validation                     │
    └────────────────┬────────────────────────────────┘
                     │ Workflow runs
                     ▼
    ┌─────────────────────────────────────────────────┐
    │                   GATE 3                        │
    │            The Infrastructure                   │
    │                                                 │
    │  🚪 Door: Deployment Command                   │
    │  🔑 Key Holder: K8s API (with RBAC)           │
    │                                                 │
    │  Agent Action:                                 │
    │    ❌ Cannot see (too far from castle)        │
    │    ❌ Cannot access                            │
    │                                                 │
    │  Protection:                                   │
    │    • Kubernetes RBAC                           │
    │    • Network policies                          │
    │    • Namespace isolation                       │
    └─────────────────────────────────────────────────┘

Result: Agents propose changes (knock on door),
        but you hold all three keys.
```

---

## 🌐 Multi-Platform View

```
┌──────────────────────────────────────────────────────────────────┐
│                   YOUR MULTI-PLATFORM SETUP                       │
│                                                                   │
│  GitHub                GitLab              Local                 │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐          │
│  │ Repos    │         │ Repos    │       │ K8s Desk │          │
│  │ Actions  │         │ CI/CD    │       │ Docker   │          │
│  │ Agents   │◄────┐   │          │       │          │          │
│  └──────────┘     │   └──────────┘       └──────────┘          │
│                   │                             ▲                │
│  Cloud Providers  │                             │                │
│  ┌──────────┐    │   ┌──────────┐              │                │
│  │ AWS      │    │   │ GCP      │              │                │
│  │ • K8s    │    │   │ • Storage│              │                │
│  │ • DBs    │    │   └──────────┘              │                │
│  └──────────┘    │                              │                │
│                  │                              │                │
│  Docker Hub      │   Discord                   │                │
│  ┌──────────┐   │   ┌──────────┐              │                │
│  │ Images   │   │   │ Bots     │              │                │
│  │ Registry │   │   │ Webhooks │              │                │
│  └──────────┘   │   └──────────┘              │                │
│                  │                              │                │
│  ┌───────────────▼──────────────┐              │                │
│  │  GITHUB COPILOT AGENTS        │              │                │
│  │  • Connected to GitHub only   │              │                │
│  │  • Cannot see other platforms │              │                │
│  │  • Cannot control deployments │              │                │
│  └───────────────────────────────┘              │                │
│                                                  │                │
│  All platforms can READ from GitHub             │                │
│  (via CI/CD pulling code)                       │                │
│                                                  │                │
│  Only YOU can directly control local/cloud      │                │
│  infrastructure via kubectl/cloud CLIs   ───────┘                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

Key Insight: Having multiple platforms doesn't mean
            agents have access to them all.
            Agents only see GitHub.
```

---

## 📊 Permission Matrix

| Resource | Agent | Human | CI/CD |
|----------|-------|-------|-------|
| **GitHub Repo** |
| Read code | ✅ | ✅ | ✅ |
| Create branches | ✅ copilot/* only | ✅ All | ✅ All |
| Open PRs | ✅ | ✅ | ✅ |
| Merge PRs | ❌ | ✅ | ⚠️ With approval |
| Push to main | ❌ | ❌ Protected | ❌ |
| **Secrets** |
| Read GitHub Secrets | ❌ | ❌ Admin only | ✅ In workflow |
| Read kubeconfig | ❌ | ✅ Local only | ✅ From secret |
| Modify secrets | ❌ | ✅ Admin only | ❌ |
| **Infrastructure** |
| View K8s resources | ❌ | ✅ | ✅ Via kubeconfig |
| Deploy to K8s | ❌ | ✅ | ✅ Via workflow |
| Scale deployments | ❌ | ✅ | ✅ Via workflow |
| Delete resources | ❌ | ✅ | ⚠️ With approval |
| **Local Systems** |
| Access laptop | ❌ | ✅ | ❌ |
| Run kubectl locally | ❌ | ✅ | ❌ |
| Access K8s Desktop | ❌ | ✅ | ❌ |

Legend:
- ✅ = Allowed
- ❌ = Not allowed
- ⚠️ = Conditional (approval required)

---

## 🎯 Summary

### Agents Are Connected To:
- ✅ GitHub repository (read/PR workflow)
- ✅ Issues and pull requests
- ✅ Code review process

### Agents Are NOT Connected To:
- ❌ Your local machines
- ❌ Kubernetes clusters
- ❌ Cloud providers
- ❌ Deployment pipelines
- ❌ Production systems

### The Control Flow:
1. **Agent** → Edits code, opens PR
2. **Human** → Reviews, approves, merges
3. **CI/CD** → Builds, tests, deploys
4. **Infrastructure** → Receives deployment

**You are the gate at step 2. Without your approval, nothing happens.**

---

## 📚 Related Documentation

- [AGENT_AUTHORIZATION_MODEL.md](../AGENT_AUTHORIZATION_MODEL.md) - Full permission model
- [SECURITY.md](../SECURITY.md) - Security policies
- [governance/agent_permissions.yaml](../governance/agent_permissions.yaml) - Explicit permissions

---

**Last Updated:** 2025-11-21  
**Maintained By:** Strategickhaos DAO LLC
