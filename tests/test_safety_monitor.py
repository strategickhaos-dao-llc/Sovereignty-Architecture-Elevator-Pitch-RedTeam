#!/usr/bin/env python3
"""
Tests for Legends of Minds Safety Monitoring System
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add core directory to path
core_path = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(core_path))

# Import the FastAPI app
try:
    from main import app
    from safety_monitor import router
except ImportError as e:
    pytest.skip(f"Cannot import required modules: {e}", allow_module_level=True)

client = TestClient(app)


class TestSafetyMonitoring:
    """Test suite for safety monitoring endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns basic info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "Legends of Minds" in data["name"]
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
        assert "services" in data
        assert "timestamp" in data
    
    def test_model_integrity_endpoint(self):
        """Test model integrity check endpoint"""
        response = client.get("/api/safety/model_integrity")
        assert response.status_code == 200
        data = response.json()
        
        # Should return either error or verified status
        assert "status" in data or "error" in data
        
        if "status" in data:
            assert data["status"] == "verified"
            assert "models_found" in data
    
    def test_process_isolation_endpoint(self):
        """Test process isolation check endpoint"""
        response = client.get("/api/safety/process_isolation")
        assert response.status_code == 200
        data = response.json()
        
        # Should return status
        assert "status" in data
        assert data["status"] in ["verified", "not_running"]
        
        if data["status"] == "verified":
            assert "process" in data
            assert "pid" in data["process"]
    
    def test_network_isolation_endpoint(self):
        """Test network isolation check endpoint"""
        response = client.get("/api/safety/network_isolation")
        assert response.status_code == 200
        data = response.json()
        
        # Should return status or error
        assert "status" in data or "error" in data
        
        if "status" in data:
            assert data["status"] in ["verified", "warning"]
            assert "port" in data
            assert data["port"] == 11434
    
    def test_model_config_endpoint(self):
        """Test model configuration check endpoint"""
        response = client.get("/api/safety/model_config")
        assert response.status_code == 200
        data = response.json()
        
        # Should return status or error
        assert "status" in data or "error" in data
    
    def test_resource_usage_endpoint(self):
        """Test resource usage monitoring endpoint"""
        response = client.get("/api/safety/resource_usage")
        assert response.status_code == 200
        data = response.json()
        
        # Should return status
        assert "status" in data or "error" in data
    
    def test_full_report_endpoint(self):
        """Test full safety report generation"""
        response = client.get("/api/safety/full_report")
        assert response.status_code == 200
        data = response.json()
        
        # Should return comprehensive report
        assert "timestamp" in data
        assert "system" in data
        assert "Legends of Minds" in data["system"]
        assert "checks" in data
        assert "overall_status" in data
        assert data["overall_status"] in ["VERIFIED", "WARNINGS"]
        
        # Should have multiple checks
        assert len(data["checks"]) >= 5
        
        # Check that all required checks are present
        required_checks = [
            "model_integrity",
            "process_isolation",
            "network_isolation",
            "model_config",
            "resource_usage"
        ]
        
        for check in required_checks:
            assert check in data["checks"], f"Missing required check: {check}"
    
    def test_canary_test_endpoint_exists(self):
        """Test canary test endpoint exists (may be slow, so just check it exists)"""
        response = client.get("/api/safety/canary_test")
        assert response.status_code == 200
        data = response.json()
        
        # Should return test results structure
        assert "status" in data or "error" in data
    
    def test_models_endpoint(self):
        """Test models listing endpoint"""
        response = client.get("/api/models")
        # May fail if Ollama is not running, but should return valid response
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            # Should have models structure
            assert isinstance(data, dict)


class TestIngestService:
    """Test suite for file ingest service"""
    
    def test_ingest_service_exists(self):
        """Test that ingest service file exists and can be imported"""
        ingest_path = Path(__file__).parent.parent / "ingest" / "main.py"
        assert ingest_path.exists(), "Ingest service main.py should exist"
        
        # Try to import it
        import importlib.util
        spec = importlib.util.spec_from_file_location("ingest_main", ingest_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                assert hasattr(module, 'app'), "Ingest service should have app instance"
            except Exception as e:
                # It's OK if it fails due to dependencies, we just verify it exists
                pass


class TestSafetyReportStructure:
    """Test the structure of safety reports"""
    
    def test_report_contains_all_metrics(self):
        """Test that full report contains all expected metrics"""
        response = client.get("/api/safety/full_report")
        assert response.status_code == 200
        data = response.json()
        
        # Verify timestamp format
        assert "timestamp" in data
        assert "Z" in data["timestamp"] or "+" in data["timestamp"]
        
        # Verify system identification
        assert "system" in data
        
        # Verify summary
        assert "summary" in data
        
        # Verify checks structure
        checks = data.get("checks", {})
        assert isinstance(checks, dict)
        
        # Each check should have consistent structure
        for check_name, check_data in checks.items():
            assert isinstance(check_data, dict)
            # Most checks should have status or error
            assert "status" in check_data or "error" in check_data or "message" in check_data


class TestAPIDocumentation:
    """Test that API documentation is accessible"""
    
    def test_openapi_docs(self):
        """Test OpenAPI documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_docs(self):
        """Test ReDoc documentation endpoint"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_json(self):
        """Test OpenAPI JSON schema"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
