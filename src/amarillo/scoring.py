from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json, read_jsonl, write_json


SCORE_WEIGHTS = {
    "completed": 20,
    "prompt_reusability": 20,
    "mode_fit": 15,
    "cost_efficiency": 15,
    "technical_availability": 10,
    "needs_human_review": 20,
}


def score_results(results_path: Path, scoreboard_path: Path) -> list[dict[str, Any]]:
    records = read_jsonl(results_path)
    reviews = load_review_notes(Path("review_notes"))
    scored = [score_record(record, reviews.get(record["run_id"])) for record in records]
    write_json(scoreboard_path, scored)
    return scored


def load_review_notes(notes_dir: Path) -> dict[str, dict[str, Any]]:
    if not notes_dir.exists():
        return {}
    reviews: dict[str, dict[str, Any]] = {}
    for path in sorted(notes_dir.glob("*.json")):
        document = read_json(path)
        for run in document.get("runs", []):
            reviews[run["run_id"]] = run
    return reviews


def score_record(record: dict[str, Any], review: dict[str, Any] | None = None) -> dict[str, Any]:
    status = record.get("status")
    cost = float(record.get("estimated_cost_usd", 0.0))
    score = 0
    reasons: list[str] = []
    if status == "completed":
        score += SCORE_WEIGHTS["completed"]
        reasons.append("Fal run completed")
    elif status == "dry_run":
        score += 5
        reasons.append("Dry run only; not visually evaluated")
    else:
        reasons.append(record.get("error", "Run failed"))
    score += SCORE_WEIGHTS["prompt_reusability"]
    reasons.append("Prompt pattern uses slots and reusable structure")
    if cost <= 0.20:
        score += SCORE_WEIGHTS["cost_efficiency"]
        reasons.append("Low estimated cost")
    elif cost <= 0.60:
        score += 8
        reasons.append("Moderate estimated cost")
    score += SCORE_WEIGHTS["technical_availability"]
    reasons.append("Endpoint and payload were represented in run log")
    if status == "completed":
        score += SCORE_WEIGHTS["needs_human_review"] // 2
        reasons.append("Needs human review for visual quality")
    row = {
        "run_id": record["run_id"],
        "variant_id": record.get("variant_id") or infer_variant_id(record["run_id"]),
        "model_id": record["model_id"],
        "endpoint": record["endpoint"],
        "status": status,
        "estimated_cost_usd": cost,
        "score_pre_review": min(score, 100),
        "reasons": reasons,
    }
    if review:
        quality_keys = [
            "prompt_adherence",
            "temporal_coherence",
            "motion_quality",
            "subject_fidelity",
            "artifact_control",
            "commercial_usefulness",
            "pattern_reusability",
        ]
        quality_score = round(
            sum(float(review[key]) for key in quality_keys) / (len(quality_keys) * 10) * 100,
            1,
        )
        row["quality_score"] = quality_score
        row["score_final"] = round((row["score_pre_review"] * 0.35) + (quality_score * 0.65), 1)
        row["review_notes"] = review.get("notes", "")
    return row


def infer_variant_id(run_id: str) -> str | None:
    parts = run_id.split("__")
    if len(parts) >= 3:
        return parts[-2]
    return None
