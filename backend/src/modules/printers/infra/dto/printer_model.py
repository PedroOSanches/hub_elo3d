from uuid import UUID

from pydantic import BaseModel

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.entities.status_printer import StatusPrinter


class PrinterModel(BaseModel):
    #quando tiver DB isso vai virar documento/tabela

    id: UUID
    apelido: str
    modelo: str
    tecnologia_impressao: str
    usuario_id: UUID
    filamentos_aceitos: list[UUID]
    status: str

    @classmethod
    def from_entity(cls, entity: Printer) -> "PrinterModel":
        return cls(
            id=entity.id,
            apelido=entity.apelido,
            modelo=entity.modelo,
            tecnologia_impressao=entity.tecnologia_impressao,
            usuario_id=entity.usuario_id,
            filamentos_aceitos=list(entity.filamentos_aceitos),
            status=entity.status.value,
        )

    def to_entity(self) -> Printer:
        return Printer(
            id=self.id,
            apelido=self.apelido,
            modelo=self.modelo,
            tecnologia_impressao=self.tecnologia_impressao,
            usuario_id=self.usuario_id,
            filamentos_aceitos=list(self.filamentos_aceitos),
            status=StatusPrinter(self.status),
        )