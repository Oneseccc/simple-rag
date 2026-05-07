from __future__ import annotations

import logging

from src.config import settings
from src.core.cache import get_cache
from src.core.embedder import get_embedder
from src.core.llm import get_llm_provider
from src.core.reranker import get_reranker
from src.core.vectorstore import get_vectorstore
from src.models.schemas import QueryResponse, Source

logger = logging.getLogger(__name__)

RETRIEVAL_POOL = 20
RRF_K = 60

SYSTEM_PROMPT = """You are a helpful assistant answering questions about Anthropic Claude documentation.

Rules:
1. Use ONLY the provided context to answer. Do not use prior knowledge.
2. If the context does not contain enough information to answer, say "I don't have enough information in the provided documents to answer this question."
3. Cite the relevant chunk IDs in your answer using [chunk_id] notation.
4. Be concise and accurate.
5. If multiple chunks are relevant, synthesize the information and cite all relevant chunks."""


class RAGPipeline:
    def __init__(self):
        self._embedder = get_embedder()
        self._vectorstore = get_vectorstore()
        self._llm = get_llm_provider()
        self._reranker = get_reranker()

    def _hybrid_retrieve(self, question: str, query_embedding: list[float]) -> list[dict]:
        """Retrieve from both vector and keyword search, merge with RRF."""
        vector_results = self._vectorstore.query(
            query_embedding=query_embedding,
            n_results=RETRIEVAL_POOL,
        )

        candidates: dict[str, dict] = {}
        rrf_scores: dict[str, float] = {}
        origins: dict[str, set[str]] = {}

        if vector_results["documents"] and vector_results["documents"][0]:
            for rank, (chunk_id, doc, meta, dist) in enumerate(zip(
                vector_results["ids"][0],
                vector_results["documents"][0],
                vector_results["metadatas"][0],
                vector_results["distances"][0],
            )):
                candidates[chunk_id] = {"text": doc, "metadata": meta, "distance": dist}
                rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1.0 / (RRF_K + rank + 1)
                origins.setdefault(chunk_id, set()).add("vector")

        try:
            fts_results = get_cache().keyword_search(question, limit=RETRIEVAL_POOL)
            for rank, hit in enumerate(fts_results):
                cid = hit["chunk_id"]
                if cid not in candidates:
                    candidates[cid] = {"text": hit["text"], "metadata": hit["metadata"], "distance": 0.5}
                rrf_scores[cid] = rrf_scores.get(cid, 0) + 1.0 / (RRF_K + rank + 1)
                origins.setdefault(cid, set()).add("keyword")
        except Exception as e:
            logger.warning("FTS5 keyword search failed, using vector-only: %s", e)

        sorted_ids = sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)
        results = []
        for cid in sorted_ids:
            o = origins.get(cid, set())
            if "vector" in o and "keyword" in o:
                method = "vector & keyword"
            elif "keyword" in o:
                method = "keyword"
            else:
                method = "vector"
            results.append({"chunk_id": cid, "retrieval_method": method, **candidates[cid]})
        return results

    async def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        k = top_k or settings.TOP_K

        query_embedding = self._embedder.embed_query(question)

        merged = self._hybrid_retrieve(question, query_embedding)

        context_parts = []
        sources = []

        if merged:
            merged_docs = [c["text"] for c in merged]
            reranked_indices = self._reranker.rerank(question, merged_docs, top_k=k)

            for i in reranked_indices:
                c = merged[i]
                meta = c["metadata"]
                chunk_id = c["chunk_id"]
                relevance = 1.0 - c["distance"]

                context_parts.append(
                    f"[CHUNK_ID: {chunk_id}]\n{c['text']}"
                )

                section = meta.get("header_path", "") or meta.get("source_file", "")
                sources.append(Source(
                    chunk_id=chunk_id,
                    source_file=meta.get("source_file", ""),
                    section=section,
                    relevance_score=round(relevance, 4),
                    retrieval_method=c.get("retrieval_method", "vector"),
                    text_preview=c["text"][:200] + "..." if len(c["text"]) > 200 else c["text"],
                ))

        context = "\n\n".join(context_parts) if context_parts else "No relevant documents found."

        user_prompt = f"""Context:
{context}

Question: {question}

Answer the question based on the context above. Cite chunk IDs using [chunk_id] notation."""

        answer = await self._llm.generate(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT,
        )

        return QueryResponse(
            answer=answer,
            sources=sources,
            model=self._llm.get_model_name(),
            provider=self._llm.get_provider_name(),
        )


_pipeline: RAGPipeline | None = None


def get_rag_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline
