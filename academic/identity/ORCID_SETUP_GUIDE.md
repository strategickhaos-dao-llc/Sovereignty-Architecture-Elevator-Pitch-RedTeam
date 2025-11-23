# ORCID Registration and Setup Guide

## What is ORCID?

**ORCID (Open Researcher and Contributor ID)** is a persistent digital identifier that distinguishes you from every other researcher. It's your academic passport and is essential for:

- Scholarly publishing and citations
- Grant applications and funding
- Academic profile management
- Research attribution and credit
- Institutional affiliations tracking

**Your ORCID Format:** `0000-0003-XXXX-XXXX` (16 digits with checksum)

---

## Quick Registration (60 Seconds)

### Step 1: Navigate to ORCID
```
URL: https://orcid.org/register
```

### Step 2: Fill Registration Form

**Required Information:**
- First Name: `Domenic`
- Last Name: `Garza`
- Email: `domenic.garza@snhu.edu` (primary academic email)
- Additional Email: (optional - add backup)
- Password: (strong password, save to password manager)
- Visibility Settings: `Public` (recommended for academic work)

**Terms:**
- [✓] I consent to the privacy policy
- [✓] I am not a robot (CAPTCHA)

### Step 3: Verify Email
```
1. Check email inbox for verification message
2. Click verification link
3. Log in to activate account
```

### Step 4: Complete Profile

**Essential Profile Information:**
- **Name:** Domenic Garza
- **Country:** United States
- **Keywords:** 
  - Neurodivergent Computing
  - Swarm Intelligence
  - Distributed Systems
  - Computational Sovereignty
  - Resource-Constrained Computing
- **Biography:** Brief description of research focus
- **Website:** https://github.com/Strategickhaos (optional)

---

## Linking Your Work

### Add Employment/Affiliation

```
Organization: Strategickhaos DAO LLC / Valoryield Engine
Role: Founder & Principal Researcher
Department: Research & Development
Start Date: June 2025
City: Longview
State/Province: Texas
Country: United States
```

### Add Education

```
Institution: Southern New Hampshire University (SNHU)
Degree: (Your current program)
Field of Study: Computer Science / Information Technology
Start Date: (Your start date)
End Date: (Expected graduation or "present")
```

### Add Works (After Publication)

Once your pre-print is uploaded to Zenodo or Google Scholar:

```
1. Navigate to "Works" section
2. Click "Add Works"
3. Choose "Search & Link" or "Add Manually"
4. Enter DOI from Zenodo: 10.5281/zenodo.XXXXXXX
5. Verify imported metadata
6. Set visibility to "Public"
7. Save
```

---

## Connecting Research Outputs

### Link USPTO Patent Applications

```
Section: Works → Add Manually
Title: "Negative-Balance Computing System"
Type: Patent
Publication Date: 2025-11-23
Country: United States
Patent Number: (Application number after filing)
URL: https://patentcenter.uspto.gov/...
```

Repeat for second provisional:
```
Title: "Neurodivergent Swarm Intelligence Architecture"
Type: Patent
(Same details as above)
```

### Link GitHub Repositories

```
Section: Works → Add Manually
Title: "Sovereignty Architecture - Implementation"
Type: Online Resource / Software
URL: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
Description: Open-source implementation of Sovereignty Architecture framework
```

### Link Pre-Print

After Zenodo upload:
```
Section: Works → Search & Link
DOI: 10.5281/zenodo.XXXXXXX
Title: "Sovereignty Architecture: A Framework for Negative-Balance Computing..."
Type: Pre-print
Publication Date: 2025-11-23
```

---

## Privacy and Visibility Settings

### Recommended Settings

**Public (Everyone):**
- Name
- ORCID iD
- Biography
- Keywords
- Employment (Strategickhaos DAO LLC)
- Works and publications
- Patents

**Trusted Parties (Institutions you grant access):**
- Additional email addresses
- Education history

**Private (Only you):**
- Personal details you don't want public
- Draft works before publication

### Update Settings
```
1. Go to Account Settings
2. Click "Visibility settings"
3. Adjust each section as needed
4. Save changes
```

---

## Integration with Research Infrastructure

### Google Scholar
```
1. Create/update Google Scholar profile
2. Add ORCID to Scholar profile
3. Link works from both directions
4. Verify citation tracking
```

### ResearchGate (Optional)
```
1. Create ResearchGate account
2. Import ORCID publications
3. Link ORCID in profile settings
4. Enable automatic sync
```

### Academic Institutions
```
1. Contact SNHU institutional repository
2. Provide ORCID for attribution
3. Link published capstone project
4. Enable automatic updates
```

---

## Quality Control Checklist

After registration, verify:

