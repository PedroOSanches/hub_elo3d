from botocore.exceptions import ClientError

from src.modules.storage.domain.gateways.gateway_storage_interface import (
    IGatewayStorage,
)
from src.shared.environments.aws_client_factory import AWSClientFactory


class GatewayS3Storage(IGatewayStorage):

    def __init__(self, aws_client: AWSClientFactory, bucket_name: str) -> None:
        self.client = aws_client.create_client_s3()
        self.bucket_name = bucket_name

    def generate_upload_url(self, object_key: str, content_type: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                "Bucket":self.bucket_name,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=3600,
        )

    def verify_upload(self, object_key: str) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key,
                )
            return True

        except ClientError as error:
            error_code = error.response["Error"]["Code"]
            if error_code in ("404", "NoSuchKey", "NotFound"):
                return False

        raise


    def generate_download_url(self, object_key:str, file_name: str) -> str:
        return self.client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={
                        "Bucket":self.bucket_name,
                        "Key": object_key,
                        "ResponseContentDisposition":(
                            f'attachment; filename"{file_name}"'
                        )
                    },
                    ExpiresIn=3600,
                )
