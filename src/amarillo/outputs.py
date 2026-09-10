from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import ensure_dir, read_json, read_jsonl, write_json
from .reports import read_assembled_outputs


def build_output_manifest(
    results_path: Path,
    scoreboard_path: Path,
    assembled_dir: Path,
    output_path: Path,
) -> dict[str, Any]:
    results = read_jsonl(results_path)
    scores = {row["run_id"]: row for row in read_json(scoreboard_path)} if scoreboard_path.exists() else {}
    generated = []
    for result in results:
        output_file = result.get("output_path") or inferred_output_path(result["run_id"])
        generated.append(
            {
                "type": "fal_generation",
                "run_id": result["run_id"],
                "pattern_id": result.get("pattern_id"),
                "variant_id": result.get("variant_id") or infer_variant(result["run_id"]),
                "model_id": result["model_id"],
                "endpoint": result["endpoint"],
                "status": result["status"],
                "estimated_cost_usd": result.get("estimated_cost_usd"),
                "latency_seconds": result.get("latency_seconds"),
                "output_path": output_file,
                "output_exists": bool(output_file and Path(output_file).exists()),
                "remote_url": remote_video_url(result.get("result")),
                "score_final": scores.get(result["run_id"], {}).get("score_final"),
                "quality_score": scores.get(result["run_id"], {}).get("quality_score"),
                "review_notes": scores.get(result["run_id"], {}).get("review_notes"),
                "prompt": result.get("input", {}).get("prompt"),
            }
        )
    assembled = [
        {
            "type": "assembled_output",
            **output,
            "output_exists": bool(output.get("output_path") and Path(output["output_path"]).exists()),
        }
        for output in read_assembled_outputs(assembled_dir)
    ]
    manifest = {
        "generated_count": len(generated),
        "assembled_count": len(assembled),
        "best_outputs": best_outputs(generated, assembled),
        "outputs": assembled + generated,
    }
    write_json(output_path, manifest)
    write_markdown(output_path.with_suffix(".md"), manifest)
    latest = output_path.parent / "latest.json"
    write_json(latest, manifest)
    write_markdown(output_path.parent / "latest.md", manifest)
    return manifest


def infer_variant(run_id: str) -> str | None:
    parts = run_id.split("__")
    if len(parts) >= 3:
        return parts[-2]
    return None


def remote_video_url(result: Any) -> str | None:
    if isinstance(result, str) and result.startswith("http"):
        return result
    if isinstance(result, dict):
        for key in ["url", "video_url"]:
            value = remote_video_url(result.get(key))
            if value:
                return value
        for child in result.values():
            value = remote_video_url(child)
            if value:
                return value
    if isinstance(result, list):
        for child in result:
            value = remote_video_url(child)
            if value:
                return value
    return None


def inferred_output_path(run_id: str) -> str | None:
    candidate = Path("artifacts/outputs") / f"{run_id}.mp4"
    if candidate.exists():
        return str(candidate)
    return None


def best_outputs(generated: list[dict[str, Any]], assembled: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_by_variant: dict[str, dict[str, Any]] = {}
    for output in generated:
        variant = output.get("variant_id") or "primary_full_prompt"
        current = best_by_variant.get(variant)
        if current is None or float(output.get("score_final") or 0) > float(current.get("score_final") or 0):
            best_by_variant[variant] = output
    best = [
        {
            "variant_id": variant,
            "model_id": output["model_id"],
            "output_path": output.get("output_path"),
            "score_final": output.get("score_final"),
        }
        for variant, output in sorted(best_by_variant.items())
    ]
    for output in assembled:
        best.insert(
            0,
            {
                "variant_id": "assembled_review",
                "model_id": output.get("tool"),
                "output_path": output.get("output_path"),
                "score_final": output.get("quality_score"),
            },
        )
    return best


def write_markdown(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Output Manifest",
        "",
        f"- Fal generations: {manifest['generated_count']}",
        f"- Assembled outputs: {manifest['assembled_count']}",
        "",
        "## Best Outputs",
        "",
        "| Variant | Model/Tool | Score | Output |",
        "| --- | --- | ---: | --- |",
    ]
    for output in manifest["best_outputs"]:
        lines.append(
            f"| `{output.get('variant_id')}` | `{output.get('model_id')}` | "
            f"{output.get('score_final', 'n/a')} | `{output.get('output_path')}` |"
        )
    lines.extend(["", "## All Outputs", ""])
    lines.append("| Type | ID | Model/Tool | Exists | Output |")
    lines.append("| --- | --- | --- | --- | --- |")
    for output in manifest["outputs"]:
        identifier = output.get("run_id") or output.get("output_id")
        model = output.get("model_id") or output.get("tool")
        lines.append(
            f"| {output['type']} | `{identifier}` | `{model}` | "
            f"{output.get('output_exists')} | `{output.get('output_path')}` |"
        )
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
