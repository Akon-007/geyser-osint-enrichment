from fastapi.testclient import TestClient
from types import SimpleNamespace
from app import api


def test_authentication_is_enforced_when_configured(monkeypatch):
    monkeypatch.setattr(api, "settings", SimpleNamespace(api_key="secret"))
    client = TestClient(api.app)
    assert client.get("/v1/tools").status_code == 401
    assert client.get("/v1/tools", headers={"X-API-Key": "secret"}).status_code == 200

