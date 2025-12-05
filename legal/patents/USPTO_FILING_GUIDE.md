# USPTO Provisional Patent Filing Guide

## Overview

This guide provides step-by-step instructions for filing a provisional patent application with the United States Patent and Trademark Office (USPTO) for the Strategickhaos DAO's "Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification."

## Why File a Provisional Patent?

- **Priority Date**: Establishes your invention date legally
- **Patent Pending Status**: Allows you to mark products/services as "Patent Pending"
- **12-Month Window**: Gives you time to develop and test before filing a full utility patent
- **Cost-Effective**: Significantly cheaper than a full utility patent application
- **Micro-Entity Discount**: 75% off filing fees if you qualify

## Eligibility: Micro-Entity Status

### Qualifications for Micro-Entity

You qualify for micro-entity status if ALL of the following are true:

1. **Income Threshold**: Your gross income is less than 3x the U.S. median household income (approximately $218,000 for 2024; check current USPTO guidelines)
2. **Prior Applications**: You have filed fewer than 5 prior patent applications
3. **Assignment Rights**: You have not assigned or licensed the patent to an entity that exceeds the income threshold

**Note**: The income threshold is adjusted annually by the USPTO. Always verify the current threshold at https://www.uspto.gov/patents/laws/micro-entity-status before filing.

### Filing Fee Comparison

- **Micro-Entity**: $75 (75% discount)
- **Small Entity**: $150 (50% discount)
- **Large Entity**: $300 (standard rate)

## Step-by-Step Filing Process

### Step 0: Obtain Micro-Entity Certification (One-Time)

1. **Download the SB/15A form**:
   - URL: https://www.uspto.gov/sites/default/files/documents/sb0015a.pdf
   - Or use the automated script provided in this repository

2. **Fill out the form**:
   - Enter your full legal name
   - Sign and date the form
   - Save as: `MICRO_ENTITY_CERT.pdf`

3. **Keep the original**: You'll upload this during the USPTO filing process

### Step 1: Prepare Your Provisional Application Document

Your provisional application should include:

1. **Title**: Clear and descriptive
   - Example: "Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification"

2. **Technical Description**: Detailed explanation of your invention
   - What it does
   - How it works
   - Technical architecture
   - Novel features

3. **Figures/Diagrams** (if applicable):
   - System architecture diagrams
   - Flowcharts
   - Screenshots

4. **Best Mode**: Your preferred implementation method

#### Format Requirements

- **Paper Size**: US Letter (8.5" x 11")
- **Margins**: Minimum 1 inch on all sides
- **Font**: 12-point or larger, non-script font
- **Line Spacing**: 1.5 or double spacing
- **Page Numbers**: Number all pages
- **File Format**: PDF only for electronic filing

#### Converting Markdown to PDF

**Using Pandoc (Recommended)**:
```bash
pandoc provisional_application.md -o PROVISIONAL_APPLICATION.pdf --pdf-engine=weasyprint
```

**Using Word/Google Docs**:
1. Copy your markdown content to Word or Google Docs
2. Format appropriately (1-inch margins, readable font)
3. Export as PDF (US Letter size)

### Step 2: File via USPTO EFS-Web (Electronic Filing System)

1. **Navigate to EFS-Web**:
   - URL: https://efs.uspto.gov/EFS-Web2/
   - Available 24/7
   - Create account if you don't have one

2. **Login and Start New Application**:
   - Click "New Application"
   - Select "Provisional Application"

3. **Upload Micro-Entity Certification**:
   - Select "Micro Entity (SB/15A)"
   - Upload your `MICRO_ENTITY_CERT.pdf`

4. **Enter Application Data**:
   - **Inventor Name**: Your full legal name as it appears on official documents
   - **Inventor Address**: Your Wyoming DAO address or personal address
   - **Correspondence Address**: Where USPTO should send notices
   - **Title**: "Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification"

5. **Upload Your Provisional Application PDF**:
   - Upload your prepared PDF document
   - The system will validate the PDF format

6. **Validate Submission**:
   - Review all entered information
   - Check for any errors or warnings
   - Make corrections if needed

7. **Pay Filing Fee**:
   - Fee: $75 (micro-entity)
   - Payment methods: Credit card or USPTO deposit account
   - Transaction is secure and immediate

8. **Submit Application**:
   - Click "Submit"
   - Save your confirmation page
   - You will receive an email confirmation

### Step 3: Receive Official Filing Receipt

**Timing**: 5-15 minutes to several hours after submission

**What You'll Receive**:
- **Application Number**: Format `63/XXXXXX` (63 prefix indicates provisional)
- **Filing Date**: Official date of filing (establishes priority)
- **Official Filing Receipt**: PDF document sent to your email

**Save Everything**:
- Application number
- Filing receipt PDF
- Confirmation email
- All uploaded documents

### Step 4: Establish Proof Chain (Cryptographic Verification)

After receiving your filing receipt, establish an immutable proof chain:

1. **Add Files to Git Repository**:
   ```bash
   git add legal/patents/provisional/STRATEGICKHAOS_PROVISIONAL_2025-11-22.pdf
   git add legal/patents/receipts/USPTO_Receipt.pdf
   git add legal/patents/receipts/MICRO_ENTITY_CERT.pdf
   ```

