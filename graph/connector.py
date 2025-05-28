from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def execute_read(self, query: str, parameters: dict = None):
        with self.driver.session() as session:
            return session.execute_read(lambda tx: tx.run(query, parameters or {}).data())

    def execute_write(self, query: str, parameters: dict = None):
        with self.driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, parameters or {}))


if __name__ == "__main__":
    db = Neo4jConnector()
    res = db.execute_read("RETURN 1 AS test")
    print("Test:", res)
    db.close()
