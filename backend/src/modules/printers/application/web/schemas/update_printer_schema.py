import uuid

from pydantic import Field

from src.modules.printers.application.web.schemas.base_request_schema import (
    BaseRequestSchema,
)
from src.modules.printers.domain.entities.status_printer import StatusPrinter


class UpdatePrinterRequestSchema(BaseRequestSchema):
    # todos os campos são opcionais: só altera o que for enviado

    apelido: str | None = Field(default=None, min_length=1)
    modelo: str | None = Field(default=None, min_length=1)
    tecnologia_impressao: str | None = Field(default=None, min_length=1)
    filamentos_aceitos: list[uuid.UUID] | None = None
    status: StatusPrinter | None = None