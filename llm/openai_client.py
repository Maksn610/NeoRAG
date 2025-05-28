from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...")

# OpenAI API client for embeddings and completions
class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=model
        )
        return response.data[0].embedding

    def generate_response(self, prompt: str, model: str = "gpt-4o") -> str:
        messages: List[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    ai = OpenAIClient()

    embed = ai.get_embedding("What is a graph database?")
    print("Embedding size:", len(embed))

    reply = ai.generate_response("What are graph databases good for?")
    print("LLM says:", reply)
