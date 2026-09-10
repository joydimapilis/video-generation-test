from __future__ import annotations

from pathlib import Path
from typing import Any

from .evaluation import evaluate_output_manifest
from .knowledge import build_knowledge_base
from .outputs import build_output_manifest
from .reference_compare import compare_reference_outputs
from .reports import write_report
from .review_pack import build_review_pack
from .scoring import score_results
from .selector import build_recommendations


def refresh_artifacts(sample_count: int = 5) -> dict[str, Any]:
    scoreboard = score_results(Path("artifacts/results/latest.jsonl"), Path("artifacts/scoreboards/latest.json"))
    recommendations = build_recommendations(
        Path("artifacts/scoreboards/latest.json"),
        Path("artifacts/recommendations/latest.json"),
    )
    output_manifest = build_output_manifest(
        Path("artifacts/results/latest.jsonl"),
        Path("artifacts/scoreboards/latest.json"),
        Path("assembled_outputs"),
        Path("artifacts/output_manifest/latest.json"),
    )
    evaluations = evaluate_output_manifest(
        Path("artifacts/output_manifest/latest.json"),
        Path("artifacts/evaluations/latest.json"),
        sample_count,
    )
    comparisons = compare_reference_outputs(
        Path("artifacts/samples/manifest.json"),
        Path("artifacts/output_manifest/latest.json"),
        Path("artifacts/evaluations/latest.json"),
        Path("artifacts/reference_comparisons/latest.json"),
        sample_count,
    )
    review_pack = build_review_pack(
        Path("artifacts/output_manifest/latest.json"),
        Path("artifacts/recommendations/latest.json"),
        Path("artifacts/evaluations/latest.json"),
        Path("artifacts/reference_comparisons/latest.json"),
        Path("artifacts/review_pack/latest.json"),
    )
    knowledge = build_knowledge_base(Path("artifacts/knowledge/latest.json"))
    report = write_report(
        Path("artifacts/reports/latest.md"),
        Path("artifacts/samples/manifest.json"),
        Path("prompt_library/patterns.json"),
        Path("artifacts/run_plans/latest.json"),
        Path("artifacts/results/latest.jsonl"),
        Path("artifacts/scoreboards/latest.json"),
    )
    return {
        "scored_runs": len(scoreboard),
        "recommendation_groups": len(recommendations["recommendations"]),
        "indexed_outputs": len(output_manifest["outputs"]),
        "evaluated_outputs": evaluations["evaluated_count"],
        "reference_comparisons": comparisons["comparison_count"],
        "review_pack_entries": review_pack["entry_count"],
        "knowledge_patterns": len(knowledge["prompt_patterns"]),
        "report_lines": len(report.splitlines()),
    }
