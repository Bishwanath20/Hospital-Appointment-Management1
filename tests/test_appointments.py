"""Tests for appointment creation and overlap prevention."""

# Some tests intentionally use many local variables; disable the warning here.
# pylint: disable=too-many-locals

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from database import get_db
from main import app


def override_get_db_factory(db_session):
    """Return a dependency override that yields the provided DB session."""

    def _override():
        try:
            yield db_session
        finally:
            pass

    return _override


def test_create_appointment_and_prevent_overlap(db_session, monkeypatch):
    """Create an appointment and verify overlapping appointments are rejected."""
    override = override_get_db_factory(db_session)
    monkeypatch.setattr("database.get_db", override)
    app.dependency_overrides[get_db] = override
    client = TestClient(app)

    # create patient and doctor
    p = client.post("/patients", json={"name": "Bob", "email": "bob@example.com"})
    assert p.status_code == 201
    patient_id = p.json()["id"]

    d = client.post("/doctors", json={"name": "Dr. Who", "specialization": "Time"})
    assert d.status_code == 201
    doctor_id = d.json()["id"]

    start1 = datetime.now(timezone.utc).replace(microsecond=0)
    end1 = start1 + timedelta(hours=1)

    # create first appointment
    ap1 = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start1.isoformat(),
            "appointment_end": end1.isoformat(),
        },
    )
    assert ap1.status_code == 201

    # overlapping appointment should be rejected
    start2 = start1 + timedelta(minutes=30)
    end2 = start2 + timedelta(hours=1)
    ap2 = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start2.isoformat(),
            "appointment_end": end2.isoformat(),
        },
    )
    assert ap2.status_code == 400

    # adjacent appointment allowed (end == start)
    start3 = end1
    end3 = start3 + timedelta(hours=1)
    ap3 = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start3.isoformat(),
            "appointment_end": end3.isoformat(),
        },
    )
    assert ap3.status_code == 201
