# Zenodo DOI Setup Guide

## What is Zenodo?

**Zenodo** is a free, open-access repository hosted by CERN that provides:
- **Persistent DOIs** (Digital Object Identifiers) for research outputs
- **Long-term preservation** of digital artifacts
- **Citeable references** for code, data, and pre-prints
- **Version control** for iterative releases
- **Integration** with GitHub and ORCID

**Your DOI Format:** `10.5281/zenodo.XXXXXXX`

---

## Why Use Zenodo?

### Benefits for Sovereignty Architecture

1. **Instant Academic Credibility**
   - DOI makes your work officially citable
   - Recognized by Google Scholar, ResearchGate, etc.
   - Professional presentation of research

2. **Permanent Archive**
   - CERN-backed infrastructure
   - Guaranteed 20+ year preservation
   - Survives even if GitHub disappears

3. **Version Management**
   - Track iterations of your work
   - Each version gets its own DOI
   - Concept DOI links all versions

4. **Legal Protection**
   - Timestamped publication record
   - Establishes prior art for patents
   - Immutable proof of authorship

5. **Integration**
   - Direct GitHub repository archiving
   - ORCID automatic linking
   - Google Scholar indexing

---

## Quick Upload (5 Minutes)

### Step 1: Create Zenodo Account

```
1. Navigate to: https://zenodo.org
2. Click "Sign Up" (top right)
3. Choose authentication method:
   - GitHub (recommended for easy integration)
   - ORCID (links directly to academic profile)
   - Email (traditional registration)
4. Complete authentication
5. Verify email if needed
```

### Step 2: Create New Upload

```
1. Log in to Zenodo
2. Click "Upload" button (top menu)
3. Click "New upload"
4. You'll see the upload form
```

### Step 3: Upload Files

**Option A: Manual Upload**
```
1. Drag and drop files into upload area
2. Or click "Choose files" to browse

Recommended files for Sovereignty Architecture:
- sovereignty-architecture-preprint.pdf (compiled LaTeX)
- 100_LAWS_OF_THE_SOVEREIGN_TINKERER.md
- README.md (project overview)
- LICENSE (CC BY 4.0)
- Optional: Source code archive (if not using GitHub integration)
```

**Option B: GitHub Integration (Recommended)**
```
1. Go to: https://zenodo.org/account/settings/github/
2. Click "Connect" next to GitHub
3. Authorize Zenodo to access repositories
4. Toggle ON for: Sovereignty-Architecture-Elevator-Pitch-
5. Create a release on GitHub
6. Zenodo automatically creates DOI from release
```

---

## Complete Metadata Form

### Basic Information (Required)

**Upload Type:**
- Select: `Publication` → `Pre-print`
- Alternative: `Software` (if focusing on code)

**Publication Date:**
```
2025-11-23
```

**Title:**
```
Sovereignty Architecture: A Framework for Negative-Balance Computing and Neurodivergent Swarm Intelligence
```

**Authors:**
```
Name: Domenic Garza
Affiliation: Strategickhaos DAO LLC / Valoryield Engine
ORCID: 0000-0003-XXXX-XXXX (if registered)
```

**Description:**
```
This pre-print presents Sovereignty Architecture, a novel computational framework 
leveraging resource constraints and neurodivergent cognitive patterns as 
computational primitives. Key innovations include Negative-Balance Computing 
and Neurodivergent Swarm Intelligence. Implementation demonstrates practical 
sovereignty through Wyoming DAO LLC formation, USPTO provisional patents, 
and autonomous swarm operations built from negative financial balance and 
thermal-limited hardware.

Includes:
- Complete research paper (LaTeX source and PDF)
- 100 Laws of the Sovereign Tinkerer (prior art documentation)
- Implementation code and architecture
- Legal compliance framework
- Patent provisional references

Entity: Strategickhaos DAO LLC (Wyoming 2025-001708194, EIN: 39-2923503)
```

**Version:**
```
1.0.0 (or use semantic versioning)
```

### Additional Information

**Keywords (10-15 recommended):**
```
- Negative-Balance Computing
- Neurodivergent Computing
- Swarm Intelligence
- Distributed Systems
- Resource-Constrained Computing
- Computational Sovereignty
- DAO Architecture
- Autonomous Agents
- Pattern Recognition
- Constitutional AI
- Wyoming LLC
- USPTO Patents
- Prior Art
- Academic Pre-print
```

**License:**
```
Select: Creative Commons Attribution 4.0 International (CC BY 4.0)

Reason: Allows maximum reuse while requiring attribution
```

**Communities (Optional but Recommended):**
```
Search and join relevant communities:
- Computer Science
- Artificial Intelligence
- Distributed Systems
- Open Source
- Neurodiversity Research
```

### Related Identifiers

Link to related resources:

**GitHub Repository:**
```
Relation: Is supplemented by
Identifier: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
Resource Type: Software
```

