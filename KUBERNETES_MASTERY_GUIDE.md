# 🚀 Kubernetes Mastery Guide for Lyra Node

**Master your local Kubernetes cluster via Docker Desktop Pro with kubeadm - Perfect for SE concentration and cyber major**

This guide helps you master Kubernetes on your Nitro V15 Lyra node (6.89GB RAM, single-node setup) through focused daily drills and hands-on practice. Built specifically for your "love-forever" deployment and swarm experiments.

## 📋 Table of Contents
- [Core Kubernetes Essentials](#core-kubernetes-essentials)
- [DevOps & Scaling](#devops--scaling)
- [Cyber-Focused Security](#cyber-focused-security)
- [Hands-On Labs](#hands-on-labs)
- [Troubleshooting](#troubleshooting)

---

## Core Kubernetes Essentials

### 🎯 10-15 Minute Daily Drills

#### kubectl Mastery Fundamentals

**Essential Commands - Practice Daily:**

```bash
# Pod Management
kubectl get pods -n default                          # List all pods in default namespace
kubectl get pods -A                                  # List pods across all namespaces
kubectl describe pod love-forever-7584dc69b7-xxxxx  # Detailed pod information
kubectl logs love-forever-7584dc69b7-xxxxx          # View pod logs
kubectl logs -f love-forever-7584dc69b7-xxxxx       # Follow/stream logs in real-time
kubectl exec -it love-forever-7584dc69b7-xxxxx -- /bin/sh  # Shell access into pod

# Deployment Management
kubectl get deployments -n default                   # List deployments
kubectl describe deployment love-forever            # Deployment details
kubectl scale deployment love-forever --replicas=5  # Scale to 5 replicas
kubectl rollout status deployment/love-forever      # Check rollout status
kubectl rollout restart deployment/love-forever     # Restart deployment

# Service Management
kubectl get services -n default                     # List services
kubectl describe service kubernetes                 # Service details
kubectl get endpoints                               # Show service endpoints

# Resource Overview
kubectl get all -n default                          # All resources in namespace
kubectl top pods                                    # Pod resource usage (requires metrics-server)
kubectl top nodes                                   # Node resource usage
```

**Advanced kubectl Operations:**

```bash
# Port Forwarding (access services locally)
kubectl port-forward service/love-forever 8080:80

# Copy Files to/from Pods
kubectl cp /local/file.txt love-forever-7584dc69b7-xxxxx:/container/path
kubectl cp love-forever-7584dc69b7-xxxxx:/container/file.txt ./local/

# Execute Commands in Pods
kubectl exec love-forever-7584dc69b7-xxxxx -- ls -la /app
kubectl exec love-forever-7584dc69b7-xxxxx -- env

# Debug with Ephemeral Containers (K8s 1.23+)
kubectl debug love-forever-7584dc69b7-xxxxx -it --image=busybox

# Resource Editing (opens in editor)
kubectl edit deployment love-forever

# Apply Configuration Changes
kubectl apply -f deployment.yaml
kubectl apply -f . --recursive                      # Apply all YAML in directory

# Delete Resources
kubectl delete pod love-forever-7584dc69b7-xxxxx
kubectl delete deployment love-forever
kubectl delete -f deployment.yaml
```

**Useful kubectl Shortcuts & Aliases:**

```bash
# Add these to your .bashrc or .zshrc
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgd='kubectl get deployments'
alias kgs='kubectl get services'
alias kga='kubectl get all'
alias kd='kubectl describe'
alias kl='kubectl logs'
alias ke='kubectl exec -it'
alias kpf='kubectl port-forward'

# Use with completion
source <(kubectl completion bash)
complete -F __start_kubectl k
```

---

### 📝 YAML Manifest Mastery

#### Deployment Manifest Template

Create `love-forever-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: love-forever
  namespace: default
  labels:
    app: love-forever
    environment: dev
spec:
  replicas: 3                    # Start with 3, scale as needed
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: love-forever
  template:
    metadata:
      labels:
        app: love-forever
        version: v1.0
    spec:
      containers:
      - name: love-forever
        image: nginx:1.21-alpine  # Replace with your image
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        env:
        - name: ENVIRONMENT
          value: "development"
        - name: APP_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /etc/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: love-forever-config
```

#### Service Manifest Types

**ClusterIP Service (Internal Only):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: love-forever
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: love-forever
  ports:
  - protocol: TCP
    port: 80
    targetPort: http
    name: http
```

**NodePort Service (External Access):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: love-forever-external
  namespace: default
spec:
  type: NodePort
  selector:
    app: love-forever
  ports:
  - protocol: TCP
    port: 80
    targetPort: http
    nodePort: 30080      # Access via localhost:30080
    name: http
```

**LoadBalancer Service (Cloud/Docker Desktop):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: love-forever-lb
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: love-forever
  ports:
  - protocol: TCP
    port: 80
    targetPort: http
    name: http
```

#### ConfigMap & Secret Examples

**ConfigMap for Application Config:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: love-forever-config
  namespace: default
data:
  app.properties: |
    server.port=8080
    logging.level=INFO
  database.host: "postgres.default.svc.cluster.local"
  cache.enabled: "true"
```

**Secret for Sensitive Data:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: love-forever-secrets
  namespace: default
type: Opaque
data:
  # Values must be base64 encoded
  # echo -n 'mypassword' | base64
  db-password: bXlwYXNzd29yZA==
  api-key: c2VjcmV0LWFwaS1rZXk=
```

**Using Secrets in Deployment:**

```yaml
spec:
  containers:
  - name: love-forever
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: love-forever-secrets
          key: db-password
```

---

### 🏗️ Namespaces & Resource Management

#### Creating and Managing Namespaces

```bash
# Create namespace
kubectl create namespace strategickhaos

# Set default namespace for context
kubectl config set-context --current --namespace=strategickhaos

# List all namespaces
kubectl get namespaces

# View resources in specific namespace
kubectl get all -n strategickhaos
```

**Namespace Manifest:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: strategickhaos
  labels:
    environment: development
    owner: domenic
```

#### Resource Quotas (Prevent Resource Hogs)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: strategickhaos-quota
  namespace: strategickhaos
spec:
  hard:
    requests.cpu: "2"           # Max 2 CPU cores requested
    requests.memory: 4Gi        # Max 4GB memory requested
    limits.cpu: "4"             # Max 4 CPU cores limit
    limits.memory: 8Gi          # Max 8GB memory limit
    pods: "20"                  # Max 20 pods
    services: "10"              # Max 10 services
    persistentvolumeclaims: "5" # Max 5 PVCs
```

#### LimitRange (Default Resource Limits)

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: strategickhaos-limits
  namespace: strategickhaos
spec:
  limits:
  - type: Pod
    max:
      cpu: "2"
      memory: 2Gi
    min:
      cpu: "100m"
      memory: 128Mi
  - type: Container
    default:                    # Default limits
      cpu: "500m"
      memory: 512Mi
    defaultRequest:             # Default requests
      cpu: "100m"
      memory: 128Mi
    max:
      cpu: "1"
      memory: 1Gi
    min:
      cpu: "50m"
      memory: 64Mi
```

**Apply Resource Management:**

```bash
kubectl apply -f namespace.yaml
kubectl apply -f resource-quota.yaml
kubectl apply -f limit-range.yaml

# Check quota usage
kubectl describe resourcequota strategickhaos-quota -n strategickhaos

# Check limit ranges
kubectl describe limitrange strategickhaos-limits -n strategickhaos
```

---

## DevOps & Scaling

### 📦 Helm Charts - Package Management for Kubernetes

#### Installing Helm

```bash
# Install Helm 3
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version

# Add common repositories
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

#### Creating a Helm Chart for love-forever

```bash
# Create new chart
helm create love-forever-chart

# Chart structure:
# love-forever-chart/
# ├── Chart.yaml          # Chart metadata
# ├── values.yaml         # Default configuration values
# ├── templates/          # Kubernetes manifests with templating
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── ingress.yaml
# │   └── _helpers.tpl
# └── charts/             # Chart dependencies
```

**Chart.yaml:**

```yaml
apiVersion: v2
name: love-forever
description: A Helm chart for love-forever deployment
type: application
version: 1.0.0
appVersion: "1.0"
keywords:
  - strategickhaos
  - love-forever
maintainers:
  - name: Domenic Garza
    email: domenic@strategickhaos.com
```

**values.yaml:**

```yaml
replicaCount: 3

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21-alpine"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: "nginx"
  hosts:
    - host: love-forever.local
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

**Helm Commands:**

```bash
# Install chart
helm install love-forever ./love-forever-chart

# Install with custom values
helm install love-forever ./love-forever-chart --values custom-values.yaml

# Upgrade release
helm upgrade love-forever ./love-forever-chart

# Rollback to previous version
helm rollback love-forever 1

# List releases
helm list

# Uninstall release
helm uninstall love-forever

# Dry-run to see what would be deployed
helm install love-forever ./love-forever-chart --dry-run --debug
```

---

### 📊 Monitoring & Logging

#### Prometheus for Metrics

**Install Prometheus via Helm:**

```bash
# Add Prometheus community charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus stack (includes Grafana)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Access Prometheus UI
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Access Grafana (default: admin/prom-operator)
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

**ServiceMonitor for love-forever:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: love-forever
  namespace: default
spec:
  selector:
    matchLabels:
      app: love-forever
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

#### Query Pod Health with kubectl top

```bash
# Install metrics-server (if not present)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View pod resource usage
kubectl top pods
kubectl top pods -n default
kubectl top pods --sort-by=memory
kubectl top pods --sort-by=cpu

# View node resource usage
kubectl top nodes
```

#### Logging with ELK/Fluentd

**Deploy Fluentd DaemonSet:**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

**Viewing Logs:**

```bash
# View logs from all pods with label
kubectl logs -l app=love-forever

# View logs from specific container in multi-container pod
kubectl logs love-forever-7584dc69b7-xxxxx -c container-name

# View previous container logs (after crash)
kubectl logs love-forever-7584dc69b7-xxxxx --previous

# Stream logs from multiple pods
kubectl logs -f -l app=love-forever --all-containers=true
```

---

### 🔄 CI/CD Integration

#### GitHub Actions Kubernetes Deployment

**`.github/workflows/deploy.yaml`:**

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.27.0'

      - name: Configure kubectl
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > ~/.kube/config

      - name: Build Docker image
        run: |
          docker build -t love-forever:${{ github.sha }} .
          docker tag love-forever:${{ github.sha }} love-forever:latest

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/love-forever \
            love-forever=love-forever:${{ github.sha }} \
            --record
          
          kubectl rollout status deployment/love-forever

      - name: Notify Discord
        if: success()
        run: |
          curl -H "Content-Type: application/json" \
               -d '{"content":"🚀 Deployment successful: love-forever:${{ github.sha }}"}' \
               ${{ secrets.DISCORD_WEBHOOK_URL }}
```

#### GitLab CI/CD Pipeline

**`.gitlab-ci.yml`:**

```yaml
stages:
  - build
  - test
  - deploy

variables:
  KUBE_NAMESPACE: default
  DEPLOYMENT_NAME: love-forever

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  script:
    - kubectl apply --dry-run=client -f k8s/

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/$DEPLOYMENT_NAME \
        love-forever=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/$DEPLOYMENT_NAME -n $KUBE_NAMESPACE
  only:
    - main
```

---

## Cyber-Focused Security

### 🔐 RBAC (Role-Based Access Control)

#### Creating Service Accounts

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: love-forever-sa
  namespace: default
```

#### Role Definition (Namespace-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: love-forever-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]
```

#### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: love-forever-rolebinding
  namespace: default
subjects:
- kind: ServiceAccount
  name: love-forever-sa
  namespace: default
roleRef:
  kind: Role
  name: love-forever-role
  apiGroup: rbac.authorization.k8s.io
```

#### ClusterRole (Cluster-wide)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

**Testing RBAC:**

```bash
# Check what actions you can perform
kubectl auth can-i create pods
kubectl auth can-i delete deployments
kubectl auth can-i get pods --as=system:serviceaccount:default:love-forever-sa
```

---

### 🛡️ Network Policies

**Deny All Ingress Traffic (Default Deny):**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

**Allow Specific Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: love-forever-allow-ingress
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: love-forever
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
```

**Restrict Egress (Block External Networks):**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: love-forever-restrict-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: love-forever
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector: {}          # Only allow internal cluster traffic
  - to:                        # Allow DNS
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

---

### 🔑 Secrets Management & Vaults

#### Creating Secrets

```bash
# Create from literal values
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secretpass123

# Create from files
kubectl create secret generic tls-certs \
  --from-file=tls.crt=./server.crt \
  --from-file=tls.key=./server.key

# Create from .env file
kubectl create secret generic app-env --from-env-file=.env
```

#### Using External Secrets Operator

```bash
# Install External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace
```

**ExternalSecret Definition:**

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: love-forever-secrets
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: love-forever-secrets
  data:
  - secretKey: db-password
    remoteRef:
      key: database/love-forever
      property: password
```

#### Sealed Secrets (Encrypted Secrets in Git)

```bash
# Install Sealed Secrets
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Install kubeseal CLI
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-linux-amd64
sudo install -m 755 kubeseal-linux-amd64 /usr/local/bin/kubeseal

# Create sealed secret
kubectl create secret generic mysecret --dry-run=client --from-literal=password=mypass -o yaml | \
  kubeseal -o yaml > mysealedsecret.yaml

# Safe to commit to Git!
git add mysealedsecret.yaml
```

---

### 🔍 Vulnerability Scanning

#### Trivy for Image Scanning

```bash
# Install Trivy
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Scan container image
trivy image nginx:1.21-alpine

# Scan running Kubernetes workloads
kubectl get pods -o json | \
  jq -r '.items[] | .spec.containers[] | .image' | \
  xargs -I {} trivy image {}

# Scan for HIGH and CRITICAL only
trivy image --severity HIGH,CRITICAL nginx:1.21-alpine
```

#### Pod Security Standards

**Enforce Pod Security:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: strategickhaos
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**PodSecurityPolicy (Deprecated in K8s 1.25+):**

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'secret'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: false
```

---

## Hands-On Labs

### Lab 1: Deploy NGINX and Expose Securely

```bash
# 1. Create namespace
kubectl create namespace security-lab

# 2. Deploy NGINX
kubectl create deployment nginx --image=nginx:alpine -n security-lab

# 3. Create network policy (deny all by default)
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: security-lab
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# 4. Allow ingress from specific source
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-nginx-ingress
  namespace: security-lab
spec:
  podSelector:
    matchLabels:
      app: nginx
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: allowed
    ports:
    - protocol: TCP
      port: 80
EOF

# 5. Test access (should fail)
kubectl run -n security-lab test-pod --image=busybox --rm -it --restart=Never -- wget -O- nginx

# 6. Test with allowed label (should succeed)
kubectl run -n security-lab test-pod --image=busybox --labels=access=allowed --rm -it --restart=Never -- wget -O- nginx
```

### Lab 2: Scan and Secure love-forever Deployment

```bash
# 1. Deploy love-forever
kubectl apply -f love-forever-deployment.yaml

# 2. Scan all images
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}' | \
  tr ' ' '\n' | \
  sort -u | \
  xargs -I {} sh -c 'echo "Scanning {}" && trivy image {}'

# 3. Create RBAC for limited access
kubectl create serviceaccount love-forever-sa
kubectl create role love-forever-role --verb=get,list,watch --resource=pods,services
kubectl create rolebinding love-forever-rb --role=love-forever-role --serviceaccount=default:love-forever-sa

# 4. Update deployment to use service account
kubectl patch deployment love-forever -p '{"spec":{"template":{"spec":{"serviceAccountName":"love-forever-sa"}}}}'
```

### Lab 3: Simulate Attack in Parrot OS

**From Parrot OS VM:**

```bash
# 1. Get NodePort service IP
NODE_PORT=$(kubectl get svc love-forever-external -o jsonpath='{.spec.ports[0].nodePort}')
CLUSTER_IP=192.168.1.100  # Your Lyra node IP

# 2. Basic port scan
nmap -p $NODE_PORT $CLUSTER_IP

# 3. Web vulnerability scan
nikto -h http://$CLUSTER_IP:$NODE_PORT

# 4. Test for common vulnerabilities
curl -v http://$CLUSTER_IP:$NODE_PORT/../../../etc/passwd
curl -X POST http://$CLUSTER_IP:$NODE_PORT -H "X-Forwarded-For: malicious-ip"

# 5. Check Kubernetes API exposure (should be denied)
curl -k https://$CLUSTER_IP:6443/api/v1/namespaces
```

**Mitigation:**

```bash
# 1. Enable admission controllers
# Add to kube-apiserver flags:
# --enable-admission-plugins=PodSecurityPolicy,NodeRestriction

# 2. Implement rate limiting
kubectl apply -f rate-limit-ingress.yaml

# 3. Deploy WAF (Web Application Firewall)
helm install modsecurity stable/modsecurity-ingress-controller
```

---

## Troubleshooting

### Common Issues & Solutions

#### Pods Not Starting

```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Previous container logs

# Common causes:
# - Image pull errors: Check image name and registry credentials
# - Resource limits: Check node capacity with kubectl top nodes
# - CrashLoopBackOff: Check application logs
```

#### Resource Issues on Lyra (6.89GB RAM)

```bash
# Check node resources
kubectl describe node

# Check pod resource usage
kubectl top pods --sort-by=memory
kubectl top pods --sort-by=cpu

# Reduce resource requests in deployments
kubectl set resources deployment love-forever \
  --requests=cpu=50m,memory=64Mi \
  --limits=cpu=100m,memory=128Mi

# Delete unused resources
kubectl delete pods --field-selector=status.phase=Failed
```

#### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints <service-name>

# Check if pods are selected
kubectl get pods -l app=love-forever

# Test connectivity from inside cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://service-name:80

# Check DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup service-name
```

### Best Practices for Single-Node Setup

1. **Resource Management**: Always set resource requests/limits
2. **Namespace Isolation**: Use namespaces to organize workloads
3. **Local Registry**: Set up local registry to avoid pull limits
4. **Monitoring**: Install metrics-server for resource monitoring
5. **Backup**: Use Velero for cluster backup/restore
6. **Development**: Use Skaffold for rapid development iteration

---

## Next Steps

### Expand to Multi-Node Cluster

**Add Nova as Worker Node:**

```bash
# On Nova (worker node):
kubeadm join <master-ip>:6443 --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# Verify from Lyra (master):
kubectl get nodes
```

### Advanced Topics

- **Service Mesh**: Istio or Linkerd for traffic management
- **GitOps**: ArgoCD or Flux for declarative deployments
- **Chaos Engineering**: Litmus for resilience testing
- **Policy Management**: Open Policy Agent (OPA) for governance
- **Observability**: Jaeger for distributed tracing

---

## Resources

- **Official Docs**: https://kubernetes.io/docs/
- **kubectl Cheat Sheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **CKA Exam Prep**: https://github.com/cncf/curriculum
- **Practice Labs**: https://killercoda.com/playgrounds
- **Security**: https://kubernetes.io/docs/concepts/security/

---

**Built for Strategickhaos Swarm Intelligence - Master your sovereign infrastructure! 🚀**
