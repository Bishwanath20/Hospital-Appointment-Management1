"""Doctor endpoints (list, create, get)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.doctor import DoctorCreate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["doctors"])

# Module-level dependency to satisfy linters (avoid calling Depends in defaults)
get_db_dep = Depends(get_db)


@router.get("", response_model=list[DoctorRead])
def list_doctors(db: Session = get_db_dep):
    """Return a list of doctors."""
    return db.query(models.doctor.Doctor).all()


@router.post("", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, db: Session = get_db_dep):
    """Create a new doctor record and return it."""
    doctor = models.doctor.Doctor(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = get_db_dep):
    """Return a doctor by id or raise 404."""
    doctor = db.get(models.doctor.Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
