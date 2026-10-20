from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)
from src.modules.printers.domain.entities.printer import Printer


class PrinterViewModel:
    #entidade pra response, a rota nunca devolve a entidade direto

    @staticmethod
    def from_entity(entity: Printer) -> PrinterResponseSchema:
        return PrinterResponseSchema(
            id=entity.id,
            apelido=entity.apelido,
            modelo=entity.modelo,
            tecnologia_impressao=entity.tecnologia_impressao,
            usuario_id=entity.usuario_id,
            filamentos_aceitos=list(entity.filamentos_aceitos),
            status=entity.status,
        )

    @staticmethod
    def from_entities(entities: list[Printer]) -> list[PrinterResponseSchema]:
        return [PrinterViewModel.from_entity(e) for e in entities]