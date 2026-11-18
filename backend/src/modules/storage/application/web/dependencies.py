from src.modules.storage.domain.gateways.gateway_storage_interface import (
    IGatewayStorage,
)
from src.modules.storage.infra.external.gateways.gateway_s3_storage import (
    GatewayS3Storage,
)
from src.shared.environments.aws_client_factory import AWSClientFactory
from src.shared.environments.environments import env


def get_gateway_s3() -> IGatewayStorage:
    return GatewayS3Storage(
        aws_client=AWSClientFactory(), 
        bucket_name=env.aws_s3_bucket_name
        )