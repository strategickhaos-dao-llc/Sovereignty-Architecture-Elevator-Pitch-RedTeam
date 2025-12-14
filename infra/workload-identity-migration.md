# GKE Workload Identity Migration Plan
## Eliminate Long-Lived Keys with Workload Identity

**Project:** jarvis-swarm-personal  
**Cluster:** jarvis-swarm-personal-001  
**Region:** us-central1

---

## Overview

Workload Identity allows GKE pods to authenticate to GCP services using Kubernetes service accounts instead of long-lived JSON keys. This eliminates `GCP_SA_KEY` secrets entirely.

---

## Phase 1: Enable Workload Identity on Cluster

### 1.1 Enable Workload Identity (if not already enabled)

```bash
# Check current status
gcloud container clusters describe jarvis-swarm-personal-001 \
  --region us-central1 \
  --project jarvis-swarm-personal \
  --format="value(workloadIdentityConfig.workloadPool)"

# Enable Workload Identity (if output is empty)
gcloud container clusters update jarvis-swarm-personal-001 \
  --region us-central1 \
  --project jarvis-swarm-personal \
  --workload-pool=jarvis-swarm-personal.svc.id.goog
```

### 1.2 Update Node Pool

```bash
# Get existing node pools
gcloud container node-pools list \
  --cluster jarvis-swarm-personal-001 \
  --region us-central1 \
  --project jarvis-swarm-personal

# Enable Workload Identity on default node pool
gcloud container node-pools update default-pool \
  --cluster jarvis-swarm-personal-001 \
  --region us-central1 \
  --project jarvis-swarm-personal \
  --workload-metadata=GKE_METADATA
```

---

## Phase 2: Create GCP Service Account

### 2.1 Create Service Account for GitHub Actions

```bash
PROJECT_ID="jarvis-swarm-personal"
GSA_NAME="github-actions-gke"
GSA_EMAIL="${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Create GCP service account
gcloud iam service-accounts create $GSA_NAME \
  --display-name="GitHub Actions GKE (Workload Identity)" \
  --project=$PROJECT_ID

# Grant minimal GKE permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${GSA_EMAIL}" \
  --role="roles/container.viewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${GSA_EMAIL}" \
  --role="roles/container.clusterViewer"
```

---

## Phase 3: Configure Kubernetes Service Account

### 3.1 Create K8s Namespace and Service Account

```bash
# Get cluster credentials
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region us-central1 \
  --project jarvis-swarm-personal

# Create namespace for GitHub Actions workloads
kubectl create namespace github-actions || true

# Create Kubernetes service account
kubectl create serviceaccount github-actions-runner \
  --namespace github-actions
```

### 3.2 Annotate K8s Service Account

```bash
PROJECT_ID="jarvis-swarm-personal"
GSA_EMAIL="github-actions-gke@${PROJECT_ID}.iam.gserviceaccount.com"

kubectl annotate serviceaccount github-actions-runner \
  --namespace github-actions \
  iam.gke.io/gcp-service-account=$GSA_EMAIL
```

---

## Phase 4: Bind GCP SA to K8s SA

### 4.1 Create IAM Policy Binding

```bash
PROJECT_ID="jarvis-swarm-personal"
GSA_NAME="github-actions-gke"
GSA_EMAIL="${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
K8S_NAMESPACE="github-actions"
K8S_SA="github-actions-runner"

# Allow K8s SA to impersonate GCP SA
gcloud iam service-accounts add-iam-policy-binding $GSA_EMAIL \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[${K8S_NAMESPACE}/${K8S_SA}]"
```

---

## Phase 5: Deploy Test Pod

### 5.1 Create Test Deployment

Save as `test-workload-identity.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: workload-identity-test
  namespace: github-actions
spec:
  serviceAccountName: github-actions-runner
  containers:
  - name: gcloud
    image: google/cloud-sdk:slim
    command:
    - sleep
    - "3600"
```

Deploy and test:

```bash
# Deploy test pod
kubectl apply -f test-workload-identity.yaml

# Wait for pod to be ready
kubectl wait --for=condition=Ready pod/workload-identity-test \
  --namespace github-actions \
  --timeout=60s

# Test authentication (should show github-actions-gke@...)
kubectl exec -n github-actions workload-identity-test -- \
  gcloud auth list

# Test GKE access
kubectl exec -n github-actions workload-identity-test -- \
  gcloud container clusters list --project jarvis-swarm-personal

# Cleanup
kubectl delete pod workload-identity-test -n github-actions
```

---

## Phase 6: Update GitHub Actions Workflow

### 6.1 Remove GCP_SA_KEY Secret

**OLD (with key):**
```yaml
- name: "🔐 Authenticate to GCP"
  uses: google-github-actions/auth@v2
  with:
    credentials_json: ${{ secrets.GCP_SA_KEY }}
```

