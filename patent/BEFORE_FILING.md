# Before Filing - Information to Complete

**Important: Fill in these placeholders before submitting to USPTO**

---

## 📝 REQUIRED INFORMATION

Before you file the provisional patent application, you must complete the following placeholder fields:

### 1. Inventor Contact Information

**In COVER_SHEET.md (Lines 23-30):**

Replace these placeholders:
```
[Street Address]  → Your actual street address
[City, State, ZIP] → Your city, state, and ZIP code
[email@example.com] → Your actual email address
[To be provided] → Your phone number
```

**Example:**
```
Name: Domenic Garza
Address:
  123 Innovation Drive
  San Francisco, CA 94102
  United States
Email: domenic.garza@strategickhaos.com
Telephone: (555) 123-4567
```

### 2. Application Number and Filing Date

**After USPTO filing, update these in all documents:**

Files to update with actual numbers:
- `patent/README.md` (multiple locations)
- `patent/QUICK_REFERENCE.md` (multiple locations)
- `patent/PATENT_PENDING_STATEMENTS.md` (all templates)

Replace:
```
[NUMBER] → 63/XXX,XXX (your actual application number)
[DATE] → MM/DD/YYYY (your actual filing date)
```

### 3. Document Metadata

**In patent/README.md (Line 502):**
```
**Last Updated:** [Current Date] → Update to actual date
```

**In patent/QUICK_REFERENCE.md (Line 457):**
```
**Last Updated:** [Current Date] → Update to actual date
```

---

## ✅ PRE-FILING CHECKLIST

### Personal Information Ready
- [ ] Full legal name: **Domenic Garza** ✓ (already filled)
- [ ] Complete mailing address: **[NEEDS TO BE FILLED]**
- [ ] Email address for USPTO correspondence: **[NEEDS TO BE FILLED]**
- [ ] Phone number: **[NEEDS TO BE FILLED]**
- [ ] Citizenship: **United States** ✓ (already filled)

### Micro Entity Verification
- [ ] I am an individual inventor (not a corporation) ✓
- [ ] I have been named on 4 or fewer previous patent applications ✓
- [ ] My gross income did not exceed 3x median household income (~$250k in 2024)
- [ ] I have not assigned rights to an entity exceeding income limits

### Documents Prepared
- [ ] PROVISIONAL_SPECIFICATION.md converted to PDF
- [ ] PDF is properly formatted and readable
- [ ] File size is under 100MB
- [ ] PDF is not password-protected

### Account and Payment
- [ ] USPTO.gov account created at https://my.uspto.gov/
- [ ] Login credentials tested and working
- [ ] Payment method ready (credit card with $75 available)

### Post-Filing Preparation
- [ ] Have calendar app open to set reminders immediately
- [ ] Have PATENT_PENDING_STATEMENTS.md ready to update repo
- [ ] Know location to save USPTO confirmation documents

---

## 🔄 QUICK UPDATE WORKFLOW

### Step 1: Fill In Personal Info (Now, Before Filing)

1. Open `patent/COVER_SHEET.md`
2. Find lines 23-30 (Applicant Information section)
3. Replace all `[To be provided]` placeholders with your actual information
4. Save the file

### Step 2: Convert to PDF

```bash
# Using Pandoc (if installed)
pandoc patent/PROVISIONAL_SPECIFICATION.md -o patent/PROVISIONAL_SPECIFICATION.pdf

# Or use VS Code Markdown PDF extension
# Or use online converter: https://www.markdowntopdf.com/
```

### Step 3: File on USPTO Patent Center

Follow the complete instructions in `patent/FILING_INSTRUCTIONS.md`

### Step 4: Update with Application Number (After Filing)

1. Receive confirmation from USPTO with application number (63/XXX,XXX)
2. Run this find-and-replace in all patent/ files:
   - Find: `[NUMBER]`
   - Replace: `63/XXX,XXX` (your actual application number)
   - Find: `[DATE]`
   - Replace: `MM/DD/YYYY` (your actual filing date)

