#!/usr/bin/env python3
"""
Professional Vulnerability Report PDF Generator (WIP-008)

Generates professional PDF reports from vulnerability data with:
- Company branding placeholders
- Executive summary auto-generation
- Technical details with syntax highlighting
- Charts and visualizations

Dependencies:
- reportlab or weasyprint for PDF generation
- pygments for syntax highlighting

Author: Strategickhaos DAO LLC
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


# Try to import PDF generation libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("Warning: reportlab not installed. Install with: pip install reportlab")
    REPORTLAB_AVAILABLE = False

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    print("Warning: pygments not installed. Install with: pip install pygments")
    PYGMENTS_AVAILABLE = False


class VulnReportPDFGenerator:
    """Generate professional PDF vulnerability reports"""
    
    def __init__(self, company_name: str = "Strategickhaos DAO LLC"):
        """
        Initialize PDF generator.
        
        Args:
            company_name: Company name for branding
        """
        self.company_name = company_name
        self.styles = self._setup_styles() if REPORTLAB_AVAILABLE else None
    
    def _setup_styles(self):
        """Setup custom PDF styles"""
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5282'),
            spaceBefore=20,
            spaceAfter=10,
            borderPadding=5
        ))
        
        styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=styles['Code'],
            fontSize=9,
            leading=12,
            fontName='Courier',
            backColor=colors.HexColor('#f5f5f5'),
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10
        ))
        
        return styles
    
    def generate_executive_summary(self, vuln_data: Dict) -> str:
        """
        Auto-generate executive summary from vulnerability data.
        
        Args:
            vuln_data: Vulnerability report data
        
        Returns:
            Executive summary text
        """
        title = vuln_data.get("title", "Vulnerability")
        severity = vuln_data.get("severity", "unknown").upper()
        cvss = vuln_data.get("cvss_score", 0.0)
        asset = vuln_data.get("asset", {}).get("name", "system")
        
        summary = f"""
This report documents a {severity} severity security vulnerability (CVSS {cvss}) 
identified in {asset}. The vulnerability, classified as "{title}", poses 
significant security risks that require immediate attention.

The issue was discovered through security testing and represents a critical 
security gap that could potentially be exploited by malicious actors. This 
document provides a comprehensive analysis including technical details, 
proof of concept, impact assessment, and remediation recommendations.

