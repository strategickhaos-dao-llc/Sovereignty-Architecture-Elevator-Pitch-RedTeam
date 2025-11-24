# Kubernetes Manifests for StrategicKhaos Operator

This directory contains Kubernetes manifests for deploying the StrategicKhaos sovereign AI infrastructure.

## Files

- **bot-deployment.yaml** - Discord bot deployment
- **gateway-deployment.yaml** - Event gateway deployment
- **configmap.yaml** - Configuration data
- **secrets.yaml** - Sensitive credentials (⚠️ REQUIRES CUSTOMIZATION)
- **ingress.yaml** - Ingress rules for external access
- **rbac.yaml** - Role-based access control

## ⚠️ Important: Configuration Before Deployment

### 1. Secrets Management

The `secrets.yaml` file contains **placeholder values starting with "REPLACE_"** that must be replaced before deployment:

```bash
# DO NOT use default secrets in production!
# Replace with actual values:
kubectl create secret generic discord-bot-secret \
  --from-literal=token=YOUR_ACTUAL_DISCORD_TOKEN

kubectl create secret generic gateway-secret \
  --from-literal=webhook-secret=YOUR_ACTUAL_WEBHOOK_SECRET
```

### 2. Configuration Values

The `configmap.yaml` file contains **placeholder values** for:
- **Discord Guild ID**: Required - Get from Discord Server Settings → Widget → Server ID
- **Discord Bot App ID**: Required - Get from Discord Developer Portal
- **GitHub App ID**: Optional - Only needed if using Git integration

Replace all values marked with "REPLACE_WITH_" before deployment.

### 3. Container Images

Both `bot-deployment.yaml` and `gateway-deployment.yaml` use the `latest` tag by default:
- **Development**: `latest` tag is acceptable
- **Production**: Replace with specific version tags (e.g., `v1.0.0`) for predictable deployments

### Recommended: Use External Secret Management

For production environments, consider using:
- **HashiCorp Vault** - Enterprise secret management
- **Sealed Secrets** - Encrypted secrets in Git
- **External Secrets Operator** - Integrate with cloud secret managers
- **SOPS** - Encrypted YAML files

## Deployment

The StrategicKhaos Operator will automatically apply these manifests when you run:

```powershell
.\StrategicKhaos-Operator.ps1 -start
```

Or manually:

```bash
kubectl apply -f k8s/ --recursive
```

## Verification

Check deployment status:

```bash
kubectl get all -n default
kubectl get ingress
kubectl logs -l app=discord-bot
kubectl logs -l app=event-gateway
```

## Security Notes

- Replace all placeholder secrets before production deployment
- Use RBAC to limit access to sensitive resources
- Enable network policies for pod-to-pod communication
- Regularly rotate credentials
- Use TLS for all external connections
