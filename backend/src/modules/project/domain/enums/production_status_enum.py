from enum import Enum

class ProductionStatus(str, Enum):
    RECEIVED = "received"
    IN_PRODUCTION = "in_production"
    FINALIZATION = "finalization"
    DELIVERED = "delivered"