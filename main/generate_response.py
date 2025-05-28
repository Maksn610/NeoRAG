from main.search_engine import search_similar_docs
from llm.openai_client import OpenAIClient
from llm.prompt_builder import PromptBuilder

# Generate answer using LLM and search
def generate_answer(user_query: str) -> str:
    retrieved_docs = search_similar_docs(user_query, top_k=3)
    prompt_builder = PromptBuilder()
    prompt = prompt_builder.build_prompt(user_query, retrieved_docs)

    client = OpenAIClient()
    response = client.generate_response(prompt)
    return response

if __name__ == "__main__":
    query = input("Enter your medical question: ").strip()
    answer = generate_answer(query)
    print("\nAnswer:")
    print(answer)
