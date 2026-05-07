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
        self._init_table()

    def _conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self._db_path)
        return self._local.conn

    def _init_table(self) -> None:
        self._conn().execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, response TEXT)"
        )
        self._conn().commit()

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

    def clear(self) -> None:
        self._conn().execute("DELETE FROM cache")
        self._conn().commit()


_cache: QueryCache | None = None


def get_cache() -> QueryCache:
    global _cache
    if _cache is None:
        _cache = QueryCache()
    return _cache
