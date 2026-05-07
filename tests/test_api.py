"""Smoke tests for the API endpoints."""
import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "llm_provider" in data


def test_query_requires_question():
    resp = client.post("/query", json={})
    assert resp.status_code == 422


def test_ingest_requires_folder_path():
    resp = client.post("/ingest", json={})
    assert resp.status_code == 422


def test_ingest_invalid_folder():
    resp = client.post("/ingest", json={"folder_path": "/nonexistent/path"})
    assert resp.status_code == 400
