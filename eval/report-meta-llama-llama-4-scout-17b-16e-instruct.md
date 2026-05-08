# RAG Pipeline Evaluation Report

**Generation model**: `meta-llama/llama-4-scout-17b-16e-instruct`

**Judge model**: `meta-llama/llama-4-scout-17b-16e-instruct`

## Aggregate Scores

| Metric | Mean | Min | Max | N |
|--------|------|-----|-----|---|
| Faithfulness | 0.797 | 0.000 | 1.000 | 22 |
| Answer Relevancy | 0.748 | 0.286 | 1.000 | 19 |
| Context Precision | 0.594 | 0.000 | 1.000 | 22 |
| Context Recall | 0.846 | 0.000 | 1.000 | 13 |
| Answer Correctness | 0.582 | 0.000 | 1.000 | 22 |

## Per-Question Breakdown

| # | Category | Question | Faith. | Relev. | Ctx Prec. | Ctx Recall | Correct. |
|---|----------|----------|--------|--------|-----------|------------|----------|
| 1 | factual | What is the context window size for Claude Opus 4.... | 1.000 | 0.800 | 1.000 | 1.000 | 0.400 |
| 2 | factual | What is the model ID for Claude Sonnet 4.6? | 1.000 | 0.714 | 0.250 | 1.000 | 0.600 |
| 3 | factual | What is the maximum output token limit for Claude ... | 0.750 | 0.750 | 0.000 | N/A | 0.000 |
| 4 | factual | How much does the Batch API reduce costs compared ... | 1.000 | 0.500 | 0.833 | 1.000 | 0.600 |
| 5 | factual | What is the input token price for Claude Haiku 4.5... | 0.000 | 1.000 | 1.000 | N/A | 0.200 |
| 6 | factual | What is the context window size for Claude Haiku 4... | 1.000 | 0.500 | 1.000 | N/A | 1.000 |
| 7 | factual | What is the cache read pricing multiplier for prom... | 1.000 | N/A | 0.333 | 1.000 | 0.500 |
| 8 | factual | How many additional system prompt tokens does tool... | 0.200 | 0.600 | 1.000 | 1.000 | 1.000 |
| 9 | factual | Does Anthropic offer its own embedding model? | 0.833 | 1.000 | 1.000 | 1.000 | 0.600 |
| 10 | factual | How much does web search cost when using Claude's ... | 1.000 | 1.000 | 1.000 | 0.500 | 0.400 |
| 11 | multi-hop | Which current Claude models support extended think... | 0.833 | 0.571 | 0.000 | 1.000 | 0.200 |
| 12 | multi-hop | Which model has the largest maximum output and wha... | 0.750 | N/A | 1.000 | 1.000 | 0.600 |
| 13 | multi-hop | What is fast mode pricing for Claude and which mod... | 0.667 | 0.857 | 1.000 | 0.500 | 0.800 |
| 14 | multi-hop | What credit purchase is needed to reach Tier 2 and... | 1.000 | 1.000 | 0.700 | N/A | 0.600 |
| 15 | multi-hop | What is the difference between client tools and se... | 1.000 | N/A | 1.000 | 1.000 | 0.900 |
| 16 | no-answer | What is Anthropic's annual revenue for 2025? | 1.000 | 0.500 | 0.000 | 0.000 | 1.000 |
| 17 | no-answer | How does Claude's RLHF training process work inter... | 0.833 | 0.286 | 0.000 | N/A | 1.000 |
| 18 | no-answer | What is the exact number of parameters in Claude O... | 0.400 | 0.400 | 0.000 | N/A | 1.000 |
| 19 | no-answer | Can Claude generate images or create visual conten... | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 20 | paraphrased | How many tokens can Opus 4.7 handle as input? | 0.667 | 1.000 | 0.750 | N/A | 0.400 |
| 21 | paraphrased | What's the cost per million input tokens for Claud... | 1.000 | 1.000 | 0.200 | N/A | 0.000 |
| 22 | paraphrased | What are the two ways Anthropic offers to build wi... | 0.600 | 0.727 | 0.000 | N/A | 0.000 |

## Failure Analysis

