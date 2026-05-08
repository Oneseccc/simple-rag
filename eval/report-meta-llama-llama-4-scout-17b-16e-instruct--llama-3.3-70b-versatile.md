# RAG Pipeline Evaluation Report

**Generation model**: `meta-llama/llama-4-scout-17b-16e-instruct`

**Judge model**: `llama-3.3-70b-versatile`

## Aggregate Scores

| Metric | Mean | Min | Max | N |
|--------|------|-----|-----|---|
| Faithfulness | 0.928 | 0.500 | 1.000 | 22 |
| Answer Relevancy | 0.881 | 0.286 | 1.000 | 22 |
| Context Precision | 0.745 | 0.000 | 1.000 | 16 |
| Context Recall | 0.810 | 0.000 | 1.000 | 21 |
| Answer Correctness | 0.536 | 0.000 | 1.000 | 22 |

## Per-Question Breakdown

| # | Category | Question | Faith. | Relev. | Ctx Prec. | Ctx Recall | Correct. |
|---|----------|----------|--------|--------|-----------|------------|----------|
| 1 | factual | What is the context window size for Claude Opus 4.... | 0.750 | 1.000 | 1.000 | 1.000 | 0.600 |
| 2 | factual | What is the model ID for Claude Sonnet 4.6? | 1.000 | 1.000 | 0.500 | 1.000 | 0.600 |
| 3 | factual | What is the maximum output token limit for Claude ... | 0.750 | 1.000 | 0.833 | 0.000 | 0.000 |
| 4 | factual | How much does the Batch API reduce costs compared ... | 1.000 | 1.000 | 0.833 | 1.000 | 0.800 |
| 5 | factual | What is the input token price for Claude Haiku 4.5... | 0.500 | 1.000 | 1.000 | 0.000 | 0.000 |
| 6 | factual | What is the context window size for Claude Haiku 4... | 1.000 | 0.571 | 1.000 | 1.000 | 0.800 |
| 7 | factual | What is the cache read pricing multiplier for prom... | 1.000 | 1.000 | N/A | 1.000 | 0.600 |
| 8 | factual | How many additional system prompt tokens does tool... | 1.000 | 1.000 | N/A | 1.000 | 1.000 |
| 9 | factual | Does Anthropic offer its own embedding model? | 0.800 | 1.000 | 1.000 | 1.000 | 0.600 |
| 10 | factual | How much does web search cost when using Claude's ... | 1.000 | 1.000 | 1.000 | 1.000 | 0.600 |
| 11 | multi-hop | Which current Claude models support extended think... | 1.000 | 0.900 | 0.000 | 1.000 | 0.000 |
| 12 | multi-hop | Which model has the largest maximum output and wha... | 1.000 | 1.000 | N/A | 1.000 | 0.600 |
| 13 | multi-hop | What is fast mode pricing for Claude and which mod... | 1.000 | 1.000 | 1.000 | 1.000 | 0.600 |
| 14 | multi-hop | What credit purchase is needed to reach Tier 2 and... | 1.000 | 1.000 | 1.000 | 1.000 | 0.600 |
| 15 | multi-hop | What is the difference between client tools and se... | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |
| 16 | no-answer | What is Anthropic's annual revenue for 2025? | 1.000 | 0.500 | 0.000 | N/A | 0.800 |
| 17 | no-answer | How does Claude's RLHF training process work inter... | 1.000 | 0.286 | N/A | 0.000 | 1.000 |
| 18 | no-answer | What is the exact number of parameters in Claude O... | 1.000 | 0.429 | N/A | 0.000 | 0.600 |
| 19 | no-answer | Can Claude generate images or create visual conten... | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |
| 20 | paraphrased | How many tokens can Opus 4.7 handle as input? | 1.000 | 1.000 | 0.750 | 1.000 | 0.200 |
| 21 | paraphrased | What's the cost per million input tokens for Claud... | 1.000 | 1.000 | N/A | 1.000 | 0.000 |
| 22 | paraphrased | What are the two ways Anthropic offers to build wi... | 0.625 | 0.700 | 0.000 | 1.000 | 0.000 |

