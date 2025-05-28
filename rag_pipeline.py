from pathlib import Path
from graph.connector import Neo4jConnector
from graph.node_manager import NodeManager
from graph.index_manager import IndexManager
from llm.openai_client import OpenAIClient
from llm.prompt_builder import PromptBuilder
import fitz

# Extract text from PDF
def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(str(pdf_path))
    full_text = []
    for page in doc:
        full_text.append(page.get_text())
    return "\n".join(full_text)

# Ingest text into Neo4j
def ingest_text(text: str, doc_id: str = "doc_1"):
    connector = Neo4jConnector()
    node_manager = NodeManager(connector)
    index_manager = IndexManager(connector)
    openai_client = OpenAIClient()

    # Use full text as one chunk
    embedding = openai_client.get_embedding(text)
    node_manager.create_doc_node(doc_id=doc_id, text=text)
    node_manager.update_doc_embedding(doc_id=doc_id, embedding=embedding)

    index_manager.create_vector_index()
    connector.close()

# Search for relevant documents
def search_docs(query: str, top_k=3):
    connector = Neo4jConnector()
    openai_client = OpenAIClient()
    embedding = openai_client.get_embedding(query)

    cypher = """
    CALL db.index.vector.queryNodes('doc_index', $top_k, $embedding)
    YIELD node, score
    RETURN node.text AS text, score
    """
    results = connector.execute_read(cypher, {"embedding": embedding, "top_k": top_k})
    connector.close()

    return [(r["text"], r["score"]) for r in results]

# Generate GPT answer
def generate_answer(query: str, retrieved_docs):
    prompt_builder = PromptBuilder()
    prompt = prompt_builder.build_prompt(query, retrieved_docs)

    openai_client = OpenAIClient()
    response = openai_client.generate_response(prompt)
    return response

# Main entry point
def main():
    # Set path to PDF
    pdf_path = Path("data/COPD_overview.pdf")

    # Extract text from PDF
    print("[INFO] Extracting text from PDF...")
    full_text = extract_text_from_pdf(pdf_path)

    # Ingest text into Neo4j
    print("[INFO] Ingesting text into Neo4j...")
    ingest_text(full_text, doc_id="medical_doc_1")

    # Cycle for user queries
    print("[INFO] Ready for questions. Type 'exit' to quit.")
    while True:
        query = input("Your question: ").strip()

        if not query:
            print("[WARN] You entered an empty question. Try again.")
            continue

        if query.lower() == "exit":
            break

        try:
            retrieved_docs = search_docs(query)
            answer = generate_answer(query, retrieved_docs)
            print("\nAnswer:\n", answer, "\n")
        except Exception as e:
            print(f"[ERROR] Failed to generate answer: {e}")


if __name__ == "__main__":
    main()
