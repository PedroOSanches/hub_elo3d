from boto3 import client

from src.shared.environments.environments import env


class AWSClientFactory:

    def __init__(self) -> None:
        self.aws_access_key_id = env.aws_access_key_id
        self.aws_secret_access_key = env.aws_secret_access_key
        self.aws_default_region = env.aws_default_region


    def create_client_s3(self):
        return client(
            "s3",
            region_name=self.aws_default_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            
        )