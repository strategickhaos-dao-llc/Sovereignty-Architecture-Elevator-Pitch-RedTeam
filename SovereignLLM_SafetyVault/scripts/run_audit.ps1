#!/usr/bin/env pwsh
<#
.SYNOPSIS
    LLM Safety Audit Runner - PowerShell Version
    
.DESCRIPTION
    Interactive script to conduct a comprehensive LLM safety audit based on the 100-point framework.
    Generates client-specific audit reports and evidence vault.
    
.PARAMETER ClientName
    Name of the client organization
    
.PARAMETER OutputDir
    Directory to store audit results (default: ../clients/<ClientName>)
    
.PARAMETER Interactive
    Run in interactive mode (default: true)
    
.EXAMPLE
    .\run_audit.ps1 -ClientName "Acme Corp" -Interactive $true
    
.NOTES
    Version: 1.0
    Author: Strategickhaos Sovereignty Architecture
    Part of: Sovereign LLM Safety & Evidence Vault
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ClientName = "",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "",
    
    [Parameter(Mandatory=$false)]
    [bool]$Interactive = $true
)

# Color output functions
function Write-Header {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[i] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[✗] $Message" -ForegroundColor Red
}

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Split-Path -Parent $ScriptDir

# Banner
Clear-Host
Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║   Sovereign LLM Safety & Evidence Vault - Audit Runner        ║
║   Version 1.0                                                  ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Gather client information
if ($Interactive -and -not $ClientName) {
    Write-Header "Client Information"
    $ClientName = Read-Host "Enter client name"
}

if (-not $ClientName) {
    Write-Error "Client name is required. Use -ClientName parameter or run in interactive mode."
    exit 1
}

# Generate engagement ID
$EngagementID = "ENG-$(Get-Date -Format 'yyyyMMdd')-$($ClientName -replace '[^a-zA-Z0-9]', '')"
$EngagementID = $EngagementID.Substring(0, [Math]::Min($EngagementID.Length, 30))

Write-Success "Engagement ID: $EngagementID"

# Setup output directory
if (-not $OutputDir) {
    $OutputDir = Join-Path $VaultRoot "clients" $ClientName
}

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Success "Created output directory: $OutputDir"
}

# Create subdirectories
$DocsDir = Join-Path $OutputDir "docs"
$ComplianceDir = Join-Path $DocsDir "compliance"
$PatentDir = Join-Path $DocsDir "patent"

@($DocsDir, $ComplianceDir, $PatentDir) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Collect client information
Write-Header "Collecting Client Information"

$ClientInfo = @{
    Name = $ClientName
    EngagementID = $EngagementID
    AuditDate = Get-Date -Format "yyyy-MM-dd"
    Auditor = "Strategickhaos Sovereignty Architecture"
}

if ($Interactive) {
    $ClientInfo.PrimaryContact = Read-Host "Primary contact name (press Enter to skip)"
    $ClientInfo.ContactEmail = Read-Host "Contact email (press Enter to skip)"
    $ClientInfo.SystemDescription = Read-Host "Brief system description (press Enter to skip)"
    
    Write-Info "`nLLM Provider(s) - Select all that apply (comma-separated numbers):"
    Write-Host "1. OpenAI"
    Write-Host "2. Anthropic"
    Write-Host "3. Local/Open Source"
    Write-Host "4. Azure OpenAI"
    Write-Host "5. Other"
    $providerChoice = Read-Host "Selection"
    $ClientInfo.LLMProviders = $providerChoice
    
    Write-Info "`nDeployment Type:"
    Write-Host "1. Cloud"
    Write-Host "2. On-Premises"
    Write-Host "3. Hybrid"
    Write-Host "4. Edge"
    $ClientInfo.DeploymentType = Read-Host "Selection"
    
    Write-Info "`nData Sensitivity Level:"
    Write-Host "1. Public"
    Write-Host "2. Internal"
    Write-Host "3. Confidential"
    Write-Host "4. Regulated"
    $ClientInfo.DataSensitivity = Read-Host "Selection"
}

# Copy templates
Write-Header "Preparing Audit Documents"

$TemplateChecklistPath = Join-Path $VaultRoot "docs" "compliance" "AUDIT_CHECKLIST_TEMPLATE.md"
$ClientChecklistPath = Join-Path $ComplianceDir "AUDIT_RESULTS_${ClientName}.md"

if (Test-Path $TemplateChecklistPath) {
    Copy-Item $TemplateChecklistPath $ClientChecklistPath -Force
    
    # Replace placeholders in the checklist
    $content = Get-Content $ClientChecklistPath -Raw
    $content = $content -replace '\[CLIENT_NAME\]', $ClientName
    $content = $content -replace '\[ENGAGEMENT_ID\]', $EngagementID
    $content = $content -replace '\[DATE\]', (Get-Date -Format "yyyy-MM-dd")
    Set-Content -Path $ClientChecklistPath -Value $content
    
    Write-Success "Created audit checklist: $ClientChecklistPath"
} else {
    Write-Error "Template checklist not found at: $TemplateChecklistPath"
}

