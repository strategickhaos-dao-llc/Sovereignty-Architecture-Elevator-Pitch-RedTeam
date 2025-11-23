# Patent Filing Resources

This directory contains resources, scripts, and documentation for filing and managing provisional patent applications with the United States Patent and Trademark Office (USPTO).

## Quick Start

### For First-Time Filers

1. **Read the comprehensive guide**: [USPTO_FILING_GUIDE.md](USPTO_FILING_GUIDE.md)
2. **Run the filing preparation script**:
   - **Windows**: `.\file-provisional-patent.ps1`
   - **Linux/Mac**: `./file-provisional-patent.sh`
3. **Complete your provisional application document**
4. **File via USPTO EFS-Web** (the script will guide you)
5. **After receiving your filing receipt, run**: 
   - **Windows**: `.\create-proof-chain.ps1 -ApplicationNumber "63/XXXXXX"`
   - **Linux/Mac**: `./create-proof-chain.sh 63/XXXXXX`

## Directory Structure

```
legal/patents/
├── README.md                       # This file
├── USPTO_FILING_GUIDE.md          # Comprehensive filing guide
├── file-provisional-patent.sh     # Bash automation script
├── file-provisional-patent.ps1    # PowerShell automation script
├── create-proof-chain.sh          # Bash proof chain script
├── create-proof-chain.ps1         # PowerShell proof chain script
├── PATENT_TRACKING.md             # Patent tracking document (created after filing)
├── provisional/                   # Provisional patent applications
│   ├── PROVISIONAL_PATENT_APPLICATION.md
│   └── STRATEGICKHAOS_PROVISIONAL_2025-11-22.pdf
├── receipts/                      # USPTO receipts and certificates
│   ├── USPTO_Receipt.pdf
│   └── MICRO_ENTITY_CERT.pdf
└── templates/                     # Document templates
    └── provisional_template.md
```

## What Each Script Does

### `file-provisional-patent.sh` / `.ps1`

**Purpose**: Automates the preparation steps for filing a provisional patent application.

**What it does**:
- Creates necessary directories
- Downloads the micro-entity certification form (SB/15A)
- Creates a template provisional application document
- Converts markdown to USPTO-ready PDF (if pandoc is available)
- Opens the USPTO EFS-Web portal
- Provides step-by-step filing instructions

**What it does NOT do**:
- Does not submit the application to USPTO (you do this manually via EFS-Web)
- Does not store your USPTO credentials
- Does not make any modifications to your application without your approval

### `create-proof-chain.sh` / `.ps1`

**Purpose**: Establishes an immutable cryptographic proof chain after you receive your USPTO filing receipt.

**What it does**:
- Verifies all required patent documents are present
- Stages patent documents in Git
- Creates a GPG-signed commit (if GPG is configured)
- Pushes to remote repository
- Creates OpenTimestamps (Bitcoin blockchain proof)
- Generates a patent tracking document

**Why this matters**:
- Provides independent proof of filing date
- Creates a verifiable, tamper-proof record
- Establishes cryptographic proof of existence
- Creates a backup of all patent documents

## File Sizes and Costs

### Micro-Entity Filing

- **Provisional Patent Fee**: $75 (75% discount)
- **Qualifications**: Income < $45k/year, < 5 prior applications, no assignment to large entity

### File Size Limits (USPTO EFS-Web)

- **Maximum file size**: 100 MB per file
- **Recommended**: Keep under 20 MB for faster processing
- **Format**: PDF only for electronic filing

## Security & Best Practices

### Before Filing

1. **Keep your invention confidential** until you file
2. **Use NDAs** when discussing with potential partners or investors
3. **Document everything**: Keep dated records of development
4. **Search prior art**: Review existing patents to ensure novelty

### After Filing

1. **Use "Patent Pending"** in all materials immediately
2. **Continue documenting** improvements and iterations
3. **Set calendar reminders**:
   - 10 months: Begin utility patent preparation
   - 11 months: File utility patent to maintain priority
4. **Maintain records** of all development work

### Cryptographic Proof Chain

The proof chain establishes three levels of verification:

1. **Git Commit**: Version-controlled record with timestamp
2. **GPG Signature**: Cryptographic signature proving authorship
3. **OpenTimestamps**: Bitcoin blockchain proof of existence

This creates an independent, verifiable record that supplements your USPTO filing.

## Common Questions

