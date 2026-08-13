"""SQLAlchemy `Appointment` model."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    """Represents a scheduled appointment between a patient and a doctor.

    Stored times are naive or timezone-aware datetimes depending on the
    application's configuration; tests use UTC-aware datetimes.
    """

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )
    doctor_id = Column(
        Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False
    )
    appointment_start = Column(DateTime, nullable=False)
    appointment_end = Column(DateTime, nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
