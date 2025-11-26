# Quick Start Guide

**Get the Security Testing Suite running in 10 minutes**

---

## Prerequisites

Ensure you have installed:
- Python 3.9+
- pip (Python package manager)

---

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to the security testing suite
cd security-testing-suite

# Install Python dependencies
pip install requests hypothesis pyjwt

# For full scanning capabilities (optional)
pip install semgrep bandit safety detect-secrets locust
```

---

## Step 2: Install OPA (1 minute)

```bash
# Linux/macOS
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod +x opa
sudo mv opa /usr/local/bin/

# Verify installation
opa version
```

---

## Step 3: Test OPA Policies (1 minute)

```bash
# Run the included policy tests
opa test policies/ -v

# Expected output:
# policies/authz_test.rego:
# data.authz_test.test_admin_can_read: PASS
# data.authz_test.test_admin_can_write: PASS
# ... (25+ tests)
```

---

## Step 4: Run OPA Fuzzing (2 minutes)

```bash
# Generate 500 random test cases
python tooling/opa_fuzz.py \
    --policy policies/authz.rego \
    --iterations 500 \
    --output reports/fuzz_results.ndjson

# View the report
cat reports/fuzz_report.json | python -m json.tool
```

---

## Step 5: Run Security Scan (3 minutes)

```bash
# Make the script executable
chmod +x tooling/security_scan.sh

# Run all security scans
./tooling/security_scan.sh --all --target ../

# Or run specific scans
./tooling/security_scan.sh --sast    # Static analysis only
./tooling/security_scan.sh --sca     # Dependency scanning only
./tooling/security_scan.sh --secrets # Secrets detection only
```

---

## Step 6: Test Your API (2 minutes)

If you have a FastAPI application running:

```bash
# Basic security test
python tooling/fastapi_security_test.py \
    --target http://localhost:8000

# With authentication
python tooling/fastapi_security_test.py \
    --target http://localhost:8000 \
    --auth-header "Bearer YOUR_TOKEN" \
    --output reports/api_security.json
```

---

## Step 7: Verify Audit Chain (Optional)

```bash
# Generate sample audit chain
python tooling/verify_audit_chain.py \
    --generate-sample 50 \
    --output reports/sample_chain.ndjson

# Verify the chain integrity
python tooling/verify_audit_chain.py \
    --file reports/sample_chain.ndjson \
    --output reports/chain_verification.json
```

---

## Step 8: Load Testing (Optional)

### Using k6

```bash
# Install k6 first (https://k6.io/docs/getting-started/installation/)
k6 run load-tests/api_load_test.js \
    --env TARGET_URL=http://localhost:8000
```

### Using Locust

```bash
# Run Locust web UI
locust -f load-tests/locustfile.py \
    --host=http://localhost:8000

# Or headless mode
locust -f load-tests/locustfile.py \
    --host=http://localhost:8000 \
    --headless \
    -u 50 \
    -r 5 \
    -t 1m
```

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Run OPA tests | `opa test policies/ -v` |
| Fuzz OPA policies | `python tooling/opa_fuzz.py -p policies/ -n 500` |
| Full security scan | `./tooling/security_scan.sh --all` |
| API security test | `python tooling/fastapi_security_test.py -t http://localhost:8000` |
| Verify audit chain | `python tooling/verify_audit_chain.py -f audit.ndjson` |
| k6 load test | `k6 run load-tests/api_load_test.js` |
| Locust load test | `locust -f load-tests/locustfile.py` |

---

## CI/CD Integration

Add the GitHub Actions workflow to your repository:

```bash
# Copy the workflow
cp .github/workflows/security-testing.yml /path/to/your/repo/.github/workflows/

# Commit and push
cd /path/to/your/repo
git add .github/workflows/security-testing.yml
git commit -m "Add security testing workflow"
git push
```

---

## Troubleshooting

### OPA not found

```bash
# Check if OPA is in PATH
which opa

# If not, add to PATH
export PATH=$PATH:/path/to/opa
```

### Python module not found

```bash
# Install missing modules
pip install <module-name>

# Or install all requirements
pip install requests hypothesis pyjwt semgrep bandit safety
```

### Permission denied on scripts

```bash
chmod +x tooling/security_scan.sh
chmod +x tooling/*.py
```

---

## Next Steps

1. **Customize policies** - Edit `policies/authz.rego` for your RBAC needs
2. **Add to CI/CD** - Use the GitHub Actions workflow
3. **Monitor continuously** - Set up scheduled scans
4. **Integrate alerting** - Connect to Discord/Slack/PagerDuty

---

## Support

For issues and questions, see the main [README.md](README.md) or open a GitHub issue.

---

**Empire Eternal** ∞
