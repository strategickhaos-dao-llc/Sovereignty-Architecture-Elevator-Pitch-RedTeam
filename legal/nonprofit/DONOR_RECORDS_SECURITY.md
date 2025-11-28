# Donor Records Security - Strategickhaos DAO LLC + Valoryield Nonprofit Arm

## Overview

This document outlines the security measures and procedures for protecting donor records using SHA-256 cryptographic hashing while maintaining privacy and compliance.

---

## Security Architecture

### Privacy-First Design
Our donor record system is built on the principle that **donor privacy is paramount** while maintaining complete compliance and auditability.

### Key Features
- **SHA-256 Hashing**: Cryptographic hashing protects donor identity
- **Secure Storage**: Distributed infrastructure with encryption at rest
- **Access Control**: Role-based access to donor information
- **Audit Trail**: Complete logging of all donor record access
- **Compliance**: Meets IRS 501(c)(3) and state requirements

---

## SHA-256 Hashing Implementation

### Why SHA-256?
- **Cryptographic Strength**: Industry-standard hashing algorithm
- **One-Way Function**: Cannot reverse-engineer donor identity from hash
- **Collision Resistant**: Virtually impossible to generate duplicate hashes
- **Deterministic**: Same donor information always produces same hash
- **Fast Verification**: Quickly verify donor records without exposing PII

### Hashing Process

```bash
# Generate donor record hash
./hash_donor_record.sh \
  --donor-info "encrypted_donor_data.json" \
  --salt "$(openssl rand -base64 32)" \
  --algorithm "sha256" \
  --output "donor_hash.txt"
```

#### Data Flow
1. **Input**: Donor provides information (name, address, donation amount)
2. **Salting**: Unique salt added to prevent rainbow table attacks
3. **Hashing**: HMAC-SHA256 applied to donor data + salt for verification hash
4. **Encryption**: Data encrypted with AES-256 for storage
5. **Storage**: Hash and encrypted data stored separately
6. **Verification**: HMAC-SHA256 hash used to verify record integrity without decryption

---

## Data Storage Architecture

### Multi-Layer Security

```
┌─────────────────────────────────────────┐
│  Layer 1: Donor Information (PII)       │
│  - Encrypted with AES-256               │
│  - Stored in secure database            │
│  - Access logged and restricted         │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 2: Cryptographic Hash            │
│  - SHA-256 hash of encrypted data       │
│  - Used for verification                │
│  - Publicly auditable (no PII exposed)  │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 3: Transaction Record            │
│  - Donation amount and date             │
│  - Tax receipt number                   │
│  - Hash reference (no PII)              │
└─────────────────────────────────────────┘
```

### Storage Locations
- **Primary**: Longview, TX Node (encrypted database)
- **Backup**: Cheyenne, WY Node (encrypted backup)
- **Archive**: Arweave (hashes only, no PII)

---

## Access Control Matrix

### Role-Based Access

| Role | Access Level | Can View PII | Can Verify Hash | Can Generate Receipt |
|------|--------------|--------------|-----------------|---------------------|
| **Donor** | Own records only | Yes (own) | Yes (own) | Yes (own) |
| **Finance Officer** | All records | Yes | Yes | Yes |
| **Auditor** | All hashes | No | Yes | No |
| **Board Member** | Summary only | No | No | No |
| **Public** | None | No | Yes (verify) | No |

### Access Logging
```bash
# All access is logged with:
- Timestamp
- User ID and role
- Records accessed (by hash, not PII)
- Action performed
- IP address and location
- Success/failure status
```

---

## Donation Processing Workflow

### Step 1: Donation Receipt
```bash
# Donor makes donation
./receive_donation.sh \
  --donor-id "auto-generated-uuid" \
  --amount "100.00" \
  --date "YYYY-MM-DD" \
  --method "credit-card"
```

### Step 2: Record Creation
```bash
# Create encrypted donor record
./create_donor_record.sh \
  --donor-info "name,email,address" \
  --donation-amount "100.00" \
  --encrypt-aes256 \
  --generate-hash-sha256 \
  --store-secure
```

### Step 3: Hash Generation
```bash
# Generate verification hash using HMAC-SHA256
echo -n "${DONOR_DATA}" | openssl dgst -sha256 -hmac "${SALT}" > donor_verification_hash.txt
```

### Step 4: Receipt Issuance
```bash
# Generate tax-deductible receipt
./generate_receipt.sh \
  --donor-hash "$(cat donor_verification_hash.txt)" \
  --amount "100.00" \
  --date "YYYY-MM-DD" \
  --ein "39-2923503" \
  --send-email
```

### Step 5: Compliance Recording
```bash
# Record for IRS compliance (hash only)
./record_compliance.sh \
  --donor-hash "$(cat donor_verification_hash.txt)" \
  --amount "100.00" \
  --receipt-number "RCP-2025-00001" \
  --arweave-store
```

---

## Privacy Protection Measures

### No PII in Public Records
- **Arweave Storage**: Only hashes stored, never PII
- **Public Audits**: Hash verification available without exposing donors
- **IRS Reporting**: Aggregate data only, individual hashes for verification