## Failure Analysis

### Failure Case 1

**Question**: What are the two ways Anthropic offers to build with Claude?

**Category**: paraphrased

**Expected**: Anthropic offers two ways to build with Claude: the Messages API for direct model prompting with custom agent loops and fine-grained control, and Claude Managed Agents for pre-built configurable agent harnesses that run in managed infrastructure for long-running and asynchronous tasks.

**Got**: Anthropic offers two ways to build with Claude: 

1. Through the Anthropic Console and API, which provide enterprise-grade features for organizations that require advanced security, compliance, and administrative controls [enterprise-features.md::Enterprise Features/Overview::chunk_0].
2. By connect

**Scores**: {
  "faithfulness": 0.625,
  "answer_relevancy": 0.7,
  "context_precision": 0,
  "context_recall": 1.0,
  "answer_correctness": 0.0
}

**Analysis**: The retrieval system returned an enterprise-features chunk instead of the correct source (`intro.md`), which clearly lists the Messages API and Claude Managed Agents as the two building options. Context precision scored 0.0 because none of the top retrieved chunks were relevant to the question. The LLM fabricated an answer from the wrong context, leading to 0.0 correctness and low faithfulness (0.625). This is a retrieval failure — the correct information exists in the corpus but was not surfaced.

---

### Manually Checked Failed Cases

The following cases were not flagged by the automated failure detection (avg score >= 0.5) but were identified through manual review as having significant issues.

#### Case M1 — Q3 (factual): Max output token limit for Claude Sonnet 4.6

**Expected**: 64k tokens | **Got**: 16,384 tokens | **Correctness**: 0.0 | **Context Recall**: 0.0

**Analysis**: The model returned a completely wrong value. The retrieved context included a chunk from `context-windows.md` with a model comparison table, but the chunking split the table in a way that associated Sonnet 4.6 with an incorrect row. The correct value (64k) exists in `models-overview.md` but the relevant row was either not retrieved or lost during chunk splitting.

#### Case M2 — Q5 (factual): Input token price for Claude Haiku 4.5

**Expected**: $1/MTok | **Got**: $0.80/MTok | **Correctness**: 0.0 | **Faithfulness**: 0.5

**Analysis**: The model confused Haiku 4.5 ($1/MTok) with Haiku 3.5 ($0.80/MTok). The retrieved context included a pricing chunk that listed Haiku 3.5's price. Since both models appear in the same pricing table, the chunk splitter separated them into different chunks and the retriever surfaced the wrong one. The low faithfulness (0.5) confirms the model's answer contradicted even its own retrieved context.

#### Case M3 — Q11 (multi-hop): Which models support extended thinking?

**Expected**: Sonnet 4.6 and Haiku 4.5 support extended thinking; Opus 4.7 does NOT (uses adaptive thinking instead) | **Got**: Generic answer about "interleaved thinking" in Claude 4 models | **Correctness**: 0.0 | **Context Precision**: 0.0

**Analysis**: The corpus does not contain a dedicated extended thinking documentation page. The model retrieved tangential context about "interleaved thinking" and cryptographic signatures from `context-windows.md`, which was insufficient to answer the specific question about which models support extended thinking vs. adaptive thinking. This is a corpus coverage gap.

#### Case M4 — Q20 (paraphrased): How many tokens can Opus 4.7 handle as input?

**Expected**: 1M tokens (~555k words, ~2.5M unicode characters) | **Got**: "200K by default, up to 1M with extended context feature" | **Correctness**: 0.2

**Analysis**: The retrieved chunk from `context-windows.md` described the 1M context window as an "extended context" optional feature, which led the LLM to frame it as non-default. According to `models-overview.md`, Opus 4.7 has a 1M token context window as its standard specification. The LLM misinterpreted the context because the chunk presented the information in a misleading way without the full surrounding context.

