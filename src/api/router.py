from __future__ import annotations

from fastapi import APIRouter

from src.api.health import router as health_router
from src.api.ingest import router as ingest_router
from src.api.query import router as query_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(ingest_router, tags=["ingestion"])
api_router.include_router(query_router, tags=["query"])
