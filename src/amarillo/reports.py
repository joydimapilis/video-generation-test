from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, read_jsonl


def write_report(
    report_path: Path,
    sample_manifest_path: Path,
    prompt_library_path: Path,
    run_plan_path: Path,
    results_path: Path,
    scoreboard_path: Path,
) -> str:
    samples = read_json(sample_manifest_path) if sample_manifest_path.exists() else []
    patterns = read_json(prompt_library_path) if prompt_library_path.exists() else []
    plan = read_json(run_plan_path) if run_plan_path.exists() else {"runs": [], "total_estimated_cost_usd": 0}
    results = read_jsonl(results_path)
    scoreboard = read_json(scoreboard_path) if scoreboard_path.exists() else []
    recommendations_path = Path("artifacts/recommendations/latest.json")
    recommendations = read_json(recommendations_path) if recommendations_path.exists() else {"recommendations": []}
    brief_plan_path = Path("artifacts/brief_plans/latest.json")
    brief_plan = read_json(brief_plan_path) if brief_plan_path.exists() else None
    assembled_outputs = read_assembled_outputs(Path("assembled_outputs"))
    evaluation_path = Path("artifacts/evaluations/latest.json")
    evaluation = read_json(evaluation_path) if evaluation_path.exists() else None
    comparison_path = Path("artifacts/reference_comparisons/latest.json")
    comparison = read_json(comparison_path) if comparison_path.exists() else None
    review_pack_path = Path("artifacts/review_pack/latest.json")
    review_pack = read_json(review_pack_path) if review_pack_path.exists() else None
    lines = [
        "# Amarillo Milestone Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        "",
        f"- Samples ingested: {len(samples)}",
        f"- Prompt patterns: {len(patterns)}",
        f"- Latest planned model runs: {len(plan.get('runs', []))}",
        f"- Latest planned estimated spend: ${float(plan.get('total_estimated_cost_usd', 0)):.2f}",
        f"- Result records: {len(results)}",
        f"- Cumulative logged estimated spend: ${sum(float(row.get('estimated_cost_usd', 0)) for row in results):.2f}",
        "",
        "## Current Status",
        "",
    ]
    if not samples:
        lines.append("No reference videos have been added yet. Drop `.mp4`, `.mov`, `.webm`, `.mkv`, or `.avi` files into `data/samples/` and rerun ingestion.")
    elif not results:
        lines.append("Samples and prompts exist, but no model runs have been logged yet.")
    else:
        lines.append("The experiment pipeline has produced run logs and a preliminary scoreboard.")
    lines.extend(["", "## Scoreboard", ""])
    if scoreboard:
        lines.extend(["| Run | Model | Status | Est. Cost | Pre-review | Quality | Final |", "| --- | --- | --- | ---: | ---: | ---: | ---: |"])
        for row in scoreboard:
            lines.append(
                f"| `{row['run_id']}` | `{row['model_id']}` | {row['status']} | "
                f"${float(row['estimated_cost_usd']):.2f} | {row['score_pre_review']} | "
                f"{row.get('quality_score', 'n/a')} | {row.get('score_final', 'n/a')} |"
            )
        reviewed = [row for row in scoreboard if row.get("review_notes")]
        if reviewed:
            lines.extend(["", "## Review Notes", ""])
            for row in reviewed:
                lines.append(f"- `{row['model_id']}`: {row['review_notes']}")
    else:
        lines.append("No scored runs yet.")
    if recommendations.get("recommendations"):
        lines.extend(["", "## Recommendations", ""])
        lines.extend(["| Shot Type | Recommended Model | Score | Guidance |", "| --- | --- | ---: | --- |"])
        for rec in recommendations["recommendations"]:
            lines.append(
                f"| `{rec['shot_type']}` | `{rec['recommended_model']}` | "
                f"{rec['score']} | {rec['runner_guidance']} |"
            )
    if brief_plan:
        lines.extend(
            [
                "",
                "## Latest Brief Plan",
                "",
                f"- Brief: {brief_plan['brief']}",
                f"- Selected variant: `{brief_plan['selected_variant_id']}`",
                f"- Recommended model: `{brief_plan['recommended_model']}`",
                f"- Tool chain: {', '.join(brief_plan['tool_chain'])}",
            ]
        )
    if Path("hyperframes/cero-overlay/index.html").exists():
        lines.extend(
            [
                "",
                "## HyperFrames Prototype",
                "",
                "- Project: `hyperframes/cero-overlay/`",
                "- Preview URL when server is running: `http://localhost:3017/#project/cero-overlay`",
                "- Purpose: combine winning generated plates with deterministic brand, reward, and phone UI overlays.",
            ]
        )
    if assembled_outputs:
        lines.extend(["", "## Assembled Outputs", ""])
        for output in assembled_outputs:
            lines.extend(
                [
                    f"- `{output['output_id']}`: {output['output_path']}",
                    f"  {output['quality_notes']}",
                ]
            )
    if Path("artifacts/output_manifest/latest.md").exists():
        lines.extend(
            [
                "",
                "## Output Index",
                "",
                "- Unified output manifest: `artifacts/output_manifest/latest.md`",
            ]
        )
    if evaluation:
        lines.extend(
            [
                "",
                "## Technical Evaluation",
                "",
                f"- Evaluated videos: {evaluation['evaluated_count']}",
                f"- Warnings: {len(evaluation['warnings'])}",
                "- Full evaluation: `artifacts/evaluations/latest.md`",
            ]
        )
    if comparison:
        top_match = comparison["comparisons"][0] if comparison.get("comparisons") else None
        lines.extend(
            [
                "",
                "## Reference Comparison",
                "",
                f"- Compared videos: {comparison['comparison_count']}",
                "- Full comparison: `artifacts/reference_comparisons/latest.md`",
            ]
        )
        if top_match:
            lines.append(
                f"- Highest automated reference similarity: `{top_match['id']}` "
                f"({top_match['reference_similarity_score']})"
            )
    if review_pack:
        lines.extend(
            [
                "",
                "## Review Pack",
                "",
                f"- Review videos: {review_pack['entry_count']}",
                "- Human review page: `artifacts/review_pack/latest.html`",
                "- Review summary: `artifacts/review_pack/latest.md`",
            ]
        )
    if Path("artifacts/knowledge/latest.md").exists():
        lines.extend(
            [
                "",
                "## Knowledge Base",
                "",
                "- Consolidated AI-readable evidence pack: `artifacts/knowledge/latest.json`",
                "- Human summary: `artifacts/knowledge/latest.md`",
            ]
        )
    lines.extend(["", "## Next Actions", ""])
    if results:
        lines.extend(
            [
                "1. Review the generated MP4s in `artifacts/outputs/` or the HTML gallery at `artifacts/reports/latest.html`.",
                "2. Use `kling_3_pro_t2v` as the current default for this reward-app montage pattern.",
                "3. Use the HyperFrames prototype in `hyperframes/cero-overlay/` for controlled UI/text overlays before treating generated app screens as production-ready.",
                "4. Add more samples from different shot families to widen the prompt library and model-selection rules.",
            ]
        )
    else:
        lines.extend(
            [
                "1. Add real reference videos to `data/samples/`.",
                "2. Run `python3 -m amarillo.cli ingest --samples data/samples`.",
                "3. Run `python3 -m amarillo.cli analyze && python3 -m amarillo.cli build-prompts`.",
                "4. Review `prompt_library/patterns.json` for the first prompt patterns.",
                "5. Run a dry model plan, then selected live Fal runs under a small budget cap.",
            ]
        )
    body = "\n".join(lines) + "\n"
    ensure_dir(report_path.parent)
    report_path.write_text(body, encoding="utf-8")
    latest = report_path.parent / "latest.md"
    latest.write_text(body, encoding="utf-8")
    write_gallery(report_path.parent / "latest.html", scoreboard, results, assembled_outputs)
    return body


