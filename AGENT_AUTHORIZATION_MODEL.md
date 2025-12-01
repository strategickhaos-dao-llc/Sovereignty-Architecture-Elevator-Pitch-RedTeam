# Agent Authorization Model
## Safe Permissions for GitHub Copilot Agents + K8s + Multi-Platform Infrastructure

**Version:** 1.0  
**Last Updated:** 2025-11-21  
**Owner:** Domenic Garza / Strategickhaos DAO LLC

---

## 🎯 Executive Summary

This document defines the **authorization boundaries** and **permission model** for GitHub Copilot Agents operating within the Strategickhaos ecosystem. It clarifies what agents can and cannot access, establishes security boundaries, and implements blast-radius control.

### Key Principles

1. **Agents open PRs only** - Never commit directly to protected branches
2. **Human-in-the-loop** - All production changes require human review and approval
3. **Separation of concerns** - Lab clusters are isolated from production clusters
4. **Explicit permissions** - Agents have no access unless explicitly granted
5. **Audit everything** - All agent actions are logged and traceable

---

## 🔒 What Agents CAN Access

### GitHub Repository Scope

Agents authorized in this organization have access to:

✅ **Read Operations:**
- Read repository code, issues, and PRs
- View commit history and branches
- Read repository metadata and configuration
- Access public documentation

✅ **Write Operations (via PR only):**
- Create branches (prefixed with `copilot/*` or `agent/*`)
- Open pull requests
- Add comments to PRs and issues
- Update PR descriptions
- Request reviews

✅ **File Operations (via PR only):**
- Edit code files
- Create new files
- Modify configuration files (YAML, JSON, etc.)
- Update documentation (Markdown files)
- Edit Kubernetes manifests and Helm charts

### What This Means

Agents can **propose changes** but cannot:
- ❌ Merge PRs (requires human approval)
- ❌ Push directly to `main`, `develop`, or `release/*` branches
- ❌ Delete branches without approval
- ❌ Modify GitHub repository settings
- ❌ Create or delete repositories
- ❌ Manage organization members or teams

---

## 🚫 What Agents CANNOT Access

### Infrastructure & Runtime

Agents have **ZERO direct access** to:

❌ **Local Infrastructure:**
- Your Kubernetes Desktop cluster
- Your k3s or Docker Desktop installations
- Your local `~/.kube/config` file
- Your Windows/Mac/Linux machines
- Your network routers (Starlink, Verizon, etc.)
- Your gaming consoles (PS5, Xbox)

❌ **Cloud Infrastructure:**
- Production Kubernetes clusters (unless deployed via approved CI/CD)
- AWS/Azure/GCP accounts
- Database servers
- API gateways
- Load balancers
- DNS records

❌ **Secrets & Credentials:**
- Kubeconfig files
- API tokens
- SSH keys
- Database passwords
- Service account keys
- TLS certificates

### The Agent → Infrastructure Wall

```
┌─────────────────────────────────────────────────────────────┐
│                     GITHUB REPOSITORY                        │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ Agent Edits  │────────▶│  Pull Request │                 │
│  │  Code/YAML   │         │  (Review Req) │                 │
│  └──────────────┘         └──────────────┘                 │
│                                   │                          │
└───────────────────────────────────┼──────────────────────────┘
                                    │
                        ╔═══════════▼═══════════╗
                        ║   HUMAN REVIEW        ║
                        ║   + APPROVAL          ║
                        ╚═══════════╤═══════════╝
                                    │
                        ┌───────────▼────────────┐
                        │   Merge to main        │
                        └───────────┬────────────┘
                                    │
                        ┌───────────▼────────────┐
                        │  GitHub Actions        │
                        │  (Automated CI/CD)     │
                        └───────────┬────────────┘
                                    │
                        ╔═══════════▼════════════╗
                        ║  INFRASTRUCTURE        ║
                        ║  • K8s Clusters        ║
                        ║  • Cloud Resources     ║
                        ║  • Production Systems  ║
                        ╚════════════════════════╝
```

**Key Point:** Agents edit code. Humans approve. CI/CD deploys. Agents never touch infrastructure directly.

