from typing import Dict
from core.intents import INTENT_REGISTRY
from core.query_runner import run_query


class UnknownIntentError(Exception):
    pass


class MissingParameterError(Exception):
    def __init__(self, intent: str, missing_params: list):
        self.intent = intent
        self.missing_params = missing_params
        message = (
            f"Missing parameters for intent '{intent}': {missing_params}"
        )
        super().__init__(message)



def execute_intent(intent: str, params: Dict = None):
    if intent not in INTENT_REGISTRY:
        raise UnknownIntentError(f"Unknown intent: {intent}")

    intent_config = INTENT_REGISTRY[intent]

    required_params = intent_config["required_params"]
    params = params or {}

    missing = [p for p in required_params if p not in params]
    if missing:
        raise MissingParameterError(
        intent=intent,
        missing_params=missing
    )


    query_file = intent_config["query_file"]

    return run_query(query_file, params)

if __name__ == "__main__":
    df = execute_intent(
        "bp_by_smoking",
        params={"smoking_status": 1}
    )
    print(df)