#### Case M5 — Q21 (paraphrased): Cost per million input tokens for Claude Haiku 3

**Expected**: $0.25/MTok (standard price) | **Got**: $0.125/MTok (Batch API price) | **Correctness**: 0.0

**Analysis**: The model picked up the Batch API discounted price instead of the standard input price. The retrieved context came from the batch processing section of `pricing.md` rather than the standard model pricing table. The retriever failed to distinguish between standard and batch pricing contexts, and the LLM did not flag the distinction.

#### Case M6 — Q16 (no-answer): Anthropic's annual revenue for 2025

**Expected**: Not available | **Got**: Correctly refused | **Correctness**: 0.8 | **Context Precision**: 0.0 | **Answer Relevancy**: 0.5

**Analysis**: The model correctly identified that this information is not in the corpus. However, context precision scored 0.0 because the retriever returned irrelevant pricing and company description chunks. The low answer relevancy (0.5) is due to the verbose refusal including unnecessary details about what the documents do contain.

#### Case M7 — Q17 (no-answer): Claude's RLHF training process

**Expected**: Not available | **Got**: Correctly refused | **Correctness**: 1.0 | **Answer Relevancy**: 0.286 | **Context Recall**: 0.0

**Analysis**: Correct refusal, but the retriever returned completely unrelated chunks (vision capabilities, context-aware parsing). The very low answer relevancy (0.286) suggests the response was overly verbose for a simple "not available" answer. The retrieval system lacks the ability to return empty results when no relevant context exists.

#### Case M8 — Q18 (no-answer): Number of parameters in Claude Opus 4.7

**Expected**: Not available | **Got**: Correctly refused | **Correctness**: 0.6 | **Answer Relevancy**: 0.429 | **Context Recall**: 0.0

**Analysis**: Similar pattern to M6 and M7. The model correctly refused but retrieved irrelevant chunks about Opus 4.7's capabilities (image support, model overview). Low answer relevancy indicates the refusal was unnecessarily verbose. The retriever has no confidence threshold to avoid returning low-relevance results.

---

## Improvement Suggestions

### 1. Table-Aware Chunking

**Problem**: Questions Q3, Q5, and Q21 all failed because pricing and specification tables were split across chunks, causing the LLM to read the wrong model's data.

**Suggestion**: Increase `chunk_size` for table-heavy documents (e.g., `pricing.md`, `models-overview.md`) or implement table-aware chunking that keeps entire tables within a single chunk. Alternatively, add metadata tagging so each chunk knows which model's data it contains.

### 2. Corpus Coverage Gaps

**Problem**: Q11 (extended thinking) failed because the corpus lacks a dedicated page on this topic. The `models-overview.md` file mentions extended thinking in the comparison table but does not explain the distinction between extended thinking and adaptive thinking.

**Suggestion**: Add the extended thinking documentation page to the corpus, or enrich the existing `models-overview.md` chunks with additional metadata about feature support per model.

### 3. Retrieval Precision and Confidence Thresholds

**Problem**: No-answer questions (Q16, Q17, Q18) correctly refused to answer but still retrieved irrelevant context with 0.0 precision. Q22 retrieved enterprise-features instead of intro.md content.

**Suggestion**: Implement a relevance score threshold on retrieved chunks so that low-confidence results are filtered out before being passed to the LLM. This would reduce noise for unanswerable questions and improve precision for answerable ones. Tuning the reranker or adding keyword-boosted hybrid search could also help.

### 4. System Prompt Guidance for Ambiguous Context

**Problem**: Q20 (context window) and Q21 (pricing) failed because the LLM misinterpreted context — treating extended context as optional and batch pricing as standard.

**Suggestion**: Update the RAG system prompt to instruct the model to prefer standard/default values over special-case pricing (batch, fast mode) unless the user specifically asks about those variants. Adding an instruction like "When multiple values are found for the same metric, prefer the standard or default value" could reduce these errors.
