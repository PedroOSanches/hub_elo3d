from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency

class UpdateProjectRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3)
    date_end: date | None = None
    pieces_quantity: int | None = Field(default=None, gt=0)
    category: Category | None = None
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=280
    )
    technical_info: str | None = None
    urgency: Urgency | None = None
    printer_id: UUID | None = None
    filament_id: UUID | None = None
    files: list[ProjectFile] | None = Field(
        default=None,
        min_length=1
    )
    new_status: OrderStatus | None = None

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @model_validator(mode="after")
    def validate_update(self):
        nullable_fields = {
            "technical_info",
            "printer_id",
            "new_status"
        }

        for field in self.model_fields_set - nullable_fields:
            if getattr(self, field) is None:
                raise ValueError(f"{field} não pode ser nulo")

        has_changes = bool(self.model_fields_set - {"new_status"})

        if not has_changes and self.new_status is None:
            raise ValueError("Nenhum campo foi alterado")

        return self

class UpdateProjectResponseSchema(GetProjectResponseSchema):
    pass