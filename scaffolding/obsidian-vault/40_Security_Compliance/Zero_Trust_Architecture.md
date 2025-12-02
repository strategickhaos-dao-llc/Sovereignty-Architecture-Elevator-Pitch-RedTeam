# Zero Trust Architecture

**Canon References: #66-70**

## Core Principle

**"Never trust, always verify."**

Traditional security: Trust based on network location (inside firewall = trusted)
Zero Trust: Trust nothing by default, verify everything explicitly

```
Traditional:                  Zero Trust:
                              
Inside Network = Trusted      Every Access = Verified
Outside = Untrusted           Location Irrelevant
                              
┌─────────────────┐          ┌─────────────────┐
│   🔓 Trusted   │          │  Verify Identity│
│    Intranet     │          │  Check Context  │
│                 │          │  Enforce Policy │
│   All access    │          │  Continuous     │
│   allowed       │          │  Re-validation  │
└─────────────────┘          └─────────────────┘
```

## Five Pillars

### 1. Never Trust, Always Verify (#66)

Every request is authenticated and authorized, regardless of source.

**Implementation:**
```typescript
// Every API call checks auth
async function handleRequest(req: Request) {
  // 1. Extract identity
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return { status: 401, body: 'No token' };
  
  // 2. Verify identity
  const identity = await verifyToken(token);
  if (!identity) return { status: 401, body: 'Invalid token' };
  
  // 3. Check authorization
  const allowed = await checkPermission(identity, req.resource, req.action);
  if (!allowed) return { status: 403, body: 'Forbidden' };
  
  // 4. Log the access
  await auditLog.record({ identity, resource: req.resource, action: req.action });
  
  // 5. Process request
  return await processRequest(req, identity);
}
```

**No Exceptions:**
- Internal services verify each other
- Admin users still authenticate
- Localhost requests are not automatically trusted

### 2. Least Privilege Access (#67)

Minimal permissions required for the task, nothing more.

**Principle:** If compromised, blast radius is minimal.

**Example: Service Permissions**
```yaml
# Bad: Overly broad permissions
permissions:
  - read:*
  - write:*
  - delete:*

# Good: Minimal required permissions
permissions:
  - read:users.profile
  - write:users.last_login
  # No delete access
  # No access to sensitive fields (SSN, passwords)
```

**Example: Time-Bound Access**
```typescript
// Grant temporary elevated access
async function grantTemporaryAccess(userId: string, resource: string, duration: number) {
  const token = await generateToken({
    userId,
    resource,
    permissions: ['read', 'write'],
    expiresAt: Date.now() + duration
  });
  
  // Automatically revoked after duration
  return token;
}
```

**JIT (Just-In-Time) Access:**
- No standing privileges for sensitive operations
- Request → Approval → Time-limited access → Auto-revoke
- Example: "I need prod database access for 1 hour to debug issue #123"

### 3. Microsegmentation (#68)

Network segmentation at the workload level, not just perimeter.

**Traditional:** Trust everything inside the network
**Zero Trust:** Each workload isolated, explicit allow rules

```
Traditional Network:              Zero Trust Microsegmentation:

┌─────────────────────────┐     ┌──────┐  ┌──────┐  ┌──────┐
│  All services can       │     │ Web  │─→│ API  │─→│  DB  │
│  talk to each other     │     └──────┘  └──────┘  └──────┘
│                         │         ↓         ↓         ↓
│  Web ↔ API ↔ DB ↔      │     Allow     Allow     Allow
│  Cache ↔ Queue ↔ ...   │     only      only      only
└─────────────────────────┘     required  required  required
                                 paths     paths     paths
```

**Kubernetes NetworkPolicy Example:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

### 4. Strong Authentication (#69)

Multi-factor, passwordless, hardware-backed authentication.

**Authentication Hierarchy (Strongest → Weakest):**
1. **Hardware Security Keys** (FIDO2/WebAuthn) - YubiKey, etc.
2. **Biometric + Device** (Face ID + phone ownership)
3. **TOTP + Password** (Google Authenticator + password)
4. **SMS + Password** (Weak, SIM-swap vulnerable)
5. **Password alone** (❌ Never sufficient)

**Implementation: Passwordless WebAuthn**
```typescript
// Registration
async function registerSecurityKey(userId: string) {
  const challenge = generateRandomChallenge();
  
  // Client creates credential with hardware key
  const credential = await navigator.credentials.create({
    publicKey: {
      challenge,
      rp: { name: "Sovereignty System" },
      user: { id: userId, name: userId, displayName: userId },
      pubKeyCredParams: [{ type: "public-key", alg: -7 }], // ES256
      authenticatorSelection: { userVerification: "required" }
    }
  });
  
  // Server stores public key
  await storePublicKey(userId, credential.publicKey);
}

// Authentication
async function authenticate(userId: string) {
  const challenge = generateRandomChallenge();
  
  // Client signs challenge with hardware key
  const assertion = await navigator.credentials.get({
    publicKey: {
      challenge,
      allowCredentials: await getStoredCredentials(userId)
    }
  });
  
  // Server verifies signature
  const valid = await verifySignature(assertion, challenge);
  if (!valid) throw new Error('Authentication failed');
  
  return generateSessionToken(userId);
}
```

### 5. Continuous Verification (#70)

Trust is not binary or permanent. Continuously reassess.

