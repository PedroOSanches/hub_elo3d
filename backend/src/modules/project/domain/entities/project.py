from uuid import uuid4, UUID
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class Project(BaseModel):
    id: UUID = Field(
        default_factory = uuid4,
        description = "ID do projeto"
    )

    title: str = Field(
        ...,
        min_length = 3,
        description = "Título do projeto"
    )

    date_end: date = Field(
        ...,
        description = "Prazo estimado para término do projeto"
    )

    model_config = ConfigDict(
        extra = "forbid",
        populate_by_name = True
    )