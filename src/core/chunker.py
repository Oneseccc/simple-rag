from __future__ import annotations

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


HEADERS_TO_SPLIT_ON = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


def chunk_documents(
    content: str,
    source_file: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    is_markdown: bool = True,
) -> list[dict]:
    if is_markdown:
        return _chunk_markdown(content, source_file, chunk_size, chunk_overlap)
    return _chunk_plain_text(content, source_file, chunk_size, chunk_overlap)


def _chunk_markdown(
    content: str,
    source_file: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict]:
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    md_sections = md_splitter.split_text(content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = []
    for section in md_sections:
        section_meta = section.metadata
        header_path = "/".join(
            section_meta.get(h, "")
            for h in ("h1", "h2", "h3")
            if section_meta.get(h)
        )

        sub_chunks = text_splitter.split_text(section.page_content)
        for idx, text in enumerate(sub_chunks):
            chunk_id = f"{source_file}::{header_path}::chunk_{idx}" if header_path else f"{source_file}::chunk_{idx}"
            chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "metadata": {
                    "source_file": source_file,
                    "h1": section_meta.get("h1", ""),
                    "h2": section_meta.get("h2", ""),
                    "h3": section_meta.get("h3", ""),
                    "header_path": header_path,
                    "chunk_index": idx,
                    "char_count": len(text),
                },
            })

    if not chunks:
        return _chunk_plain_text(content, source_file, chunk_size, chunk_overlap)

    return chunks


def _chunk_plain_text(
    content: str,
    source_file: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    sub_chunks = text_splitter.split_text(content)

    return [
        {
            "chunk_id": f"{source_file}::chunk_{idx}",
            "text": text,
            "metadata": {
                "source_file": source_file,
                "h1": "",
                "h2": "",
                "h3": "",
                "header_path": "",
                "chunk_index": idx,
                "char_count": len(text),
            },
        }
        for idx, text in enumerate(sub_chunks)
    ]
