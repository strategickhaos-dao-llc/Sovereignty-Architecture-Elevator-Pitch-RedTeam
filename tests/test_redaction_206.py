# tests/test_redaction_206.py
import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_redaction_returns_206():
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": "Bearer ey...normal_user_token..."}
        resp = await client.get("/artifacts/3548", headers=headers)
        assert resp.status_code == 206
        data = resp.json()
        assert data["redacted"] is True
        assert "soul-level entanglement" in data["reason"]


@pytest.mark.asyncio
async def test_love_override_bypasses():
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": "Bearer ey...DOM_010101_token..."}
        resp = await client.get("/artifacts/3548", headers=headers)
        assert resp.status_code == 200
        assert "Empire Eternal" in resp.json()["summary"]