### Encryption Standards
- **At Rest**: AES-256 encryption for all stored donor data
- **In Transit**: TLS 1.3 for all data transmission
- **Key Management**: HSM-backed encryption key storage
- **Key Rotation**: Annual rotation of encryption keys

### Data Minimization
- Only collect information necessary for tax receipts
- No selling or sharing of donor information
- No third-party access to donor data
- Automatic deletion of unnecessary data after retention period

---

## Verification Process

### Donor Verification
Donors can verify their donation records without exposing their identity:

```bash
# Donor provides their original information
./verify_donation.sh \
  --donor-email "donor@example.com" \
  --donor-name "John Doe" \
  --amount "100.00" \
  --date "YYYY-MM-DD"

# System generates hash and checks against stored hashes
# Returns: "Verified: Donation record found and confirmed"
```

### Auditor Verification
Auditors can verify donation integrity without accessing PII:

```bash
# Auditor checks hash integrity
./audit_donor_records.sh \
  --verify-all-hashes \
  --check-receipt-numbers \
  --validate-totals \
  --date-range "2025-01-01:2025-12-31"

# Output: Summary report with hash verification status
```

---

## IRS Compliance

### 501(c)(3) Requirements Met
✅ **Donor Receipts**: All donations acknowledged with proper receipts
✅ **Record Keeping**: 7-year retention of all donation records
✅ **Substantiation**: Proper documentation for donations over $250
✅ **Quid Pro Quo**: Disclosure for donations with goods/services
✅ **Privacy**: Donor information protected per IRS guidelines

### Annual Reporting (Form 990)
```bash
# Generate Form 990 data without exposing donor PII
./generate_990_data.sh \
  --year "2025" \
  --include-totals \
  --verify-hashes \
  --no-donor-pii \
  --output "form_990_schedule_b_data.csv"
```

---

## Security Monitoring

### Real-Time Monitoring
```bash
# Monitor for suspicious access patterns
./monitor_donor_records.sh \
  --alert-on-unusual-access \
  --alert-on-failed-verification \
  --alert-on-bulk-queries \
  --notify-security-team
```

### Security Alerts
- Unusual access patterns detected
- Failed verification attempts
- Bulk query attempts
- Unauthorized access attempts
- Encryption key usage anomalies

---

## Monthly Audit Process

### Audit Checklist
- [ ] All donation records have valid SHA-256 hashes
- [ ] All hashes verify against encrypted records
- [ ] No PII exposed in public records
- [ ] All receipts issued and documented
- [ ] Access logs reviewed for anomalies
- [ ] Encryption keys rotated if scheduled
- [ ] Backup systems verified
- [ ] Compliance requirements met

### Audit Report Generation
```bash
# Generate monthly audit report
./audit_donor_security.sh \
  --month "YYYY-MM" \
  --verify-all-hashes \
  --check-access-logs \
  --validate-encryption \
  --output-report "donor_security_audit_YYYY-MM.pdf"
```

---

## Disaster Recovery

### Backup Strategy
- **Real-Time Backup**: Continuous replication to WY node
- **Daily Backup**: Encrypted backup to secure cloud storage
- **Monthly Archive**: Permanent hash storage on Arweave
- **Quarterly Test**: Full disaster recovery drill

### Recovery Procedures
```bash
# In case of primary system failure
./recover_donor_records.sh \
  --restore-from-backup "cheyenne-wy-node" \
  --verify-all-hashes \
  --validate-encryption \
  --test-access-controls
```

---

## Best Practices

### For Administrators
1. **Regular Audits**: Complete monthly security audits
2. **Access Review**: Review access logs weekly
3. **Key Management**: Secure encryption key storage
4. **Backup Verification**: Test backups monthly
5. **Incident Response**: Have plan ready for security incidents

### For Auditors
1. **Hash Verification**: Verify all hashes during audits
2. **No PII Access**: Use hashes for verification only
3. **Report Issues**: Immediately report any security concerns
4. **Documentation**: Maintain detailed audit trails

### For Donors
1. **Keep Records**: Retain donation receipts for tax purposes
2. **Verify Donations**: Use verification system to confirm records
3. **Report Issues**: Contact us if discrepancies found
4. **Trust Privacy**: Your information is protected with enterprise-grade security

---

## Integration with Nonprofit Stack

### Deployment Integration
```bash
./deploy_nonprofit_stack.sh \
  --donor-records-sha256 \
  --encrypt-aes256 \
  --secure-storage \
  --audit-monthly
```

---

## Contact & Support

### Security Concerns
- **Email**: security@strategickhaos.dao
- **Emergency**: Node 137 security contact
- **Incident Report**: Use secure reporting system

### Donor Support
- **Donation Verification**: verify@strategickhaos.dao
- **Receipt Requests**: receipts@strategickhaos.dao
- **Privacy Questions**: privacy@strategickhaos.dao

---

*Security Policy Version: 1.0*
*Last Updated: November 2025*
*Compliance: IRS 501(c)(3), Wyoming DAO LLC, Texas Foreign LLC*
