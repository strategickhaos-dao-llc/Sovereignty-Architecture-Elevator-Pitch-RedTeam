# Kubernetes Multi-Node Cluster Setup Guide

This guide provides step-by-step instructions for setting up a multi-node Kubernetes cluster on your infrastructure with TrueNAS, laptops, and desktop systems.

## Hardware Configuration

### Nodes Overview

- **Control Plane**: Nitro V15 Lyra (128 GB RAM)
- **Worker Node 1**: ASUS TUF Gaming A15 - Nova Athena (16 GB RAM)
- **Worker Node 2**: Sony CI5 - Asteroth (8 GB RAM)
- **Storage**: TrueNAS for persistent storage

## Prerequisites

Before beginning the setup, ensure the following requirements are met:

1. **Network Configuration**: All nodes must be on the same subnet and able to communicate
2. **Operating System**: Ubuntu 20.04+ or compatible Linux distribution on all nodes
3. **Ports**: Ensure required Kubernetes ports are open (see Port Requirements below)
4. **Root Access**: Administrative privileges on all nodes
5. **Container Runtime**: Docker or containerd installed on all nodes

### Port Requirements

**Control Plane Node:**
- 6443: Kubernetes API server
- 2379-2380: etcd server client API
- 10250: Kubelet API
- 10259: kube-scheduler
- 10257: kube-controller-manager

**Worker Nodes:**
- 10250: Kubelet API
- 30000-32767: NodePort Services

## Installation Steps

### Step 1: Install Container Runtime on All Nodes

Install Docker or containerd on each node:

```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker
```

### Step 2: Install Kubernetes Components on All Nodes

Install kubeadm, kubelet, and kubectl:

```bash
# Add Kubernetes apt repository
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install Kubernetes packages
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# Hold packages at current version
sudo apt-mark hold kubelet kubeadm kubectl
```

### Step 3: Disable Swap on All Nodes

Kubernetes requires swap to be disabled:

```bash
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

### Step 4: Initialize Control Plane Node (Nitro V15 Lyra)

On the control plane node (128 GB RAM system), run:

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=<CONTROL_PLANE_IP>
```

Replace `<CONTROL_PLANE_IP>` with the actual IP address of your control plane node.

After successful initialization, you'll see output containing:
- The kubeconfig setup commands
- A join command for worker nodes (save this!)

### Step 5: Configure kubectl on Control Plane

Set up kubectl access for your user:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### Step 6: Install Pod Network Add-on

Install Calico for pod networking:

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

Wait for all Calico pods to be running:

```bash
kubectl get pods -n kube-system -w
```

### Step 7: Join Worker Nodes

On each worker node (ASUS TUF Gaming A15 and Sony CI5), run the join command from Step 4:

```bash
sudo kubeadm join <CONTROL_PLANE_IP>:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
```

If you didn't save the join command, generate a new one on the control plane:

```bash
kubeadm token create --print-join-command
```

### Step 8: Verify Cluster Status

On the control plane node, verify all nodes have joined:

```bash
kubectl get nodes
```

You should see all nodes in "Ready" status:

```
NAME                STATUS   ROLES           AGE   VERSION
nitro-v15-lyra      Ready    control-plane   10m   v1.28.x
asus-tuf-nova       Ready    <none>          5m    v1.28.x
sony-ci5-asteroth   Ready    <none>          5m    v1.28.x
```

## Advanced Configuration

### Label Nodes by Resource Capacity

Label nodes to help with pod scheduling:

```bash
# Label high-memory control plane
kubectl label nodes nitro-v15-lyra node-type=high-memory

# Label medium-memory worker
kubectl label nodes asus-tuf-nova node-type=medium-memory

# Label low-memory worker
kubectl label nodes sony-ci5-asteroth node-type=low-memory
```

### Apply Resource Quotas

Create resource quotas for different node types. See the YAML configurations in `bootstrap/k8s/` directory.

## Deploying Applications

After cluster setup, deploy applications using the provided YAML configurations:

```bash
# Deploy the black hole engine
kubectl apply -f bootstrap/k8s/black-hole-engine-deployment.yaml

# Deploy the Dom Compiler
kubectl apply -f bootstrap/k8s/dom-compiler-deployment.yaml
```

## Troubleshooting

### Node Not Ready

If a node shows "NotReady" status:

```bash
# Check kubelet status
sudo systemctl status kubelet

# Check kubelet logs
sudo journalctl -u kubelet -f
```

### Pod Network Issues

If pods can't communicate:

```bash
# Verify Calico pods are running
kubectl get pods -n kube-system | grep calico

# Check Calico logs
kubectl logs -n kube-system -l k8s-app=calico-node
```

### Reset a Node

To reset a node and start over:

```bash
sudo kubeadm reset
sudo rm -rf /etc/cni/net.d
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
```

## Next Steps

1. Set up persistent storage with TrueNAS integration
2. Configure monitoring with Prometheus and Grafana
3. Set up ingress controller for external access
4. Deploy the Dom Compiler and black hole engine services
5. Configure backup and disaster recovery

## References

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Calico Networking Documentation](https://docs.projectcalico.org/)
- [kubeadm Installation Guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
