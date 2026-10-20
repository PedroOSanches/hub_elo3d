from uuid import uuid4, UUID
from datetime import date

import pytest
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project

class TestProject:

    def test_create_project(self):
        project = Project(
            title = "Prótese de mão"
        )

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.date_end is None

    def test_different_ids(self):
        project1 = Project(
            title = "Prótese de mão"
        )

        project2 = Project(
            title = "Suporte de braço"
        )

        assert project1.id != project2.id

    def test_required_title(self):
        with pytest.raises(ValidationError):
            Project()

    def test_short_title(self):
        with pytest.raises(ValidationError):
            Project(title = "AB")

    def test_completed_project(self):
        completion_date = date(2026, 10, 19)

        project = Project(
            title = "Prótese de mão",
            date_end = completion_date
        )

        assert project.date_end == completion_date

    def test_unknown_field(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                unknown_field = "Teste"
            )