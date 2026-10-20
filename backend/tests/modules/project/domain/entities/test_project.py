from uuid import UUID
from datetime import date

import pytest
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.production_status_enum import ProductionStatus
from src.modules.project.domain.enums.urgency_enum import Urgency

class TestProject:

    def test_create_project(self):
        project = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15),
            urgency = Urgency.HIGH
        )

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.date_end == date(2026, 11, 15)
        assert project.urgency == Urgency.HIGH
        assert project.order_status == OrderStatus.WAITING_FOR_PARTNER
        assert project.production_status is None

    def test_different_ids(self):
        project1 = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15),
            urgency = Urgency.HIGH
        )

        project2 = Project(
            title = "Suporte de braço",
            date_end = date(2026, 11, 15),
            urgency = Urgency.LOW
        )

        assert project1.id != project2.id

    def test_required_title(self):
        with pytest.raises(ValidationError):
            Project(
                date_end = date(2026, 11, 15),
                urgency = Urgency.HIGH
            )

    def test_short_title(self):
        with pytest.raises(ValidationError):
            Project(
                title = "AB",
                date_end = date(2026, 11, 15),
                urgency = Urgency.MEDIUM
            )

    def test_required_date_end(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                urgency = Urgency.HIGH
            )

    def test_unknown_field(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                date_end = date(2026, 11, 15),
                urgency = Urgency.HIGH,
                unknown_field = "Teste"
            )

    def test_required_urgency(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                date_end = date(2026, 11, 15)
            )

    def test_production_status(self):
        project = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15),
            urgency = Urgency.MEDIUM,
            production_status = ProductionStatus.IN_PRODUCTION
        )

        assert project.production_status == ProductionStatus.IN_PRODUCTION

    def test_custom_order_status(self):
        project = Project(
            title = "Prótese de mão",
            date_end = date(2026, 11, 15),
            urgency = Urgency.LOW,
            order_status = OrderStatus.IN_PROGRESS
        )

        assert project.order_status == OrderStatus.IN_PROGRESS

    def test_invalid_urgency(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                date_end = date(2026, 11, 15),
                urgency = "critical"
            )

    def test_invalid_order_status(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                date_end = date(2026, 11, 15),
                urgency = Urgency.HIGH,
                order_status = "canceled"
            )

    def test_invalid_production_status(self):
        with pytest.raises(ValidationError):
            Project(
                title = "Prótese de mão",
                date_end = date(2026, 11, 15),
                urgency = Urgency.HIGH,
                production_status = "printing_error"
            )