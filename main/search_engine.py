from typing import List, Tuple
from graph.connector import Neo4jConnector
from llm.openai_client import OpenAIClient

# Search for similar documents in Neo4j
def search_similar_docs(query: str, top_k: int = 3) -> List[Tuple[str, float]]:
    connector = Neo4jConnector()
    client = OpenAIClient()
    embedding = client.get_embedding(query)

    vector_query = """
    CALL db.index.vector.queryNodes('doc_index', $top_k, $embedding)
    YIELD node, score
    RETURN node.text AS text, score
    """

    results = connector.execute_read(vector_query, {"embedding": embedding, "top_k": top_k})
    connector.close()

    return [(row["text"], row["score"]) for row in results]

if __name__ == "__main__":
    query = "What are the effects of treatment X?"
    results = search_similar_docs(query)

    for i, (text, score) in enumerate(results):
        print(f"[{i+1}] Score: {score:.4f}")
        print(text[:200])
        print("-" * 40)
