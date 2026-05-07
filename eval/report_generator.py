"""Generate evaluation report from DeepEval results."""
from __future__ import annotations

import json
from pathlib import Path

RESULTS_PATH = Path(__file__).parent / "results" / "eval_results.json"
REPORT_PATH = Path(__file__).parent / "report.md"

METRIC_NAMES = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
    "answer_correctness",
]


def load_results() -> list[dict]:
    return json.loads(RESULTS_PATH.read_text())


def compute_aggregates(results: list[dict]) -> dict[str, dict]:
    aggregates = {}
    for metric in METRIC_NAMES:
        scores = [
            r["scores"].get(metric)
            for r in results
            if isinstance(r["scores"], dict) and r["scores"].get(metric) is not None
        ]
        if scores:
            aggregates[metric] = {
                "mean": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores),
                "count": len(scores),
            }
        else:
            aggregates[metric] = {"mean": 0, "min": 0, "max": 0, "count": 0}
    return aggregates


def find_failures(results: list[dict]) -> list[dict]:
    failures = []
    for r in results:
        if not isinstance(r["scores"], dict) or "error" in r["scores"]:
            failures.append(r)
            continue
        avg_score = 0
        count = 0
        for m in METRIC_NAMES:
            s = r["scores"].get(m)
            if s is not None:
                avg_score += s
                count += 1
        if count > 0:
            avg_score /= count
        if avg_score < 0.5:
            r["avg_score"] = avg_score
            failures.append(r)
    failures.sort(key=lambda x: x.get("avg_score", 0))
    return failures


def generate_report(results: list[dict]) -> str:
    aggregates = compute_aggregates(results)
    failures = find_failures(results)

    lines = []
    lines.append("# RAG Pipeline Evaluation Report\n")
    lines.append("## Aggregate Scores\n")
    lines.append("| Metric | Mean | Min | Max | N |")
    lines.append("|--------|------|-----|-----|---|")
    for metric, stats in aggregates.items():
        lines.append(
            f"| {metric.replace('_', ' ').title()} "
            f"| {stats['mean']:.3f} | {stats['min']:.3f} | {stats['max']:.3f} | {stats['count']} |"
        )

    lines.append("\n## Per-Question Breakdown\n")
    lines.append("| # | Category | Question | Faith. | Relev. | Ctx Prec. | Ctx Recall | Correct. |")
    lines.append("|---|----------|----------|--------|--------|-----------|------------|----------|")
    def _fmt(v):
        return f"{v:.3f}" if isinstance(v, (int, float)) else "N/A"

    for i, r in enumerate(results):
        q = r["question"][:50] + "..." if len(r["question"]) > 50 else r["question"]
        scores = r.get("scores", {})
        if isinstance(scores, dict) and "error" not in scores:
            row = (
                f"| {i+1} | {r.get('category', 'N/A')} | {q} "
                f"| {_fmt(scores.get('faithfulness'))} "
                f"| {_fmt(scores.get('answer_relevancy'))} "
                f"| {_fmt(scores.get('context_precision'))} "
                f"| {_fmt(scores.get('context_recall'))} "
                f"| {_fmt(scores.get('answer_correctness'))} |"
            )
        else:
            row = f"| {i+1} | {r.get('category', 'N/A')} | {q} | ERROR | ERROR | ERROR | ERROR | ERROR |"
        lines.append(row)

    lines.append("\n## Failure Analysis\n")
    top_failures = failures[:5]
    if not top_failures:
        lines.append("No significant failures detected.\n")
    else:
        for idx, f in enumerate(top_failures[:3], 1):
            lines.append(f"### Failure Case {idx}\n")
            lines.append(f"**Question**: {f['question']}\n")
            lines.append(f"**Category**: {f.get('category', 'N/A')}\n")
            lines.append(f"**Expected**: {f['ground_truth_answer']}\n")
            lines.append(f"**Got**: {f.get('actual_answer', 'N/A')[:300]}\n")
            scores = f.get("scores", {})
            if isinstance(scores, dict) and "error" not in scores:
                lines.append(f"**Scores**: {json.dumps(scores, indent=2)}\n")

            lines.append("**Analysis**:\n")
            category = f.get("category", "")
            if category == "no-answer":
                lines.append(
                    "The pipeline failed to recognize that this question cannot be answered from the corpus. "
                    "This indicates the LLM is hallucinating rather than admitting lack of knowledge. "
                    "The system prompt should be strengthened to emphasize when to say 'I don't know'.\n"
                )
            elif category == "multi-hop":
                lines.append(
                    "This multi-hop question requires synthesizing information from multiple chunks. "
                    "The retrieval may not have fetched all necessary chunks, or the LLM failed to "
                    "connect information across the provided contexts. Increasing top_k or implementing "
                    "a reranking step could help.\n"
                )
            else:
                lines.append(
                    "The retrieved context may not have been sufficiently relevant, or the LLM "
                    "did not correctly extract the answer from the available context. This could be "
                    "improved with better chunking strategy or a reranking step.\n"
                )
            lines.append("---\n")

    lines.append("## Improvement Suggestions\n")
    lines.append("### 1. Add a Reranking Step\n")
    lines.append(
        "Implement a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) between "
        "retrieval and generation. Retrieve top-20 chunks from the vector store, then rerank to top-5 "
        "using the cross-encoder. This would significantly improve context precision and recall, "
        "especially for multi-hop questions where the most relevant chunks may not have the highest "
        "vector similarity scores.\n"
    )
    lines.append("### 2. Implement Hybrid Search (Vector + BM25)\n")
    lines.append(
        "Combine vector similarity search with BM25 keyword matching for hybrid retrieval. "
        "Vector search excels at semantic similarity but can miss exact keyword matches. "
        "BM25 handles exact term matching well. A weighted combination (e.g., 0.7 * vector + 0.3 * BM25) "
        "would improve retrieval for questions containing specific technical terms, model names, or "
        "exact figures that appear in the documentation.\n"
    )
    lines.append("### 3. Improve Chunking with Semantic Boundaries\n")
    lines.append(
        "The current recursive character splitting can break chunks in the middle of important context. "
        "Implementing semantic chunking that respects paragraph and section boundaries would produce "
        "more coherent chunks. Additionally, adding chunk overlap summaries (a brief summary of the "
        "previous chunk at the start of each new chunk) would help maintain context across chunk boundaries.\n"
    )

    return "\n".join(lines)


def main():
    if not RESULTS_PATH.exists():
        print("No results found. Run eval/run_eval.py first.")
        return

    print("Loading results...")
    results = load_results()
    print(f"  {len(results)} results loaded")

    print("Generating report...")
    report = generate_report(results)
    REPORT_PATH.write_text(report)
    print(f"Report saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