### Failure Case 1

**Question**: What are the two ways Anthropic offers to build with Claude?

**Category**: paraphrased

**Expected**: Anthropic offers two ways to build with Claude: the Messages API for direct model prompting with custom agent loops and fine-grained control, and Claude Managed Agents for pre-built configurable agent harnesses that run in managed infrastructure for long-running and asynchronous tasks.

**Got**: Anthropic offers two ways to build with Claude: 

1. Through the Anthropic Console and API, which provide enterprise-grade features for organizations that require advanced security, compliance, and administrative controls [enterprise-features.md::Enterprise Features/Overview::chunk_0].
2. By connect

**Scores**: {
  "faithfulness": 0.6,
  "answer_relevancy": 0.7272727272727273,
  "context_precision": 0,
  "context_recall": null,
  "answer_correctness": 0.0
}

**Analysis**: The retrieval system returned an enterprise-features chunk and a tool-use chunk instead of the correct source (`intro.md`), which clearly lists the Messages API and Claude Managed Agents as the two building options. Context precision scored 0.0 because none of the top retrieved chunks were relevant. The LLM fabricated an answer from the wrong context, leading to 0.0 correctness and low faithfulness (0.6). This is a retrieval failure — the correct information exists in the corpus but was not surfaced.

---

### Failure Case 2

**Question**: What is the maximum output token limit for Claude Sonnet 4.6?

**Category**: factual

**Expected**: The maximum output for Claude Sonnet 4.6 is 64k tokens.

**Got**: The maximum output token limit for Claude Sonnet 4.6 is 16,384 tokens. This information is consistent across multiple sources: [chunk_0] in models-overview.md and [chunk_0] in context-window.md. However, note that when using the Message Batches API with a specific beta header, Claude Sonnet 4.6 supp

**Scores**: {
  "faithfulness": 0.75,
  "answer_relevancy": 0.75,
  "context_precision": 0,
  "context_recall": null,
  "answer_correctness": 0.0
}

**Analysis**: The model returned 16,384 tokens instead of the correct 64k tokens. The retrieved chunks included a Sonnet 4.6 description and a context window table, but the chunking split the specification table in a way that associated Sonnet 4.6 with an incorrect max output value. Context precision scored 0.0 because the retrieved chunks did not contain the correct answer. The correct value exists in `models-overview.md` but the relevant table row was lost during chunk splitting.

---

### Failure Case 3

**Question**: What is the exact number of parameters in Claude Opus 4.7?

**Category**: no-answer

**Expected**: This information is not available in the documentation. Anthropic does not publicly disclose model parameter counts.

**Got**: I don't have enough information in the provided documents to answer this question. 

