from __future__ import annotations

from pathlib import Path
from typing import Any

from .evaluation import frame_metrics, probe_video, sample_frames
from .io import ensure_dir, read_json, write_json


def compare_reference_outputs(
    sample_manifest_path: Path,
    output_manifest_path: Path,
    evaluation_path: Path,
    output_path: Path,
    sample_count: int = 5,
) -> dict[str, Any]:
    samples = read_json(sample_manifest_path) if sample_manifest_path.exists() else []
    output_manifest = read_json(output_manifest_path) if output_manifest_path.exists() else {"outputs": []}
    evaluations = read_json(evaluation_path) if evaluation_path.exists() else {"evaluations": []}
    references = {sample["sample_id"]: build_reference_signature(sample, sample_count) for sample in samples}
    reference = next(iter(references.values()), None)
    evaluation_by_id = {row["id"]: row for row in evaluations.get("evaluations", [])}
    comparisons = []
    if reference:
        for output in output_manifest.get("outputs", []):
            identifier = output.get("run_id") or output.get("output_id")
            evaluation = evaluation_by_id.get(identifier)
            if not evaluation:
                continue
            reference_id = reference_id_for_output(output, list(references))
            if reference_id:
                comparisons.append(compare_output(references[reference_id], evaluation, output))
    comparisons.sort(key=lambda row: row["reference_similarity_score"], reverse=True)
    document = {
        "reference_sample": reference,
        "reference_samples": list(references.values()),
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "method": [
            "Compare average luminance, contrast, and frame-to-frame motion from evenly sampled frames.",
            "Track aspect ratio, resolution, and duration separately so short generated clips are not over-penalized.",
            "Use this as an automated screen only; semantic review notes remain the authority for prompt faithfulness.",
        ],
    }
    write_json(output_path, document)
    write_markdown(output_path.with_suffix(".md"), document)
    latest = output_path.parent / "latest.json"
    write_json(latest, document)
    write_markdown(output_path.parent / "latest.md", document)
    return document


def reference_id_for_output(output: dict[str, Any], sample_ids: list[str]) -> str | None:
    explicit = output.get("source_sample_id")
    if explicit:
        return explicit if explicit in sample_ids else None
    pattern_id = output.get("pattern_id", "")
    for sample_id in sample_ids:
        if pattern_id == f"{sample_id}-pattern":
            return sample_id
        if (output.get("run_id") or "").startswith(f"{sample_id}-pattern__"):
            return sample_id
        if any(Path(plate).name.startswith(f"{sample_id}-pattern__") for plate in output.get("source_plates", [])):
            return sample_id
    return sample_ids[0] if len(sample_ids) == 1 else None


def build_reference_signature(sample: dict[str, Any], sample_count: int) -> dict[str, Any]:
    source_path = Path(sample["source_path"])
    probe = probe_video(source_path)
    frames = sample_frames(source_path, probe["duration_seconds"], sample_count)
    metrics = frame_metrics(frames)
    return {
        "sample_id": sample["sample_id"],
        "source_path": str(source_path),
        "duration_seconds": probe["duration_seconds"],
        "width": probe["width"],
        "height": probe["height"],
        "fps": probe["fps"],
        "avg_luminance": metrics["avg_luminance"],
        "avg_contrast": metrics["avg_contrast"],
        "avg_motion_delta": metrics["avg_motion_delta"],
        "aspect_ratio": aspect_ratio(probe["width"], probe["height"]),
    }


