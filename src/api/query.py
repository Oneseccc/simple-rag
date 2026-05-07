from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.core.cache import get_cache
from src.core.rag import get_rag_pipeline
from src.models.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    cache = get_cache()
    cached = cache.get(request.question, request.top_k)
    if cached:
        return QueryResponse(**cached)

    pipeline = get_rag_pipeline()

    try:
        result = await pipeline.query(
            question=request.question,
            top_k=request.top_k,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

    cache.put(request.question, request.top_k, result.model_dump())
    return result
