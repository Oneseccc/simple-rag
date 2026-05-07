# Embeddings

## Overview

While Anthropic does not provide a dedicated embeddings API, Claude can be used in conjunction with embedding models for RAG (Retrieval-Augmented Generation) and semantic search workflows.

## Recommended Embedding Models

For use with Claude-based RAG systems:

### Local Models (via Ollama or sentence-transformers)
- **all-MiniLM-L6-v2**: 384 dimensions, fast, good general-purpose quality
- **nomic-embed-text**: 768 dimensions, strong performance on benchmarks
- **bge-small-en-v1.5**: 384 dimensions, optimized for retrieval tasks

### API-based Models
- **Voyage AI**: Recommended by Anthropic for best quality embeddings
- **OpenAI text-embedding-3-small**: 1536 dimensions, widely used

## Best Practices for RAG with Claude

1. **Chunk Size**: Use 256-1024 tokens per chunk depending on content type
2. **Overlap**: 10-20% overlap between chunks preserves context
3. **Metadata**: Store source information with embeddings for citations
4. **Top-K**: Retrieve 3-10 chunks depending on context window budget
5. **Prompt Design**: Clearly delineate retrieved context from the user question