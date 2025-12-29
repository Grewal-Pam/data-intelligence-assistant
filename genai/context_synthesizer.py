import os
from groq import Groq


class ContextSynthesizer:
    """
    Uses an LLM to synthesize an answer ONLY from retrieved context.
    Prevents hallucination.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model

    def synthesize(self, question: str, context: str) -> str:
        prompt = f"""
You are a scientific assistant.

Answer the question ONLY using the provided context.
Do NOT add external knowledge.
If context is insufficient, say so clearly.

Question:
{question}

Context:
{context}

Answer clearly and concisely.
Do NOT speculate.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()
