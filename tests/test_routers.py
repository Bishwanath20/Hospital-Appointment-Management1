"""Additional router tests to improve coverage for create/list/get paths."""

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from database import get_db
from main import app


def override_get_db_factory(db_session):
    def _override():
        try:
            yield db_session
        finally:
            pass

    return _override


def test_doctor_create_list_get_and_not_found(db_session, monkeypatch):
    """Create a doctor, list doctors, get by id, and verify 404 for missing."""
    override = override_get_db_factory(db_session)
    monkeypatch.setattr("database.get_db", override)
    app.dependency_overrides[get_db] = override
    client = TestClient(app)

    # initially empty
    resp = client.get("/doctors")
    assert resp.status_code == 200

    # create
    r = client.post("/doctors", json={"name": "Dr. Strange"})
    assert r.status_code == 201
    did = r.json()["id"]

    # list contains created doctor
    resp = client.get("/doctors")
    assert resp.status_code == 200
    assert any(d["id"] == did for d in resp.json())

    # get by id
    resp = client.get(f"/doctors/{did}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Dr. Strange"

    # missing id returns 404
    resp = client.get("/doctors/9999")
    assert resp.status_code == 404


def test_appointment_fk_checks_and_not_found(db_session, monkeypatch):
    """Verify appointment creation validates patient/doctor FKs and 404s."""
    override = override_get_db_factory(db_session)
    monkeypatch.setattr("database.get_db", override)
    app.dependency_overrides[get_db] = override
    client = TestClient(app)

    # ensure no appointments initially
    resp = client.get("/appointments")
    assert resp.status_code == 200

    start = datetime.now(timezone.utc).replace(microsecond=0)
    end = start + timedelta(hours=1)

    # create appointment with missing patient -> 404
    r = client.post(
        "/appointments",
        json={
            "patient_id": 9999,
            "doctor_id": 1,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        },
    )
    assert r.status_code == 404

    # create a patient and doctor then create appointment
    p = client.post("/patients", json={"name": "P", "email": "p@x.com"})
    assert p.status_code == 201
    pid = p.json()["id"]
    d = client.post("/doctors", json={"name": "D"})
    assert d.status_code == 201
    did = d.json()["id"]

    r = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        },
    )
    assert r.status_code == 201
    aid = r.json()["id"]

    # get created appointment
    resp = client.get(f"/appointments/{aid}")
    assert resp.status_code == 200

    # missing appointment returns 404
    resp = client.get("/appointments/9999")
    assert resp.status_code == 404
