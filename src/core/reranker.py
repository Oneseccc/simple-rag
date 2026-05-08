from __future__ import annotations

from sentence_transformers import CrossEncoder

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    def __init__(self):
        self._model = CrossEncoder(RERANKER_MODEL)

    def rerank(
        self,
        question: str,
        documents: list[str],
        top_k: int = 5,
    ) -> list[int]:
        """Score each (question, document) pair and return indices of the top_k highest-scoring documents."""
        pairs = [[question, doc] for doc in documents]
        scores = self._model.predict(pairs)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return ranked[:top_k]


_reranker: Reranker | None = None


def get_reranker() -> Reranker:
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker
