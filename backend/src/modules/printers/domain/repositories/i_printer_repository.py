import abc
from abc import abstractmethod
from uuid import UUID

from ..entities.printer import Printer


class IPrinterRepository(abc.ABC):
    @abstractmethod
    def create_printer(self, printer: Printer) -> Printer:
       #cria impressora nova
        pass

    @abstractmethod
    def get_printer(self, printer_id: UUID) -> Printer:
        #retorna uma impressora pelo id
        pass

    @abstractmethod
    def get_all_printers(self, user_id: UUID | None = None) -> list[Printer]:
        #retorna todas as impressoras, mas se informar id do usuario retorna so as dele, se não achar levanta PrinterNotFound
        pass

    @abstractmethod
    def update_printer(self, printer_id: UUID, updated_printer: Printer) -> Printer:
        #atualiza a impressora pelo id, retorna com as alterações e se não achar levanta PrinterNotFound
        pass

    @abstractmethod
    def delete_printer(self, printer_id: UUID) -> None:
       #deleta impressora pelo id, se nao achar levanta erro PrinterNotFound
        pass