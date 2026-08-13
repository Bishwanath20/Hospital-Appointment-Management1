"""Appointment business logic and helpers."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models


def create_appointment(db: Session, appointment_in):
    """Create an appointment after validating times and overlap rules."""
    # check times
    start = appointment_in.appointment_start
    end = appointment_in.appointment_end
    if not isinstance(start, datetime) or not isinstance(end, datetime) or start >= end:
        raise HTTPException(status_code=400, detail="Invalid appointment range")

    # overlapping check for same doctor
    overlapping = (
        db.query(models.appointment.Appointment)
        .filter(
            models.appointment.Appointment.doctor_id == appointment_in.doctor_id,
            models.appointment.Appointment.appointment_start < end,
            models.appointment.Appointment.appointment_end > start,
        )
        .first()
    )
    if overlapping:
        raise HTTPException(
            status_code=400, detail="Overlapping appointment for this doctor"
        )

    appt = models.appointment.Appointment(**appointment_in.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt
