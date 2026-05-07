# RAG Pipeline Evaluation Report

## Aggregate Scores

| Metric | Mean | Min | Max | N |
|--------|------|-----|-----|---|
| Faithfulness | 0.909 | 0.500 | 1.000 | 22 |
| Answer Relevancy | 0.812 | 0.375 | 1.000 | 19 |
| Context Precision | 0.733 | 0.000 | 1.000 | 22 |
| Context Recall | 0.900 | 0.500 | 1.000 | 10 |
| Answer Correctness | 0.795 | 0.000 | 1.000 | 22 |

## Per-Question Breakdown

| # | Category | Question | Faith. | Relev. | Ctx Prec. | Ctx Recall | Correct. |
|---|----------|----------|--------|--------|-----------|------------|----------|
| 1 | factual | What is the maximum number of tools you can pass i... | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |
| 2 | factual | What is the context window size for Claude Opus 4.... | 1.000 | 1.000 | 1.000 | N/A | 1.000 |
| 3 | factual | What is the model ID for Claude Sonnet 4.6? | 1.000 | 1.000 | 0.917 | N/A | 1.000 |
| 4 | factual | What is the minimum cacheable prompt prefix length... | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |
| 5 | factual | What is the maximum output token limit for Claude ... | 1.000 | 1.000 | 0.833 | N/A | 1.000 |
| 6 | factual | How much does the Batch API reduce costs compared ... | 0.500 | 1.000 | 0.750 | N/A | 1.000 |
| 7 | factual | What image formats does Claude support? | 1.000 | 1.000 | 1.000 | N/A | 1.000 |
| 8 | factual | What is the input token price for Claude Haiku 4.5... | 1.000 | N/A | 1.000 | 1.000 | 1.000 |
| 9 | factual | What is the maximum number of images Claude can pr... | 1.000 | 1.000 | 1.000 | N/A | 1.000 |
| 10 | multi-hop | Which Claude models support extended thinking, and... | 1.000 | 0.538 | 1.000 | 1.000 | 0.400 |
| 11 | multi-hop | If I want to use the cheapest model with prompt ca... | 1.000 | 0.375 | 0.250 | N/A | 0.000 |
| 12 | multi-hop | Which model has the largest maximum output and wha... | 1.000 | 0.714 | 0.750 | N/A | 0.900 |
| 13 | multi-hop | For a RAG system using Claude, what embedding mode... | 1.000 | 0.667 | 1.000 | 1.000 | 0.000 |
| 14 | multi-hop | How can I use prompt caching with the batch API to... | 0.875 | 0.600 | 1.000 | N/A | 0.400 |
| 15 | no-answer | What is Anthropic's annual revenue for 2025? | 0.833 | 0.500 | 0.000 | N/A | 1.000 |
| 16 | no-answer | How does Claude's RLHF training process work inter... | 1.000 | 0.714 | 1.000 | 1.000 | 1.000 |
| 17 | no-answer | What is the exact number of parameters in Claude O... | 0.667 | 0.750 | 0.200 | 0.500 | 0.900 |
| 18 | no-answer | Can Claude generate images or create visual conten... | 1.000 | 0.857 | 0.000 | 0.500 | 1.000 |
| 19 | paraphrased | How many tokens can Opus 4.7 handle as input? | 0.875 | 0.857 | 0.917 | N/A | 0.800 |
| 20 | paraphrased | What's the cost per million input tokens for the c... | 0.500 | N/A | 0.000 | N/A | 0.900 |
| 21 | paraphrased | How do I install Anthropic's command-line coding t... | 0.750 | 0.857 | 0.500 | 1.000 | 0.600 |
| 22 | factual | What is the cache lifetime for prompt caching in C... | 1.000 | N/A | 1.000 | 1.000 | 0.800 |

## Failure Analysis

### Failure Case 1

**Question**: If I want to use the cheapest model with prompt caching, what is the cache read price and what is the minimum cacheable length?

**Category**: multi-hop

**Expected**: The cheapest model is Claude Haiku 4.5 with a cache read price of $0.08/MTok and a minimum cacheable length of 2,048 tokens.

**Got**: I don't have enough information in the provided documents to answer this question. 

The provided context mentions the benefits of prompt caching, cache lifetime, minimum cacheable length for different models, and how prompt caching works, but it does not provide information on the cache read price 

**Scores**: {
  "faithfulness": 1.0,
  "answer_relevancy": 0.375,
  "context_precision": 0.25,
  "context_recall": null,
  "answer_correctness": 0.0
}

**Analysis**:

This multi-hop question requires synthesizing information from multiple chunks. The retrieval may not have fetched all necessary chunks, or the LLM failed to connect information across the provided contexts. Increasing top_k or implementing a reranking step could help.

---

### Failure Case 2

**Question**: What's the cost per million input tokens for the cheapest Claude model?

**Category**: paraphrased

**Expected**: The cheapest Claude model is Haiku 4.5 at $0.80 per million input tokens.

**Got**: To determine the cost per million input tokens for the cheapest Claude model, we first need to identify the cheapest model and then find its input token pricing.

The cheapest model is likely to be Claude Haiku 4.5, as it is described as "the fastest and most cost-effective model" [models-overview.m

**Scores**: {
  "faithfulness": 0.5,
  "answer_relevancy": null,
  "context_precision": 0,
  "context_recall": null,
  "answer_correctness": 0.9
}

**Analysis**:

The retrieved context may not have been sufficiently relevant, or the LLM did not correctly extract the answer from the available context. This could be improved with better chunking strategy or a reranking step.

---

## Improvement Suggestions

### 1. Add a Reranking Step

Implement a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) between retrieval and generation. Retrieve top-20 chunks from the vector store, then rerank to top-5 using the cross-encoder. This would significantly improve context precision and recall, especially for multi-hop questions where the most relevant chunks may not have the highest vector similarity scores.

### 2. Implement Hybrid Search (Vector + BM25)

Combine vector similarity search with BM25 keyword matching for hybrid retrieval. Vector search excels at semantic similarity but can miss exact keyword matches. BM25 handles exact term matching well. A weighted combination (e.g., 0.7 * vector + 0.3 * BM25) would improve retrieval for questions containing specific technical terms, model names, or exact figures that appear in the documentation.

### 3. Improve Chunking with Semantic Boundaries

The current recursive character splitting can break chunks in the middle of important context. Implementing semantic chunking that respects paragraph and section boundaries would produce more coherent chunks. Additionally, adding chunk overlap summaries (a brief summary of the previous chunk at the start of each new chunk) would help maintain context across chunk boundaries.
