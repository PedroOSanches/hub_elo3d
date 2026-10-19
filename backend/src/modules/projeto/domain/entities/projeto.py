from uuid import uuid4, UUID
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class Projeto(BaseModel):
    id: UUID = Field(
        default_factory = uuid4,
        description = "ID do projeto"
    )

    titulo: str = Field(
        ...,
        min_length = 3,
        description = "Título do projeto"
    )

    date_end: date | None = Field(
        default = None,
        description = "Data de término do projeto"
    )

    model_config = ConfigDict(
        extra = "forbid",
        populate_by_name = True
    )