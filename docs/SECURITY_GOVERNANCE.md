# Security & Governance

## Security Model

The Strategickhaos Sovereignty Architecture implements a defense-in-depth security model with multiple layers of protection.

## Multi-Layer Security

### Layer 1: Network Security

```yaml
# Network policies restrict pod-to-pod communication
networkPolicies:
  - name: discord-ops-bot
    ingress:
      - from:
          - namespaceSelector:
              matchLabels:
                name: ops
        ports:
          - protocol: TCP
            port: 8080
    egress:
      - to:
          - ipBlock:
              cidr: 0.0.0.0/0
        ports:
          - protocol: TCP
            port: 443  # Discord API, GitHub API
```

### Layer 2: Authentication & Authorization

#### RBAC Configuration

```yaml
rbac:
  prod_role: "ReleaseMgr"
  allow_commands:
    - "/status"
    - "/logs"
    - "/deploy"
    - "/scale"
    - "/review"
  prod_protected_commands:
    - "/deploy"
    - "/scale"
```

#### Kubernetes RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: discord-ops-bot
  namespace: ops
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "patch"]
  - apiGroups: ["apps"]
    resources: ["deployments/scale"]
    verbs: ["patch"]
```

### Layer 3: Secret Management

#### Vault Integration

```yaml
secrets_manager: "vault"
secrets:
  discord_token:
    path: "vault://kv/discord/bot_token"
    rotate_days: 30
  webhook_secret:
    path: "vault://kv/events/hmac_key"
    rotate_days: 90
  github_app_key:
    path: "vault://kv/git/app_private_key"
    rotate_days: 365
```

#### Secret Rotation

```python
async def rotate_secret(secret_name: str):
    """Rotate a secret in Vault and update Kubernetes."""
    # Generate new secret
    new_value = generate_secret(secret_name)
    
    # Store in Vault
    await vault.write(f"kv/{secret_name}", {"value": new_value})
    
    # Update Kubernetes secret
    await k8s.patch_secret("discord-ops-secrets", {
        secret_name: base64.encode(new_value)
    })
    
    # Trigger rolling restart
    await k8s.rollout_restart("deployment/discord-ops-bot")
```

### Layer 4: Webhook Verification

#### HMAC Signature Verification

```python
import hmac
import hashlib

def verify_signature(body: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature from webhook."""
    expected = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)
```

#### GitHub App Verification

```python
from github import GithubIntegration

async def verify_github_webhook(request: Request) -> bool:
    """Verify GitHub webhook signature."""
    signature = request.headers.get("X-Hub-Signature-256")
    body = await request.body()
    secret = os.environ["GITHUB_WEBHOOK_SECRET"]
    
    return verify_signature(body, signature, secret)
```

## Governance Framework

### Change Management

```yaml
governance:
  approvals:
    prod_commands_require: ["ReleaseMgr"]
  change_management:
    link: "https://wiki.strategickhaos.internal/change-management"
    required_for:
      - production_deployments
      - infrastructure_changes
      - security_policy_updates
```

### Approval Workflow

```
1. Developer requests deployment via /deploy
2. Bot checks user has ReleaseMgr role
3. Bot creates change request ticket
4. Approver reviews in Discord thread
5. On approval, deployment proceeds
6. Audit log records full workflow
```

### Data Handling Policy

```yaml
data_handling:
  post_pii_to_discord: false
  redaction:
    patterns:
      - "(?i)api[_-]?key\\s*[:=]\\s*\\S+"
      - "(?i)password\\s*[:=]\\s*\\S+"
      - "Bearer\\s+[A-Za-z0-9._-]+"
      - "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
```

### Content Redaction

```python
import re

def redact_sensitive(content: str) -> str:
    """Redact sensitive information from content."""
    patterns = config.security.redaction.patterns
    
    for pattern in patterns:
        content = re.sub(pattern, "[REDACTED]", content)
    
    return content
```

## Audit Logging

### Log Structure

```json
{
  "timestamp": "2024-01-15T10:23:45.123Z",
  "event_type": "command_execution",
  "user": {
    "id": "123456789",
    "name": "developer#1234",
    "roles": ["developer", "ReleaseMgr"]
  },
  "command": {
    "name": "/deploy",
    "args": {
      "env": "staging",
      "tag": "v1.2.3"
    }
  },
  "channel": {
    "id": "987654321",
    "name": "#deployments"
  },
  "result": {
    "status": "success",
    "message": "Deployment triggered",
    "workflow_id": "12345"
  },
  "metadata": {
    "ip": "10.0.0.1",
    "user_agent": "Discord Bot"
  }
}
```

### Log Sink Configuration

```yaml
audit_log_sink: "cloudwatch://discord-audit"
```

### Audit Trail Retention

```yaml
retention:
  audit_logs: 365  # days
  metrics: 90      # days
  traces: 30       # days
```

## Security Incident Response

### Detection

```python
async def detect_anomaly(event: AuditEvent):
    """Detect potential security anomalies."""
    # Rate limiting violation
    if await is_rate_limited(event.user_id):
        await alert_security("Rate limit exceeded", event)
    
    # Unauthorized command attempt
    if event.result.status == "unauthorized":
        await alert_security("Unauthorized access attempt", event)
    
    # Off-hours activity
    if is_off_hours() and event.command.name in SENSITIVE_COMMANDS:
        await alert_security("Off-hours sensitive command", event)
```

### Response

```python
async def respond_to_incident(incident: SecurityIncident):
    """Automated incident response."""
    severity = incident.severity
    
    if severity == "critical":
        # Immediate lockdown
        await disable_bot_commands()
        await notify_security_team(incident, urgent=True)
        await create_incident_ticket(incident)
    
    elif severity == "high":
        await notify_security_team(incident)
        await increase_logging_verbosity()
    
    # Always log
    await audit_log.record(incident)
```

## Compliance

### Supported Frameworks

```yaml
compliance:
  frameworks:
    - soc2
    - iso27001
    - gdpr
  evidence_collection:
    enabled: true
    storage: "s3://compliance-evidence"
```

### Compliance Checks

```python
async def compliance_check():
    """Run periodic compliance checks."""
    checks = [
        check_secret_rotation(),
        check_rbac_policies(),
        check_network_policies(),
        check_audit_log_retention(),
    ]
    
    results = await asyncio.gather(*checks)
    
    for result in results:
        if not result.passed:
            await alert_compliance_team(result)
```

## LLM Directive: Security Extensions

> **AI Agent Note**: When extending security features:
> 1. Never log or transmit secrets in plaintext
> 2. Always use HMAC verification for webhooks
> 3. Apply rate limiting to all public endpoints
> 4. Implement audit logging for all state changes
> 5. Follow principle of least privilege for RBAC

---

*Part of the Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane*
