from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from src.app.app import app
from src.shared.environments import env

ABS_ID = "9f1c2a10-6b1e-4d3a-8c55-0a1b2c3d4e02"


@pytest.fixture
def client():
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": "b189d11a-25d1-430e-b5a1-c53db528337e",
            "role": "user",
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=30),
        },
        env.jwt_secret,
        algorithm="HS256",
    )
    client = TestClient(app=app)
    client.cookies.set("access_token", token)
    return client


class TestGetFilamentRoute:
    def test_get_filament(self, client):
        response = client.get(f"/api/filament/get/{ABS_ID}")

        assert response.status_code == 200
        assert response.json() == {"id": ABS_ID, "nome": "ABS", "tipo": "ABS"}

    def test_get_filament_not_found(self, client):
        response = client.get("/api/filament/get/3fa85f64-5717-4562-b3fc-2c963f66afa6")

        assert response.status_code == 404

    def test_get_filament_invalid_id(self, client):
        response = client.get("/api/filament/get/abc")

        assert response.status_code == 400

    def test_get_filament_without_token(self):
        response = TestClient(app=app).get(f"/api/filament/get/{ABS_ID}")

        assert response.status_code == 401


class TestGetAllFilamentsRoute:
    def test_get_all_filaments(self, client):
        response = client.get("/api/filament/get_all")

        assert response.status_code == 200
        assert [f["nome"] for f in response.json()] == ["PLA", "ABS", "PETG", "TPU"]