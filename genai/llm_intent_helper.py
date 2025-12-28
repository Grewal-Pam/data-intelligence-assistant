import os
import json
from typing import Dict
from groq import Groq


class LLMIntentHelper:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def suggest_intent(self, question: str) -> Dict:
        """
        Ask LLM to convert question into intent + params.
        Must return JSON ONLY.
        """

        prompt = f"""
You are a system that converts natural language questions into JSON.

Return ONLY valid JSON.
DO NOT explain.
DO NOT add text.

Allowed intents:
- bmi_change
- bmi_change_by_participant
- bp_by_smoking
- sleep_by_education

Rules:
- participant_id must look like P001, P002, etc
- smoking_status must be 0 or 1
- If unsure, return intent="unknown"

Question:
{question}

JSON:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"intent": "unknown", "params": {}}