**NEW (Workload Identity):**
```yaml
- name: "🔐 Authenticate to GCP via Workload Identity"
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
    service_account: 'github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com'
```

### 6.2 Setup Workload Identity Federation for GitHub Actions

```bash
PROJECT_ID="jarvis-swarm-personal"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
POOL_NAME="github-pool"
PROVIDER_NAME="github-provider"
GSA_EMAIL="github-actions-gke@${PROJECT_ID}.iam.gserviceaccount.com"
GITHUB_REPO="strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam"

# Create Workload Identity Pool
gcloud iam workload-identity-pools create $POOL_NAME \
  --project=$PROJECT_ID \
  --location=global \
  --display-name="GitHub Actions Pool"

# Create Workload Identity Provider
gcloud iam workload-identity-pools providers create-oidc $PROVIDER_NAME \
  --project=$PROJECT_ID \
  --location=global \
  --workload-identity-pool=$POOL_NAME \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='${GITHUB_REPO}'"

# Grant GitHub Actions access to impersonate service account
gcloud iam service-accounts add-iam-policy-binding $GSA_EMAIL \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}"

# Get Workload Identity Provider resource name
echo "Workload Identity Provider:"
echo "projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
```

---

## Phase 7: Update overnight.yml Workflow

Replace the auth step in `.github/workflows/overnight.yml`:

```yaml
gke-health:
  name: "☸️ GKE Cluster Health"
  runs-on: ubuntu-latest
  needs: overnight
  if: ${{ inputs.gke_health == 'true' || github.event_name == 'schedule' }}
  timeout-minutes: 15
  
  permissions:
    contents: read
    id-token: write  # Required for Workload Identity Federation
  
  steps:
    - name: "🔐 Authenticate to GCP via Workload Identity"
      uses: google-github-actions/auth@v2
      with:
        workload_identity_provider: 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
        service_account: 'github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com'

    - name: "🛠️ Setup gcloud CLI"
      uses: google-github-actions/setup-gcloud@v2
      with:
        install_components: "kubectl,gke-gcloud-auth-plugin"

    # Rest of workflow unchanged...
```

---

## Phase 8: Verification

### 8.1 Verify No Keys Required

```bash
# List service account keys (should only show Google-managed keys)
gcloud iam service-accounts keys list \
  --iam-account=github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com \
  --project=jarvis-swarm-personal
```

### 8.2 Test Workflow

```bash
# Trigger workflow manually from GitHub UI
# Actions → Overnight Autonomous Evolution → Run workflow
# Enable: gke_health = true
```

### 8.3 Audit Access

```bash
# View Cloud Audit Logs
gcloud logging read \
  'protoPayload.authenticationInfo.principalEmail="github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com"' \
  --project=jarvis-swarm-personal \
  --limit=50 \
  --format=json
```

---

## Phase 9: Cleanup

### 9.1 Delete Old Service Account Keys

```bash
# List all keys
gcloud iam service-accounts keys list \
  --iam-account=github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com \
  --project=jarvis-swarm-personal \
  --format="value(name)"

# Delete specific key (user-managed only)
# gcloud iam service-accounts keys delete KEY_ID \
#   --iam-account=github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com \
#   --project=jarvis-swarm-personal
```

### 9.2 Remove GitHub Secret

```bash
# After confirming Workload Identity works, delete from GitHub:
# Settings → Secrets → Actions → Delete GCP_SA_KEY
```

---

## Rollback Plan

If Workload Identity fails:

```bash
# Re-create service account key
gcloud iam service-accounts keys create ~/gke-sa-key-rollback.json \
  --iam-account=github-actions-gke@jarvis-swarm-personal.iam.gserviceaccount.com \
  --project=jarvis-swarm-personal

# Re-add to GitHub secrets
cat ~/gke-sa-key-rollback.json
# Paste back into GitHub: Settings → Secrets → GCP_SA_KEY

# Revert workflow changes
git revert <commit-hash>
git push origin main
```

---

## Benefits Achieved

| Before | After |
|--------|-------|
| Long-lived JSON key in GitHub secrets | No keys - short-lived tokens only |
| Manual key rotation required | Automatic token rotation (1h TTL) |
| Key compromise = full access | Token scoped to specific workflow |
| Key exposure risk in logs | No secrets to expose |
| Manual audit trail | Automatic Cloud Audit Logs |

---

## Next Steps

1. **Run Phase 1-4** to enable Workload Identity
2. **Test with Phase 5** to verify setup
3. **Implement Phase 6-7** to update GitHub Actions
4. **Verify with Phase 8** that no keys are needed
5. **Execute Phase 9** to remove old keys

**Estimated time:** 30-45 minutes  
**Rollback time:** 5 minutes

---

**Ready to execute?** Run the commands in sequence and report any errors. 🔥
