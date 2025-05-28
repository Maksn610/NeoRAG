from typing import List, Tuple

# Prompt builder for LLM context
class PromptBuilder:
    """
    Builds a prompt for the LLM using retrieved context documents and user query.
    """

    def __init__(self, system_instruction: str = None):
        self.system_instruction = system_instruction or (
            "You are a helpful medical assistant. Answer based on the provided context. You may summarize or rephrase if helpful, but do not fabricate information."
        )

    def build_prompt(self, query: str, retrieved_docs: List[Tuple[str, float]]) -> str:
        """
        Constructs a prompt for LLM using user query and context from top documents.

        :param query: User's input question.
        :param retrieved_docs: List of tuples (doc_text, score).
        :return: Prompt string.
        """
        context_blocks = [f"- {text.strip()}" for text, _ in retrieved_docs]
        context_text = "\n".join(context_blocks)

        full_prompt = f"""{self.system_instruction}

Context:
{context_text}

Question: {query}
Answer:"""
        return full_prompt


if __name__ == "__main__":
    docs = [
        ("Study A found that treatment X improved condition Y.", 0.87),
        ("Another result confirmed similar outcomes.", 0.83),
    ]
    builder = PromptBuilder()
    result_prompt = builder.build_prompt(
        query="What are the effects of treatment X?",
        retrieved_docs=docs
    )
    print(result_prompt)