# 📖 CYB 200 - Cybersecurity Foundations Spellbook

> **Hogwarts Protocol Integration**  
> *"Defense Against the Dark Arts of the Digital Realm"*

---

## 🎯 Course Objectives

By completing this spellbook, you will:

1. Understand the CIA Triad (Confidentiality, Integrity, Availability)
2. Identify common cyber threats and attack vectors
3. Apply basic security controls and countermeasures
4. Analyze risk management frameworks
5. Implement fundamental security practices

---

## 📚 Chapter 1: The CIA Triad

### Confidentiality 🔒
```
Definition: Ensuring information is accessible only to authorized parties

Spells (Controls):
- Encryption (AES, RSA)
- Access Control Lists (ACLs)
- Authentication mechanisms
- Data classification

Example Incantation (Python):
```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt secret message
secret = b"Sovereignty Architecture is online"
encrypted = cipher.encrypt(secret)
print(f"Protected: {encrypted}")
```

### Integrity ✅
```
Definition: Ensuring data has not been tampered with

Spells (Controls):
- Hash functions (SHA-256, SHA-3)
- Digital signatures
- Version control
- Checksums

Example Incantation (Python):
```python
import hashlib

def verify_integrity(data: bytes, expected_hash: str) -> bool:
    """Verify data integrity using SHA-256"""
    calculated = hashlib.sha256(data).hexdigest()
    return calculated == expected_hash

# Create integrity hash
message = b"Critical configuration file"
integrity_hash = hashlib.sha256(message).hexdigest()
print(f"Integrity seal: {integrity_hash}")
```

### Availability 🌐
```
Definition: Ensuring systems and data are accessible when needed

Spells (Controls):
- Redundancy
- Load balancing
- Backup systems
- DDoS protection

Example Architecture:
```
┌─────────────┐
│ Load Balancer│
└──────┬──────┘
       │
  ┌────┼────┐
  │    │    │
┌─┴─┐┌─┴─┐┌─┴─┐
│S1 ││S2 ││S3 │  ← Redundant servers
└───┘└───┘└───┘
```

---

## 📚 Chapter 2: Threat Landscape

### Common Attack Vectors

| Threat | Description | Defense Spell |
|--------|-------------|---------------|
| Phishing | Social engineering via email | User training, email filters |
| Malware | Malicious software | Antivirus, sandboxing |
| DDoS | Overwhelming traffic | Rate limiting, CDN |
| SQL Injection | Database manipulation | Parameterized queries |
| XSS | Script injection | Input validation |
| MITM | Interception attacks | TLS/SSL encryption |

### Threat Actor Categories

1. **Script Kiddies** - Low skill, use existing tools
2. **Hacktivists** - Politically motivated
3. **Organized Crime** - Profit-driven
4. **Nation States** - Advanced Persistent Threats (APTs)
5. **Insider Threats** - Internal malicious actors

---

## 📚 Chapter 3: Security Frameworks

### NIST Cybersecurity Framework

```
┌────────────────────────────────────────────────────────┐
│                    NIST CSF                            │
├────────────┬────────────┬────────────┬────────────────┤
│  IDENTIFY  │  PROTECT   │   DETECT   │    RESPOND     │
│            │            │            │    RECOVER     │
├────────────┼────────────┼────────────┼────────────────┤
│ Asset Mgmt │ Access Ctrl│ Anomalies  │ Response Plan  │
│ Risk Assess│ Training   │ Monitoring │ Communications │
│ Governance │ Data Sec   │ Detection  │ Analysis       │
│            │ Maintenance│            │ Mitigation     │
└────────────┴────────────┴────────────┴────────────────┘
```

### Implementation Tiers

- **Tier 1: Partial** - Ad hoc, reactive
- **Tier 2: Risk Informed** - Approved but not organization-wide
- **Tier 3: Repeatable** - Formal policies, regularly reviewed
- **Tier 4: Adaptive** - Continuous improvement, lessons learned

---

## 📚 Chapter 4: Risk Management

### Risk Formula
```
Risk = Threat × Vulnerability × Impact
```

### Risk Assessment Process

1. **Identify Assets** - What are you protecting?
2. **Identify Threats** - What could harm your assets?
3. **Identify Vulnerabilities** - What weaknesses exist?
4. **Analyze Impact** - What's the damage if exploited?
5. **Calculate Risk** - Prioritize based on likelihood and impact
6. **Implement Controls** - Apply appropriate countermeasures

### Risk Response Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| Accept | Acknowledge and monitor | Low-impact risks |
| Mitigate | Reduce likelihood/impact | Apply patches |
| Transfer | Share with third party | Cyber insurance |
| Avoid | Eliminate risk source | Remove vulnerable system |

---

## 📚 Chapter 5: Security Controls

### Control Categories

#### Administrative Controls
- Security policies
- Training programs
- Background checks
- Incident response procedures

#### Technical Controls
- Firewalls
- Encryption
- Access control systems
- Intrusion detection

#### Physical Controls
- Locks and barriers
- Security cameras
- Biometric access
- Environmental controls

### Defense in Depth

```
    ┌─────────────────────────────────────┐
    │         PHYSICAL SECURITY           │
    │  ┌───────────────────────────────┐  │
    │  │      NETWORK SECURITY         │  │
    │  │  ┌─────────────────────────┐  │  │
    │  │  │    HOST SECURITY        │  │  │
    │  │  │  ┌───────────────────┐  │  │  │
    │  │  │  │ APPLICATION SEC   │  │  │  │
    │  │  │  │  ┌─────────────┐  │  │  │  │
    │  │  │  │  │  DATA       │  │  │  │  │
    │  │  │  │  │  SECURITY   │  │  │  │  │
    │  │  │  │  └─────────────┘  │  │  │  │
    │  │  │  └───────────────────┘  │  │  │
    │  │  └─────────────────────────┘  │  │
    │  └───────────────────────────────┘  │
    └─────────────────────────────────────┘
