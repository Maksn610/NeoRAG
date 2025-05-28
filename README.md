# RAG Graph Pipeline with Neo4j & OpenAI

This project implements a lightweight Retrieval-Augmented Generation (RAG) pipeline using:
- `Neo4j` as a graph database for storing embedded document data
- `OpenAI` APIs for embedding generation and response generation (e.g., GPT-4o)
- `PyMuPDF` for PDF parsing
- `FPDF` for generating test documents

---

## Features

- PDF ingestion and preprocessing
- Embedding via OpenAI (`text-embedding-3-small`)
- Graph storage in Neo4j with vector indexing
- Similarity-based search using `db.index.vector.queryNodes`
- Prompt generation and LLM response (`gpt-4o`)
- Terminal-based interactive querying

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-graph.git
cd rag-graph
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # on Linux/macOS
.venv\Scripts\activate           # on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required `.env` Configuration

Create a `.env` file in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=sk-...
```

---

## Neo4j Setup (Local Docker)

If you don't already have a Neo4j instance:

```bash
docker run \
  --name neo4j-graph \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  -e NEO4J_PLUGINS='["graph-data-science"]' \
  neo4j:5.14
```

> Visit [http://localhost:7474](http://localhost:7474) and log in with `neo4j/your_password`.

---

## Generate Sample Data

Run this script to generate a sample PDF:

```bash
python generate_data.py
```

It will create a file at: `data/sample_medical_document.pdf`

---

## Run the Full Pipeline

Execute the pipeline end-to-end:

```bash
python rag_pipeline.py
```

It will:

* Extract text from the PDF
* Embed the text
* Store embeddings and nodes in Neo4j
* Create a vector index
* Enter an interactive prompt for question answering

---

## Example Interaction

```text
Your question: What are graph databases used for?

Answer:
Graph databases are useful when your data is highly connected and queries depend on relationships between entities...
```

---

## Project Structure

```
├── data/
│   └── sample_medical_document.pdf
├── graph/
│   ├── connector.py
│   ├── node_manager.py
│   └── index_manager.py
├── llm/
│   ├── openai_client.py
│   └── prompt_builder.py
├── utils/
├── main/
│   ├── embed_and_store.py
│   ├── ingest_dataset.py
│   ├── search_engine.py
│   └── generate_response.py
├── rag_pipeline.py
├── generate_data.py
├── requirements.txt
└── .env
```
