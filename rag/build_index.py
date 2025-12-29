from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DB_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"
COLLECTION_NAME = "dzne_context"

def chunk_text(text: str, max_chars: int = 150):
    # Simple safe chunking by paragraphs
    paras = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, current = [], ""
    for p in paras:
        if len(current) + len(p) + 1 <= max_chars:
            current += (" " + p) if current else p
        else:
            chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks

def main():
    client = chromadb.PersistentClient(path=str(DB_DIR))

    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    col = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )

    # reset collection (simple + safe for now)
    try:
        client.delete_collection(COLLECTION_NAME)
        col = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn
        )
    except Exception:
        pass

    doc_files = sorted(DOCS_DIR.glob("*.md"))
    if not doc_files:
        raise FileNotFoundError(f"No markdown files found in {DOCS_DIR}")

    ids, docs, metas = [], [], []
    idx = 0

    for f in doc_files:
        text = f.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for c_i, chunk in enumerate(chunks):
            ids.append(f"{f.stem}_{c_i}")
            docs.append(chunk)
            metas.append({"source": f.name, "chunk": c_i})
            idx += 1

    col.add(ids=ids, documents=docs, metadatas=metas)
    print(f"✅ Indexed {len(docs)} chunks into ChromaDB at {DB_DIR}")

if __name__ == "__main__":
    main()
