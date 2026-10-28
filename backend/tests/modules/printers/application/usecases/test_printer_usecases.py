from uuid import uuid4

import pytest

from src.modules.printers.application.usecases.create_printer_usecase import (
    CreatePrinterUsecase,
)
from src.modules.printers.application.usecases.delete_printer_usecase import (
    DeletePrinterUsecase,
)
from src.modules.printers.application.usecases.get_printer_usecase import (
    GetPrinterUsecase,
)
from src.modules.printers.application.usecases.list_printers_usecase import (
    ListPrintersUsecase,
)
from src.modules.printers.application.usecases.update_printer_usecase import (
    UpdatePrinterUsecase,
)
from src.modules.printers.domain.entities.status_printer import StatusPrinter
from src.modules.printers.domain.errors.printer_errors import (
    PrinterNotFoundError,
    UserNotFoundError,
)
from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway
from src.modules.printers.infra.repositories.printer_repository_mock import (
    PrinterRepositoryMock,
)

from src.modules.printers.application.usecases.get_all_printers_by_user_usecase import (
    GetAllPrintersByUserUsecase,
)


class UserGatewayFake(IUserGateway):
    def __init__(self, exists: bool = True) -> None:
        self._exists = exists

    def exists(self, user_id) -> bool:
        return self._exists


def create_printer(repo, user_id=None, apelido="AD5X 1"):
    usecase = CreatePrinterUsecase(repo, UserGatewayFake(True))
    return usecase(
        apelido=apelido,
        modelo="Flashforge AD5X",
        tecnologia_impressao="FDM",
        usuario_id=user_id or uuid4(),
        filamentos_aceitos=[],
    )


class TestCreatePrinterUsecase:
    def test_create_printer(self):
        repo = PrinterRepositoryMock()

        printer = create_printer(repo)

        assert repo.get_printer(printer.id) == printer

    def test_create_printer_user_not_found(self):
        repo = PrinterRepositoryMock()
        usecase = CreatePrinterUsecase(repo, UserGatewayFake(False))

        with pytest.raises(UserNotFoundError):
            usecase(
                apelido="AD5X 1",
                modelo="Flashforge AD5X",
                tecnologia_impressao="FDM",
                usuario_id=uuid4(),
                filamentos_aceitos=[],
            )

        assert repo.get_all_printers() == []


class TestGetPrinterUsecase:
    def test_get_printer(self):
        repo = PrinterRepositoryMock()
        printer = create_printer(repo)

        assert GetPrinterUsecase(repo)(printer.id) == printer

    def test_get_printer_not_found(self):
        with pytest.raises(PrinterNotFoundError):
            GetPrinterUsecase(PrinterRepositoryMock())(uuid4())


class TestListPrintersUsecase:
    def test_list_all(self):
        repo = PrinterRepositoryMock()
        create_printer(repo)
        create_printer(repo)

        assert len(ListPrintersUsecase(repo)()) == 2

    def test_list_by_user(self):
        repo = PrinterRepositoryMock()
        user_id = uuid4()
        mine = create_printer(repo, user_id=user_id)
        create_printer(repo)

        assert ListPrintersUsecase(repo)(user_id) == [mine]

    def test_list_empty(self):
        assert ListPrintersUsecase(PrinterRepositoryMock())() == []


class TestUpdatePrinterUsecase:
    def test_update_only_given_fields(self):
        repo = PrinterRepositoryMock()
        printer = create_printer(repo)

        updated = UpdatePrinterUsecase(repo)(
            printer.id, {"apelido": "Nova", "status": StatusPrinter.EM_USO}
        )

        assert updated.apelido == "Nova"
        assert updated.status == StatusPrinter.EM_USO
        assert updated.modelo == printer.modelo
        assert updated.id == printer.id

    def test_update_printer_not_found(self):
        with pytest.raises(PrinterNotFoundError):
            UpdatePrinterUsecase(PrinterRepositoryMock())(uuid4(), {"apelido": "X"})


class TestDeletePrinterUsecase:
    def test_delete_printer(self):
        repo = PrinterRepositoryMock()
        printer = create_printer(repo)

        DeletePrinterUsecase(repo)(printer.id)

        assert repo.get_all_printers() == []

    def test_delete_printer_not_found(self):
        with pytest.raises(PrinterNotFoundError):
            DeletePrinterUsecase(PrinterRepositoryMock())(uuid4())

class TestGetAllPrintersByUserUsecase:
    def test_get_all_printers_by_user(self):
        repo = PrinterRepositoryMock()
        user_id = uuid4()
        p1 = create_printer(repo, user_id=user_id, apelido="A")
        p2 = create_printer(repo, user_id=user_id, apelido="B")
        create_printer(repo)

        result = GetAllPrintersByUserUsecase(repo)(user_id)

        assert result == [p1, p2]

    def test_user_without_printers_returns_empty_list(self):
        repo = PrinterRepositoryMock()
        create_printer(repo)

        assert GetAllPrintersByUserUsecase(repo)(uuid4()) == []