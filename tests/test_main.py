from fastapi.testclient import TestClient
from app.main import app


def test_app_startup():
    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code == 200