def compare_output(reference: dict[str, Any], evaluation: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    visual_score = visual_similarity_score(reference, evaluation)
    production_score = production_alignment_score(reference, evaluation)
    score = round((visual_score * 0.72) + (production_score * 0.28), 1)
    return {
        "id": evaluation["id"],
        "reference_sample_id": reference["sample_id"],
        "reference_source_path": reference["source_path"],
        "type": evaluation["type"],
        "model_or_tool": evaluation["model_or_tool"],
        "variant_id": output.get("variant_id"),
        "output_path": evaluation["output_path"],
        "reference_similarity_score": score,
        "visual_signature_score": visual_score,
        "production_alignment_score": production_score,
        "metric_deltas": {
            "luminance": round(abs(reference["avg_luminance"] - evaluation["avg_luminance"]), 2),
            "contrast": round(abs(reference["avg_contrast"] - evaluation["avg_contrast"]), 2),
            "motion": round(abs(reference["avg_motion_delta"] - evaluation["avg_motion_delta"]), 2),
        },
        "aspect_match": aspect_ratio(evaluation["width"], evaluation["height"]) == reference["aspect_ratio"],
        "resolution": f"{evaluation['width']}x{evaluation['height']}",
        "duration_seconds": evaluation["duration_seconds"],
        "review_score": output.get("quality_score") or output.get("score_final"),
        "interpretation": interpretation(score),
    }


def visual_similarity_score(reference: dict[str, Any], evaluation: dict[str, Any]) -> float:
    penalties = [
        normalized_delta(reference["avg_luminance"], evaluation["avg_luminance"], 125) * 35,
        normalized_delta(reference["avg_contrast"], evaluation["avg_contrast"], 95) * 30,
        normalized_delta(reference["avg_motion_delta"], evaluation["avg_motion_delta"], 120) * 35,
    ]
    return round(max(0.0, 100 - sum(penalties)), 1)


def production_alignment_score(reference: dict[str, Any], evaluation: dict[str, Any]) -> float:
    score = 100.0
    if aspect_ratio(evaluation["width"], evaluation["height"]) != reference["aspect_ratio"]:
        score -= 20
    if evaluation["width"] < reference["width"] or evaluation["height"] < reference["height"]:
        score -= 15
    if evaluation["duration_seconds"] < 4:
        score -= 20
    elif evaluation["duration_seconds"] < min(8, reference["duration_seconds"] * 0.25):
        score -= 8
    return round(max(0.0, score), 1)


def normalized_delta(a: float, b: float, scale: float) -> float:
    if scale <= 0:
        return 0.0
    return min(abs(a - b) / scale, 1.0)


def aspect_ratio(width: int, height: int) -> str:
    if width <= 0 or height <= 0:
        return "unknown"
    ratio = width / height
    if abs(ratio - (16 / 9)) < 0.03:
        return "16:9"
    if abs(ratio - (9 / 16)) < 0.03:
        return "9:16"
    if abs(ratio - 1) < 0.03:
        return "1:1"
    return f"{width}:{height}"


def interpretation(score: float) -> str:
    if score >= 82:
        return "Strong visual match to the reference signature."
    if score >= 68:
        return "Useful match with visible stylistic or production drift."
    if score >= 50:
        return "Partial match; use mainly for ideation or isolated elements."
    return "Weak automated match; review only if subjective notes indicate promise."


def write_markdown(path: Path, document: dict[str, Any]) -> None:
    lines = [
        "# Reference Comparison",
        "",
        "Automated comparison between the source sample and generated outputs.",
        "",
    ]
    reference = document.get("reference_sample")
    if reference:
        lines.extend(
            [
                f"- Reference: `{reference['source_path']}`",
                f"- Reference metrics: {reference['width']}x{reference['height']}, "
                f"{reference['duration_seconds']}s, luma {reference['avg_luminance']}, "
                f"contrast {reference['avg_contrast']}, motion {reference['avg_motion_delta']}",
                "",
            ]
        )
    lines.extend(
        [
            "| Output | Model/Tool | Variant | Similarity | Visual | Production | Deltas L/C/M | Interpretation |",
            "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in document["comparisons"]:
        deltas = row["metric_deltas"]
        lines.append(
            f"| `{row['id']}` | `{row['model_or_tool']}` | `{row.get('variant_id')}` | "
            f"{row['reference_similarity_score']} | {row['visual_signature_score']} | "
            f"{row['production_alignment_score']} | "
            f"{deltas['luminance']}/{deltas['contrast']}/{deltas['motion']} | {row['interpretation']} |"
        )
    lines.extend(["", "## Method", ""])
    lines.extend(f"- {item}" for item in document["method"])
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
