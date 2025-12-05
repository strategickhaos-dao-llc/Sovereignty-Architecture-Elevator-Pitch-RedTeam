# Legal Entity Verification Template

## Purpose

This template provides a structured checklist and documentation format for verifying the legal entity status of Strategickhaos DAO LLC and associated entities.

---

## Entity Information

### Primary Entity

| Field | Value | Verified |
|-------|-------|----------|
| Legal Name | Strategickhaos DAO LLC / Valoryield Engine | ☐ |
| Entity Type | Limited Liability Company | ☐ |
| Management Structure | Member-Managed | ☐ |
| Formation State | Wyoming | ☐ |
| Formation Date | 2025-06-25 | ☐ |
| Domicile State | Texas | ☐ |

### Entity Identifiers

| Identifier | Value | Source | Verified |
|------------|-------|--------|----------|
| Wyoming Filing ID | 2025-001708194 | Harbor Compliance | ☐ |
| Alternative ID | 312 | Harbor Compliance | ☐ |
| EIN | 39-2923503 | IRS | ☐ |
| NAICS Code | 561611 | Self-reported | ☐ |

### Contact Information

| Field | Value | Verified |
|-------|-------|----------|
| Principal Address | 1216 S Fredonia St, Longview, TX 75602-2544 | ☐ |
| Mailing Address | Same as above | ☐ |
| Email | domenic.garza@snhu.edu | ☐ |
| Phone | +1 346-263-2887 | ☐ |

---

## Verification Checklist

### Step 1: Harbor Compliance Portal

- [ ] Log into Harbor Compliance account
- [ ] Navigate to entity dashboard
- [ ] Capture screenshot of entity status
- [ ] Download filing confirmation PDF
- [ ] Download registered agent confirmation
- [ ] Note annual report due dates

**Screenshot Timestamp:** _______________

**File Names:**
- Filing Confirmation: _______________
- Agent Confirmation: _______________

### Step 2: Wyoming Secretary of State

- [ ] Visit https://wyobiz.wyo.gov/Business/FilingSearch.aspx
- [ ] Search by entity name: "Strategickhaos DAO LLC"
- [ ] Search by filing ID: 2025-001708194
- [ ] Capture search results screenshot
- [ ] Note: New filings may not be immediately indexed

**Search Timestamp:** _______________
**Search Result:** ☐ Found ☐ Not Found ☐ Pending Indexing

### Step 3: EIN Verification

**Note:** EINs are NOT publicly searchable by IRS design.

- [ ] Locate IRS EIN confirmation letter (CP 575 or SS-4)
- [ ] Check email for IRS correspondence
- [ ] Check physical mail records
- [ ] Photograph or scan EIN documentation

**Document Located:** ☐ Yes ☐ No
**Document Type:** _______________
**Document Date:** _______________

### Step 4: Registered Agent Verification

- [ ] Confirm registered agent name
- [ ] Verify agent address is current
- [ ] Check for any correspondence from agent

**Registered Agent:** Harbor Compliance (or specify)
**Agent Status:** ☐ Active ☐ Inactive

---

## Document Collection Checklist

### Required Documents

| Document | Status | File Name | Hash |
|----------|--------|-----------|------|
| Wyoming Filing Confirmation | ☐ | | |
| EIN Confirmation (CP 575/SS-4) | ☐ | | |
| Operating Agreement | ☐ | | |
| Registered Agent Agreement | ☐ | | |
| Certificate of Formation | ☐ | | |

### Optional Documents

| Document | Status | File Name | Hash |
|----------|--------|-----------|------|
| Annual Report | ☐ | | |
| Good Standing Certificate | ☐ | | |
| Bank Account Confirmation | ☐ | | |
| Business License | ☐ | | |

---

## Privacy & Redaction Guidelines

Before making documents public, redact the following:

### Always Redact

- [ ] Social Security Numbers
- [ ] Bank account numbers
- [ ] Credit card information
- [ ] Personal phone numbers (except business contact)
- [ ] Home addresses (if different from business)

### Consider Redacting

- [ ] Full names (use initials if preferred)
- [ ] Specific dollar amounts (use ranges)
- [ ] Internal reference numbers

### Never Redact (Required for Verification)

- [ ] Entity name
- [ ] Filing ID numbers
- [ ] EIN (required for legal verification)
- [ ] Business address
- [ ] Formation date
- [ ] Entity type

---

## Verification Statement Template

### For Public Repository

```markdown
## Legal Entity Verification Statement

I, [FULL NAME], confirm that:

1. **Strategickhaos DAO LLC** is a legally formed Limited Liability Company
2. Formation jurisdiction: Wyoming
3. Formation date: [DATE]
4. Wyoming Filing ID: [ID]
5. Federal EIN: [EIN]

I have personally verified this information through:
- Harbor Compliance portal access
- IRS correspondence
- Wyoming Secretary of State records (where available)

Signed: ________________________
Date: _________________________
GPG Key: 261AEA44C0AF89CD

[GPG SIGNATURE BLOCK]
```

---

## Common Verification Issues

### Issue: Entity Not Found in Public Search

**Possible Causes:**
1. Too new - not yet indexed (can take 2-4 weeks)
2. Search syntax incorrect (try variations)
3. Privacy settings limiting public visibility
4. Filed under slightly different name

**Solution:**
- Use Harbor Compliance portal as primary source
- Contact Wyoming SOS directly if needed
- Wait and re-check if recently filed

### Issue: EIN Returns No Results

**This is EXPECTED behavior.**

**Explanation:**
- EINs are NOT publicly searchable
- IRS protects this information
- Only the entity owner and authorized parties can verify

**Solution:**
- Use IRS-issued documentation (CP 575, SS-4)
- Contact IRS if documentation is lost

### Issue: Can't Access Harbor Compliance

**Solution:**
- Reset password
- Contact Harbor Compliance support
- Use recovery email/phone

---

## After Verification

### Next Steps

1. [ ] Save all documents securely
2. [ ] Create redacted versions for public sharing
3. [ ] Generate SHA-256 hashes of originals
4. [ ] Create anchor file with document hashes
5. [ ] Sign anchor file with GPG key
6. [ ] Upload to public proof repository

### File Naming Convention

```
ENTITY_TYPE_DATE_VERSION.pdf

Examples:
- WYOMING_FILING_20250625_v1.pdf
- EIN_CONFIRMATION_20250701_v1.pdf
- OPERATING_AGREEMENT_20250625_v1_REDACTED.pdf
```

### Hash Generation

```bash
# Generate hashes for all documents
sha256sum *.pdf > document_hashes.txt

# Verify later
sha256sum -c document_hashes.txt
```

---

## Verification Complete Checklist

Before marking verification as complete:

- [ ] All required documents collected
- [ ] All documents reviewed for accuracy
- [ ] Sensitive information redacted from public versions
- [ ] SHA-256 hashes generated
- [ ] Anchor file created
- [ ] Anchor file GPG signed
- [ ] Documents uploaded to secure storage
- [ ] Public versions uploaded to proof repository
- [ ] Verification statement signed

**Verification Status:** ☐ Complete ☐ Pending ☐ In Progress

**Completed By:** _______________
**Completion Date:** _______________
**GPG Signature:** _______________

---

*Legal Entity Verification Template v1.0*
*Sovereignty Architecture Project*
*For internal verification purposes*
