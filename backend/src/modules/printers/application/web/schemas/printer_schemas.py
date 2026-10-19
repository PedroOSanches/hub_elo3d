from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.modules.impressoras.domain.entities.status_impressora import StatusImpressora


class CriarImpressoraRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    apelido: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    tecnologia_impressao: str = Field(min_length=1)
    usuario_id: UUID
    filamentos_aceitos: list[UUID] = Field(default_factory=list)


class AtualizarImpressoraRequest(BaseModel):
    #tudo opcional (so vai oque foi alterado)

    model_config = ConfigDict(str_strip_whitespace=True)

    apelido: str | None = Field(default = None, min_length=1)
    modelo: str | None = Field(default = None, min_length=1)
    tecnologia_impressao: str | None = Field(default=None, min_length=1)
    filamentos_aceitos: list[UUID] | None = None
    status: StatusImpressora | None = None


class ImpressoraResponse(BaseModel):
    id: UUID
    apelido: str
    modelo: str
    tecnologia_impressao: str
    usuario_id: UUID
    filamentos_aceitos: list[UUID]
    status: StatusImpressora