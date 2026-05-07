#!/bin/bash
# Convenience script to ingest all corpus documents via the API
set -e

API_URL="${API_URL:-http://localhost:8080}"

echo "Waiting for API to be ready..."
until curl -sf "$API_URL/health" > /dev/null 2>&1; do
    echo "  API not ready, retrying in 3s..."
    sleep 3
done

echo "API is ready. Ingesting documents..."
curl -s -X POST "$API_URL/ingest" \
    -H "Content-Type: application/json" \
    -d '{"folder_path": "corpus/anthropic"}' | python3 -m json.tool

echo ""
echo "Ingestion complete. Checking health..."
curl -s "$API_URL/health" | python3 -m json.tool
