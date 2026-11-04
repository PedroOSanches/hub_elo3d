from pytest import raises
from pydantic import ValidationError

from src.modules.project.domain.entities.project_file import ProjectFile

class TestProjectFile:
    def test_create_project_file(self):
        project_file = ProjectFile(
            title = "Modelo de prótese",
            file_url = "https://example.com/protese.pdf"
        )

        assert project_file.title == "Modelo de prótese"
        assert project_file.file_url == "https://example.com/protese.pdf"

    def test_required_title(self):
        with raises(ValidationError):
            ProjectFile(
                title = "",
                file_url = "https://example.com/protese.pdf"
            )

    def test_required_file_url(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                file_url = ""
            )

    def test_empty_title(self):
        with raises(ValidationError):
            ProjectFile(
                title = "",
                file_url = "https://example.com/protese.pdf"
            )

    def test_empty_file_url(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                file_url = ""
            )

    def test_unknown_field(self):
        with raises(ValidationError):
            ProjectFile(
                title = "Modelo de prótese",
                file_url = "https://example.com/protese.pdf",
                unknown_field = "value"
            )