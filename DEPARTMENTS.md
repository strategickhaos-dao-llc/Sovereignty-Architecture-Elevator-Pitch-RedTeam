# Departments Overview

**Organizational structure for specialized functions within the Sovereignty Architecture.**

## 🏛️ Department System

The Sovereignty Architecture includes specialized departments that handle specific operational functions:

### 🔐 Identity & Access Management (IAM)
**Location:** `departments/iam/`

Handles all aspects of user identity, authentication, and access control across the ecosystem.

**Key Functions:**
- User registration and onboarding
- Multi-factor authentication
- Cross-platform identity linking (GitHub, Discord, GitLens)
- Role-based access control (RBAC)
- Session management and security

**API Endpoint:** `/api/iam`
**Service Port:** 8090
**Discord Channel:** `#iam`

**Quick Start:**
```bash
# Register a new user
./departments/iam/register-user.sh \
  --name "Jane Doe" \
  --email "jane@example.com" \
  --github "janedoe"

# Link accounts via Discord
/register  # Use in Discord to start interactive registration
```

📖 **[Full Documentation](departments/iam/README.md)**

---

### 📜 Patent & IP Research
**Location:** `departments/patent-research/`

Autonomous patent scanning and intellectual property protection system.

**Key Functions:**
- Automated patent database scanning (USPTO, EPO, WIPO)
- Prior art detection and analysis
- Design and innovation tracking with cryptographic proofs
- Freedom to operate (FTO) analysis
- Patent application support

**API Endpoint:** `/api/patent-research`
**Service Port:** 8095
**Discord Channels:** 
- `#patent-alerts` - Priority findings
- `#research` - General updates

**Autonomous Scanning:**
- Schedule: Weekly (Monday 04:00 UTC)
- Databases: USPTO, EPO, WIPO, Google Patents
- Technology domains: AI/ML, Distributed Systems, DevOps, Security, Data Processing

**Quick Start:**
```bash
# Run manual scan
./departments/patent-research/autonomous-scanner.sh \
  --databases "uspto,epo,wipo" \
  --keywords "vector-search,RAG"

# Register a design
./departments/patent-research/register-design.sh \
  --title "My Innovation" \
  --inventors "Your Name"

# Generate FTO report
./departments/patent-research/fto-report.sh \
  --product "my-product" \
  --territory "US,EU"
```

📖 **[Full Documentation](departments/patent-research/README.md)**

---

## 🔌 Integration

### Discord Integration

Both departments integrate with Discord for notifications and user interaction:

**IAM Commands:**
- `/register` - Register new user account
- `/link` - Link platform identities
- `/whoami` - View your identity information
- `/profile` - View or update profile

**Patent Research Commands:**
- `/patent-scan` - Trigger manual patent scan
- `/fto-check` - Check freedom to operate for a product
- `/design-register` - Register a new design/innovation

### API Integration

All departments expose RESTful APIs for programmatic access:

```typescript
// IAM API
POST /api/iam/register      // Register user
POST /api/iam/login         // Authenticate
POST /api/iam/link          // Link identity
GET  /api/iam/users         // List users
GET  /api/iam/stats         // Get statistics

// Patent Research API
POST /api/patent-research/scan        // Trigger scan
GET  /api/patent-research/scans       // List scan history
POST /api/patent-research/designs     // Register design
GET  /api/patent-research/prior-art   // Query prior art
POST /api/patent-research/fto         // Generate FTO report
```

### GitLens Integration

IAM department tracks GitLens user activity and links VS Code users to the central identity system.

### GitHub Integration

Both departments integrate with GitHub:
- **IAM:** OAuth authentication, org member syncing
- **Patent Research:** Repository scanning for innovations, automatic design registration

---

## 📊 Monitoring

### Health Checks

All department services expose health check endpoints:

```bash
# IAM health
curl http://localhost:8090/health

# Patent Research health
curl http://localhost:8095/health
```

### Metrics

Prometheus metrics available at:
- IAM: `http://localhost:9091/metrics`
- Patent Research: `http://localhost:9095/metrics`

### Dashboards

Grafana dashboards available:
- `iam-overview` - IAM statistics and activity
- `patent-research-overview` - Patent scanning metrics

---

## 🚀 Deployment

### Docker Compose

```yaml
services:
  iam-service:
    build: ./departments/iam
    ports:
      - "8090:8090"
    environment:
      - DATABASE_URL=${IAM_DB_URL}
      - DISCORD_TOKEN=${DISCORD_TOKEN}
    
  patent-research-service:
    build: ./departments/patent-research
    ports:
      - "8095:8095"
    environment:
      - DATABASE_URL=${PATENT_DB_URL}
      - USPTO_API_KEY=${USPTO_API_KEY}
```

### Kubernetes

```bash
# Deploy IAM
kubectl apply -f departments/iam/k8s/

# Deploy Patent Research
kubectl apply -f departments/patent-research/k8s/
```

---

## 🔐 Security

### IAM Security
- Password hashing with bcrypt (12 rounds)
- JWT token signing with RS256
- MFA support (TOTP, backup codes)
- Rate limiting on authentication
- Comprehensive audit logging

### Patent Research Security
- Confidential information protection
- Access control for sensitive patent data
- Attorney-client privilege maintained
- Cryptographic proofs for design timestamps
- Secure API key management

---

## 📈 Metrics & KPIs

### IAM Metrics
- Total registered users
- Active sessions
- MFA adoption rate
- Identity linking success rate
- Authentication success/failure rate

### Patent Research Metrics
- Patents scanned per period
- Priority alerts generated
- Designs registered
- FTO clearances completed
- Average scan processing time

---

## 🛠️ Development

### Adding a New Department

1. Create department directory: `departments/my-department/`
2. Add configuration: `departments/my-department/config.yaml`
3. Implement service code
4. Update `discovery.yml` with department config
5. Add Discord integration (optional)
6. Document in README
7. Deploy and test

### Department Template

```yaml
# departments/my-department/config.yaml
version: "1.0"
department: "my-department"
description: "My department description"

my_department:
  enabled: true
  service_port: 8XXX
  api_endpoint: "/api/my-department"
  # ... specific configuration
```

---

## 📚 Resources

- [IAM Documentation](departments/iam/README.md)
- [Patent Research Documentation](departments/patent-research/README.md)
- [Main README](README.md)
- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)

---

## 🤝 Support

For department-specific questions:
- **IAM:** `#iam` channel on Discord
- **Patent Research:** `#patent-alerts` or `#research` channels

For general support: `#support` channel or create a GitHub issue.

---

**Maintained by the Strategickhaos Team**
*Building sovereign infrastructure through specialized departments*
