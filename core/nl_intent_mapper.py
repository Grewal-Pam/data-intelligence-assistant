import re
from typing import Dict


def map_nl_to_intent(text: str) -> Dict:
    """
    Map natural language text to a known intent and parameters.
    Deterministic, rule-based, safe.
    """

    text = text.lower()

    # -----------------------------
    # Blood pressure by smoking
    # -----------------------------
    if "blood pressure" in text or "bp" in text:

        # Explicit numeric smoking value
        match = re.search(r"smoking\s*=\s*([01])", text)
        if match:
            return {
                "intent": "bp_by_smoking",
                "params": {"smoking_status": int(match.group(1))}
            }

        # Semantic phrases
        if "non-smoker" in text or "non smoker" in text:
            return {
                "intent": "bp_by_smoking",
                "params": {"smoking_status": 0}
            }

        if "smoker" in text:
            return {
                "intent": "bp_by_smoking",
                "params": {"smoking_status": 1}
            }

        # Missing parameter case
        return {
            "intent": "bp_by_smoking",
            "params": {}
        }

   # -----------------------------
    # BMI change by participant (SPECIFIC)
    # -----------------------------
    match = re.search(r"\b(p\d+)\b", text)
    if match and "bmi" in text and "change" in text:
        return {
            "intent": "bmi_change_by_participant",
            "params": {"participant_id": match.group(1).upper()}
        }

    # -----------------------------
    # BMI change (GENERIC)
    # -----------------------------
    if "bmi" in text and "change" in text:
        return {
            "intent": "bmi_change",
            "params": {}
        }


    # -----------------------------
    # Sleep by education
    # -----------------------------
    if "sleep" in text and "education" in text:
        return {
            "intent": "sleep_by_education",
            "params": {}
        }

    raise ValueError("Could not map text to a known intent")
