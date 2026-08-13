"""Tests for patient endpoints."""

from fastapi.testclient import TestClient

from database import get_db
from main import app


def test_create_and_get_patient(db_session, monkeypatch):
    """Create a patient and exercise list/get endpoints."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr("database.get_db", override_get_db)
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    # create
    resp = client.post(
        "/patients",
        json={"name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Alice"

    # list
    resp = client.get("/patients")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # get by id
    pid = data["id"]
    resp = client.get(f"/patients/{pid}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"
