import pytest

from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency

class TestProjectEnums:

    def test_order_status_values(self):
        assert OrderStatus.WAITING_FOR_PARTNER.value == "waiting_for_partner"
        assert OrderStatus.RECEIVED.value == "received"
        assert OrderStatus.IN_PROGRESS.value == "in_progress"
        assert OrderStatus.FINALIZED.value == "finalized"
        assert OrderStatus.DELIVERED.value == "delivered"

    def test_urgency_values(self):
        assert Urgency.LOW.value == "low"
        assert Urgency.MEDIUM.value == "medium"
        assert Urgency.HIGH.value == "high"

    def test_order_status_invalid(self):
        with pytest.raises(ValueError):
            OrderStatus("canceled")

    def test_urgency_invalid(self):
        with pytest.raises(ValueError):
            Urgency("critical")