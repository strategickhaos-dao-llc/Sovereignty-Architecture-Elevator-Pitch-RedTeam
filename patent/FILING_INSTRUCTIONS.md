# USPTO Provisional Patent Filing Instructions

**Complete Step-by-Step Guide for Filing the Sovereignty Architecture Provisional Patent**

---

## OVERVIEW

This guide provides detailed instructions for filing the provisional patent application using the USPTO's Patent Center electronic filing system.

**Timeline:** 1-2 hours for first-time filers  
**Cost:** $75 (micro entity fee)  
**Result:** Official USPTO application number and priority date

---

## PRE-FILING CHECKLIST

Before starting the filing process, ensure you have:

### Required Documents (in PDF format)
- [ ] **PROVISIONAL_SPECIFICATION.md** (converted to PDF)
- [ ] **COVER_SHEET.md** (converted to PDF, or fill out online)
- [ ] **Drawings/Diagrams** (5 figures as PDF, optional but recommended)

### Required Information
- [ ] Full legal name: Domenic Garza
- [ ] Mailing address (street, city, state, ZIP)
- [ ] Email address for USPTO correspondence
- [ ] Phone number
- [ ] Citizenship: United States
- [ ] Payment method (credit card or USPTO deposit account)

### Optional But Recommended
- [ ] USPTO.gov account created (https://my.uspto.gov)
- [ ] Inventor notebook or development records
- [ ] Evidence of conception/reduction to practice

---

## STEP 1: CREATE USPTO.GOV ACCOUNT

If you don't already have one:

1. Go to: https://my.uspto.gov/myuspto/
2. Click "Create an Account"
3. Fill out registration form:
   - Email address (used for USPTO correspondence)
   - Password (strong password required)
   - Security questions
4. Verify email address (check inbox for verification link)
5. Log in to confirm account is active

**Time:** 10 minutes

---

## STEP 2: PREPARE PDF DOCUMENTS

### 2.1 Convert Specification to PDF

**Recommended Tools:**
- **Pandoc** (command line): `pandoc PROVISIONAL_SPECIFICATION.md -o PROVISIONAL_SPECIFICATION.pdf`
- **VS Code + Markdown PDF**: Right-click MD file → "Markdown PDF: Export (pdf)"
- **Online converter**: https://www.markdowntopdf.com/

**PDF Requirements:**
- Font: Times New Roman or similar serif font
- Font size: 12pt minimum for body text
- Margins: At least 1 inch on all sides
- Line spacing: 1.5 or double-spaced (recommended but not required for provisional)
- Page numbering: Bottom center
- File size: Under 100MB
- Format: PDF/A preferred, standard PDF acceptable

**Quality Check:**
- [ ] All text is readable and searchable
- [ ] No formatting errors or missing characters
- [ ] Figures/diagrams are clear and legible
- [ ] Page numbers are sequential
- [ ] Total pages: ~120

### 2.2 Prepare Drawings (Optional but Recommended)

The specification references 5 figures. You can either:

**Option A: Create Formal Patent Drawings**

Use the existing diagrams in the repository:
1. `cognitive_architecture.svg` → Convert to PDF
2. Create Discord event mesh diagram
3. Create AI agent routing diagram
4. Create security flow diagram
5. Create PR workflow sequence diagram

**Drawing Requirements:**
- Black and white line drawings (no color, no photographs)
- Minimum line width: 0.3mm
- Margins: At least 1 inch on all sides
- Each drawing on separate page
- Figure numbers clearly labeled
- Reference characters (if any) clearly visible

**Option B: Include Diagrams in Specification**

Embed diagrams directly in the specification PDF (simpler for provisional)

**Option C: Submit Without Drawings**

Provisional applications don't strictly require drawings. You can file without them and add formal drawings when converting to non-provisional.

### 2.3 Verify PDF Files

Before proceeding:
- [ ] Open each PDF to verify it displays correctly
- [ ] Check that all pages are present
- [ ] Verify file size is reasonable (under 100MB total)
- [ ] Ensure PDFs are not password-protected
- [ ] Confirm PDFs are text-searchable (not just scanned images)

**Time:** 30-60 minutes

---

## STEP 3: ACCESS USPTO PATENT CENTER

1. Go to: https://patentcenter.uspto.gov/
2. Log in with your USPTO.gov credentials
3. You should see the Patent Center dashboard

**First-time Users:**
- The interface may prompt you to take a tutorial (recommended)
- Familiarize yourself with the layout
- Note: The system auto-saves as you work

**Alternative:** If Patent Center is unavailable, you can use EFS-Web (older system): https://efs.uspto.gov/

**Time:** 5 minutes

---

## STEP 4: START NEW APPLICATION

### 4.1 Initiate Filing

1. Click **"New Application"** button (usually top-right)
2. Select **"Utility Application"**
3. Choose **"Provisional"** application type
4. Click **"Continue"** or **"Next"**

### 4.2 Application Data Sheet (ADS)

The system will guide you through creating an Application Data Sheet:

#### Applicant Information

**Inventor 1:**
- Legal name: Domenic Garza
- Applicant type: Inventor
- Citizenship: United States
- Residence: [Your state and country]
- Mailing address:
  - Street address: [Your address]
  - City: [City]
  - State: [State]
  - ZIP: [ZIP code]
  - Country: United States

**Note:** If there are additional inventors, add them here. Based on the repository, it appears you are the sole inventor.

#### Correspondence Information

- Name: Domenic Garza
- Email: [Your email]
- Phone: [Your phone number]
- Correspondence address: Same as inventor address (or different if using attorney)

**Email Authorization:** Check the box authorizing USPTO to send correspondence via email

#### Entity Status

**Select:** Micro Entity

**Certification basis:** Gross income basis (37 CFR 1.29(a))

Check all boxes certifying that:
- [ ] Qualifies as small entity
- [ ] Named on 4 or fewer previously filed patent applications
- [ ] Gross income did not exceed 3x median household income
- [ ] Has not assigned rights to entity exceeding income limits

#### Application Information

- **Application Title:** AI-Governed DevOps Control Plane with Discord-Integrated Event Mesh and Human-LLM Co-Sovereignty
- **Attorney Docket Number:** [Optional - use your own reference like "SOVA-001"]
- **Suggested Technology Center:** 2100 (Computer Architecture, Software, and Information Security)

**Time:** 20 minutes

---

## STEP 5: UPLOAD DOCUMENTS

### 5.1 Specification

1. Click **"Add Documents"** or **"Upload Files"**
2. Select **"Specification"** as document type
3. Choose your `PROVISIONAL_SPECIFICATION.pdf` file
4. Click **"Upload"**
5. Wait for upload confirmation
6. Verify page count is correct (~120 pages)

### 5.2 Drawings (If Prepared)

1. Click **"Add Documents"**
2. Select **"Drawings"** as document type
3. Choose your drawings PDF file(s)
4. Click **"Upload"**
5. Verify upload completed

**Note:** If you embedded drawings in the specification, you can skip separate drawings upload.

### 5.3 Cover Sheet (Optional)

The system generates a cover sheet automatically based on the ADS, but you can upload your custom cover sheet:

1. Click **"Add Documents"**
2. Select **"Other"** or **"Miscellaneous"**
3. Upload `COVER_SHEET.pdf`

### 5.4 Verify All Documents

Review the document list:
- [ ] Specification: Present, correct page count
- [ ] Drawings: Present (if applicable)
- [ ] Cover sheet: Auto-generated or uploaded
- [ ] Total file size: Under 100MB

**Time:** 10 minutes

---

## STEP 6: REVIEW APPLICATION

### 6.1 Use Validation Tool

Patent Center includes a validation tool:

1. Click **"Validate"** button
2. Review any errors (red) or warnings (yellow)
3. **Errors must be fixed** before submission
4. **Warnings** can often be ignored for provisionals

**Common warnings (can ignore):**
- "Claims not present" (claims optional for provisional)
- "Abstract not identified separately" (embedded in specification is fine)
- "Drawings reference not found" (if you included drawings in spec)

### 6.2 Review Fees

1. Go to **"Fees"** section
2. Verify fee calculation:
   - Provisional Application Filing Fee (Micro Entity): **$75**
   - Total: **$75**

3. If fee is incorrect:
   - Verify micro entity status is properly selected
   - Check that application type is "Provisional"

### 6.3 Final Review Checklist

Before submitting:
- [ ] All inventor information is accurate
- [ ] Email address is correct (you'll receive confirmation here)
- [ ] Application title is correct
- [ ] Micro entity status is certified
- [ ] Specification PDF is uploaded successfully
- [ ] Fee amount is $75
- [ ] Payment method is ready

**Time:** 10 minutes

---

## STEP 7: PAYMENT

### 7.1 Select Payment Method

**Option A: Credit Card** (most common)
1. Click **"Pay Fees"** or **"Proceed to Payment"**
2. Select **"Credit Card"**
3. Enter card details:
   - Card number
   - Expiration date
   - CVV
   - Billing address
4. Click **"Submit Payment"**

**Option B: USPTO Deposit Account** (if you have one)
1. Select **"Deposit Account"**
2. Enter account number
3. Authorize charge

**Option C: Electronic Funds Transfer**
1. Select **"EFT"**
2. Follow bank authorization process

### 7.2 Payment Confirmation

- Wait for payment processing (usually instant)
- Verify you receive payment confirmation
- Note the payment confirmation number
- **Save the receipt PDF** (download/print it)

**Time:** 5 minutes

---

## STEP 8: SUBMIT APPLICATION

### 8.1 Final Submission

1. Review the submission summary one last time
2. Check the box agreeing to terms and conditions
3. Click **"Submit"** or **"File Application"**
4. **Do not close browser** until you see confirmation

### 8.2 Wait for Processing

- The system will process your submission (30 seconds to 2 minutes)
- You'll see a progress indicator
- **Do not refresh or close the page**

### 8.3 Confirmation Screen

Upon successful submission, you'll see:

- **Application Number:** 63/XXX,XXX (your provisional application number)
- **Filing Date:** [Today's date]
- **Confirmation Number:** [Transaction ID]

**CRITICAL: Save this information immediately**

**Time:** 5 minutes

---

## STEP 9: SAVE CONFIRMATION DOCUMENTS

### 9.1 Download Filing Receipt

1. On the confirmation screen, click **"Download Filing Receipt"**
2. Save as: `USPTO_Filing_Receipt_[DATE].pdf`
3. Store in secure location (cloud backup recommended)

### 9.2 Note Key Information

Create a text file or document with:

```
USPTO PROVISIONAL PATENT APPLICATION

Application Number: 63/XXX,XXX
Filing Date: [DATE]
Confirmation Number: [NUMBER]
Title: AI-Governed DevOps Control Plane with Discord-Integrated Event Mesh and Human-LLM Co-Sovereignty
Inventor: Domenic Garza
Entity Status: Micro Entity
Filing Fee: $75.00
Payment Date: [DATE]

CRITICAL DEADLINES:
- Non-provisional conversion deadline: [FILING DATE + 12 MONTHS]
- 11-month reminder: [FILING DATE + 11 MONTHS]

USPTO CORRESPONDENCE:
- Email: [Your email]
- Customer Number: [If assigned]
```

### 9.3 Set Calendar Reminders

**CRITICAL:** Set reminders for:

1. **11 months from filing date:**
   - Title: "Patent Deadline - 1 Month Warning"
   - Action: Begin preparing non-provisional application

2. **11.5 months from filing date:**
   - Title: "Patent Deadline - 2 Week Warning"
   - Action: File non-provisional or request extension

**The 12-month deadline is ABSOLUTE. Missing it means losing your priority date.**

**Time:** 10 minutes

---

## STEP 10: POST-FILING ACTIONS

### 10.1 Email Confirmation

Within 24 hours, you should receive:
- Email from USPTO confirming receipt
- Formal filing receipt (PDF attachment)

If you don't receive this:
- Check spam folder
- Log back into Patent Center and download receipt manually
- Contact USPTO: 1-800-786-9199

### 10.2 Update Repository and Communications

**Immediate updates:**

1. **Update README.md:**
```markdown
[![Patent Pending](https://img.shields.io/badge/Patent-Pending-yellow)](./patent/)

**Patent Status:** Patent Pending  
**U.S. Provisional Application No.:** 63/XXX,XXX  
**Filing Date:** [DATE]
```

2. **Update LICENSE file:**
```markdown
## Patent Notice

This software implements technologies covered by:
U.S. Provisional Patent Application No. 63/XXX,XXX
Filing Date: [DATE]
Patent rights are reserved.
```

3. **Update Discord bot status:**
```javascript
client.user.setActivity('Patent Pending 63/XXX,XXX', { type: 'WATCHING' });
```

4. **Post Discord announcement:** See `PATENT_PENDING_STATEMENTS.md` for template

### 10.3 Documentation and Record Keeping

Create a `patent/` directory structure:

```
patent/
├── filed/
│   ├── PROVISIONAL_SPECIFICATION.pdf
│   ├── USPTO_Filing_Receipt_[DATE].pdf
│   ├── Payment_Receipt_[DATE].pdf
│   └── Application_Details.txt
├── correspondence/
│   └── [Future USPTO letters]
├── supporting_evidence/
│   ├── development_timeline.md
│   ├── code_snapshots/
│   └── documentation_versions/
└── non_provisional_prep/
    └── [Start preparing in month 11]
```

**Backup:** Store copies in:
- Local secure folder
- Cloud storage (Google Drive, Dropbox)
- Physical USB drive (air-gapped backup)

### 10.4 Notify Stakeholders

Inform the following parties (as appropriate):

**Internal:**
- [ ] Development team
- [ ] Business partners
- [ ] Advisors/mentors
- [ ] Investors (current or prospective)

**External:**
- [ ] Website visitors (update site)
- [ ] Social media followers (announcement post)
- [ ] Newsletter subscribers
- [ ] Community members (Discord announcement)
- [ ] Potential customers/partners

**Use templates from:** `PATENT_PENDING_STATEMENTS.md`

**Time:** 1-2 hours

---

## TROUBLESHOOTING

### Problem: "Validation errors prevent submission"

**Solutions:**
- Review each error message carefully
- Common fixes:
  - Add missing inventor information
  - Verify entity status certification is complete
  - Ensure specification PDF is properly formatted
  - Check that file sizes are under limits

### Problem: "Payment declined"

**Solutions:**
- Verify credit card has sufficient funds
- Check that card accepts online payments
- Try a different payment method
- Contact your bank if card is being blocked

### Problem: "Session timeout"

**Solutions:**
- Patent Center auto-saves most data
- Log back in and resume where you left off
- If data is lost, you'll need to re-enter
- Keep a separate document with all info to copy-paste

### Problem: "Can't upload PDF"

**Solutions:**
- Verify file size is under 100MB
- Check that PDF is not password-protected
- Try re-saving PDF with different software
- Ensure PDF is not corrupted (open and view it first)

### Problem: "Didn't receive confirmation email"

**Solutions:**
- Check spam/junk folder
- Wait 24 hours (system can be slow)
- Log into Patent Center and download receipt manually
- Contact USPTO at 1-800-786-9199

---

## USPTO CONTACT INFORMATION

### General Inquiries
- **Phone:** 1-800-786-9199 (1-800-PTO-9199)
- **Hours:** Monday-Friday, 8:30 AM - 5:00 PM Eastern Time
- **TTY:** 1-571-272-9950 (for deaf/hard of hearing)

### Email Support
- **General:** usptoinfo@uspto.gov
- **Electronic filing:** ebc@uspto.gov
- **Fees:** feeslegal@uspto.gov

### Patent Center Technical Support
- **Help Desk:** Available through Patent Center interface
- **Live Chat:** Available during business hours

### Mailing Address (for paper filing, not recommended)
```
Commissioner for Patents
P.O. Box 1450
Alexandria, VA 22313-1450
```

### In-Person Assistance
**Alexandria Campus:**
600 Dulany Street
Alexandria, VA 22314

**Public Search Facility:** Available for in-person research

---

## COST BREAKDOWN

### Filing Fees (Micro Entity)
| Item | Fee | Notes |
|------|-----|-------|
| Provisional Application Filing Fee | $75 | One-time, at filing |
| **Total at Filing** | **$75** | **Required to submit** |

### Future Costs (When Converting to Non-Provisional)
| Item | Micro Entity Fee | Notes |
|------|------------------|-------|
| Non-provisional Filing Fee | $200 | Due at non-provisional filing |
| Search Fee | $200 | Due at non-provisional filing |
| Examination Fee | $200 | Due at non-provisional filing |
| **Total at Conversion** | **$600** | **Due within 12 months** |

### Total Cost to Patent Issuance (Estimated)
- Filing and examination: ~$1,000 (micro entity)
- Maintenance fees over 20 years: ~$5,000 (micro entity)
- Attorney fees (optional): $5,000-$15,000
- **Total DIY cost:** ~$6,000 over patent lifetime
- **Total with attorney:** ~$11,000-$21,000

**Note:** Micro entity fees are 75% cheaper than standard fees. Maintain micro entity status to minimize costs.

---

## TIMELINE AND MILESTONES

### Immediate (Today)
- [ ] File provisional application
- [ ] Save all confirmation documents
- [ ] Set 11-month calendar reminder
- [ ] Update repository with patent pending notice

### Week 1
- [ ] Receive USPTO email confirmation
- [ ] Update all documentation and communications
- [ ] Announce to stakeholders
- [ ] Post on social media

### Month 1-3
- [ ] Monitor for USPTO correspondence
- [ ] Continue development and documentation
- [ ] Gather user feedback and usage data

### Month 6
- [ ] Review progress and decide on non-provisional strategy
- [ ] Consider whether international protection is needed
- [ ] Begin researching patent attorneys (if desired)

### Month 9
- [ ] Conduct thorough prior art search
- [ ] Document all improvements and new features
- [ ] Draft additional claims for non-provisional

### Month 11
- [ ] **CRITICAL:** Begin non-provisional preparation
- [ ] Finalize claims
- [ ] Prepare formal drawings
- [ ] Engage patent attorney if needed

### Month 11.5
- [ ] File non-provisional application or extension
- [ ] **DEADLINE CANNOT BE MISSED**

### Month 12 (Deadline Day)
- [ ] Provisional expires if not converted
- [ ] Non-provisional must be filed by end of day

---

## CHECKLIST: READY TO FILE?

### Documents Prepared
- [ ] Specification PDF (~120 pages)
- [ ] Cover sheet completed
- [ ] Drawings prepared (optional)
- [ ] All files under 100MB total

### Information Collected
- [ ] Full legal name
- [ ] Complete mailing address
- [ ] Email for USPTO correspondence
- [ ] Phone number
- [ ] Citizenship confirmed

### Account Setup
- [ ] USPTO.gov account created
- [ ] Login credentials verified
- [ ] Payment method ready ($75)

### Understanding Confirmed
- [ ] Read this entire guide
- [ ] Understand provisional vs non-provisional
- [ ] Aware of 12-month deadline
- [ ] Know how to use "patent pending" properly
- [ ] Set calendar reminders

### Ready to Proceed
- [ ] All above items checked
- [ ] Have 1-2 hours available
- [ ] Stable internet connection
- [ ] Quiet workspace for focus

**If all boxes are checked, you're ready to file! Proceed to Step 1.**

---

## AFTER FILING: WHAT'S NEXT?

### Immediate Benefits

**You can now:**
- Use "Patent Pending" in all materials
- Mark products/software with pending status
- Disclose invention publicly without losing rights
- Discuss technology with investors/partners
- Market the innovation with IP protection notice

### 12-Month Strategy

**Option 1: Convert to Non-Provisional** (most common)
- File full utility patent application
- Maintain priority date from provisional
- Begin examination process
- Patent can issue 2-4 years later

**Option 2: File PCT Application**
- International patent protection
- Single application covering 150+ countries
- 30 months to decide which countries to pursue
- More expensive but broader protection

**Option 3: Let Provisional Expire**
- If invention didn't prove valuable
- If market conditions changed
- If better alternatives emerged
- No further fees, no obligations

### Long-Term Patent Strategy

**Year 1:** Provisional period
- Continue development
- Gather evidence of market demand
- Refine technology
- Build user base

**Year 1-3:** Non-provisional examination
- Respond to USPTO office actions
- Refine claims
- Conduct prior art defense
- Negotiate claim scope

**Year 3-20:** Patent in force
- Enforce against infringers
- License technology
- Build defensive patent portfolio
- Pay maintenance fees

**Beyond Year 20:** Patent expires
- Technology enters public domain
- You've had 20+ years of protection
- Focus shifts to trade secrets/ongoing innovation

---

## EXPERT TIPS

### Tip 1: Document Everything
Keep detailed records of:
- Development timeline
- Design decisions
- Failed approaches (shows non-obviousness)
- Customer feedback
- Market research

These may be valuable if patent is challenged.

### Tip 2: Maintain Micro Entity Status
Don't jeopardize micro entity status by:
- Assigning rights to large company
- Exceeding income thresholds
- Being named on too many applications

Micro entity saves thousands in fees.

### Tip 3: Use 12 Months Wisely
Don't rush non-provisional conversion:
- Refine invention based on user feedback
- Add improvements to patent claims
- Gather data proving commercial viability
- Assess market opportunity

But don't forget the deadline!

### Tip 4: Consider Professional Help
For non-provisional conversion, consider hiring patent attorney:
- They can strengthen claims
- Navigate USPTO examination
- Avoid common pitfalls
- Save time and stress

Cost: $5k-$15k (expensive but potentially worthwhile)

### Tip 5: International Protection
If targeting global markets:
- File PCT within 12 months
- Evaluate which countries matter
- Budget for international prosecution
- Consider regional offices (EPO, WIPO)

---

## ADDITIONAL RESOURCES

### USPTO Resources
- **Patent Center:** https://patentcenter.uspto.gov/
- **General Information:** https://www.uspto.gov/patents
- **Fee Schedule:** https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule
- **Provisional Application Guide:** https://www.uspto.gov/patents/basics/types-patent-applications/provisional-application-patent

### Educational Resources
- **USPTO Training:** Free webinars and tutorials
- **Patent It Yourself** (book by David Pressman)
- **PatentWizard** software for DIY filing
- **Law school clinics:** Free patent help in some areas

### Online Communities
- **Reddit r/patents:** Informal advice (not legal advice)
- **IP Watchdog Forums:** Discussion by patent professionals
- **USPTO's Independent Inventor Resources**

---

## LEGAL DISCLAIMER

This guide is for informational purposes only and does not constitute legal advice. Patent law is complex and situation-specific. For official legal advice regarding your specific circumstances, consult a registered patent attorney or agent.

The author(s) of this guide are not responsible for any errors, omissions, or outcomes resulting from following these instructions. Always verify current USPTO rules and fees, as they may change.

---

## DOCUMENT HISTORY

**Version:** 1.0  
**Created:** [DATE]  
**Author:** Strategickhaos DAO LLC  
**Last Updated:** [DATE]

---

**YOU'VE GOT THIS.**

**The hardest part is starting. Once you begin the process, it's straightforward and well-guided by the USPTO system. Take your time, double-check everything, and don't hesitate to contact USPTO if you have questions.**

**This filing establishes your priority date and protects your innovation. Everything you build from here branches off this anchor.**

**Good luck! 🚀**

---

*END OF FILING INSTRUCTIONS*
