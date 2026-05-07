"""Tests for the chunking pipeline."""
from src.core.chunker import chunk_documents


def test_markdown_chunking():
    content = """# Main Title

## Section One

This is the first section with some content about the API.
It has multiple sentences that should be kept together when possible.

## Section Two

This is the second section with different content about models.
It also has multiple sentences.
"""
    chunks = chunk_documents(
        content=content,
        source_file="test.md",
        chunk_size=200,
        chunk_overlap=20,
        is_markdown=True,
    )
    assert len(chunks) > 0
    assert all("chunk_id" in c for c in chunks)
    assert all("text" in c for c in chunks)
    assert all("metadata" in c for c in chunks)
    assert all(c["metadata"]["source_file"] == "test.md" for c in chunks)


def test_plain_text_chunking():
    content = "This is a test. " * 100
    chunks = chunk_documents(
        content=content,
        source_file="test.txt",
        chunk_size=100,
        chunk_overlap=10,
        is_markdown=False,
    )
    assert len(chunks) > 1
    assert all(c["metadata"]["source_file"] == "test.txt" for c in chunks)


def test_chunk_id_format():
    content = """# Title

## Subtitle

Some content here.
"""
    chunks = chunk_documents(
        content=content,
        source_file="doc.md",
        chunk_size=512,
        chunk_overlap=50,
        is_markdown=True,
    )
    for chunk in chunks:
        assert "::" in chunk["chunk_id"]
        assert chunk["chunk_id"].startswith("doc.md::")


def test_empty_content():
    chunks = chunk_documents(
        content="",
        source_file="empty.md",
        chunk_size=512,
        chunk_overlap=50,
        is_markdown=True,
    )
    assert chunks == []


def test_configurable_chunk_size():
    content = "Word " * 500
    small = chunk_documents(content, "test.txt", chunk_size=100, chunk_overlap=10, is_markdown=False)
    large = chunk_documents(content, "test.txt", chunk_size=1000, chunk_overlap=50, is_markdown=False)
    assert len(small) > len(large)
