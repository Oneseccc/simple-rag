from __future__ import annotations

import chromadb

from src.config import settings


class VectorStore:
    def __init__(self, host: str, port: int, collection_name: str):
        self._client = chromadb.HttpClient(host=host, port=port)
        self._collection_name = collection_name
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end = i + batch_size
            self._collection.upsert(
                ids=ids[i:end],
                documents=texts[i:end],
                embeddings=embeddings[i:end],
                metadatas=metadatas[i:end],
            )

    def query(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> dict:
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )
        return results

    def get_collection_stats(self) -> dict:
        count = self._collection.count()
        peek = self._collection.peek(limit=1)
        source_files = set()
        if peek.get("metadatas"):
            for meta in peek["metadatas"]:
                if meta and meta.get("source_file"):
                    source_files.add(meta["source_file"])
        return {
            "chunks": count,
            "documents": len(source_files) if source_files else 0,
        }

    def reset_collection(self) -> None:
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )


_vectorstore: VectorStore | None = None


def get_vectorstore() -> VectorStore:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = VectorStore(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            collection_name=settings.CHROMA_COLLECTION,
        )
    return _vectorstore
