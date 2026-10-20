from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .status_printer import StatusPrinter


class Printer(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: UUID = Field(default_factory=uuid4)
    apelido: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    tecnologia_impressao: str = Field(min_length=1)
    usuario_id: UUID 
    filamentos_aceitos: list[UUID] = Field(default_factory=list)
    status: StatusPrinter = StatusPrinter.DISPONIVEL

    @field_validator("filamentos_aceitos")
    @classmethod
    def _sem_duplicados(cls, v: list[int]) -> list[int]:
        return list(dict.fromkeys(v))

    def alterar_status(self, novo_status: StatusPrinter) -> None:
        self.status = novo_status

    @property
    def disponivel(self) -> bool:
        return self.status is StatusPrinter.DISPONIVEL