"""Generate evaluation report from DeepEval results."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
REPORT_DIR = Path(__file__).parent

METRIC_NAMES = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
    "answer_correctness",
]


def sanitize_model_name(name: str) -> str:
    return re.sub(r'[^\w\-.]', '-', name)


def find_latest_results() -> Path:
    candidates = sorted(
        RESULTS_DIR.glob("eval_results-*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    legacy = RESULTS_DIR / "eval_results.json"
    if legacy.exists():
        return legacy
    raise FileNotFoundError("No eval_results file found in results/")


def load_results(path: Path) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "results" in data:
        return data.get("metadata", {}), data["results"]
    return {}, data


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


def is_rate_limited(r: dict) -> bool:
    scores = r.get("scores", {})
    if not isinstance(scores, dict) or "error" in scores:
        return False
    return all(scores.get(m) is None for m in METRIC_NAMES)


def find_failures(results: list[dict]) -> list[dict]:
    failures = []
    for r in results:
        if is_rate_limited(r):
            continue
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


def generate_report(results: list[dict], metadata: dict) -> str:
    aggregates = compute_aggregates(results)
    failures = find_failures(results)
    rate_limited = sum(1 for r in results if is_rate_limited(r))

    lines = []
    lines.append("# RAG Pipeline Evaluation Report\n")

    if metadata:
        gen = metadata.get("generation_model", "unknown")
        judge = metadata.get("judge_model", "unknown")
        lines.append(f"**Generation model**: `{gen}`\n")
        lines.append(f"**Judge model**: `{judge}`\n")

    lines.append("## Aggregate Scores\n")
    if rate_limited > 0:
        lines.append(
            f"> **Note**: {rate_limited} of {len(results)} questions could not be "
            f"evaluated due to API rate limits and are excluded from the scores below.\n"
        )
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
    if rate_limited > 0:
        lines.append(
            f"> {rate_limited} question(s) excluded from failure analysis "
            f"due to API rate limits.\n"
        )
    top_failures = failures[:3]
    if not top_failures:
        lines.append("No significant failures detected.\n")
    else:
        for idx, f in enumerate(top_failures, 1):
            lines.append(f"### Failure Case {idx}\n")
            lines.append(f"**Question**: {f['question']}\n")
            lines.append(f"**Category**: {f.get('category', 'N/A')}\n")
            lines.append(f"**Expected**: {f['ground_truth_answer']}\n")
            lines.append(f"**Got**: {f.get('actual_answer', 'N/A')[:300]}\n")
            scores = f.get("scores", {})
            if isinstance(scores, dict) and "error" not in scores:
                lines.append(f"**Scores**: {json.dumps(scores, indent=2)}\n")
            lines.append("---\n")

    lines.append("## Improvement Suggestions\n")
    lines.append("*Improvement suggestions are written by the authors after analyzing the evaluation results above.*\n")

    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        results_path = Path(sys.argv[1])
    else:
        try:
            results_path = find_latest_results()
        except FileNotFoundError as e:
            print(str(e))
            print("Run eval/run_eval.py first.")
            return

    print(f"Loading results from {results_path}...")
    metadata, results = load_results(results_path)
    print(f"  {len(results)} results loaded")

    gen = metadata.get("generation_model", "unknown")
    judge = metadata.get("judge_model", "unknown")
    gen_slug = sanitize_model_name(gen)
    judge_slug = sanitize_model_name(judge)
    report_tag = gen_slug if gen_slug == judge_slug else f"{gen_slug}--{judge_slug}"
    report_path = REPORT_DIR / f"report-{report_tag}.md"

    print("Generating report...")
    report = generate_report(results, metadata)
    report_path.write_text(report)
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
