"""Pydantic schemas for patient create/read models."""

from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    """Schema for creating a new patient."""

    name: str
    email: str
    phone: str | None = None


class PatientRead(PatientCreate):
    id: int
    """Read schema for a patient including the database `id`."""

    model_config = ConfigDict(from_attributes=True)
