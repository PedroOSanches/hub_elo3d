from datetime import datetime, timedelta, timezone
import jwt
from pytest import fixture
from uuid import uuid4
from fastapi.testclient import TestClient
from uuid import UUID

from src.app.app import app
from src.shared.environments.environments import env

from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def access_token():
    payload = {
        "sub": str(uuid4()),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    return jwt.encode(payload, env.jwt_secret, algorithm="HS256")

@fixture
def client(access_token):

    client = TestClient(app=app)
    client.cookies.set('access_token', access_token)

    return client

def test_create_project_in_real_app(client):

    request_data = {
        "title": "Prótese de mão",
        "date_end": "2026-11-15",
        "pieces_quantity": 1,
        "category": "prosthesis",
        "description": "Prótese para reabilitação",
        "urgency": "high",
        "filament_id": str(uuid4()),
        "files": [
            {
                "title": "Modelo 3D",
                "file_url": "https://example.com/model.stl"
            }
        ]
    }

    response = client.post("/api/projects/create", json=request_data)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Prótese de mão"
    assert "waiting_for_partner" in data["order_status"]

def test_create_project_with_real_dependencies(access_token):
    repo = get_repo_project()

    assert isinstance(repo, ProjectRepositoryMock)

    original_ids = set(repo.projects.keys())

    request_data = {
        "title": "Prótese de mão",
        "date_end": "2026-11-15",
        "pieces_quantity": 1,
        "category": "prosthesis",
        "description": "Prótese para reabilitação",
        "urgency": "high",
        "filament_id": str(uuid4()),
        "files": [
            {
                "title": "Modelo 3D",
                "file_url": "https://example.com/model.stl"
            }
        ]
    }

    try:
        with TestClient(app) as client:
            client.cookies.set("access_token", access_token)
            response = client.post("/api/projects/create", json=request_data)

        assert response.status_code == 201

        project_id = UUID(response.json()["id"])

        assert project_id in repo.projects
        assert repo.projects[project_id].title == "Prótese de mão"
        
    finally:
        for project_id in set(repo.projects) - original_ids:
            repo.projects.pop(project_id, None)