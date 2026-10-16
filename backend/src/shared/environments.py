import os
from enum import Enum

class STAGE(Enum):
    DOTENV = 'DOTENV'
    TEST = 'TEST'
    PROD = "PROD"

class Environments:

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE", STAGE.DOTENV.value) 

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]

        self.mongo_host = os.environ.get("MONGO_HOST",'localhost')
        self.mongo_port = os.environ.get("MONGO_PORT", 27017)
        self.mongo_user = os.environ.get("MONGO_USER", '')
        self.mongo_pass = os.environ.get("MONGO_PASS", '')

        if self.stage == STAGE.TEST.value:
            self.mongo_url = f'mongodb://{self.mongo_host}:{self.mongo_port}/'
        else:
            self.mongo_url = f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:{self.mongo_port}/"

    @staticmethod
    def get_envs() -> "Environments":
        envs = Environments()
        envs.load_envs()
        return envs