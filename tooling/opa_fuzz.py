#!/usr/bin/env python3
"""
OPA Policy Fuzz Harness - Schema-aware testing for access policies
Strategickhaos DAO LLC - Security Policy Validation

Features:
- Generates valid and invalid inputs for OPA policy testing
- Schema-aware structured mutation
- Failure logging with full audit trail
- Coverage metrics for policy outcomes
"""

import random
import json
import subprocess
import os
import sys
import tempfile
from pathlib import Path

# --- SCHEMA: expected for access policy ---
ROLE_VALUES = ["admin", "owner", "user", "guest"]
BAD_ROLE_VALUES = [123, None, "", [], {}, True, False]
EXTRA_FIELDS = [
    {},
    {"extra": "foo"},
    {"note": "bar"},
    {"role": "user", "unexpected": "value"},
]


def gen_input(valid=True):
    """Generate structured input for policy testing.
    
    Args:
        valid: If True, generate valid inputs. If False, generate adversarial inputs.
    
    Returns:
        dict: Input data for policy evaluation
    """
    if valid:
        return {"role": random.choice(ROLE_VALUES)}
    else:
        fields = []
        # Pick a bad role value and randomly add extras/missing fields
        fields.append({"role": random.choice(BAD_ROLE_VALUES)})
        fields.append({})
        fields.append({"unexpected": random.randint(1, 100)})
        fields.extend(EXTRA_FIELDS)
        return random.choice(fields)


def parse_opa_result(output):
    """Parse OPA eval output to extract the boolean result.
    
    OPA eval returns JSON in the format:
    {"result": [{"expressions": [{"value": true|false, ...}]}]}
    
    Args:
        output: Raw stdout from OPA eval command
    
    Returns:
        bool or None: The policy result (True if allowed, False if denied, None if parse error)
    """
    if not output:
        return None
    try:
        data = json.loads(output)
        # Navigate the OPA result structure
        if "result" in data and len(data["result"]) > 0:
            expressions = data["result"][0].get("expressions", [])
            if expressions and len(expressions) > 0:
                value = expressions[0].get("value")
                if isinstance(value, bool):
                    return value
        return None
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return None


def run_opa_eval(input_data, idx, policy_path="policies/access.rego"):
    """Run OPA evaluation on input data.
    
    Args:
        input_data: Dictionary of input data for policy
        idx: Index for temporary file naming
        policy_path: Path to the OPA policy file
    
    Returns:
        dict: Result including input, output, error, and success status
    """
    # Use tempfile for secure temporary file creation
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', prefix=f'opa_input_{idx}_', delete=False
    ) as f:
        json.dump(input_data, f)
        input_file = f.name
    
    try:
        proc = subprocess.run(
            ["opa", "eval", "-i", input_file, "-d", policy_path, "data.access.allow"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = proc.stdout.strip()
        error = proc.stderr.strip()
        success = proc.returncode == 0
    except subprocess.TimeoutExpired:
        output = ""
        error = "Timeout expired"
        success = False
    except FileNotFoundError:
        output = ""
        error = "OPA binary not found. Please install OPA: https://www.openpolicyagent.org/docs/latest/#1-download-opa"
        success = False
    except Exception as e:
        output = ""
        error = str(e)
        success = False
    finally:
        # Clean up temporary file
        try:
            os.remove(input_file)
        except OSError:
            pass
    
    return {
        "input": input_data,
        "output": output,
        "error": error,
        "success": success
    }


def is_suspicious(result):
    """Flag suspicious policy outcomes.
    
    Suspicious cases include:
    - Non-admin/owner getting allowed
    - Errors during policy evaluation
    - Admin/owner being denied
    - Invalid roles getting allowed
    
    Args:
        result: Dictionary with policy evaluation result
    
    Returns:
        bool: True if the result is suspicious
    """
    # Parse OPA output as JSON to reliably extract the boolean result
    parsed_result = parse_opa_result(result["output"])
    allowed = parsed_result is True
    role = result["input"].get("role")
    
    if role in ["admin", "owner"]:
        # Should always allow
        return not allowed or not result["success"] or bool(result["error"])
    elif role in ["user", "guest"]:
        # Should always deny
        return allowed or not result["success"] or bool(result["error"])
    else:
        # Non-string/unexpected roles should always be denied
        return allowed or not result["success"] or bool(result["error"])


def run_fuzz_campaign(num_valid=20, num_invalid=20, policy_path="policies/access.rego"):
    """Run a fuzz testing campaign against OPA policies.
    
    Args:
        num_valid: Number of valid input tests to run
        num_invalid: Number of invalid input tests to run
        policy_path: Path to the OPA policy file
    
    Returns:
        tuple: (results list, coverage stats dict, suspicious findings list)
    """
    results = []
    
    # Run valid input tests
    for idx in range(num_valid):
        inp = gen_input(True)
        res = run_opa_eval(inp, idx, policy_path)
        res["fuzz_type"] = "valid"
        res["suspicious"] = is_suspicious(res)
        results.append(res)
    
    # Run invalid input tests
    for idx in range(num_invalid):
        inp = gen_input(False)
        res = run_opa_eval(inp, num_valid + idx, policy_path)
        res["fuzz_type"] = "invalid"
        res["suspicious"] = is_suspicious(res)
        results.append(res)
    
    # Coverage stats - parse OPA output as JSON for accurate results
    allowed = sum(1 for r in results if parse_opa_result(r["output"]) is True)
    denied = sum(1 for r in results if parse_opa_result(r["output"]) is False)
    errors = sum(1 for r in results if r["error"])
    suspicious = [r for r in results if r["suspicious"]]
    
    stats = {
        "total": len(results),
        "allowed": allowed,
        "denied": denied,
        "errors": errors,
        "suspicious_count": len(suspicious)
    }
    
    return results, stats, suspicious


def main():
    """Main entry point for the OPA fuzz harness."""
    # Configuration
    NUM_VALID = 20
    NUM_INVALID = 20
    LOG_PATH = "opa_fuzz_results.json"
    POLICY_PATH = "policies/access.rego"
    
    print("🔍 OPA Policy Fuzz Harness - Starting...")
    print(f"   Policy: {POLICY_PATH}")
    print(f"   Valid tests: {NUM_VALID}")
    print(f"   Invalid tests: {NUM_INVALID}")
    print()
    
    # Run the fuzz campaign
    results, stats, suspicious = run_fuzz_campaign(
        num_valid=NUM_VALID,
        num_invalid=NUM_INVALID,
        policy_path=POLICY_PATH
    )
    
    # Save results to log file
    with open(LOG_PATH, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"Total runs: {stats['total']}")
    print(f"Allowed: {stats['allowed']}, Denied: {stats['denied']}, Errors: {stats['errors']}")
    print(f"Suspicious findings: {stats['suspicious_count']}")
    
    if suspicious:
        print("\n⚠️  Suspicious (policy/engine bug) examples:")
        for r in suspicious[:5]:
            print(json.dumps(r, indent=2))
        print(f"\nSee full details in {LOG_PATH}")
    else:
        print("\n✅ No suspicious findings detected.")
    
    # Final tip
    print("\n💡 Tip: Use this tool as a nightly/final-stage CI job.")
    print("   Tailor schema checks for new fields or policies!")
    
    return stats['suspicious_count'] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
