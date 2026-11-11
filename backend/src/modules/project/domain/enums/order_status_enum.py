from enum import Enum

class OrderStatus(str, Enum):
    WAITING_FOR_PARTNER = "waiting_for_partner"
    RECEIVED = "received"
    IN_PROGRESS = "in_progress"
    FINALIZED = "finalized"
    DELIVERED = "delivered"