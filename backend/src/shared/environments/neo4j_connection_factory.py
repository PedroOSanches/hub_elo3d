from src.shared.environments.environments import env
from neo4j import GraphDatabase

class Neo4JConnectionFactory:
    
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            uri=env.neo_uri,
            auth=(env.neo_user, env.neo_pass)
        )

    def get_session(self):
        return self.driver.session()

    def close(self):
        self.driver.close()