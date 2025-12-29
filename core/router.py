def needs_context(question: str) -> bool:
    keywords = [
        "what is", "what does", "meaning",
        "define", "explain", "why"
    ]
    q = question.lower()
    return any(k in q for k in keywords)
