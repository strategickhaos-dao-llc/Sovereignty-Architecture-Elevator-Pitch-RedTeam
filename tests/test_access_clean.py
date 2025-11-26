# tests/test_access_clean.py
import pytest


@pytest.mark.asyncio
async def test_full_access(client, authorized_token):
    resp = await client.get("/artifacts/3552", headers={"Authorization": f"Bearer {authorized_token}"})
    assert resp.status_code == 200
    assert "Empire Eternal" in resp.json()["summary"]


@pytest.mark.asyncio
async def test_redaction_206(client, partial_token):
    resp = await client.get("/artifacts/3552", headers={"Authorization": f"Bearer {partial_token}"})
    assert resp.status_code == 206
    data = resp.json()
    assert data["redacted"] is True
    assert data["visible_preview"] == "Empire Eternal – access restricted by policy"


@pytest.mark.asyncio
async def test_deny_403(client, unauthorized_token):
    resp = await client.get("/artifacts/3552", headers={"Authorization": f"Bearer {unauthorized_token}"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_audit_contains_no_backdoor_terms(get_audit_logs):
    logs = get_audit_logs()
    log_text = str(logs).lower()
    assert "love" not in log_text
    assert "backdoor" not in log_text
    assert "soul" not in log_text
