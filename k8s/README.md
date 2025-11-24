# Kubernetes Configuration

This directory contains Kubernetes manifests for the StrategicKhaos Operator.

## Structure

Place your Kubernetes manifests here:
- Deployments
- Services
- ConfigMaps
- Secrets
- Ingress configurations

## Usage

The StrategicKhaos-Operator.ps1 script will automatically apply all manifests in this directory when using the `-start` command:

```powershell
.\StrategicKhaos-Operator.ps1 -start
```

This will execute:
```bash
kubectl apply -f k8s/ --recursive
```
