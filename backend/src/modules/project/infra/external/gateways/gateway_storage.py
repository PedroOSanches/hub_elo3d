from src.modules.project.domain.gateways.storage_gateway import IGatewayStorage
from src.modules.storage.domain.errors.file_not_found_error import FileNotFound

from .dependencies import get_gateway_storage


class GatewayStorage(IGatewayStorage):

    def __init__(self) -> None:
        self.gateway_s3 = get_gateway_storage()

    def verify_upload(self, file_name: str, file_object_key: str) -> bool:
        if not self.gateway_s3.verify_upload(
            object_key=file_object_key
            ):
            raise FileNotFound(
                file_name=file_name
                )
        return True 

    def generate_download_url(self, file_name: str, object_key: str) -> str:
        return self.gateway_s3.generate_download_url(
            file_name=file_name,
            object_key=object_key
            )