from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.config import settings


class Embedder:
    def __init__(self, model_name: str):
        self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self._model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self._model.encode(query, show_progress_bar=False)
        return embedding.tolist()


_embedder: Embedder | None = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder(settings.EMBEDDING_MODEL)
    return _embedder
