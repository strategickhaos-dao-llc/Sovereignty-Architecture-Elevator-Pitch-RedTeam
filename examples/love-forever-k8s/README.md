# Love Forever - Kubernetes Deployment Example

This directory contains complete Kubernetes manifests for deploying the "love-forever" application mentioned in the Kubernetes Mastery Guide. These manifests demonstrate best practices for deploying applications on your Lyra node's local Kubernetes cluster.

## 📋 Overview

The deployment includes:
- **Deployment**: 13 replicas with rolling update strategy
- **Service**: ClusterIP (10.99.92.11) and NodePort (30080) services
- **ConfigMap**: Application and NGINX configuration
- **Secrets**: Sensitive data (database passwords, API keys, TLS certificates)
- **RBAC**: ServiceAccount, Role, and RoleBinding for least-privilege access
- **NetworkPolicy**: Ingress/egress rules for network security
- **HorizontalPodAutoscaler**: Auto-scaling based on CPU/memory usage
- **Ingress**: HTTPS access with TLS termination

## 🚀 Quick Start

### Prerequisites

Ensure your Kubernetes cluster is running:
```bash
kubectl cluster-info
kubectl get nodes
```

### Deploy All Components

```bash
# Navigate to the examples directory
cd examples/love-forever-k8s

# Apply all manifests in order
kubectl apply -f rbac.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f networkpolicy.yaml
kubectl apply -f hpa.yaml
kubectl apply -f ingress.yaml

# Or apply all at once (order may vary)
kubectl apply -f .
```

### Verify Deployment

```bash
# Check deployment status
kubectl get deployments love-forever
kubectl rollout status deployment/love-forever

# Check pods (should show 13 replicas)
kubectl get pods -l app=love-forever

# Check services
kubectl get services love-forever love-forever-nodeport

# Check HPA status
kubectl get hpa love-forever-hpa

# Check ingress
kubectl get ingress love-forever-ingress
```

## 🔍 Accessing the Application

### Via ClusterIP (from within cluster)

```bash
# Run a test pod
kubectl run -it --rm debug --image=busybox --restart=Never -- sh

# Inside the pod
wget -O- http://love-forever
wget -O- http://10.99.92.11
```

### Via NodePort (from your machine)

```bash
# Access via localhost on Docker Desktop
curl http://localhost:30080

# Or get the NodePort dynamically
NODE_PORT=$(kubectl get svc love-forever-nodeport -o jsonpath='{.spec.ports[0].nodePort}')
curl http://localhost:$NODE_PORT
```

### Via Ingress (with hostname)

```bash
# Add to /etc/hosts (or C:\Windows\System32\drivers\etc\hosts on Windows)
echo "127.0.0.1 love-forever.local" | sudo tee -a /etc/hosts

# Access via browser or curl
curl http://love-forever.local
```

## 📊 Monitoring and Observability

### Check Metrics

```bash
# Install metrics-server if not present
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View resource usage
kubectl top pods -l app=love-forever
kubectl top nodes
```

### View Logs

```bash
# Stream logs from all pods
kubectl logs -f -l app=love-forever --all-containers=true

# View logs from specific pod
kubectl logs -f love-forever-7584dc69b7-xxxxx

# View previous logs (after crash)
kubectl logs love-forever-7584dc69b7-xxxxx --previous
```

### Prometheus Metrics

The deployment exposes metrics on port 8080:
```bash
# Port-forward to access metrics
kubectl port-forward svc/love-forever 8080:8080

# Access metrics endpoint
curl http://localhost:8080/metrics
```

## 🔐 Security Features

### RBAC

The deployment uses a dedicated ServiceAccount (`love-forever-sa`) with minimal permissions:
- Read-only access to pods, services, endpoints
- Read-only access to configmaps
- Limited access to specific secrets

```bash
# Test RBAC permissions
kubectl auth can-i get pods --as=system:serviceaccount:default:love-forever-sa
kubectl auth can-i delete deployments --as=system:serviceaccount:default:love-forever-sa
```

### Network Policies

