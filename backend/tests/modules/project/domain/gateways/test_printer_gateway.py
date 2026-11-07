from uuid import UUID, uuid4
from pytest import raises

from src.modules.project.domain.gateways.printer_gateway import IPrinterGateway

class FakePrinterGateway(IPrinterGateway):
    def __init__(self, printer_ids: set[UUID]):
        self._printer_ids = printer_ids

    def exists(self, printer_id: UUID) -> bool:
        return printer_id in self._printer_ids

class TestPrinterGateway:
    def test_gateway_cannot_be_instantiated(self):
        with raises(TypeError):
            IPrinterGateway()

    def test_existing_printer(self):
        printer_id = uuid4()
        gateway = FakePrinterGateway({printer_id})
        assert gateway.exists(printer_id) is True

    def test_nonexistent_printer(self):
        printer_id = uuid4()
        gateway = FakePrinterGateway(set())
        assert gateway.exists(printer_id) is False