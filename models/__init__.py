"""Models package exports for SQLAlchemy mappers.

Import model modules here so SQLAlchemy registers mappers when the
package is imported by Alembic or application startup code.
"""

from database import Base

# Import model classes so SQLAlchemy mappers are registered when `models` is imported
from .appointment import Appointment
from .doctor import Doctor
from .patient import Patient

__all__ = ["Appointment", "Base", "Doctor", "Patient"]
