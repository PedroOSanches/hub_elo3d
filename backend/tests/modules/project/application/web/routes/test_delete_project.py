from datetime import date
from uuid import uuid7
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

from src.modules.project.application.controllers.delete_project_controller import DeleteProjectController
from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.application.web.routes.delete_project import get_delete_project_dependencies
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
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )

@fixture
def client_and_repo():
    app = FastAPI()
    app.include_router(project_router, prefix="/projects")
    app.add_exception_handler(BaseError, base_error_handler)

    repo = ProjectRepositoryMock()
    usecase = DeleteProjectUsecase(repo)
    controller = DeleteProjectController(usecase)

    app.dependency_overrides[get_delete_project_dependencies] = (lambda: controller)

    with TestClient(app) as client:
        yield client, repo

    app.dependency_overrides.clear()

class TestDeleteProjectRoute:
    def test_delete_existing_project(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.delete(f"/projects/delete/{valid_project.id}")

        assert response.status_code == 200
        assert response.json()["id"] == str(valid_project.id)
        assert response.json()["title"] == valid_project.title
        assert valid_project.id not in repo.projects

    def test_delete_nonexistent_project(self, client_and_repo):
        client, _ = client_and_repo
        project_id = uuid7()

        response = client.delete(f"/projects/delete/{project_id}")

        assert response.status_code == 404
        assert str(project_id) in response.json()["message"]

    def test_delete_invalid_project_id(self, client_and_repo):
        client, repo = client_and_repo

        response = client.delete("/projects/delete/invalid-uuid")

        assert response.status_code == 422
        assert len(repo.projects) == 0