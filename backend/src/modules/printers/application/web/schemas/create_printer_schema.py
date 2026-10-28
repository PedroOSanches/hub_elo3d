import uuid

from pydantic import Field

from src.modules.printers.application.web.schemas.base_request_schema import (
    BaseRequestSchema,
)


class CreatePrinterRequestSchema(BaseRequestSchema):
    campos_obrigatorios = ("apelido", "modelo", "tecnologia_impressao", "usuario_id")

    apelido: str = Field(..., min_length=1, description="Apelido da printer")
    modelo: str = Field(..., min_length=1, description="Modelo da printer")
    tecnologia_impressao: str = Field(..., min_length=1, description="Ex.: FDM, SLA")
    usuario_id: uuid.UUID = Field(..., description="Usuário dono da printer")
    filamentos_aceitos: list[uuid.UUID] = Field(default_factory=list)