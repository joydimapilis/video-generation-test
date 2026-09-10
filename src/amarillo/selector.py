from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def build_recommendations(scoreboard_path: Path, output_path: Path) -> dict[str, Any]:
    scoreboard = read_json(scoreboard_path) if scoreboard_path.exists() else []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scoreboard:
        grouped[row.get("variant_id") or "primary_full_prompt"].append(row)
    recommendations = {
        "recommendations": [
            recommendation_for_group(variant_id, rows)
            for variant_id, rows in sorted(grouped.items())
        ]
    }
    write_json(output_path, recommendations)
    write_markdown(output_path.with_suffix(".md"), recommendations)
    latest = output_path.parent / "latest.json"
    write_json(latest, recommendations)
    write_markdown(output_path.parent / "latest.md", recommendations)
    return recommendations


def recommendation_for_group(variant_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = sorted(rows, key=lambda row: float(row.get("score_final", row.get("score_pre_review", 0))), reverse=True)
    winner = ranked[0]
    return {
        "shot_type": variant_id,
        "recommended_model": winner["model_id"],
        "recommended_endpoint": winner["endpoint"],
        "score": winner.get("score_final", winner.get("score_pre_review")),
        "runner_guidance": runner_guidance(variant_id, winner["model_id"]),
        "evidence": winner.get("review_notes") or "; ".join(winner.get("reasons", [])),
        "alternates": [
            {
                "model_id": row["model_id"],
                "score": row.get("score_final", row.get("score_pre_review")),
                "use_when": alternate_guidance(row),
            }
            for row in ranked[1:]
        ],
    }


def runner_guidance(variant_id: str, model_id: str) -> str:
    if variant_id == "single_shot_launch":
        return "Use a strong launch keyframe and run image-to-video for the opening hook."
    if variant_id == "checkout_proof":
        return "Use a checkout keyframe with image-to-video, then replace phone UI with deterministic overlays."
    if variant_id == "full_montage":
        return "Use text-to-video for a commercial montage candidate; keep prompts specific to avoid structure drift."
    if variant_id == "primary_full_prompt":
        return "Use the longer reverse-engineered prompt when preserving the whole reference structure matters."
    if "wan" in model_id:
        return "Use for cheap exploration before escalating to a premium model."
    return "Use for finalist generation under the current evidence base."


def alternate_guidance(row: dict[str, Any]) -> str:
    model_id = row["model_id"]
    if "wan" in model_id:
        return "Cheap exploration or alternate mood discovery."
    if "i2v" in model_id:
        return "Use when an input image or keyframe is important."
    return "Use when cinematic coherence matters more than cost."


def write_markdown(path: Path, recommendations: dict[str, Any]) -> None:
    lines = ["# Amarillo Recommendations", ""]
    for rec in recommendations["recommendations"]:
        lines.extend(
            [
                f"## {rec['shot_type']}",
                "",
                f"- Recommended model: `{rec['recommended_model']}`",
                f"- Score: {rec['score']}",
                f"- Guidance: {rec['runner_guidance']}",
                f"- Evidence: {rec['evidence']}",
                "",
            ]
        )
        if rec["alternates"]:
            lines.append("| Alternate | Score | Use When |")
            lines.append("| --- | ---: | --- |")
            for alternate in rec["alternates"]:
                lines.append(
                    f"| `{alternate['model_id']}` | {alternate['score']} | {alternate['use_when']} |"
                )
            lines.append("")
    ensure_dir(path.parent)
    path.write_text("\n".join(lines), encoding="utf-8")
