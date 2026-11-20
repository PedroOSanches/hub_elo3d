from src.modules.project.domain.gateways.storage_gateway import IGatewayStorage
from src.modules.storage.domain.errors.file_not_found_error import FileNotFound


class GatewayStorageMock(IGatewayStorage):

    def __init__(self) -> None:
        self.storage = [
                'projects/mock_ortese/01a1fa0d-0959-741e-a966-dfb9ad976800.obj',
                'projects/mock_protese/01a1fa0d-aa4c-76df-88e0-b7b3333e63c2.pdf',
                'projects/mock_ortese_craniana/01a1fa0d-bcb1-73ab-8108-733b38b4bad2.stl',
        ]

    def verify_upload(self, file_object_key: str, file_name: str) -> bool:
        if file_object_key in self.storage:
            return True
        else:
            raise FileNotFound(file_name=file_name)