from graph.connector import Neo4jConnector

# Vector index management for Neo4j
default_label = "Document"
class IndexManager:
    def __init__(self, connector: Neo4jConnector):
        self.db = connector

    def create_vector_index(self, index_name: str = "doc_index", dimension: int = 1536):
        query = f"""
        CREATE VECTOR INDEX {index_name} IF NOT EXISTS
        FOR (d:{default_label})
        ON (d.embedding)
        OPTIONS {{
            indexConfig: {{
                `vector.dimensions`: {dimension},
                `vector.similarity_function`: 'cosine'
            }}
        }}
        """
        self.db.execute_write(query)
