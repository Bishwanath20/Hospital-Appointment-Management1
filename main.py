"""FastAPI application factory and router registration with lifespan."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers import appointments, doctors, patients


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan handler: create DB tables on startup for local runs/tests."""
    # ensure tables exist on startup (migrations recommended for production)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Hospital Appointment Management API", lifespan=lifespan)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
