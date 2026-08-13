"""Pytest fixtures for database-backed tests."""

import os
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure tests use an isolated temporary DB unless overridden
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

# Ensure project root is on sys.path so tests can import top-level modules
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import after env setup; disable import-position lint for the DB binding
from database import Base  # pylint: disable=wrong-import-position


@pytest.fixture(scope="function")
def db_session(tmp_path):
    # use a temporary file-backed SQLite DB so multiple connections share the same schema
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
