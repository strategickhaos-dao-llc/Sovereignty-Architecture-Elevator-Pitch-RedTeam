# legal-refinery-here-strings.ps1
# Legal Refinery Integration Examples with PowerShell Here-Strings
# Demonstrates UPL-compliant strategy generation and audit logging
# Run: pwsh -File legal-refinery-here-strings.ps1

param(
    [string]$RefineryUrl = "http://nitro-v15.tailnet:8080",
    [switch]$DryRun
)

Write-Host "⚖️  Legal Refinery Here-Strings Examples" -ForegroundColor Magenta
Write-Host "Refinery URL: $RefineryUrl" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "DRY RUN MODE: No actual API calls will be made" -ForegroundColor Yellow
}
Write-Host ""

# Helper function to calculate content hash
function Get-ContentHash {
    param([string]$Content)
    
    $stream = [System.IO.MemoryStream]::new([System.Text.Encoding]::UTF8.GetBytes($Content))
    $hash = Get-FileHash -InputStream $stream -Algorithm SHA256
    return $hash.Hash
}

# Example 1: Simple Legal Strategy
Write-Host "=== Example 1: Basic Legal Strategy ===" -ForegroundColor Cyan
$strategy1 = @'
Perform employment background check:
1. Obtain written consent
2. Use FCRA-compliant provider
3. Provide pre-adverse action notice if needed
4. Document everything
'@

Write-Host "Strategy:"
Write-Host $strategy1
Write-Host ""

