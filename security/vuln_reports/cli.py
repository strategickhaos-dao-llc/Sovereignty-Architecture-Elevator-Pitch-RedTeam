#!/usr/bin/env python3
"""
Vulnerability Report CLI Tool (WIP-006)

Command-line interface for creating vulnerability reports with templates,
CVSS calculation, and remediation recommendations.

Usage:
    python cli.py create --template hackerone --interactive
    python cli.py create --from-json finding.json
    python cli.py calculate-cvss --interactive
    python cli.py validate report.json

Author: Strategickhaos DAO LLC
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


try:
    from models import (
        VulnerabilityReport, CVSSVector, AssetInfo,
        ProofOfConcept, ImpactAssessment, RemediationAdvice,
        SeverityLevel
    )
    MODELS_AVAILABLE = True
except ImportError:
    print("Warning: models.py not found. Some features may be limited.")
    MODELS_AVAILABLE = False


class CVSSCalculator:
    """Calculate CVSS v3.1 scores"""
    
    # Base score metrics
    ATTACK_VECTOR = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
    ATTACK_COMPLEXITY = {"L": 0.77, "H": 0.44}
    PRIVILEGES_REQUIRED = {
        "N": {"U": 0.85, "C": 0.85},
        "L": {"U": 0.62, "C": 0.68},
        "H": {"U": 0.27, "C": 0.50}
    }
    USER_INTERACTION = {"N": 0.85, "R": 0.62}
    SCOPE = {"U": "unchanged", "C": "changed"}
    IMPACT = {"N": 0.0, "L": 0.22, "H": 0.56}
    
    @classmethod
    def calculate(cls, vector: Dict[str, str]) -> float:
        """
        Calculate CVSS score from vector components.
        
        Args:
            vector: Dictionary with CVSS vector components
        
        Returns:
            CVSS score (0.0-10.0)
        """
        # Extract values
        av = cls.ATTACK_VECTOR[vector["attack_vector"]]
        ac = cls.ATTACK_COMPLEXITY[vector["attack_complexity"]]
        
        scope = vector["scope"]
        pr = cls.PRIVILEGES_REQUIRED[vector["privileges_required"]][scope]
        ui = cls.USER_INTERACTION[vector["user_interaction"]]
        
        c = cls.IMPACT[vector["confidentiality"]]
        i = cls.IMPACT[vector["integrity"]]
        a = cls.IMPACT[vector["availability"]]
        
        # Calculate impact sub-score
        if scope == "U":
            impact = 6.42 * (1 - (1 - c) * (1 - i) * (1 - a))
        else:
            impact = 7.52 * (1 - (1 - c) * (1 - i) * (1 - a)) - 0.029 - 3.25 * ((1 - (1 - c) * (1 - i) * (1 - a)) - 0.02) ** 15
        
        # Calculate exploitability sub-score
        exploitability = 8.22 * av * ac * pr * ui
        
        # Calculate base score
        if impact <= 0:
            return 0.0
        
        if scope == "U":
            base_score = min(impact + exploitability, 10.0)
        else:
            base_score = min(1.08 * (impact + exploitability), 10.0)
        
        # Round up to one decimal
        return round(base_score * 10) / 10
    
    @classmethod
    def interactive_calculate(cls) -> tuple:
        """Interactive CVSS calculator"""
        print("\n" + "=" * 70)
        print("CVSS v3.1 CALCULATOR (Interactive)")
        print("=" * 70)
        
        vector = {}
        
        # Attack Vector
        print("\n1. Attack Vector (AV):")
        print("   N = Network (remotely exploitable)")
        print("   A = Adjacent (same network segment)")
        print("   L = Local (local access required)")
        print("   P = Physical (physical access required)")
        av = input("   Select [N/A/L/P]: ").upper()
        vector["attack_vector"] = av if av in ["N", "A", "L", "P"] else "N"
        
        # Attack Complexity
        print("\n2. Attack Complexity (AC):")
        print("   L = Low (straightforward to exploit)")
        print("   H = High (requires special conditions)")
        ac = input("   Select [L/H]: ").upper()
        vector["attack_complexity"] = ac if ac in ["L", "H"] else "L"
        
        # Privileges Required
        print("\n3. Privileges Required (PR):")
        print("   N = None (unauthenticated)")
        print("   L = Low (basic user privileges)")
        print("   H = High (admin privileges)")
        pr = input("   Select [N/L/H]: ").upper()
        vector["privileges_required"] = pr if pr in ["N", "L", "H"] else "N"
        
        # User Interaction
        print("\n4. User Interaction (UI):")
        print("   N = None (no user interaction)")
        print("   R = Required (user must take action)")
        ui = input("   Select [N/R]: ").upper()
        vector["user_interaction"] = ui if ui in ["N", "R"] else "N"
        
        # Scope
        print("\n5. Scope (S):")
        print("   U = Unchanged (contained to vulnerable component)")
        print("   C = Changed (impacts beyond vulnerable component)")
        s = input("   Select [U/C]: ").upper()
        vector["scope"] = s if s in ["U", "C"] else "U"
        
        # Confidentiality Impact
        print("\n6. Confidentiality Impact (C):")
        print("   N = None (no information disclosure)")
        print("   L = Low (limited information disclosure)")
        print("   H = High (total information disclosure)")
        c = input("   Select [N/L/H]: ").upper()
        vector["confidentiality"] = c if c in ["N", "L", "H"] else "N"
        
        # Integrity Impact
        print("\n7. Integrity Impact (I):")
        print("   N = None (no modification possible)")
        print("   L = Low (limited modification possible)")
        print("   H = High (total data modification)")
        i = input("   Select [N/L/H]: ").upper()
        vector["integrity"] = i if i in ["N", "L", "H"] else "N"
        
        # Availability Impact
        print("\n8. Availability Impact (A):")
        print("   N = None (no availability impact)")
        print("   L = Low (reduced performance)")
        print("   H = High (total system unavailable)")
        a = input("   Select [N/L/H]: ").upper()
        vector["availability"] = a if a in ["N", "L", "H"] else "N"
        
        # Calculate score
        score = cls.calculate(vector)
        
        # Determine severity
        if score >= 9.0:
            severity = "CRITICAL"
        elif score >= 7.0:
            severity = "HIGH"
        elif score >= 4.0:
            severity = "MEDIUM"
        elif score > 0.0:
            severity = "LOW"
        else:
            severity = "NONE"
        
        print("\n" + "=" * 70)
        print(f"CVSS Score: {score}")
        print(f"Severity: {severity}")
        print("\nVector String:")
        print(f"CVSS:3.1/AV:{vector['attack_vector']}/AC:{vector['attack_complexity']}/"
              f"PR:{vector['privileges_required']}/UI:{vector['user_interaction']}/"
              f"S:{vector['scope']}/C:{vector['confidentiality']}/"
              f"I:{vector['integrity']}/A:{vector['availability']}")
        print("=" * 70)
        
        return score, vector, severity


class VulnReportCLI:
    """CLI interface for vulnerability report management"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path(__file__).parent / "reports"
        self.output_dir.mkdir(exist_ok=True)
    
    def create_interactive(self, template: str = "hackerone") -> Dict:
        """
        Create vulnerability report interactively.
        
        Args:
            template: Template name to use
        
        Returns:
            Report dictionary
        """
        print("\n" + "🔥" * 35)
        print("VULNERABILITY REPORT CREATOR (Interactive)")
        print("🔥" * 35)
        
        report = {}
        
        # Basic information
        print("\n--- BASIC INFORMATION ---")
        report["report_id"] = input("Report ID (e.g., VR-2025-001): ") or f"VR-{datetime.now().year}-001"
        report["title"] = input("Vulnerability Title: ")
        report["submitted_by"] = input("Your Name/Handle: ")
        
        # Severity and CVSS
        print("\n--- SEVERITY ASSESSMENT ---")
        print("Would you like to calculate CVSS score? (y/n)")
        if input("> ").lower() == 'y':
            score, vector, severity = CVSSCalculator.interactive_calculate()
            report["cvss_score"] = score
            report["cvss_vector"] = vector
            report["severity"] = severity.lower()
        else:
            report["severity"] = input("Severity (critical/high/medium/low): ").lower()
            report["cvss_score"] = float(input("CVSS Score (0.0-10.0): "))
        
        # Weakness type
        report["weakness_type"] = input("CWE/Weakness Type (e.g., CWE-79: XSS): ")
        
        # Asset information
        print("\n--- ASSET INFORMATION ---")
        report["asset"] = {
            "name": input("Asset Name: "),
            "type": input("Asset Type (web_app/api/mobile/etc.): "),
            "url": input("Asset URL (if applicable): "),
            "environment": input("Environment (production/staging/dev): ")
        }
        
        # Content
        print("\n--- VULNERABILITY DETAILS ---")
        print("Summary (executive summary for management):")
        report["summary"] = input("> ")
        
        print("\nTechnical Details (detailed explanation):")
        report["technical_details"] = input("> ")
        
        # Proof of Concept
        print("\n--- PROOF OF CONCEPT ---")
        report["proof_of_concept"] = {
            "description": input("Reproduction steps:\n> "),
            "code": input("PoC code/payload (optional):\n> ")
        }
        
        # Impact
        print("\n--- IMPACT ASSESSMENT ---")
        report["impact"] = {
            "confidentiality_impact": input("Confidentiality Impact: "),
            "integrity_impact": input("Integrity Impact: "),
            "availability_impact": input("Availability Impact: "),
            "business_impact": input("Business Impact: ")
        }
        
        # Remediation
        print("\n--- REMEDIATION ---")
        report["remediation"] = {
            "short_term": [input("Short-term mitigation 1: "), input("Short-term mitigation 2: ")],
            "long_term": [input("Long-term fix 1: "), input("Long-term fix 2: ")]
        }
        
        # Save report
        output_file = self.output_dir / f"{report['report_id']}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved to: {output_file}")
        
        return report
    
    def create_from_json(self, json_file: str) -> Dict:
        """
        Create report from JSON file.
        
        Args:
            json_file: Path to JSON file
        
        Returns:
            Report dictionary
        """
        with open(json_file) as f:
            report = json.load(f)
        
        print(f"✅ Loaded report from {json_file}")
        return report
    
    def validate_report(self, report_file: str) -> bool:
        """
        Validate vulnerability report.
        
        Args:
            report_file: Path to report JSON file
        
        Returns:
            True if valid, False otherwise
        """
        if not MODELS_AVAILABLE:
            print("❌ Cannot validate: models.py not available")
            return False
        
        try:
            with open(report_file) as f:
                data = json.load(f)
            
            # Validate using Pydantic model
            report = VulnerabilityReport(**data)
            
            print(f"✅ Report validation passed!")
            print(f"   ID: {report.report_id}")
            print(f"   Title: {report.title}")
            print(f"   Severity: {report.severity.value.upper()}")
            print(f"   CVSS: {report.cvss_score}")
            
            return True
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return False
    
    def list_templates(self):
        """List available templates"""
        print("\n📋 Available Templates:")
        templates = list(self.templates_dir.glob("*.md"))
        for template in templates:
            print(f"  • {template.stem}")
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Vulnerability Report CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create report interactively
  python cli.py create --interactive

  # Create from JSON
  python cli.py create --from-json finding.json

  # Calculate CVSS score
  python cli.py calculate-cvss

  # Validate report
  python cli.py validate report.json

  # List templates
  python cli.py list-templates
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create vulnerability report")
    create_parser.add_argument("--template", default="hackerone", help="Template name")
    create_parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    create_parser.add_argument("--from-json", help="Create from JSON file")
    
    # Calculate CVSS command
    cvss_parser = subparsers.add_parser("calculate-cvss", help="Calculate CVSS score")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate report")
    validate_parser.add_argument("report_file", help="Report JSON file to validate")
    
    # List templates command
    list_parser = subparsers.add_parser("list-templates", help="List available templates")
    
    args = parser.parse_args()
    
    cli = VulnReportCLI()
    
    if args.command == "create":
        if args.interactive:
            cli.create_interactive(args.template)
        elif args.from_json:
            cli.create_from_json(args.from_json)
        else:
            print("❌ Please specify --interactive or --from-json")
            
    elif args.command == "calculate-cvss":
        CVSSCalculator.interactive_calculate()
        
    elif args.command == "validate":
        cli.validate_report(args.report_file)
        
    elif args.command == "list-templates":
        cli.list_templates()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
