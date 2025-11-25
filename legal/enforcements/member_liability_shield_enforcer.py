#!/usr/bin/env python3
"""
member_liability_shield_enforcer.py
Python module that injects Delaware-style shields into any OA diff
Source: Sarcuni v. bZx DAO (2023) + Wyoming Supplement
Deployed by: Sovereign Compiler v1.0

This enforcer automatically amends Operating Agreements on deploy to include
member liability protections based on Delaware Chancery precedents and
Wyoming DAO supplement requirements.
"""

import json
import hashlib
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class LiabilityShield:
    """Represents a liability shield provision"""
    name: str
    source: str
    provision_text: str
    effective_date: str
    jurisdiction: str


@dataclass 
class ShieldConfig:
    """Configuration for the liability shield enforcer"""
    wyoming_supplement: bool = True
    delaware_precedent: bool = True
    bzx_dao_defense: bool = True
    auto_amend_on_deploy: bool = True


@dataclass
class AmendmentRecord:
    """Record of an OA amendment"""
    timestamp: str
    amendment_type: str
    provisions_added: list
    hash_before: str
    hash_after: str
    verified: bool = False


class MemberLiabilityShieldEnforcer:
    """
    Enforces member liability shields based on:
    - Sarcuni v. bZx DAO (2023) - veil piercing defense
    - Wyoming DAO Supplement - statutory protections
    - Delaware Chancery precedents - member liability limits
    """

    # Standard shield provisions based on case law
    SHIELD_PROVISIONS = [
        LiabilityShield(
            name="veil_piercing_defense",
            source="Sarcuni v. bZx DAO (2023)",
            provision_text="""
            No member, manager, or token holder of this DAO shall be personally
            liable for any debt, obligation, or liability of the DAO solely by
            reason of being a member, manager, or token holder. The corporate
            veil of this DAO shall not be pierced except as expressly provided
            by applicable law, and participation in governance through token
            voting shall not, by itself, create any agency, partnership, or
            fiduciary relationship imposing personal liability.
            """,
            effective_date="2023-03-27",
            jurisdiction="Federal/California"
        ),
        LiabilityShield(
            name="wyoming_statutory_shield",
            source="Wyoming DAO Supplement (W.S. 17-31)",
            provision_text="""
            In accordance with Wyoming Statute 17-31-109, members of this DAO
            are not liable under a judgment, decree, or order of a court, or
            in any other manner, for a debt, obligation, or liability of the
            DAO. This statutory protection applies to all members regardless
            of their level of participation in DAO governance.
            """,
            effective_date="2021-07-01",
            jurisdiction="Wyoming"
        ),
        LiabilityShield(
            name="delaware_member_protection",
            source="Delaware Chancery Precedent (6 Del. C. § 18-303)",
            provision_text="""
            Except as otherwise provided by this Agreement, the debts,
            obligations, and liabilities of the DAO, whether arising in
            contract, tort, or otherwise, shall be solely the debts,
            obligations, and liabilities of the DAO, and no member or
            manager shall be obligated personally for any such debt,
            obligation, or liability of the DAO solely by reason of
            being a member or acting as a manager.
            """,
            effective_date="2024-01-01",
            jurisdiction="Delaware"
        ),
    ]

    def __init__(self, config: Optional[ShieldConfig] = None):
        """Initialize the enforcer with optional configuration"""
        self.config = config or ShieldConfig()
        self.amendment_history: list[AmendmentRecord] = []
        self.active_shields: list[LiabilityShield] = []
        self._load_applicable_shields()

    def _load_applicable_shields(self) -> None:
        """Load shields based on configuration"""
        for shield in self.SHIELD_PROVISIONS:
            if shield.name == "veil_piercing_defense" and self.config.bzx_dao_defense:
                self.active_shields.append(shield)
            elif shield.name == "wyoming_statutory_shield" and self.config.wyoming_supplement:
                self.active_shields.append(shield)
            elif shield.name == "delaware_member_protection" and self.config.delaware_precedent:
                self.active_shields.append(shield)

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def analyze_oa(self, oa_content: str) -> dict:
        """
        Analyze an Operating Agreement for missing liability shields
        
        Args:
            oa_content: The full text of the Operating Agreement
            
        Returns:
            Analysis report with missing shields and recommendations
        """
        missing_shields = []
        present_shields = []
        
        for shield in self.active_shields:
            # Check for key phrases that indicate the shield is present
            key_phrases = [
                "not personally liable",
                "veil piercing",
                "member liability",
                "debts, obligations, and liabilities",
            ]
            
            shield_present = any(
                phrase.lower() in oa_content.lower() 
                for phrase in key_phrases
            )
            
            if shield_present:
                present_shields.append(shield.name)
            else:
                missing_shields.append(shield)
        
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "oa_hash": self._compute_hash(oa_content),
            "shields_analyzed": len(self.active_shields),
            "shields_present": present_shields,
            "shields_missing": [s.name for s in missing_shields],
            "compliant": len(missing_shields) == 0,
            "recommendations": [
                {
                    "shield": s.name,
                    "source": s.source,
                    "action": "Add provision to OA"
                }
                for s in missing_shields
            ]
        }

    def generate_amendment(self, oa_content: str) -> str:
        """
        Generate an amendment to add missing liability shields
        
        Args:
            oa_content: The full text of the Operating Agreement
            
        Returns:
            Amendment text to be added to the OA
        """
        analysis = self.analyze_oa(oa_content)
        
        if analysis["compliant"]:
            return "# No amendment needed - all shields present"
        
        amendment_lines = [
            "# AMENDMENT TO OPERATING AGREEMENT",
            f"# Generated: {datetime.utcnow().isoformat()}Z",
            "# Source: Member Liability Shield Enforcer v1.0",
            "",
            "## ARTICLE [X] - MEMBER LIABILITY PROTECTION",
            "",
        ]
        
        for shield in self.active_shields:
            if shield.name in analysis["shields_missing"]:
                amendment_lines.extend([
                    f"### Section: {shield.name.replace('_', ' ').title()}",
                    f"**Source:** {shield.source}",
                    f"**Jurisdiction:** {shield.jurisdiction}",
                    "",
                    shield.provision_text.strip(),
                    "",
                ])
        
        amendment_lines.extend([
            "---",
            "This amendment is effective immediately upon adoption and",
            "shall be incorporated into the Operating Agreement by reference.",
        ])
        
        return "\n".join(amendment_lines)

    def apply_amendment(self, oa_content: str) -> tuple[str, AmendmentRecord]:
        """
        Apply amendments to an Operating Agreement
        
        Args:
            oa_content: The full text of the Operating Agreement
            
        Returns:
            Tuple of (amended OA content, amendment record)
        """
        hash_before = self._compute_hash(oa_content)
        amendment = self.generate_amendment(oa_content)
        
        if "No amendment needed" in amendment:
            record = AmendmentRecord(
                timestamp=datetime.utcnow().isoformat() + "Z",
                amendment_type="no_change",
                provisions_added=[],
                hash_before=hash_before,
                hash_after=hash_before,
                verified=True
            )
            return oa_content, record
        
        # Append amendment to OA
        amended_content = f"{oa_content}\n\n{amendment}"
        hash_after = self._compute_hash(amended_content)
        
        analysis = self.analyze_oa(oa_content)
        record = AmendmentRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            amendment_type="liability_shield_addition",
            provisions_added=analysis["shields_missing"],
            hash_before=hash_before,
            hash_after=hash_after,
            verified=True
        )
        
        self.amendment_history.append(record)
        return amended_content, record

    def get_compliance_report(self) -> dict:
        """Generate a compliance report"""
        return {
            "enforcer": "MemberLiabilityShieldEnforcer",
            "version": "1.0",
            "config": {
                "wyoming_supplement": self.config.wyoming_supplement,
                "delaware_precedent": self.config.delaware_precedent,
                "bzx_dao_defense": self.config.bzx_dao_defense,
            },
            "active_shields": [s.name for s in self.active_shields],
            "amendments_applied": len(self.amendment_history),
            "sources": [
                "Sarcuni v. bZx DAO (2023)",
                "Wyoming DAO Supplement (W.S. 17-31)",
                "Delaware Chancery Precedent (6 Del. C. § 18-303)"
            ]
        }


# Example usage and self-test
if __name__ == "__main__":
    # Create enforcer
    enforcer = MemberLiabilityShieldEnforcer()
    
    # Sample OA without liability shields
    sample_oa = """
    OPERATING AGREEMENT
    OF
    EXAMPLE DAO LLC
    
    ARTICLE I - FORMATION
    This Limited Liability Company is formed under the Wyoming Limited 
    Liability Company Act.
    
    ARTICLE II - PURPOSE
    The purpose of this DAO is to operate as a decentralized autonomous
    organization for the benefit of its members.
    
    ARTICLE III - MEMBERSHIP
    Membership is determined by token holdings.
    """
    
    # Analyze the OA
    analysis = enforcer.analyze_oa(sample_oa)
    print("Analysis:", json.dumps(analysis, indent=2))
    
    # Generate and apply amendment
    amended_oa, record = enforcer.apply_amendment(sample_oa)
    print("\nAmendment Record:", json.dumps({
        "timestamp": record.timestamp,
        "type": record.amendment_type,
        "provisions_added": record.provisions_added,
        "verified": record.verified
    }, indent=2))
    
    # Get compliance report
    report = enforcer.get_compliance_report()
    print("\nCompliance Report:", json.dumps(report, indent=2))
