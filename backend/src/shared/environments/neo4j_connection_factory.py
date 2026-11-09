from src.shared.environments.environments import env
from neo4j import GraphDatabase

class Neo4JConnectionFactory:
    
    def __init__(self) -> None:
        self.driver = GraphDatabase().driver(
            uri = env.neo_uri,
            auth=(env.neo_user, env.neo_pass)
        )
        self.database = env.neo_database

    def execute_read(self, callback):
        with self.driver.session(database=self.database) as session:
            return session.execute_read(callback)

    def execute_write(self, callback):
        with self.driver.session(database=self.database) as session:
            return session.execute_write(callback)

    def close(self):
        self.driver.close()

connection = Neo4JConnectionFactory()