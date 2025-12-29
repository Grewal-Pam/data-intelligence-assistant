from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"
COLLECTION_NAME = "dzne_context"

class ContextRetriever:
    def __init__(self, threshold: float = 0.55):
        self.threshold = threshold
        self.client = chromadb.PersistentClient(path=str(DB_DIR))
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.col = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embed_fn
        )

    def retrieve(self, question: str, top_k: int = 3):
        res = self.col.query(query_texts=[question], n_results=top_k)

        hits = []
        for text, meta, dist in zip(
            res["documents"][0],
            res["metadatas"][0],
            res["distances"][0],
        ):
            similarity = 1 - dist

            # 🔹 Lower bar for glossary / metrics
            min_sim = 0.35 if meta["source"] in {"glossary.md", "metrics.md"} else self.threshold

            if similarity >= min_sim:
                hits.append((text, meta, similarity))

        return hits
