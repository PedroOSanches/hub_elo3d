from datetime import date
from uuid import uuid4
from fastapi.testclient import TestClient
from pytest import fixture

from src.app.app import app
from src.modules.project.application.web import dependencies as project_dependencies

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def valid_project():
    return Project(
        id=uuid4(),
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="Ortopedia",
        description="Projeto para reabilitação",
        technical_info=None,
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
def client_and_repo(monkeypatch):
    repo = ProjectRepositoryMock()
    monkeypatch.setattr(project_dependencies, "_project_repository", repo)

    with TestClient(app) as client:
        yield client, repo

class TestGetProjectIntegration:
    def test_get_project_success(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.get(f"/projects/get/{valid_project.id}")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(valid_project.id)
        assert data["title"] == valid_project.title
        assert data["date_end"] == "2026-11-15"
        assert data["order_status"] == "waiting_for_partner"
        assert data["files"][0]["title"] == "Modelo 3D"

    def test_get_nonexistent_project(self, client_and_repo):
        client, repo = client_and_repo
        project_id = uuid4()

        response = client.get(f"/projects/get/{project_id}")

        assert response.status_code == 404
        assert str(project_id) in response.json()["message"]
        assert len(repo.projects) == 0

    def test_get_project_invalid_id(self, client_and_repo):
        client, repo = client_and_repo
        
        response = client.get(f"/projects/get/invalid-uuid")

        assert response.status_code == 422
        assert len(repo.projects) == 0