#!/usr/bin/env python3
"""
Test Suite for Nonprofit Final Artifacts
Strategickhaos DAO LLC | EIN 39-2923503
Tests the four final artifacts for functionality and compliance
"""

import os
import sys
import hashlib
import subprocess
import tempfile
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class NonprofitArtifactsTests:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.repo_root = self.script_dir.parent
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
        self.test_results.append((test_name, passed))
        print(f"{status} | {test_name}")
        if message:
            print(f"      {message}")
    
    def test_artifacts_directory_exists(self):
        """Test that nonprofit_final_artifacts directory exists"""
        exists = self.script_dir.exists()
        self.log_test(
            "Artifacts directory exists",
            exists,
            f"Path: {self.script_dir}"
        )
        return exists
    
    def test_minutes_template_exists(self):
        """Test that minutes_template.md exists and has required content"""
        template_path = self.script_dir / "minutes_template.md"
        exists = template_path.exists()
        
        if exists:
            content = template_path.read_text()
            has_date_placeholder = "{{DATE}}" in content
            has_ein = "39-2923503" in content
            has_gpg = "9F3A 2C8B D407 1810" in content
            has_arweave = "ar://" in content
            
            passed = has_date_placeholder and has_ein and has_gpg and has_arweave
            self.log_test(
                "Board minutes template content",
                passed,
                f"Date placeholder: {has_date_placeholder}, EIN: {has_ein}, GPG: {has_gpg}, Arweave: {has_arweave}"
            )
        else:
            self.log_test("Board minutes template exists", False, "File not found")
            passed = False
        
        return passed
    
    def test_donor_hash_script_syntax(self):
        """Test that donor_hash.py has valid Python syntax"""
        script_path = self.script_dir / "donor_hash.py"
        
        if not script_path.exists():
            self.log_test("Donor hash script exists", False, "File not found")
            return False
        
        # Check Python syntax
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True
        )
        
        passed = result.returncode == 0
        self.log_test(
            "Donor hash script Python syntax",
            passed,
            "Syntax error" if not passed else "Valid Python"
        )
        return passed
    
    def test_donor_hash_functionality(self):
        """Test that donor_hash.py generates proper hashes"""
        script_path = self.script_dir / "donor_hash.py"
        
        if not script_path.exists():
            self.log_test("Donor hash functionality", False, "Script not found")
            return False
        
        # Test that script requires correct arguments
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Should exit with error if no args provided
        has_usage = "Usage:" in result.stdout or "Usage:" in result.stderr
        passed = result.returncode != 0 and has_usage
        
        self.log_test(
            "Donor hash script argument validation",
            passed,
            "Script validates input arguments"
        )
        return passed
    
    def test_irs_audit_generator_syntax(self):
        """Test that irs_audit_generator.py has valid Python syntax"""
        script_path = self.script_dir / "irs_audit_generator.py"
        
        if not script_path.exists():
            self.log_test("IRS audit generator exists", False, "File not found")
            return False
        
        # Check Python syntax
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True
        )
        
        passed = result.returncode == 0
        self.log_test(
            "IRS audit generator Python syntax",
            passed,
            "Syntax error" if not passed else "Valid Python"
        )
        return passed
    
    def test_irs_audit_generator_functionality(self):
        """Test that irs_audit_generator.py generates audit packages"""
        script_path = self.script_dir / "irs_audit_generator.py"
        
        if not script_path.exists():
            self.log_test("IRS audit generator functionality", False, "Script not found")
            return False
        
        # Test generation in temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                
                # Run generator
                result = subprocess.run(
                    [sys.executable, str(script_path), "2025"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # Check for success indicators
                success = result.returncode == 0
                output_dir = Path(tmpdir) / "irs_audit_2025"
                dir_created = output_dir.exists()
                
                required_files = [
                    "990_pf_summary.md",
                    "valorield_proof.md",
                    "board_minutes_compilation.md",
                    "donor_registry_anonymized.md",
                    "MASTER_INDEX.md"
                ]
                
                files_created = all((output_dir / f).exists() for f in required_files) if dir_created else False
                
                passed = success and dir_created and files_created
                
                self.log_test(
                    "IRS audit generator creates package",
                    passed,
                    f"Success: {success}, Dir: {dir_created}, Files: {files_created}"
                )
                
                return passed
            finally:
                os.chdir(old_cwd)
    
    def test_court_defense_boilerplate_content(self):
        """Test that court_defense_boilerplate.md has required content"""
        template_path = self.script_dir / "court_defense_boilerplate.md"
        
        if not template_path.exists():
            self.log_test("Court defense boilerplate exists", False, "File not found")
            return False
        
        content = template_path.read_text()
        
        required_sections = [
            "Wyoming DAO LLC Filing",
            "EIN 39-2923503",
            "Board Minute",
            "Donor Record",
            "Zero Cloud Dependency",
            "ValorYield",
            "Texas Anti-SLAPP"
        ]
        
        has_sections = all(section in content for section in required_sections)
        has_filing = "2025-001708194" in content
        has_gpg = "9F3A 2C8B D407 1810" in content
        
        passed = has_sections and has_filing and has_gpg
        
        self.log_test(
            "Court defense boilerplate content",
            passed,
            f"Sections: {has_sections}, Filing#: {has_filing}, GPG: {has_gpg}"
        )
        return passed
    
    def test_orchestra_script_exists(self):
        """Test that _Orchestra.ps1 orchestration script exists"""
        orchestra_path = self.repo_root / "_Orchestra.ps1"
        exists = orchestra_path.exists()
        
        if exists:
            content = orchestra_path.read_text()
            has_final_seal = "FinalNonprofitSeal" in content
            has_immortalize = "ImmortalizeDonors" in content
            has_irs_audit = "GenerateIrsAudit" in content
            has_nuclear = "NuclearDefense" in content
            
            passed = has_final_seal and has_immortalize and has_irs_audit and has_nuclear
            
            self.log_test(
                "_Orchestra.ps1 orchestration commands",
                passed,
                f"Seal: {has_final_seal}, Donors: {has_immortalize}, IRS: {has_irs_audit}, Nuclear: {has_nuclear}"
            )
        else:
            self.log_test("_Orchestra.ps1 exists", False, "File not found")
            passed = False
        
        return passed
    
    def test_readme_exists(self):
        """Test that README.md documentation exists"""
        readme_path = self.script_dir / "README.md"
        exists = readme_path.exists()
        
        if exists:
            content = readme_path.read_text()
            has_usage = "Usage:" in content or "usage:" in content.lower()
            has_ein = "39-2923503" in content
            
            passed = has_usage and has_ein
            self.log_test(
                "README.md documentation",
                passed,
                f"Has usage docs: {has_usage}, Has EIN: {has_ein}"
            )
        else:
            self.log_test("README.md exists", False, "File not found")
            passed = False
        
        return passed
    
    def run_all_tests(self):
        """Run all tests and report results"""
        print("\n" + "="*60)
        print("🏛️  NONPROFIT FINAL ARTIFACTS TEST SUITE")
        print("    Strategickhaos DAO LLC | EIN 39-2923503")
        print("="*60 + "\n")
        
        # Run all tests
        tests = [
            self.test_artifacts_directory_exists,
            self.test_minutes_template_exists,
            self.test_donor_hash_script_syntax,
            self.test_donor_hash_functionality,
            self.test_irs_audit_generator_syntax,
            self.test_irs_audit_generator_functionality,
            self.test_court_defense_boilerplate_content,
            self.test_orchestra_script_exists,
            self.test_readme_exists,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, f"Exception: {str(e)}")
        
        # Summary
        print("\n" + "="*60)
        total = len(self.test_results)
        passed = sum(1 for _, p in self.test_results if p)
        failed = total - passed
        
        print(f"RESULTS: {passed}/{total} tests passed")
        
        if failed > 0:
            print(f"{YELLOW}⚠ {failed} tests failed{RESET}")
            print("\nFailed tests:")
            for name, result in self.test_results:
                if not result:
                    print(f"  - {name}")
        else:
            print(f"{GREEN}✅ All tests passed!{RESET}")
        
        print("="*60 + "\n")
        
        return failed == 0

if __name__ == "__main__":
    tester = NonprofitArtifactsTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