---

## 🏗️ Architecture: What's Connected vs Not Connected

### System Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                          GITHUB ECOSYSTEM                            │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ Copilot Agents  │  │  Repositories   │  │  GitHub Actions │    │
│  │                 │  │                 │  │                 │    │
│  │ • Code editing  │  │ • Source code   │  │ • CI/CD pipelines│   │
│  │ • PR creation   │──│ • K8s manifests │──│ • Build & test  │   │
│  │ • Issue mgmt    │  │ • Helm charts   │  │ • Docker build  │    │
│  └─────────────────┘  └─────────────────┘  └────────┬────────┘    │
│                                                      │              │
└──────────────────────────────────────────────────────┼──────────────┘
                                                       │
                         ╔═════════════════════════════▼════════╗
                         ║   DEPLOYMENT GATE                     ║
                         ║   • Manual approval required          ║
                         ║   • Secrets injected here             ║
                         ║   • KUBECONFIG from GitHub Secrets    ║
                         ╚═════════════════════════════╤═════════╝
                                                       │
               ┌───────────────────────────────────────┼───────────────────┐
               │                                       │                   │
               ▼                                       ▼                   ▼
    ┌─────────────────────┐              ┌──────────────────┐  ┌─────────────────┐
    │  LAB CLUSTER        │              │  STAGING CLUSTER │  │  PROD CLUSTER   │
    │  (Local K8s)        │              │  (Cloud K8s)     │  │  (Cloud K8s)    │
    │                     │              │                  │  │                 │
    │ • Auto-deploy on    │              │ • Auto on merge  │  │ • Manual only   │
    │   PR merge (opt)    │              │   to develop     │  │ • Approval req  │
    │ • No secrets in GH  │              │ • Limited scope  │  │ • Full audit    │
    │ • Pull from GH      │              │                  │  │                 │
    │   manually          │              │                  │  │                 │
    └─────────────────────┘              └──────────────────┘  └─────────────────┘
         ↑                                       ↑                      ↑
         │                                       │                      │
         │ YOU control with                      │                      │
         │ kubectl locally                       │                      │
         │                                       │                      │
    ┌────┴────────┐                    ┌────────┴──────┐      ┌────────┴──────┐
    │ Your Local  │                    │ Cloud Account │      │ Cloud Account │
    │ Machines    │                    │ (Dev/Test)    │      │ (Production)  │
    │             │                    │               │      │               │
    │ • K8s Desk  │                    │ • Lower env   │      │ • Critical    │
    │ • Docker    │                    │ • Cheaper     │      │ • High avail  │
    │ • Dev tools │                    │ • Isolated    │      │ • Multi-AZ    │
    └─────────────┘                    └───────────────┘      └───────────────┘
```

### Key Insights

1. **Agents live in GitHub** - They can't jump out to your laptop/cloud
2. **GitHub Actions is the bridge** - Only way code reaches infrastructure
3. **Secrets are the keys** - Stored in GitHub Secrets, injected at deploy time
4. **You control the gates** - Merge, approve, and trigger deployments

---

## 🔐 Permission Model by Environment

### Lab / Local Development

**Purpose:** Safe experimentation, rapid iteration, agent learning

| Resource | Agent Access | Human Access | Auto-Deploy |
|----------|-------------|--------------|-------------|
| Local K8s cluster | ❌ None | ✅ Full | ⚠️ Optional |
| Kubeconfig | ❌ Never in GitHub | ✅ Local only | N/A |
| Code via PR | ✅ Propose changes | ✅ Review & merge | N/A |
| Manifests | ✅ Edit via PR | ✅ `kubectl apply` | ⚠️ Optional |

**Recommended Pattern:**
```bash
# Agent opens PR with K8s manifest changes
# You review and merge the PR
# You manually apply to your local cluster
git pull origin main
kubectl apply -f bootstrap/k8s/
```

**Optional Auto-Deploy:**
If you want to auto-apply to local cluster on merge:
1. Keep it a **separate repo** or **separate branch**
2. Use GitHub Actions with self-hosted runner on your machine
3. Never commit kubeconfig to repo (mount as runner secret)

### Staging / Dev Cloud

**Purpose:** Pre-production validation, integration testing

| Resource | Agent Access | Human Access | Auto-Deploy |
|----------|-------------|--------------|-------------|
| Dev K8s cluster | ❌ None | ✅ Full | ✅ On merge to `develop` |
| Kubeconfig | ❌ None | ✅ Via GitHub Secret | N/A |
| Code via PR | ✅ Propose changes | ✅ Review & merge | N/A |
| Deployment | ❌ None | ⚠️ Via workflow | ✅ Automatic |

**Workflow:**
```yaml
# .github/workflows/deploy-dev.yml
on:
  push:
    branches: [develop]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: dev  # GitHub environment with approval (optional)
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Dev K8s
        env:
          KUBECONFIG: ${{ secrets.DEV_KUBECONFIG }}
        run: |
          kubectl apply -f bootstrap/k8s/
