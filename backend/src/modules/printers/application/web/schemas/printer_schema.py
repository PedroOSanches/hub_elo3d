import uuid

from pydantic import BaseModel, ConfigDict

from src.modules.printers.domain.entities.status_printer import StatusPrinter


class PrinterResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    apelido: str
    modelo: str
    tecnologia_impressao: str
    usuario_id: uuid.UUID
    filamentos_aceitos: list[uuid.UUID]
    status: StatusPrinter