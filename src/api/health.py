from __future__ import annotations

from fastapi import APIRouter

from src.config import settings
from src.core.vectorstore import get_vectorstore

router = APIRouter()


@router.get("/health")
async def health_check():
    vs = get_vectorstore()
    try:
        stats = vs.get_collection_stats()
        chroma_ok = True
    except Exception:
        stats = {"documents": 0, "chunks": 0}
        chroma_ok = False

    return {
        "status": "ok" if chroma_ok else "degraded",
        "chroma_connected": chroma_ok,
        "llm_provider": settings.LLM_PROVIDER,
        "documents_count": stats.get("documents", 0),
        "chunks_count": stats.get("chunks", 0),
    }
