from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.enums.category_enum import Category

class GetProjectResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    date_end: date
    pieces_quantity: int
    category: Category
    description: str
    technical_info: str | None
    urgency: Urgency
    order_status: OrderStatus
    printer_id: UUID | None
    filament_id: UUID
    files: list[ProjectFile]