def read_assembled_outputs(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [read_json(file_path) for file_path in sorted(path.glob("*.json"))]


def write_gallery(
    path: Path,
    scoreboard: list[dict[str, Any]],
    results: list[dict[str, Any]],
    assembled_outputs: list[dict[str, Any]] | None = None,
) -> None:
    records = {record["run_id"]: record for record in results}
    cards = []
    for output in assembled_outputs or []:
        output_path = output.get("output_path")
        video = f'<video controls src="../../{output_path}"></video>' if output_path and Path(output_path).exists() else "<p>No local video file found.</p>"
        cards.append(
            "\n".join(
                [
                    '<article class="card featured">',
                    f"<h2>{output['output_id']} · {output['tool']}</h2>",
                    video,
                    f"<p><strong>Recommended use:</strong> {output.get('recommended_use', '')}</p>",
                    f"<p>{output.get('quality_notes', '')}</p>",
                    "</article>",
                ]
            )
        )
    for row in scoreboard:
        run_id = row["run_id"]
        output_path = output_for_run(run_id, records.get(run_id, {}))
        video = f'<video controls src="../../{output_path}"></video>' if output_path else "<p>No local video file found.</p>"
        cards.append(
            "\n".join(
                [
                    '<article class="card">',
                    f"<h2>{row['model_id']}</h2>",
                    video,
                    f"<p><strong>Final score:</strong> {row.get('score_final', 'n/a')} "
                    f"<strong>Quality:</strong> {row.get('quality_score', 'n/a')} "
                    f"<strong>Cost:</strong> ${float(row['estimated_cost_usd']):.2f}</p>",
                    f"<p>{row.get('review_notes', '')}</p>",
                    "</article>",
                ]
            )
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Amarillo Review Gallery</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f7f8; color: #171a1c; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px; }}
    h1 {{ font-size: 28px; margin: 0 0 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px; }}
    .card {{ background: white; border: 1px solid #dfe3e6; border-radius: 8px; padding: 14px; }}
    .featured {{ grid-column: 1 / -1; }}
    h2 {{ font-size: 17px; margin: 0 0 10px; }}
    video {{ width: 100%; aspect-ratio: 16 / 9; background: #111; display: block; }}
    p {{ font-size: 14px; line-height: 1.45; }}
  </style>
</head>
<body>
  <main>
    <h1>Amarillo Review Gallery</h1>
    <section class="grid">
      {''.join(cards)}
    </section>
  </main>
</body>
</html>
"""
    ensure_dir(path.parent)
    path.write_text(html, encoding="utf-8")


def output_for_run(run_id: str, record: dict[str, Any]) -> str | None:
    recorded = record.get("output_path")
    if recorded and Path(recorded).exists():
        return recorded
    candidate = Path("artifacts/outputs") / f"{run_id}.mp4"
    if candidate.exists():
        return str(candidate)
    return None