**USPTO Provisional Patents (after filing):**
```
Relation: Is documented by
Identifier: USPTO Application XXXXXXXX (Negative-Balance Computing)
Resource Type: Patent

Relation: Is documented by
Identifier: USPTO Application XXXXXXXX (Neurodivergent Swarm)
Resource Type: Patent
```

**Compliance Vault:**
```
Relation: Is supplemented by
Identifier: https://github.com/Me10101-01/Strategickhaos-DAO_Compliance
Resource Type: Dataset
```

### Contributors

**Additional Contributors (if any):**
```
Name: (Co-authors, if applicable)
Type: (Researcher, Data Collector, etc.)
Affiliation: (Organization)
ORCID: (Their ORCID)
```

### Funding (Optional)

```
Grant Title: Self-Funded (Negative-Balance Computing Proof-of-Concept)
Funder: Strategickhaos DAO LLC
Grant Number: N/A
```

### References (Optional but Recommended)

```
Add key papers cited in your work:
- Vaswani et al. (2017) - Attention is All You Need
- Brown et al. (2020) - GPT-3
- Lewis et al. (2020) - RAG
- Bai et al. (2022) - Constitutional AI
- Wyoming SF0068 (2022) - DAO Legislation
```

---

## Review and Publish

### Pre-Publication Checklist

- [ ] All files uploaded successfully
- [ ] Title is clear and descriptive
- [ ] Authors with ORCID linked
- [ ] Description is comprehensive
- [ ] Keywords include all relevant terms
- [ ] License is CC BY 4.0
- [ ] Related identifiers added (GitHub, patents)
- [ ] Publication date is correct
- [ ] Upload type is "Pre-print"
- [ ] Files are final versions (publishing is permanent)

### Publish

```
1. Click "Preview" to see how it will look
2. Review all information carefully
3. Click "Publish" button
4. Confirm publication (this cannot be undone)
5. Wait for DOI assignment (immediate)
```

### Post-Publication

**Immediately after publishing:**
```
1. Copy your DOI: 10.5281/zenodo.XXXXXXX
2. Save DOI URL: https://doi.org/10.5281/zenodo.XXXXXXX
3. Test DOI link (should resolve to Zenodo page)
4. Screenshot Zenodo page for records
```

---

## Using Your DOI

### In Academic Papers

**LaTeX Citation:**
```latex
\bibitem{sovereignty2025}
Garza, D. (2025). Sovereignty Architecture: A Framework for Negative-Balance 
Computing and Neurodivergent Swarm Intelligence. 
Zenodo. \url{https://doi.org/10.5281/zenodo.XXXXXXX}
```

**In Text:**
```latex
Our implementation \cite{sovereignty2025} demonstrates...
```

### In README Files

