import os
from enum import Enum
from dotenv import load_dotenv
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
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

        self.jwt_secret: str = os.environ.get("JWT_SECRET", '')

        self.repo_user = self.get_repository_user()

        if not self.jwt_secret:
            raise RuntimeError('Missing JWT_SECRET in enviroments')
        
        self.NEO_URL = f'neo4j://{self.neo_host}:{self.neo_port}'

    @staticmethod
    def get_envs() -> "Environments":
        envs = Environments()
        envs.load_envs()
        return envs

    def get_repository_user(self):
        return UserRepositoryMock()

env = Environments.get_envs()