# Documentation Notes and Placeholders

## Overview

This documentation package is designed to guide the user through three critical actions. Several files contain intentional placeholders that should be updated once the actions are completed.

---

## Intentional Placeholders

### USPTO Application Numbers

**Files to Update After Filing:**

1. **CAPSTONE_COMPLETE.md**
   - Line 19-20: Update status from "🟡 READY" to "✅ FILED"
   - Add application numbers where indicated

2. **sovereignty-architecture-preprint.tex**
   - Line references to USPTO applications
   - Update from "Application pending" to actual numbers

3. **FILING_CHECKLIST.md**
   - Filing Receipt Documentation section
   - Record actual application numbers after filing

**Update Format:**
```
Application Number: [ACTUAL NUMBER FROM USPTO]
Filing Date: 2025-11-23 (or actual date)
Confirmation Number: [FROM RECEIPT]
```

---

### ORCID Identifier

**Files to Update After Registration:**

1. **sovereignty-architecture-preprint.tex**
   - Line 31: Replace "(pending registration)" with actual ORCID
   - Format: `0000-0003-XXXX-XXXX`

2. **CAPSTONE_COMPLETE.md**
   - Multiple references to ORCID
   - Update with actual identifier

3. **LEGAL_ACADEMIC_INDEX.md**
   - ORCID profile references
   - Update with working URL

**Update Format:**
```latex
% In LaTeX:
ORCID: 0000-0003-1234-5678  % Replace XXXX with actual numbers

% In Markdown:
ORCID: https://orcid.org/0000-0003-1234-5678
```

---

### Zenodo DOI

**Files to Update After Publication:**

1. **All documentation referring to DOI**
   - Replace `10.5281/zenodo.XXXXXXX` with actual DOI
   - Update all `https://doi.org/10.5281/zenodo.XXXXXXX` links

2. **README.md**
   - Add DOI badge once published

3. **sovereignty-architecture-preprint.tex**
   - Update references and self-citation

**DOI Badge Format:**
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)]
(https://doi.org/10.5281/zenodo.1234567)
```

---

### Signature and Verification Blocks

**100_LAWS_OF_THE_SOVEREIGN_TINKERER.md**
- Lines 278-279: Cryptographic signature block
- Update after GPG signing:

```
GPG Signature: (Add actual signature or signature file reference)
SHA-256 Hash: (Compute: sha256sum 100_LAWS_OF_THE_SOVEREIGN_TINKERER.md)
```

**How to Generate:**
```bash
# Generate SHA-256 hash
sha256sum legal/patents/prior-art/100_LAWS_OF_THE_SOVEREIGN_TINKERER.md

# Generate GPG signature (if GPG is configured)
gpg --armor --detach-sign legal/patents/prior-art/100_LAWS_OF_THE_SOVEREIGN_TINKERER.md
# Creates: 100_LAWS_OF_THE_SOVEREIGN_TINKERER.md.asc
```

---

## Post-Completion Update Checklist

### After USPTO Filing
- [ ] Update FILING_CHECKLIST.md with application numbers
- [ ] Update CAPSTONE_COMPLETE.md status to "✅ FILED"
- [ ] Update sovereignty-architecture-preprint.tex with application numbers
- [ ] Commit changes with message: "Add USPTO provisional application numbers"

### After ORCID Registration  
- [ ] Update sovereignty-architecture-preprint.tex with ORCID
- [ ] Update all author references with ORCID URL
- [ ] Update email signature
- [ ] Commit changes with message: "Add ORCID to all author attributions"

### After Zenodo Publication
- [ ] Update all DOI placeholders with actual DOI
- [ ] Add DOI badge to README.md
- [ ] Update sovereignty-architecture-preprint.tex self-citation
- [ ] Commit changes with message: "Add Zenodo DOI to all documentation"

### After GPG Signing (Optional)
- [ ] Sign 100_LAWS_OF_THE_SOVEREIGN_TINKERER.md
- [ ] Compute SHA-256 hash
- [ ] Update signature block in document
- [ ] Commit .asc signature file
- [ ] Commit changes with message: "Add cryptographic signatures to prior art"

---

## Automated Update Script (Optional)

Create a script to help update placeholders:

```bash
#!/bin/bash
# update-placeholders.sh

USPTO_APP_1="$1"  # First application number
USPTO_APP_2="$2"  # Second application number
ORCID="$3"        # ORCID identifier
ZENODO_DOI="$4"   # Zenodo DOI number

if [ -z "$USPTO_APP_1" ] || [ -z "$USPTO_APP_2" ] || [ -z "$ORCID" ] || [ -z "$ZENODO_DOI" ]; then
    echo "Usage: $0 <uspto_app_1> <uspto_app_2> <orcid> <zenodo_doi>"
    echo "Example: $0 63/123456 63/123457 0000-0003-1234-5678 1234567"
    exit 1
fi

# Update USPTO application numbers
find . -type f -name "*.md" -o -name "*.tex" | while read file; do
    sed -i.bak "s/USPTO Application XXXXXXXX (Negative-Balance)/USPTO Application $USPTO_APP_1/g" "$file"
    sed -i.bak "s/USPTO Application XXXXXXXX (Neurodivergent)/USPTO Application $USPTO_APP_2/g" "$file"
done

# Update ORCID
find . -type f -name "*.md" -o -name "*.tex" | while read file; do
    sed -i.bak "s/0000-0003-XXXX-XXXX/$ORCID/g" "$file"
    sed -i.bak "s/(pending registration)/$ORCID/g" "$file"
done

# Update Zenodo DOI
find . -type f -name "*.md" -o -name "*.tex" | while read file; do
    sed -i.bak "s/zenodo\.XXXXXXX/zenodo.$ZENODO_DOI/g" "$file"
done

echo "✅ Placeholders updated!"
echo "Review changes and commit:"
echo "  git diff"
echo "  git add ."
echo "  git commit -m 'Update placeholders with actual values'"
```

---

## Verification Before Publication

Before publishing the 100 Laws as prior art, verify:

1. **Date is Correct:** Reflects actual publication date
2. **Entity Information:** Wyoming filing and EIN are accurate
3. **License Terms:** CC BY 4.0 properly applied
4. **Timestamp:** Git commit provides cryptographic timestamp
5. **Publication Channels:** GitHub + X/Twitter for public disclosure

---

## Documentation Integrity

**Version Control:**
- All documentation tracked in Git
- Timestamps verifiable via Git history
- Cryptographic commit signatures (if GPG configured)
- Immutable history provides proof of priority

**Prior Art Establishment:**
- Public disclosure on GitHub (open source)
- Timestamped commits
- Optional: X/Twitter public posts
- Optional: Wayback Machine archiving

---

## Contact for Questions

If unclear about any placeholder or update procedure:

- **Review:** Relevant guide (FILING_CHECKLIST.md, ORCID_SETUP_GUIDE.md, etc.)
- **Documentation:** LEGAL_ACADEMIC_INDEX.md (complete index)
- **Quick Start:** QUICK_START_LEGAL_ACADEMIC.md (60-minute workflow)
- **Repository:** Check commit history for examples

---

## Final Notes

These placeholders are **intentional design decisions** to ensure documentation is ready for immediate use. The user will naturally fill in actual values as they complete each action.

All guides include clear instructions on where and how to update these values once obtained.

---

**Document Status:** Complete  
**Placeholders:** Intentional - to be updated during execution  
**Last Updated:** 2025-11-23  
**Author:** Domenic Garza (Node 137)  
**Purpose:** Clarify placeholder strategy for code review