**Markdown Badge:**
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)]
(https://doi.org/10.5281/zenodo.XXXXXXX)
```

**Citation Section:**
```markdown
## Citation

If you use this work, please cite:

Garza, D. (2025). Sovereignty Architecture: A Framework for Negative-Balance 
Computing and Neurodivergent Swarm Intelligence. 
Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

### In ORCID Profile

```
1. Log in to ORCID
2. Go to "Works" section
3. Click "Add Works"
4. Choose "Search & Link" → "Zenodo"
5. Authorize Zenodo connection
6. Select your upload
7. Import to ORCID profile
```

### On Social Media

**Twitter/X Post Template:**
```
🚀 Just published: "Sovereignty Architecture" pre-print

Novel framework for Negative-Balance Computing + Neurodivergent Swarm Intelligence

From $-32.67 to federally-protected empire 🏛️

📄 DOI: https://doi.org/10.5281/zenodo.XXXXXXX
🔗 GitHub: https://github.com/Strategickhaos/...
⚖️ USPTO provisionals filed
🎓 ORCID: 0000-0003-XXXX-XXXX

#OpenScience #ComputerScience #Neurodiversity
```

---

## GitHub Integration (Advanced)

### Automatic DOI on Release

**One-Time Setup:**
```
1. Go to: https://zenodo.org/account/settings/github/
2. Connect your GitHub account
3. Enable Zenodo for your repository
4. Toggle ON for: Sovereignty-Architecture-Elevator-Pitch-
```

**Create a Release:**
```bash
# Tag your code
git tag -a v1.0.0 -m "First public release with DOI"
git push origin v1.0.0

# Or use GitHub web interface:
1. Go to repository "Releases" tab
2. Click "Draft a new release"
3. Choose tag: v1.0.0
4. Release title: "Sovereignty Architecture v1.0.0"
5. Description: (Release notes)
6. Publish release

# Zenodo automatically:
- Archives the release
- Assigns DOI
- Links to GitHub
- Updates ORCID (if configured)
```

**Concept DOI vs Version DOI:**
```
Concept DOI: 10.5281/zenodo.1234567  (points to latest version)
Version DOI: 10.5281/zenodo.1234568  (points to specific v1.0.0)

Always cite specific version DOI for reproducibility
```

---

## Version Management

### Uploading New Versions

When updating your pre-print:

```
1. Go to your Zenodo upload page
2. Click "New version" button
3. Upload updated files
4. Update metadata (version number, date, description)
5. Publish new version
6. New DOI assigned to new version
7. Concept DOI always points to latest
```

**Version Numbering:**
```
v1.0.0 - Initial pre-print
v1.1.0 - Minor updates (typos, formatting)
v2.0.0 - Major revisions (new content, experiments)
v3.0.0 - Peer-reviewed published version
```

---

## Maximizing Impact

### Google Scholar Indexing

Zenodo uploads are automatically indexed by Google Scholar:
```
1. Wait 24-48 hours after publication
2. Search for your paper on Google Scholar
3. Claim it in your Scholar profile
4. Citations will be tracked automatically
```

### ResearchGate

```
1. Log in to ResearchGate
2. Add publication manually or import via DOI
3. Share with followers
4. Track reads and citations
```

### Academic Social Networks

Share on:
- Academia.edu
- ResearchGate  
- Mendeley
- Twitter/X (academic community)
- LinkedIn (professional network)

### Press Release

Consider writing a brief press release:
```
"Strategickhaos DAO LLC Publishes Groundbreaking Research on 
Negative-Balance Computing and Neurodivergent Swarm Intelligence"

Include:
- Research highlights
- Practical applications
- DOI for full paper
- Contact information
```

---

## Troubleshooting

### Common Issues

**Problem:** Files won't upload
```
Solution:
- Check file size limits (50 GB per file)
- Verify file format is supported
- Try compressing large files
- Use GitHub integration for code repositories
```

**Problem:** DOI not resolving
```
Solution:
- Wait 5-10 minutes after publication for indexing
- Clear browser cache
- Try different browser
- Contact Zenodo support if persistent
```

**Problem:** Can't link to ORCID
```
Solution:
- Ensure ORCID is registered first
- Connect ORCID account in Zenodo settings
- Use correct ORCID format (0000-0003-XXXX-XXXX)
- Wait 24 hours for sync
```

---

## Post-Publication Actions

### Within 24 Hours

- [ ] Copy and save DOI (10.5281/zenodo.XXXXXXX)
- [ ] Update GitHub README with DOI badge
- [ ] Add citation to repository
- [ ] Update LaTeX paper with DOI
- [ ] Link DOI in ORCID profile
- [ ] Post announcement on X/Twitter
- [ ] Share on LinkedIn
- [ ] Email to key collaborators
- [ ] Update USPTO provisionals with DOI reference

### Within 1 Week

- [ ] Verify Google Scholar indexing
- [ ] Add to ResearchGate profile
- [ ] Update academic CV with DOI
- [ ] Add to institution repository (SNHU)
- [ ] Share in relevant communities
- [ ] Monitor citation tracking
- [ ] Consider submitting to conferences

---

## Cost and Limits

**Free Forever:**
- Zenodo is free for all users
- No storage limits for reasonably-sized uploads
- Unlimited DOIs
- No publication fees
- No access restrictions

**Technical Limits:**
- 50 GB per file
- Unlimited number of files per upload
- 2 GB GitHub integration file limit (larger requires manual)

---

## Support and Resources

**Official Resources:**
- Zenodo Homepage: https://zenodo.org
- Help Documentation: https://help.zenodo.org
- API Documentation: https://developers.zenodo.org
- Community Forum: https://github.com/zenodo/zenodo/discussions

**Support Channels:**
- Email: support@zenodo.org
- Twitter: @ZENODO_ORG
- GitHub Issues: https://github.com/zenodo/zenodo/issues

---

## Final Checklist

- [ ] Zenodo account created
- [ ] LaTeX PDF compiled and uploaded
- [ ] 100 Laws document included
- [ ] Complete metadata entered
- [ ] All authors with ORCID listed
- [ ] Keywords optimized for discovery
- [ ] License set to CC BY 4.0
- [ ] GitHub repository linked
- [ ] USPTO patents referenced (after filing)
- [ ] Publication reviewed and published
- [ ] DOI obtained and saved: 10.5281/zenodo.XXXXXXX
- [ ] GitHub README updated with DOI badge
- [ ] ORCID profile updated with DOI
- [ ] X/Twitter announcement posted
- [ ] Google Scholar indexing verified

---

**Status:** READY FOR UPLOAD  
**Estimated Time:** 5-15 minutes (5 minutes for basic upload + metadata completion)  
**Cost:** FREE  
**Last Updated:** 2025-11-23

---

**Next Steps:**
1. Compile LaTeX to PDF
2. Create Zenodo account
3. Upload pre-print and supporting materials
4. Complete metadata form
5. Publish and obtain DOI
6. Update all references with DOI
7. Monitor indexing and citations

**Your DOI will be:** `10.5281/zenodo.XXXXXXX` (revealed after publication)