```

### Production

**Purpose:** Customer-facing systems, revenue-critical

| Resource | Agent Access | Human Access | Auto-Deploy |
|----------|-------------|--------------|-------------|
| Prod K8s cluster | ❌ None | ✅ Full | ❌ Manual only |
| Kubeconfig | ❌ None | ✅ Via GitHub Secret | N/A |
| Code via PR | ✅ Propose changes | ✅ **Required review** | N/A |
| Deployment | ❌ None | ✅ Manual trigger | ⚠️ Approval required |

**Required Safeguards:**
1. **Branch protection** on `main`:
   - Require PR reviews (1+ approvers)
   - Require status checks to pass
   - No force pushes
   - No deletions

2. **GitHub Environment** with protection rules:
   - Required reviewers: `@Strategickhaos-admins`
   - Wait timer: 5 minutes
   - Deployment branches: `main` only

3. **Manual workflow dispatch:**
```yaml
# .github/workflows/deploy-prod.yml
on:
  workflow_dispatch:  # Manual trigger only
    inputs:
      confirm:
        description: 'Type "DEPLOY" to confirm'
        required: true
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    if: github.event.inputs.confirm == 'DEPLOY'
```

---

## 🛡️ Security Controls & Blast Radius

### 1. Repository Level

**Branch Protection (`main` and `develop`):**
```yaml
# Enforced via GitHub Settings → Branches
protection:
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  required_status_checks:
    strict: true
    contexts:
      - "CI / build-and-test"
      - "Security / CodeQL"
  enforce_admins: true
  restrictions:
    users: []
    teams: ["admins"]
  allow_force_pushes: false
  allow_deletions: false
```

**CODEOWNERS:**
```
# Require review from specific people for critical paths
/bootstrap/k8s/           @Strategickhaos-admins
/.github/workflows/       @Strategickhaos-admins
/governance/              @Strategickhaos-admins
/SECURITY.md              @Strategickhaos-admins
```

### 2. CI/CD Level

**Secret Management:**
- All secrets stored in GitHub Secrets (encrypted at rest)
- Secrets never logged or printed
- Use environment-specific secrets (`DEV_KUBECONFIG`, `PROD_KUBECONFIG`)
- Rotate secrets quarterly

**Deployment Environments:**
```yaml
# GitHub Environments with protection rules
environments:
  - name: dev
    protection_rules: []  # Auto-deploy OK
  
  - name: staging
    protection_rules:
      - type: wait_timer
        minutes: 2
  
  - name: production
    protection_rules:
      - type: required_reviewers
        reviewers: ["@strategickhaos-admins"]
      - type: wait_timer
        minutes: 5
      - type: branch_policy
        allowed_branches: ["main"]
```

### 3. Kubernetes Level

**RBAC Least Privilege:**
```yaml
# bot-deployment.yaml already implements:
# - ServiceAccount with limited permissions
# - ClusterRole with explicit verbs and resources
# - No create/delete for critical resources
# - Network policies for pod isolation
# See: bootstrap/k8s/rbac.yaml
```

**Namespace Isolation:**
- `ops-dev` - Development bots and services
- `ops-staging` - Staging bots and services  
- `ops-prod` - Production bots and services
- No cross-namespace communication except via explicit NetworkPolicy

**Resource Quotas:**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ops-quota
  namespace: ops-prod
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 2Gi
    limits.cpu: "4"
    limits.memory: 4Gi
```

