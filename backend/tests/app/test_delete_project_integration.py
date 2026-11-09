from datetime import date, datetime, timedelta, timezone
from uuid import uuid7
import jwt
from fastapi.testclient import TestClient
from pytest import fixture

from src.app.app import app
from src.shared.environments import env
from src.modules.project.application.web import dependencies as project_dependencies
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.modules.project.domain.enums.order_status_enum import OrderStatus

def make_access_token(role: str) -> str:
    payload = {
        "sub": str(uuid7()),
        "type": "access",
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, env.jwt_secret, algorithm="HS256")

@fixture
def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto para reabilitação",
        urgency="high",
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )

@fixture
def access_token():
    return make_access_token("hospital")

@fixture
def client_and_repo(monkeypatch, access_token):
    repo = ProjectRepositoryMock()

    monkeypatch.setattr(project_dependencies, "_project_repository", repo)

    with TestClient(app) as client:
        client.cookies.set("access_token", access_token)
        yield client, repo

class TestDeleteProjectIntegration:
    def test_delete_existing_project(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.delete(
            f"/api/projects/delete/{valid_project.id}"
        )

        assert response.status_code == 200
        assert response.json()["id"] == str(valid_project.id)
        assert response.json()["title"] == valid_project.title
        assert valid_project.id not in repo.projects

    def test_delete_nonexistent_project(self, client_and_repo):
        client, repo = client_and_repo
        project_id = uuid7()

        response = client.delete(
            f"/api/projects/delete/{project_id}"
        )

        assert response.status_code == 404
        assert str(project_id) in response.json()["message"]
        assert len(repo.projects) == 0

    def test_delete_invalid_project_id(self, client_and_repo):
        client, repo = client_and_repo

        response = client.delete(
            "/api/projects/delete/invalid-uuid"
        )

        assert response.status_code == 422
        assert len(repo.projects) == 0

    def test_delete_same_project_twice(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        url = f"/api/projects/delete/{valid_project.id}"

        first_response = client.delete(url)
        second_response = client.delete(url)

        assert first_response.status_code == 200
        assert second_response.status_code == 404
        assert valid_project.id not in repo.projects
    
    def test_cannot_delete_project_in_progress(self, client_and_repo, valid_project):
        client, repo = client_and_repo

        valid_project.register_order_status(OrderStatus.RECEIVED)

        repo.create_project(valid_project)

        response = client.delete(f"/api/projects/delete/{valid_project.id}")

        assert response.status_code == 409
        assert repo.get_project(valid_project.id) == valid_project
        assert len(repo.projects) == 1
        assert len(valid_project.order_status) == 2
    
    def test_user_hospital_can_delete(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user_hospital"))

        response = client.delete(f"/api/projects/delete/{valid_project.id}")

        assert response.status_code == 200
        assert valid_project.id not in repo.projects

    def test_user_cannot_delete(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user"))

        response = client.delete(f"/api/projects/delete/{valid_project.id}")

        assert response.status_code == 403
        assert repo.get_project(valid_project.id) == valid_project

    def test_invalid_role_cannot_delete(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("invalid_role"))

        response = client.delete(f"/api/projects/delete/{valid_project.id}")

        assert response.status_code == 403
        assert valid_project.id in repo.projects

    def test_user_cannot_delete_project_in_progress(self, client_and_repo, valid_project):
        client, repo = client_and_repo

        valid_project.register_order_status(OrderStatus.RECEIVED)

        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user"))

        response = client.delete(f"/api/projects/delete/{valid_project.id}")

        assert response.status_code == 403
        assert valid_project.id in repo.projects