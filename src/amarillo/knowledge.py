from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def build_knowledge_base(output_path: Path) -> dict[str, Any]:
    document = {
        "purpose": "Compact evidence pack for selecting, adapting, and combining video prompts and generation tools.",
        "prompt_patterns": load_optional_json(Path("prompt_library/patterns.json"), []),
        "model_catalog": load_optional_json(Path("catalog/fal_video_models.json"), []),
        "scoreboard": load_optional_json(Path("artifacts/scoreboards/latest.json"), []),
        "recommendations": load_optional_json(Path("artifacts/recommendations/latest.json"), {"recommendations": []}),
        "outputs": load_optional_json(Path("artifacts/output_manifest/latest.json"), {"outputs": []}),
        "technical_evaluations": load_optional_json(Path("artifacts/evaluations/latest.json"), {"evaluations": []}),
        "reference_comparisons": load_optional_json(Path("artifacts/reference_comparisons/latest.json"), {"comparisons": []}),
        "review_pack": load_optional_json(Path("artifacts/review_pack/latest.json"), {"entries": []}),
        "model_selection_rules": Path("docs/MODEL_SELECTION_RULES.md").read_text(encoding="utf-8")
        if Path("docs/MODEL_SELECTION_RULES.md").exists()
        else "",
        "usage_guidance": [
            "Use prompt_patterns for reusable creative structure and prompt slots.",
            "Use recommendations before selecting a model for a known shot type.",
            "Use scoreboard and technical_evaluations to understand quality, cost, latency, and resolution tradeoffs.",
            "Use HyperFrames when generated video text, app UI, counters, overlays, or edit timing must be deterministic.",
            "Avoid copying exact source brands or copyrighted executions unless those assets are supplied and authorized.",
        ],
    }
    write_json(output_path, document)
    write_markdown(output_path.with_suffix(".md"), document)
    latest = output_path.parent / "latest.json"
    write_json(latest, document)
    write_markdown(output_path.parent / "latest.md", document)
    return document


def load_optional_json(path: Path, fallback: Any) -> Any:
    return read_json(path) if path.exists() else fallback


def write_markdown(path: Path, document: dict[str, Any]) -> None:
    lines = [
        "# Amarillo Knowledge Base",
        "",
        document["purpose"],
        "",
        "## Counts",
        "",
        f"- Prompt patterns: {len(document['prompt_patterns'])}",
        f"- Models cataloged: {len(document['model_catalog'])}",
        f"- Scored runs: {len(document['scoreboard'])}",
        f"- Recommendation groups: {len(document['recommendations'].get('recommendations', []))}",
        f"- Outputs indexed: {len(document['outputs'].get('outputs', []))}",
        f"- Technical evaluations: {len(document['technical_evaluations'].get('evaluations', []))}",
        f"- Reference comparisons: {len(document['reference_comparisons'].get('comparisons', []))}",
        f"- Review pack entries: {len(document['review_pack'].get('entries', []))}",
        "",
        "## Current Recommendations",
        "",
        "| Shot Type | Model | Score | Guidance |",
        "| --- | --- | ---: | --- |",
    ]
    for rec in document["recommendations"].get("recommendations", []):
        lines.append(
            f"| `{rec['shot_type']}` | `{rec['recommended_model']}` | "
            f"{rec['score']} | {rec['runner_guidance']} |"
        )
    lines.extend(["", "## Best Outputs", ""])
    lines.append("| Variant | Model/Tool | Score | Output |")
    lines.append("| --- | --- | ---: | --- |")
    for output in document["outputs"].get("best_outputs", []):
        lines.append(
            f"| `{output.get('variant_id')}` | `{output.get('model_id')}` | "
            f"{output.get('score_final')} | `{output.get('output_path')}` |"
        )
    lines.extend(["", "## Usage Guidance", ""])
    lines.extend(f"- {item}" for item in document["usage_guidance"])
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
