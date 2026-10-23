from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)
from src.modules.printers.domain.entities.printer import Printer


class PrinterViewModel:
    

    @staticmethod
    def from_entity(entity: Printer) -> PrinterResponseSchema:
        return PrinterResponseSchema.model_validate(entity)

    @staticmethod
    def from_entities(entities: list[Printer]) -> list[PrinterResponseSchema]:
        return [PrinterViewModel.from_entity(e) for e in entities]