### Do I need a patent attorney?

**For provisional patents**: Not required. You can file yourself.
**For utility patents**: Highly recommended. Patent prosecution is complex and mistakes can be costly.

### What if I miss the 12-month deadline?

Your provisional application will expire and you'll lose your priority date. You cannot extend this deadline.

### Can I file multiple provisional patents?

Yes! You can file as many as you want. Consider filing provisionals for:
- Different aspects of your system
- Improvements and iterations
- Related inventions

### What's the difference between provisional and utility patents?

| Feature | Provisional | Utility (Non-Provisional) |
|---------|------------|---------------------------|
| Cost | $75 (micro) | ~$680+ (micro) |
| Examination | No | Yes |
| Duration | 12 months | 20 years from filing |
| Patent Rights | None | Full patent protection |
| Purpose | Establish priority | Obtain patent rights |

### How long does the filing process take?

- **Preparation**: 1-4 hours (first time)
- **Online filing**: 15-45 minutes
- **Receipt**: 5 minutes to several hours
- **Total**: Can be done in one day

### What happens after I file?

1. **Immediately**: You can use "Patent Pending"
2. **5-15 minutes**: You receive a filing receipt with application number
3. **12 months**: You must file a utility patent or your provisional expires
4. **18-36 months**: USPTO examines your utility patent (if filed)
5. **24-48 months**: Potential patent grant (if approved)

## Resources

### USPTO Resources

- **EFS-Web**: https://efs.uspto.gov/EFS-Web2/
- **Patent Center**: https://patentcenter.uspto.gov/
- **Micro-Entity Form**: https://www.uspto.gov/sites/default/files/documents/sb0015a.pdf
- **Patent Search**: https://patft.uspto.gov/
- **Patent Examination Guides**: https://www.uspto.gov/patents/laws

### Tools

- **Pandoc** (Markdown to PDF): https://pandoc.org/
- **OpenTimestamps**: https://opentimestamps.org/
- **GPG/GnuPG**: https://gnupg.org/
- **Git**: https://git-scm.com/

### Legal Support

- **USPTO Contact Center**: 1-800-786-9199
- **Pro Bono Programs**: https://www.uspto.gov/patents/basics/using-legal-services/pro-bono
- **Patent Attorney Directory**: https://www.uspto.gov/learning-and-resources/patent-and-trademark-practitioners

## Troubleshooting

### Script won't run (Bash)

```bash
# Make sure the script is executable
chmod +x file-provisional-patent.sh
chmod +x create-proof-chain.sh

# Run with bash explicitly
bash file-provisional-patent.sh
```

### Script won't run (PowerShell)

```powershell
# Enable script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run the script
.\file-provisional-patent.ps1
```

### Pandoc not found

**Install Pandoc**:
- **Windows**: Download from https://pandoc.org/installing.html
- **Mac**: `brew install pandoc`
- **Linux**: `sudo apt-get install pandoc` or `sudo yum install pandoc`

**Alternative**: Use Word or Google Docs to convert markdown to PDF manually.

### OpenTimestamps not found

**Install OpenTimestamps**:
```bash
# Using pip
pip install opentimestamps-client

# Or download binary from:
# https://github.com/opentimestamps/opentimestamps-client
```

### GPG not configured

**Setup GPG signing**:
```bash
# Generate a key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Configure git
git config --global user.signingkey [KEY_ID]
git config --global commit.gpgsign true
```

## Support

For questions or issues with these scripts:
1. Review the [USPTO_FILING_GUIDE.md](USPTO_FILING_GUIDE.md)
2. Check the troubleshooting section above
3. Open an issue in this repository
4. Contact USPTO at 1-800-786-9199 for official filing questions

## Legal Disclaimer

**These scripts and guides are provided for informational purposes only and do not constitute legal advice.** 

- The scripts automate preparation only; you are responsible for filing
- Review all documents before submitting to USPTO
- Consider consulting a licensed patent attorney for complex inventions
- The USPTO has final authority on all patent matters

## Version History

- **v1.0** (2025-11-22): Initial release
  - Comprehensive USPTO filing guide
  - Automated filing preparation scripts
  - Cryptographic proof chain establishment
  - Patent tracking documentation

---

**Last Updated**: November 22, 2025  
**Maintained by**: Strategickhaos DAO LLC  
**License**: MIT (scripts), Proprietary (patent applications)
