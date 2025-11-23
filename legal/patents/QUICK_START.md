# Quick Start: File Your Provisional Patent in < 45 Minutes

## TL;DR - The Nuclear Option

You're about to establish **Patent Pending** status for **$75** and lock in your priority date **forever**. This guide gets you from zero to filed in under 45 minutes.

## Prerequisites (2 minutes)

- [ ] USPTO.gov account (create at https://efs.uspto.gov/EFS-Web2/)
- [ ] $75 (credit card or deposit account)
- [ ] Your legal name and address
- [ ] Basic description of your invention

## Step 1: Micro-Entity Certification (5 minutes)

**Do this FIRST - saves you 75% on all fees forever**

### Quick Check - Do You Qualify?
✓ Income < 3x median U.S. household income (~$45k in 2025)?  
✓ Fewer than 5 prior patent applications?  
✓ No obligation to assign to a large company?

**YES to all three** = You're micro-entity qualified

**Note**: Income threshold changes annually. Check current limits at: https://www.uspto.gov/patents/laws/micro-entity-status

### Action:
```bash
# Windows PowerShell
.\legal\patents\file-provisional-patent.ps1

# Linux/Mac
./legal/patents/file-provisional-patent.sh
```

The script will:
- Open the SB/15A form in your browser
- Download it
- Tell you where to save it

**Fill it out**:
1. Your full legal name
2. Today's date
3. Your signature
4. Save as: `legal/patents/receipts/MICRO_ENTITY_CERT.pdf`

## Step 2: Provisional Application (10-20 minutes)

### Option A: Use the Template (Recommended for First-Timers)

The script created a template at `legal/patents/provisional/PROVISIONAL_PATENT_APPLICATION.md`

**Edit these sections** (keep it simple):
- **Title**: What your invention is called
- **Summary**: What it does (2-3 paragraphs)
- **Detailed Description**: How it works (technical details)
- **Novel Features**: What makes it unique (bullet points)

### Option B: Write Your Own

**Minimum requirements**:
- **Title** (one line)
- **What it is** (one paragraph)
- **How it works** (technical description)
- **What's new** (novel features)
- **Diagrams** (optional but helpful)

**Format**:
- US Letter (8.5" x 11")
- 1-inch margins
- 12-point font
- Save as PDF

### Convert to PDF

**If you have Pandoc**:
```bash
pandoc PROVISIONAL_PATENT_APPLICATION.md -o STRATEGICKHAOS_PROVISIONAL_2025-11-22.pdf -V geometry:margin=1in
```

**Otherwise**:
1. Open the markdown in Word/Google Docs
2. Format (1" margins, 12pt font)
3. Export as PDF

## Step 3: File via USPTO EFS-Web (15 minutes)

### Login
https://efs.uspto.gov/EFS-Web2/

### Click Through:
1. **New Application** → **Provisional Application**
2. **Micro Entity (SB/15A)** → Upload `MICRO_ENTITY_CERT.pdf`
3. **Inventor Information**:
   - Name: [Your legal name]
   - Address: [Your address]
4. **Title**: 
   ```
   Autonomous Charitable Revenue Distribution System Using AI-Governed DAO with Cryptographic Verification
   ```
5. **Upload Application**: Your provisional PDF
6. **Validate** → Fix any errors
7. **Pay $75** → Credit card or deposit account
8. **Submit** → Save confirmation page

## Step 4: Wait for Receipt (5-60 minutes)

**You'll receive an email with**:
- Application Number: `63/XXXXXX`
- Filing Date: Today's date
- Official Filing Receipt (PDF)

**Save the receipt**: `legal/patents/receipts/USPTO_Receipt.pdf`

## Step 5: Proof Chain (5 minutes)

**After you get your receipt**, run:

```bash
# Windows PowerShell
.\legal\patents\create-proof-chain.ps1 -ApplicationNumber "63/XXXXXX"

# Linux/Mac
./legal/patents/create-proof-chain.sh 63/XXXXXX
```

This creates:
- ✓ Git commit with all patent files
- ✓ GPG signature (if configured)
- ✓ OpenTimestamps (Bitcoin proof)
- ✓ Patent tracking document

## Done! 🎉

### You Now Have:

✓ **Patent Pending Status** (use it everywhere)  
✓ **Priority Date** (locked in forever)  
✓ **Application Number** (63/XXXXXX)  
✓ **12 Months** to file utility patent  
✓ **Proof Chain** (Git + GPG + Bitcoin)  
✓ **$75** total cost (vs $300 standard)  

### Use This Everywhere:

> **Strategickhaos DAO LLC – Patent Pending (U.S. Provisional Application 63/XXXXXX)**

### Where to Use It:

- GitHub README.md
- Website footer
- Documentation
- Pitch decks
- Business cards
- Contracts
- Marketing materials

## What Happens Next?

### Immediately
- **Start using "Patent Pending"** on everything
- Mark your calendar: Filing date + 12 months

### Month 1-6
- Continue developing your product
- Document all improvements
- Test and iterate
- Build your business

### Month 6-9
- Begin drafting utility patent with attorney
- Conduct prior art search (if not done)
- Refine claims and specifications

### Month 10-11
- **DEADLINE APPROACHING**
- File utility patent (non-provisional)
- Cost: ~$3,680-$10,680 (including attorney)

### Month 12
- **HARD DEADLINE**
- Provisional expires if no utility patent filed
- You lose priority date forever

## Important Reminders

### DO Use Patent Pending
✓ On all products and services  
✓ In marketing materials  
✓ On your website  
✓ In investor materials  

### DON'T
✗ Call it a "patent" (it's "pending")  
✗ Miss the 12-month deadline  
✗ Publicly disclose inventions BEFORE filing  
✗ Ignore improvements (file additional provisionals)  

## Cost Breakdown

### Today (Provisional)
- Filing fee (micro): **$75**
- Time investment: **< 45 minutes**
- **Total: $75**

### Within 12 Months (Utility Patent)
- Filing fees (micro): ~$680
- Patent attorney: $3,000-$10,000
- **Total: ~$3,680-$10,680**

### Return on Investment
- **Patent protection**: 20 years
- **Competitive advantage**: Priceless
- **Investor confidence**: Massive
- **Legal deterrent**: Significant

## Emergency Contact

**Problem during filing?**
- USPTO Contact Center: **1-800-786-9199**
- Hours: Mon-Fri, 8:30 AM - 8:00 PM ET

**Technical issues with scripts?**
- Check: `legal/patents/README.md`
- Open issue in this repo

**Need legal advice?**
- Consult a licensed patent attorney
- USPTO Pro Bono: https://www.uspto.gov/patents/basics/using-legal-services/pro-bono

## Success Checklist

After filing, verify you have:

- [ ] Application number (63/XXXXXX)
- [ ] Official filing receipt (saved as PDF)
- [ ] Micro-entity certification (on file)
- [ ] Provisional application PDF (saved)
- [ ] Git commit with proof chain
- [ ] Calendar reminder for 12-month deadline
- [ ] Started using "Patent Pending" statement

## You Did It!

**Congratulations!** You just:

- Established a priority date for your invention
- Protected your intellectual property for $75
- Created a cryptographic proof chain
- Joined the ranks of patent holders
- Gave your company serious legal armor

**This single filing receipt is worth more than most AI startups that raised $50M this year.**

You're now **untouchable on three axes**:
1. **Legal**: Wyoming DAO + irrevocable charity + Patent Pending
2. **Cryptographic**: GPG + OpenTimestamps + Arweave
3. **Intellectual Property**: USPTO priority date

The empire just grew fangs. 🐉

---

**Questions?** See [USPTO_FILING_GUIDE.md](USPTO_FILING_GUIDE.md) for comprehensive details.

**Need help?** Open an issue or contact USPTO at 1-800-786-9199.

---

**Last Updated**: 2025-11-22  
**Version**: 1.0  
**Time to Complete**: < 45 minutes  
**Cost**: $75 (micro-entity)  
**Value**: Priceless
