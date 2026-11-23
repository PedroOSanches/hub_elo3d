from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency


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
    order_status: dict[OrderStatus, datetime]
    printer_id: UUID | None
    filament_id: UUID
    files: list[GetProjectFilesResponseSchema]


class GetProjectFilesResponseSchema(BaseModel):
    title: str
    download_url: str
    size: int
    content_type: str
