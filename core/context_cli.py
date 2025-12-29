from genai.context_answer import answer_from_context

if __name__ == "__main__":
    print("📚 Context Assistant (type 'exit')\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        out = answer_from_context(q, top_k=3)
        print("\nAssistant:")
        print(out)
        print("-" * 50)
