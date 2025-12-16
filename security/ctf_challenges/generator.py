#!/usr/bin/env python3
"""
CTF Challenge Generator from Vulnerability Findings (WIP-005)

Generates CTF challenges from vulnerability reports for security training.
Supports JSON, YAML, and HackerOne-compatible formats.

Reference: INV-082 SwarmBounty specification
Author: Strategickhaos DAO LLC
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Literal
from datetime import datetime
from enum import Enum

try:
    from pydantic import BaseModel, Field
except ImportError:
    print("Warning: pydantic not installed. Install with: pip install pydantic")
    BaseModel = object
    Field = lambda *args, **kwargs: None


class DifficultyLevel(str, Enum):
    """CTF challenge difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    INSANE = "insane"


class CTFCategory(str, Enum):
    """CTF challenge categories"""
    WEB = "web"
    PWNABLE = "pwnable"
    REVERSING = "reversing"
    CRYPTO = "crypto"
    FORENSICS = "forensics"
    MISC = "misc"


class CTFChallenge(BaseModel):
    """
    CTF challenge data structure.
    
    Compatible with major CTF platforms:
    - CTFd
    - HackerOne CTF
    - PicoCTF
    """
    
    # Metadata
    id: str = Field(..., description="Challenge unique identifier")
    name: str = Field(..., description="Challenge name")
    category: CTFCategory
    difficulty: DifficultyLevel
    points: int = Field(..., ge=10, le=1000, description="Point value")
    
    # Content
    description: str = Field(..., description="Challenge description")
    hints: List[str] = Field(default_factory=list, description="Progressive hints")
    flag: str = Field(..., description="Flag to capture")
    flag_format: str = Field(
        default="flag{...}",
        description="Expected flag format"
    )
    
    # Challenge files and resources
    files: List[str] = Field(
        default_factory=list,
        description="Challenge files for download"
    )
    url: Optional[str] = Field(None, description="Challenge instance URL")
    connection_info: Optional[Dict[str, str]] = Field(
        None,
        description="Connection details (host, port, etc.)"
    )
    
    # Solution and learning
    solution: str = Field(..., description="Detailed solution writeup")
    learning_objectives: List[str] = Field(
        default_factory=list,
        description="Skills learned from this challenge"
    )
    tags: List[str] = Field(default_factory=list, description="Search tags")
    
    # Sourcing
    source_vuln_report: Optional[str] = Field(
        None,
        description="Source vulnerability report ID"
    )
    cwe_reference: Optional[str] = Field(
        None,
        description="Related CWE ID"
    )
    
    # Platform-specific
    author: str = Field(default="Strategickhaos DAO")
    created_date: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True


