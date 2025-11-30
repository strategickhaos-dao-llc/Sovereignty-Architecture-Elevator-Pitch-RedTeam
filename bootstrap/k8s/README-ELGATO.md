# Elgato Capture System Deployment

This directory contains the Kubernetes deployment manifests for the Elgato capture system with Ollama video analysis capabilities.

## Overview

The Elgato capture system is designed to capture video streams from Elgato hardware, analyze them using AI (Ollama with LLaVA), and stream to RTMP endpoints with NAS backup capabilities.

## Architecture

### Components

1. **Namespace**: `elgato-capture`
   - Isolated namespace for all capture system resources
   - Labeled with `app: strategickhaos-synthesis`

2. **Storage (PersistentVolumeClaims)**
   - `elgato-primary-recordings`: 500Gi storage for primary recordings
   - `elgato-secondary-recordings`: 500Gi storage for secondary recordings
   - Storage class: `local-path` (can be adjusted for your cluster)

3. **Elgato Primary Capture**
   - **Deployment**: `elgato-primary-capture`
   - **Image**: `strategickhaos/elgato-capture:latest`
   - **Capabilities**:
     - Video device access via `/dev/video0`
     - RTMP streaming to `rtmp://192.168.1.175:1935/live/primary`
     - NAS backup to `\\192.168.4.62\Intel\Captures\Primary`
     - Integration with Ollama for AI video analysis
   - **Resources**: 4Gi memory, 2 CPU cores
   - **Security**: Privileged container with host network access (required for device access)

4. **Ollama Video Analyzer**
   - **Deployment**: `ollama-video-analyzer`
   - **Image**: `ollama/ollama:latest`
   - **Model**: `llava:latest` (multimodal vision-language model)
   - **GPU**: Requires 1 NVIDIA GPU (`nvidia.com/gpu: 1`)
   - **Resources**: 8Gi memory, 4 CPU cores
   - **Storage**: Host path mounted at `/mnt/ollama_models`

5. **Services**
   - **elgato-primary-service**: LoadBalancer exposing dashboard on port 8080
   - **ollama-service**: Headless ClusterIP for internal Ollama communication

6. **Ingress**
   - **Host**: `elgato.lyra.local`
   - **Backend**: Routes to `elgato-primary-service:8080`

## Prerequisites

Before deploying this system, ensure you have:

1. **Kubernetes Cluster** with:
   - `local-path` storage provisioner (or modify `storageClassName`)
   - NVIDIA GPU support and device plugin installed
   - At least 1TB available storage across two volumes
   - Support for privileged containers and host network mode

2. **Hardware**:
   - Elgato capture device connected to the node
   - NVIDIA GPU for video analysis
   - Video device accessible at `/dev/video0` (adjust if different)

3. **Network**:
   - Access to RTMP server at `192.168.1.175:1935`
   - Access to NAS at `192.168.4.62`
   - DNS resolution for `elgato.lyra.local` (or configure your ingress controller)

4. **Node Configuration**:
   - The capture deployment requires node selection or affinity rules to run on a node with:
     - Elgato hardware attached
     - GPU available
     - Access to `/dev` devices

## Deployment

### Quick Deploy

```bash
# Deploy all resources
kubectl apply -f bootstrap/k8s/elgato-capture-deployment.yaml

# Verify deployment
kubectl get all -n elgato-capture

# Check pod status
kubectl get pods -n elgato-capture -w
```

### Step-by-Step Deploy

```bash
# 1. Create namespace
kubectl apply -f bootstrap/k8s/elgato-capture-deployment.yaml --namespace=default

# 2. Verify PVCs are bound
kubectl get pvc -n elgato-capture

# 3. Check deployments
kubectl get deployments -n elgato-capture

# 4. Monitor pod creation
kubectl get pods -n elgato-capture -w

# 5. Check services
kubectl get svc -n elgato-capture

# 6. Verify ingress
kubectl get ingress -n elgato-capture
```

## Configuration

### Environment Variables

The capture engine uses several environment variables that can be customized:

```yaml
env:
- name: CAPTURE_DEVICE
  value: "/dev/video0"              # Video device path
- name: OLLAMA_ENDPOINT
  value: "http://127.0.0.1:11434"   # Ollama API endpoint (use localhost due to hostNetwork)
- name: RTMP_ENDPOINT
  value: "rtmp://192.168.1.175:1935/live/primary"  # RTMP streaming target
- name: NAS_BACKUP
  value: "\\\\192.168.4.62\\Intel\\Captures\\Primary"  # Windows share path
```

### Storage Configuration

Adjust storage size based on your needs:

```yaml
spec:
  resources:
    requests:
      storage: 500Gi  # Modify as needed
```

### GPU Configuration

If your cluster uses a different GPU resource name:

```yaml
resources:
  limits:
    nvidia.com/gpu: 1  # Or use amd.com/gpu, etc.
```

## Accessing the System

### Dashboard

Access the Elgato capture dashboard via:

- **External LoadBalancer**: Check `kubectl get svc elgato-primary-service -n elgato-capture`
- **Ingress**: Navigate to `http://elgato.lyra.local`

