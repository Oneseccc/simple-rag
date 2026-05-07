from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.core.rag import get_rag_pipeline
from src.models.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    pipeline = get_rag_pipeline()

    try:
        result = await pipeline.query(
            question=request.question,
            top_k=request.top_k,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

    return result
