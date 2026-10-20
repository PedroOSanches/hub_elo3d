import uuid

from pydantic import BaseModel

from src.modules.printers.domain.entities.status_printer import StatusPrinter


class PrinterResponseSchema(BaseModel):
    id: uuid.UUID
    apelido: str
    modelo: str
    tecnologia_impressao: str
    usuario_id: uuid.UUID
    filamentos_aceitos: list[uuid.UUID]
    status: StatusPrinter