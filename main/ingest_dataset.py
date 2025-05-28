import json
from pathlib import Path
from graph.connector import Neo4jConnector
from graph.node_manager import NodeManager
from graph.index_manager import IndexManager
from llm.openai_client import OpenAIClient

DATA_PATH = Path("data/training_reviews.json")
NUM_RECORDS = 500

# Ingest abstracts from dataset into Neo4j
def ingest_abstracts():
    connector = Neo4jConnector()
    node_manager = NodeManager(connector)
    index_manager = IndexManager(connector)
    openai_client = OpenAIClient()

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)  # it's not JSONL, but JSON array

        for i, record in enumerate(data):
            if i >= NUM_RECORDS:
                break

            doc_id = record.get("docid", f"doc_{i}")
            abstract = record.get("abstract", "").strip()
            if not abstract:
                continue

            docs = [abstract]  # Store the whole text as one document
            for j, doc in enumerate(docs):
                full_doc_id = f"{doc_id}_{j}"
                embedding = openai_client.get_embedding(doc)
                node_manager.create_doc_node(doc_id=full_doc_id, text=doc)
                node_manager.update_doc_embedding(doc_id=full_doc_id, embedding=embedding)

    index_manager.create_vector_index()
    connector.close()

if __name__ == "__main__":
    ingest_abstracts()