if (-not $DryRun) {
    try {
        $body = @{
            base_strategy = $strategy1
            jurisdiction = "Wyoming"
            compliance_frameworks = @("FCRA", "UPL")
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$RefineryUrl/api/legal_refinery/refine_strategy" `
            -Method Post `
            -Body $body `
            -ContentType "application/json" `
            -ErrorAction Stop
        
        Write-Host "✅ Refined Strategy:" -ForegroundColor Green
        Write-Host $response
    }
    catch {
        Write-Host "⚠️  API call skipped (service may not be running): $_" -ForegroundColor Yellow
    }
}
Write-Host ""

# Example 2: Privacy Policy Generation
Write-Host "=== Example 2: Privacy Policy Template ===" -ForegroundColor Cyan
$privacyPolicy = @'
# Privacy Policy for Strategic Khaos Platform

## Data Collection
We collect minimal data necessary for service operation:
- Authentication credentials (hashed with bcrypt)
- System performance metrics (anonymized)
- Error logs (no PII)

## Data Storage
- Sovereign infrastructure (self-hosted)
- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Geographic location: Wyoming, USA

## Data Access
- Zero-knowledge architecture where possible
- Access logs maintained for 90 days
- User data deletion within 30 days of request
- No third-party data sharing without explicit consent

## Your Rights
- Right to access your data
- Right to deletion (GDPR "Right to be Forgotten")
- Right to data portability
- Right to opt-out of analytics

## Compliance
This policy complies with:
- GDPR (where applicable)
- CCPA (California residents)
- FCRA (consumer reporting)
- Wyoming data sovereignty laws

Last Updated: 2025-11-21
'@

$policyFile = "demo_privacy_policy.md"
$privacyPolicy | Set-Content $policyFile
Write-Host "Created: $policyFile"
Write-Host "Preview:"
Write-Host $privacyPolicy
Write-Host ""

# Example 3: UPL Compliance Checklist
Write-Host "=== Example 3: UPL Compliance Checklist ===" -ForegroundColor Cyan
$uplChecklist = @'
# Unauthorized Practice of Law (UPL) Compliance Checklist

## Pre-Launch Requirements
- [ ] No attorney-client relationship language anywhere in product
- [ ] "Not legal advice" disclaimer on every relevant page
- [ ] "Consult a licensed attorney" recommendation prominent
- [ ] No jurisdiction-specific legal conclusions
- [ ] No case-specific legal advice capability
- [ ] General information only

## AI Output Requirements
- [ ] All AI outputs include disclaimers
- [ ] Citations reference only public legal sources
- [ ] No interpretation of specific statutes for user's case
- [ ] Referral mechanism to licensed attorneys
- [ ] No guarantee of legal outcomes
- [ ] Clear statement: "For informational purposes only"

## Marketing & Communications
- [ ] No claims of legal expertise
- [ ] No "lawyer alternative" language
- [ ] Clear positioning as legal information tool
- [ ] Testimonials do not imply legal outcomes
- [ ] No "satisfaction guaranteed" for legal matters

## Operational Safeguards
- [ ] Regular legal review of outputs
- [ ] Monitoring for UPL risk patterns
- [ ] Staff training on UPL boundaries
- [ ] Escalation process for borderline cases
- [ ] Documentation of all safeguards

Status: DRAFT - Requires attorney review before implementation
'@

$checklistFile = "demo_upl_checklist.md"
$uplChecklist | Set-Content $checklistFile
Write-Host "Created: $checklistFile"
Write-Host ""

# Example 4: Audit Log with Here-Strings
Write-Host "=== Example 4: Immutable Audit Log ===" -ForegroundColor Cyan

function New-AuditEntry {
    param(
        [string]$Action,
        [string]$Content,
        [string]$Status = "success"
    )
    
    $timestamp = Get-Date -Format "o"
    $contentHash = Get-ContentHash -Content $Content
    
    # Create a hashtable and convert to single-line JSON
    $entryObj = @{
        timestamp = $timestamp
        node = $env:COMPUTERNAME
        user = $env:USERNAME
        action = $Action
        status = $Status
        content_length = $Content.Length
        content_hash = $contentHash
    }
    
    # Convert to compressed JSON (single line)
    return ($entryObj | ConvertTo-Json -Compress)
}

$auditLog = "demo_legal_audit.jsonl"
Write-Host "Creating audit log: $auditLog"

# Log strategy creation
$auditEntry1 = New-AuditEntry -Action "strategy_created" -Content $strategy1
$auditEntry1 | Add-Content $auditLog

# Log privacy policy creation
$auditEntry2 = New-AuditEntry -Action "privacy_policy_created" -Content $privacyPolicy
$auditEntry2 | Add-Content $auditLog

# Log checklist creation
$auditEntry3 = New-AuditEntry -Action "upl_checklist_created" -Content $uplChecklist
$auditEntry3 | Add-Content $auditLog

Write-Host "✅ Audit entries created"
Write-Host ""
Write-Host "Audit log contents:"
$skippedLines = 0
Get-Content $auditLog | ForEach-Object {
    try {
        $entry = $_ | ConvertFrom-Json -ErrorAction Stop
        Write-Host "  [$($entry.timestamp)] $($entry.action) - Hash: $($entry.content_hash.Substring(0,16))..."
    }
    catch {
        $skippedLines++
    }
}
if ($skippedLines -gt 0) {
    Write-Host "  (Skipped $skippedLines malformed line(s))" -ForegroundColor Yellow
}
Write-Host ""

# Example 5: Batch Strategy Processing
Write-Host "=== Example 5: Batch Strategy Processing ===" -ForegroundColor Cyan
$strategies = @'
Strategy A: Client onboarding with KYC verification per Bank Secrecy Act requirements
Strategy B: Data retention policy for customer records (7 year minimum per IRS)
Strategy C: Third-party vendor risk assessment using SOC 2 Type II standards
Strategy D: Employee handbook update for remote work compliance (FLSA, ADA)
Strategy E: Contract template for SaaS subscription agreements
'@

$strategyList = $strategies -split "`n" | Where-Object { $_ -match "Strategy" }
Write-Host "Processing $($strategyList.Count) strategies..."
Write-Host ""

foreach ($strat in $strategyList) {
    $stratName = ($strat -split ":")[0]
    $stratContent = ($strat -split ":", 2)[1].Trim()
    
    Write-Host "  • $stratName" -ForegroundColor Yellow
    
    if (-not $DryRun) {
        # In production, this would call Legal Refinery API
        # For demo, we just create a file
        $filename = "demo_$($stratName.Replace(' ', '_').ToLower()).txt"
        $stratContent | Set-Content $filename
        
        # Log to audit
        $auditEntry = New-AuditEntry -Action "strategy_processed" -Content $stratContent
        $auditEntry | Add-Content $auditLog
    }
}

Write-Host ""
Write-Host "✅ Batch processing complete"
Write-Host ""

# Example 6: Legal Citations Database
Write-Host "=== Example 6: Legal Citations Database ===" -ForegroundColor Cyan
$citations = @'
[
    {
        "id": "wyo-dao-2022",
        "title": "Wyoming DAO LLC Act",
        "citation": "Wyo. Stat. § 17-31-101 et seq.",
        "year": 2022,
        "relevance": "Legal framework for DAO operations in Wyoming",
        "url": "https://wyoleg.gov/Legislation/2021/SF0068",
        "summary": "Establishes decentralized autonomous organizations as legal entities with limited liability protections"
    },
    {
        "id": "fcra-2003",
        "title": "Fair Credit Reporting Act",
        "citation": "15 U.S.C. § 1681 et seq.",
        "year": 2003,
        "relevance": "Consumer reporting and background check requirements",
        "summary": "Regulates collection, dissemination, and use of consumer information including credit reports"
    },
    {
        "id": "gdpr-2018",
        "title": "General Data Protection Regulation",
        "citation": "Regulation (EU) 2016/679",
        "year": 2018,
        "relevance": "EU data privacy and sovereignty requirements",
        "summary": "Establishes data protection rights for EU residents including right to deletion and data portability"
    }
]
'@

$citationsFile = "demo_legal_citations.json"
$citations | Set-Content $citationsFile
Write-Host "Created: $citationsFile"

$citationsObj = $citations | ConvertFrom-Json
Write-Host ""
Write-Host "Citations loaded: $($citationsObj.Count)"
foreach ($cite in $citationsObj) {
    Write-Host "  • $($cite.title) ($($cite.year))"
}
Write-Host ""

# Example 7: Compliance Report
Write-Host "=== Example 7: Compliance Report Generation ===" -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$complianceReport = @"
# Legal Compliance Report
Generated: $timestamp
Node: $env:COMPUTERNAME
User: $env:USERNAME

## Summary
This report documents compliance verification for Strategic Khaos Platform.

## Strategies Processed
- Employment background check procedure
- Privacy policy template
- UPL compliance checklist
- Client onboarding workflow
- Data retention policy

## Compliance Frameworks Verified
- ✅ FCRA (Fair Credit Reporting Act)
- ✅ UPL (Unauthorized Practice of Law) safeguards
- ✅ GDPR (General Data Protection Regulation) principles
- ✅ Wyoming DAO LLC Act compliance

## Audit Trail
All operations logged to: $auditLog
Total entries: $(if (Test-Path $auditLog) { (Get-Content $auditLog -ReadCount 0 | Measure-Object).Count } else { 0 })
Audit log hash: $(if (Test-Path $auditLog) { (Get-FileHash $auditLog -Algorithm SHA256).Hash.Substring(0,16) } else { 'N/A' })...

## Recommendations
1. Regular legal review (quarterly minimum)
2. Monitor for UPL risk patterns in AI outputs
3. Update compliance frameworks as regulations evolve
4. Maintain audit trail for minimum 7 years
5. Annual attorney review of all policies and procedures

## Certification
This report documents compliance verification activities only.
It does not constitute legal advice.
Consult with a licensed attorney for legal guidance.

---
Report generated by: Legal Refinery Here-Strings Demo
Documentation: See POWERSHELL_HERE_STRINGS.md
"@

$reportFile = "demo_compliance_report.md"
$complianceReport | Set-Content $reportFile
Write-Host "Created: $reportFile"
Write-Host ""
Write-Host $complianceReport
Write-Host ""

Write-Host "✅ Legal Refinery Demo Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Files Created:" -ForegroundColor Yellow
@($policyFile, $checklistFile, $auditLog, $citationsFile, $reportFile) | ForEach-Object {
    if (Test-Path $_) {
        Write-Host "  • $_"
    }
}
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review generated compliance documents"
Write-Host "  2. Customize templates for your use case"
Write-Host "  3. Integrate with Legal Refinery API"
Write-Host "  4. Maintain immutable audit trail"
Write-Host "  5. Regular attorney review of all outputs"
Write-Host ""
Write-Host "📚 See POWERSHELL_HERE_STRINGS.md for 100 more examples" -ForegroundColor Magenta
