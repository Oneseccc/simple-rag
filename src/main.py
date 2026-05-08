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


def _auto_ingest_if_empty() -> None:
    """Ingest the corpus on first startup if the collection is empty."""
    from src.core.vectorstore import get_vectorstore
    from src.core.cache import get_cache
    from src.core.chunker import chunk_documents
    from src.core.embedder import get_embedder

    vs = get_vectorstore()
    stats = vs.get_collection_stats()
    if stats.get("chunks", 0) > 0:
        logger.info("Collection already has %d chunks, skipping auto-ingest", stats["chunks"])
        return

    corpus_dir = Path("/app/corpus/anthropic")
    if not corpus_dir.exists():
        logger.warning("Corpus dir %s not found, skipping auto-ingest", corpus_dir)
        return

    logger.info("Collection is empty — auto-ingesting from %s", corpus_dir)
    supported = [f for f in corpus_dir.rglob("*") if f.suffix.lower() in (".md", ".txt", ".pdf")]
    if not supported:
        logger.warning("No supported files found in corpus dir")
        return

    all_chunks: list[dict] = []
    for file_path in supported:
        try:
            if file_path.suffix.lower() in (".md", ".txt"):
                content = file_path.read_text(encoding="utf-8", errors="replace")
            elif file_path.suffix.lower() == ".pdf":
                import pymupdf4llm
                content = pymupdf4llm.to_markdown(str(file_path))
            else:
                continue
        except Exception as e:
            logger.warning("Failed to read %s: %s", file_path.name, e)
            continue

        if not content or not content.strip():
            continue

        is_markdown = file_path.suffix.lower() in (".md", ".pdf")
        chunks = chunk_documents(
            content=content,
            source_file=file_path.name,
            chunk_size=512,
            chunk_overlap=50,
            is_markdown=is_markdown,
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        logger.warning("No chunks produced from corpus")
        return

    embedder = get_embedder()
    texts = [c["text"] for c in all_chunks]
    embeddings = embedder.embed_texts(texts)

    chunk_ids = [c["chunk_id"] for c in all_chunks]
    metadatas = [c["metadata"] for c in all_chunks]
    vs.add_documents(ids=chunk_ids, texts=texts, embeddings=embeddings, metadatas=metadatas)

    get_cache().index_chunks(all_chunks)

    logger.info("Auto-ingest complete: %d files, %d chunks", len(supported), len(all_chunks))


@asynccontextmanager
async def lifespan(app: FastAPI):
    _wait_for_chromadb()
    _auto_ingest_if_empty()
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
