from datetime import date
from uuid import uuid4
from pytest import fixture

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.application.web.schemas.get_all_projects_schema import GetAllProjectsResponseSchema

@fixture
def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="Ortopedia",
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

class TestGetAllProjectsResponseSchema:
    def test_response_with_multiple_projects(self, valid_project):
        second_project = valid_project.model_copy(update={"id": uuid4(), "title": "Prótese de perna"})
        projects = [valid_project, second_project]

        response = GetAllProjectsResponseSchema.model_validate(projects)

        assert len(response.root) == 2
        assert response.root[0].id == valid_project.id
        assert response.root[1].id == second_project.id
        assert response.root[1].title == "Prótese de perna"

    def test_response_with_empty_list(self):
        response = GetAllProjectsResponseSchema.model_validate([])

        assert response.root == []
        assert response.model_dump(mode="json") == []

    def test_serialize_to_json(self, valid_project):
        response = GetAllProjectsResponseSchema.model_validate([valid_project])
        json_data = response.model_dump(mode="json")

        assert isinstance(json_data, list)
        assert json_data[0]["id"] == str(valid_project.id)
        assert json_data[0]["date_end"] == "2026-11-15"
        assert json_data[0]["order_status"] == "waiting_for_partner"
        assert json_data[0]["files"][0]["title"] == "Modelo 3D"