from __future__ import annotations

import time
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.router import api_router

logger = logging.getLogger(__name__)


def _wait_for_chromadb(max_retries: int = 30, delay: float = 2.0) -> None:
    """Block until ChromaDB is reachable, retrying with a delay."""
    from src.config import settings
    import httpx

    url = f"http://{settings.CHROMA_HOST}:{settings.CHROMA_PORT}/api/v2/heartbeat"
    for attempt in range(1, max_retries + 1):
        try:
            resp = httpx.get(url, timeout=5.0)
            resp.raise_for_status()
            logger.info("ChromaDB ready (attempt %d)", attempt)
            return
        except Exception:
            logger.info("Waiting for ChromaDB... (%d/%d)", attempt, max_retries)
            time.sleep(delay)
    raise RuntimeError("ChromaDB not reachable after %d attempts" % max_retries)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _wait_for_chromadb()
    yield


app = FastAPI(
    title="RAG Service",
    description="Retrieval-Augmented Generation service for Anthropic Claude documentation",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)

static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
