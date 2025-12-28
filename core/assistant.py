from core.intent_executor import execute_intent, MissingParameterError
from core.nl_intent_mapper import map_nl_to_intent

from genai.llm_intent_helper import LLMIntentHelper
from core.nl_intent_mapper import map_nl_to_intent


llm = LLMIntentHelper()

def ask(question: str):
    try:
        # 1️⃣ Try deterministic rules FIRST
        try:
            mapped = map_nl_to_intent(question)
            intent = mapped["intent"]
            params = mapped["params"]
        except ValueError:
            # 2️⃣ Only if rules fail → ask LLM
            llm_guess = llm.suggest_intent(question)
            intent = llm_guess["intent"]
            params = llm_guess.get("params", {})

        df = execute_intent(intent, params)

        if df.empty:
            return {
                "status": "ok",
                "intent": intent,
                "rows": 0,
                "message": "No matching data found."
            }

        return {
            "status": "ok",
            "intent": intent,
            "rows": len(df),
            "data": df
        }

    except MissingParameterError as e:
        return {
            "status": "needs_clarification",
            "intent": e.intent,
            "required": e.missing_params,
            "message": f"I need more information: {e.missing_params}"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}



#if __name__ == "__main__":
 #   q = "bmi change participant p002"
  #  print(ask(q))

if __name__ == "__main__":
    print("🧠 Data Intelligence Assistant (type 'exit' to quit)\n")

    while True:
        question = input("You: ")

        if question.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        result = ask(question)

        print("\nAssistant:")
        print(result)
        print("-" * 40)
