# tests/conftest.py
"""Pytest configuration and fixtures for artifact access control tests."""
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

# Mock the database and artifact lookup before importing main
import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_artifact():
    """Create a mock artifact for testing."""
    from models import Artifact
    return Artifact(
        id="3552",
        classification="Secret",
        summary="Empire Eternal - Sovereign Architecture Document",
        content="Full classified content here",
        need_to_know=[]
    )


@pytest.fixture
def authorized_token():
    """Token for full access user."""
    return "full_access_token"


@pytest.fixture
def partial_token():
    """Token for partial access user."""
    return "partial_access_token"


@pytest.fixture
def unauthorized_token():
    """Token for unauthorized user."""
    return "unauthorized_token"


@pytest_asyncio.fixture
async def client(mock_artifact):
    """Async HTTP client for testing with mocked database."""
    from main import app
    
    # Create a mock session that returns our test artifact
    mock_result = MagicMock()
    mock_result.one_or_none.return_value = mock_artifact
    
    mock_session = AsyncMock()
    mock_session.exec = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    # Patch the async_session context manager
    with patch('routes.artifacts.async_session', return_value=mock_session):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture
def get_audit_logs():
    """Fixture to retrieve audit logs."""
    from audit import get_audit_log
    def _get_logs():
        return get_audit_log()
    return _get_logs


@pytest.fixture(autouse=True)
def reset_audit():
    """Reset audit log before each test."""
    from audit import clear_audit_log
    clear_audit_log()
    yield
    clear_audit_log()
