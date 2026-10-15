from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .status_impressora import StatusImpressora


class Impressora(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: UUID = Field(default_factory=uuid4)
    apelido: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    tecnologia_impressao: str = Field(min_length=1)
    usuario_id: UUID 
    filamentos_aceitos: list[int] = Field(default_factory=list)
    status: StatusImpressora = StatusImpressora.DISPONIVEL

    @field_validator("filamentos_aceitos")
    @classmethod
    def _sem_duplicados(cls, v: list[int]) -> list[int]:
        return list(dict.fromkeys(v))

    def alterar_status(self, novo_status: StatusImpressora) -> None:
        self.status = novo_status

    @property
    def disponivel(self) -> bool:
        return self.status is StatusImpressora.DISPONIVEL