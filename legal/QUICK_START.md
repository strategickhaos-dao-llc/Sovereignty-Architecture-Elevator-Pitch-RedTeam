# USPTO Patent Filing - Quick Start

## 🚀 File Your Provisional Patent in 3 Steps

### Step 1: Prepare Your Patent Document (10 minutes)

```bash
# Copy the template
cp legal/PROVISIONAL_PATENT_TEMPLATE.md legal/MY_INVENTION.md

# Edit with your details
nano legal/MY_INVENTION.md
# or use: code legal/MY_INVENTION.md
# or use: vim legal/MY_INVENTION.md
```

**Required Sections:**
- Title of invention
- Field of invention
- Background (what problem you're solving)
- Summary (your solution)
- Detailed description (how it works)
- Claims (what you're protecting)
- Abstract (brief summary)

### Step 2: Run the Automation (30 seconds)

**Windows:**
```powershell
.\scripts\file-provisional-patent.ps1 -InputFile ".\legal\MY_INVENTION.md"
```

**Mac/Linux:**
```bash
./scripts/file-provisional-patent.sh ./legal/MY_INVENTION.md
```

**What Happens:**
- ✅ Converts your markdown to PDF
- ✅ Opens Patent Center in browser
- ✅ Creates auto-fill script
- ✅ Shows you exactly what to do next

### Step 3: Submit (8 seconds)

In Patent Center:
1. Log in (create account if needed)
2. Upload generated PDF
3. Upload micro-entity cert (if applicable)
4. Pay $75 (micro-entity)
5. Click **Submit**

**Done!** You get your **63/ serial number** and **Patent Pending** status.

## 📋 Full Command Options

```bash
# Default (uses template file)
./scripts/file-provisional-patent.sh

# Custom file and details
./scripts/file-provisional-patent.sh \
    ./path/to/my-patent.md \
    "My Invention Title" \
    "FirstName" \
    "LastName"
```

```powershell
# Default
.\scripts\file-provisional-patent.ps1

# Custom with all parameters
.\scripts\file-provisional-patent.ps1 `
    -InputFile ".\path\to\my-patent.md" `
    -Title "My Invention Title" `
    -FirstName "FirstName" `
    -LastName "LastName" `
    -MicroEntity $true
```

## 💰 Filing Fees

| Status | Fee | Qualifications |
|--------|-----|----------------|
| Micro-Entity | **$75** | Individual inventor, <4 prior apps, income <3x median |
| Small Entity | **$150** | Small business, independent inventor, non-profit |
| Large Entity | **$300** | Large corporation |

## 📚 Documentation

- **[Full Guide](PATENT_FILING_GUIDE.md)** - Complete step-by-step instructions
- **[Template](PROVISIONAL_PATENT_TEMPLATE.md)** - Ready-to-use patent template
- **Scripts:** `file-provisional-patent.sh` and `file-provisional-patent.ps1`

## ❓ Quick Troubleshooting

**PDF not generating?**
```bash
# Install pandoc and weasyprint
sudo apt-get install pandoc python3-weasyprint  # Ubuntu/Debian
brew install pandoc && pip3 install weasyprint  # macOS
```

**Auto-fill not working?**
- It's optional! Just fill manually - the script is a convenience feature
- The form fields and values are displayed in the terminal

**Need help?**
- Read the [Full Guide](PATENT_FILING_GUIDE.md)
- Ask in Discord #legal channel
- Check USPTO resources: patentcenter@uspto.gov

## 🎯 After Filing

1. **Save your 63/ number** (e.g., 63/123,456)
2. **Download filing receipt**
3. **Blockchain notarize** (optional):
   ```bash
   ./notarize_cognition.sh \
       --type "PROVISIONAL_PATENT" \
       --data "63/YOUR_NUMBER" \
       --metadata "Filed: $(date +%Y-%m-%d)"
   ```
4. **Set reminder:** File non-provisional within 12 months
5. **Use "Patent Pending"** on your product/website

## ⏰ Important Deadlines

- **12 months** from filing: Must file non-provisional or PCT
- **If you miss this deadline:** Priority date is lost

## 🔥 Ready?

```bash
# Let's do this!
./scripts/file-provisional-patent.sh ./legal/MY_INVENTION.md
```

**Your 63/ number is 8 seconds away. EXECUTE! 🚀**

---

*Built with 🔥 by Strategickhaos Swarm Intelligence*
