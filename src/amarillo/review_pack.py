from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, write_json


def build_review_pack(
    output_manifest_path: Path,
    recommendations_path: Path,
    evaluation_path: Path,
    comparison_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    manifest = read_json(output_manifest_path) if output_manifest_path.exists() else {"outputs": []}
    recommendations = read_json(recommendations_path) if recommendations_path.exists() else {"recommendations": []}
    evaluations = read_json(evaluation_path) if evaluation_path.exists() else {"evaluations": []}
    comparisons = read_json(comparison_path) if comparison_path.exists() else {"comparisons": []}
    entries = select_review_entries(manifest, recommendations, evaluations, comparisons)
    document = {
        "purpose": "Compact review pack containing the highest-signal videos to judge progress without inspecting every run.",
        "reference_sample": comparisons.get("reference_sample"),
        "entry_count": len(entries),
        "entries": entries,
        "label_options": ["usable", "needs_iteration", "reject", "rerun_on_stronger_model"],
        "review_questions": [
            "Does the video make the reward-app value clear without needing technical explanation?",
            "Are the phone/payment/UI moments believable enough to keep, or should HyperFrames replace them?",
            "Which shot family should become the next production template: launch hook, checkout proof, full montage, or assembled overlay?",
            "Are any cheap exploration outputs interesting enough to re-run on a stronger model?",
        ],
    }
    write_json(output_path, document)
    write_markdown(output_path.with_suffix(".md"), document)
    latest = output_path.parent / "latest.json"
    write_json(latest, document)
    write_markdown(output_path.parent / "latest.md", document)
    write_html(output_path.parent / "latest.html", document)
    return document


def select_review_entries(
    manifest: dict[str, Any],
    recommendations: dict[str, Any],
    evaluations: dict[str, Any],
    comparisons: dict[str, Any],
) -> list[dict[str, Any]]:
    outputs = manifest.get("outputs", [])
    evaluation_by_id = {row["id"]: row for row in evaluations.get("evaluations", [])}
    comparison_by_id = {row["id"]: row for row in comparisons.get("comparisons", [])}
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()

    for output in outputs:
        if output.get("type") == "assembled_output":
            add_entry(selected, selected_ids, output, "current_best_assembled", evaluation_by_id, comparison_by_id)

    for rec in recommendations.get("recommendations", []):
        output = find_output(outputs, rec.get("shot_type"), rec.get("recommended_model"))
        if output:
            add_entry(selected, selected_ids, output, f"best_{rec['shot_type']}", evaluation_by_id, comparison_by_id)

    for output in manifest.get("best_outputs", []):
        source = find_output_by_path(outputs, output.get("output_path"))
        if source:
            add_entry(selected, selected_ids, source, f"best_{output.get('variant_id')}", evaluation_by_id, comparison_by_id)

    cheap = best_cheap_output(outputs, selected_ids)
    if cheap:
        add_entry(selected, selected_ids, cheap, "best_low_cost_explorer", evaluation_by_id, comparison_by_id)

    selected.sort(key=entry_sort_key)
    return selected


def add_entry(
    selected: list[dict[str, Any]],
    selected_ids: set[str],
    output: dict[str, Any],
    reason: str,
    evaluation_by_id: dict[str, Any],
    comparison_by_id: dict[str, Any],
) -> None:
    identifier = output.get("run_id") or output.get("output_id")
    if not identifier or identifier in selected_ids:
        return
    selected_ids.add(identifier)
    evaluation = evaluation_by_id.get(identifier, {})
    comparison = comparison_by_id.get(identifier, {})
    selected.append(
        {
            "id": identifier,
            "reason": reason,
            "type": output.get("type"),
            "variant_id": variant_label(output),
            "model_or_tool": output.get("model_id") or output.get("tool"),
            "output_path": output.get("output_path"),
            "score_final": output.get("score_final") or output.get("quality_score"),
            "quality_score": output.get("quality_score"),
            "technical_score": evaluation.get("technical_score"),
            "reference_similarity_score": comparison.get("reference_similarity_score"),
            "estimated_cost_usd": output.get("estimated_cost_usd"),
            "review_notes": output.get("review_notes") or output.get("quality_notes"),
            "recommended_use": output.get("recommended_use"),
            "suggested_decision": suggested_decision(output, evaluation, comparison),
        }
    )


def variant_label(output: dict[str, Any]) -> str:
    if output.get("type") == "assembled_output":
        return "assembled_review"
    return output.get("variant_id") or "primary_full_prompt"


def find_output(outputs: list[dict[str, Any]], variant_id: str | None, model_id: str | None) -> dict[str, Any] | None:
    for output in outputs:
        output_variant = output.get("variant_id") or "primary_full_prompt"
        if output_variant == variant_id and output.get("model_id") == model_id:
            return output
    return None


def find_output_by_path(outputs: list[dict[str, Any]], path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    for output in outputs:
        if output.get("output_path") == path:
            return output
    return None


def best_cheap_output(outputs: list[dict[str, Any]], selected_ids: set[str]) -> dict[str, Any] | None:
    candidates = [
        output
        for output in outputs
        if output.get("type") == "fal_generation"
        and (output.get("run_id") not in selected_ids)
        and float(output.get("estimated_cost_usd") or 999) <= 0.25
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda output: float(output.get("score_final") or output.get("quality_score") or 0))


def suggested_decision(output: dict[str, Any], evaluation: dict[str, Any], comparison: dict[str, Any]) -> str:
    if output.get("type") == "assembled_output" and float(output.get("quality_score") or 0) >= 80:
        return "usable"
    score = float(output.get("score_final") or output.get("quality_score") or 0)
    tech = float(evaluation.get("technical_score") or 0)
    similarity = float(comparison.get("reference_similarity_score") or 0)
    cost = float(output.get("estimated_cost_usd") or 999)
    if score >= 75 and tech >= 90:
        return "usable"
    if score >= 65 and similarity >= 70 and tech >= 85:
        return "needs_iteration"
    if score >= 60 and cost <= 0.25:
        return "rerun_on_stronger_model"
    return "reject"


def entry_sort_key(entry: dict[str, Any]) -> tuple[int, float]:
    priority = {
        "current_best_assembled": 0,
        "best_checkout_proof": 1,
        "best_single_shot_launch": 2,
        "best_primary_full_prompt": 3,
        "best_full_montage": 4,
        "best_low_cost_explorer": 5,
    }
    return (priority.get(entry["reason"], 10), -float(entry.get("score_final") or 0))


def write_markdown(path: Path, document: dict[str, Any]) -> None:
    lines = [
        "# Review Pack",
        "",
        document["purpose"],
        "",
        "| Reason | Output | Model/Tool | Variant | Decision | Score | Tech | Reference | File |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for entry in document["entries"]:
        lines.append(
            f"| `{entry['reason']}` | `{entry['id']}` | `{entry['model_or_tool']}` | "
            f"`{entry['variant_id']}` | `{entry['suggested_decision']}` | {entry.get('score_final')} | "
            f"{entry.get('technical_score')} | {entry.get('reference_similarity_score')} | "
            f"`{entry.get('output_path')}` |"
        )
    lines.extend(["", "## Notes", ""])
    for entry in document["entries"]:
        lines.append(f"- `{entry['id']}`: {entry.get('review_notes') or entry.get('recommended_use') or 'No notes.'}")
    lines.extend(["", "## Review Questions", ""])
    lines.extend(f"- {question}" for question in document["review_questions"])
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(path: Path, document: dict[str, Any]) -> None:
    cards = []
    for entry in document["entries"]:
        output_path = entry.get("output_path")
        video = "<p>No local video file found.</p>"
        if output_path and Path(output_path).exists():
            src = html.escape(os.path.relpath(output_path, path.parent))
            video = f'<video controls preload="metadata" src="{src}"></video>'
        cards.append(
            "\n".join(
                [
                    '<article class="card">',
                    f"<div class=\"reason\">{html.escape(entry['reason'].replace('_', ' '))}</div>",
                    f"<h2>{html.escape(entry['model_or_tool'])}</h2>",
                    video,
                    '<dl class="stats">',
                    f"<div><dt>Variant</dt><dd>{html.escape(str(entry['variant_id']))}</dd></div>",
                    f"<div><dt>Score</dt><dd>{html.escape(str(entry.get('score_final')))}</dd></div>",
                    f"<div><dt>Tech</dt><dd>{html.escape(str(entry.get('technical_score')))}</dd></div>",
                    f"<div><dt>Reference</dt><dd>{html.escape(str(entry.get('reference_similarity_score')))}</dd></div>",
                    "</dl>",
                    f"<p><strong>Suggested decision:</strong> {html.escape(entry['suggested_decision'].replace('_', ' '))}</p>",
                    f"<p>{html.escape(str(entry.get('review_notes') or entry.get('recommended_use') or ''))}</p>",
                    "</article>",
                ]
            )
        )
    questions = "\n".join(f"<li>{html.escape(question)}</li>" for question in document["review_questions"])
    reference_html = ""
    reference = document.get("reference_sample")
    if reference and reference.get("source_path") and Path(reference["source_path"]).exists():
        src = html.escape(os.path.relpath(reference["source_path"], path.parent))
        reference_html = f"""
    <section class="reference">
      <div>
        <div class="reason">Reference sample</div>
        <h2>{html.escape(reference['source_path'])}</h2>
      </div>
      <video controls preload="metadata" src="{src}"></video>
    </section>
"""
    html_body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Amarillo Review Pack</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f3f5f7; color: #151719; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px; }}
    header {{ margin-bottom: 18px; }}
    h1 {{ font-size: 30px; margin: 0 0 8px; }}
    .sub {{ max-width: 760px; color: #4d565f; line-height: 1.5; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 18px; }}
    .reference {{ background: #fff; border: 1px solid #dce2e7; border-radius: 8px; padding: 14px; margin-bottom: 18px; }}
    .card {{ background: #fff; border: 1px solid #dce2e7; border-radius: 8px; padding: 14px; }}
    .card:first-child {{ grid-column: 1 / -1; }}
    .reason {{ color: #53616d; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    h2 {{ font-size: 18px; margin: 6px 0 12px; }}
    video {{ width: 100%; aspect-ratio: 16 / 9; background: #111; display: block; }}
    .stats {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; margin: 12px 0; }}
    .stats div {{ border: 1px solid #e1e6ea; border-radius: 6px; padding: 8px; }}
    dt {{ color: #66727d; font-size: 11px; }}
    dd {{ margin: 2px 0 0; font-weight: 650; font-size: 14px; }}
    p, li {{ font-size: 14px; line-height: 1.45; }}
    section.questions {{ margin-top: 20px; background: #fff; border: 1px solid #dce2e7; border-radius: 8px; padding: 16px; }}
    @media (max-width: 700px) {{ main {{ padding: 16px; }} .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Amarillo Review Pack</h1>
      <p class="sub">{html.escape(document['purpose'])}</p>
    </header>
    {reference_html}
    <section class="grid">
      {''.join(cards)}
    </section>
    <section class="questions">
      <h2>Review Questions</h2>
      <ul>{questions}</ul>
    </section>
  </main>
</body>
</html>
"""
    ensure_dir(path.parent)
    path.write_text(html_body, encoding="utf-8")
