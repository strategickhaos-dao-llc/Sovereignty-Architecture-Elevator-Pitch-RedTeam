# Legion Console

Central cockpit for the **Legion of Minds Council OS**.

This repo is the *one place* you drop into when you want to drive:
- Kubernetes clusters (GKE, k3s, homelab)
- Self-hosted GitHub runners
- Offline LLM services (Ollama, vLLM, etc.)
- Swarm agents and experiments

Instead of "which portal do I click?", you ask:
> **Which branch of `legion-console` am I on?**

---

## Quickstart

### 1. Clone

```bash
git clone https://github.com/<ORG>/legion-console.git
cd legion-console
```

### 2. Copy example configs

```bash
cp config/contexts.example.yaml config/contexts.yaml
cp k8s/kubeconfig.example k8s/kubeconfig
```

Edit `config/contexts.yaml` and fill in your:
- GCP project ID
- GKE cluster names / regions
- default namespace(s)

### 3. Set Kubernetes context

```bash
./scripts/set-context.sh gke-jarvis-swarm-personal
```

### 4. Bootstrap core infra into the cluster

```bash
./scripts/bootstrap-cluster.sh
```

### 5. Deploy Legion services

```bash
./scripts/deploy-legion.sh
```

### 6. Attach to LLM console

```bash
./scripts/attach-llm.sh
```

From here, you live in tmux/vim/CLI and treat this repo as your OS shell.

---

## Structure

### `.devcontainer/`
Devcontainer definition for Codespaces / VS Code / Cloud Shell.

### `config/contexts.yaml`
High-level description of all clusters and namespaces you care about.

### `k8s/kubeconfig`
Optional pinned kubeconfig (or you can use the default one in `~/.kube/config`).

### `scripts/`
Small, readable Bash scripts that:
- connect to clusters
- run `gcloud container clusters get-credentials`
- apply K8s manifests / Helm charts
- port-forward LLM endpoints

Customize everything – this is your cockpit.
