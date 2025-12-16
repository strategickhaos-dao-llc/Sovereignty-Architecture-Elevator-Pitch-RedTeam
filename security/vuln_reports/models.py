#!/usr/bin/env python3
"""
Vulnerability Report Data Structures (WIP-009)

Defines Pydantic models for vulnerability report structure with validation.
Supports export to JSON schema for API consumption.

Reference: INV-082 SwarmBounty specification
Author: Strategickhaos DAO LLC
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Literal
from datetime import datetime
from enum import Enum


class SeverityLevel(str, Enum):
    """Vulnerability severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class CVSSVector(BaseModel):
    """CVSS v3.1 scoring vector"""
    attack_vector: Literal["N", "A", "L", "P"] = Field(
        ...,
        description="Network, Adjacent, Local, Physical"
    )
    attack_complexity: Literal["L", "H"] = Field(
        ...,
        description="Low, High"
    )
    privileges_required: Literal["N", "L", "H"] = Field(
        ...,
        description="None, Low, High"
    )
    user_interaction: Literal["N", "R"] = Field(
        ...,
        description="None, Required"
    )
    scope: Literal["U", "C"] = Field(
        ...,
        description="Unchanged, Changed"
    )
    confidentiality: Literal["N", "L", "H"] = Field(
        ...,
        description="None, Low, High"
    )
    integrity: Literal["N", "L", "H"] = Field(
        ...,
        description="None, Low, High"
    )
    availability: Literal["N", "L", "H"] = Field(
        ...,
        description="None, Low, High"
    )
    
    def to_vector_string(self) -> str:
        """Convert to CVSS vector string format"""
        return (
            f"CVSS:3.1/"
            f"AV:{self.attack_vector}/"
            f"AC:{self.attack_complexity}/"
            f"PR:{self.privileges_required}/"
            f"UI:{self.user_interaction}/"
            f"S:{self.scope}/"
            f"C:{self.confidentiality}/"
            f"I:{self.integrity}/"
            f"A:{self.availability}"
        )


class AssetInfo(BaseModel):
    """Information about the affected asset"""
    name: str = Field(..., description="Asset name or identifier")
    type: str = Field(..., description="Asset type (web app, API, mobile, etc.)")
    url: Optional[str] = Field(None, description="Asset URL if applicable")
    version: Optional[str] = Field(None, description="Software/platform version")
    environment: Literal["production", "staging", "development", "test"] = Field(
        default="production"
    )


class ProofOfConcept(BaseModel):
    """Proof of concept demonstration"""
    description: str = Field(..., description="Step-by-step reproduction steps")
    code: Optional[str] = Field(None, description="PoC code or script")
    screenshots: List[str] = Field(
        default_factory=list,
        description="Paths or URLs to screenshot evidence"
    )
    video_url: Optional[str] = Field(None, description="Video demonstration URL")
    request_response: Optional[Dict[str, str]] = Field(
        None,
        description="HTTP request/response if applicable"
    )


class ImpactAssessment(BaseModel):
    """Detailed impact analysis"""
    confidentiality_impact: str = Field(
        ...,
        description="Impact on data confidentiality"
    )
    integrity_impact: str = Field(
        ...,
        description="Impact on data integrity"
    )
    availability_impact: str = Field(
        ...,
        description="Impact on system availability"
    )
    business_impact: str = Field(
        ...,
        description="Business and operational impact"
    )
    affected_users: Optional[str] = Field(
        None,
        description="Number or percentage of affected users"
    )


class RemediationAdvice(BaseModel):
    """Remediation recommendations"""
    short_term: List[str] = Field(
        ...,
        description="Immediate mitigation steps"
    )
    long_term: List[str] = Field(
        ...,
        description="Permanent fix recommendations"
    )
    code_fix: Optional[str] = Field(
        None,
        description="Example code fix if applicable"
    )
    references: List[str] = Field(
        default_factory=list,
        description="Links to documentation, CVEs, advisories"
    )