### 4. Audit & Observability

**What Gets Logged:**
- All agent PR creations and edits
- All PR approvals and merges
- All deployment triggers
- All kubectl commands executed by CI/CD
- All pod creations and deletions in prod

**Where Logs Go:**
- GitHub Actions logs (retained 90 days)
- Kubernetes audit logs → Loki
- Discord notifications → `#alerts` and `#deployments`
- Alertmanager → PagerDuty (for prod incidents)

**Metrics:**
- Time from PR to deploy
- Number of agent-created PRs per day
- Success/failure rate of deployments
- MTTR (Mean Time To Recovery)

---

## 🚦 Agent Workflow Examples

### Safe Pattern: Agent Edits Infrastructure Code

1. **Agent creates branch:**
   ```
   Branch: copilot/update-deployment-resources
   ```

2. **Agent edits manifest:**
   ```yaml
   # bootstrap/k8s/bot-deployment.yaml
   resources:
     requests:
       memory: "512Mi"  # was 256Mi
   ```

3. **Agent opens PR:**
   - Title: "Increase bot memory to 512Mi"
   - Description: Explains why (e.g., OOMKilled events observed)
   - Labels: `infrastructure`, `kubernetes`

4. **Human reviews:**
   - Checks memory usage metrics
   - Verifies cost impact
   - Approves or requests changes

5. **Human merges PR:**
   - Code merged to `main`

6. **Optional: Auto-deploy to dev:**
   - GitHub Actions triggered
   - Deploys to `ops-dev` namespace automatically

7. **Manual deploy to prod:**
   - Human triggers workflow
   - Reviews approval required
   - Deploys to `ops-prod` namespace

### Unsafe Pattern (Prevented by This Model)

❌ **Agent commits directly to main** - Prevented by branch protection  
❌ **Agent runs kubectl** - Agent has no kubeconfig or cluster access  
❌ **Agent merges own PR** - Requires human approval  
❌ **Agent deploys to prod** - No workflow_dispatch permission  
❌ **Agent accesses secrets** - Secrets not visible to agents  

---

## 🎓 Mental Model: The Three Gates

Think of your infrastructure as a medieval castle with three gates:

### Gate 1: The Repository (GitHub)
- **Guarded by:** Branch protection, CODEOWNERS
- **Agents can:** Knock on the door (open PR)
- **Agents cannot:** Walk through (merge)
- **Key holder:** You (the maintainer)

