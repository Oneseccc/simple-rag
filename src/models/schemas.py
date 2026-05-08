from __future__ import annotations

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    folder_path: str = Field(..., description="Path to folder containing documents")
    chunk_size: int | None = Field(None, description="Override default chunk size")
    chunk_overlap: int | None = Field(None, description="Override default chunk overlap")


class IngestResponse(BaseModel):
    documents_processed: int
    chunks_created: int
    chunk_ids: list[str]


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(None, ge=1, le=20)


class Source(BaseModel):
    chunk_id: str
    source_file: str
    section: str
    relevance_score: float
    retrieval_method: str
    text_preview: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    provider: str


class HealthResponse(BaseModel):
    status: str
    chroma_connected: bool
    llm_provider: str
    documents_count: int
    chunks_count: int