Immediate action is recommended to address this vulnerability and prevent 
potential security incidents.
        """.strip()
        
        return summary
    
    def generate_pdf(
        self,
        vuln_data: Dict,
        output_file: str,
        include_logo: bool = True,
        logo_path: Optional[str] = None
    ) -> bool:
        """
        Generate professional PDF report.
        
        Args:
            vuln_data: Vulnerability report data
            output_file: Output PDF file path
            include_logo: Whether to include company logo
            logo_path: Path to company logo image
        
        Returns:
            True if successful, False otherwise
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ reportlab not available. Cannot generate PDF.")
            return False
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Story (content) container
        story = []
        
        # Add logo if available
        if include_logo and logo_path and Path(logo_path).exists():
            try:
                logo = Image(logo_path, 2*inch, 0.5*inch)
                story.append(logo)
                story.append(Spacer(1, 12))
            except:
                pass
        
        # Title page
        story.append(Paragraph(
            f"Security Vulnerability Report",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph(
            f"<b>{vuln_data.get('title', 'Vulnerability Report')}</b>",
            self.styles['Heading1']
        ))
        story.append(Spacer(1, 24))
        
        # Metadata table
        metadata = [
            ['Report ID:', vuln_data.get('report_id', 'N/A')],
            ['Severity:', vuln_data.get('severity', 'N/A').upper()],
            ['CVSS Score:', str(vuln_data.get('cvss_score', 'N/A'))],
            ['Date:', datetime.now().strftime('%Y-%m-%d')],
            ['Submitted By:', vuln_data.get('submitted_by', 'N/A')],
            ['Company:', self.company_name]
        ]
        
        t = Table(metadata, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e6e6e6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t)
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        exec_summary = self.generate_executive_summary(vuln_data)
        story.append(Paragraph(exec_summary, self.styles['ExecutiveSummary']))
        story.append(Spacer(1, 20))
        
        # Vulnerability Classification
        story.append(Paragraph("Vulnerability Classification", self.styles['SectionHeader']))
        classification_data = [
            ['Weakness Type:', vuln_data.get('weakness_type', 'N/A')],
            ['Category:', vuln_data.get('asset', {}).get('type', 'N/A')],
            ['Affected Asset:', vuln_data.get('asset', {}).get('name', 'N/A')],
            ['Environment:', vuln_data.get('asset', {}).get('environment', 'N/A')]
        ]
        
        t = Table(classification_data, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Technical Details
        story.append(Paragraph("Technical Details", self.styles['SectionHeader']))
        tech_details = vuln_data.get('technical_details', 'No technical details provided.')
        story.append(Paragraph(tech_details, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Proof of Concept
        story.append(Paragraph("Proof of Concept", self.styles['SectionHeader']))
        poc = vuln_data.get('proof_of_concept', {})
        poc_desc = poc.get('description', 'No PoC provided.')
        story.append(Paragraph(poc_desc, self.styles['Normal']))
        
        if poc.get('code'):
            story.append(Spacer(1, 10))
            story.append(Paragraph("<b>Code:</b>", self.styles['Normal']))
            code_text = poc.get('code', '')
            # Format code (basic)
            code_para = Paragraph(
                f"<font name='Courier' size='9'>{code_text}</font>",
                self.styles['CodeBlock']
            )
            story.append(code_para)
        
        story.append(Spacer(1, 20))
        
        # Impact Assessment
        story.append(Paragraph("Impact Assessment", self.styles['SectionHeader']))
        impact = vuln_data.get('impact', {})
        
        impact_data = [
            ['Confidentiality:', impact.get('confidentiality_impact', 'N/A')],
            ['Integrity:', impact.get('integrity_impact', 'N/A')],
            ['Availability:', impact.get('availability_impact', 'N/A')],
            ['Business Impact:', impact.get('business_impact', 'N/A')]
        ]
        
        t = Table(impact_data, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff4e6')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Remediation Recommendations
        story.append(Paragraph("Remediation Recommendations", self.styles['SectionHeader']))
        remediation = vuln_data.get('remediation', {})
        
        story.append(Paragraph("<b>Short-term Mitigations:</b>", self.styles['Normal']))
        for i, mitigation in enumerate(remediation.get('short_term', []), 1):
            story.append(Paragraph(f"{i}. {mitigation}", self.styles['Normal']))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Long-term Fixes:</b>", self.styles['Normal']))
        for i, fix in enumerate(remediation.get('long_term', []), 1):
            story.append(Paragraph(f"{i}. {fix}", self.styles['Normal']))
        
        story.append(PageBreak())
        
        # Appendix
        story.append(Paragraph("Appendix", self.styles['SectionHeader']))
        story.append(Paragraph(
            f"This report was generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            f"by {self.company_name}. All information contained in this report is confidential "
            f"and should be treated as sensitive security information.",
            self.styles['Normal']
        ))
        
        # Build PDF
        try:
            doc.build(story)
            print(f"✅ PDF report generated: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return False


def demo():
    """Demonstrate PDF generation"""
    print("\n" + "=" * 70)
    print("PROFESSIONAL VULNERABILITY REPORT PDF GENERATOR")
    print("=" * 70)
    
    # Sample vulnerability data
    sample_vuln = {
        "report_id": "VR-2025-001",
        "title": "SQL Injection in User Search Endpoint",
        "severity": "high",
        "cvss_score": 8.6,
        "weakness_type": "CWE-89: SQL Injection",
        "submitted_by": "Security Researcher",
        "asset": {
            "name": "Main Web Application",
            "type": "web_app",
            "url": "https://example.com",
            "environment": "production"
        },
        "technical_details": (
            "The application fails to properly sanitize user input in the search "
            "parameter, allowing SQL injection attacks. The vulnerability exists in "
            "the search functionality where user-supplied data is directly concatenated "
            "into SQL queries without parameterization or input validation."
        ),
        "proof_of_concept": {
            "description": (
                "1. Navigate to /search endpoint\n"
                "2. Enter payload: ' OR '1'='1\n"
                "3. Observe database error revealing injection point\n"
                "4. Use UNION queries to extract data"
            ),
            "code": "curl 'https://example.com/search?q=%27+OR+%271%27%3D%271'"
        },
        "impact": {
            "confidentiality_impact": "Complete database access to sensitive user data",
            "integrity_impact": "Potential data modification and deletion",
            "availability_impact": "Minimal - no direct DoS impact",
            "business_impact": "Major data breach risk affecting all users, regulatory compliance violations"
        },
        "remediation": {
            "short_term": [
                "Disable search functionality immediately",
                "Implement WAF rules to block SQL injection patterns",
                "Enable query logging for monitoring"
            ],
            "long_term": [
                "Rewrite queries using parameterized statements",
                "Implement comprehensive input validation",
                "Conduct security code review of entire codebase",
                "Provide security training to development team"
            ]
        }
    }
    
    # Generate PDF
    generator = VulnReportPDFGenerator(company_name="Strategickhaos DAO LLC")
    
    output_dir = Path(__file__).parent / "reports"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "sample_vulnerability_report.pdf"
    
    success = generator.generate_pdf(sample_vuln, str(output_file))
    
    if success:
        print(f"\n📄 Sample report available at: {output_file}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo()
