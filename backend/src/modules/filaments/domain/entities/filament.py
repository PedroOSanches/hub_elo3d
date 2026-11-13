from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Filament(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: UUID = Field(default_factory=uuid4)
    nome: str = Field(min_length=1)
    tipo: str = Field(min_length=1)