**Adaptive Authentication:**
```typescript
interface AccessContext {
  identity: Identity;
  device: DeviceInfo;
  location: GeoLocation;
  time: Date;
  sensitivity: 'low' | 'medium' | 'high';
}

async function evaluateAccess(context: AccessContext): Promise<Decision> {
  const riskScore = calculateRiskScore(context);
  
  if (riskScore < 0.3) {
    // Low risk: Allow
    return { allow: true };
  } else if (riskScore < 0.7) {
    // Medium risk: Step-up authentication
    return { allow: false, require: 'mfa' };
  } else {
    // High risk: Deny
    await alertSecurityTeam(context);
    return { allow: false, reason: 'Suspicious activity' };
  }
}

function calculateRiskScore(context: AccessContext): number {
  let score = 0;
  
  // New device?
  if (!context.device.recognized) score += 0.3;
  
  // Unusual location?
  if (context.location.distance > 1000) score += 0.2; // >1000km from usual
  
  // Unusual time?
  if (context.time.getHours() < 6 || context.time.getHours() > 22) score += 0.1;
  
  // Accessing sensitive data?
  if (context.sensitivity === 'high') score += 0.2;
  
  // Recent failed login attempts?
  const recentFailures = await getRecentFailures(context.identity);
  if (recentFailures > 3) score += 0.4;
  
  return Math.min(score, 1.0);
}
```

## Implementation Patterns

### Service-to-Service Authentication

**Mutual TLS (mTLS):**
```yaml
# Both client and server verify each other's certificates
apiVersion: v1
kind: Service
metadata:
  name: api
  annotations:
    service.istio.io/tls-mode: mutual
spec:
  ports:
  - port: 8080
```

**Service Mesh (Istio/Linkerd):**
- Automatic mTLS between services
- Identity-based authorization policies
- Observability of all service-to-service traffic

### API Gateway with Zero Trust

```typescript
// Gateway enforces zero trust for all APIs
class ZeroTrustGateway {
  async handleRequest(req: Request): Promise<Response> {
    // 1. Authenticate
    const identity = await this.authenticate(req);
    
    // 2. Context-aware authorization
    const context = this.buildContext(identity, req);
    const decision = await this.authorize(context);
    
    if (!decision.allow) {
      if (decision.require === 'mfa') {
        return this.challengeMFA(identity);
      }
      return new Response('Forbidden', { status: 403 });
    }
    
    // 3. Proxy with identity header
    req.headers.set('X-Identity', identity.id);
    req.headers.set('X-Identity-Claims', JSON.stringify(identity.claims));
    
    // 4. Forward to backend
    const response = await fetch(this.getBackendUrl(req), req);
    
    // 5. Audit log
    await this.auditLog(identity, req, response);
    
    return response;
  }
}
```

## Zero Trust for AI Agents

**Special Considerations:**

### Agent Identity
```typescript
interface AgentIdentity {
  agentId: string;
  heirVersion: string;
  createdBy: string;
  capabilities: string[]; // ['read:data', 'write:logs', 'execute:code']
  trustScore: number; // Evolves based on behavior
}
```

### Tool Access Control
```typescript
class AgentToolAccess {
  async canUseTool(agent: AgentIdentity, tool: string): Promise<boolean> {
    // Check explicit permissions
    if (!agent.capabilities.includes(`use:${tool}`)) {
      await this.auditLog(`Agent ${agent.agentId} denied ${tool} - no permission`);
      return false;
    }
    
    // Check trust score
    if (agent.trustScore < 0.7 && SENSITIVE_TOOLS.includes(tool)) {
      await this.auditLog(`Agent ${agent.agentId} denied ${tool} - low trust`);
      return false;
    }
    
    // Rate limiting per agent
    const usage = await this.getRecentUsage(agent.agentId, tool);
    if (usage > RATE_LIMITS[tool]) {
      await this.auditLog(`Agent ${agent.agentId} denied ${tool} - rate limit`);
      return false;
    }
    
    return true;
  }
}
```

### Evolution Safeguards
```typescript
// Heir evolution must be authorized
async function evolveHeir(heir: Heir, newDNA: DNA) {
  // 1. Verify evolution request is legitimate
  const authorized = await verifyEvolutionRequest(heir, newDNA);
  if (!authorized) throw new Error('Unauthorized evolution');
  
  // 2. Check constraints
  if (newDNA.capabilities.length > heir.dna.capabilities.length * 1.5) {
    throw new Error('Evolution too rapid - capability growth limited');
  }
  
  // 3. Sandbox test new DNA
  const testEnv = await createSandbox();
  const testResult = await testEnv.runHeir(newDNA);
  if (!testResult.safe) {
    await quarantine(newDNA);
    throw new Error('Unsafe evolution detected');
  }
  
  // 4. Gradual rollout
  await rolloutEvolution(heir, newDNA, { canary: 0.01 });
}
```

## Monitoring Zero Trust

**Key Metrics:**
- Authentication failures by source IP
- Authorization denials by resource
- Step-up authentication triggers
- Device/location anomalies
- Service-to-service auth failures

**Alerting:**
```typescript
// Alert on suspicious patterns
if (authFailures > 10 in 5 minutes) {
  alert('Possible brute force attack');
}

if (newDevice && sensitiveAccess) {
  alert('New device accessing sensitive data');
}

if (geoDistance > 500km && timeDelta < 1hour) {
  alert('Impossible travel detected');
}
```

## Related Concepts

- [[Least_Privilege]] - Deep dive on minimal permissions
- [[Authentication_Methods]] - MFA, WebAuthn, biometrics
- [[Service_Mesh]] - Zero trust for microservices
- [[Audit_Logging]] - Recording all access decisions

## Further Reading

- NIST SP 800-207: Zero Trust Architecture
- "Zero Trust Networks" by Gilman & Barth
- Google BeyondCorp papers
- Azure Zero Trust guidance

---

**Key Takeaway:** In a zero trust world, verification is continuous, context-aware, and never assumes trust based on location or past behavior. Build systems where every access is a fresh security decision.
