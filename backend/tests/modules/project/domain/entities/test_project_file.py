from uuid import UUID

from pydantic import ValidationError
from pytest import raises

from src.modules.project.domain.entities.project_file import ProjectFile


class TestProjectFile:
    def test_create_project_file(self):
        project_file = ProjectFile(
            title = "Modelo de prótese",
            object_key = UUID("01a1eb3e-d77e-738b-97ef-cb486c7ad4ab"),
            size=123,
            content_type="model/stl",
        )

        assert project_file.title == "Modelo de prótese"
        assert project_file.object_key == UUID("01a1eb3e-d77e-738b-97ef-cb486c7ad4ab")

    def test_required_title(self):
        with raises(ValidationError):
            ProjectFile(
                title = "",
                object_key = UUID("01a1eb3e-d77e-738b-97ef-cb486c7ad4ab"),
                content_type="model/stl",
            )

    def test_required_object_key(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                object_key = "",
                content_type="model/stl",
            )

    def test_empty_title(self):
        with raises(ValidationError):
            ProjectFile(
                title = "",
                object_key = UUID("01a1eb3e-d77e-738b-97ef-cb486c7ad4ab"),
                content_type="model/stl",
            )

    def test_empty_object_key(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                object_key = "",
                content_type="model/stl",
            )

    def test_unknown_field(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                object_key = UUID("01a1eb3e-d77e-738b-97ef-cb486c7ad4ab"),
                content_type="model/stl",
                unknown_field = "value"
            )