3. Files that need updating:
   - patent/README.md
   - patent/QUICK_REFERENCE.md
   - patent/PATENT_PENDING_STATEMENTS.md

### Step 5: Update Repository

Use templates from `patent/PATENT_PENDING_STATEMENTS.md` to:
1. Add patent pending badge to main README.md
2. Update LICENSE file with patent notice
3. Update Discord bot status
4. Post announcement in Discord

---

## ⚠️ IMPORTANT NOTES

### Why Are There Placeholders?

These placeholder fields contain personal information that:
- Cannot be pre-filled without knowing your details
- Must be accurate for USPTO correspondence
- Are required by USPTO for application processing

### What Happens If I File With Placeholders?

**Do NOT file with incomplete information!**

The USPTO will:
- Reject the application
- Request corrected information
- May charge correction fees
- Delay your priority date

**Always complete ALL placeholder fields before filing.**

### Can I Change Information Later?

**Before filing:** Change freely  
**After filing:** 
- Address changes: Notify USPTO (form available)
- Name changes: Requires legal documentation
- Email/phone: Update through Patent Center
- Specification content: Cannot change (provisional is locked)

---

## 📋 SPECIFIC FIELD LOCATIONS

### In COVER_SHEET.md

**Section: Applicant Information (Line 14-30)**
```markdown
**Mailing Address:**  
  [Street Address]           ← FILL THIS
  [City, State, ZIP]         ← FILL THIS
  [Country]                  ← Should be "United States"

**Email:** [To be provided]  ← FILL THIS
**Telephone:** [To be provided]  ← FILL THIS
```

**Section: Correspondence Information (Line 38-46)**
```markdown
Address:  
  [Street Address]           ← FILL THIS (can be same as above)
  [City, State, ZIP]         ← FILL THIS
  United States

Email: [To be provided]      ← FILL THIS
Telephone: [To be provided]  ← FILL THIS
```

### In PROVISIONAL_SPECIFICATION.md

**Section: Inventor Information (End of document)**
```markdown
**Email:** [To be provided]  ← OPTIONAL for spec, required for cover sheet
**Citizenship:** [To be provided]  ← Should be "United States"
**Residence:** [To be provided]    ← Should be your state
```

---

## 🎯 RECOMMENDED: FILL NOW

**It will take 2 minutes and prevent filing delays.**

Open `patent/COVER_SHEET.md` and fill in your:
1. Street address
2. City, State, ZIP
3. Email address
4. Phone number

Then you'll be 100% ready to file immediately.

---

## 📞 QUESTIONS?

**USPTO Help:**
- Phone: 1-800-786-9199
- Email: usptoinfo@uspto.gov
- Hours: Mon-Fri, 8:30 AM - 5:00 PM ET

**Common Questions:**

**Q: What if I don't want to put my home address?**  
A: You can use a business address, PO Box, or registered agent address. Must be reliable for receiving USPTO mail.

**Q: What email should I use?**  
A: Use an email you check regularly. USPTO will send important correspondence here. Gmail, Outlook, etc. are fine.

**Q: What if my phone number changes?**  
A: Update it through Patent Center at https://patentcenter.uspto.gov/ after filing.

**Q: Can I file without completing these fields?**  
A: No. USPTO requires complete inventor contact information. Application will be rejected if incomplete.

---

## ✅ READY TO PROCEED?

Once you've filled in the personal information placeholders:

1. Check the **PRE-FILING CHECKLIST** at the top of this document
2. If all boxes are checked, proceed to **FILING_INSTRUCTIONS.md**
3. Follow the step-by-step guide to file on USPTO Patent Center

**You're 2 minutes of data entry away from being ready to file!**

---

**Document Version:** 1.0  
**Purpose:** Pre-filing preparation checklist  
**Maintained By:** Strategickhaos DAO LLC

---

*END OF BEFORE FILING GUIDE*
