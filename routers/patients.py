"""Patient endpoints (list, create, get)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.patient import PatientCreate, PatientRead

router = APIRouter(prefix="/patients", tags=["patients"])

# Module-level dependency to satisfy linters (avoid calling Depends in defaults)
get_db_dep = Depends(get_db)


@router.get("", response_model=list[PatientRead])
def list_patients(db: Session = get_db_dep):
    """Return a list of patients."""
    return db.query(models.patient.Patient).all()


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = get_db_dep):
    """Create a new patient and return it."""
    patient = models.patient.Patient(**payload.model_dump())
    db.add(patient)
    try:
        db.commit()
        db.refresh(patient)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    return patient


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = get_db_dep):
    """Return a patient by id or raise 404."""
    patient = db.get(models.patient.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