class CTFChallengeGenerator:
    """Generate CTF challenges from vulnerability findings"""
    
    def __init__(self):
        self.challenges: List[CTFChallenge] = []
    
    @staticmethod
    def calculate_difficulty(cvss_score: float, complexity: str) -> DifficultyLevel:
        """
        Calculate CTF difficulty based on vulnerability characteristics.
        
        Args:
            cvss_score: CVSS score (0-10)
            complexity: Attack complexity (low, medium, high)
        
        Returns:
            DifficultyLevel enum
        """
        # Higher CVSS often means easier to exploit -> easier CTF
        # But we adjust for complexity
        
        if cvss_score >= 9.0 and complexity.lower() == "low":
            return DifficultyLevel.EASY
        elif cvss_score >= 7.0 and complexity.lower() in ["low", "medium"]:
            return DifficultyLevel.MEDIUM
        elif cvss_score >= 4.0:
            return DifficultyLevel.HARD
        else:
            return DifficultyLevel.INSANE
    
    @staticmethod
    def calculate_points(difficulty: DifficultyLevel) -> int:
        """
        Calculate point value based on difficulty.
        
        Args:
            difficulty: Challenge difficulty level
        
        Returns:
            Point value (10-1000)
        """
        points_map = {
            DifficultyLevel.EASY: 100,
            DifficultyLevel.MEDIUM: 250,
            DifficultyLevel.HARD: 500,
            DifficultyLevel.INSANE: 1000
        }
        return points_map.get(difficulty, 100)
    
    @staticmethod
    def map_weakness_to_category(cwe_id: str) -> CTFCategory:
        """
        Map CWE to CTF category.
        
        Args:
            cwe_id: CWE identifier (e.g., "CWE-79")
        
        Returns:
            CTFCategory enum
        """
        # Web vulnerabilities
        web_cwes = ["79", "89", "91", "94", "352", "611", "918"]
        # Binary/pwn vulnerabilities
        pwn_cwes = ["119", "120", "121", "122", "125", "416", "787"]
        # Crypto vulnerabilities
        crypto_cwes = ["327", "328", "330", "331", "347", "759"]
        
        cwe_num = cwe_id.split("-")[-1].strip()
        
        if cwe_num in web_cwes:
            return CTFCategory.WEB
        elif cwe_num in pwn_cwes:
            return CTFCategory.PWNABLE
        elif cwe_num in crypto_cwes:
            return CTFCategory.CRYPTO
        else:
            return CTFCategory.MISC
    
    def generate_from_vuln_report(
        self,
        vuln_report: Dict,
        sanitize: bool = True
    ) -> CTFChallenge:
        """
        Generate CTF challenge from vulnerability report.
        
        Args:
            vuln_report: Vulnerability report dictionary
            sanitize: Whether to sanitize sensitive information
        
        Returns:
            CTFChallenge object
        """
        # Extract vulnerability details
        report_id = vuln_report.get("report_id", "VR-UNKNOWN")
        title = vuln_report.get("title", "Unknown Vulnerability")
        weakness_type = vuln_report.get("weakness_type", "")
        cvss_score = vuln_report.get("cvss_score", 5.0)
        technical_details = vuln_report.get("technical_details", "")
        poc = vuln_report.get("proof_of_concept", {})
        
        # Calculate difficulty
        complexity = vuln_report.get("cvss_vector", {}).get("attack_complexity", "M")
        difficulty = self.calculate_difficulty(cvss_score, complexity)
        points = self.calculate_points(difficulty)
        
        # Determine category
        category = self.map_weakness_to_category(weakness_type)
        
        # Generate challenge ID
        challenge_id = f"CTF-{report_id.split('-')[-1]}"
        
        # Create sanitized description
        if sanitize:
            description = self._sanitize_description(title, technical_details)
            flag = f"flag{{{report_id.lower().replace('-', '_')}_solved}}"
        else:
            description = technical_details
            flag = f"flag{{{report_id}_production}}"
        
        # Extract hints from PoC
        hints = self._extract_hints(poc.get("description", ""))
        
        # Generate solution writeup
        solution = self._generate_solution(
            technical_details,
            poc,
            vuln_report.get("remediation", {})
        )
        
        # Extract learning objectives
        learning_objectives = self._extract_learning_objectives(weakness_type)
        
        # Create challenge
        challenge = CTFChallenge(
            id=challenge_id,
            name=f"{category.value.upper()}: {title}",
            category=category,
            difficulty=difficulty,
            points=points,
            description=description,
            hints=hints,
            flag=flag,
            solution=solution,
            learning_objectives=learning_objectives,
            tags=[category.value, difficulty.value, weakness_type.split(":")[0]],
            source_vuln_report=report_id,
            cwe_reference=weakness_type.split(":")[0].strip()
        )
        
        self.challenges.append(challenge)
        return challenge
    
    @staticmethod
    def _sanitize_description(title: str, details: str) -> str:
        """Sanitize description for CTF challenge"""
        # Remove sensitive information
        sanitized = details.replace("production", "target")
        sanitized = sanitized.replace("example.com", "challenge.ctf")
        
        description = f"""
**Challenge Scenario:**

You've discovered a security issue in a web application. Your task is to 
exploit this vulnerability and capture the flag.

**Vulnerability Type:** {title}

**Background:**
{sanitized[:500]}...

**Your Goal:**
Find and exploit the vulnerability to capture the flag.

**Flag Format:** flag{{...}}
""".strip()
        
        return description
    
    @staticmethod
    def _extract_hints(poc_description: str) -> List[str]:
        """Extract progressive hints from PoC"""
        hints = []
        
        if "search" in poc_description.lower():
            hints.append("Look for user input fields")
            hints.append("Try injecting special characters")
            hints.append("Observe the application's response")
        
        if "sql" in poc_description.lower():
            hints.append("The application uses a database")
            hints.append("Try SQL injection techniques")
            hints.append("Look for error messages")
        
        if not hints:
            hints = [
                "Read the vulnerability description carefully",
                "Test all input points",
                "Use browser developer tools"
            ]
        
        return hints[:3]  # Limit to 3 hints
    
    @staticmethod
    def _generate_solution(
        technical_details: str,
        poc: Dict,
        remediation: Dict
    ) -> str:
        """Generate solution writeup"""
        solution = f"""
## Solution Writeup

### Step 1: Reconnaissance
{technical_details[:200]}...

### Step 2: Exploitation
{poc.get('description', 'Follow the proof of concept steps')}

### Step 3: Capturing the Flag
Execute the exploit and observe the response containing the flag.

### Code:
```
{poc.get('code', '# PoC code here')}
```

### What We Learned
This challenge demonstrates a real-world vulnerability. In production:
- {remediation.get('short_term', ['Implement proper input validation'])[0] if remediation.get('short_term') else 'Implement proper security controls'}
- {remediation.get('long_term', ['Use secure coding practices'])[0] if remediation.get('long_term') else 'Follow security best practices'}

### Prevention
{remediation.get('references', ['See OWASP guidelines'])[0] if remediation.get('references') else 'Follow industry standards'}
""".strip()
        
        return solution
    
    @staticmethod
    def _extract_learning_objectives(weakness_type: str) -> List[str]:
        """Extract learning objectives from weakness type"""
        objectives = [
            f"Understanding {weakness_type}",
            "Exploiting web vulnerabilities",
            "Security testing methodology"
        ]
        return objectives
    
    def export_json(self, output_file: str) -> None:
        """Export challenges to JSON format (CTFd compatible)"""
        challenges_data = [c.dict() for c in self.challenges]
        
        with open(output_file, 'w') as f:
            json.dump({
                "challenges": challenges_data,
                "metadata": {
                    "generator": "Strategickhaos CTF Generator",
                    "version": "1.0.0",
                    "generated_at": datetime.now().isoformat(),
                    "total_challenges": len(self.challenges)
                }
            }, f, indent=2, default=str)
        
        print(f"✅ Exported {len(self.challenges)} challenges to {output_file}")
    
    def export_yaml(self, output_file: str) -> None:
        """Export challenges to YAML format"""
        challenges_data = [c.dict() for c in self.challenges]
        
        with open(output_file, 'w') as f:
            yaml.dump({
                "challenges": challenges_data,
                "metadata": {
                    "generator": "Strategickhaos CTF Generator",
                    "version": "1.0.0",
                    "generated_at": datetime.now().isoformat()
                }
            }, f, default_flow_style=False)
        
        print(f"✅ Exported {len(self.challenges)} challenges to {output_file}")
    
    def export_hackerone_format(self, output_file: str) -> None:
        """Export in HackerOne-compatible format"""
        hackerone_data = []
        
        for challenge in self.challenges:
            hackerone_data.append({
                "title": challenge.name,
                "vulnerability_information": challenge.description,
                "impact": f"Learning objective for {challenge.category} vulnerabilities",
                "severity_rating": challenge.difficulty if isinstance(challenge.difficulty, str) else challenge.difficulty.value,
                "proof_of_concept": challenge.solution,
                "suggested_remediation": "\n".join(challenge.learning_objectives),
                "custom_fields": {
                    "ctf_points": challenge.points,
                    "flag": challenge.flag,
                    "source_report": challenge.source_vuln_report
                }
            })
        
        with open(output_file, 'w') as f:
            json.dump(hackerone_data, f, indent=2)
        
        print(f"✅ Exported {len(self.challenges)} challenges in HackerOne format to {output_file}")


def demo():
    """Demonstrate CTF challenge generation"""
    print("\n" + "=" * 70)
    print("CTF CHALLENGE GENERATOR DEMO")
    print("=" * 70)
    
    # Sample vulnerability report
    sample_vuln = {
        "report_id": "VR-2025-001",
        "title": "SQL Injection in User Search",
        "weakness_type": "CWE-89: SQL Injection",
        "cvss_score": 8.6,
        "cvss_vector": {
            "attack_complexity": "low"
        },
        "technical_details": "The application fails to properly sanitize user input in the search parameter, allowing SQL injection attacks that can compromise the entire database.",
        "proof_of_concept": {
            "description": "1. Navigate to /search\n2. Enter payload: ' OR '1'='1\n3. Observe database error revealing injection\n4. Extract data using UNION queries",
            "code": "curl 'https://example.com/search?q=%27+OR+%271%27%3D%271'"
        },
        "remediation": {
            "short_term": ["Disable search functionality", "Add WAF rules"],
            "long_term": ["Use parameterized queries", "Input validation"],
            "references": ["https://owasp.org/www-community/attacks/SQL_Injection"]
        }
    }
    
    # Generate CTF challenge
    generator = CTFChallengeGenerator()
    challenge = generator.generate_from_vuln_report(sample_vuln)
    
    print(f"\n✅ Generated CTF Challenge:")
    print(f"   ID: {challenge.id}")
    print(f"   Name: {challenge.name}")
    print(f"   Category: {challenge.category}")
    print(f"   Difficulty: {challenge.difficulty}")
    print(f"   Points: {challenge.points}")
    print(f"   Flag: {challenge.flag}")
    print(f"   Hints: {len(challenge.hints)}")
    
    # Export in different formats
    output_dir = Path(__file__).parent / "generated"
    output_dir.mkdir(exist_ok=True)
    
    generator.export_json(str(output_dir / "challenges.json"))
    generator.export_yaml(str(output_dir / "challenges.yaml"))
    generator.export_hackerone_format(str(output_dir / "challenges_hackerone.json"))
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo()
