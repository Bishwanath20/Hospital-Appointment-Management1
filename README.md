# Hospital Appointment Management API

This repository implements a FastAPI application for managing patients, doctors, and appointments with an overlap-prevention business rule.

Key features:
- FastAPI + Pydantic
- SQLAlchemy ORM and Alembic migrations
- Overlapping appointments prevented per-doctor
- Tests with pytest and coverage (>=85% required in CI)
- Linting (flake8) and security scan (Bandit) in CI
- Docker image build and publish to Docker Hub via GitHub Actions

See `.github/workflows/ci.yml` for the CI pipeline; set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets to enable publishing.

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Run tests:

```bash
pytest --cov=.
```
