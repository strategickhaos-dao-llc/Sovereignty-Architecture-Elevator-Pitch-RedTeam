# Quick Reference Guide - Sovereignty Architecture

Fast commands for common operations.

## 🚀 Deployment

```bash
# Deploy to local environment
./deploy-production.sh

# Deploy to staging
./deploy-production.sh staging

# Deploy to production
./deploy-production.sh production

# Verify infrastructure
./verify-infrastructure.sh
```

## 📊 Monitoring

```bash
# Access Grafana (dashboards)
kubectl port-forward -n sovereignty-system svc/grafana 3000:3000
# Open: http://localhost:3000

# Access Prometheus (metrics)
kubectl port-forward -n sovereignty-system svc/prometheus 9090:9090
# Open: http://localhost:9090

# Access Loki (logs)
kubectl port-forward -n sovereignty-system svc/loki 3100:3100

# View logs
kubectl logs -f -n sovereignty-system -l app=sovereignty-core
```

## 🔐 Secrets

```bash
# Access Vault UI
kubectl port-forward -n sovereignty-system svc/vault 8200:8200
# Open: http://localhost:8200

# Vault CLI
export VAULT_ADDR='http://localhost:8200'
vault status
vault kv list secret/
```

## ☸️ Kubernetes

```bash
# View all resources
kubectl get all -n sovereignty-system

# Check deployment status
kubectl rollout status deployment/sovereignty-core -n sovereignty-system

# Scale deployment
kubectl scale deployment/sovereignty-core --replicas=5 -n sovereignty-system

# View pod logs
kubectl logs -f deployment/sovereignty-core -n sovereignty-system

# Restart deployment
kubectl rollout restart deployment/sovereignty-core -n sovereignty-system

# Apply base configuration
kubectl apply -k kubernetes/base/

# Apply production overlay
kubectl apply -k kubernetes/overlays/production/
```

## 🔄 GitOps

```bash
# Bootstrap ArgoCD
kubectl apply -f gitops/bootstrap/

# Access ArgoCD UI
kubectl port-forward -n argocd svc/argocd-server 8080:443
# Open: https://localhost:8080

# Check Flux status
flux get all

# Reconcile Flux
flux reconcile kustomization sovereignty-architecture

# View GitOps applications
kubectl get applications -n argocd
```

## 🏗️ Terraform

```bash
cd terraform

# Initialize
terraform init

# Plan deployment
terraform plan -var-file=environments/chaos-god-local/terraform.tfvars

# Apply changes
terraform apply -var-file=environments/chaos-god-local/terraform.tfvars

# Destroy infrastructure
terraform destroy -var-file=environments/chaos-god-local/terraform.tfvars

# View outputs
terraform output
```

## 🔍 Troubleshooting

```bash
# Check cluster info
kubectl cluster-info

# View node status
kubectl get nodes

# Check pod events
kubectl get events -n sovereignty-system --sort-by='.lastTimestamp'

# Describe pod
kubectl describe pod <pod-name> -n sovereignty-system

# Check resource usage
kubectl top nodes
kubectl top pods -n sovereignty-system

# View all namespaces
kubectl get namespaces

# Check service endpoints
kubectl get endpoints -n sovereignty-system
```

## 🔧 CI/CD

```bash
# View Tekton pipelines
kubectl get pipelines -n sovereignty-system

# View pipeline runs
kubectl get pipelineruns -n sovereignty-system

# Watch pipeline execution
kubectl logs -f -n sovereignty-system <pipelinerun-pod>

# Trigger manual pipeline
kubectl create -f ci-cd/tekton/pipeline.yaml
```

## 📦 Build & Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build TypeScript
npm run build

# Lint code
npm run lint

# Run Discord bot
npm run bot
```

## 🌐 Network

```bash
# Check Tailscale status
tailscale status

# View WireGuard config
wg show

# Test network connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash
```

## 🔄 Updates

```bash
# Pull latest changes
git pull origin main

# Redeploy infrastructure
./deploy-production.sh

# Update specific deployment
kubectl set image deployment/sovereignty-core sovereignty-core=sovereignty/core:v2

# Rollback deployment
kubectl rollout undo deployment/sovereignty-core -n sovereignty-system
```

## 📝 Documentation

- **Production Guide**: [PRODUCTION_README.md](PRODUCTION_README.md)
- **Future Roadmap**: [NEXT_100_ASCENSION.md](NEXT_100_ASCENSION.md)
- **Deployment Summary**: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)
- **Main README**: [README.md](README.md)

## 🆘 Common Issues

### Pods stuck in Pending
```bash
kubectl describe pod <pod-name> -n sovereignty-system
# Check: insufficient resources, PVC not bound, or image pull errors
```

### Service not accessible
```bash
kubectl get svc -n sovereignty-system
kubectl get endpoints -n sovereignty-system
# Check: selector labels match pod labels
```

### GitOps not syncing
```bash
argocd app get sovereignty-architecture
argocd app sync sovereignty-architecture --force
```

### Terraform state locked
```bash
cd terraform
rm .terraform.tfstate.lock.info
```

---

**Quick Help**: Run `./verify-infrastructure.sh` to check infrastructure health

🧠⚡🌍❤️🐐∞
