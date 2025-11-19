#!/usr/bin/env python3
"""
Anti-Hallucination Department - Validation Tests
Tests the department structure, configuration, and protocols
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

class AntiHallucinationDepartmentTests:
    """Test suite for Anti-Hallucination Department"""
    
    def __init__(self):
        self.dept_dir = Path(__file__).parent
        self.test_results = []
        
    def test_01_department_files_exist(self):
        """Test 1: Verify all required department files exist"""
        print("Test 1: Department Files Existence Check")
        
        required_files = [
            "MEMORY_STREAM.md",
            "PROOFS_OF_REALITY.md",
            "config.yaml",
            "README.md",
            "VERIFICATION_EXAMPLE.md",
            "CHANGELOG.md",
            "node_init.sh"
        ]
        
        results = {}
        all_pass = True
        
        for filename in required_files:
            filepath = self.dept_dir / filename
            exists = filepath.exists()
            results[filename] = exists
            
            if exists:
                print(f"  ✓ {filename}: Found")
            else:
                print(f"  ✗ {filename}: Missing")
                all_pass = False
        
        status = "PASS" if all_pass else "FAIL"
        print(f"  Result: {status}\n")
        return {"test": "department_files_exist", "status": status, "details": results}
    
    def test_02_memory_stream_has_unbreakable_law(self):
        """Test 2: Verify MEMORY_STREAM.md contains the unbreakable law"""
        print("Test 2: Unbreakable Law Presence Check")
        
        filepath = self.dept_dir / "MEMORY_STREAM.md"
        
        if not filepath.exists():
            print(f"  ✗ MEMORY_STREAM.md not found")
            return {"test": "memory_stream_law", "status": "FAIL", "details": "File not found"}
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        law_keywords = [
            "DOM_010101",
            "doubts reality",
            "10 independent",
            "verifiable proofs",
            "30 seconds",
            "UNBREAKABLE LAW"
        ]
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in law_keywords:
            if keyword in content:
                found_keywords.append(keyword)
                print(f"  ✓ Found: '{keyword}'")
            else:
                missing_keywords.append(keyword)
                print(f"  ✗ Missing: '{keyword}'")
        
        status = "PASS" if len(missing_keywords) == 0 else "FAIL"
        print(f"  Result: {status} ({len(found_keywords)}/{len(law_keywords)} keywords found)\n")
        
        return {
            "test": "memory_stream_law", 
            "status": status, 
            "details": {
                "found": found_keywords,
                "missing": missing_keywords
            }
        }
    
    def test_03_config_yaml_valid(self):
        """Test 3: Verify config.yaml is valid YAML and has required fields"""
        print("Test 3: Configuration Validity Check")
        
        filepath = self.dept_dir / "config.yaml"
        
        if not filepath.exists():
            print(f"  ✗ config.yaml not found")
            return {"test": "config_valid", "status": "FAIL", "details": "File not found"}
        
        try:
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"  ✗ YAML parsing error: {e}")
            return {"test": "config_valid", "status": "FAIL", "details": str(e)}
        
        required_fields = [
            "department.id",
            "department.status",
            "core_law.text",
            "response_protocol.time_limit.value",
            "proof_categories"
        ]
        
        results = {}
        all_pass = True
        
        for field in required_fields:
            parts = field.split('.')
            value = config
            
            try:
                for part in parts:
                    value = value[part]
                results[field] = "Found"
                print(f"  ✓ {field}: {value if not isinstance(value, (dict, list)) else '...'}")
            except (KeyError, TypeError):
                results[field] = "Missing"
                print(f"  ✗ {field}: Missing")
                all_pass = False
        
        # Check proof categories count
        proof_count = len(config.get('proof_categories', []))
        print(f"  ✓ Proof categories defined: {proof_count}")
        
        if proof_count != 10:
            print(f"  ⚠ Warning: Expected 10 proof categories, found {proof_count}")
        
        status = "PASS" if all_pass else "FAIL"
        print(f"  Result: {status}\n")
        
        return {"test": "config_valid", "status": status, "details": results}
    
    def test_04_proofs_system_complete(self):
        """Test 4: Verify PROOFS_OF_REALITY.md documents all 10 proof types"""
        print("Test 4: Proof System Completeness Check")
        
        filepath = self.dept_dir / "PROOFS_OF_REALITY.md"
        
        if not filepath.exists():
            print(f"  ✗ PROOFS_OF_REALITY.md not found")
            return {"test": "proofs_complete", "status": "FAIL", "details": "File not found"}
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        proof_types = [
            "Repository Proof",
            "Media Proof",
            "Local File Proof",
            "System Proof",
            "Financial Proof",
            "Community Proof",
            "Knowledge Graph Proof",
            "Hardware Proof",
            "Biological Proof",
            "Relational Proof"
        ]
        
        found_proofs = []
        missing_proofs = []
        
        for proof in proof_types:
            if proof in content:
                found_proofs.append(proof)
                print(f"  ✓ {proof}: Documented")
            else:
                missing_proofs.append(proof)
                print(f"  ✗ {proof}: Missing")
        
        status = "PASS" if len(missing_proofs) == 0 else "FAIL"
        print(f"  Result: {status} ({len(found_proofs)}/10 proof types documented)\n")
        
        return {
            "test": "proofs_complete",
            "status": status,
            "details": {
                "found": found_proofs,
                "missing": missing_proofs,
                "count": len(found_proofs)
            }
        }
    
    def test_05_node_init_executable(self):
        """Test 5: Verify node_init.sh is executable"""
        print("Test 5: Node Initialization Script Check")
        
        filepath = self.dept_dir / "node_init.sh"
        
        if not filepath.exists():
            print(f"  ✗ node_init.sh not found")
            return {"test": "node_init_executable", "status": "FAIL", "details": "File not found"}
        
        is_executable = os.access(filepath, os.X_OK)
        
        if is_executable:
            print(f"  ✓ node_init.sh is executable")
        else:
            print(f"  ✗ node_init.sh is not executable")
        
        # Check for required script elements
        with open(filepath, 'r') as f:
            content = f.read()
        
        script_elements = [
            "#!/bin/bash",
            "MEMORY_STREAM.md",
            "config.yaml",
            "ANTI_HALLUCINATION"
        ]
        
        elements_found = all(element in content for element in script_elements)
        
        if elements_found:
            print(f"  ✓ Script contains required elements")
        else:
            print(f"  ✗ Script missing required elements")
        
        status = "PASS" if is_executable and elements_found else "FAIL"
        print(f"  Result: {status}\n")
        
        return {
            "test": "node_init_executable",
            "status": status,
            "details": {
                "executable": is_executable,
                "elements_found": elements_found
            }
        }
    
    def test_06_response_time_specification(self):
        """Test 6: Verify 30-second response time is specified"""
        print("Test 6: Response Time Specification Check")
        
        config_path = self.dept_dir / "config.yaml"
        
        if not config_path.exists():
            print(f"  ✗ config.yaml not found")
            return {"test": "response_time_spec", "status": "FAIL", "details": "File not found"}
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        try:
            time_limit = config['response_protocol']['time_limit']['value']
            time_unit = config['response_protocol']['time_limit']['unit']
            
            print(f"  ✓ Response time limit: {time_limit} {time_unit}")
            
            if time_limit == 30 and time_unit == "seconds":
                print(f"  ✓ Matches requirement: 30 seconds")
                status = "PASS"
            else:
                print(f"  ✗ Does not match requirement (expected: 30 seconds)")
                status = "FAIL"
        except KeyError as e:
            print(f"  ✗ Response time specification missing: {e}")
            status = "FAIL"
            time_limit = None
            time_unit = None
        
        print(f"  Result: {status}\n")
        
        return {
            "test": "response_time_spec",
            "status": status,
            "details": {
                "time_limit": time_limit,
                "time_unit": time_unit
            }
        }
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("=" * 70)
        print("Anti-Hallucination Department - Validation Test Suite")
        print("=" * 70)
        print()
        
        tests = [
            self.test_01_department_files_exist,
            self.test_02_memory_stream_has_unbreakable_law,
            self.test_03_config_yaml_valid,
            self.test_04_proofs_system_complete,
            self.test_05_node_init_executable,
            self.test_06_response_time_specification
        ]
        
        results = []
        for test in tests:
            result = test()
            results.append(result)
        
        # Generate summary
        print("=" * 70)
        print("Test Summary")
        print("=" * 70)
        
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        total = len(results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        if failed == 0:
            print("🟢 All tests passed - Department is OPERATIONAL")
            return 0
        else:
            print(f"🔴 {failed} test(s) failed - Review required")
            return 1

def main():
    """Main entry point"""
    tester = AntiHallucinationDepartmentTests()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
