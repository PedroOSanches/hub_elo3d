import os
from enum import Enum

from dotenv import load_dotenv


class STAGE(Enum):
    DOTENV = 'DOTENV'
    TEST = 'TEST'
    PROD = "PROD"

class Environments:

    def _configure_local(self):
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE", STAGE.DOTENV.value) 

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE", 'DOENV')]

        self.neo_host = os.environ.get("NEO_HOST",'localhost')
        self.neo_port = os.environ.get("NEO_PORT", 7687)
        self.neo_user = os.environ.get("NEO_USER", '')
        self.neo_pass = os.environ.get("NEO_PASS", '')
        self.neo_database = os.environ.get("NEO_DATABASE")

        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        self.aws_default_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.aws_s3_bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "")

        self.jwt_secret: str = os.environ.get("JWT_SECRET", '')

        self.frontend_origin = [
            origin.strip()
            for origin in os.environ.get(
                'FRONTEND_ORIGINS', 
                'http://localhost:3000, http://localhost'
                ).split(',')
                if origin.strip()
                ]
        if not self.aws_s3_bucket_name:
            raise RuntimeError("Missing AWS_S3_BUCKET_NAME in environments")
        
        if not self.jwt_secret:
            raise RuntimeError('Missing JWT_SECRET in enviroments')
        
        if self.stage == STAGE.PROD:
            self.neo_uri = f'neo4j+s://{self.neo_host}.databases.neo4j.io'
        else:
            self.neo_uri = f'neo4j://{self.neo_host}:{self.neo_port}'

    @staticmethod
    def get_envs() -> "Environments":
        envs = Environments()
        envs.load_envs()
        return envs
    
env = Environments.get_envs()