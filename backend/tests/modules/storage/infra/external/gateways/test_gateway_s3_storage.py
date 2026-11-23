from pytest import fixture, raises
from src.modules.storage.domain.errors.file_not_found_error import FileNotFound
from src.modules.storage.infra.external.gateways.gateway_s3_storage import GatewayS3Storage
from src.shared.environments.environments import env
from src.shared.environments.aws_client_factory import AWSClientFactory

@fixture
def client_s3():
    return  GatewayS3Storage(
        aws_client=AWSClientFactory(),
        bucket_name=env.aws_s3_bucket_name,
    )

class Test_GatewayS3Storage:

    def test_generate_download_url(self, client_s3):

        url = client_s3.generate_download_url(
            object_key='teste.txt',
            file_name='teste.txt',
            expires_in=60
        )

        print(url)
        assert f'https://{env.aws_s3_bucket_name}.s3.amazonaws.com/teste.txt?' in url