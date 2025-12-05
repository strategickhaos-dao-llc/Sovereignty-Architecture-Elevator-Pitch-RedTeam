# FastAPI + OPA Security Testing Suite

**Strategickhaos Sovereign Infrastructure**

A comprehensive, production-ready security testing suite for FastAPI applications with OPA (Open Policy Agent) integration. Designed for deployment on sovereign Kubernetes clusters with full observability integration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)
- [CI/CD Integration](#cicd-integration)
- [Configuration](#configuration)
- [Reporting](#reporting)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Contributing](#contributing)

---

## Overview

This security testing suite provides comprehensive coverage for:

- **Static Application Security Testing (SAST)** - Source code analysis
- **Software Composition Analysis (SCA)** - Dependency vulnerability scanning
- **Secrets Detection** - Credential and API key scanning
- **OPA Policy Testing** - Authorization policy validation and fuzzing
- **API Security Testing** - Authentication, injection, and vulnerability testing
- **Audit Chain Verification** - Cryptographic integrity verification
- **Load Testing** - Performance under security constraints

---

## Features

### 🔍 Security Scanning

| Tool | Purpose | Coverage |
|------|---------|----------|
| Semgrep | SAST | SQL injection, XSS, command injection, hardcoded secrets |
| Bandit | Python SAST | Insecure crypto, shell injection, SQL injection |
| Safety | Python SCA | Known CVEs in dependencies |
| npm audit | JavaScript SCA | Known vulnerabilities in npm packages |
| TruffleHog | Secrets | Git history secrets, API keys, credentials |
| detect-secrets | Secrets | Pre-commit secrets detection |

### 🔐 OPA Policy Testing

- **Unit Tests** - Comprehensive test coverage with `authz_test.rego`
- **Fuzzing** - Property-based testing with Hypothesis
- **Edge Cases** - Null, empty, malformed, and oversized inputs
- **Coverage Analysis** - Policy coverage reporting
- **Performance Testing** - Policy evaluation latency

### 🌐 API Security Testing

- Authentication bypass detection
- JWT manipulation and weak secret testing
- SQL injection detection
- Command injection detection
- XSS vulnerability scanning
- IDOR (Insecure Direct Object Reference) testing
- Rate limiting verification
- Security header validation
- CORS configuration testing

### 📊 Load Testing

- **k6** - Multi-stage load profiles (20 → 50 → 100 users)
- **Locust** - Multiple user behavior patterns
- Policy evaluation time tracking
- P95/P99 latency thresholds
- Failure rate monitoring

### 🔗 Audit Chain Verification

- Hash chain integrity verification
- Sequence continuity checking
- Timestamp monotonicity validation
- Tamper detection
- Watch mode for continuous monitoring

---

## Quick Start

```bash
# Clone the repository
git clone <your-repo>
cd security-testing-suite

# Install Python dependencies
pip install -r requirements.txt

# Install OPA
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod +x opa && sudo mv opa /usr/local/bin/

# Run OPA policy tests
opa test policies/ -v

# Run security scan
chmod +x tooling/security_scan.sh
./tooling/security_scan.sh --all

# Test your API
python tooling/fastapi_security_test.py --target http://localhost:8000
```

See [QUICKSTART.md](QUICKSTART.md) for a complete 10-minute deployment guide.

---

## Components

### Directory Structure

```
security-testing-suite/
├── policies/                 # OPA policies
│   ├── authz.rego           # Authorization policy
│   └── authz_test.rego      # Policy tests
├── tooling/                  # Security testing scripts
│   ├── opa_fuzz.py          # OPA policy fuzzer
│   ├── fastapi_security_test.py  # API security tester
│   ├── verify_audit_chain.py     # Audit verification
│   └── security_scan.sh     # Orchestration script
├── load-tests/               # Load testing scripts
│   ├── api_load_test.js     # k6 load test
│   └── locustfile.py        # Locust load test
├── .github/workflows/        # CI/CD integration
│   └── security-testing.yml # GitHub Actions workflow
├── README.md                 # This file
└── QUICKSTART.md            # Quick deployment guide
```

---

## Installation

### Prerequisites

- Python 3.9+
- Node.js 18+ (for k6)
- OPA CLI
- Docker (optional, for container testing)

### Python Dependencies

```bash
pip install \
    requests \
    hypothesis \
    pyjwt \
    semgrep \
    bandit \
    safety \
    detect-secrets \
    locust
```

### Install OPA

```bash
# Linux
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod +x opa
sudo mv opa /usr/local/bin/

# macOS
brew install opa

# Windows
choco install open-policy-agent
```

### Install k6

```bash
# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# macOS
brew install k6
```

---

## Usage

### OPA Policy Testing

```bash
# Run unit tests
opa test policies/ -v

# Run with coverage
opa test policies/ --coverage --format=json

# Fuzz testing
python tooling/opa_fuzz.py \
    --policy policies/authz.rego \
    --iterations 1000 \
    --output reports/fuzz_results.ndjson \
    --report reports/fuzz_report.json
```

### Security Scanning

```bash
# Run all scans
./tooling/security_scan.sh --all

# SAST only
./tooling/security_scan.sh --sast

# SCA only
./tooling/security_scan.sh --sca

# Secrets detection only
./tooling/security_scan.sh --secrets

# OPA testing only
./tooling/security_scan.sh --opa

# Specify target directory
./tooling/security_scan.sh --all --target /path/to/project
```

### API Security Testing

```bash
# Basic scan
python tooling/fastapi_security_test.py \
    --target http://localhost:8000

# With authentication
python tooling/fastapi_security_test.py \
    --target http://localhost:8000 \
    --auth-header "Bearer YOUR_TOKEN"

# Output to JSON
python tooling/fastapi_security_test.py \
    --target http://localhost:8000 \
    --output reports/api_security.json

# Verbose output
python tooling/fastapi_security_test.py \
    --target http://localhost:8000 \
    --verbose
```

### Audit Chain Verification

```bash
# Generate sample chain
python tooling/verify_audit_chain.py \
    --generate-sample 100 \
    --output sample_chain.ndjson

# Verify chain
python tooling/verify_audit_chain.py \
    --file audit_logs.ndjson \
    --output verification_report.json

# Watch mode (continuous monitoring)
python tooling/verify_audit_chain.py \
    --file audit_logs.ndjson \
    --watch \
    --poll-interval 5

# Strict mode
python tooling/verify_audit_chain.py \
    --file audit_logs.ndjson \
    --strict
```

### Load Testing

```bash
# k6 load test
k6 run load-tests/api_load_test.js \
    --env TARGET_URL=http://localhost:8000 \
    --env AUTH_TOKEN=your-token

# Locust load test
locust -f load-tests/locustfile.py \
    --host=http://localhost:8000 \
    --headless \
    -u 100 \
    -r 10 \
    -t 5m
```

---

## CI/CD Integration

### GitHub Actions

The included workflow (`.github/workflows/security-testing.yml`) provides:

- **Push triggers** - Scan on push to main/develop
- **Pull request checks** - Security gate for PRs
- **Nightly scans** - Comprehensive scheduled scanning
- **Manual dispatch** - On-demand full scans

```yaml
# Example: Add to your repository's workflows
- uses: ./.github/workflows/security-testing.yml
```

### Security Gate

The workflow includes a security gate that:
- Fails on critical vulnerabilities
- Warns on high severity issues
- Posts summary to pull requests
- Uploads SARIF to GitHub Security

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TARGET_DIR` | Directory to scan | Project root |
| `REPORTS_DIR` | Report output directory | `./reports` |
| `POLICIES_DIR` | OPA policies directory | `./policies` |
| `OPA_BINARY` | Path to OPA binary | `opa` |

### OPA Policy Customization

Edit `policies/authz.rego` to customize:
- Role definitions
- Action permissions
- Protected resources
- Public endpoints

---

## Reporting

### Report Formats

| Format | Use Case |
|--------|----------|
| JSON | Programmatic consumption, CI/CD integration |
| NDJSON | Log aggregation (Loki, Elasticsearch) |
| SARIF | GitHub Security tab integration |
| Console | Human-readable output |

### Prometheus Metrics

Export metrics for Grafana dashboards:
- `security_scan_duration_seconds`
- `security_findings_total{severity}`
- `opa_policy_coverage_percent`
- `api_security_test_results`

---

## Kubernetes Deployment

### CronJob for Scheduled Scanning

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-scanner
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scanner
            image: your-registry/security-scanner:latest
            command:
            - /bin/bash
            - -c
            - ./tooling/security_scan.sh --all
          restartPolicy: OnFailure
```

### Distributed Testing

Deploy across multiple clusters:

```bash
# Nova cluster
kubectl --context=nova apply -f k8s/security-testing.yaml

# Lyra cluster
kubectl --context=lyra apply -f k8s/security-testing.yaml

# Athena cluster
kubectl --context=athena apply -f k8s/security-testing.yaml
```

---

## Security Considerations

This suite is designed with security in mind:

- **No external data exfiltration** - All testing is local-first
- **Minimal dependencies** - Reduced attack surface
- **Audit logging** - All operations are logged
- **Cryptographic verification** - Hash chain integrity
- **Air-gap compatible** - Works in isolated environments

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run existing tests
4. Add tests for new features
5. Submit a pull request

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - 10-minute deployment guide
- [OPA Documentation](https://www.openpolicyagent.org/docs/)
- [Semgrep Rules](https://semgrep.dev/explore)
- [k6 Documentation](https://k6.io/docs/)
- [Locust Documentation](https://locust.io/)

---

**Empire Eternal** ∞

*"Where comprehensive security testing meets sovereign infrastructure."*
