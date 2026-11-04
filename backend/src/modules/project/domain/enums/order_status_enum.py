from enum import Enum

class OrderStatus(str, Enum):
    WAITING_FOR_PARTNER = "waiting_for_partner"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"