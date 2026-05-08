"""Run DeepEval evaluation against the RAG pipeline."""
from __future__ import annotations

import json
import os
import sys
import re
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Point DeepEval at Groq's OpenAI-compatible endpoint
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if GROQ_API_KEY:
    os.environ["OPENAI_API_KEY"] = GROQ_API_KEY
    os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

import httpx

API_URL = os.getenv("API_URL", "http://localhost:8080")
DATASET_PATH = Path(__file__).parent / "dataset.json"
RESULTS_PATH = Path(__file__).parent / "results"

JUDGE_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def sanitize_model_name(name: str) -> str:
    return re.sub(r'[^\w\-.]', '-', name)


def query_rag(question: str, top_k: int = 5) -> dict:
    """Query the RAG API and return the response."""
    resp = httpx.post(
        f"{API_URL}/query",
        json={"question": question, "top_k": top_k},
        timeout=120.0,
    )
    resp.raise_for_status()
    return resp.json()


def collect_responses(dataset: list[dict]) -> list[dict]:
    """Query the RAG pipeline for each question and collect responses."""
    results = []
    for i, item in enumerate(dataset):
        print(f"  [{i+1}/{len(dataset)}] {item['question'][:60]}...")
        try:
            response = query_rag(item["question"])
            results.append({
                **item,
                "actual_answer": response["answer"],
                "retrieved_contexts": [s["text_preview"] for s in response["sources"]],
                "source_details": response["sources"],
                "model": response["model"],
                "provider": response["provider"],
            })
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({
                **item,
                "actual_answer": f"ERROR: {e}",
                "retrieved_contexts": [],
                "source_details": [],
                "model": "unknown",
                "provider": "unknown",
            })
        time.sleep(5)
    return results


def run_deepeval_metrics(results: list[dict]) -> list[dict]:
    """Run DeepEval metrics on collected results."""
    try:
        from deepeval.metrics import (
            AnswerRelevancyMetric,
            ContextualPrecisionMetric,
            ContextualRecallMetric,
            FaithfulnessMetric,
            GEval,
        )
        from deepeval.test_case import LLMTestCase, LLMTestCaseParams
    except ImportError:
        print("DeepEval not installed. Install with: pip install -r requirements-eval.txt")
        print("Falling back to manual metric computation...")
        return run_manual_metrics(results)

    correctness_metric = GEval(
        name="Answer Correctness",
        criteria="Determine if the actual output matches the expected output in meaning and factual accuracy.",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        model=JUDGE_MODEL,
    )

    faithfulness = FaithfulnessMetric(model=JUDGE_MODEL)
    relevancy = AnswerRelevancyMetric(model=JUDGE_MODEL)
    ctx_precision = ContextualPrecisionMetric(model=JUDGE_MODEL)
    ctx_recall = ContextualRecallMetric(model=JUDGE_MODEL)

    evaluated = []
    for i, r in enumerate(results):
        print(f"  Evaluating [{i+1}/{len(results)}] {r['question'][:50]}...")
        if r["actual_answer"].startswith("ERROR"):
            evaluated.append({**r, "scores": {"error": "Query failed"}})
            continue

        test_case = LLMTestCase(
            input=r["question"],
            actual_output=r["actual_answer"],
            expected_output=r["ground_truth_answer"],
            retrieval_context=r["retrieved_contexts"] if r["retrieved_contexts"] else ["No context retrieved."],
        )

        scores = {}
        metrics = [
            ("faithfulness", faithfulness),
            ("answer_relevancy", relevancy),
            ("context_precision", ctx_precision),
            ("context_recall", ctx_recall),
            ("answer_correctness", correctness_metric),
        ]

        for name, metric in metrics:
            try:
                metric.measure(test_case)
                scores[name] = metric.score
            except Exception as e:
                print(f"    {name} failed: {e}")
                scores[name] = None
            time.sleep(10)

        evaluated.append({**r, "scores": scores})
        print(f"    Scores: {scores}")

    return evaluated


def run_manual_metrics(results: list[dict]) -> list[dict]:
    """Fallback: compute simple metrics without DeepEval."""
    evaluated = []
    for r in results:
        if r["actual_answer"].startswith("ERROR"):
            evaluated.append({**r, "scores": {"error": "Query failed"}})
            continue

        has_context = len(r["retrieved_contexts"]) > 0
        answer_lower = r["actual_answer"].lower()
        truth_lower = r["ground_truth_answer"].lower()

        is_no_answer = r["category"] == "no-answer"
        says_no_info = any(phrase in answer_lower for phrase in [
            "don't have enough information",
            "not available",
            "cannot find",
            "no information",
            "i don't know",
        ])

        if is_no_answer:
            correctness = 1.0 if says_no_info else 0.0
            faithfulness = 1.0 if says_no_info else 0.3
        else:
            key_terms = set(truth_lower.split()) - {"the", "a", "is", "are", "of", "to", "and", "in", "for"}
            answer_terms = set(answer_lower.split())
            overlap = len(key_terms & answer_terms) / max(len(key_terms), 1)
            correctness = min(overlap * 1.5, 1.0)
            faithfulness = 0.8 if has_context else 0.2

        scores = {
            "faithfulness": round(faithfulness, 3),
            "answer_relevancy": round(0.8 if has_context else 0.3, 3),
            "context_precision": round(0.7 if has_context else 0.0, 3),
            "context_recall": round(0.6 if has_context else 0.0, 3),
            "answer_correctness": round(correctness, 3),
        }

        evaluated.append({**r, "scores": scores})

    return evaluated


def main():
    print("Loading evaluation dataset...")
    dataset = json.loads(DATASET_PATH.read_text())
    print(f"  {len(dataset)} questions loaded\n")

    print("Step 1: Collecting RAG responses...")
    results = collect_responses(dataset)

    gen_models = {r["model"] for r in results if r["model"] != "unknown"}
    gen_model = gen_models.pop() if len(gen_models) == 1 else "mixed"
    gen_slug = sanitize_model_name(gen_model)
    judge_slug = sanitize_model_name(JUDGE_MODEL)
    file_tag = gen_slug if gen_slug == judge_slug else f"{gen_slug}--{judge_slug}"

    RESULTS_PATH.mkdir(exist_ok=True)
    responses_file = RESULTS_PATH / f"raw_responses-{file_tag}.json"
    payload = {
        "metadata": {"generation_model": gen_model, "judge_model": JUDGE_MODEL},
        "results": results,
    }
    responses_file.write_text(json.dumps(payload, indent=2))
    print(f"  Responses saved to {responses_file}")

    print("\nWaiting 60 seconds for Groq rate limit to reset...")
    time.sleep(60)

    print("\nStep 2: Running evaluation metrics...")
    evaluated = run_deepeval_metrics(results)

    output_file = RESULTS_PATH / f"eval_results-{file_tag}.json"
    payload = {
        "metadata": {"generation_model": gen_model, "judge_model": JUDGE_MODEL},
        "results": evaluated,
    }
    output_file.write_text(json.dumps(payload, indent=2))
    print(f"\nResults saved to {output_file}")

    print("\n--- Aggregate Scores ---")
    metric_names = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "answer_correctness"]
    for metric in metric_names:
        scores = [r["scores"].get(metric) for r in evaluated if r["scores"].get(metric) is not None]
        if scores:
            avg = sum(scores) / len(scores)
            print(f"  {metric}: {avg:.3f} (n={len(scores)})")
        else:
            print(f"  {metric}: N/A")


if __name__ == "__main__":
    main()