2. **Commit with GPG Signature**:
   ```bash
   git commit -S -m "PATENT PENDING: Provisional 63/XXXXXX filed 2025-11-22 – micro-entity"
   ```

3. **Push to Repository**:
   ```bash
   git push
   ```

4. **Create OpenTimestamps** (Bitcoin blockchain proof):
   ```bash
   ots stamp legal/patents/provisional/STRATEGICKHAOS_PROVISIONAL_2025-11-22.pdf
   ots stamp legal/patents/receipts/USPTO_Receipt.pdf
   ```

5. **Optional: Archive on Arweave** (permanent storage):
   - Upload to Arweave for permanent, decentralized storage
   - Save transaction ID

## After Filing: Using "Patent Pending" Status

### Legal Usage

Once you receive your filing receipt, you can legally state:

> **Strategickhaos DAO LLC – Patent Pending (U.S. Provisional Application 63/XXXXXX)**

### Where to Use It

- Website footer
- Product documentation
- Marketing materials
- Investor presentations
- GitHub repository README
- Business cards
- Contracts and agreements

### Duration

- **Patent Pending Status**: Valid for 12 months from filing date
- **Action Required**: File a full utility patent application within 12 months to maintain priority date
- **If No Action**: Provisional expires after 12 months and becomes abandoned

## Timeline for Full Patent

After filing your provisional:

| Month | Action |
|-------|--------|
| 0 | File provisional - Patent Pending begins |
| 1-6 | Develop product, gather user feedback, refine implementation |
| 6-9 | Begin drafting full utility patent application with attorney |
| 10-11 | File full utility patent (non-provisional) to claim priority |
| 12 | **DEADLINE**: Must file full patent or provisional expires |
| 18-36 | USPTO examination process begins |
| 24-48 | Potential patent grant (if approved) |

## Cost Summary

### Provisional Patent (Today)
- **Filing Fee (Micro-Entity)**: $75
- **Total Cost**: $75

### Full Utility Patent (Within 12 Months)
- **Filing Fee (Micro-Entity)**: ~$300
- **Search Fee**: ~$180
- **Examination Fee**: ~$200
- **Patent Attorney** (optional but recommended): $3,000-$10,000
- **Total Estimated**: $3,680-$10,680

## Important Dates to Track

1. **Filing Date**: [Date you filed]
2. **12-Month Deadline**: [Filing date + 12 months]
3. **Priority Date**: Same as filing date
4. **Expiration Date**: [Filing date + 12 months] if no utility patent filed

## Resources

### USPTO Resources
- **EFS-Web**: https://efs.uspto.gov/EFS-Web2/
- **Micro-Entity Form (SB/15A)**: https://www.uspto.gov/sites/default/files/documents/sb0015a.pdf
- **Provisional Patent Guide**: https://www.uspto.gov/patents/basics/types-patent-applications/provisional-application-patent
- **Patent Application Guide**: https://www.uspto.gov/patents/basics/apply

### Tools
- **Pandoc**: https://pandoc.org/ (Markdown to PDF conversion)
- **OpenTimestamps**: https://opentimestamps.org/ (Blockchain proof)
- **GPG**: https://gnupg.org/ (Cryptographic signatures)

### Support
- **USPTO Contact Center**: 1-800-786-9199 (Monday-Friday, 8:30 AM - 8:00 PM ET)
- **Patent Trial and Appeal Board**: https://www.uspto.gov/patents/ptab

## Legal Disclaimers

**This guide is for informational purposes only and does not constitute legal advice. Consider consulting with a licensed patent attorney for:**
- Prior art searches
- Patentability assessments
- Claim drafting
- Full utility patent preparation
- International patent protection (PCT)
- Patent prosecution and defense

## Security & Confidentiality

### Before Filing
- **Keep confidential**: Do not publicly disclose your invention before filing
- **Non-disclosure agreements**: Use NDAs when discussing with potential partners
- **Private repositories**: Keep development private until filing

### After Filing
- **Public disclosure allowed**: You can publicly disclose after filing
- **Patent Pending**: Use this status to warn potential copiers
- **Document everything**: Keep records of development, prior art searches, and communications

## Three-Axis Protection

Your invention is now protected on three levels:

1. **Legal Protection**: Wyoming DAO LLC + irrevocable charity structure
2. **Cryptographic Protection**: GPG signatures + OpenTimestamps + Arweave
3. **Intellectual Property Protection**: Patent Pending status with USPTO priority date

## Next Steps After Filing

1. **Mark your filing date on calendar**
2. **Set reminder for 10-month mark** (time to prepare utility patent)
3. **Begin using "Patent Pending" in materials**
4. **Continue developing and testing your system**
5. **Document all improvements and iterations**
6. **Consider international protection** (PCT application if needed)
7. **Schedule provisional filings for additional inventions**

## Questions?

For assistance with this repository's patent filing process, please open an issue or contact the repository maintainers.

---

**Last Updated**: November 22, 2025  
**Status**: Active Guide  
**Version**: 1.0
