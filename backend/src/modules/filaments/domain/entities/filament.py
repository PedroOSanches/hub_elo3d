from uuid import UUID, uuid7

from pydantic import BaseModel, ConfigDict, Field


class Filament(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    filament_id: UUID = Field(default_factory=uuid7)
    tipo: str = Field(min_length=1)