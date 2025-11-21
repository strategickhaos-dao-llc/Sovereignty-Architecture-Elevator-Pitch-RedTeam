"""
Legends of Minds - Legal Compliance Module
Multi-jurisdiction legal compliance checking with 30+ laws
"""

import logging
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


class JurisdictionType(str, Enum):
    """Supported jurisdictions"""
    FEDERAL_US = "federal_us"
    WYOMING = "wyoming"
    CALIFORNIA = "california"
    DELAWARE = "delaware"
    EU = "european_union"
    UK = "united_kingdom"


class ComplianceCategory(str, Enum):
    """Compliance categories"""
    DAO = "dao"
    INTELLECTUAL_PROPERTY = "ip"
    MARKETING = "marketing"
    PRIVACY = "privacy"
    SECURITIES = "securities"
    TAX = "tax"
    EMPLOYMENT = "employment"
    DATA_PROTECTION = "data_protection"
    ACCESSIBILITY = "accessibility"
    CONSUMER_PROTECTION = "consumer_protection"


@dataclass
class ComplianceLaw:
    """Legal compliance law definition"""
    id: str
    name: str
    jurisdiction: JurisdictionType
    category: ComplianceCategory
    description: str
    requirements: List[str]
    penalties: str
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "jurisdiction": self.jurisdiction.value,
            "category": self.category.value,
            "description": self.description,
            "requirements": self.requirements,
            "penalties": self.penalties
        }


