from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import PrinterNotFoundError
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.printers.infra.dto.printer_model import PrinterModel


class PrinterRepositoryMock(IPrinterRepository):
    #repositorio em memoria que os dados somem quando reinicia a aplicação

    def __init__(self) -> None:
        self.printers: dict[UUID, PrinterModel] = {}

    def create_printer(self, printer: Printer) -> Printer:
        self.printers[printer.id] = PrinterModel.from_entity(printer)
        return printer

    def get_printer(self, printer_id: UUID) -> Printer:
        model = self.printers.get(printer_id)
        if model is None:
            raise PrinterNotFoundError(printer_id)
        return model.to_entity()

    def get_all_printers(self, user_id: UUID | None = None) -> list[Printer]:
        models = list(self.printers.values())
        if user_id is not None:
            models = [m for m in models if m.usuario_id == user_id]
        return [m.to_entity() for m in models]

    def update_printer(self, printer_id: UUID, updated_printer: Printer) -> Printer:
        if printer_id not in self.printers:
            raise PrinterNotFoundError(printer_id)
        self.printers[printer_id] = PrinterModel.from_entity(updated_printer)
        return updated_printer

    def delete_printer(self, printer_id: UUID) -> None:
        if printer_id not in self.printers:
            raise PrinterNotFoundError(printer_id)
        del self.printers[printer_id]