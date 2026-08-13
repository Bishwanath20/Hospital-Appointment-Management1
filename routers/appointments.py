"""Appointment endpoints (list, create, get)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.appointment import AppointmentCreate, AppointmentRead
from services.appointments import create_appointment as svc_create

router = APIRouter(prefix="/appointments", tags=["appointments"])

# Module-level dependency to satisfy linters (avoid calling Depends in defaults)
get_db_dep = Depends(get_db)


@router.get("", response_model=list[AppointmentRead])
def list_appointments(db: Session = get_db_dep):
    """Return a list of appointments."""
    return db.query(models.appointment.Appointment).all()


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = get_db_dep):
    """Validate foreign keys and create an appointment via services."""
    # validate foreign keys exist
    patient = db.get(models.patient.Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    doctor = db.get(models.doctor.Doctor, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return svc_create(db, payload)


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: int, db: Session = get_db_dep):
    """Return an appointment by id or raise 404."""
    appt = db.get(models.appointment.Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt
