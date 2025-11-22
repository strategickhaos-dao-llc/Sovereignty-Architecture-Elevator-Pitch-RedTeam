#!/usr/bin/env python3
"""
Privacy Search Node Tests
Strategic Khaos - Distributed AI Intelligence Layer
"""

import pytest
from fastapi.testclient import TestClient
import os
import tempfile
import json


def test_app_imports():
    """Test that the FastAPI app can be imported successfully."""
    from main import app
    assert app is not None
    assert app.title == "Privacy Search Node"


def test_routes_exist():
    """Test that all expected routes are defined."""
    from main import app
    
    expected_routes = {"/search", "/browse", "/health"}
    actual_routes = {route.path for route in app.routes if hasattr(route, 'path')}
    
    for route in expected_routes:
        assert route in actual_routes, f"Route {route} not found"


def test_health_endpoint():
    """Test the /health endpoint returns expected structure."""
    from main import app
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "exit_ip" in data
    assert data["status"] == "healthy"


def test_search_endpoint_requires_query():
    """Test that /search endpoint requires 'q' parameter."""
    from main import app
    
    client = TestClient(app)
    response = client.get("/search")
    
    # Should return 422 Unprocessable Entity without required parameter
    assert response.status_code == 422


def test_browse_endpoint_requires_url():
    """Test that /browse endpoint requires 'url' parameter."""
    from main import app
    
    client = TestClient(app)
    response = client.get("/browse")
    
    # Should return 422 Unprocessable Entity without required parameter
    assert response.status_code == 422


def test_search_endpoint_structure():
    """Test that /search endpoint returns expected structure (mocked)."""
    from main import app
    from unittest.mock import patch, MagicMock
    
    # Mock DDGS to avoid actual network requests
    mock_results = [
        {"title": "Test Result", "href": "https://example.com", "body": "Test description"}
    ]
    
    with patch('main.DDGS') as mock_ddgs:
        mock_instance = MagicMock()
        mock_instance.__enter__ = MagicMock(return_value=mock_instance)
        mock_instance.__exit__ = MagicMock(return_value=False)
        mock_instance.text = MagicMock(return_value=mock_results)
        mock_ddgs.return_value = mock_instance
        
        # Create temp log directory
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "events.jsonl")
            
            with patch('main.psyche_log') as mock_log:
                client = TestClient(app)
                response = client.get("/search?q=test&max_results=5")
                
                assert response.status_code == 200
                data = response.json()
                assert "query" in data
                assert "results" in data
                assert data["query"] == "test"
                assert isinstance(data["results"], list)


def test_openapi_docs_available():
    """Test that OpenAPI docs are accessible."""
    from main import app
    
    client = TestClient(app)
    
    # Test OpenAPI JSON
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert "openapi" in openapi_spec
    assert "info" in openapi_spec
    
    # Test Swagger UI
    response = client.get("/docs")
    assert response.status_code == 200


def test_psyche_log_function(monkeypatch):
    """Test that psyche_log function works correctly."""
    from main import psyche_log
    import tempfile
    import json
    
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "events.jsonl")
        
        # Patch the LOG_FILE constant
        import main
        monkeypatch.setattr("main.LOG_FILE", log_file)
        
        # Write a log entry
        psyche_log("test_event", test_param="test_value")
        
        # Read and verify
        with open(log_file, "r") as f:
            log_entry = json.loads(f.readline())
            assert log_entry["event"] == "test_event"
            assert log_entry["test_param"] == "test_value"
            assert "timestamp" in log_entry


def test_ssrf_protection_rejects_localhost():
    """Test that SSRF protection rejects localhost URLs."""
    from main import app
    
    client = TestClient(app)
    
    # Test various localhost URLs
    unsafe_urls = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://0.0.0.0:8080",
    ]
    
    for unsafe_url in unsafe_urls:
        response = client.get(f"/browse?url={unsafe_url}")
        assert response.status_code == 400
        assert "unsafe" in response.json()["detail"].lower()


def test_ssrf_protection_rejects_private_ips():
    """Test that SSRF protection rejects private IP ranges."""
    from main import app
    
    client = TestClient(app)
    
    # Test various private IP ranges
    unsafe_urls = [
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://172.16.0.1",
    ]
    
    for unsafe_url in unsafe_urls:
        response = client.get(f"/browse?url={unsafe_url}")
        assert response.status_code == 400
        assert "unsafe" in response.json()["detail"].lower()


def test_ssrf_protection_allows_public_urls():
    """Test that SSRF protection allows legitimate public URLs."""
    from main import is_safe_url
    
    # Test legitimate public URLs
    safe_urls = [
        "https://example.com",
        "https://www.google.com",
        "http://public-site.org",
    ]
    
    for safe_url in safe_urls:
        assert is_safe_url(safe_url) == True


def test_ssrf_protection_rejects_invalid_schemes():
    """Test that SSRF protection rejects invalid URL schemes."""
    from main import is_safe_url
    
    unsafe_urls = [
        "file:///etc/passwd",
        "ftp://internal-server.local",
        "gopher://example.com",
    ]
    
    for unsafe_url in unsafe_urls:
        assert is_safe_url(unsafe_url) == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
