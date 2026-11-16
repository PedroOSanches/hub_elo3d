import abc
from abc import abstractmethod
from uuid import UUID

from ..entities.printer import Printer


class IPrinterRepository(abc.ABC):
    @abstractmethod
    def create_printer(self, printer: Printer) -> Printer:
        """
        Cria impressora nova
        """
        pass

    @abstractmethod
    def get_printer(self, printer_id: UUID) -> Printer:
        """Retorna uma impressora pelo id"""
        pass

    @abstractmethod
    def get_all_printers(self, user_id: UUID | None = None) -> list[Printer]:
        """
        Retorna todas as impressoras.
        Mas se informar id do usuario retorna so as dele.,
        Se não achar levanta PrinterNotFound
        """
        pass

    @abstractmethod
    def update_printer(self, printer_id: UUID, updated_printer: Printer) -> Printer:
        """
        Atualiza a impressora pelo id.
        Retorna com as alterações e se não achar levanta PrinterNotFound
        """
        pass

    @abstractmethod
    def delete_printer(self, printer_id: UUID) -> None:
        """
        Deleta impressora pelo id.
        Se nao achar levanta erro PrinterNotFound
        """
        pass