from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from pathlib import Path

CACHE_DB_PATH = Path("/app/data/cache.db")


def _get_key(question: str, top_k: int) -> str:
    raw = f"{question.strip().lower()}:{top_k}"
    return hashlib.sha256(raw.encode()).hexdigest()


class QueryCache:
    def __init__(self, db_path: Path = CACHE_DB_PATH):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path = str(db_path)
        self._local = threading.local()
        self._init_tables()

    def _conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self._db_path)
        return self._local.conn

    def _init_tables(self) -> None:
        conn = self._conn()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, response TEXT)"
        )
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts "
            "USING fts5(chunk_id, text, metadata)"
        )
        conn.commit()

    # --- query cache ---

    def get(self, question: str, top_k: int) -> dict | None:
        key = _get_key(question, top_k)
        row = self._conn().execute(
            "SELECT response FROM cache WHERE key = ?", (key,)
        ).fetchone()
        if row:
            return json.loads(row[0])
        return None

    def put(self, question: str, top_k: int, response: dict) -> None:
        key = _get_key(question, top_k)
        self._conn().execute(
            "INSERT OR REPLACE INTO cache (key, response) VALUES (?, ?)",
            (key, json.dumps(response)),
        )
        self._conn().commit()

    # --- FTS5 keyword index ---

    def index_chunks(self, chunks: list[dict]) -> None:
        conn = self._conn()
        conn.execute("DELETE FROM chunks_fts")
        for chunk in chunks:
            conn.execute(
                "INSERT INTO chunks_fts (chunk_id, text, metadata) VALUES (?, ?, ?)",
                (chunk["chunk_id"], chunk["text"], json.dumps(chunk["metadata"])),
            )
        conn.commit()

    def keyword_search(self, query: str, limit: int = 20) -> list[dict]:
        terms = query.strip().split()
        if not terms:
            return []
        fts_query = " OR ".join(f'"{t}"' for t in terms if t)
        rows = self._conn().execute(
            "SELECT chunk_id, text, metadata, rank FROM chunks_fts "
            "WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?",
            (fts_query, limit),
        ).fetchall()
        return [
            {
                "chunk_id": r[0],
                "text": r[1],
                "metadata": json.loads(r[2]),
                "rank": r[3],
            }
            for r in rows
        ]

    # --- clear both ---

    def clear(self) -> None:
        conn = self._conn()
        conn.execute("DELETE FROM cache")
        conn.execute("DELETE FROM chunks_fts")
        conn.commit()


_cache: QueryCache | None = None


def get_cache() -> QueryCache:
    global _cache
    if _cache is None:
        _cache = QueryCache()
    return _cache