```

---

## 🧪 Lab Exercises

### Lab 1: Password Analysis
```python
import re

def check_password_strength(password: str) -> dict:
    """Analyze password strength"""
    checks = {
        'length': len(password) >= 12,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'numbers': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    }
    
    score = sum(checks.values())
    strength = 'Weak' if score < 3 else 'Medium' if score < 5 else 'Strong'
    
    return {
        'checks': checks,
        'score': f"{score}/5",
        'strength': strength
    }

# Test
result = check_password_strength("Sovereignty@2024!")
print(result)
```

### Lab 2: Basic Network Scan Simulation
```python
import socket

def port_scan_simulation(target: str, ports: list) -> dict:
    """Educational port scan simulation (use only on authorized systems)"""
    results = {}
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        try:
            result = sock.connect_ex((target, port))
            results[port] = 'Open' if result == 0 else 'Closed'
        except socket.error:
            results[port] = 'Error'
        finally:
            sock.close()
    
    return results

# Only scan your own systems!
# results = port_scan_simulation('localhost', [22, 80, 443, 8080])
```

### Lab 3: Hash Verification
```python
import hashlib
import os

def create_file_integrity_baseline(directory: str) -> dict:
    """Create integrity baseline for files"""
    baseline = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                baseline[filepath] = file_hash
            except PermissionError:
                baseline[filepath] = 'ACCESS_DENIED'
    
    return baseline

def verify_integrity(baseline: dict) -> list:
    """Check files against baseline"""
    alerts = []
    
    for filepath, expected_hash in baseline.items():
        if expected_hash == 'ACCESS_DENIED':
            continue
            
        try:
            with open(filepath, 'rb') as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            
            if current_hash != expected_hash:
                alerts.append(f"MODIFIED: {filepath}")
        except FileNotFoundError:
            alerts.append(f"DELETED: {filepath}")
    
    return alerts
```

---

## ✅ Mastery Quiz

### Questions

1. What are the three components of the CIA Triad?
2. Name three types of threat actors.
3. What is the NIST Cybersecurity Framework's five core functions?
4. Explain the risk formula.
5. What is "Defense in Depth"?
6. Name two administrative, technical, and physical controls each.
7. What's the difference between a vulnerability and a threat?
8. How would you respond to a detected security incident?

### Practical Assessment

Complete the following tasks:
- [ ] Create a password strength checker
- [ ] Build a file integrity monitoring script
- [ ] Document a personal risk assessment
- [ ] Design a defense-in-depth architecture

---

## 🏆 Mastery Milestones

- [ ] **Apprentice** - Complete Chapter 1 & Quiz
- [ ] **Journeyman** - Complete Lab 1-2
- [ ] **Expert** - Complete all labs and assessment
- [ ] **Master** - Apply concepts to Sovereignty Architecture

---

## 🔗 Integration with StrategicKhaos

### Repository Connections
- Apply CIA Triad to `sovereignty-architecture` configs
- Implement integrity checks in `security-playbooks`
- Use risk framework for `dao_record.yaml` decisions

### Real-World Application
- The `VAULT_SECURITY_PLAYBOOK.md` implements these concepts
- The `100-point security framework` builds on this foundation
- All Docker containers follow Defense in Depth principles

---

*"As above, so below. Secure the foundation, protect the sovereignty."* 🔐

**Spellbook Version:** 1.0  
**Last Updated:** December 2024  
**Course:** CYB 200 - Cybersecurity Foundations
