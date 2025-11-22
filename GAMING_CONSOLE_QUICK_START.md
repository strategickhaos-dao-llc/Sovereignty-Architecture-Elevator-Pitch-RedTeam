# Gaming Console Infrastructure - Quick Start Guide

## 🎮 One-Command Deployment

```bash
./deploy-gaming-consoles.sh
```

This single command deploys:
- ✅ 4 PlayStation gaming consoles in Kubernetes
- ✅ PlayStation Remote Play gateway
- ✅ Closed-loop network security
- ✅ 36 scholarly web resources (.org/.gov domains)

## 📊 Check Status

```bash
./manage-gaming-consoles.sh status
```

## 🔍 Quick Commands

| Command | Description |
|---------|-------------|
| `./manage-gaming-consoles.sh status` | View all components |
| `./manage-gaming-consoles.sh health` | Run health check |
| `./manage-gaming-consoles.sh logs 1` | View console 1 logs |
| `./manage-gaming-consoles.sh resources` | List 36 web pages |
| `./manage-gaming-consoles.sh restart all` | Restart all consoles |

## 🌐 Access Points

### Gateway (Load Balanced)
```
playstation-remote-play-gateway.gaming-consoles.svc.cluster.local:9987
```

### Individual Consoles
```
ps5-console-1.gaming-consoles.svc.cluster.local:9987
ps5-console-2.gaming-consoles.svc.cluster.local:9987
ps5-console-3.gaming-consoles.svc.cluster.local:9987
ps5-console-4.gaming-consoles.svc.cluster.local:9987
```

## 📚 Scholarly Resources

36 web pages from authoritative sources:
- 10 federal government (.gov) resources
- 26 educational/standards organizations (.org)

View all resources:
```bash
./manage-gaming-consoles.sh resources
```

## 🔐 Security Features

- ✅ **Closed-loop network** - Isolated namespace
- ✅ **Network policies** - Strict ingress/egress rules
- ✅ **RBAC** - Least privilege access
- ✅ **TLS 1.3** - Encryption enforced
- ✅ **Resource quotas** - Prevent resource exhaustion

## 📦 What Gets Deployed

1. **Namespace**: `gaming-consoles`
2. **StatefulSet**: 4 gaming console pods
3. **Deployment**: Remote Play gateway
4. **Services**: 5 ClusterIP services (1 gateway + 4 consoles)
5. **ConfigMaps**: PlayStation configuration + scholarly resources
6. **NetworkPolicies**: Closed-loop security
7. **RBAC**: Service account and roles
8. **PVCs**: 100Gi per console (400Gi total)

## 🚀 Advanced Usage

### Scale Consoles
```bash
./manage-gaming-consoles.sh scale 4
```

### Deploy Web Resources
```bash
./manage-gaming-consoles.sh deploy-resources
```

### Monitor Connections
```bash
./manage-gaming-consoles.sh connections
```

### View Gateway Logs
```bash
./manage-gaming-consoles.sh gateway-logs
```

## 🛠️ Troubleshooting

### Console Not Ready?
```bash
kubectl describe pod ps5-console-0 -n gaming-consoles
```

### Check Resource Usage
```bash
kubectl top pods -n gaming-consoles
```

### Network Issues?
```bash
kubectl get networkpolicy -n gaming-consoles
```

## 🗑️ Uninstall

```bash
./manage-gaming-consoles.sh uninstall
```

## 📖 Full Documentation

See [GAMING_CONSOLE_INFRASTRUCTURE.md](GAMING_CONSOLE_INFRASTRUCTURE.md) for complete details.

---

**Ready to game sovereignly!** 🎮🔒