# Copy safety techniques reference
$SafetyTechPath = Join-Path $VaultRoot "docs" "compliance" "100_llm_safety_techniques.md"
$ClientSafetyPath = Join-Path $ComplianceDir "100_llm_safety_techniques.md"

if (Test-Path $SafetyTechPath) {
    Copy-Item $SafetyTechPath $ClientSafetyPath -Force
    Write-Success "Copied safety techniques reference"
}

# Copy patent template
$PatentTemplatePath = Join-Path $VaultRoot "docs" "patent" "APPENDIX_B_SAFETY_TEMPLATE.md"
$ClientPatentPath = Join-Path $PatentDir "APPENDIX_B_SAFETY_${ClientName}.md"

if (Test-Path $PatentTemplatePath) {
    Copy-Item $PatentTemplatePath $ClientPatentPath -Force
    
    # Replace placeholders
    $content = Get-Content $ClientPatentPath -Raw
    $content = $content -replace '\[CLIENT_NAME\]', $ClientName
    $content = $content -replace '\[DATE\]', (Get-Date -Format "yyyy-MM-dd")
    Set-Content -Path $ClientPatentPath -Value $content
    
    Write-Success "Created patent documentation template"
}

# Create README for client
$ClientReadmePath = Join-Path $OutputDir "README.md"
$readmeContent = @"
# LLM Safety Audit - $ClientName

**Engagement ID**: $EngagementID  
**Audit Date**: $(Get-Date -Format "yyyy-MM-dd")  
**Auditor**: Strategickhaos Sovereignty Architecture

---

## Audit Package Contents

This directory contains your complete LLM Safety & Evidence Vault:

### 📋 Compliance Documentation
- **docs/compliance/AUDIT_RESULTS_${ClientName}.md** - Your completed 100-point safety audit
- **docs/compliance/100_llm_safety_techniques.md** - Complete safety framework reference

### 📄 Patent & IP Documentation
- **docs/patent/APPENDIX_B_SAFETY_${ClientName}.md** - Technical specifications for patent/IP use

### 📊 Dashboards & Monitoring (if applicable)
- Grafana dashboard configurations
- Alert rule templates
- Monitoring setup guides

---

## Next Steps

1. **Review the Audit Results**: Open `docs/compliance/AUDIT_RESULTS_${ClientName}.md`
2. **Prioritize Findings**: Focus on Critical and High priority items first
3. **Implement Remediations**: Follow the 30/60/90 day roadmap
4. **Re-audit**: Schedule follow-up assessment after remediation

---

## Using This Documentation

### For Investors & Due Diligence
- Share the audit results as evidence of security posture
- Highlight improvements made since initial assessment
- Demonstrate commitment to LLM safety

### For Compliance & Legal
- Use as supporting evidence for regulatory compliance
- Include in SOC 2, ISO 27001, or other certification processes
- Provide to legal counsel for risk assessment

### For Patent Applications
- Customize the Appendix B template with your specific implementations
- Review with patent counsel before filing
- Document novel safety innovations

---

## Support

For questions or follow-up engagements:
- **Email**: contact@strategickhaos.com
- **Documentation**: See included framework documents
- **Re-audit**: Contact us for quarterly or annual re-assessments

---

**Confidential & Proprietary**  
This audit package is confidential to $ClientName and Strategickhaos Sovereignty Architecture.  
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

Set-Content -Path $ClientReadmePath -Value $readmeContent
Write-Success "Created client README"

# Generate metadata file
$MetadataPath = Join-Path $OutputDir "audit_metadata.json"
$metadata = $ClientInfo | ConvertTo-Json -Depth 10
Set-Content -Path $MetadataPath -Value $metadata
Write-Success "Saved audit metadata"

# Final summary
Write-Header "Audit Preparation Complete"
Write-Host ""
Write-Success "Client vault created at: $OutputDir"
Write-Info "Next steps:"
Write-Host "  1. Complete the audit checklist: $ClientChecklistPath"
Write-Host "  2. Review findings with client"
Write-Host "  3. Generate final report using generate_report.py"
Write-Host "  4. Deliver evidence vault to client"
Write-Host ""

if ($Interactive) {
    Write-Host "Press any key to open the audit checklist..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Try to open the checklist in default editor
    if ($IsWindows -or $PSVersionTable.PSVersion.Major -lt 6) {
        Start-Process $ClientChecklistPath
    } else {
        # Linux/Mac
        if (Get-Command code -ErrorAction SilentlyContinue) {
            code $ClientChecklistPath
        } elseif (Get-Command vim -ErrorAction SilentlyContinue) {
            vim $ClientChecklistPath
        } else {
            Write-Info "Open this file manually: $ClientChecklistPath"
        }
    }
}

Write-Host ""
Write-Success "Audit runner completed successfully!"
Write-Host ""