### Gate 2: The CI/CD Pipeline (GitHub Actions)
- **Guarded by:** Workflow permissions, environment secrets
- **Agents can:** Nothing (they're outside the castle)
- **Triggers:** Merge to main, manual dispatch
- **Key holder:** GitHub Actions (with your secrets)

### Gate 3: The Infrastructure (Kubernetes)
- **Guarded by:** RBAC, network policies, namespaces
- **Agents can:** Nothing (too far from the castle)
- **Deploys via:** kubectl with kubeconfig from secrets
- **Key holder:** K8s API server (with your RBAC rules)

**Result:** Agents can draft the plans (code changes), but you approve the plans, and CI/CD executes them. Agents never touch the castle.

---

## ✅ Validation Checklist

Use this checklist to verify your setup is safe:

### Repository Configuration
- [ ] Branch protection enabled on `main` and `develop`
- [ ] Required reviews: 1+ approvers
- [ ] CODEOWNERS file exists and covers critical paths
- [ ] No admin bypass on branch protection
- [ ] Agent GitHub App scoped to repository (not org-wide admin)

### CI/CD Configuration
- [ ] Kubeconfig never committed to repository
- [ ] All sensitive values in GitHub Secrets
- [ ] Workflows use `environment:` for prod deploys
- [ ] Production requires manual `workflow_dispatch`
- [ ] Secrets rotated and documented

### Kubernetes Configuration
- [ ] RBAC implemented with least privilege
- [ ] Network policies restrict pod communication
- [ ] Resource quotas prevent resource exhaustion
- [ ] Separate namespaces for dev/staging/prod
- [ ] Audit logging enabled

### Observability
- [ ] Discord notifications on deploy success/failure
- [ ] Kubernetes audit logs flowing to Loki
- [ ] Prometheus scraping all components
- [ ] Alertmanager routing critical alerts
- [ ] PagerDuty integration for prod incidents

### Documentation
- [ ] This document (`AGENT_AUTHORIZATION_MODEL.md`) up to date
- [ ] Architecture diagrams reflect reality
- [ ] Runbooks exist for common operations
- [ ] Incident response plan documented
- [ ] Security contacts listed in `SECURITY.md`

---

## 🆘 What If Things Go Wrong?

### Scenario 1: Agent opens bad PR (wrong config, buggy code)

**Impact:** Zero. PR not merged yet.  
**Action:** Review, comment, reject, close PR.  
**Prevention:** Better agent prompts, more context.

### Scenario 2: Bad PR merged to main (human error)

**Impact:** Code in repo, not deployed yet.  
**Action:** 
1. Revert commit: `git revert <sha>`
2. Open PR with revert
3. Merge revert
**Prevention:** More reviewers, better tests, staging environment.

### Scenario 3: Bad deploy to dev/staging

**Impact:** Dev/staging broken, no customer impact.  
**Action:**
1. Rollback deployment: `kubectl rollout undo deployment/discord-ops-bot -n ops-dev`
2. Fix code, open new PR
3. Deploy fix
**Prevention:** Better testing, canary deploys, health checks.

### Scenario 4: Bad deploy to prod (worst case)

**Impact:** Customer-facing issue, potential downtime.  
**Action:**
1. **Immediate:** Rollback: `kubectl rollout undo deployment/discord-ops-bot -n ops-prod`
2. Verify service health: `kubectl get pods -n ops-prod`
3. Check logs: `kubectl logs -f deployment/discord-ops-bot -n ops-prod`
4. Alert team via Discord `#alerts`
5. Document incident, postmortem
**Prevention:** 
- Staging deploy first, wait 24h
- Canary deploy (10% → 50% → 100%)
- Automated rollback on error rate spike
- Require 2 approvers for prod deploys

### Scenario 5: Secrets leaked (GitHub Actions logs)

**Impact:** Potential credential compromise.  
**Action:**
1. **Immediate:** Rotate all secrets
2. Audit access logs for misuse
3. Review Actions workflows for log leaks
4. Update workflows to redact secrets
**Prevention:**
- Never `echo` secrets
- Use `::add-mask::` in Actions
- Regular secret rotation (quarterly)
- Alerts on secret access

---

## 📚 Additional Resources

### Internal Documentation
- [Architecture Diagrams](./ARCHITECTURE.md) *(to be created)*
- [Security Policy](./SECURITY.md)
- [Vault Security Playbook](./VAULT_SECURITY_PLAYBOOK.md)
- [Governance Access Matrix](./governance/access_matrix.yaml)

### GitHub Documentation
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Environments for Deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [GitHub Secrets Management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Apps Permissions](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/choosing-permissions-for-a-github-app)

### Kubernetes Documentation
- [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)

---

## 🔄 Review & Update Cycle

This document should be reviewed and updated:

- **Quarterly:** Review permissions, update diagrams
- **After incidents:** Document new scenarios, improve controls
- **On architecture changes:** New clusters, new agents, new platforms
- **Before onboarding:** Ensure new team members understand model

**Last Review:** 2025-11-21  
**Next Review:** 2026-02-21  
**Reviewed By:** Domenic Garza

---

## 📞 Questions or Concerns?

If you're unsure whether an agent action is safe, or if you need to expand agent permissions:

1. **Review this document** for common scenarios
2. **Check with team** in Discord `#agents` channel
3. **Open an issue** in this repo with tag `security-review`
4. **Principle:** When in doubt, require human approval

**Remember:** It's better to have tight permissions and expand carefully than to give too much access upfront.

---

**Built with 🔒 by Strategickhaos DAO LLC**  
*Sovereignty through explicit boundaries and transparent controls*