### Ollama API

The Ollama service is accessible within the cluster:

```bash
# From within the cluster
curl http://ollama-service.elgato-capture.svc.cluster.local:11434/api/tags

# From the capture pod (via localhost due to hostNetwork)
curl http://127.0.0.1:11434/api/tags
```

## Monitoring

### Check Logs

```bash
# Capture engine logs
kubectl logs -f deployment/elgato-primary-capture -n elgato-capture

# Ollama logs
kubectl logs -f deployment/ollama-video-analyzer -n elgato-capture

# Follow logs from all pods
kubectl logs -f -l app=elgato-primary -n elgato-capture
kubectl logs -f -l app=ollama-analyzer -n elgato-capture
```

### Resource Usage

```bash
# Check resource usage
kubectl top pods -n elgato-capture

# Check PVC usage
kubectl get pvc -n elgato-capture
```

## Troubleshooting

### Capture Pod Not Starting

```bash
# Check pod events
kubectl describe pod -l app=elgato-primary -n elgato-capture

# Common issues:
# - Device not found: Verify /dev/video0 exists on the node
# - Privileged mode denied: Check PSP/PodSecurity policies
# - Node not available: Add node selector or affinity rules
```

### Ollama Pod Stuck Pending

```bash
# Check GPU availability
kubectl describe pod -l app=ollama-analyzer -n elgato-capture

# Common issues:
# - No GPU available: Verify GPU device plugin is running
# - Resource limits: Check cluster capacity
# - Node selector missing: May need to target GPU-enabled nodes
```

### Storage Issues

```bash
# Check PVC status
kubectl describe pvc elgato-primary-recordings -n elgato-capture

# Verify storage provisioner
kubectl get storageclass

# Check available storage
kubectl get pv
```

### Network Connectivity

```bash
# Test RTMP endpoint from capture pod
kubectl exec -it deployment/elgato-primary-capture -n elgato-capture -- sh -c 'ping -c 3 192.168.1.175'

# Test NAS connectivity
kubectl exec -it deployment/elgato-primary-capture -n elgato-capture -- sh -c 'ping -c 3 192.168.4.62'

# Test Ollama connectivity
kubectl exec -it deployment/elgato-primary-capture -n elgato-capture -- sh -c 'curl -v http://127.0.0.1:11434/api/tags'
```

## Security Considerations

### Privileged Containers

The capture pod runs in privileged mode to access hardware devices. This is necessary but should be restricted:

```yaml
securityContext:
  privileged: true  # Required for device access
```

**Mitigation**:
- Use node selectors to restrict deployment to specific nodes
- Implement Pod Security Policies/Standards
- Regularly audit container images for vulnerabilities
- Use network policies to restrict pod communication

### Host Network

The capture pod uses `hostNetwork: true` to access localhost Ollama endpoint:

```yaml
spec:
  hostNetwork: true  # Required for localhost communication
```

**Considerations**:
- Pod shares host network namespace
- Port conflicts possible with host services
- Consider using service mesh for better isolation in production

### Storage Access

Ensure appropriate permissions for NAS access:
- Use secrets for SMB/CIFS credentials if needed
- Consider using CSI drivers for Windows share mounting

## Upgrading

### Update Images

```bash
# Update capture image
kubectl set image deployment/elgato-primary-capture capture-engine=strategickhaos/elgato-capture:v2.0.0 -n elgato-capture

# Update Ollama image
kubectl set image deployment/ollama-video-analyzer ollama=ollama/ollama:latest -n elgato-capture

# Or edit the manifest and reapply
kubectl apply -f bootstrap/k8s/elgato-capture-deployment.yaml
```

### Update Ollama Models

```bash
# Exec into Ollama pod
kubectl exec -it deployment/ollama-video-analyzer -n elgato-capture -- sh

# Pull new model
ollama pull llava:13b

# Update environment variable to use new model
kubectl set env deployment/ollama-video-analyzer OLLAMA_MODELS=llava:13b -n elgato-capture
```

## Cleanup

### Remove Deployment

```bash
# Delete all resources in namespace
kubectl delete -f bootstrap/k8s/elgato-capture-deployment.yaml

# Verify cleanup
kubectl get all -n elgato-capture

# Note: PVCs and PVs may need manual deletion if retention policy is Retain
kubectl delete pvc --all -n elgato-capture
```

### Preserve Recordings

Before cleanup, backup recordings if needed:

```bash
# Port-forward to access recordings
kubectl port-forward -n elgato-capture svc/elgato-primary-service 8080:8080

# Or copy from PVC via pod
kubectl exec -it deployment/elgato-primary-capture -n elgato-capture -- tar czf /tmp/backup.tar.gz /recordings
kubectl cp elgato-capture/$(kubectl get pod -l app=elgato-primary -n elgato-capture -o jsonpath='{.items[0].metadata.name}'):/tmp/backup.tar.gz ./recordings-backup.tar.gz
```

## Support

For issues or questions:
- Check the main repository README.md
- Review logs using the monitoring commands above
- Open an issue in the repository

## License

See [LICENSE](../../LICENSE) file in the repository root.
