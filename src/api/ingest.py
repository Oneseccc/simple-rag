from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pathlib import Path

from src.config import settings
from src.core.cache import get_cache
from src.core.chunker import chunk_documents
from src.core.embedder import get_embedder
from src.core.vectorstore import get_vectorstore
from src.models.schemas import IngestRequest, IngestResponse

router = APIRouter()


def _load_file(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        import pymupdf4llm
        return pymupdf4llm.to_markdown(str(path))
    return None


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest):
    folder = Path(request.folder_path)
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=400, detail=f"Folder not found: {request.folder_path}")

    chunk_size = request.chunk_size or settings.CHUNK_SIZE
    chunk_overlap = request.chunk_overlap or settings.CHUNK_OVERLAP

    files = list(folder.rglob("*"))
    supported = [f for f in files if f.suffix.lower() in (".md", ".txt", ".pdf")]

    if not supported:
        raise HTTPException(status_code=400, detail="No supported files found (.md, .txt, .pdf)")

    all_chunks: list[dict] = []
    docs_processed = 0

    for file_path in supported:
        content = _load_file(file_path)
        if not content or not content.strip():
            continue

        is_markdown = file_path.suffix.lower() in (".md", ".pdf")
        chunks = chunk_documents(
            content=content,
            source_file=file_path.name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            is_markdown=is_markdown,
        )
        all_chunks.extend(chunks)
        docs_processed += 1

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No content extracted from files")

    embedder = get_embedder()
    texts = [c["text"] for c in all_chunks]
    embeddings = embedder.embed_texts(texts)

    vs = get_vectorstore()
    chunk_ids = [c["chunk_id"] for c in all_chunks]
    metadatas = [c["metadata"] for c in all_chunks]
    vs.add_documents(
        ids=chunk_ids,
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    cache = get_cache()
    cache.clear()
    cache.index_chunks(all_chunks)

    return IngestResponse(
        documents_processed=docs_processed,
        chunks_created=len(all_chunks),
        chunk_ids=chunk_ids,
    )
