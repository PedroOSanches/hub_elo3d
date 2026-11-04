from datetime import date
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from src.modules.project.application.controllers.get_all_projects_controller import GetAllProjectsController
from src.modules.project.application.usecases.get_all_projects_usecase import GetAllProjectsUsecase
from src.modules.project.application.web.routes.get_all_projects import get_get_all_projects_dependencies
from src.modules.project.application.web.routes.index import project_router
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
def client_and_repo():
    app = FastAPI()
    app.include_router(project_router, prefix="/projects")

    repo = ProjectRepositoryMock()
    usecase = GetAllProjectsUsecase(repo)
    controller = GetAllProjectsController(usecase)

    app.dependency_overrides[get_get_all_projects_dependencies] = lambda: controller

    with TestClient(app) as client:
        yield client, repo

class TestGetAllProjectsRoute:
    def test_get_all_projects_success(self, client_and_repo, valid_project):
        client, repo = client_and_repo

        second_project = valid_project.model_copy(update={"id": uuid4(), "title": "Órtese de punho", "category": "orthosis"})

        repo.create_project(valid_project)
        repo.create_project(second_project)

        response = client.get("/projects/get_all")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2

        returned_ids = {project["id"] for project in data}

        assert str(valid_project.id) in returned_ids
        assert str(second_project.id) in returned_ids

    def test_get_all_projects_empty(self, client_and_repo):
        client, repo = client_and_repo

        response = client.get("/projects/get_all")

        assert response.status_code == 200
        assert response.json() == []
        assert len(repo.projects) == 0

    def test_get_all_projects_serialization(self, client_and_repo, valid_project):
        client, repo = client_and_repo

        repo.create_project(valid_project)

        response = client.get("/projects/get_all")

        assert response.status_code == 200

        data = response.json()

        assert data[0]["id"] == str(valid_project.id)
        assert data[0]["date_end"] == "2026-11-15"
        assert data[0]["category"] == "prosthesis"
        assert data[0]["order_status"] == "waiting_for_partner"
        assert data[0]["files"][0]["title"] == "Modelo 3D"