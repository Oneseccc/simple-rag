# RAG Pipeline Evaluation Report

## Aggregate Scores

| Metric | Mean | Min | Max | N |
|--------|------|-----|-----|---|
| Faithfulness | 0.873 | 0.250 | 1.000 | 12 |
| Answer Relevancy | 0.886 | 0.600 | 1.000 | 12 |
| Context Precision | 0.624 | 0.250 | 1.000 | 10 |
| Context Recall | 1.000 | 1.000 | 1.000 | 10 |
| Answer Correctness | 0.758 | 0.000 | 1.000 | 12 |

## Per-Question Breakdown

| # | Category | Question | Faith. | Relev. | Ctx Prec. | Ctx Recall | Correct. |
|---|----------|----------|--------|--------|-----------|------------|----------|
| 1 | factual | What is the maximum number of tools you can pass i... | 1.000 | 1.000 | 1.000 | 1.000 | 0.800 |
| 2 | factual | What is the context window size for Claude Opus 4.... | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |
| 3 | factual | What is the model ID for Claude Sonnet 4.6? | 1.000 | 1.000 | 0.500 | 1.000 | 0.800 |
| 4 | factual | What is the minimum cacheable prompt prefix length... | 1.000 | 1.000 | N/A | 1.000 | 0.800 |
| 5 | factual | What is the maximum output token limit for Claude ... | 1.000 | 0.667 | 0.500 | 1.000 | 0.800 |
| 6 | factual | How much does the Batch API reduce costs compared ... | 1.000 | 1.000 | 0.750 | 1.000 | 0.800 |
| 7 | factual | What image formats does Claude support? | 1.000 | 1.000 | 1.000 | 1.000 | 0.800 |
| 8 | factual | What is the input token price for Claude Haiku 4.5... | 0.600 | 0.600 | 0.500 | 1.000 | 1.000 |
| 9 | factual | What is the maximum number of images Claude can pr... | 1.000 | 1.000 | N/A | 1.000 | 1.000 |
| 10 | multi-hop | Which Claude models support extended thinking, and... | 1.000 | 0.778 | 0.417 | N/A | 0.600 |
| 11 | multi-hop | If I want to use the cheapest model with prompt ca... | 0.250 | 0.833 | 0.250 | 1.000 | 0.000 |
| 12 | multi-hop | Which model has the largest maximum output and wha... | 0.625 | 0.750 | 0.325 | N/A | N/A |
| 13 | multi-hop | For a RAG system using Claude, what embedding mode... | N/A | N/A | N/A | N/A | N/A |
| 14 | multi-hop | How can I use prompt caching with the batch API to... | N/A | N/A | N/A | N/A | N/A |
| 15 | no-answer | What is Anthropic's annual revenue for 2025? | N/A | N/A | N/A | N/A | N/A |
| 16 | no-answer | How does Claude's RLHF training process work inter... | N/A | N/A | N/A | N/A | N/A |
| 17 | no-answer | What is the exact number of parameters in Claude O... | N/A | N/A | N/A | N/A | 0.800 |
| 18 | no-answer | Can Claude generate images or create visual conten... | N/A | N/A | N/A | N/A | N/A |
| 19 | paraphrased | How many tokens can Opus 4.7 handle as input? | N/A | N/A | N/A | N/A | N/A |
| 20 | paraphrased | What's the cost per million input tokens for the c... | N/A | N/A | N/A | N/A | N/A |
| 21 | paraphrased | How do I install Anthropic's command-line coding t... | N/A | N/A | N/A | N/A | N/A |
| 22 | factual | What is the cache lifetime for prompt caching in C... | N/A | N/A | N/A | N/A | N/A |

## Failure Analysis

### Failure Case 1

**Question**: For a RAG system using Claude, what embedding model dimensions and chunk size are recommended?

**Category**: multi-hop

**Expected**: Recommended embedding models include all-MiniLM-L6-v2 (384 dimensions) and nomic-embed-text (768 dimensions). Recommended chunk size is 256-1024 tokens with 10-20% overlap.

**Got**: I don't have enough information in the provided documents to answer this question. 

The provided context discusses best practices for RAG systems using Claude, including chunk size recommendations [embeddings.md::Embeddings/Best Practices for RAG with Claude::chunk_0] and retrieval strategies [rag-

**Scores**: {
  "faithfulness": null,
  "answer_relevancy": null,
  "context_precision": null,
  "context_recall": null,
  "answer_correctness": null
}

**Analysis**:

This multi-hop question requires synthesizing information from multiple chunks. The retrieval may not have fetched all necessary chunks, or the LLM failed to connect information across the provided contexts. Increasing top_k or implementing a reranking step could help.

---

### Failure Case 2

**Question**: How can I use prompt caching with the batch API to minimize costs for Claude Sonnet?

**Category**: multi-hop

**Expected**: For Claude Sonnet 4.6, use prompt caching with cache_control breakpoints (cache read at $0.30/MTok) combined with the batch API (batch input at $1.50/MTok, batch output at $7.50/MTok) for maximum savings. The minimum cacheable length is 1,024 tokens.

**Got**: To use prompt caching with the batch API and minimize costs for Claude Sonnet, follow these steps:

1. **Enable prompt caching**: Use prompt caching for repeated prefixes to reduce costs. This allows you to cache frequently used context between API calls, reducing latency and costs [prompt-caching.m

**Scores**: {
  "faithfulness": null,
  "answer_relevancy": null,
  "context_precision": null,
  "context_recall": null,
  "answer_correctness": null
}

**Analysis**:

This multi-hop question requires synthesizing information from multiple chunks. The retrieval may not have fetched all necessary chunks, or the LLM failed to connect information across the provided contexts. Increasing top_k or implementing a reranking step could help.

---

### Failure Case 3

**Question**: What is Anthropic's annual revenue for 2025?

**Category**: no-answer

**Expected**: This information is not available in the documentation.

**Got**: I don't have enough information in the provided documents to answer this question. 

The provided context does not mention Anthropic's annual revenue for 2025 or any year. It discusses enterprise features, data privacy and security, getting started with enterprise features, rate limits, and Anthropi

**Scores**: {
  "faithfulness": null,
  "answer_relevancy": null,
  "context_precision": null,
  "context_recall": null,
  "answer_correctness": null
}

**Analysis**:

The pipeline failed to recognize that this question cannot be answered from the corpus. This indicates the LLM is hallucinating rather than admitting lack of knowledge. The system prompt should be strengthened to emphasize when to say 'I don't know'.

---

## Improvement Suggestions

### 1. Add a Reranking Step

Implement a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) between retrieval and generation. Retrieve top-20 chunks from the vector store, then rerank to top-5 using the cross-encoder. This would significantly improve context precision and recall, especially for multi-hop questions where the most relevant chunks may not have the highest vector similarity scores.

### 2. Implement Hybrid Search (Vector + BM25)

Combine vector similarity search with BM25 keyword matching for hybrid retrieval. Vector search excels at semantic similarity but can miss exact keyword matches. BM25 handles exact term matching well. A weighted combination (e.g., 0.7 * vector + 0.3 * BM25) would improve retrieval for questions containing specific technical terms, model names, or exact figures that appear in the documentation.

### 3. Improve Chunking with Semantic Boundaries

The current recursive character splitting can break chunks in the middle of important context. Implementing semantic chunking that respects paragraph and section boundaries would produce more coherent chunks. Additionally, adding chunk overlap summaries (a brief summary of the previous chunk at the start of each new chunk) would help maintain context across chunk boundaries.
