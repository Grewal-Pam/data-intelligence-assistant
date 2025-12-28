import os
import pandas as pd
from groq import Groq


class ResultExplainer:
    """
    Uses an LLM to explain query results in natural language.
    The LLM NEVER generates SQL or touches the database.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model

    def explain(self, question: str, df: pd.DataFrame) -> str:
        """
        Generate a natural-language explanation of query results.
        """

        if df.empty:
            return "No data was found that matches the query."

        preview = df.head(5).to_string(index=False)

        prompt = f"""
You are a data analyst supporting medical researchers.

User question:
{question}

Query result (preview):
{preview}

Explain the result clearly in simple language.
If any values are NULL or missing, explicitly say that the result cannot be fully interpreted.
Do NOT assume trends, improvements, or health outcomes unless directly shown in the data.
Do NOT speculate beyond the data provided.

"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You explain data analysis results clearly and cautiously."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