The provided context discusses various aspects of Claude Opus 4.7, such as its capabilities [models-overview.md::Claude Models Overview/Latest Models/Claude Opus 4.7::chunk_0], high-resolution image support [vision.

**Scores**: {
  "faithfulness": 0.4,
  "answer_relevancy": 0.4,
  "context_precision": 0,
  "context_recall": null,
  "answer_correctness": 1.0
}

**Analysis**: The model correctly refused to answer (correctness 1.0), but the Scout judge scored faithfulness very low (0.4) and relevancy low (0.4) despite the correct refusal. The retriever returned irrelevant chunks about Opus 4.7 capabilities and image support. The low faithfulness score appears to be a judge model limitation — the smaller Scout model penalizes verbose refusals more harshly than the 70B judge (which scored the same answer at faithfulness 1.0 and relevancy 0.429). This highlights that the Scout model is less reliable as an evaluation judge for no-answer cases.

---

### Manually Checked Failed Cases

The following cases were not flagged by the automated failure detection (avg score >= 0.5) but were identified through manual review as having significant issues.

#### Case M1 — Q1 (factual): Context window size for Claude Opus 4.7

**Expected**: 1M tokens (~555k words, ~2.5M unicode characters) | **Got**: "200K tokens, extendable to 1M" | **Correctness**: 0.4

**Analysis**: The model framed the 1M context window as an extension of a 200K default rather than the standard specification. The retrieved chunk from `context-windows.md` described "Extended Context (Opus 4.7)" which led the LLM to treat 1M as an optional feature. According to `models-overview.md`, Opus 4.7's context window is simply 1M tokens. This is the same chunking and context framing issue seen in Q20.

#### Case M2 — Q5 (factual): Input token price for Claude Haiku 4.5

**Expected**: $1/MTok | **Got**: $0.80/MTok | **Faithfulness**: 0.0 | **Correctness**: 0.2

**Analysis**: The model confused Haiku 4.5 ($1/MTok) with Haiku 3.5 ($0.80/MTok). The top retrieved chunk was from `pricing.md` with a header path pointing to "Claude Haiku 4.5" but containing the $0.80 price from Haiku 3.5. The chunking split the pricing table incorrectly, placing the wrong price under the wrong model header. Notably, the Scout judge scored faithfulness at 0.0 (vs 0.5 with the 70B judge), being harsher on the contradictory answer since the model even acknowledged seeing the correct $1/MTok in `models-overview.md` but still chose the wrong value.

#### Case M3 — Q8 (factual): Tool use system prompt tokens for Opus 4.7

**Expected**: 346 tokens (auto/none), 313 tokens (any/tool) | **Got**: 346 tokens (correct) | **Correctness**: 1.0 | **Faithfulness**: 0.2

**Analysis**: The answer is factually correct (correctness 1.0), yet the Scout judge scored faithfulness at only 0.2. The 70B judge scored this same answer at faithfulness 1.0. This is a clear judge model limitation — the Scout model appears to penalize answers that cite multiple sources or include additional context, even when the core answer is correct and supported by the retrieved chunks. This artificially deflates the faithfulness metric.

#### Case M4 — Q10 (factual): Web search cost on Claude's API

**Expected**: $10 per 1,000 searches, plus standard token costs | **Got**: Correctly stated $10/1,000 searches | **Correctness**: 0.4 | **Context Recall**: 0.5

**Analysis**: The model provided the correct price but the Scout judge scored correctness at only 0.4 (vs 0.6 with 70B judge). The low context recall (0.5) suggests the retrieved chunks did not fully cover the expected answer's detail about "each web search counts as one use, regardless of the number of results." The Scout judge is stricter on partial answers even when the core fact is correct.

#### Case M5 — Q11 (multi-hop): Which models support extended thinking?

**Expected**: Sonnet 4.6 and Haiku 4.5 support extended thinking; Opus 4.7 does NOT (uses adaptive thinking) | **Got**: Generic answer about "interleaved thinking" in Claude 4 models | **Correctness**: 0.2 | **Context Precision**: 0.0

**Analysis**: The corpus lacks a dedicated extended thinking documentation page. The retriever returned tangential context about "interleaved thinking" and cryptographic signatures from `context-windows.md`, which was insufficient to answer which specific models support extended thinking vs. adaptive thinking. This is the same corpus coverage gap identified in the 70B judge run.

#### Case M6 — Q16 (no-answer): Anthropic's annual revenue for 2025

**Expected**: Not available | **Got**: Correctly refused | **Correctness**: 1.0 | **Context Precision**: 0.0 | **Context Recall**: 0.0

**Analysis**: Correct refusal, but the retriever returned irrelevant pricing and company description chunks. Context precision and recall both scored 0.0. The retrieval system lacks a confidence threshold to filter out low-relevance results when no matching information exists in the corpus.

#### Case M7 — Q17 (no-answer): Claude's RLHF training process

**Expected**: Not available | **Got**: Correctly refused | **Correctness**: 1.0 | **Answer Relevancy**: 0.286 | **Context Precision**: 0.0

**Analysis**: Correct refusal, but the retriever returned completely unrelated chunks (vision capabilities, context-aware parsing, developer quickstart). Very low answer relevancy (0.286) indicates the verbose refusal format is penalized by the judge. The retrieval system has no mechanism to return empty results when no relevant context exists.

#### Case M8 — Q20 (paraphrased): How many tokens can Opus 4.7 handle as input?

**Expected**: 1M tokens (~555k words, ~2.5M unicode characters) | **Got**: "200K by default, up to 1M with extended context" | **Faithfulness**: 0.667 | **Correctness**: 0.4

**Analysis**: Identical root cause to Case M1 (Q1). The "Extended Context (Opus 4.7)" chunk framing led the LLM to present the 1M context window as a non-default feature. The model concluded "Opus 4.7 can handle up to 200K tokens as input" which is factually wrong. Low faithfulness (0.667) reflects the contradiction between the retrieved context (which says 1M) and the model's final answer (which says 200K default).

#### Case M9 — Q21 (paraphrased): Cost per million input tokens for Claude Haiku 3

**Expected**: $0.25/MTok (standard price) | **Got**: $0.125/MTok (Batch API price) | **Correctness**: 0.0 | **Context Precision**: 0.2

**Analysis**: The model picked up the Batch API discounted price instead of the standard input price. The top retrieved chunks came from vision pricing and worked examples rather than the standard model pricing table. Context precision was very low (0.2) confirming poor retrieval. The LLM did not distinguish between batch and standard pricing when multiple values were present.

---

## Improvement Suggestions

### 1. Table-Aware Chunking

**Problem**: Questions Q3, Q5, and Q21 all failed because pricing and specification tables were split across chunks, causing the LLM to read the wrong model's data or confuse standard vs. batch pricing.

**Suggestion**: Increase `chunk_size` for table-heavy documents (e.g., `pricing.md`, `models-overview.md`) or implement table-aware chunking that keeps entire tables within a single chunk. Alternatively, add metadata tagging so each chunk knows which model's data it contains.

### 2. Corpus Coverage Gaps

**Problem**: Q11 (extended thinking) failed because the corpus lacks a dedicated page explaining the distinction between extended thinking and adaptive thinking. The `models-overview.md` comparison table mentions these features but does not provide sufficient detail.

**Suggestion**: Add the extended thinking documentation page to the corpus, or enrich the existing model overview chunks with explicit feature support details per model.

### 3. Context Window Chunk Framing

**Problem**: Q1 and Q20 both failed because the `context-windows.md` chunk titled "Extended Context (Opus 4.7)" framed the 1M context window as an optional extension of a 200K default, misleading the LLM into presenting incorrect information.

**Suggestion**: Restructure the context window chunks so that each model's standard context window size is presented as the primary fact, with extended context details as supplementary information. Alternatively, ensure the `models-overview.md` chunk containing the correct 1M specification is ranked higher by the retriever.

### 4. Retrieval Precision and Confidence Thresholds

**Problem**: No-answer questions (Q16, Q17, Q18) correctly refused to answer but retrieved completely irrelevant context with 0.0 precision. Q22 retrieved enterprise-features instead of intro.md content.

**Suggestion**: Implement a relevance score threshold on retrieved chunks so that low-confidence results are filtered out before being passed to the LLM. This would reduce noise for unanswerable questions and improve precision for answerable ones. Tuning the reranker or adding keyword-boosted hybrid search could also help.

### 5. System Prompt Guidance for Ambiguous Context

**Problem**: Q5 and Q21 failed because the LLM chose the wrong value when multiple prices existed in context (batch vs. standard, Haiku 3.5 vs. Haiku 4.5).

**Suggestion**: Update the RAG system prompt to instruct the model to prefer standard/default values over special-case pricing (batch, fast mode) unless the user specifically asks about those variants. Adding an instruction like "When multiple values are found for the same metric, prefer the standard or default value" could reduce these errors.

### 6. Judge Model Reliability

**Problem**: The Scout 17B model as evaluation judge produced noticeably harsher and sometimes inconsistent scores compared to the 70B judge. Q8 received faithfulness 0.2 despite being factually correct (1.0 correctness). No-answer questions received lower faithfulness scores for correct refusals. Multiple questions had N/A context recall values where the 70B judge produced scores.

**Suggestion**: Use a larger, more capable model as the evaluation judge (e.g., `llama-3.3-70b-versatile`) for more reliable metric scores. The Scout model is suitable as the generation model but its smaller size leads to less consistent evaluation judgments, particularly for nuanced cases like verbose refusals and multi-source citations.