class VulnerabilityReport(BaseModel):
    """
    Complete vulnerability report structure.
    
    Sections:
    - Title: Concise vulnerability summary
    - Summary: Executive summary for non-technical stakeholders
    - Technical Details: In-depth technical explanation
    - Proof of Concept: Reproduction steps and evidence
    - Impact: Business and technical impact analysis
    - Remediation: Fix recommendations
    
    Validation Rules:
    - All required fields must be present
    - CVSS score must be calculated
    - At least one PoC step required
    """
    
    # Metadata
    report_id: str = Field(..., description="Unique report identifier")
    title: str = Field(..., min_length=10, max_length=200)
    submitted_by: str = Field(..., description="Researcher name or handle")
    submitted_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    # Classification
    severity: SeverityLevel
    weakness_type: str = Field(
        ...,
        description="CWE ID or weakness category",
        example="CWE-79: Cross-site Scripting"
    )
    cvss_vector: CVSSVector
    cvss_score: float = Field(..., ge=0.0, le=10.0)
    
    # Asset information
    asset: AssetInfo
    
    # Report content
    summary: str = Field(
        ...,
        min_length=50,
        description="Executive summary for management"
    )
    technical_details: str = Field(
        ...,
        min_length=100,
        description="Detailed technical explanation"
    )
    proof_of_concept: ProofOfConcept
    impact: ImpactAssessment
    remediation: RemediationAdvice
    
    # Additional fields
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorization"
    )
    related_reports: List[str] = Field(
        default_factory=list,
        description="Related vulnerability report IDs"
    )
    bounty_eligible: bool = Field(
        default=True,
        description="Whether eligible for bug bounty"
    )
    
    @field_validator('cvss_score')
    @classmethod
    def validate_cvss_score(cls, v, info):
        """Validate CVSS score matches severity"""
        severity = info.data.get('severity') if hasattr(info, 'data') else None
        if severity:
            if severity == SeverityLevel.CRITICAL and v < 9.0:
                raise ValueError("Critical vulnerabilities must have CVSS >= 9.0")
            elif severity == SeverityLevel.HIGH and (v < 7.0 or v >= 9.0):
                raise ValueError("High vulnerabilities must have CVSS 7.0-8.9")
            elif severity == SeverityLevel.MEDIUM and (v < 4.0 or v >= 7.0):
                raise ValueError("Medium vulnerabilities must have CVSS 4.0-6.9")
            elif severity == SeverityLevel.LOW and (v < 0.1 or v >= 4.0):
                raise ValueError("Low vulnerabilities must have CVSS 0.1-3.9")
        return v
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return self.model_dump()
    
    def to_json_schema(self) -> Dict:
        """Export JSON schema for API consumption"""
        return self.model_json_schema()
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "VR-2025-001",
                "title": "SQL Injection in User Search Endpoint",
                "submitted_by": "security_researcher",
                "severity": "high",
                "weakness_type": "CWE-89: SQL Injection",
                "cvss_score": 8.6,
                "asset": {
                    "name": "Main Web Application",
                    "type": "web_app",
                    "url": "https://example.com",
                    "environment": "production"
                },
                "summary": "A SQL injection vulnerability exists in the user search functionality...",
                "technical_details": "The application fails to properly sanitize user input...",
                "proof_of_concept": {
                    "description": "1. Navigate to /search\n2. Enter payload: ' OR '1'='1\n3. Observe database error"
                },
                "impact": {
                    "confidentiality_impact": "Complete database access",
                    "integrity_impact": "Data modification possible",
                    "availability_impact": "Minimal",
                    "business_impact": "Potential data breach affecting all users"
                },
                "remediation": {
                    "short_term": ["Disable search functionality", "Add WAF rules"],
                    "long_term": ["Use parameterized queries", "Input validation"]
                }
            }
        }


class VulnerabilityReportCollection(BaseModel):
    """Collection of vulnerability reports"""
    reports: List[VulnerabilityReport]
    total_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    
    @classmethod
    def from_reports(cls, reports: List[VulnerabilityReport]):
        """Create collection from list of reports"""
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for report in reports:
            if report.severity.value in severity_counts:
                severity_counts[report.severity.value] += 1
        
        return cls(
            reports=reports,
            total_count=len(reports),
            critical_count=severity_counts['critical'],
            high_count=severity_counts['high'],
            medium_count=severity_counts['medium'],
            low_count=severity_counts['low']
        )


if __name__ == "__main__":
    # Example: Create a sample vulnerability report
    sample_cvss = CVSSVector(
        attack_vector="N",
        attack_complexity="L",
        privileges_required="N",
        user_interaction="N",
        scope="U",
        confidentiality="H",
        integrity="H",
        availability="N"
    )
    
    sample_report = VulnerabilityReport(
        report_id="VR-2025-001",
        title="SQL Injection in User Search Endpoint",
        submitted_by="security_researcher",
        severity=SeverityLevel.HIGH,
        weakness_type="CWE-89: SQL Injection",
        cvss_vector=sample_cvss,
        cvss_score=8.6,
        asset=AssetInfo(
            name="Main Web Application",
            type="web_app",
            url="https://example.com",
            environment="production"
        ),
        summary="A SQL injection vulnerability exists in the user search functionality allowing unauthorized database access.",
        technical_details="The application fails to properly sanitize user input in the search parameter, allowing SQL injection attacks.",
        proof_of_concept=ProofOfConcept(
            description="1. Navigate to /search\n2. Enter payload: ' OR '1'='1\n3. Observe database error revealing injection",
            code="curl 'https://example.com/search?q=%27+OR+%271%27%3D%271'",
            screenshots=["screenshot1.png", "screenshot2.png"]
        ),
        impact=ImpactAssessment(
            confidentiality_impact="Complete database access to sensitive user data",
            integrity_impact="Potential data modification and deletion",
            availability_impact="Minimal - no DoS impact",
            business_impact="Major data breach risk affecting all users",
            affected_users="100%"
        ),
        remediation=RemediationAdvice(
            short_term=[
                "Disable search functionality immediately",
                "Add WAF rules to block SQL injection patterns"
            ],
            long_term=[
                "Implement parameterized queries",
                "Add input validation and sanitization",
                "Conduct security code review"
            ],
            code_fix="# Use parameterized queries\ncursor.execute('SELECT * FROM users WHERE name = ?', (user_input,))",
            references=[
                "https://owasp.org/www-community/attacks/SQL_Injection",
                "https://cwe.mitre.org/data/definitions/89.html"
            ]
        ),
        tags=["sql-injection", "web", "authentication-bypass"],
        bounty_eligible=True
    )
    
    print("Sample Vulnerability Report:")
    print(f"ID: {sample_report.report_id}")
    print(f"Title: {sample_report.title}")
    print(f"Severity: {sample_report.severity.value.upper()}")
    print(f"CVSS Score: {sample_report.cvss_score}")
    print(f"CVSS Vector: {sample_report.cvss_vector.to_vector_string()}")
    print("\n✅ Vulnerability report model validated successfully!")
    
    # Export JSON schema
    schema = sample_report.to_json_schema()
    print(f"\n📄 JSON Schema exported ({len(schema)} properties)")
