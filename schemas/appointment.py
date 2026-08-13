"""Pydantic schemas for appointment create/read models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    """Schema for creating an appointment."""

    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime


class AppointmentRead(AppointmentCreate):
    id: int

    """Read schema for an appointment including the database `id`."""

    model_config = ConfigDict(from_attributes=True)
