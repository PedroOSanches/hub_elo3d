from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.urgency_enum import Urgency

class CreateProjectRequestSchema(BaseModel):
    title: str = Field(
        ...,
        min_length = 3
    )

    date_end: date

    pieces_quantity: int = Field(
        ...,
        gt = 0
    )

    category: str = Field(
        ...,
        min_length = 1
    )

    description: str = Field(
        ...,
        min_length = 1,
        max_length = 280
    )

    urgency: Urgency

    filament_id: UUID

    files: list[ProjectFile] = Field(
        ...,
        min_length = 1
    )

    technical_info: str | None = None

    @field_validator("description", mode = "before")
    @classmethod
    def strip_description(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()

        return value

    model_config = ConfigDict(
        extra = "forbid"
    )