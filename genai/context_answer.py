from rag.retriever import ContextRetriever
from genai.context_synthesizer import ContextSynthesizer


def answer_from_context(question: str, top_k: int = 3):
    retriever = ContextRetriever()
    hits = retriever.retrieve(question, top_k=top_k)

    if not hits:
        return {
            "status": "no_context",
            "message": "No relevant documentation found."
        }

    context_blocks = []
    citations = []

    for text, meta, sim in hits:
        context_blocks.append(text)
        citations.append(f"{meta['source']}#chunk{meta['chunk']}")
        
    # Combine retrieved chunks
    context_text = "\n\n".join([text for text, meta, sim in hits])

    synthesizer = ContextSynthesizer()
    answer = synthesizer.synthesize(question, context_text)

    citations = [
        f"{meta['source']}#chunk{meta['chunk']}"
        for _, meta, _ in hits
    ]

    return {
        "status": "ok",
        "question": question,
        "answer": answer,
        "citations": citations
    }
