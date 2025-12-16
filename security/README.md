# Security Infrastructure: CTF & Vulnerability Management

**Project**: Strategickhaos DAO LLC Security Tools  
**Reference**: INV-082 SwarmBounty Specification  
**Version**: 1.0.0

## 🎯 Overview

Comprehensive security infrastructure for vulnerability management and CTF (Capture The Flag) challenge generation. Converts vulnerability findings into educational security challenges and professional reports.

## 📁 Directory Structure

```
security/
├── vuln_reports/          # Vulnerability report management
│   ├── models.py          # Pydantic data models
│   ├── cli.py            # Command-line interface
│   ├── pdf_generator.py  # PDF report generation
│   └── reports/          # Generated reports
├── ctf_challenges/       # CTF challenge generator
│   ├── generator.py      # Challenge generation engine
│   └── generated/        # Output challenges
├── templates/            # Report templates
│   └── hackerone_template.md
└── README.md            # This file
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to security directory
cd security

# Install dependencies
pip install pydantic reportlab pygments pyyaml
```

### 1. Create Vulnerability Report

#### Interactive Mode
```bash
cd vuln_reports
python cli.py create --interactive
```

#### From JSON
```bash
python cli.py create --from-json finding.json
```

### 2. Calculate CVSS Score

```bash
python cli.py calculate-cvss
```

**Interactive CVSS Calculator:**
```
CVSS v3.1 CALCULATOR (Interactive)
1. Attack Vector (AV): N/A/L/P
2. Attack Complexity (AC): L/H
3. Privileges Required (PR): N/L/H
...
CVSS Score: 8.6
Severity: HIGH
```

### 3. Generate CTF Challenges

```bash
cd ctf_challenges
python generator.py
```

**Output formats:**
- JSON (CTFd compatible)
- YAML
- HackerOne format

### 4. Generate PDF Report

```python
from vuln_reports.pdf_generator import VulnReportPDFGenerator

generator = VulnReportPDFGenerator(company_name="Your Company")
generator.generate_pdf(vuln_data, "report.pdf")
```

## 📊 Features

### Vulnerability Report Management

#### Pydantic Data Models (`models.py`)

**Complete validation and structure:**
- Title, Summary, Technical Details
- Proof of Concept with evidence
- Impact Assessment (CIA triad)
- Remediation Recommendations
- CVSS v3.1 scoring

**Example:**
```python
from models import VulnerabilityReport, CVSSVector, AssetInfo

report = VulnerabilityReport(
    report_id="VR-2025-001",
    title="SQL Injection in User Search",
    severity=SeverityLevel.HIGH,
    cvss_score=8.6,
    cvss_vector=CVSSVector(
        attack_vector="N",
        attack_complexity="L",
        # ...
    ),
    # ...
)
```

#### CLI Tool (`cli.py`)

**Commands:**
```bash
# Create report
python cli.py create --interactive
python cli.py create --from-json finding.json

# Calculate CVSS
python cli.py calculate-cvss

# Validate report
python cli.py validate report.json

# List templates
python cli.py list-templates
```

**Features:**
- Interactive report creation
- CVSS v3.1 calculator
- Template selection
- Report validation
- JSON export

#### PDF Generator (`pdf_generator.py`)

**Professional Reports:**
- Company branding placeholders
- Auto-generated executive summaries
- Technical details with code formatting
- Impact assessment tables
- Remediation recommendations
- Appendices and metadata

**Usage:**
```python
generator = VulnReportPDFGenerator(company_name="Strategickhaos DAO")
success = generator.generate_pdf(vuln_data, "output.pdf")
```

### CTF Challenge Generation

#### Challenge Generator (`generator.py`)

**Converts vulnerability findings to CTF challenges:**

**Features:**
- Difficulty calculation based on CVSS
- Automatic categorization (Web, Pwn, Crypto, etc.)
- Point value assignment
- Progressive hint generation
- Solution writeup creation
- Multiple export formats

**Difficulty Levels:**
| Level | CVSS Range | Points |
|-------|------------|--------|
| Easy | 9.0-10.0 (low complexity) | 100 |
| Medium | 7.0-8.9 | 250 |
| Hard | 4.0-6.9 | 500 |
| Insane | 0.0-3.9 | 1000 |

**CTF Categories:**
- `web` - Web application vulnerabilities
- `pwnable` - Binary exploitation
- `crypto` - Cryptographic challenges
- `forensics` - Digital forensics
- `reversing` - Reverse engineering
- `misc` - Miscellaneous

**Example:**
```python
from generator import CTFChallengeGenerator

generator = CTFChallengeGenerator()
challenge = generator.generate_from_vuln_report(vuln_report)

# Export in different formats
generator.export_json("challenges.json")
generator.export_yaml("challenges.yaml")
generator.export_hackerone_format("challenges_hackerone.json")
```

