from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FilamentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    tipo: str