- [ ] Email verified and account activated
- [ ] Profile photo added (professional headshot)
- [ ] Biography completed with research focus
- [ ] Keywords added (5-10 relevant terms)
- [ ] Strategickhaos DAO LLC employment added
- [ ] SNHU education added
- [ ] Visibility settings configured
- [ ] Email preferences set (monthly digest recommended)
- [ ] Trusted organizations configured
- [ ] Mobile app downloaded (optional)

---

## Maintenance and Updates

### Regular Tasks (Quarterly)

1. **Update Publications:**
   - Add new papers, patents, pre-prints
   - Update citation counts
   - Verify metadata accuracy

2. **Update Affiliations:**
   - Add new positions or roles
   - Update current organization details
   - Archive past positions

3. **Review Connections:**
   - Accept institution verification requests
   - Link new collaborator ORCIDs
   - Update trusted organization list

4. **Privacy Audit:**
   - Review what's public vs. private
   - Update email addresses
   - Verify auto-update settings

---

## ORCID in Citations

### How to Reference Your ORCID

**In Papers:**
```latex
\author{
    Domenic Garza\\
    \textit{Strategickhaos DAO LLC}\\
    ORCID: 0000-0003-XXXX-XXXX
}
```

**In Email Signatures:**
```
Domenic Garza
Founder & Principal Researcher
Strategickhaos DAO LLC / Valoryield Engine
ORCID: https://orcid.org/0000-0003-XXXX-XXXX
```

**On Business Cards:**
```
Domenic Garza
ORCID: 0000-0003-XXXX-XXXX
```

---

## Troubleshooting

### Common Issues

**Problem:** Email verification not received
```
Solution:
1. Check spam/junk folder
2. Request resend from account settings
3. Try alternative email address
4. Contact ORCID support if persistent
```

**Problem:** Cannot link DOI from Zenodo
```
Solution:
1. Wait 24-48 hours after Zenodo upload for indexing
2. Use manual "Add Work" instead of auto-search
3. Verify DOI is active at doi.org
4. Contact ORCID support with DOI details
```

**Problem:** Institutional affiliation not found
```
Solution:
1. Search by alternate names (acronyms, full names)
2. Use "Add manually" if not in database
3. Contact institution to register with ORCID
4. Request ORCID add organization to registry
```

---

## Advanced Features

### ORCID API Integration

For automated updates from your research infrastructure:

```python
# Example: Auto-update ORCID from GitHub releases
import requests

ORCID_API = "https://pub.orcid.org/v3.0"
ORCID_ID = "0000-0003-XXXX-XXXX"

# Requires authentication token from ORCID
# See: https://info.orcid.org/documentation/api-tutorials/
```

### Trusted Organizations

Configure automatic updates from:
- Your university (SNHU)
- Publisher platforms (arXiv, IEEE, ACM)
- Grant agencies (NSF, NIH)
- Patent offices (USPTO)

---

## Documentation and Support

**Official Resources:**
- ORCID Homepage: https://orcid.org
- Knowledge Base: https://support.orcid.org
- API Documentation: https://info.orcid.org/documentation/
- Status Page: https://status.orcid.org

**Support Channels:**
- Email: support@orcid.org
- Twitter: @ORCID_Org
- Community Forum: https://groups.google.com/g/orcid-api-users

---

## Post-Registration Actions

Once your ORCID is active:

1. **Update All Profiles:**
   - GitHub README
   - LinkedIn
   - Academic CVs
   - University profiles
   - Email signatures

2. **Share with Collaborators:**
   - Co-authors on papers
   - Grant co-investigators
   - Institutional administrators

3. **Enable Auto-Updates:**
   - Connect to university systems
   - Link to publisher accounts
   - Configure API integrations

4. **Regular Maintenance:**
   - Review quarterly
   - Update after each publication
   - Verify citation accuracy

---

## Final Checklist

- [ ] ORCID registered: `0000-0003-XXXX-XXXX`
- [ ] Profile completed with bio and keywords
- [ ] Strategickhaos DAO LLC employment added
- [ ] SNHU education added
- [ ] Pre-print linked (after Zenodo upload)
- [ ] USPTO provisional patents added
- [ ] GitHub repository linked
- [ ] Email signature updated with ORCID
- [ ] LaTeX paper updated with ORCID
- [ ] Google Scholar profile linked
- [ ] Visibility settings configured
- [ ] Profile photo uploaded

---

**Status:** READY FOR REGISTRATION  
**Estimated Time:** 5-10 minutes (60 seconds for basic registration + profile setup)  
**Cost:** FREE (ORCID registration is free)  
**Last Updated:** 2025-11-23

---

**Next Steps:**
1. Register at https://orcid.org/register
2. Complete profile with employment and education
3. Update all academic materials with ORCID
4. Link works as they are published
5. Add ORCID to email signature and CVs

**Your ORCID will be:** `0000-0003-XXXX-XXXX` (revealed after registration)
