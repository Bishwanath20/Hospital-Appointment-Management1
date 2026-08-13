"""SQLAlchemy `Patient` model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Patient(Base):
    __tablename__ = "patients"

    """Represents a patient who can book appointments."""

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)

    appointments = relationship(
        "Appointment", back_populates="patient", cascade="all, delete-orphan"
    )