Network policies restrict traffic:
- **Ingress**: Only allow traffic from pods in the same namespace
- **Egress**: Only allow DNS, database, cache, and HTTPS traffic

```bash
# View network policies
kubectl get networkpolicies
kubectl describe networkpolicy love-forever-network-policy
```

### Pod Security

Pods run with security best practices:
- Non-root user (UID 10001)
- Read-only root filesystem
- No privilege escalation
- Dropped all capabilities
- Seccomp profile enabled

## 📈 Scaling

### Manual Scaling

```bash
# Scale to 5 replicas
kubectl scale deployment love-forever --replicas=5

# Scale to 20 replicas
kubectl scale deployment love-forever --replicas=20

# Check scaling status
kubectl get deployment love-forever
kubectl get pods -l app=love-forever
```

### Auto-Scaling (HPA)

The HorizontalPodAutoscaler automatically scales between 3-20 replicas based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

```bash
# Watch HPA in action
kubectl get hpa love-forever-hpa --watch

# Generate load to trigger scaling
kubectl run -it --rm load-generator --image=busybox --restart=Never -- sh -c "while true; do wget -q -O- http://love-forever; done"
```

## 🛠️ Configuration Updates

### Update ConfigMap

```bash
# Edit configmap
kubectl edit configmap love-forever-config

# Or apply updated file
kubectl apply -f configmap.yaml

# Restart pods to pick up changes
kubectl rollout restart deployment/love-forever
```

### Update Secrets

```bash
# Create new secret value
echo -n 'new-password' | base64
# Output: bmV3LXBhc3N3b3Jk

# Update secrets.yaml with new value
kubectl apply -f secrets.yaml

# Restart pods to pick up changes
kubectl rollout restart deployment/love-forever
```

## 🔄 Updates and Rollbacks

### Rolling Update

```bash
# Update image
kubectl set image deployment/love-forever love-forever=nginx:1.22-alpine

# Watch rollout
kubectl rollout status deployment/love-forever

# Check rollout history
kubectl rollout history deployment/love-forever
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/love-forever

# Rollback to specific revision
kubectl rollout undo deployment/love-forever --to-revision=2

# Check rollout history
kubectl rollout history deployment/love-forever
```

## 🧹 Cleanup

```bash
# Delete all love-forever resources
kubectl delete -f .

# Or delete specific resources
kubectl delete deployment love-forever
kubectl delete service love-forever love-forever-nodeport
kubectl delete configmap love-forever-config
kubectl delete secret love-forever-secrets love-forever-tls
kubectl delete serviceaccount love-forever-sa
kubectl delete role love-forever-role
kubectl delete rolebinding love-forever-rolebinding
kubectl delete networkpolicy love-forever-network-policy
kubectl delete hpa love-forever-hpa
kubectl delete ingress love-forever-ingress
```

## 🔧 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -l app=love-forever

# Describe pod for events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints love-forever

# Test connectivity from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://love-forever

# Check DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup love-forever
```

### Resource Issues (on 6.89GB RAM Lyra node)

```bash
# Check node resources
kubectl describe node

# Check pod resource usage
kubectl top pods --sort-by=memory

# Reduce replicas if needed
kubectl scale deployment love-forever --replicas=3
```

## 📚 Related Documentation

- [Kubernetes Mastery Guide](../../KUBERNETES_MASTERY_GUIDE.md) - Comprehensive K8s learning guide
- [Bloom's Interview Questions](../../BLOOMS_INTERVIEW_QUESTIONS.md) - Advanced interview prep
- [Main README](../../README.md) - Project overview

## 🎯 Next Steps

1. **Customize the deployment**: Update image, replicas, resources to match your needs
2. **Add monitoring**: Deploy Prometheus and Grafana for observability
3. **Implement CI/CD**: Automate deployments with GitHub Actions or GitLab CI
4. **Security hardening**: Scan images with Trivy, implement pod security policies
5. **Multi-node expansion**: Add Nova as a worker node for distributed workloads

---

**Built for Strategickhaos Swarm Intelligence - Love Forever on Kubernetes! 💙🚀**
