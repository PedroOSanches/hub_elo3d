from datetime import date, datetime, timedelta, timezone
from uuid import uuid4
import jwt
from fastapi.testclient import TestClient
from pytest import fixture

from src.app.app import app
from src.shared.environments import env
from src.modules.project.application.web import dependencies as project_dependencies

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto para reabilitação",
        urgency="high",
        filament_id=uuid4(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl",
            )
        ],
    )

@fixture
def access_token():
    payload = {
        "sub": str(uuid4()),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    return jwt.encode(payload, env.jwt_secret, algorithm="HS256")

@fixture
def client_and_repo(monkeypatch, access_token):
    repo = ProjectRepositoryMock()
    monkeypatch.setattr(project_dependencies, "_project_repository", repo)
    
    with TestClient(app) as client:
        client.cookies.set("access_token", access_token)
        yield client, repo

class TestGetAllProjectsIntegration:
    def test_get_all_projects(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        second_project = valid_project.model_copy(update={"id": uuid4(), "title": "Prótese de perna", "category": "orthosis"})

        repo.create_project(valid_project)
        repo.create_project(second_project)

        response = client.get("/api/projects/get_all")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2

        returned_ids = {project["id"] for project in data}

        assert str(valid_project.id) in returned_ids
        assert str(second_project.id) in returned_ids
        assert data[0]["category"] == "prosthesis"

    def test_get_all_projects_empty(self, client_and_repo):
        client, repo = client_and_repo

        response = client.get("/api/projects/get_all")

        assert response.status_code == 200
        assert response.json() == []
        assert len(repo.projects) == 0

    def test_get_all_projects_unauthorized(self):
        with TestClient(app) as client:
            response = client.get("/api/projects/get_all")

            assert response.status_code == 401
            assert response.json()["message"] == "Authentication required"

    def test_get_all_projects_invalid_token(self):
        with TestClient(app) as client:
            client.cookies.set("access_token", "invalid_token")
            response = client.get("/api/projects/get_all")

            assert response.status_code == 401
            assert response.json()["message"] == "Invalid or expired access token"