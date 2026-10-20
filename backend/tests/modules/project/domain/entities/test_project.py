from uuid import uuid4, UUID
from datetime import date

import pytest
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project

class TestProject:

    def test_create_project(self):
        project = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15)
        )

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.date_end == date(2026, 11, 15)

    def test_different_ids(self):
        project1 = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15)
        )

        project2 = Project(
            title = "Suporte de braço",
            date_end = date(2026, 11, 15)
        )

        assert project1.id != project2.id

    def test_required_title(self):
        with pytest.raises(ValidationError):
            Project(
                date_end = date(2026, 11, 15)
            )

    def test_short_title(self):
        with pytest.raises(ValidationError):
            Project(
                title = "AB",
                date_end = date(2026, 11, 15)
            )

    def test_required_date_end(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão"
            )

    def test_unknown_field(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                unknown_field = "Teste"
            )