"""Pydantic schemas for doctor create/read models."""

from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    """Schema used to create a new `Doctor`."""

    name: str
    specialization: str | None = None


class DoctorRead(DoctorCreate):
    id: int

    """Read/response schema for a `Doctor` including the `id`."""

    model_config = ConfigDict(from_attributes=True)
