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
        self.jwt_secret: str = os.environ.get("JWT_SECRET", '')

        if not self.jwt_secret:
            raise RuntimeError('Missing JWT_SECRET in enviroments')
        
        self.neo_uri = f'neo4j+s://{self.neo_host}.databases.neo4j.io' if self.stage == STAGE.PROD else f'neo4j://{self.neo_host}:{self.neo_port}'

    @staticmethod
    def get_envs() -> "Environments":
        envs = Environments()
        envs.load_envs()
        return envs
    
env = Environments.get_envs()