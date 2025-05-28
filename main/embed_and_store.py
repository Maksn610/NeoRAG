from graph.connector import Neo4jConnector
from graph.node_manager import NodeManager
from llm.openai_client import OpenAIClient

# Store embedded text in Neo4j
def embed_and_store(doc_id: str, full_text: str):
    connector = Neo4jConnector()
    node_manager = NodeManager(connector)
    client = OpenAIClient()

    docs = [full_text]  # Store the whole text as one document

    for i, doc in enumerate(docs):
        full_doc_id = f"{doc_id}_{i}"
        embedding = client.get_embedding(doc)
        node_manager.create_doc_node(doc_id=full_doc_id, text=doc)
        node_manager.update_doc_embedding(doc_id=full_doc_id, embedding=embedding)

    connector.close()

if __name__ == "__main__":
    sample_text = (
        "This medical study evaluated the effectiveness of treatment A for disease B. "
        "Results showed statistically significant improvement compared to placebo. "
        "Side effects were mild and infrequent."
    )
    embed_and_store("custom_doc_001", sample_text)
