from __future__ import annotations

from src.config import settings
from src.core.embedder import get_embedder
from src.core.llm import get_llm_provider
from src.core.reranker import get_reranker
from src.core.vectorstore import get_vectorstore
from src.models.schemas import QueryResponse, Source

RETRIEVAL_POOL = 20

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

    async def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        k = top_k or settings.TOP_K

        query_embedding = self._embedder.embed_query(question)

        results = self._vectorstore.query(
            query_embedding=query_embedding,
            n_results=RETRIEVAL_POOL,
        )

        context_parts = []
        sources = []

        if results["documents"] and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            ids = results["ids"][0]
            distances = results["distances"][0]

            reranked_indices = self._reranker.rerank(question, docs, top_k=k)

            for rank, i in enumerate(reranked_indices):
                doc = docs[i]
                meta = metas[i]
                chunk_id = ids[i]
                relevance = 1.0 - distances[i]

                context_parts.append(
                    f"[CHUNK_ID: {chunk_id}]\n{doc}"
                )

                section = meta.get("header_path", "") or meta.get("source_file", "")
                sources.append(Source(
                    chunk_id=chunk_id,
                    source_file=meta.get("source_file", ""),
                    section=section,
                    relevance_score=round(relevance, 4),
                    text_preview=doc[:200] + "..." if len(doc) > 200 else doc,
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
