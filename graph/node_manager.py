from typing import List, Union
from graph.connector import Neo4jConnector

# Node management for Neo4j
default_label = "Document"
class NodeManager:
    def __init__(self, connector: Neo4jConnector):
        self.db = connector

    def create_doc_node(self, doc_id: str, text: str):
        query = f"""
        CREATE (d:{default_label} {{doc_id: $doc_id, text: $text}})
        """
        self.db.execute_write(query, {"doc_id": doc_id, "text": text})

    def update_doc_embedding(self, doc_id: str, embedding: List[float]):
        query = f"""
        MATCH (d:{default_label} {{doc_id: $doc_id}})
        SET d.embedding = $embedding
        """
        self.db.execute_write(query, {"doc_id": doc_id, "embedding": embedding})

    def get_all_docs(self) -> List[dict]:
        query = f"MATCH (d:{default_label}) RETURN d.doc_id AS id, d.text AS text"
        return self.db.execute_read(query)

if __name__ == "__main__":
    from pprint import pprint
    db = Neo4jConnector()
    manager = NodeManager(db)

    manager.create_doc_node("doc_001", "Example text for testing.")

    fake_embedding = [0.1] * 1536
    manager.update_doc_embedding("doc_001", fake_embedding)

    pprint(manager.get_all_docs())

    db.close()