class LegalComplianceChecker:
    """Multi-jurisdiction legal compliance checker"""
    
    def __init__(self):
        self.laws = self._initialize_laws()
        logger.info(f"Initialized {len(self.laws)} compliance laws")
    
    def _initialize_laws(self) -> List[ComplianceLaw]:
        """Initialize 30+ legal compliance laws"""
        
        return [
            # DAO Laws
            ComplianceLaw(
                id="wy_sf0068",
                name="Wyoming SF0068 - DAO Supplement",
                jurisdiction=JurisdictionType.WYOMING,
                category=ComplianceCategory.DAO,
                description="Wyoming DAO LLC statute enabling blockchain-based organizations",
                requirements=[
                    "File articles of organization with Wyoming SOS",
                    "Designate as DAO in formation documents",
                    "Maintain smart contract governance",
                    "Annual report filing requirement"
                ],
                penalties="Administrative dissolution, loss of DAO status"
            ),
            ComplianceLaw(
                id="wy_llc_act",
                name="Wyoming LLC Act (Title 17)",
                jurisdiction=JurisdictionType.WYOMING,
                category=ComplianceCategory.DAO,
                description="General LLC provisions applicable to DAOs",
                requirements=[
                    "Operating agreement (on-chain or off-chain)",
                    "Registered agent in Wyoming",
                    "Annual license tax payment",
                    "Good standing maintenance"
                ],
                penalties="Loss of limited liability protection"
            ),
            
            # Federal Privacy Laws
            ComplianceLaw(
                id="us_privacy_act",
                name="Privacy Act of 1974",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Federal law governing collection and use of personal information",
                requirements=[
                    "Notice of information collection",
                    "Individual access rights",
                    "Security safeguards",
                    "Records management"
                ],
                penalties="Civil penalties up to $5,000 per violation"
            ),
            ComplianceLaw(
                id="us_coppa",
                name="Children's Online Privacy Protection Act (COPPA)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Protection of children's online privacy",
                requirements=[
                    "Parental consent for children under 13",
                    "Privacy policy disclosure",
                    "Data security measures",
                    "Limited data collection"
                ],
                penalties="Civil penalties up to $43,280 per violation"
            ),
            
            # Data Protection
            ComplianceLaw(
                id="eu_gdpr",
                name="General Data Protection Regulation (GDPR)",
                jurisdiction=JurisdictionType.EU,
                category=ComplianceCategory.DATA_PROTECTION,
                description="EU comprehensive data protection law",
                requirements=[
                    "Lawful basis for processing",
                    "Data subject rights (access, erasure, portability)",
                    "Data breach notification (72 hours)",
                    "Privacy by design and default",
                    "DPO appointment (if required)"
                ],
                penalties="Up to €20 million or 4% of global revenue"
            ),
            ComplianceLaw(
                id="ca_ccpa",
                name="California Consumer Privacy Act (CCPA)",
                jurisdiction=JurisdictionType.CALIFORNIA,
                category=ComplianceCategory.PRIVACY,
                description="California consumer privacy rights",
                requirements=[
                    "Privacy notice at collection",
                    "Right to know, delete, opt-out",
                    "Do not sell my personal information",
                    "Non-discrimination"
                ],
                penalties="Statutory damages $100-$750 per incident"
            ),
            ComplianceLaw(
                id="ca_cpra",
                name="California Privacy Rights Act (CPRA)",
                jurisdiction=JurisdictionType.CALIFORNIA,
                category=ComplianceCategory.PRIVACY,
                description="Enhanced California privacy law (CCPA 2.0)",
                requirements=[
                    "Data minimization",
                    "Purpose limitation",
                    "Sensitive personal information controls",
                    "Automated decision-making disclosures"
                ],
                penalties="Up to $7,500 per intentional violation"
            ),
            
            # Intellectual Property
            ComplianceLaw(
                id="us_copyright_act",
                name="Copyright Act of 1976",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                description="Federal copyright protection",
                requirements=[
                    "Copyright notice (recommended)",
                    "Registration for enforcement",
                    "DMCA compliance",
                    "Fair use consideration"
                ],
                penalties="Statutory damages up to $150,000 per work"
            ),
            ComplianceLaw(
                id="us_dmca",
                name="Digital Millennium Copyright Act (DMCA)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                description="Digital copyright protections",
                requirements=[
                    "DMCA agent registration",
                    "Takedown procedure compliance",
                    "Counter-notice process",
                    "Repeat infringer policy"
                ],
                penalties="Loss of safe harbor protection"
            ),
            ComplianceLaw(
                id="us_trademark_act",
                name="Lanham Act (Trademark)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                description="Federal trademark law",
                requirements=[
                    "Use in commerce",
                    "Registration (optional)",
                    "Enforcement of marks",
                    "Avoid confusion/dilution"
                ],
                penalties="Treble damages, attorney fees"
            ),
            
            # Marketing & Advertising
            ComplianceLaw(
                id="us_ftc_act",
                name="FTC Act Section 5",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.MARKETING,
                description="Prohibition of unfair/deceptive practices",
                requirements=[
                    "Truthful advertising",
                    "Substantiation of claims",
                    "Clear disclosures",
                    "Endorsement guidelines"
                ],
                penalties="Civil penalties, corrective advertising"
            ),
            ComplianceLaw(
                id="us_can_spam",
                name="CAN-SPAM Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.MARKETING,
                description="Email marketing requirements",
                requirements=[
                    "Accurate header information",
                    "Clear identification as advertisement",
                    "Unsubscribe mechanism",
                    "Physical address"
                ],
                penalties="Up to $43,280 per violation"
            ),
            ComplianceLaw(
                id="us_tcpa",
                name="Telephone Consumer Protection Act (TCPA)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.MARKETING,
                description="Telemarketing and robocall restrictions",
                requirements=[
                    "Prior express written consent",
                    "Do Not Call registry compliance",
                    "Time restrictions",
                    "Identification requirements"
                ],
                penalties="$500-$1,500 per violation"
            ),
            
            # Securities
            ComplianceLaw(
                id="us_securities_act_1933",
                name="Securities Act of 1933",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.SECURITIES,
                description="Securities registration and disclosure",
                requirements=[
                    "Registration or exemption",
                    "Prospectus disclosure",
                    "Anti-fraud provisions",
                    "Howey test compliance"
                ],
                penalties="Civil and criminal penalties"
            ),
            ComplianceLaw(
                id="us_securities_exchange_act_1934",
                name="Securities Exchange Act of 1934",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.SECURITIES,
                description="Secondary market regulation",
                requirements=[
                    "Periodic reporting (if registered)",
                    "Insider trading prohibitions",
                    "Market manipulation prevention",
                    "Broker-dealer registration"
                ],
                penalties="Criminal penalties up to 20 years"
            ),
            
            # Tax
            ComplianceLaw(
                id="us_irc",
                name="Internal Revenue Code",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.TAX,
                description="Federal tax requirements",
                requirements=[
                    "Tax identification number",
                    "Annual tax filing",
                    "Employment tax withholding",
                    "1099 reporting"
                ],
                penalties="Interest, penalties, criminal prosecution"
            ),
            ComplianceLaw(
                id="wy_business_tax",
                name="Wyoming Business Taxes",
                jurisdiction=JurisdictionType.WYOMING,
                category=ComplianceCategory.TAX,
                description="Wyoming state tax requirements",
                requirements=[
                    "Annual license tax",
                    "Sales tax collection (if applicable)",
                    "Workers compensation",
                    "Unemployment insurance"
                ],
                penalties="Interest, penalties, license revocation"
            ),
            
            # Employment
            ComplianceLaw(
                id="us_flsa",
                name="Fair Labor Standards Act (FLSA)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.EMPLOYMENT,
                description="Minimum wage and overtime requirements",
                requirements=[
                    "Minimum wage compliance",
                    "Overtime pay (1.5x)",
                    "Child labor restrictions",
                    "Recordkeeping"
                ],
                penalties="Back wages, liquidated damages"
            ),
            ComplianceLaw(
                id="us_title_vii",
                name="Title VII Civil Rights Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.EMPLOYMENT,
                description="Employment discrimination prohibition",
                requirements=[
                    "Non-discrimination policies",
                    "Equal opportunity",
                    "Harassment prevention",
                    "Accommodation"
                ],
                penalties="Compensatory and punitive damages"
            ),
            ComplianceLaw(
                id="us_ada",
                name="Americans with Disabilities Act (ADA)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.ACCESSIBILITY,
                description="Disability discrimination and accessibility",
                requirements=[
                    "Reasonable accommodation",
                    "Accessible facilities",
                    "Website accessibility (Title III)",
                    "Non-discrimination"
                ],
                penalties="Compensatory damages, attorney fees"
            ),
            
            # Consumer Protection
            ComplianceLaw(
                id="us_magnuson_moss",
                name="Magnuson-Moss Warranty Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.CONSUMER_PROTECTION,
                description="Consumer product warranty requirements",
                requirements=[
                    "Clear warranty terms",
                    "Pre-sale availability",
                    "Full or limited designation",
                    "Dispute resolution"
                ],
                penalties="Attorney fees, injunctive relief"
            ),
            ComplianceLaw(
                id="us_cfpb",
                name="Consumer Financial Protection Bureau Rules",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.CONSUMER_PROTECTION,
                description="Financial consumer protection",
                requirements=[
                    "Fair lending",
                    "Disclosure requirements",
                    "Complaint handling",
                    "Data security"
                ],
                penalties="Civil money penalties"
            ),
            
            # UK Laws
            ComplianceLaw(
                id="uk_dpa",
                name="UK Data Protection Act 2018",
                jurisdiction=JurisdictionType.UK,
                category=ComplianceCategory.DATA_PROTECTION,
                description="UK data protection law (post-GDPR)",
                requirements=[
                    "Lawful processing",
                    "Data subject rights",
                    "ICO registration",
                    "Breach notification"
                ],
                penalties="Up to £17.5 million or 4% of turnover"
            ),
            
            # Additional Federal Laws
            ComplianceLaw(
                id="us_hipaa",
                name="Health Insurance Portability and Accountability Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Health information privacy (if applicable)",
                requirements=[
                    "PHI protection",
                    "Security rule compliance",
                    "Breach notification",
                    "Business associate agreements"
                ],
                penalties="Up to $1.5 million per year per violation"
            ),
            ComplianceLaw(
                id="us_ecpa",
                name="Electronic Communications Privacy Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Electronic communications protection",
                requirements=[
                    "Consent for interception",
                    "Stored communications protection",
                    "Pen register restrictions"
                ],
                penalties="Criminal penalties, civil damages"
            ),
            ComplianceLaw(
                id="us_ferpa",
                name="Family Educational Rights and Privacy Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Student education records privacy",
                requirements=[
                    "Parental access rights",
                    "Consent for disclosure",
                    "Directory information notice",
                    "Record amendment rights"
                ],
                penalties="Loss of federal funding"
            ),
            ComplianceLaw(
                id="us_glba",
                name="Gramm-Leach-Bliley Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.PRIVACY,
                description="Financial privacy requirements",
                requirements=[
                    "Privacy notices",
                    "Opt-out rights",
                    "Safeguards rule",
                    "Pretexting protection"
                ],
                penalties="Up to $100,000 per violation"
            ),
            
            # State-Specific
            ComplianceLaw(
                id="de_corporate_law",
                name="Delaware General Corporation Law",
                jurisdiction=JurisdictionType.DELAWARE,
                category=ComplianceCategory.DAO,
                description="Delaware corporate governance (alternative to WY DAO)",
                requirements=[
                    "Certificate of incorporation",
                    "Bylaws adoption",
                    "Annual franchise tax",
                    "Registered agent"
                ],
                penalties="Administrative penalties, dissolution"
            ),
            
            # Additional Compliance Areas
            ComplianceLaw(
                id="us_export_control",
                name="Export Administration Regulations (EAR)",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.INTELLECTUAL_PROPERTY,
                description="Export control for technology",
                requirements=[
                    "Export classification",
                    "License requirements",
                    "Restricted party screening",
                    "Recordkeeping"
                ],
                penalties="Criminal penalties, export privileges denial"
            ),
            ComplianceLaw(
                id="us_cfaa",
                name="Computer Fraud and Abuse Act",
                jurisdiction=JurisdictionType.FEDERAL_US,
                category=ComplianceCategory.DATA_PROTECTION,
                description="Computer crime prohibitions",
                requirements=[
                    "Authorized access only",
                    "No exceeding authorization",
                    "Terms of service compliance",
                    "Security testing authorization"
                ],
                penalties="Criminal penalties up to 10 years"
            ),
            ComplianceLaw(
                id="eu_dma",
                name="Digital Markets Act (DMA)",
                jurisdiction=JurisdictionType.EU,
                category=ComplianceCategory.CONSUMER_PROTECTION,
                description="Digital platform gatekeeper regulation",
                requirements=[
                    "Fair, transparent conditions",
                    "Interoperability",
                    "Data portability",
                    "Self-preferencing restrictions"
                ],
                penalties="Up to 10% of global turnover"
            ),
            ComplianceLaw(
                id="eu_dsa",
                name="Digital Services Act (DSA)",
                jurisdiction=JurisdictionType.EU,
                category=ComplianceCategory.CONSUMER_PROTECTION,
                description="Digital services liability and safety",
                requirements=[
                    "Content moderation",
                    "Transparency reporting",
                    "Notice and action mechanism",
                    "Risk assessment"
                ],
                penalties="Up to 6% of global turnover"
            ),
        ]
    
    def check_compliance(self, content: str, jurisdictions: Optional[List[str]] = None, 
                        categories: Optional[List[str]] = None) -> Dict:
        """Check content for compliance violations"""
        
        applicable_laws = self.laws
        
        if jurisdictions:
            applicable_laws = [law for law in applicable_laws 
                             if law.jurisdiction.value in jurisdictions]
        
        if categories:
            applicable_laws = [law for law in applicable_laws 
                             if law.category.value in categories]
        
        # Simple keyword-based compliance checking
        violations = []
        warnings = []
        
        # Check for common compliance issues
        patterns = {
            "personal_data": r"\b(ssn|social security|credit card|passport)\b",
            "health_info": r"\b(medical|health|diagnosis|prescription)\b",
            "financial": r"\b(bank account|routing number|investment advice)\b",
            "children": r"\b(child|children|minor|kid)\b",
            "marketing": r"\b(guarantee|promise|100%|risk-free)\b"
        }
        
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                warnings.append(f"Potential {pattern_name} content detected - review applicable laws")
        
        return {
            "status": "checked",
            "applicable_laws": len(applicable_laws),
            "laws": [law.to_dict() for law in applicable_laws],
            "violations": violations,
            "warnings": warnings,
            "recommendation": "Manual legal review recommended for production use"
        }
    
    def get_laws_by_category(self, category: str) -> List[ComplianceLaw]:
        """Get all laws in a specific category"""
        return [law for law in self.laws if law.category.value == category]
    
    def get_laws_by_jurisdiction(self, jurisdiction: str) -> List[ComplianceLaw]:
        """Get all laws for a specific jurisdiction"""
        return [law for law in self.laws if law.jurisdiction.value == jurisdiction]
    
    def get_all_laws(self) -> List[Dict]:
        """Get all compliance laws"""
        return [law.to_dict() for law in self.laws]
    
    def get_stats(self) -> Dict:
        """Get compliance checker statistics"""
        
        by_jurisdiction = {}
        by_category = {}
        
        for law in self.laws:
            jurisdiction = law.jurisdiction.value
            category = law.category.value
            
            by_jurisdiction[jurisdiction] = by_jurisdiction.get(jurisdiction, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            "total_laws": len(self.laws),
            "by_jurisdiction": by_jurisdiction,
            "by_category": by_category
        }


# Global compliance checker instance
compliance_checker = LegalComplianceChecker()