**Output Structure:**
```json
{
  "challenges": [
    {
      "id": "CTF-001",
      "name": "WEB: SQL Injection in User Search",
      "category": "web",
      "difficulty": "medium",
      "points": 250,
      "description": "Challenge scenario...",
      "hints": ["Hint 1", "Hint 2", "Hint 3"],
      "flag": "flag{vr_2025_001_solved}",
      "solution": "Detailed writeup...",
      "learning_objectives": ["SQL injection", "Input validation"],
      "source_vuln_report": "VR-2025-001"
    }
  ]
}
```

### HackerOne Template

**Comprehensive vulnerability report template** (`templates/hackerone_template.md`)

**Sections:**
1. Report Metadata
2. Summary (Executive)
3. Severity Assessment (CVSS)
4. Asset Information
5. Weakness Classification (CWE)
6. Technical Details
7. Proof of Concept
8. Impact Assessment
9. Remediation Recommendations
10. References
11. Bug Bounty Information

**Features:**
- Checkboxes for classification
- CVSS calculator link
- Code block formatting
- Evidence attachment checklist
- Severity guidelines
- Responsible disclosure notes

## 🎓 Usage Examples

### Example 1: Full Workflow

```bash
# Step 1: Create vulnerability report
cd vuln_reports
python cli.py create --interactive

# Step 2: Validate report
python cli.py validate reports/VR-2025-001.json

# Step 3: Generate PDF report
python pdf_generator.py

# Step 4: Generate CTF challenge
cd ../ctf_challenges
python generator.py
```

### Example 2: Programmatic Usage

```python
from vuln_reports.models import VulnerabilityReport
from ctf_challenges.generator import CTFChallengeGenerator
from vuln_reports.pdf_generator import VulnReportPDFGenerator

# Load vulnerability report
with open("vuln_report.json") as f:
    vuln_data = json.load(f)

# Generate CTF challenge
ctf_gen = CTFChallengeGenerator()
challenge = ctf_gen.generate_from_vuln_report(vuln_data)
ctf_gen.export_json("challenge.json")

# Generate PDF report
pdf_gen = VulnReportPDFGenerator(company_name="Your Company")
pdf_gen.generate_pdf(vuln_data, "vuln_report.pdf")
```

### Example 3: CVSS Calculation

```python
from vuln_reports.cli import CVSSCalculator

# Calculate score from vector
score = CVSSCalculator.calculate({
    "attack_vector": "N",
    "attack_complexity": "L",
    "privileges_required": "N",
    "user_interaction": "N",
    "scope": "U",
    "confidentiality": "H",
    "integrity": "H",
    "availability": "N"
})

print(f"CVSS Score: {score}")  # 8.6
```

## 🔐 Security Best Practices

### Responsible Disclosure

1. **Private Reporting**: Submit vulnerabilities privately first
2. **Grace Period**: Allow 90 days for remediation
3. **Coordinated Disclosure**: Work with vendors
4. **No Public PoC**: Until fix is deployed
5. **Sanitize Reports**: Remove sensitive production data

### Report Quality Checklist

- [ ] Clear, concise title
- [ ] Accurate severity assessment
- [ ] Complete CVSS vector
- [ ] Detailed technical explanation
- [ ] Working proof of concept
- [ ] Realistic impact assessment
- [ ] Actionable remediation advice
- [ ] All evidence attached
- [ ] No sensitive data exposed

### CTF Challenge Guidelines

**Sanitization:**
- Replace production URLs with `challenge.ctf`
- Generate dummy flags
- Remove sensitive business logic
- Create isolated test environments

**Educational Value:**
- Clear learning objectives
- Progressive hints
- Detailed solution writeups
- Real-world relevance

## 📚 References

### Standards & Frameworks
- [CVSS v3.1 Specification](https://www.first.org/cvss/v3.1/specification-document)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Bug Bounty Platforms
- [HackerOne](https://www.hackerone.com/)
- [Bugcrowd](https://www.bugcrowd.com/)
- [Synack](https://www.synack.com/)
- [YesWeHack](https://www.yeswehack.com/)

### CTF Platforms
- [CTFd](https://ctfd.io/)
- [PicoCTF](https://picoctf.org/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

## 📝 Dependencies

```
pydantic>=2.0.0       # Data validation
reportlab>=4.0.0      # PDF generation
pygments>=2.15.0      # Syntax highlighting
pyyaml>=6.0          # YAML support
```

## 🤝 Integration

### INV-082 SwarmBounty

This infrastructure aligns with the INV-082 SwarmBounty specification for:
- Automated vulnerability triage
- Challenge generation pipeline
- Report standardization
- Bounty calculation frameworks

### Strategickhaos Ecosystem

Part of the broader Strategickhaos DAO security initiative:
- Red Team operations
- Security training programs
- Bug bounty management
- CTF competition hosting

## 🎯 Roadmap

- [ ] Automatic report submission to bug bounty platforms
- [ ] Integration with SIEM/EDR systems
- [ ] Vulnerability tracking dashboard
- [ ] Team collaboration features
- [ ] Automated severity assessment with ML
- [ ] CTF platform auto-deployment

## 📄 License

MIT License - Strategickhaos DAO LLC

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Empowering security researchers through automation and education"*

---

**Last Updated**: 2025-12-16  
**Version**: 1.0.0  
**Status**: Production Ready
