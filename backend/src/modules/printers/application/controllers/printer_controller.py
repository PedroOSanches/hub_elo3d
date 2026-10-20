from uuid import UUID

from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    CreatePrinterRequestSchema,
    PrinterResponseSchema,
    UpdatePrinterRequestSchema,
)
from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import (
    PrinterNotFoundError,
    UserNotFoundError,
)
from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class PrinterController:
    
    def __init__(
        self,
        repository: IPrinterRepository,
        user_gateway: IUserGateway,
    ) -> None:
        self._repository = repository
        self._user_gateway = user_gateway

    def criar(self, request: CreatePrinterRequestSchema) -> PrinterResponseSchema:
        if not self._user_gateway.exists(request.usuario_id):
            raise UserNotFoundError(request.usuario_id)
        printer = Printer(**request.model_dump())
        self._repository.criar(printer)
        return PrinterViewModel.from_entity(printer)

    def obter(self, printer_id: UUID) -> PrinterResponseSchema:
        return PrinterViewModel.from_entity(self._buscar_ou_falhar(printer_id))

    def listar(self, usuario_id: UUID | None = None) -> list[PrinterResponseSchema]:
        return PrinterViewModel.from_entities(self._repository.listar(usuario_id))

    def atualizar(
        self, printer_id: UUID, request: UpdatePrinterRequestSchema) -> PrinterResponseSchema:
        atual = self._buscar_ou_falhar(printer_id)
        dados = {**atual.model_dump(), **request.model_dump(exclude_none=True)}
        updated = Printer(**dados)
        self._repository.atualizar(updated)
        return PrinterViewModel.from_entity(updated)

    def deletar(self, printer_id: UUID) -> None:
        self._buscar_ou_falhar(printer_id)
        self._repository.deletar(printer_id)

    def _buscar_ou_falhar(self, printer_id: UUID) -> Printer:
        printer = self._repository.buscar_por_id(printer_id)
        if printer is None:
            raise PrinterNotFoundError(printer_id)
        return printer